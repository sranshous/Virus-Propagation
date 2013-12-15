import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

/**
 * A simulator for the SIS virus propagation model, with no immunization.
 * For every simulation object you must provide the beta and delta values.
 * These values are the transmission probability and headling probability,
 * respectively. It uses the UUGraph class to represent the graph.
 *
 * Author: Stephen Ranshous
 * Date:   5 December, 2013
 */
public class SIS_Static {
    protected double beta;      // Transmission probability
    protected double delta;     // Headling probability

    protected UUGraph g = null; // Graph for simulation

    /**
     * Create a SIS Static simulation with the given beta and delta probabilities
     * and simulated the spread over the graph from "graphFile".
     */
    public SIS_Static(double beta, double delta, String graphFile) throws IOException {
        this.beta = beta;
        this.delta = delta;
        this.g = new UUGraph(graphFile);
    }

    /**
     * Simulate the virus propagation process.
     * 100 time steps will be simulated. The number of nodes infected initially
     * is 10% of the graph.
     *
     * @return The number of infected nodes at each time step.
     */
    public int[] simulate() {
        int nIters = 100;
        int nToInfect = g.n() / 10;
        int nInfected = 0;

        int[] infectedPerTime = new int[nIters+1];
        boolean[] infected = new boolean[g.n()];

        Random rand = new Random();
        while (nInfected != nToInfect) {
            int v = rand.nextInt(g.n());
            if (!infected[v]) {
                infected[v] = true;
                nInfected++;
            }
        }

        // At t=0 there are nToInfect number of infected persons
        infectedPerTime[0] = nInfected;

        // Do not update the infected / cured nodes until the end of each iteration.
        for (int i = 0; i < nIters; i++) {
            ArrayList<Integer> infect = new ArrayList<>();
            ArrayList<Integer> cure   = new ArrayList<>();

            // Loop over entire populous and check for infected to spread
            for (int j = 0; j < infected.length; j++) {
                if (!infected[j]) {
                    continue;
                }

                // try to infect neighbors
                ArrayList<Integer> neighbors = g.neighbors(j);

                for (Integer v : neighbors) {
                    // Infect with probability beta if node is healthy
                    if (!infected[v] && rand.nextDouble() < beta) {
                        infect.add(v);
                    }
                }
            }

            // Loop over entire populous and check for infected to cure
            for (int j = 0; j < infected.length; j++) {
                // Cure with probability delta
                if (infected[j] && rand.nextDouble() < delta) {
                    cure.add(j);
                }
            }

            // Do updates
            for (Integer v : infect) {
                // This check is necessary because two nodes may try to infect the same
                // neighbor, which we do not want to double count in the infected count.
                if (!infected[v]) {
                    infected[v] = true;
                    nInfected++;
                }
            }

            for (Integer v : cure) {
                infected[v] = false;
                nInfected--;
            }

            infectedPerTime[i+1] = nInfected;
        }

        return infectedPerTime;
    }

    public static void main(String[] args) throws IOException {
        double beta = 0.01;
        double delta = 0.6;
        final String graphFile = args[0];
        final int nSims = 10;

        SIS_Static ss = new SIS_Static(beta, delta, graphFile);
        int[] ipt_vanish = null;
        double[] avgIPT_vanish = null;

        // do 10 simulations
        for (int i = 0; i < nSims; i++) {
            int[] temp = ss.simulate();

            if (ipt_vanish == null) ipt_vanish = new int[temp.length];

            for (int j = 0; j < ipt_vanish.length; j++) {
                ipt_vanish[j] += temp[j];
            }
        }

        avgIPT_vanish = new double[ipt_vanish.length];
        for (int i = 0; i < ipt_vanish.length; i++) {
            avgIPT_vanish[i] = (double) ipt_vanish[i] / (double) nSims;
        }

        beta = 0.2;
        delta = 0.7;
        ss = new SIS_Static(beta, delta, graphFile);

        int[] ipt_spread = null;
        double[] avgIPT_spread = null;

        // do 10 simulations
        for (int i = 0; i < nSims; i++) {
            int[] temp = ss.simulate();

            if (ipt_spread == null) ipt_spread = new int[temp.length];

            for (int j = 0; j < ipt_spread.length; j++) {
                ipt_spread[j] += temp[j];
            }
        }

        avgIPT_spread = new double[ipt_spread.length];
        for (int i = 0; i < ipt_spread.length; i++) {
            avgIPT_spread[i] = (double) ipt_spread[i] / (double) nSims;
        }

        // Print a gnuplot style output
        System.out.println("# Timestep\tVanish\tSpread");
        for (int i = 0; i < ipt_vanish.length; i++) {
            System.out.printf("%d\t%f\t%f\n", i, avgIPT_vanish[i], avgIPT_spread[i]);
        }
    }
}
