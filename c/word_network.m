

% Create undirected graph using adjacency matrix A
nodenames = {'V1','V2','V3'};

% Create empty graph
G = graph;

% s = [1 2 1];
% t = [2 3 3];
G = addedge(G,s,t);
% https://www.mathworks.com/help/matlab/ref/graph.html

s = [1 1 1 2 3];
t = [2 3 4 3 4];
weights = [6 6.5 7 11.5 17]';
code = {'1/44' '1/49' '1/33' '44/49' '49/33'}';
EdgeTable = table([s' t'],weights,code, ...
    'VariableNames',{'EndNodes' 'Weight' 'Code'})

names = {'USA' 'GBR' 'DEU' 'FRA'}';
country_code = {'1' '44' '49' '33'}';
NodeTable = table(names,country_code,'VariableNames',{'Name' 'Country'})


G = graph(EdgeTable,NodeTable);
plot(G,'NodeLabel',G.Nodes.Country,'EdgeLabel',G.Edges.Code)


% Compute Laplacian

L = D - A;

% https://www.mathworks.com/help/matlab/graph-and-network-algorithms.html
%%%%%%% https://www.cs.purdue.edu/homes/dgleich/demos/matlab/spectral/spectral.html


