// parallel-aproach.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include <omp.h>
#include <stdio.h>
#include <limits.h>
#include <float.h>
#include <cstdint> 
const float INFINITE_DISTANCE = 1000000000;

extern "C" {
    __declspec(dllexport) void process_matrix(float* input_matrix,int32_t* next_node_matrix, float* output_matrix, int n) {
        for (int k = 0; k < n; ++k) {
            #pragma omp parallel for num_threads(n) schedule(dynamic) collapse(2)
            for (int i = 0; i < n; ++i) {
                for (int j = 0; j < n; ++j) {
                    float new_dist = input_matrix[i * n + k] + input_matrix[k * n + j];
                    if (input_matrix[i * n + j] > new_dist) {
                        input_matrix[i * n + j] = new_dist;
                        next_node_matrix[i * n + j] = next_node_matrix[i * n + k];
                    }
                }
            }
        }

        #pragma omp parallel for
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                output_matrix[i * n + j] = input_matrix[i * n + j];
            }
        }
    }
    __declspec(dllexport) void process_social_matrix(float* input_matrix, float* output_matrix, int n) {
        for (int k = 0; k < n; ++k) {
            #pragma omp parallel for num_threads(n) schedule(dynamic) collapse(2)
            for (int i = 0; i < n; ++i) {
                for (int j = 0; j < n; ++j) {
                    if (i == j) {
                        continue;
                    }
                    float new_dist = input_matrix[i * n + k] * input_matrix[k * n + j];
                    if (input_matrix[i * n + j] < new_dist) {
                        input_matrix[i * n + j] = new_dist;
                    }
                }
            }
        }

        #pragma omp parallel for
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                output_matrix[i * n + j] = input_matrix[i * n + j];
            }
        }
    }
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
