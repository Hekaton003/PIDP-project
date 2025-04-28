import ctypes
import sqlite3

import numpy as np
import pandas as pd
import time

INFINITE_DISTANCE = 1000000000


def reconstruct_path(next_node, start, end, max_steps=10000):
    if next_node[start][end] is None:
        return None  # No path exists
    path = [start]
    step = 0
    while start != end:
        if start is None or step >= max_steps:
            return None
        start = next_node[start][end]
        path.append(start)
        step += 1
    return path


def fetching_data(n: int):
    conn = sqlite3.connect('us-cities.db')
    cursor = conn.cursor()
    cities = set()
    querry = """SELECT c.city_name cityFrom,c.city_state state,c1.city_name cityTo,c1.city_state state, distances.distance FROM distances
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
    return [distance_matrix, cities]


if __name__ == '__main__':
    n = int(input())
    distance_matrix, cities = fetching_data(n)
    cities = list(cities)
    next_node = {city: {city: None for city in cities} for city in cities}
    for i in cities:
        for j in cities:
            if distance_matrix[i][j] != INFINITE_DISTANCE and i != j:
                next_node[i][j] = j
            elif distance_matrix[i][j] == 0 and i == j:
                next_node[i][j] = i

    df = pd.DataFrame.from_dict(distance_matrix, orient='index', columns=cities)
    df.to_csv(f'initial_distances-p-{n}.csv')
    # Initialize the input_matrix with float32 dtype
    input_matrix = np.zeros((n, n), dtype=np.float32)
    next_node_matrix = np.full((n, n), -1, dtype=np.int32)
    # Fill the input_matrix with values from distance_matrix
    for i, city in enumerate(cities):
        for j, city2 in enumerate(cities):
            input_matrix[i, j] = np.float32(distance_matrix[city][city2])
            if i == j:
                next_node_matrix[i, j] = i  # Diagonal points to self
            elif distance_matrix[city][city2] < INFINITE_DISTANCE:
                next_node_matrix[i, j] = j  # Point to destination if direct path exists
            else:
                next_node_matrix[i, j] = -1.0

    output_matrix = input_matrix.copy()
    # This should now print "float32"
    lib = ctypes.CDLL(
        r'C:\Users\Jovan\OneDrive\Documents\Real-Doc\Pidp\MainProject\parallel-aproach\x64\Debug\parallel-aproach.dll')
    print("Library loaded successfully!")
    print(next_node_matrix.dtype)
    inp_ptr = input_matrix.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    next_ptr = next_node_matrix.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
    out_ptr = output_matrix.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    # Check if the function is accessible
    if hasattr(lib, 'process_matrix'):
        print("Function 'process_matrix' is available.")
    else:
        print("Function 'process_matrix' is not found.")

    # Test the function with an argument
    try:
        start_time = time.perf_counter()
        lib.process_matrix(inp_ptr, next_ptr, out_ptr, n)
        end_time = time.perf_counter()
        print("Function 'process_matrix' is successfully executed.")
        i = 0
        j = 0
        for city in cities:
            for city2 in cities:
                distance_matrix[city][city2] = output_matrix[i][j]
                node_index = next_node_matrix[i][j]
                if node_index >= len(cities):  # No path exists
                    next_node[city][city2] = None
                else:
                    next_node[city][city2] = cities[node_index]
                j += 1
            i += 1
            j = 0
        df = pd.DataFrame.from_dict(distance_matrix, orient='index', columns=cities)
        df.to_csv(f'final_distances-p-{n}.csv')
        print(f"Total execution time: {end_time - start_time:.6f} seconds")
    except Exception as e:
        print(f"Function call failed: {e}")

    with open(f"shortest-paths-p-{n}.txt", "w") as file:
        for i in cities:
            for j in cities:
                path = reconstruct_path(next_node, i, j)
                file.write(f'Path from {i} to {j} -> {path}\n')
                file.write('-' * 50 + '\n')
