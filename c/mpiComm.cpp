//
//  mpiComm.cpp
//  
//
//
//
//

/* Reference :
 1. http://mpitutorial.com/tutorials/mpi-hello-world/ : mpi cod example / mpicc
 2. https://www.open-mpi.org/faq/?category=rsh : avoid password prompt
 2-1. http://linuxcommand.org/lts0070.php : change file/directory permissions
 3. https://www.open-mpi.org/faq/?category=running#mpirun-specify-hosts : running mpi program / mpirun
 4. Run SPMD : mpirun --hostfile clusters -np 4 ./a.out
 4-1. compile : mpiCC mpiComm.cpp -std=c++11
 5. Run MPMD : mpirun -np 2 a.out : -np 2 b.out
 */

#include "mpi.h"
#include "header.hpp"


int main(int argc, char* argv[]){
    
    // Initialize the MPI environment
    MPI_Init(NULL, NULL);
    
    // Get the number of processes
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);
    
    // Get the rank of the process
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    
    // Get the name of the processor
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);
    
    // Print off a hello world message
    printf("Hello world from processor %s, rank %d"
           " out of %d processors\n",
           processor_name, world_rank, world_size);
    
    // Finalize the MPI environment.
    MPI_Finalize();
    
    return 0;
}
