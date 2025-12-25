# MC-Metro-Planning
Based on an integer point city map, this repository will generate different plannings of metro lines, and test them within the system to find the best planning(s).

## Description
Input the city map, and the **solver** will generate a metro system for the city. Then, the **simulator** will test the system with random values of a set of passengers with:
*   Spawn time
*   Spawn location
*   Destination

It then outputs a "run form" with criteria on how well the metro system did. Under a refined **Monte Carlo method**, the solver will eventually provide a near-optimal metro system for the city.
To give more freedom for the user, the test set of passengers is also customizable. To have the case closer to real-life usages, certain parameters are also customizable.

### Detailed Description
This repository consists of 5 main files:

#### `determine_lines.py`
The "solver" actually only gives the ordered set of stations in lines. In `determine_path`, the stations will connect based on greedy heuristic principles of minimizing a certain objective function: `min f = 1/w + sld`.
*   **w**: weight of the integer point
*   **sld**: straight line distance between the integer point and the straight line between 2 adjacent stations

#### `simulation.py`
After getting the complete metro lines, a set of passengers will be put in to test it, then output results of that set of passengers.

#### `montecarlo.py`
Generates different sets of passengers to put into `simulation.py`.

#### `evaluation.py`
Evaluates all corresponding results from all sets of passenger inputs. It visualizes and determines how well the solver did, giving feedback to the solver to refine the next planning.

#### `main.py`
Handles all files and orchestrates the process.

## Prerequisites
This repository uses **Python 3**.
*   `pandas` (External library)
*   `math` (Standard library)
