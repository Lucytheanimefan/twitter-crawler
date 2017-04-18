#
#
# Usage:
#				[Compile with:]
#	make			[g++]	*** default compiler ***
#	make CC=g++		[g++]
#
# Reference : https://www.gnu.org/software/make/manual/html_node/Implicit-Variables.html    # Implicit, default variables
#	    : https://www.cs.duke.edu/courses/spring04/cps108/resources/makefiles/sample.html # Example / Special Macros <, @, ^, +
#           : https://www.cs.swarthmore.edu/~newhall/unixhelp/howto_makefiles.html  # Example2
#           : http://www.cs.colby.edu/maxwell/courses/tutorials/maketutor/    # Special Macros <, @, ^, +


########## Default Compiler

CXX = g++
CC = $(CXX)

########## Machine-specific Setting / Environment Paths

PATH_MATLAB   = /Applications/MATLAB_R2016b.app
ARCH          = maci64
INC          +=	-std=c++11
INC          += -I/auto/pkg/python-2.7.2/include/python2.7
LIB          += -L/auto/pkg/python-2.7.2/lib/python2.7/config

########## Compilation flags
# CFLAGS : C compiler flags
# LFLAGS : Linker flags
# -Wall  : Warning
# -O3    : Optimization level
# -fPIC  : Position-independent
# -Wl    :
# -rpath : 

CFLAGS        = -O3 -fPIC -Wall
LFLAGS        = -lm -Wall
PYFLAGS	      = -lpython2.7

########## Variables
# SRCS   : Source .cpp files
# OBJS   : Object files

SRCS          = main.cpp indexFunc.cpp resourceFunc.cpp viterbi.cpp #C_Implements_Python.cpp 
OBJS          = $(SRCS:%.cpp=%.o)
PROGS         = PROG1 #PROG1 PROG2

########## Compilation Recipes
# all : default rule
# $@  : file name of the target
# $<  : the name of the first dependency
# $+  : the names of the all dependencies

all: $(PROGS) $(OBJS)

PROG1    : main.o indexFunc.o resourceFunc.o viterbi.o
	$(CC) $(INC) -o $@ $+ $(LFLAGS) $(PYFLAGS)
PROG2    : test.o indexFunc.o
	$(CC) $(INC) -o $@ $+ $(LFLAGS)
%.o      : %.cpp
	$(CC) -c $(INC) -o $@ $< $(CFLAGS)

########## Clean-up

.PHONY: clean

clean:
	$(RM) $(PROGS) $(OBJS)
