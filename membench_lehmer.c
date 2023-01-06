#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/time.h>
#include <stdbool.h>

#include <search.h>
#include <math.h>

#define DEFAULT_MEMORY_BENCH_SIZE_TO_BENCH (1024*1024*1024) // In bytes (1GB)
#define DEFAULT_SPINLOOP_ITERATIONS 0

#define DATA_UNIT_SIZE      sizeof(uint64_t) // In bytes = 8
#define CACHE_LINE_SIZE     64 // In bytes

#define N_OPERATIONS        100000000 // 100 million

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
    register uint64_t fake = 0;
    fake += *address;
    return fake;
}

static __inline__ unsigned long time_diff(struct timeval *start, struct timeval *stop) {
    register unsigned long sec_res = stop->tv_sec - start->tv_sec;
    register unsigned long usec_res = stop->tv_usec - start->tv_usec;
    return 1000000 * sec_res + usec_res;
}


// state for splitmix64
uint64_t splitmix64_x; /* The state can be seeded with any value. */

// call this one before calling splitmix64
static inline void splitmix64_seed(uint64_t seed) { splitmix64_x = seed; }

// floor( ( (1+sqrt(5))/2 ) * 2**64 MOD 2**64)
#define GOLDEN_GAMMA UINT64_C(0x9E3779B97F4A7C15)

// returns random number, modifies seed[0]
// compared with D. Lemire against
// http://grepcode.com/file/repository.grepcode.com/java/root/jdk/openjdk/8-b132/java/util/SplittableRandom.java#SplittableRandom.0gamma
static inline uint64_t splitmix64_r(uint64_t *seed) {
    uint64_t z = (*seed += GOLDEN_GAMMA);
    // David Stafford's Mix13 for MurmurHash3's 64-bit finalizer
    z = (z ^ (z >> 30)) * UINT64_C(0xBF58476D1CE4E5B9);
    z = (z ^ (z >> 27)) * UINT64_C(0x94D049BB133111EB);
    return z ^ (z >> 31);
}

// returns random number, modifies splitmix64_x
static inline uint64_t splitmix64(void) {
    return splitmix64_r(&splitmix64_x);
}

// returns the 32 least significant bits of a call to splitmix64
// this is a simple (inlined) function call followed by a cast
static inline uint32_t splitmix64_cast32(void) {
    return (uint32_t)splitmix64();
}

// returns the value of splitmix64 "offset" steps from seed
static inline uint64_t splitmix64_stateless(uint64_t seed, uint64_t offset) {
    seed += offset*GOLDEN_GAMMA;
    return splitmix64_r(&seed);
}

static __uint128_t g_lehmer64_state;

/**
* D. H. Lehmer, Mathematical methods in large-scale computing units.
* Proceedings of a Second Symposium on Large Scale Digital Calculating
* Machinery;
* Annals of the Computation Laboratory, Harvard Univ. 26 (1951), pp. 141-146.
*
* P L'Ecuyer,  Tables of linear congruential generators of different sizes and
* good lattice structure. Mathematics of Computation of the American
* Mathematical
* Society 68.225 (1999): 249-260.
*/

static inline void lehmer64_seed(uint64_t seed) {
    g_lehmer64_state = (((__uint128_t)splitmix64_stateless(seed, 0)) << 64) +
                       splitmix64_stateless(seed, 1);
}

static inline uint64_t lehmer64(void) {
    g_lehmer64_state *= UINT64_C(0xda942042e4dd58b5);
    return g_lehmer64_state >> 64;
}

static inline uint32_t lehmer64_cast32(void) { return (uint32_t)lehmer64(); }

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
    return ((lehmer64_cast32() >> 3) << 3) % access_max;
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


void hcreate_count_repetitions(const int *array, int array_size) {
    printf("val,count\n");

    hcreate(10 * array_size);
    ENTRY item, *found_item;

    for (int i = 0; i < array_size; i++) {
        char str[10];
        sprintf(str, "%d", array[i]);
        item.key = str;
        found_item = hsearch(item, FIND);
        if (found_item == NULL) {
            item.data = (void *) 1UL;
            hsearch(item, ENTER);
        } else {
            size_t val = (size_t) found_item->data + 1;
            found_item->data = (void *) val;
        }
    }

    for (int i = 0; i < array_size; i++) {
        char str[10];
        sprintf(str, "%d", array[i]);
        item.key = str;
        found_item = hsearch(item, FIND);
        if (found_item != NULL) {
            size_t val = (size_t) found_item->data;
            printf("%s,%lu\n", item.key, val);
        }
    }

    hdestroy();
}

void print_array(const int *array, int array_size) {
    printf("val,count\n");
    for (int i = 0; i < array_size; i++) {
        printf("%d,1\n", array[i]);
    }
}

int main(int argc, char *argv[]) {

    // Parse command line arguments
    argparse(argc, argv);

    struct timeval tstart, tend;
    unsigned int seed = 0;
    lehmer64_seed(seed);

    int data_len =
            DEFAULT_MEMORY_BENCH_SIZE_TO_BENCH / DATA_UNIT_SIZE; // Number of positions in the data array = 134,217,728

    // Pregen array initialization
    int *pgn_addr = malloc(N_OPERATIONS * sizeof(int));
    gettimeofday(&tstart, NULL);
    for (register int i = 0; i < N_OPERATIONS; i++) {
        pgn_addr[i] = gen_address_CL64(&seed, data_len);
    }
    gettimeofday(&tend, NULL);
    unsigned long duration = time_diff(&tstart, &tend);
    print_array(pgn_addr, N_OPERATIONS);
//    printf( "Duration: %lu\n", duration);

    //    hcreate_count_repetitions(pgn_addr, N_OPERATIONS);


    return 0;
}
