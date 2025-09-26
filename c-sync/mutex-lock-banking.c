#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <pthread.h>

pthread_mutex_t mutex;

int shared = 0; //shared variable
void *incrementer(void *args) {
    for (int i = 0; i < 100; i++) {
        pthread_mutex_lock(&mutex);
        shared++; //increment
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    pthread_mutex_init(&mutex, NULL);   // init mutex
    pthread_t *threads;
    int n, i;
    if (argc < 2) {
        fprintf(stderr, "ERROR: Invalid number of threads\n");
        exit(1);
    }
    //convert argv[1] to a long
    if ((n = atol(argv[1])) == 0) {
        fprintf(stderr, "ERROR: Invalid number of threads\n");
        exit(1);
    }
    //allocate array of pthread_t identifiers
    threads = calloc(n, sizeof(pthread_t));
    //create n threads
    for (i = 0; i < n; i++) {
        pthread_create(&threads[i], NULL, incrementer, NULL);
    }
    //join all threads
    for (i = 0; i < n; i++) {
        pthread_join(threads[i], NULL);
    }
    //print shared value and result
    printf("Shared: %d\n", shared);
    printf("Expect: %d\n", n * 100);

    pthread_mutex_destroy(&mutex);  // destroy mutex
    return 0;
}
