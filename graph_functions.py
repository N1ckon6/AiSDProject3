import sys
import random
from collections import deque

class Graph:
    """
    Directed graph with support for adjacency matrix, list, and table views.
    Includes graph generation, I/O, and topological sort.
    """
    def __init__(self):
        self.matrix = []
        self.nodes = 0
        self.representation = 'matrix'

    def set_representation(self, representation):
        """
        Set display format: 'matrix', 'list', or 'table'.
        """
        rep = representation.lower()
        while rep not in ['matrix', 'list', 'table']:
            print("Invalid representation. Choose 'matrix', 'list', or 'table'.")
            rep = input("type> ").lower()
        self.representation = rep

    # ----- Graph Generation -----
    def generate_graph(self, nodes, saturation):
        """
        Create a random DAG with given node count and edge saturation percentage.
        """
        self.nodes = nodes
        self.matrix = self.generate_dag(nodes, saturation)

    # ----- Graph Input -----
    def load_graph_from_user(self):
        """
        Load graph either from heredoc stdin or interactive prompts.
        """
        if not sys.stdin.isatty():
            adjacency_list, self.nodes = self.read_heredoc_input()
        else:
            adjacency_list, self.nodes = self.get_user_input()
        self.matrix = self.adjacency_list_to_matrix(adjacency_list, self.nodes)

    def read_heredoc_input(self):
        lines = sys.stdin.read().splitlines()
        nodes = int(lines[0])
        adjacency_list = []
        for i in range(nodes):
            successors = [int(x)-1 for x in lines[i+1].split() if x.isdigit()]
            adjacency_list.append(successors)
        return adjacency_list, nodes

    def get_user_input(self):
        nodes = int(input("nodes> "))
        adjacency_list = []
        for i in range(nodes):
            successors = [int(x)-1 for x in input(f"{i+1}> ").split() if x.isdigit()]
            adjacency_list.append(successors)
        return adjacency_list, nodes

    # ----- Converters -----
    def adjacency_list_to_matrix(self, adjacency_list, nodes):
        matrix = [[0 for _ in range(nodes)] for _ in range(nodes)]
        for i in range(nodes):
            for succ in adjacency_list[i]:
                if 0 <= succ < nodes:
                    matrix[i][succ] = 1
        return matrix

    def matrix_to_adjacency_list(self):
        return [[j for j in range(self.nodes) if self.matrix[i][j] == 1]
                for i in range(self.nodes)]

    # ----- Printing -----
    def print_graph(self):
        """
        Display graph in the chosen format.
        """
        print(f"\nGraph representation ({self.representation}):")
        if self.representation == 'matrix':
            self.print_matrix()
        elif self.representation == 'list':
            self.print_adjacency_list()
        else:
            self.print_adjacency_table()

    def print_matrix(self):
        # Header row with node labels
        print('    |' + ''.join(f' {i+1}' for i in range(self.nodes)))
        print('----+' + '--'*self.nodes)
        # Each row of adjacency
        for i in range(self.nodes):
            print(f"{i+1:3} |" + ''.join(f' {self.matrix[i][j]}' for j in range(self.nodes)))

    def print_adjacency_list(self):
        for i in range(self.nodes):
            successors = [str(j+1) for j in range(self.nodes) if self.matrix[i][j] == 1]
            print(f"{i+1}> {' '.join(successors)}")

    def print_adjacency_table(self):
        print('Node | Successors')
        print('-----+-----------')
        for i in range(self.nodes):
            successors = [str(j+1) for j in range(self.nodes) if self.matrix[i][j] == 1]
            print(f"{i+1:4} | {' '.join(successors)}")

    # ----- Edge Query -----
    def find_edge(self, from_node, to_node):
        """
        Return True if edge exists from from_node to to_node (1-indexed).
        """
        if from_node < 1 or from_node > self.nodes or to_node < 1 or to_node > self.nodes:
            return False
        return self.matrix[from_node-1][to_node-1] == 1

    # ----- Internal DAG Generator -----
    def generate_dag(self, nodes, saturation):
        matrix = [[0 for _ in range(nodes)] for _ in range(nodes)]
        max_edges = nodes * (nodes - 1) // 2
        target_edges = int(max_edges * saturation / 100)
        edges_added = 0
        while edges_added < target_edges:
            for i in range(nodes):
                for j in range(i + 1, nodes):
                    if random.random() < 0.5 and edges_added < target_edges and matrix[i][j] == 0:
                        matrix[i][j] = 1
                        edges_added += 1
        return matrix

    # ----- Traversal Stubs -----
    def bfs(self):
        """
        Perform breadth-first search over the graph, covering all components.
        Prints and returns the order of visited nodes (1-indexed).
        """
        visited = [False] * self.nodes
        order = []
        queue = deque()

        for start in range(self.nodes):
            if not visited[start]:
                visited[start] = True
                queue.append(start)
                while queue:
                    u = queue.popleft()
                    order.append(u + 1)
                    for v in range(self.nodes):
                        if self.matrix[u][v] == 1 and not visited[v]:
                            visited[v] = True
                            queue.append(v)
        print("inline>", " ".join(map(str, order)))
        return order

    def dfs(self):
        """
        Perform depth-first search over the graph, covering all components.
        Prints and returns the order of visited nodes (1-indexed).
        """
        visited = [False] * self.nodes
        order = []

        def dfs_visit(u):
            visited[u] = True
            order.append(u + 1)
            for v in range(self.nodes):
                if self.matrix[u][v] == 1 and not visited[v]:
                    dfs_visit(v)

        for start in range(self.nodes):
            if not visited[start]:
                dfs_visit(start)
        print("inline>", " ".join(map(str, order)))
        return order

    # ----- Kahn's Topological Sort -----
    def topological_sort_Kahn(self):
        if not self.matrix:
            return []
        in_degree = [0] * self.nodes
        for i in range(self.nodes):
            for j in range(self.nodes):
                if self.matrix[i][j] == 1:
                    in_degree[j] += 1
        queue = deque()
        for i in range(self.nodes):
            if in_degree[i] == 0:
                queue.append(i)
        topo_order = []
        count = 0
        while queue:
            u = queue.popleft()
            topo_order.append(u + 1)
            for v in range(self.nodes):
                if self.matrix[u][v] == 1:
                    in_degree[v] -= 1
                    if in_degree[v] == 0:
                        queue.append(v)
            count += 1
        if count != self.nodes:
            return None
        return topo_order
    
    # ----- Tarjan's Topological Sort -----
    def topological_sort_Tarjan(self):
        n = self.nodes
        mark = [0] * n
        L = []
        def visit(u):
            if mark[u] == 2:
                return
            if mark[u] == 1:
                raise RuntimeError("cycle")
            mark[u] = 1
            for v in range(n):
                if self.matrix[u][v] == 1:
                    visit(v)
            mark[u] = 2
            L.append(u + 1)
        try:
            for u in range(n):
                if mark[u] == 0:
                    visit(u)
        except RuntimeError:
            return None
        L.reverse()
        return L
