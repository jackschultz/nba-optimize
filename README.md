# nba-optimize
Code that show how to optimize a DFS NBA lineup, which is a version of a knapsack problem

Three files included, `slow_optimize.py`, `brisk_optimize.py`, and `quick_optimize.py` each show different ways to perform the optimization.

I included a couple csv data files for us to use. I used other code to get the data from nba.com and the info from FanDuel csv files that list the players and their salaries.

To run, pip install the requirements for python3, and then run:

`$ python quick_optimize.py 2019-01-09`, where the second argument is the data file to use.
