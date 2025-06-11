from collections import defaultdict

import numpy as np
import pandas as pd
import time


def Floyd_Warshall(matrix: dict, cities: list):
    for k in cities:
        for i in cities:
            for j in cities:
                if i == j:
                    continue
                distance = matrix[i][k] * matrix[k][j]
                if distance > matrix[i][j]:
                    matrix[i][j] = distance

    return matrix


def fetching_data():
    matrix = np.zeros(shape=(301, 301), dtype=int)
    with open('edges.txt', 'r') as f:
        for line in f:
            lineF = line.strip().split('\t')
            if len(lineF) == 2:
                user1,user2 = int(lineF[0]), int(lineF[1])
                matrix[user1][user2] = 1
    return matrix


def build_city_matrix(matrix, city_file_path):
    user_city = {}
    city_users = defaultdict(set)

    with open(city_file_path, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                user_id, city = int(parts[0]), parts[1]
                user_city[user_id] = city
                city_users[city].add(user_id)

    city_connections = defaultdict(lambda: defaultdict(int))
    city_pair_counts = defaultdict(lambda: defaultdict(int))

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] == 1:
                cityA = user_city.get(i)
                cityB = user_city.get(j)
                if cityA and cityB:
                    city_connections[cityA][cityB] += 1
                    city_pair_counts[cityA][cityB] += 1

    city_avg_matrix = defaultdict(dict)
    for cityA in city_connections:
        for cityB in city_connections:
            total_connections = city_connections[cityA][cityB]
            num_users_A = len(city_users[cityA])
            num_users_B = len(city_users[cityB])
            if num_users_A > 0 and num_users_B > 0:
                # Average friendships per possible user pair
                avg = total_connections / (num_users_A * num_users_B)
                if cityA == cityB:
                    city_avg_matrix[cityA][cityB] = 0.0
                elif cityA != cityB:
                    city_avg_matrix[cityA][cityB] = avg
            else:
                city_avg_matrix[cityA][cityB] = 0.0
    return city_avg_matrix


if __name__ == '__main__':
    friendship = fetching_data()
    cities = build_city_matrix(friendship, 'user_most_visited_city.txt')
    df = pd.DataFrame.from_dict(cities, orient='index', columns=list(cities.keys()))
    df.to_csv(f'initial_cities_distances-s.csv')
    final_matrix = Floyd_Warshall(cities, list(cities.keys()))
    df_final = pd.DataFrame.from_dict(final_matrix, orient='index', columns= list(cities.keys()))
    df_final.to_csv(f'final_cities_distances-s.csv')
