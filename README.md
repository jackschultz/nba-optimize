# nba-optimize

Code that show how to optimize a Daily Fantasy Sports (DFS) NBA lineup, which is a version of a knapsack problem.

Three files included, `basic_optimize.py`, `brisk_optimize.py`, and `fast_optimize.py` each show different ways to perform the optimization.

I included a couple csv data files for us to use. I used other code to get the data from nba.com and the info from FanDuel csv files that list the players and their salaries.

I'm assuming you'll have a virtualenv running python3. If so, run the following:

```
(nbaoptimize) $ pip install -r requirements
  .....
(nbaoptimize) $ python fast_optimize.py 2018-10-24
```

where the second argument is the data file to use.
