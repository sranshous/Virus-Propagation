import random
import numpy
import scipy
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh
from operator import itemgetter

class SIS_Static_Healing(object):
    def __init__(self, beta, delta, graphFile):
        self.beta = beta        # Transmission probability
        self.delta = delta      # Healing probability
        self.g = Graph(graphFile)

    def simulate(self, immunizationPolicy, iterations = 100):
        """Simulate the virus propagation. By default there will be 100 time steps.
        The return value is the number of nodes infected at each time point.

        immunizationPolicy - The policy to use for immunization. See the help for immunize."""

        #print "Simulating %d iterations with beta = %f and delta = %f" % (iterations, self.beta, self.delta)

        infectedPerIter = [0] * (iterations+1)
        infected = [False] * self.g.n

        # Infect 10% of the graph
        infect = random.sample(xrange(self.g.n), int(self.g.n / 10))
        for u in infect:
            infected[u] = True

        immune = self.immunize(infected, immunizationPolicy)

        print "The effective strength after immunization is %f" % ((beta / delta) * self.g.maxEigenValRemoved(immune))


        numInfected = sum([1 for x in infected if x == True])

        # Simulate
        infectedPerIter[0] = numInfected
        for k in xrange(iterations):
            infect = set()
            cure = set()

            # Do infections
            for i in xrange(self.g.n):
                # If the node is infected loop over its neighbors and try to infect
                # them if they are not currently infected and not immune
                if infected[i]:
                    for v in self.g.neighbors(i):
                        if not infected[v] and random.random() < self.beta and self.g.al != -1:
                            infect.add(v)

            # Do cures
            for i in xrange(self.g.n):
                # If a node is infected try to cure it
                if infected[i] and random.random() < self.delta:
                    cure.add(i)

            # Update the infected nodes. No need to check for double infection
            # like we did in problem 2 since we are using a set in this code.
            for v in infect:
                infected[v] = True
                numInfected += 1

            # Update the cured nodes
            for v in cure:
                infected[v] = False
                numInfected -= 1

            infectedPerIter[k+1] = numInfected

        #print sum([1 for x in infected if x == True])
        return infectedPerIter

    def immunize(self, infected, policy):
        """Given the array of boolean values of who is infected apply an immunization
        policy and cure some nodes. There are 200 vaccines available.

        Note: Immunization REMOVES the node and its edges from the network.

        Policies:
            'A' - Select k random nodes to immunize.
            'B' - Select the k nodes with the highest degree for immunization.
            'C' - Select the node with the highest degree at each iteration, considering
                    the updated degrees after each removal.
            'D' - Find the eigenvector corresponding to the largest eigenvalue of the
                    contact network's adjacency matrix. Find the k largest (absolute)
                    values in the eigenvector. Select the k nodes at the corresponding
                    positions in the eigenvector.

        Returns a list of the immunized nodes."""

        MAX_VACCINES = 200
        vaccines = MAX_VACCINES
        immune = []

        if policy == 'A':
            immune = random.sample(xrange(self.g.n), MAX_VACCINES)

            # Remove node u and all edges (u, v)
            for u in immune:
                # Remove all edges
                for v in self.g.al[u]:
                    self.g.al[v].remove(u)

            # Set the immunized nodes to -1 so we do not mess up the rest of the
            # graph indexing.
            for u in immune:
                self.g.al[u] = -1
                infected[u] = False

        elif policy == 'B':
            degs = []
            for u, neighbors in enumerate(self.g.al):
                degs.append((u, len(neighbors)))

            immune = [u[0] for u in sorted(degs, key = itemgetter(1), reverse = True)[:MAX_VACCINES]]

            # Remove node u and all edges (u, v)
            for u in immune:
                # Remove all edges
                for v in self.g.al[u]:
                    self.g.al[v].remove(u)

            # Set the immunized nodes to -1 so we do not mess up the rest of the
            # graph indexing.
            for u in immune:
                self.g.al[u] = -1
                infected[u] = False

        elif policy == 'C':
            while vaccines > 0:
                # find highest degree node, immunize it, then repeat
                degs = []
                for u, neighbors in enumerate(self.g.al):
                    if neighbors != -1:
                        degs.append((u, len(neighbors)))

                u = sorted(degs, key = itemgetter(1), reverse = True)[0][0]
                immune.append(u)

                # Remove all edges
                for v in self.g.al[u]:
                    self.g.al[v].remove(u)

                # Set the immunized nodes to -1 so we do not mess up the rest of the
                # graph indexing.
                self.g.al[u] = -1
                infected[u] = False

                vaccines -= 1

        elif policy == 'D':
            vec = self.g.maxEigenVector()
            vec = numpy.absolute(vec)

            immune = [u[0] for u in sorted(enumerate(vec), reverse = True, key = itemgetter(1))[:200]]

            #print sorted(enumerate(vec), reverse = True, key = itemgetter(1))[:10]

            # Remove node u and all edges (u, v)
            for u in immune:
                # Remove all edges
                for v in self.g.al[u]:
                    self.g.al[v].remove(u)

            # Set the immunized nodes to -1 so we do not mess up the rest of the
            # graph indexing.
            for u in immune:
                self.g.al[u] = -1
                infected[u] = False

        else:
            raise "Invalid policy"

        return immune

