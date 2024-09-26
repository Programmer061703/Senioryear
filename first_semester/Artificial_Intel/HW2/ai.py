import heapq

# Define the graph (edge costs and heuristic values)
# (node): [(neighbor, edge_cost), ...]
graph = {
    'S': [('B', 4), ('D', 2)],
    'D': [('A', 1), ('E', 5)],
    'B': [('T', 2), ('J', 1)],
    'E': [('J', 1)],
    'A': [('F', 3)], 
    'T': [('G', 3)],
    'J': [('G', 6)],
    'F': [],
    'G': []
}

# Heuristic values (estimated cost to reach 'G' from each node)
heuristic = {
    'S': 9,
    'D': 12,
    'B': 5,
    'A': 15,
    'T': 3, 
    'E': 7,
    'J': 6,
    'F': 18,
    'G': 0
}

# Greedy Best First Search
def greedy_search(graph, heuristic, start, goal):
    # Initialize the frontier with the start node
    # Each item in the frontier is (heuristic value, node)
    frontier = [(heuristic[start], start)]
    heapq.heapify(frontier)
    
    # Set to keep track of visited nodes
    visited = set()
    
    # Parent dictionary to reconstruct the path
    parent = {}
    
    while frontier:
        # Pop the node with lowest heuristic value
        h_value, current = heapq.heappop(frontier)
        
        # Goal test
        if current == goal:
            # Reconstruct path
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            return f"Path found: {' -> '.join(path)}"
        
        visited.add(current)
        
        # Expand neighbors
        for neighbor, cost in graph[current]:
            if neighbor not in visited:
                heapq.heappush(frontier, (heuristic[neighbor], neighbor))
                parent[neighbor] = current  # Keep track of parent
    return "Goal not reachable"

# A* Search
def a_search(graph, heuristic, start, goal):
    # Initialize the frontier with the start node
    # Each item in the frontier is (f_value, g_value, node)
    frontier = [(heuristic[start], 0, start)]
    heapq.heapify(frontier)
    
    # Set to keep track of visited nodes
    visited = set()
    
    # Parent dictionary to reconstruct the path
    parent = {}
    
    while frontier:
        # Pop the node with lowest f_value
        f_value, g_value, current = heapq.heappop(frontier)
        
        # Goal test
        if current == goal:
            # Reconstruct path
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            return f"Path found: {' -> '.join(path)} with total cost {g_value}"
        
        if current in visited:
            continue
        visited.add(current)
        
        # Expand neighbors
        for neighbor, cost in graph[current]:
            if neighbor not in visited:
                g = g_value + cost
                f = g + heuristic[neighbor]
                heapq.heappush(frontier, (f, g, neighbor))
                parent[neighbor] = current  # Keep track of parent
    return "Goal not reachable"

# Test the functions
print(greedy_search(graph, heuristic, 'S', 'G'))  # Output should indicate reaching the goal
print(a_search(graph, heuristic, 'S', 'G'))  # Output should indicate reaching the goal and the cost
