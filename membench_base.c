#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/time.h>
#include <stdbool.h>

#define DEFAULT_MEMORY_BENCH_SIZE_TO_BENCH (1024*1024*1024) // In bytes (1GB)
#define DEFAULT_SPINLOOP_ITERATIONS 0

#define DATA_UNIT_SIZE      sizeof(uint64_t) // In bytes
#define CACHE_LINE_SIZE     64 // In bytes

#define N_OPERATIONS        100000000

bool op_seq, op_rand, op_pregen, op_prefetch, op_csv = false;
int spinloop_iterations = DEFAULT_SPINLOOP_ITERATIONS;

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
    printf("  -w iterations\tnumber of iterations for the spinloop after each prefetch (default=%d)\n",
           DEFAULT_SPINLOOP_ITERATIONS);
    printf("\n");
    printf("Output control:\n");
    printf("  -c\t\toutput in csv format (throughput,cache_misses)\n");
    printf("\n");
    printf("Miscellaneous:\n");
    printf("  -h\t\tprint this message\n");
}

void print_usage(char *exec_name) {
    printf("Usage: %s [OPTION]....\n", exec_name);
    printf("Try 'grep -h' for more information.\n");
}

static __inline__ uint64_t access_memory(register uint64_t *address) {
    register uint64_t fake = 33333;
    fake += *address;
    return fake;
}

static __inline__ unsigned long time_diff(struct timeval *start, struct timeval *stop) {
    register unsigned long sec_res = stop->tv_sec - start->tv_sec;
    register unsigned long usec_res = stop->tv_usec - start->tv_usec;
    return 1000000 * sec_res + usec_res;
}

static __inline__ int gen_address_CL64(register unsigned int *seed, register int access_max) {
    return ((rand_r(seed) >> 3) << 3) % access_max;
}

static __inline__ void spinloop(register int iterations) {
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
                spinloop_iterations = atoi(argv[++i]);
                break;
            case 'h':
                print_help(argv[0]);
                exit(0);
            default:
                printf("Unknown option: %s\n", token);
                print_usage(argv[0]);
                exit(0);
        }

        if ((op_seq && op_rand) || (op_seq && op_pregen) || (op_rand && op_pregen)) {
            printf("Only one access type can be specified.\n");
            print_usage(argv[0]);
            exit(0);
        }
    }

}

int main(int argc, char *argv[]) {

    // Parse command line arguments
    argparse(argc, argv);

    // Runtime variable declarations and initialization
    struct timeval tstart, tend;
    unsigned int seed = 0;

    struct timeval spinloop_tstart, spinloop_tend;
    register unsigned long spinloop_duration = 0;
    register int offset = 0;

    int data_size = DEFAULT_MEMORY_BENCH_SIZE_TO_BENCH; // In bytes
    int data_len = DEFAULT_MEMORY_BENCH_SIZE_TO_BENCH / DATA_UNIT_SIZE; // Number of positions in the data array
    int cache_line_size = CACHE_LINE_SIZE / DATA_UNIT_SIZE; // Number of data array positions per cache line

    // Data initialization

    // Pregen array initialization

    // Main loop

    // Output

    return 0;
}