class Graph(object):

    def __init__(self, graphFile):
        with open(graphFile, 'r') as fin:
            self.n, self.m = map(int, fin.readline().strip().split())
            self.al = [[] for _ in xrange(self.n)]
            self.sm = self.sparseMatrix()
            self.maxEigenVector()

            for edge in fin:
                u, v = map(int, edge.strip().split())
                self.al[u].append(v)
                self.al[v].append(u)

    def __str__(self):
        output = ""
        for k, v in enumerate(self.al):
            output += str(k) + ": " + ' '.join([str(u) for u in v]) + "\n"

        return output

    def sparseMatrix(self):
        """Create a sparse matrix representation of the graph."""
        rows = [0] * 2 * self.m
        cols = [0] * 2 * self.m
        data = [0] * 2 * self.m
        index = 0

        for u, neighbors in enumerate(self.al):
            for v in neighbors:
                rows[index], cols[index] = u, v
                data[index] = 1
                index += 1

        return csr_matrix((data, (rows, cols)), shape = (self.n, self.n), dtype = numpy.float64)

    def maxEigenVector(self):
        """Get the eigen vector corresponding to the largest eigen value for the
        sparse matrix eigen decomposition of the adjacency matrix."""
        evals, evecs = eigsh(self.sm, k = 1)
        return evecs

    def maxEigenValRemoved(self, removeMe):
        """Find the maximum eigen value corresponding to the sparse matrix as if
        the vertices listed in "removeMe" were not in the graph."""

        # Remap the vertices and create a new adjacency matrix
        ignore = set(removeMe)
        vmap = {}
        index = 0
        for u in xrange(self.n):
            if u not in ignore:
                vmap[u] = index
                index += 1

        alNew = [[] for _ in xrange(len(vmap))]
        mNew = 0

        for u, neighbors in enumerate(self.al):
            if u not in ignore:
                alNew[vmap[u]] = [vmap[v] for v in neighbors if v not in ignore]
                mNew += len(alNew[vmap[u]])

        rows = [0] * 2 * mNew
        cols = [0] * 2 * mNew
        data = [0] * 2 * mNew
        index = 0

        for u, neighbors in enumerate(alNew):
            for v in neighbors:
                rows[index], cols[index] = u, v
                data[index] = 1
                index += 1

        smNew = csr_matrix((data, (rows, cols)), shape = (self.n, self.n), dtype = numpy.float64)
        evals, evecs = eigsh(smNew, k = 1)
        return evals[0]

    def neighbors(self, u):
        """Get a list of the neighbors of node u."""
        return self.al[u]

if __name__ == "__main__":
    from sys import argv

    #policy = 'A'

    if len(argv) < 2:
        print "Usage: python %s <graph file> [policy]" % argv[0]
        exit(1)

    #if len(argv) == 3:
        #print "policy = %s" % argv[2]
        #policy = argv[2]

    beta = 0.2
    delta = 0.7
    #beta = 0.01
    #delta = 0.6
    #ssh = SIS_Static_Healing(beta, delta, argv[1])

    for p in ['A', 'B', 'C', 'D']:
        print "---- Simulating policy %s ----" % p
        for iterations in range(50, 150, 10):
            print "Number of iterations = %d" % iterations
            avgs = [0] * (iterations+1)
            for i in range(10):
                ssh = SIS_Static_Healing(beta, delta, argv[1])
                infectedPerIter = ssh.simulate(p, iterations)
                for j in range(len(infectedPerIter)):
                    avgs[j] += infectedPerIter[j]
            for i in range(len(avgs)):
                avgs[i] /= float(10)

            print avgs
