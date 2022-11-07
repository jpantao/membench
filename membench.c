#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/time.h>
#include <stdbool.h>

#define DEFAULT_MEMORY_BENCH_SIZE_TO_BENCH  (1024*1024*1024) // In bytes
#define DEFAULT_WAITLOOP_ITERATIONS 500 // 1M

#define DATA_UNIT_SIZE      sizeof(uint64_t) // In bytes
#define CACHE_LINE_SIZE     64 // In bytes

#define N_OPERATIONS        100000000


bool op_seq, op_rand, op_pregen, op_prefetch, op_csv = false;
unsigned long waitloop_iterations = DEFAULT_WAITLOOP_ITERATIONS;

void print_usage(char *exec_name) {
    printf("Usage: %s [OPTION]....\n", exec_name);
    printf("Try 'grep -h' for more information.\n");
}

void print_help(char *exec_name) {
    printf("Usage: %s [OPTION]...\n", exec_name);
    printf("Benchmark different kinds of memory accesses.\n");
    printf("\n");
    printf("Access types:\n");
    printf("  -s\t\tsequential memory access\n");
    printf("  -r\t\trandom memory access (generate a random address at 'access time')\n");
    printf("  -g\t\trandom memory access (pre-generate random addresses for all accesses)\n");
    printf("\n");
    printf("Processor cache prefetch options:\n");
    printf("  -p\t\tprefetch data to processor cache before each access (default=do not use prefetch)\n");
    printf("  -w iterations\tnumber of iterations for the waitloop after each prefetch (default=%d)\n",
           DEFAULT_WAITLOOP_ITERATIONS);
    printf("\n");
    printf("Output control:\n");
    printf("  -c\t\toutput in csv format (throughput,cache_misses)\n");
    printf("\n");
    printf("Miscellaneous:\n");
    printf("  -h\t\tprint this message\n");
}

unsigned long time_diff(struct timeval *start, struct timeval *stop) {
    unsigned long sec_res = stop->tv_sec - start->tv_sec;
    unsigned long usec_res = stop->tv_usec - start->tv_usec;
    return 1000000 * sec_res + usec_res;
}

static inline uint64_t access_memory(const uint64_t *address) {
    uint64_t fake = 0;
    fake += *address;
    return fake;
}

static inline int gen_address_CL64(unsigned int *seed, int access_max) {
    return ((rand_r(seed) >> 3) << 3) % access_max;
}

static inline void waitloop(unsigned long iterations) {
    while (iterations--) {
        __asm__ __volatile__("");
    }
}

void argparse(int argc, char *argv[]) {

    for (int i = 1; i < argc; i++) {
        char *token = argv[i];

        if (token[0] != '-')
            continue;

        switch (token[1]) {
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
            case 'w':
                waitloop_iterations = atoi(argv[++i]);
                break;
            case 'h':
                print_help(argv[0]);
                exit(0);
            default:
                printf("Unknown option: %s\n", token);
                print_usage(argv[0]);
                exit(0);
        }
    }

}


int main(int argc, char *argv[]) {
    argparse(argc, argv);

    struct timeval tstart, tend;
    unsigned int seed = 0;

    // Initialize data
    unsigned long data_size = DEFAULT_MEMORY_BENCH_SIZE_TO_BENCH;
    uint64_t *data = malloc(data_size);

    memset(data, 1, data_size);

    int cache_line_size = CACHE_LINE_SIZE / DATA_UNIT_SIZE; // 8 positions = 64 bytes
    unsigned long access_max = data_size / DATA_UNIT_SIZE;

    unsigned long iterations, seq_offset, rand_offset, pregen_offset;

    iterations = N_OPERATIONS;

    int *pregen_array;
    pregen_array = malloc(iterations);
    for (int i = 0; i < iterations; i++)
        pregen_array[i] = gen_address_CL64(&seed, access_max);


    gettimeofday(&tstart, NULL);

//    printf("%lu\n", waitloop_iterations);
    for (int i = 0; i < iterations; i++) {

        if (op_seq) {
            seq_offset = (seq_offset + cache_line_size) % access_max;
            if (op_prefetch) {
                __builtin_prefetch(data + seq_offset);
            }
            waitloop(waitloop_iterations);
            access_memory(data + seq_offset);
        }

        if (op_rand) {
            rand_offset = gen_address_CL64(&seed, access_max);
            if (op_prefetch) {
                __builtin_prefetch(data + rand_offset);
            }
            waitloop(waitloop_iterations);
            access_memory(data + rand_offset);
        }

        if (op_pregen) {
            pregen_offset = pregen_array[i++];
            if (op_prefetch) {
                __builtin_prefetch(data + pregen_offset);
            }
            waitloop(waitloop_iterations);
            access_memory(data + pregen_offset);
        }

    }

    gettimeofday(&tend, NULL);

    unsigned long duration = time_diff(&tstart, &tend);
    unsigned long tp = iterations / (duration / 1000);

    if (op_csv) {
        printf("%ld\n", tp);
    } else {
        printf("throughput: %ld op/ms\n", tp);
    }

    return 0;
}