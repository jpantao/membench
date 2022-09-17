#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/time.h>
#include <time.h>
#include <stdbool.h>

#define DEFAULT_MEMORY_BENCH_SIZE_TO_BENCH  (1024*1024*1024) // In bytes

#define DATA_UNIT_SIZE      sizeof(uint64_t) // In bytes
#define CACHE_LINE_SIZE     64 // In bytes

bool op_seq, op_rand, op_pregen, op_prefetch = false;


unsigned long time_diff(struct timeval *start, struct timeval *stop) {
    unsigned long sec_res = stop->tv_sec - start->tv_sec;
    unsigned long usec_res = stop->tv_usec - start->tv_usec;
    return 1000000 * sec_res + usec_res;
}

void prefetch_memory(uint64_t *address, int size){
    uint64_t fake = 0;
    const void* current;
    for(int i = 0; i < size; i++){
        current = address + i;
        __builtin_prefetch(current);
    }
}

uint64_t access_memory(uint64_t *address, int size){
    uint64_t fake = 0;
    for(int i = 0; i < size; i++){
        fake += *(address+i);
    }
    return fake;
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
        	default:
				printf("Uknown option: %s\n", token);
        }
    }

}

int main(int argc, char *argv[]){  
    argparse(argc,argv);

    struct timeval tstart, tend;
    unsigned int seed = time(NULL);

    // Initialize data
    int data_size = DEFAULT_MEMORY_BENCH_SIZE_TO_BENCH;
    uint64_t* data =  malloc(data_size);
    memset(data, 0, data_size); 
    
    int size_to_access = CACHE_LINE_SIZE / DATA_UNIT_SIZE; // 8 positions = 64 bytes
    int access_max = data_size / DATA_UNIT_SIZE - size_to_access;
    // printf("%d\n", rand_max);
    // printf("%d\n", rand_r(&seed) % rand_max);

    // printf("iterations: %d\n", iterations);
    int iterations, seq_offset, rand_offset, pregen_offset;
    iterations = data_size / DATA_UNIT_SIZE;
    

    gettimeofday(&tstart, NULL);
    for(int i = 0; i < iterations; i++){
      

		if(op_seq){
			seq_offset = i % access_max; // for when iterations > data_size
			if (op_prefetch)
				prefetch_memory(data + seq_offset, size_to_access);
			access_memory(data + seq_offset, size_to_access);
		}
		
		if(op_rand){
			rand_offset = rand_r(&seed) % access_max; 
			if(op_prefetch)
        		prefetch_memory(data + rand_offset, size_to_access);
			access_memory(data + rand_offset, size_to_access);
		}

		if(op_pregen){
			printf("pregen not implemented\n");
			exit(0);
			// pregen_offset =  ;
			// access_memory(data + pregen_offset, size_to_access);
		}

        // access_memory(data + rand_offset, size_to_access);

    }
    gettimeofday(&tend, NULL);

    unsigned long duration = time_diff(&tstart, &tend);

    // printf("duration: %ld ms\n", duration / 1000);
    printf("troughput: %ld op/ms\n", iterations/(duration / 1000));

    return 0;
}
