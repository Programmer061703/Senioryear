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

### YOUR CODE HERE ###
# Heuristic values: FILL IN THE VALUES
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
### END YOUR CODE ###

# Greedy Search
def greedy_search(graph, heuristic, start, goal):
    # Initialize the frontier with the start node and its heuristic value
    frontier = [(heuristic[start], start)]
    explored = set()  # To keep track of explored nodes

    while frontier:
        # Select the node with the lowest heuristic value
        _, current_node = heapq.heappop(frontier)

        if current_node == goal:
            return f"Goal reached: {current_node}"

        explored.add(current_node)

        # Expand the node
        for neighbor, _ in graph[current_node]:
            if neighbor not in explored:
                heapq.heappush(frontier, (heuristic[neighbor], neighbor))

    return "Goal not reachable"


# A Search (A* Search)
def a_search(graph, heuristic, start, goal):
    # Initialize the frontier with the start node, its cumulative cost, and heuristic value
    frontier = [(heuristic[start], 0, start)]
    explored = set()  # To keep track of explored nodes
    costs = {start: 0}  # Track the cost of reaching each node

    while frontier:
        _, current_cost, current_node = heapq.heappop(frontier)

        if current_node == goal:
            return f"Goal reached: {current_node}, Total cost: {current_cost}"

        explored.add(current_node)

        # Expand the node
        for neighbor, cost in graph[current_node]:
            new_cost = current_cost + cost

            if neighbor not in explored or new_cost < costs.get(neighbor, float('inf')):
                costs[neighbor] = new_cost
                total_cost = new_cost + heuristic[neighbor]
                heapq.heappush(frontier, (total_cost, new_cost, neighbor))

    return "Goal not reachable"


# Test the functions
print(greedy_search(graph, heuristic, 'S', 'G'))  # Output should indicate reaching the goal
print(a_search(graph, heuristic, 'S', 'G'))  # Output should indicate reaching the goal and the cost
