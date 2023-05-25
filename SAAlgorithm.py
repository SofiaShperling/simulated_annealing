from typing import List
from Item import Item
from skylinePacking import skyline_func
from getPermutation import get_permutation

import numpy as np
import math


def sa_algorithm(items: List[Item], pallet_width: int, pallet_height: int, x_tol: int, y_tol: int ):

    dif = 0
    # best_dist = 10000
    permutations = [i for i in range(len(items))]
    for i in range(10):
        newWay1 = list(np.random.permutation(permutations))
        newWay2 = list(np.random.permutation(permutations))
        dist1, res, results1, go1, centers_x1, centers_y1 = skyline_func(pallet_width, pallet_height, 10, items, x_tol,
                                                                         y_tol, newWay1)
        dist2, res, results2, go2, centers_x2, centers_y2 = skyline_func(pallet_width, pallet_height, 10, items, x_tol,
                                                                         y_tol, newWay2)
        difNew = abs(dist1 - dist2)
        if difNew >= dif:
            dif = difNew

    pr = 0.97
    T0 = dif * pr
    T = T0
    k = len(items)
    permutations = list(np.random.permutation(permutations))
    dist = -1
    # res = 0
    while dist < 0:
        dist, res, results, go, centers_x, centers_y = skyline_func(pallet_width, pallet_height, 10, items,
                                                                    x_tol, y_tol, permutations)
        if dist < 0:
            a = 0
            b = 0
            while a == b:
                a = np.random.randint(0, k)
                b = np.random.randint(0, k)
            te = permutations[a]
            permutations[a] = permutations[b]
            permutations[b] = te

    minPermutation = permutations
    minDist = dist
    minResults: [] = [None for i in range(len(items))]
    iteration = 0
    outs_func = []
    outs_clean = []
    penalty = 10
    go_counter = 0
    time_count = 0
    old_dist = dist
    counter_t = 0
    while counter_t < 20:
        permutations = minPermutation
        for i in range(100):
            newPermutation = permutations
            newDist, res, newResults, newGo, centers_x, centers_y = skyline_func(pallet_width, pallet_height,penalty,
                                                                                 items, x_tol, y_tol, newPermutation)
            if newDist == 0 and time_count == 0:
                time_count = 1
            if newDist < 0:
                newDist = dist
                newResults = results
            if newGo == 1:
                go_counter += 1
                newPermutation = get_permutation(items, newResults, newPermutation, centers_x, centers_y, x_tol, y_tol)
            else:
                go_counter = 0
                a = 0
                b = 0
                while a == b:
                    a = np.random.randint(0, k)
                    b = np.random.randint(0, k)
                    te = 0
                te = newPermutation[a]
                newPermutation[a] = newPermutation[b]
                newPermutation[b] = te
            penalty = go_counter * 10
            if minDist > newDist and newGo == 0:
                minDist = newDist
                minResults = newResults
                minPermutation = newPermutation
            if newDist < dist:
                if res > 0:
                    dist = newDist
                    results = newResults
                    res_clean = res
            else:
                p = math.exp((dist - newDist) / T)
                if p > 1 - p and res > 0:
                    dist = newDist
                    results = newResults
                    if res > 0:
                        res_clean = res
            outs_func.append(dist)
            outs_clean.append(res_clean)
            iteration += 1

        if minDist == old_dist:
            counter_t += 1
            old_dist = minDist
        else:
            counter_t = 0
            old_dist = minDist
        T = T * pr

    if minDist <= dist:
        results = minResults

    return results, outs_func, outs_clean
