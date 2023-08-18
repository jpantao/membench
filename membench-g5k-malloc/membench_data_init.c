#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/time.h>
#include <stdbool.h>

#define DEFAULT_MEMORY_BENCH_SIZE_TO_BENCH (1024*1024*1024) // In bytes (1GB)
#define DEFAULT_SPINLOOP_ITERATIONS 0
#define DEFAULT_N_OPERATIONS 100000000 // Number of operations to perform = 100M

#define DATA_UNIT_SIZE      sizeof(uint64_t) // In bytes = 8
#define CACHE_LINE_SIZE     64 // In bytes

bool op_seq, op_rand, op_pregen, op_prefetch, op_csv = false;
int spinloop_iterations = DEFAULT_SPINLOOP_ITERATIONS;
int n_operations = DEFAULT_N_OPERATIONS; // Number of operations to perform = 0
int pgn_len = DEFAULT_N_OPERATIONS;

// TODO: update message to reflect the new options (-o)
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
    printf("Try 'membench -h' for more information.\n");
}

static __inline__ uint64_t access_memory(register uint64_t *address) {
    register uint64_t fake = 333333;
    fake += *address;
    return fake;
}

/**
 * @param start
 * @param stop
 * @return time difference in microseconds
 */
static __inline__ unsigned long time_diff(struct timeval *start, struct timeval *stop) {
    register unsigned long sec_res = stop->tv_sec - start->tv_sec;
    register unsigned long usec_res = stop->tv_usec - start->tv_usec;
    return 1000000 * sec_res + usec_res;
}

/**
 * Generate random addresses (i.e., array positions). The function takes a seed and the length of the array as
 * arguments. The seed is used to initialize the random number generator, and the length of the array is used to
 * generate random numbers between 0 and the length of the array. Furthermore, the function ensures that the
 * generated addresses are aligned to cache lines, i.e., that the addresses are multiples of 8.
 * @param seed
 * @param access_max
 * @return
 */
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
            case 'o':
                n_operations = atoi(argv[++i]);
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

    // If no access type is specified, use sequential access by default
    if (!op_seq && !op_rand && !op_pregen) {
        op_seq = true;
    }

    // Check if the user has selected at least one access type
    if ((op_seq && op_rand) || (op_seq && op_pregen) || (op_rand && op_pregen)) {
        printf("Only one access type can be specified.\n");
        print_usage(argv[0]);
        exit(0);
    }

}

int main(int argc, char *argv[]) {

    // Parse command line arguments
    argparse(argc, argv);

    // Runtime variable declarations and initialization
    struct timeval tstart, tend;
    unsigned int seed = 0;

    struct timeval spinloop_tstart, spinloop_tend;
    register double total_spinloop_duration = 0;
    register int offset = 0;

    int data_size = DEFAULT_MEMORY_BENCH_SIZE_TO_BENCH; // In bytes
    int data_len =
            DEFAULT_MEMORY_BENCH_SIZE_TO_BENCH / DATA_UNIT_SIZE; // Number of positions in the data array = 134,217,728
    int cache_line_size = CACHE_LINE_SIZE / DATA_UNIT_SIZE; // Number of data array positions per cache line

    uint64_t access_1 = gen_address_CL64(&seed, data_len);
    int access_2 = gen_address_CL64(&seed, data_len);

    // Data initialization
    uint64_t *data = malloc(data_size);
    access_1 += data[gen_address_CL64(&seed, data_len)];
//    for (register int i = 0; i < data_len; i++) {
//        data[i] = gen_address_CL64(&seed, data_len);
//    }

    // print access_1 to prevent compiler from optimizing it away
    printf("access_1: %lu\n", access_1);

    return 0;
}
