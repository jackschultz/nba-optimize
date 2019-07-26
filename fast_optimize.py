import sys
import itertools
import cProfile, pstats, io

import numpy as np
import pandas as pd
import pdb
pry = pdb.set_trace #yeah, I have a ruby background too


def calc_cost_ranges(num_players):
    return np.array(list(range(3500*num_players, 60000+100, 100)))

def combine_single_position(position, num_players, df):
    posdf = df[df.pos == position]#.sort_values(by='sal')
    posdf_indicies = posdf.index.values
    points = posdf['pts'].values
    costs = posdf['sal'].values

    #splitting the data fram into the necessary fields
    ids_comb = np.array(list(itertools.combinations(posdf_indicies, num_players)))
    points_comb = np.array(list(itertools.combinations(points, num_players)))
    cost_comb = np.array(list(itertools.combinations(costs, num_players)))

    cost_ranges = calc_cost_ranges(num_players)
    #num_players, inds_comb, points_comb, cost_comb, cost_ranges


    return restrict_and_merge(ids_comb, points_comb, cost_comb, cost_ranges)

def combine_multiple_positions(pos1, pos2):

    #pos1 varaibles don't have a 1 at the end, pos 2 variables do at the beginning

    _, ids, points, costs = pos1
    _, ids2, points2, costs2 = pos2

    _, inds = np.unique(points, return_index=True)
    _, inds2 = np.unique(points2, return_index=True)

    #shrinking the data to remove repeats. Again, we're wanting to keep them all the same length
    #so the same ids reference the correct data
    shrunk_costs = costs[inds]
    shrunk_costs2 = costs2[inds2]
    shrunk_points = points[inds]
    shrunk_points2 = points2[inds2]
    shrunk_ids = ids[inds]
    shrunk_ids2 = ids2[inds2]

    #combine the status using the product
    costs_comb = np.array(list(itertools.product(shrunk_costs, shrunk_costs2)))
    points_comb = np.array(list(itertools.product(shrunk_points, shrunk_points2)))
    ids_comb = np.array([ np.concatenate((x,y)) for x,y in  list(itertools.product(shrunk_ids, shrunk_ids2))   ] )

    num_players = ids.shape[1] + ids2.shape[1]
    cost_ranges = calc_cost_ranges(num_players)

    return restrict_and_merge(ids_comb, points_comb, costs_comb, cost_ranges)


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

        return combine_multiple_positions(half1top, half2top)


def restrict_and_merge(ids_comb, points_comb, cost_comb, cost_ranges):

    player_combination_size, num_ids_size = ids_comb.shape
    cost_ranges_size = cost_ranges.size #used to know how big to make the arrays

    cost_ranges_full = np.broadcast_to(cost_ranges,(player_combination_size, cost_ranges_size)).T

    #creating an array where we add the costs together to get a 1d array
    cost_sum = cost_comb.sum(axis=1)
    points_sum = points_comb.sum(axis=1)

    cost_sum_full = np.broadcast_to(cost_sum,(cost_ranges_size, player_combination_size))
    #adding the points of the combinations and making them zero if the salary sum is
    #higher than the max_salary
    points_sum_full = np.broadcast_to(points_sum,(cost_ranges_size, player_combination_size))

    #used to snag the best players who've been selected
    ids_comb_full = np.broadcast_to(ids_comb, (cost_ranges_size, player_combination_size, num_ids_size))

    under_cost_limit = cost_sum_full <= cost_ranges_full

    calculated_points = points_sum_full * under_cost_limit

    #we're finding the max indicies
    #argmax() returns the index of the max value
    top_inds = calculated_points.argmax(axis=1)

    #now that we know the index of the maximum, we return the relevant info
    row_selectors = np.arange(cost_ranges_size)
    max_points = points_sum_full[row_selectors, top_inds]
    max_costs = cost_sum_full[row_selectors, top_inds]
    max_inds = ids_comb_full[row_selectors, top_inds]
    return cost_ranges, max_inds, max_points, max_costs


def optimize(combo_positions_dict, df):

    tops={}
    for position, num_players in combo_positions_dict.items():
        print(f"Calculating initial positions for {position}")
        tops[position] = combine_single_position(position, num_players, df)

    tops_array = [vals for pos, vals in tops.items()]
    fin = combine_all_positions(tops_array)
    winner = fin[1]
    winning_ids = winner[-1]

    print(df.iloc[winning_ids])
    print("\n")
    print("Combined player points:", sum(df.iloc[winning_ids].pts))
    print("Combined player salary:", sum(df.iloc[winning_ids].sal))
    print("\n")


if __name__ == '__main__':

    #in the future, if there are different rules or you have a keeper player
    #who is alreay set in a position, we can change this and still get a valid
    #lineup
    combo_positions_dict = {'PG': 2, 'SG': 2, 'SF': 2, 'PF': 2, 'C': 1}

    opt_date = sys.argv[1] #always assuming there's a date passed from the command line
    data_filename = f"{opt_date}.csv"
    df = pd.read_csv(data_filename)

    pr = cProfile.Profile()
    pr.enable()
    s = io.StringIO()

    fin = optimize(combo_positions_dict, df)

    pr.disable()
    s = io.StringIO()
    sortby = 'tottime'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(10)
    print(s.getvalue())




