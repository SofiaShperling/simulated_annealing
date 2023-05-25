from guillotineCutting import guillotine_cutting
from Item import Item, Position
from SAAlgorithm import sa_algorithm
from packingVisualisation import draw_packing_mass
import random


if __name__ == '__main__':
    N = 50
    pallet_width = 100
    pallet_height = 100
    x_tol = 25
    y_tol = 25
    permutation = None

    data, masses = guillotine_cutting(pallet_width, pallet_height, x_tol, y_tol)

    items = [0 for _ in range(N)]

    for i in range(N):
        r = 1 - random.randint(0, 3) / 100
        if i < len(masses):
            items[i] = Item(data[i][2] * r, data[i][3] * r, masses[i])
        else:
            items[i] = Item(random.randint(5, 30), random.randint(5, 30), random.randint(1, 100))

    random.shuffle(items)

    results, outs_func, outs_clean = sa_algorithm(items, pallet_width, pallet_height, x_tol, y_tol)

    k = 0
    for i in range(len(results)):
        if results[i] is not None:
            k += 1
            results[i] = Position(results[i][0], results[i][1], results[i][2])

    draw_packing_mass(items, results, pallet_width, pallet_height, x_tol, y_tol)






