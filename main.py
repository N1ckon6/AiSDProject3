from graph_functions import Graph
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py --generate or python main.py --user-provided")
        return
    
    graph = Graph()
    graph.set_representation(input("type> "))
    
    if sys.argv[1] == "--generate":
        nodes = int(input("nodes> "))
        saturation = int(input("saturation> "))
        
        if saturation < 0 or saturation > 100:
            print("Saturation must be between 0 and 100")
            return
            
        graph.generate_graph(nodes, saturation)
    elif sys.argv[1] == "--user-provided":
        graph.load_graph_from_user()
    else:
        print("Invalid mode. Use --generate or --user-provided")
        return
    
    action_menu(graph)

def action_menu(graph):
    print("\nAvailable actions:")
    print("help - For help")
    print("print - Print graph in selected representation")
    print("find - Check if edge exists")
    print("bfs - Breath-first search")
    print("dfs - Depth-first search")
    print("sortK - Perform topological sort (Kahn's algorithm)")
    print("sortT - Perform topological sort (Tarjan's algorithm)")
    print("printTikz - Export graph to TikZ format for LaTeX")
    print("exit - Exit program\n")
    while True:
        action = input("actions> ").lower()
        match action:
            case 'print':
                 graph.print_graph()
            case 'find':
                from_node = int(input("from> "))
                to_node = int(input("to> "))
                exists = graph.find_edge(from_node, to_node)
                if exists:
                    print(f"True: edge ({from_node},{to_node}) exists in the Graph")
                else:
                    print(f"False: edge ({from_node},{to_node}) does not exist in the Graph")
            case 'bfs':
                inline = graph.bfs()
            case 'dfs':
                inline = graph.dfs()
            case 'sortk':
                result = graph.topological_sort_Kahn()
                if result is None:
                    print("Graph contains at least one cycle - cannot perform topological sort")
                else:
                    print("Topological order:", " ".join(map(str, result)))
            case 'sortt':
                result = graph.topological_sort_Tarjan()
                if result is None:
                    print("Graph contains at least one cycle - cannot perform topological sort")
                else:
                    print("Topological order:", " ".join(map(str, result)))
            case 'printtikz':
                tikz_code = graph.export_to_tikz()
                print("\nTikZ code for LaTeX:\n")
                print(tikz_code)
                print("\nCopy this code into your LaTeX document.")
            case 'exit':
                break
            case _ :
                print("Invalid action. Use 'print', 'find', 'sortK' or 'exit'")
                
if __name__ == "__main__":
    main()