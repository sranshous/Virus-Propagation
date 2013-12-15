# Author: Stephen Ranshous
# Date:   5 December, 2013
# Plot the average number of infected nodes for the vanishing version
# as well as the spreading version, on the same plot.

set terminal png nocrop
set title "Plot of vanishing compared to spreading virus"
set xlabel "Time step"
set ylabel "Average number of infected nodes"
set output 'p2.png'
plot "problem2.out" using 1:2 title 'Vanish' with linespoints, \
     "problem2.out" using 1:3 title 'Spread' with linespoints
