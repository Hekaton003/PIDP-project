# A Parallel Processing Implementation of the Floyd-Warshall Algorithm for Optimizing Shortest Transportation Routes Between U.S. Cities

## Brief description
The PIDP-project calculates the shortest distances in a transportation network connecting 950 U.S. cities. It also calculates the strength of social connections between 1900 random people in these cities.
The project includes:
- The serial implementation of the FW (located in the **MainProject** directory)
- The parallel implementation of the FW using OpenMP (located in the **parallel-aproach** directory)

For this project, various tools and libraries were used to enable efficient parallel processing and data handling:
- **OpenMP** is utilized for key computational tasks, leveraging multiple CPU threads to maximize performance.
- The connection between C and Python is facilitated through a shared **Dynamic Link Library (DLL)**. This DLL, built from a single C function, performs the core distance matrix calculations, optimizing the Floyd-Warshall algorithm for parallel execution.
- The **ctypes** module in Python allows seamless interaction with the DLL, enabling efficient integration between the two languages.

The primary storage system forthis project is an **SQLite database**.
- The database schema, defined using SQL DDL statements, includes tables such as **cities** and **distances** for storing city metadata and pairwise city distances, respectively, as well as **Friend** and **Friendship** tables for managing the social network data.

![The Entity Relation Diagram of the us-cities.db](https://drive.usercontent.google.com/download?id=1fIih_oUdFxqWFERXnZEY9IcyyQt0fWlZ&export=view&authuser=0)
<p align="center"><i>Figure 1: Entity-Relationship Diagram of the <code>us-cities.db</code> database.</i></p>

## Project Structure
```                   
├── Results.xlsx                          # An excel file containing time performances between the Serial vs the Parallel imp of the Floyd-Warshall algorithm.
├── city-distances-results/               # A subdirectory that contains the initial distance matrices for 40 and 80 cities, the final distance matrices after the Floyd-Warshall implementation,
                                          and text files containing the shortest paths between each pair of cities.
├── city-social-connection-results/       # A subdirectory that contains the initial social connection matrices for 40 and 80 cities, the final social connection matrices  after the Floyd-Warshall implementation.
├── friendship-connection-results/        # A subdirectory that contains the initial social connection matrices for 40 and 80 random people, the final social connection matrices after the Floyd-Warshall implementation.
├── real-data/                            # A subdirectory that contains a text file with 300 different users from the Stanford Gowalla social network dataset,
                                          along with their friendship connections and the resulting social distance matrix between cities based on where the users live.
├── main-program-cityDistance.py          # Sequential implementation of the FW algorithm for calculating the road distances between the cities.
├── parallel-aproach-cityDistance.py      # A python file for calling the parallel implementation of the FW algorithm for calculating the road distances between the cities.
├── main-program-citySocialConnections.py # Sequential implementation of the FW algorithm for calculating the social connections between the cities.
├── parallel-aproach-citySocialConnections.py   # A python file for calling the parallel implementation of the FW algorithm for calculating the social connections between the cities.
├── main-program-friendships.py           # Sequential implementation of the FW algorithm for calculating the social connections between random people.
├── parallel-aproach-friendships.py       # A python file for calling the parallel implementation of the FW algorithm for calculating the social connections between random people.
├── parallel-aproach/
│   ├── parallel-aproach/
│       ├── parallel-aproach.cpp      # A cpp file containing the parallel implementation of the FW algorithm   
├── us-cities.db
|   ├── cities.sql                    # Contains the city name and the name of the state where the city is located
|   ├── distances.sql                 # Contains the pairwise city distances
|   ├── Friend.sql                    # Data for random people in the social network.
|   ├── Friendship.sql                # Pairwise friendship data.
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
