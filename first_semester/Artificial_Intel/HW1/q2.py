from collections import deque


dx = [0, 0, -1, 1]
dy = [-1, 1, 0, 0]

def is_valid(x, y, m, n, matrix, visited):
    return 0 <= x < m and 0 <= y < n and matrix[x][y] == 1 and not visited[x][y]

def print_path(path):
    for i in range(len(path)):
        if i > 0:
            print("-->", end="")
        print(f"({path[i][0]},{path[i][1]})", end="")
    print()


def bfs(m, n, matrix):
    visited = [[False for _ in range(n)] for _ in range(m)]
    queue = deque()
    

    queue.append((0, 0, [(0, 0)]))  # (x, y, path)
    visited[0][0] = True

    while queue:
        x, y, path = queue.popleft()


        if x == m - 1 and y == n - 1:
            print_path(path)
            return

        # Explore all 4 possible directions (up, down, left, right)
        for i in range(4):
            new_x, new_y = x + dx[i], y + dy[i]

            # If the new position is valid, enqueue it with the updated path
            if is_valid(new_x, new_y, m, n, matrix, visited):
                visited[new_x][new_y] = True
                queue.append((new_x, new_y, path + [(new_x, new_y)]))

    print("-1")


def dfs(m, n, matrix):
    visited = [[False for _ in range(n)] for _ in range(m)]
    stack = deque()

    stack.append((0, 0, [(0, 0)]))  # (x, y, path)
    visited[0][0] = True

    while stack:
        x, y, path = stack.pop()

        if x == m - 1 and y == n - 1:
            print_path(path)
            return

        # Explore all 4 possible directions (up, down, left, right)
        for i in range(4):
            new_x, new_y = x + dx[i], y + dy[i]

            # If the new position is valid, push it with the updated path
            if is_valid(new_x, new_y, m, n, matrix, visited):
                visited[new_x][new_y] = True
                stack.append((new_x, new_y, path + [(new_x, new_y)]))

    print("-1")



# Example usage
matrix = [
    [1, 1, 1, 0, 1],
    [0, 0, 1, 1, 0],
    [0, 1, 1, 1, 1],
    [1, 1, 0, 1, 0],
    [0, 1, 0, 1, 1]
]


m = len(matrix)
n = len(matrix[0])
print("BFS:")
bfs(m, n, matrix)
print("\nDFS:")
dfs(m, n, matrix)




