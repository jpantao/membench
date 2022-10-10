#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/time.h>
#include <time.h>
#include <stdbool.h>

#include <linux/hw_breakpoint.h> /* Definition of HW_* constants */
#include <linux/perf_event.h>    /* Definition of PERF_* constants */
#include <sys/syscall.h>         /* Definition of SYS_* constants */
#include <unistd.h>
#include <sys/ioctl.h>

#define DEFAULT_MEMORY_BENCH_SIZE_TO_BENCH  (1024*1024*1024) // In bytes

#define DATA_UNIT_SIZE      sizeof(uint64_t) // In bytes
#define CACHE_LINE_SIZE     64 // In bytes

#define N_OPERATIONS        100000000

bool op_seq, op_rand, op_pregen, op_prefetch, op_csv = false;


static long perf_event_open(struct perf_event_attr *hw_event, pid_t pid, int cpu, int group_fd, unsigned long flags) {
    int ret;
    ret = syscall(__NR_perf_event_open, hw_event, pid, cpu,group_fd, flags);
    return ret;
}


unsigned long time_diff(struct timeval *start, struct timeval *stop) {
    unsigned long sec_res = stop->tv_sec - start->tv_sec;
    unsigned long usec_res = stop->tv_usec - start->tv_usec;
    return 1000000 * sec_res + usec_res;
}

static inline uint64_t access_memory(uint64_t *address){
    uint64_t fake = 0;
    fake += *address;
    return fake;
}

static inline int gen_address(int* seed, int cacheline_size, int access_max){
    return ((rand_r(seed) >> 3) <<3) % access_max;
}

void argparse(int argc, char *argv[]){

    for(int i = 1; i < argc; i++){
        char * token = argv[i];

        if(token[0] != '-')
            continue;
        
        switch (token[1]){
        	case 's':
				op_seq = true; 
            	break;
			case 'r':
				op_rand = true;
            	break;
			case 'g':
				op_pregen = true;
            	break;
			case 'p':
				op_prefetch = true;
            	break;
			case 'c':
				op_csv = true;
            	break;
        	default:
				printf("Uknown option: %s\n", token);
        }
    }

}

int main(int argc, char *argv[]){  
    argparse(argc,argv);

    struct timeval tstart, tend;
    // unsigned int seed = time(NULL);
    unsigned int seed = 0;

    // setup perf_event (for more details: man perf_event_open)
    int fd;
    long long miss_count;
    struct perf_event_attr pe;
    memset(&pe, 0, sizeof(struct perf_event_attr));
    pe.type = PERF_TYPE_HW_CACHE;
    pe.size = sizeof(struct perf_event_attr);
    pe.config = PERF_COUNT_HW_CACHE_LL |
                PERF_COUNT_HW_CACHE_OP_READ << 8 |
                PERF_COUNT_HW_CACHE_RESULT_MISS << 16;
    pe.disabled = 1;
    pe.exclude_kernel = 1;
    pe.exclude_hv = 1;
    
    
    // Initialize data
    int data_size = DEFAULT_MEMORY_BENCH_SIZE_TO_BENCH;
    uint64_t* data =  malloc(data_size);

    memset(data, 0, data_size); 
    
    int cache_line_size = CACHE_LINE_SIZE / DATA_UNIT_SIZE; // 8 positions = 64 bytes
    int access_max = data_size / DATA_UNIT_SIZE;
    
    int iterations, seq_offset, rand_offset, pregen_offset = 0;
    int next_seq_offset, next_rand_offset, next_pregen_offset, pregen_i = 0;

    next_seq_offset = 0;
    next_rand_offset = gen_address(&seed, cache_line_size, access_max); 


    iterations = N_OPERATIONS;

    int* pregen_array;
    if(op_pregen){
        pregen_array = malloc(iterations);
        for(int i=0; i<iterations; i++)
            pregen_array[i] = gen_address(&seed, cache_line_size, access_max);
        next_pregen_offset = pregen_array[pregen_i++];
    }
    
    

    fd = perf_event_open(&pe, 0, -1, -1, 0);
    if (fd == -1) {
        fprintf(stderr, "Error opening leader %llx\n", pe.config);
        exit(EXIT_FAILURE);
    }

    gettimeofday(&tstart, NULL);

    ioctl(fd, PERF_EVENT_IOC_RESET, 0);
    ioctl(fd, PERF_EVENT_IOC_ENABLE, 0);

    for(int i = 0; i < iterations; i++){
        
		if(op_seq){
			seq_offset = next_seq_offset; 
			next_seq_offset = (seq_offset + cache_line_size) % access_max;; 
			if (op_prefetch){
                __builtin_prefetch(data + next_seq_offset);
                //TODO: waitloop
            }
			access_memory(data + seq_offset);
		}
		
		if(op_rand){
			rand_offset = next_rand_offset; 
			next_rand_offset = gen_address(&seed, cache_line_size, access_max); 
			if(op_prefetch){
        	    __builtin_prefetch(data + next_rand_offset);
                //TODO: waitloop
            }
			access_memory(data + rand_offset);
		}

		if(op_pregen){
			pregen_offset = next_pregen_offset;            
			next_pregen_offset = pregen_array[pregen_i++];          
            pregen_i = pregen_i % iterations;
            if(op_prefetch){
                __builtin_prefetch(data + next_pregen_offset);
                //TODO: waitloop
            }
			access_memory(data + pregen_offset);
		}     

    }

    ioctl(fd, PERF_EVENT_IOC_DISABLE, 0);
    gettimeofday(&tend, NULL);

    unsigned long duration = time_diff(&tstart, &tend);
    read(fd, &miss_count, sizeof(long long));

    int tp = iterations/(duration / 1000);

    if(op_csv){
        printf("%ld,%lld\n", tp, miss_count);
    }else {
        printf("troughput: %ld op/ms\n", tp);
        printf("cache_misses: %lld \n", miss_count);
    }
    
    return 0;
}