import sys
import itertools

from utils import time_and_slow_calls

import numpy as np
import pandas as pd
import pdb
pry = pdb.set_trace

def calculate_position_combination(test_salary, num_players, costs, points, posdf_indicies):

    #splitting the data fram into the necessary fields
    #Note that we're using the combinations of the players so that we don't
    #have a test with the same player.
    inds_comb = np.array(list(itertools.combinations(posdf_indicies, num_players)))
    cost_comb = np.array(list(itertools.combinations(costs, num_players)))
    points_comb = np.array(list(itertools.combinations(points, num_players)))

    #creating an array where we add the costs together to get a 1d array
    cost_sum = cost_comb.sum(axis=1)

    under_cost_limit = cost_sum <= test_salary

    #adding the points of the combinations and making them zero if the salary sum is
    #higher than the test_salary
    points_sum = points_comb.sum(axis=1) * under_cost_limit

    #KEY LINE: we're finding the max indicies
    #argmax() returns the index of the max value
    max_ind = np.unravel_index(points_sum.argmax(), points_sum.shape)

    #now that we know the index of the maximum, we return the relevant info
    max_points = points_comb[max_ind].sum()
    max_cost = cost_comb[max_ind].sum()
    top_inds = inds_comb[max_ind]
    return test_salary, top_inds, max_points, max_cost

def combine_single_position(position, num_players, df):

    posdf = df[df.pos == position]
    posdf_indicies = posdf.index.values
    points = posdf['pts'].values
    costs = posdf['sal'].values

    cost_ranges = range(3500*num_players, 12000*num_players, 100)
    return [calculate_position_combination(test_salary, num_players, costs, points, posdf_indicies) for test_salary in cost_ranges]

def calculate_max_points(pos1, pos2, test_salary):

    costs = np.array([cost for _,_,_,cost in pos1])
    costs2 = np.array([cost for _,_,_,cost in pos2])

    points = np.array([point for _,_,point,_ in pos1])
    points2 = np.array([point for _,_,point,_ in pos2])

    ids = np.array([ind for _,ind,_,_ in pos1])
    ids2 = np.array([ind for _,ind,_,_ in pos2])

    #combining the two arrays to create a full testable combinations
    full_costs = costs[:, np.newaxis] + costs2
    full_points = points[:, np.newaxis] + points2

    valids = full_costs <= test_salary
    possibilites = full_points * valids
    x, y = np.unravel_index(possibilites.argmax(), possibilites.shape)

    max_points = full_points[x,y]
    max_costs = full_costs[x,y]
    max_inds = np.concatenate([ids[x], ids2[y]])

    return test_salary, max_inds, max_points, max_costs

def combine_multiple_positions(pos1, pos2, num_players):

    cost_ranges = range(3500*num_players, 60000+100, 100)
    return [calculate_max_points(pos1, pos2, test_salary) for test_salary in cost_ranges]

def combine_all_positions(tops_array):

    tops_array_len = len(tops_array)
    if tops_array_len == 1:
        return tops_array[0]
    else:
        half_len = tops_array_len // 2 #we want this non floating
        half1 = tops_array[:half_len]
        half2 = tops_array[half_len:]
        half1top = combine_all_positions(half1)
        half2top = combine_all_positions(half2)

        players_in_first = len(half1top[1][1])
        players_in_second = len(half2top[1][1])
        players_in_combo = players_in_first + players_in_second
        print('Players in combining combo:', players_in_combo)

        return combine_multiple_positions(half1top, half2top, players_in_combo)

@time_and_slow_calls
def optimize(combo_positions_dict, df):

    tops={} #tops meaning, well, they're on top.
    for position, num_players in combo_positions_dict.items():
        print(f"Calculating initial positions for {position}")
        tops[position] = combine_single_position(position, num_players, df)

    tops_array = [vals for pos, vals in tops.items()]
    asdf = combine_all_positions(tops_array)
    winner = asdf[-1]
    winning_ids = winner[1]

    return winning_ids

if __name__ == '__main__':

    #combo_positions_dict shows what FD requires for a lineup
    combo_positions_dict = {'PG': 2, 'SG': 2, 'SF': 2, 'PF': 2, 'C': 1}

    opt_date = sys.argv[1] #always assuming there's a date passed from the command line
    data_filename = f"{opt_date}.csv"
    df = pd.read_csv(data_filename)

    winning_ids = optimize(combo_positions_dict, df)

    print(df.iloc[winning_ids])
    print(sum(df.iloc[winning_ids].pts))
    print(sum(df.iloc[winning_ids].sal))

