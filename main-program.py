import sqlite3

import pandas as pd
import time

INFINITE_DISTANCE = 1000000000


def Floyd_Warshall(matrix: dict, cities: list, next_node: dict):
    for k in cities:
        for i in cities:
            if matrix[i][k] >= INFINITE_DISTANCE:
                continue  # Skip infinite distances
            for j in cities:
                if matrix[k][j] >= INFINITE_DISTANCE:
                    continue
                distance = matrix[i][k] + matrix[k][j]
                if distance < matrix[i][j]:
                    matrix[i][j] = distance
                    next_node[i][j] = next_node[i][k]

    return matrix, next_node


def fetching_data(n: int):
    conn = sqlite3.connect('us-cities.db')
    cursor = conn.cursor()
    cities = set()
    querry = """SELECT c.city_name cityFrom,c.city_state state,c1.city_name cityTo,c1.city_state state, distances.distance  FROM distances
    JOIN cities c ON distances.city_id_one = c.id
    JOIN cities c1 ON distances.city_id_two = c1.id
    WHERE city_id_one<=? and  city_id_two<=?"""
    cursor.execute(querry, (n, n))
    rows = cursor.fetchall()
    for row in rows:
        if row[0] not in cities or row[2] not in cities:
            cities.add(f'{row[0]}({row[1]})')
            cities.add(f'{row[2]}({row[3]})')

    distance_matrix = {city: {city: INFINITE_DISTANCE for city in cities} for city in cities}
    for row in rows:
        distance_matrix[f'{row[0]}({row[1]})'][f'{row[2]}({row[3]})'] = row[4]
        distance_matrix[f'{row[2]}({row[3]})'][f'{row[0]}({row[1]})'] = row[4]
        distance_matrix[f'{row[0]}({row[1]})'][f'{row[0]}({row[1]})'] = 0
        distance_matrix[f'{row[2]}({row[3]})'][f'{row[2]}({row[3]})'] = 0
    conn.close()
    return distance_matrix, list(cities)


def reconstruct_path(next_node, start, end):
    if next_node[start][end] is None:
        return None  # No path exists
    path = [start]
    while start != end:
        if start is None:
            return None
        start = next_node[start][end]
        path.append(start)
    return path


if __name__ == '__main__':
    n = int(input())
    matrix, cities = fetching_data(n)
    df = pd.DataFrame.from_dict(matrix, orient='index', columns=cities)
    df.to_csv(f'initial_distances-s-{n}.csv')
    next_node = {city: {city: None for city in cities} for city in cities}
    for i in cities:
        for j in cities:
            if matrix[i][j] != float('inf') and i != j:
                next_node[i][j] = j
            elif matrix[i][j] == 0 and i == j:
                next_node[i][j] = i

    start_time = time.perf_counter()
    final_matrix, next_node = Floyd_Warshall(matrix, cities, next_node)
    end_time = time.perf_counter()
    df_final = pd.DataFrame.from_dict(final_matrix, orient='index', columns=cities)
    df_final.to_csv(f'final_distances-s-{n}.csv')
    time_taken = end_time - start_time
    print(f'{time_taken:} seconds')
    with open(f"shortest-paths-s-{n}.txt", "w") as file:
        for i in cities:
            for j in cities:
                path = reconstruct_path(next_node, i, j)
                file.write(f'Path from {i} to {j} -> {path}\n')
                file.write('-' * 50 + '\n')
