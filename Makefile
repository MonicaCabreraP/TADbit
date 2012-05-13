OBJECTS= tadbit.o main.o tadbit_R.o tadbit_R.so tadbit

all: tadbit tadbit_R.so

clean:
	- rm -f $(OBJECTS)

tadbit_R.so: tadbit.o tadbit_R.c
	R CMD SHLIB tadbit_R.c tadbit.o

tadbit: tadbit.o main.o
	- rm -f tadbit
	gcc -std=gnu99 -g -Wall \
	tadbit.o main.o -o tadbit -lpthread -lm

tadbit.o: tadbit.c
	gcc -std=gnu99 -fPIC -g -c tadbit.c -o tadbit.o -lpthread -Wall
#tadbit.o: tadbit.c
#	cc -std=gnu99 -fPIC -g -c tadbit.c -o tadbit.o -O3 -lpthread -Wall

main.o: main.c
	gcc -std=gnu99 -g -c main.c -o main.o -Wall
#main.o: main.c
#	cc -std=gnu99 -g -c main.c -o main.o -O3 -Wall
