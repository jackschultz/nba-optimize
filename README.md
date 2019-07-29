# nba-optimize

Code that show how to optimize a Daily Fantasy Sports (DFS) NBA lineup, which is a version of a knapsack problem.

[Assiciated blog post where I talk about the code](https://bigishdata.com/2019/07/28/optimizing-a-daily-fantasy-sports-nba-lineup-knapsack-numpy-and-giannis/).

Three files included, `basic_optimize.py`, `brisk_optimize.py`, and `fast_optimize.py` each show different ways to perform the optimization.

I included csv data files for us to use. I used other code to get the data from nba.com and the info from FanDuel csv files that list the players and their salaries.

I'm assuming you'll have a virtualenv running python3. If so, run the following:

```
(nbaoptimize) $ pip install -r requirements
  .....
(nbaoptimize) $ python fast_optimize.py 2018-10-24
```

where the second argument is the data file to use.

Three files are also included to show examples of how the three solutions were done using Jupyter notebooks: `example_basic_optimize.ipynb`, `example_brisk_optimize.ipynb`, and `example_fast_optimize.ipynb`.

To run the Jupyter notebooks, instead of looking at the files here, run
```
$ jupyter notebook
```
which opens a new tab in browser where you can click the notebook files and run them yourself.
