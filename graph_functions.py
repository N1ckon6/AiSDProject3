import sys
import random

class Graph:
    def __init__(self):
        self.matrix = []
        self.nodes = 0
        self.representation = 'matrix'
    
    def set_representation(self, representation):
        self.representation = representation.lower()
        while self.representation not in ['matrix', 'list', 'table']:
            print("Invalid representation. Choose 'matrix', 'list', or 'table'")
            self.representation = input("type> ").lower()
    
    def generate_graph(self, nodes, saturation):
        self.nodes = nodes
        self.matrix = self.generate_dag(nodes, saturation)  # This is the critical fix
    
    def load_graph_from_user(self):
        if not sys.stdin.isatty():
            adjacency_list, self.nodes = self.read_heredoc_input()
        else:
            adjacency_list, self.nodes = self.get_user_input()
        
        self.matrix = self.adjacency_list_to_matrix(adjacency_list, self.nodes)
    
    def print_graph(self):
        print(f"\nGraph representation ({self.representation}):")
        if self.representation == "matrix":
            self.print_matrix()
        elif self.representation == "list":
            self.print_adjacency_list()
        elif self.representation == "table":
            self.print_adjacency_table()
    
    def print_matrix(self):
        print("    |", end="")
        for i in range(self.nodes):
            print(f" {i+1}", end="")
        print("\n----+" + "--" * self.nodes)
        
        for i in range(self.nodes):
            print(f"{i+1:3} |", end="")
            for j in range(self.nodes):
                print(f" {self.matrix[i][j]}", end="")
            print()
    
    def print_adjacency_list(self):
        adjacency_list = self.matrix_to_adjacency_list()
        for i in range(self.nodes):
            successors = [str(j+1) for j in range(self.nodes) if self.matrix[i][j] == 1]
            print(f"{i+1}> {' '.join(successors)}")
    
    def print_adjacency_table(self):
        print("Node | Successors")
        print("-----+-----------")
        adjacency_list = self.matrix_to_adjacency_list()
        for i in range(self.nodes):
            successors = [str(j+1) for j in range(self.nodes) if self.matrix[i][j] == 1]
            print(f"{i+1:4} | {' '.join(successors)}")
    
    def find_edge(self, from_node, to_node):
        if from_node < 1 or from_node > self.nodes or to_node < 1 or to_node > self.nodes:
            return False
        return self.matrix[from_node-1][to_node-1] == 1
    
    def matrix_to_adjacency_list(self):
        return [[j for j in range(self.nodes) if self.matrix[i][j] == 1] for i in range(self.nodes)]
    
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
    
    def read_heredoc_input(self):
        lines = sys.stdin.read().splitlines()
        nodes = int(lines[0])
        adjacency_list = []
        
        for i in range(nodes):
            successors = lines[i+1].split()
            successors = [int(node)-1 for node in successors if node.isdigit()]
            adjacency_list.append(successors)
        
        return adjacency_list, nodes
    
    def get_user_input(self):
        nodes = int(input("nodes> "))
        adjacency_list = []
        
        for i in range(nodes):
            successors = input(f"{i+1}> ").split()
            successors = [int(node)-1 for node in successors if node.isdigit()]
            adjacency_list.append(successors)
        
        return adjacency_list, nodes
    
    def adjacency_list_to_matrix(self, adjacency_list, nodes):
        matrix = [[0 for _ in range(nodes)] for _ in range(nodes)]
        
        for i in range(nodes):
            for successor in adjacency_list[i]:
                if successor < nodes:
                    matrix[i][successor] = 1
        
        return matrix