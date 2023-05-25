from collections import Iterable
import random
from typing import Optional

from numpy import sign

from Item import Item, Position


def get_permutation(items: Iterable[Item], positions: Iterable[Optional[Position]], permutation, centers_x: int, centers_y: int, x_tol: int, y_tol: int):
    x_mass = sum(
            (position[0] + (item.width if not position[2] else item.height) / 2) * item.mass for item, position in
            zip(items, positions) if position is not None) / sum(
            item.mass for item, position in zip(items, positions) if position is not None)

    y_mass = sum(
            (position[1] + (item.height if not position[2] else item.width) / 2) * item.mass for item, position in
            zip(items, positions) if position is not None) / sum(
            item.mass for item, position in zip(items, positions) if position is not None)
    sign_x = sign(50 - x_mass)
    sign_y = sign(50 - y_mass)
    # по хорошему надо переписать
    W = 100
    aa = []
    bb = []
    a = 1000
    b = 1000
    if x_mass < W/2 - x_tol or x_mass > W/2 + x_tol:

        for i in range(len(permutation)-1):
            if centers_x[i] is not None:
                center = centers_x[i][0]
                if sign_x == sign(50 - center):
                    aa.append(i)
                    # p = random.random()
                    # if 1 - p > p:
                    #     a = i
                elif sign_x != sign(50 - center):
                    bb.append(i)
                    # p = random.random()
                    # if 1 - p > p:
                    #     b = i

    elif y_mass < W/2 - y_tol or y_mass > W/2 + y_tol:
        for i in range(len(permutation)-1):
            if centers_y[i] is not None:
                center = centers_y[i][0]
                if sign_y == sign(50 - center):
                    aa.append(i)
                    # p = random.random()
                    # if 1 - p > p:
                    #     a = i
                elif sign_y != sign(50 - center):
                    bb.append(i)
    if a == 1000:
        a = random.randint(0, len(permutation)-1)
    if b == 1000:
        b = random.randint(0, len(permutation)-1)

    te = permutation[a]
    permutation[a] = permutation[b]
    permutation[b] = te
    return permutation
