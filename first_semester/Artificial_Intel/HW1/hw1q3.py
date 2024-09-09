from collections import deque
import heapq

# Define the graph
graph = {
    'A': ['D'],
    'B': ['A', 'E'],
    'C': ['G', 'E'],
    'D': ['C'],
    'E': [],
    'S': ['D', 'B', 'A'],
    'G': []
}
graph2 = {
    'A': [('D', 1)],
    'B': [('A', 3), ('E', 4)],
    'C': [('G', 1), ('E', 3)],
    'D': [('C', 1)],
    'E': [],
    'S': [('D', 4), ('B', 2), ('A', 2)],
    'G': []
}

# Uniform Cost Search (UCS) Implementation
def ucs(graph, start, end):
    # Priority queue to store (cost, path)
    # Start with the initial node and a path cost of 0
    queue = [(0, [start])]
    
    # Visited dictionary to track the minimum cost to reach each node
    visited = {}
    
    while queue:
        # Pop the node with the smallest cost
        cost, path = heapq.heappop(queue)
        node = path[-1]
        
        # If the goal is reached, return the path and cost
        if node == end:
            return path, cost
        
        # If the node hasn't been visited or a cheaper path is found, explore it
        if node not in visited or cost < visited[node]:
            visited[node] = cost
            
            # Explore the neighbors
            for neighbor, edge_cost in graph[node]:
                new_cost = cost + edge_cost
                new_path = path + [neighbor]
                heapq.heappush(queue, (new_cost, new_path))
    
    # If no path is found
    return None, float('inf')

# Depth First Search (DFS) Implementation
def dfs(graph, start, end, path=None):
    if path is None:
        path = []
    
    path.append(start)
    
    if start == end:
        return path
    
    for neighbor in graph[start]:
        if neighbor not in path:
            result = dfs(graph, neighbor, end, path.copy())
            if result is not None:
                return result

    return None

# Breadth First Search (BFS) Implementation
def bfs(graph, start, end):
    queue = deque([[start]])
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        if node == end:
            return path
        
        for neighbor in graph[node]:
            new_path = list(path)
            new_path.append(neighbor)
            queue.append(new_path)

    return None


# User input for start and end nodes
start_node = input("Enter the start node: ").strip().upper()
end_node = input("Enter the end node: ").strip().upper()

# Check if nodes exist in the graph
if start_node not in graph or end_node not in graph:
    print("Invalid start or end node.")
else:
    # Perform DFS
    dfs_path = dfs(graph, start_node, end_node)
    print(f"DFS Path from {start_node} to {end_node}: {dfs_path if dfs_path else 'No path found'}")

    # Perform BFS
    bfs_path = bfs(graph, start_node, end_node)
    print(f"BFS Path from {start_node} to {end_node}: {bfs_path if bfs_path else 'No path found'}")

    # Perform UCS
    ucs_path, ucs_cost = ucs(graph2, start_node, end_node)
    print(f"UCS Path from {start_node} to {end_node}: {ucs_path if ucs_path else 'No path found'} with cost {ucs_cost}")
