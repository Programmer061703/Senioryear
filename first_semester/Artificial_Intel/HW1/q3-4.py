from collections import deque
import heapq


graph = {
    'A': ['D'],
    'B': ['A', 'E'],
    'C': ['G', 'E'],
    'D': ['C'],
    'E': [],
    'S': ['D','A' , 'B' ],
    'G': []
}


graph2 = {
    'A': [('D', 1)],
    'B': [('A', 3), ('E', 4)],
    'C': [('G', 1), ('E', 3)],
    'D': [('C', 1)],
    'E': [],
    'S': [('D', 4), ('A', 2), ('B', 2)],
    'G': []
}

graph3 = {
    'S': ['F', 'T'],
    'F': ['N'],
    'T': ['P', 'O'],
    'N': ['Q'],
    'P': ['N', 'M', 'D'],
    'O': ['O', 'D'],
    'Q': [],
    'D': [],
    'M': ['G'],
    'G': []
}

graph4 = {
    'S': [('F', 4), ('T', 1)],
    'F': [('N', 1)],
    'T': [('P', 2), ('O', 3)],
    'N': [('Q', 2)],
    'P': [('N', 1), ('M', 1), ('D', 2)],
    'O': [('O', 1), ('D', 3)],
    'Q': [],
    'D': [],
    'M': [('G', 1)],
    'G': []
}


def ucs(graph, start, end):
    queue = [(0, [start])]
    visited = {}
    search_table = []
    expansion_order = []  

    while queue:
        cost, path = heapq.heappop(queue)
        node = path[-1]
        

        if node not in expansion_order:
            expansion_order.append(node)
        

        search_table.append({
            'Node': node,
            'Parent': path[-2] if len(path) > 1 else None,
            'Cost': cost,
            'Path': path
        })

        if node == end:
            return search_table, expansion_order

        if node not in visited or cost < visited[node]:
            visited[node] = cost
            for neighbor, edge_cost in graph[node]:
                new_cost = cost + edge_cost
                new_path = path + [neighbor]
                heapq.heappush(queue, (new_cost, new_path))

    return search_table, expansion_order


def dfs(graph, start, end, path=None, search_table=None, expansion_order=None):
    if path is None:
        path = []
    if search_table is None:
        search_table = []
    if expansion_order is None:
        expansion_order = []

    path.append(start)


    if start not in expansion_order:
        expansion_order.append(start)
    

    search_table.append({
        'Node': start,
        'Parent': path[-2] if len(path) > 1 else None,
        'Path': path
    })

    if start == end:
        return search_table, expansion_order

    for neighbor in graph[start]:
        if neighbor not in path:

            result = dfs(graph, neighbor, end, path.copy(), search_table, expansion_order)

            if result is not None:
                return result


    return None


def bfs(graph, start, end):
    queue = deque([[start]])
    search_table = []
    visited = set()
    expansion_order = []  

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node not in expansion_order:
            expansion_order.append(node)


        search_table.append({
            'Node': node,
            'Parent': path[-2] if len(path) > 1 else None,
            'Path': path
        })

        if node == end:
            return search_table, expansion_order

        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return search_table, expansion_order


graph_selection = input("Enter the graph to use (1 or 2): ").strip()


start_node = input("Enter the start node: ").strip().upper()
end_node = input("Enter the end node: ").strip().upper()


if graph_selection == '1':
    dfs_table, dfs_expansion_order = dfs(graph, start_node, end_node)
    print(f"DFS Graph 1 Search Table from {start_node} to {end_node}:")
    for row in dfs_table:
        print(row)
    print(f"DFS Node Expansion Order: {dfs_expansion_order}\n")

    bfs_table, bfs_expansion_order = bfs(graph, start_node, end_node)
    print(f"BFS Graph 1 Search Table from {start_node} to {end_node}:")
    for row in bfs_table:
        print(row)
    print(f"BFS Node Expansion Order: {bfs_expansion_order}\n")

    ucs_table, ucs_expansion_order = ucs(graph2, start_node, end_node)
    print(f"UCS Graph 1 Search Table from {start_node} to {end_node}:")
    for row in ucs_table:
        print(row)
    print(f"UCS Node Expansion Order: {ucs_expansion_order}\n")
else:
    dfs_table, dfs_expansion_order = dfs(graph3, start_node, end_node)
    print(f"DFS Graph 2 Search Table from {start_node} to {end_node}:")
    for row in dfs_table:
        print(row)
    print(f"DFS Node Expansion Order: {dfs_expansion_order}\n")

    bfs_table, bfs_expansion_order = bfs(graph3, start_node, end_node)
    print(f"BFS Graph 2 Search Table from {start_node} to {end_node}:")
    for row in bfs_table:
        print(row)
    print(f"BFS Node Expansion Order: {bfs_expansion_order}\n")

    ucs_table, ucs_expansion_order = ucs(graph4, start_node, end_node)
    print(f"UCS Graph 2 Search Table from {start_node} to {end_node}:")
    for row in ucs_table:
        print(row)
    print(f"UCS Node Expansion Order: {ucs_expansion_order}\n")


