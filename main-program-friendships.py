import pandas as pd
import time
import sqlite3


def Floyd_Warshall(matrix: dict, friends: list):
    for k in friends:
        for i in friends:
            for j in friends:
                if i == j:
                    continue
                distance = matrix[i][k] * matrix[k][j]
                if distance > matrix[i][j]:
                    matrix[i][j] = distance

    return matrix


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
    matrix, friends = fetching_data(n)
    df = pd.DataFrame.from_dict(matrix, orient='index', columns=friends)
    df.to_csv(f'initial_friend_distances-s-{n}.csv')
    next_node = {friend: {friend: None for friend in friends} for friend in friends}
    for i in friends:
        for j in friends:
            if matrix[i][j] != 0 and i != j:
                next_node[i][j] = j
            elif matrix[i][j] == 0 and i == j:
                next_node[i][j] = i

    start_time = time.perf_counter()
    final_matrix = Floyd_Warshall(matrix,friends)
    end_time = time.perf_counter()
    df_final = pd.DataFrame.from_dict(final_matrix, orient='index', columns=friends)
    df_final.to_csv(f'final_friend_distances-s-{n}.csv')
    time_taken = end_time - start_time
    print(f'{time_taken:} seconds')
