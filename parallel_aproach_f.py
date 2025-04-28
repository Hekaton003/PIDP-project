import ctypes
import sqlite3

import numpy as np
import pandas as pd
import time


def fetching_data(n: int):
    conn = sqlite3.connect('us-cities.db')
    cursor = conn.cursor()
    friends = set()
    querry = """SELECT f1.name,f2.name,weight FROM Friendship
    JOIN Friend f1 ON Friendship.friend1_id = f1.id
    JOIN Friend f2 ON Friendship.friend2_id = f2.id
    WHERE friend1_id<=? and  friend2_id<=?;"""
    cursor.execute(querry, (n, n))
    rows = cursor.fetchall()
    for row in rows:
        if row[0] not in friends or row[1] not in friends:
            friends.add(f'{row[0]}')
            friends.add(f'{row[1]}')

    distance_matrix = {friend: {friend: 0 for friend in friends} for friend in friends}
    for row in rows:
        distance_matrix[f'{row[0]}'][f'{row[1]}'] = row[2]
    conn.close()
    return distance_matrix, list(friends)


if __name__ == '__main__':
    n = int(input())
    distance_matrix, friends = fetching_data(n)
    next_node = {friend: {friend: None for friend in friends} for friend in friends}
    for i in friends:
        for j in friends:
            if distance_matrix[i][j] != 0 and i != j:
                next_node[i][j] = j
            elif distance_matrix[i][j] == 0 and i == j:
                next_node[i][j] = i

    df = pd.DataFrame.from_dict(distance_matrix, orient='index', columns=friends)
    df.to_csv(f'initial_friend_distances-p-{n}.csv')
    # Initialize the input_matrix with float32 dtype
    input_matrix = np.zeros((n, n), dtype=np.float32)
    for i, city in enumerate(friends):
        for j, city2 in enumerate(friends):
            input_matrix[i, j] = np.float32(distance_matrix[city][city2])

    output_matrix = input_matrix.copy()
    # This should now print "float32"
    lib = ctypes.CDLL(
        r'C:\Users\Jovan\OneDrive\Documents\Real-Doc\Pidp\MainProject\parallel-aproach\x64\Debug\parallel-aproach.dll')
    print("Library loaded successfully!")
    inp_ptr = input_matrix.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    out_ptr = output_matrix.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    # Check if the function is accessible
    if hasattr(lib, 'process_social_matrix'):
        print("Function 'process_matrix' is available.")
    else:
        print("Function 'process_matrix' is not found.")

    # Test the function with an argument
    try:
        start_time = time.perf_counter()
        lib.process_social_matrix(inp_ptr, out_ptr, n)
        end_time = time.perf_counter()
        print("Function 'process_matrix' is successfully executed.")
        i = 0
        j = 0
        for friend in friends:
            for friend2 in friends:
                distance_matrix[friend][friend2] = output_matrix[i][j]
                j += 1
            i += 1
            j = 0
        df = pd.DataFrame.from_dict(distance_matrix, orient='index', columns=friends)
        df.to_csv(f'final_friend_distances-p-{n}.csv')
        print(f"Total execution time: {end_time - start_time:.6f} seconds")
    except Exception as e:
        print(f"Function call failed: {e}")
