import math
import sys
import random
from collections import deque
from collections import Counter

class Graph:
    """
    Directed graph with support for adjacency matrix, list, and table views.
    Includes graph generation, I/O, and topological sort.
    """
    def __init__(self):
        self.matrix = []
        self.nodes = 0
        self.representation = 'matrix'
        self.table = []

    def set_representation(self, representation):
        """
        Set display format: 'matrix', 'list', or 'table'.
        """
        rep = representation.lower()
        while rep not in ['matrix', 'list', 'table']:
            print("Invalid representation. Choose 'matrix', 'list', or 'table'.")
            rep = input("type> ").lower()
        self.representation = rep
        if rep == 'table':
            self.matrix_to_table()

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
        while True:
            user_input = input("nodes> ")
            try:
                nodes = int(user_input)
            except ValueError:
                print("Error: Invalid input - must be numbers")
                continue
            if nodes < 0:
                print("Error: Invalid input - nodes must be >= 0")
                continue
            break
        adjacency_list = []
        for i in range(nodes):
            raw = [int(x)-1 for x in input(f"{i+1}> ").split() if x.isdigit()]
            # Detect invalid nodes
            invalids = sorted({val+1 for val in raw if val < 0 or val >= nodes})
            if invalids:
                inv_str = ", ".join(str(n) for n in invalids)
                print(f"Error: node(s) {inv_str} exceed number of nodes ({nodes}), ignoring these values.")
            # Keep only valid
            valid_raw = [val for val in raw if 0 <= val < nodes]
            # Detect duplicates
            counts = Counter(valid_raw)
            duplicates = [node for node, cnt in counts.items() if cnt > 1]
            if duplicates:
                dup_str = ", ".join(str(d+1) for d in duplicates)
                print(f"Warning: In {i+1}>, node(s) {dup_str} occur multiple times; duplicates will be ignored.")
            # Preserve order, remove duplicates
            seen = set()
            clean = []
            for succ in valid_raw:
                if succ not in seen:
                    seen.add(succ)
                    clean.append(succ)
            adjacency_list.append(clean)
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
    
    def matrix_to_table(self):
        self.table = [(i, j) for i in range(self.nodes) for j in range(self.nodes) if self.matrix[i][j] == 1]

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
        if not self.table:
            self.matrix_to_table()
        print(" From | To")
        print("------+----")
        for frm, to in self.table:
            print(f"  {frm+1:<4}| {to+1}")

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

    # ----- Helper methods for representation-dependent operations -----
    def _get_successors(self, node):
        if self.representation == 'matrix':
            return [j for j in range(self.nodes) if self.matrix[node][j] == 1]
        elif self.representation == 'list':
            adj_list = self.matrix_to_adjacency_list()
            return adj_list[node]
        else:  # table
            return [to for frm, to in self.table if frm == node]


    def _get_all_edges(self):
        """Get all edges in the graph based on current representation"""
        return self.matrix_to_table_list()
        if self.representation == 'matrix':
            return [(i, j) for i in range(self.nodes) for j in range(self.nodes) if self.matrix[i][j] == 1]
        elif self.representation == 'list':
            adj_list = self.matrix_to_adjacency_list()
            return [(i, j) for i in range(self.nodes) for j in adj_list[i]]
        else:  # table
            return self.table
    # ----- Traversal Methods -----
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
                    for v in self._get_successors(u):
                        if not visited[v]:
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
            for v in self._get_successors(u):
                if not visited[v]:
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
        edges = self._get_all_edges()
        for (u, v) in edges:
            in_degree[v] += 1
        queue = deque()
        for i in range(self.nodes):
            if in_degree[i] == 0:
                queue.append(i)       
        topo_order = []
        count = 0
        while queue:
            u = queue.popleft()
            topo_order.append(u + 1)
            for v in self._get_successors(u):
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
            for v in self._get_successors(u):
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
    
    def export_to_tikz(self, directed=True):
        """
        Export the graph to TikZ code for LaTeX visualization.
        Args:
            directed: If True, creates directed edges with arrows
        Returns:
            String with tikzpicture environment that can be used in LaTeX
        """
        if not self.nodes:
            return "% Empty graph (no nodes)"
        
        # Node positioning in a circle
        tikz_code = "\\begin{tikzpicture}["
        if directed:
            tikz_code += "->, >=stealth', shorten >=1pt, auto, "
        tikz_code += "node distance=3cm, every node/.style={circle, draw, minimum size=8mm, font=\\small}]\n\n"
        
        # Calculate node positions on a circle
        angle = 360 / self.nodes
        radius = 3 if self.nodes <= 5 else (4 if self.nodes <= 10 else 5)
        
        # Add nodes
        for i in range(self.nodes):
            x = radius * math.cos(math.radians(i * angle))
            y = radius * math.sin(math.radians(i * angle))
            tikz_code += f"  \\node (n{i+1}) at ({x:.2f},{y:.2f}) {{{i+1}}};\n"
        
        # Add edges based on current representation
        edges = self._get_all_edges()
        if edges:
            tikz_code += "\n"
            for (u, v) in edges:
                if directed:
                    # For directed graph, use proper arrow tips at the end
                    tikz_code += f"  \\draw[->] (n{u+1}) -- (n{v+1});\n"
                else:
                    tikz_code += f"  \\draw (n{u+1}) -- (n{v+1});\n"
        
        tikz_code += "\\end{tikzpicture}"
        return tikz_code