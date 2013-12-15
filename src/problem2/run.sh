#!/bin/bash

printf "Compiling the java source files..."
javac *.java
printf "done.\n"

printf "Running the simulation..."
java SIS_Static ../../datasets/static.network > problem2.out
printf "done.\n"

printf "Plotting results..."
gnuplot p2_plot.gnu
printf "done. The plot is in 'p2.png'\n"
