# A Parallel Processing Implementation of the Floyd-Warshall Algorithm for Optimizing Shortest Transportation Routes Between U.S. Cities

## Brief description
The **PIDP-project** contains the source code for calculating the shortest distances in a transportation network connecting 300 U.S. cities.
It includes two distinct implementations of the Floyd-Warshall (FW) algorithm:
- The serial implementation (located in the **MainProject** directory)
- The parallel implementation using OpenMP (located in the **parallel-aproach** directory)

For this project, various tools and libraries were used to enable efficient parallel processing and data handling:
- **OpenMP** is utilized for key computational tasks, leveraging multiple CPU threads to maximize performance.
- The connection between C and Python is facilitated through a shared **Dynamic Link Library (DLL)**. This DLL, built from a single C function, performs the core distance matrix calculations, optimizing the Floyd-Warshall algorithm for parallel execution.
- The **ctypes** module in Python allows seamless interaction with the DLL, enabling efficient integration between the two languages.

The primary storage system for distances between 300 U.S. cities is an **SQLite database**.
- The database schema is defined using SQL DDL statements, creating tables such as **cities** and **distances**, which store pairwise city distances and city metadata, respectively.

## Project Structure
```
├── MainProject/                      
│   ├── Results.xlsx                  # An excel file containing the time performances between the Serial vs the Parallel imp.
│   ├── main-program.py               # Sequential implementation of the FW algorithm
│   ├── parallel_aproach.py           # A python file for calling the parallel implementation of the FW algorithm
│   ├── performance_comparison.png    # Visual description of Results.xlsx
├── parallel-aproach/
│   ├── parallel-aproach/
│       ├── parallel-aproach.cpp      # A cpp file containing the parallel implementation of the FW algorithm   
├── us-cities.db
|   ├── cities.sql                    # Contains the city name and the name of the state where the city is located
|   ├── distances.sql                 # Contains the pairwise city distances
├── README.md                         # Documentation
```

## Running the serial implementation of the FW algorithm
```sh
python main-program.py
```

## Running the parallel implementation of the FW algorithm

1. Inside the parallel-aproach directory open the **parallel-aproach.sln** file on Visual Studio 2022.
2. In Visual Studio, go to the **Build** menu and click on **Build Solution**.
3. After the file is successfully build or rebuild, now you need to open the **parallel_aproach.py** file inside the **MainProject** directory.
4. Inside the **parallel_approach.py** file, on line 63, replace the URL path of parallel_approach.dll with the local file path on your machine.
5. Then you can run this command:
```sh
   python parallel_approach.py
```
