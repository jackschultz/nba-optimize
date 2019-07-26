import csv
import sys
import itertools
import numpy as np

from utils import time_and_slow_calls

import pdb
pry = pdb.set_trace

def index_generator(ind_lists):
    return itertools.product(*ind_lists)

def calculate_position_combinations(player_combinations, test_salary, num_players):
    '''
    Loop through the combinations of the single position, and if it's under
    the test_salary and has more points than the current best combination set
    those values. Returns an array of the best.
    '''
    #loop through the list of players that are of that posision
    max_found_points = 0
    best_combined_salary = 0
    top_players = [-1] * num_players
    player_index_lists = [list(range(0, len(player_combinations)))] * num_players
    for indicies in index_generator(player_index_lists):

        if len(set(indicies)) != len(indicies):
            continue

        if indicies[0] > indicies[-1]:
            continue

        test_players = [player_combinations[index] for index in indicies] #grab the two testers

        combined_salary = sum([p['sal'] for p in test_players])
        if combined_salary > test_salary:
            continue

        points = sum([p['pts'] for p in test_players])
        if points > max_found_points:
            top_players = [p['pid'] for p in test_players]
            max_found_points = points
            best_combined_salary = sum([p['sal'] for p in test_players])

    return [test_salary, best_combined_salary, max_found_points, top_players]

def combine_single_position(players, num_players):
    '''
    Goal is to have it where the for each salary in the range, have a list of the num_players
    player ids who have the best combined points where their combined salary is below the salary
    total.
    #array of sets where (max_salary, combined salary, [list of pids], total_points)
    '''
    cost_ranges = range(3500*num_players, 60000 + 100, 100)

    return [calculate_position_combinations(players, cost, num_players) for cost in cost_ranges]

def calculate_max_points(pos1, pos2, test_salary):
    '''
    Double loop so we test each combination of the two sets of positions.
    We store the information for each new max point combinations, as long as
    they're under the test_salary limit, and return those fields.
    '''
    max_found_points = 0
    for g1 in pos1: #g1 stands for group 1
        for g2 in pos2:
            #break if combined salary is above the test_salary
            if g1[1] + g2[1] > test_salary:
                #thankfully we can break if we've hit the point where the combined salary is bigger
                #because the positions are sorted by salary
                break
            points = g1[2] + g2[2]
            #if the two point totals added together > current max point total
            if points > max_found_points:
                top_players = g1[3] + g2[3]
                max_found_points = points
                combined_sal = g1[1] + g2[1]
    return [test_salary, combined_sal, max_found_points, top_players]

def combine_multiple_positions(pos1, pos2):

    num_players = len(pos1[0][3]) + len(pos2[0][3]) #counting the number of pids in those arrays
    max_salary = min(60000 + 100, 13000 * num_players) #if we're only testing 3 players, the max salary they can have combined is 13000 * 3
    cost_ranges = range(3500*num_players, max_salary, 100)

    return [calculate_max_points(pos1, pos2, salary) for salary in cost_ranges]

@time_and_slow_calls
def optimize(pgs, sgs, sfs, pfs, cs):
    print("Calculating initial PGs")
    pgt = combine_single_position(pgs, 2)
    print("Calculating initial SGs")
    sgt = combine_single_position(sgs, 2)
    print("Calculating initial SFs")
    sft = combine_single_position(sfs, 2)
    print("Calculating initial PFs")
    pft = combine_single_position(pfs, 2)
    print("Calculating initial Cs")
    ct = combine_single_position(cs, 1)

    print("Combining PGs and SGs")
    pgsg = combine_multiple_positions(pgt, sgt)

    print("Combining PFs and SFs")
    sfpf = combine_multiple_positions(sft, pft)

    print("Combining PFs, SFs, and Cs")
    sfpfc = combine_multiple_positions(sfpf, ct)

    print("Combining all positions")
    fin = combine_multiple_positions(pgsg, sfpfc)

    print(fin)
    return fin

if __name__ == '__main__':

    opt_date = sys.argv[1] #always assuming there's a date passed from the command line
    data_filename = f"{opt_date}.csv"

    pgs = []
    sgs = []
    sfs = []
    pfs = []
    cs = []
    with open(data_filename) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = list(csv_reader)
        for row in reversed(rows):
            row['pid'] = int(row['pid'])
            row['sal'] = int(row['sal'])
            row['pts'] = float(row['pts'])
            if row['pos'] == 'PG':
                pgs.append(row)
            elif row['pos'] == 'SG':
                sgs.append(row)
            elif row['pos'] == 'SF':
                sfs.append(row)
            elif row['pos'] == 'PF':
                pfs.append(row)
            elif row['pos'] == 'C':
                cs.append(row)



    fin = optimize(pgs, sgs, sfs, pfs, cs)

    print(fin[-1])
    pids = fin[-1][3]

    dbid = {}
    with open(data_filename) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            dbid[int(row[0])] = row

    for pid in pids:
        pinfo = dbid[pid]
        print(pinfo)

