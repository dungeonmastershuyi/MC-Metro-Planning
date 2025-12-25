# MC-Metro-Planning
Based on an integer point city map, this repository will generate different plannings of metro lines, and test them within the system to find the best planning(s).

## Description
Input the city map, and the **solver** will generate a metro system for the city. Then, the **simulator** will test the system with random values of a set of passengers with:
*   Spawn time
*   Spawn location
*   Destination

It then outputs a "run form" with criteria on how well the metro system did. Under a refined **Monte Carlo method**, the solver will eventually provide a near-optimal metro system for the city.

To give more freedom for the user, the test set of passengers is also customizable. To have the case closer to real-life usages, certain parameters are also customizable.

## Prerequisites
This repository uses **Python 3**.
*   `pandas` (External library)
*   `math` (Standard library)
