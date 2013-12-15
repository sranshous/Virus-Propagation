function [ graph ] = readGraph( graphFile )
%READGRAPH Create a sparse matrix representation of a graph
%   Create a sparse matrix representation of an adjacency list for the
%   graph which is described in the file "graphFile". The first line of the
%   file should be two integer values, n and m, which is the number of
%   nodes followed by the number of edges.
%
%   Author: Stephen Ranshous
%   Date:   5 December, 2013

f = fopen(graphFile, 'r');

% Read the edges of the graph into the matrix A. Then append a second
% matrix to A, which is A except flipped since the graph is undirected.
header = fgetl(f);
A = fscanf(f, '%d %d\n', [2 inf])';
A = [A; [A(:, 2), A(:, 1)]];

% Add 1 to every entry since the file is a zero based graph and Matlab is a
% one based language.
A = A + 1;

m = size(A, 1);
graph = sparse(A(:, 1), A(:, 2), ones(m, 1), m, m, m);

end

