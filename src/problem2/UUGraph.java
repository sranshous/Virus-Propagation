import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * A static undirected, unweighted graph. Once created no edges or vertices
 * can be added. It uses an adjacency list format representation. Internally
 * it uses integers to represent the nodes, so there cannot be more than
 * (2^31 - 1) vertices or there will be problems with overflow.
 *
 * Author: Stephen Ranshous
 * Date:   5 December, 2013
 */
public class UUGraph {
    private final BufferedReader br;                // To read the graph
    private String filename;                        // File to create graph from

    private ArrayList<ArrayList<Integer>> al;       // Adjacency list representation

    private int n;      // Number of nodes in the graph
    private int m;      // Number of edges in the graph

    /**
     * Initialize the graph with an edgelist.
     * The first line of the file is the number of nodes then the number of
     * edges. Nodes should have a linear indexing, starting at 0 going to n-1.
     * Every line following is an undirected edge and should have only
     * two integers on it, u and v which are the endpoints of the edge. The file
     * should be either space or tab delimited. Anything after the first two
     * fields will be ignored.
     *
     * @param filename Graph file name.
     */
    public UUGraph(String filename) throws IOException {
        this.filename = filename;
        this.br = new BufferedReader(new FileReader(filename));
        readGraphFile();
    }

    private void readGraphFile() {
        // Read the first line, which should be the number of nodes then the
        // number of edges

        try {
            String[] line = br.readLine().trim().split("\\s");  // Split on whitespace
            n = Integer.parseInt(line[0]);
            m = Integer.parseInt(line[1]);

            // Create the adjacency list
            al = new ArrayList<>(n);
            for (int i = 0; i < n; i++) al.add(new ArrayList<Integer>());

            // Read until EOF. If the number of lines read does not match the number of
            // edges provided in the first line there is a problem so exit with an error.
            int nLines = 0;
            String edge = "";
            while ((edge = br.readLine()) != null) {
                nLines++;
                line = edge.trim().split("\\s");    // Split on whitespace

                int u = Integer.parseInt(line[0]);
                int v = Integer.parseInt(line[1]);

                try {
                    al.get(u).add(v);
                    al.get(v).add(u);
                }
                catch (IndexOutOfBoundsException ioobe) {
                    System.err.printf("There was an error reading the edge on line %d. ", nLines+1);
                    System.err.printf("One of the nodes was out of the range [0, N-1].\n");
                    System.exit(1);
                }
            }

            if (nLines != m) {
                System.err.printf("The number of edges in the file (%d) does not match the ", nLines);
                System.err.printf("number of edges indicated in the first line of the file (%d).", m);
                System.exit(1);
            }
        }
        catch (IOException ioe) {
            System.err.printf("Error creating the graph from the given file: %s\n", filename);
            System.err.printf("Make sure the file uses the correct format.\n");
            System.exit(1);
        }
    }

    /**
     * Number of nodes in the graph.
     *
     * @return Number of nodes.
     */
    public int n() {
        return n;
    }

    /**
     * Number of edges in the graph.
     *
     * @return Number of edges.
     */
    public int m() {
        return m;
    }

    /**
     * Get all of the neighbors of the node v.
     *
     * @return All the neighbors of node v or null if v is invalid.
     */
    public ArrayList<Integer> neighbors(int v) {
        if (v >= n || v < 0) return null;
        return al.get(v);
    }

    public String toString() {
        StringBuffer graph = new StringBuffer();
        graph.append("n = " + n + "\tm = " + m + "\n");

        // Append the adjacency list
        for (int i = 0; i < al.size(); i++) {
            graph.append(i + ":");

            ArrayList<Integer> vertex = al.get(i);
            for (int j = 0; j < vertex.size(); j++) {
                graph.append(" " + vertex.get(j));
            }

            graph.append("\n");
        }

        return graph.toString();
    }

    public static void main(String[] args) throws IOException {
        UUGraph g = new UUGraph(args[0]);
        System.out.println(g);
    }
}
