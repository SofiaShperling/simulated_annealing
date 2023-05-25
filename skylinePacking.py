#%%
import math
from typing import List, Optional, Iterable

from Item import Item
from structures import LinkedList


def skyline_func(pallet_width: int, pallet_height: int, fine: int, items: List[Item], x_tol: int, y_tol: int,
                 permutation: Optional[Iterable[int]] = None):
    # x_tol = 5
    # y_tol = 5

    if permutation is None:
        permutation = range(len(items))
    skyline = LinkedList()
    skyline.add((0, 0))

    items_list = LinkedList()
    for item in permutation:
        items_list.add((items[item].width, items[item].height, items[item].mass, item))

    results: [] = [None for _ in range(len(items))]
    centers_x = [None for _ in range((len(items)))]
    centers_y = [None for _ in range((len(items)))]
    sum_x = 0
    sum_y = 0
    sum_mass = 0
    counter = 0
    while not items_list.is_empty():
        gap = None
        level = pallet_height + 1
        for current in skyline:
            if current.data[1] < level:
                level = current.data[1]
                gap = current

        if level == pallet_height:
            break
        if gap == None:
            break
        width = (gap.next.data[0] - gap.data[0]) if gap.next is not None else pallet_width - gap.data[0]
        height1 = (gap.prev.data[1] - gap.data[1]) if gap.prev is not None else pallet_height - gap.data[1]
        height2 = (gap.next.data[1] - gap.data[1]) if gap.next is not None else pallet_height - gap.data[1]

        best_item = None
        score = -1
        rotated = False
        for current_item in items_list:
            if gap is not None:
                if current_item.data[1] <= pallet_height - gap.data[1] and current_item.data[0] <= width:
                    cur_score = int(current_item.data[1] == height1) + int(current_item.data[1] == height2) + int(
                            current_item.data[0] == width)
                    if cur_score > score:
                        core = cur_score
                        best_item = current_item
                        rotated = False
                if current_item.data[0] <= pallet_height - gap.data[1] and current_item.data[1] <= width:
                    cur_score = int(current_item.data[0] == height1) + int(current_item.data[0] == height2) + int(
                            current_item.data[1] == width)
                    if cur_score > score:
                        score = cur_score
                        best_item = current_item
                        rotated = True
        best_item_width = (best_item.data[0] if not rotated else best_item.data[1]) if best_item is not None else None
        best_item_height = (best_item.data[1] if not rotated else best_item.data[0]) if best_item is not None else None
        best_item_mass = (best_item.data[2]) if best_item is not None else None
        if score == -1:
            if height1 <= height2:
                if gap is not skyline.first:
                    prev = skyline.remove(gap)
                    if prev is not None and prev.next is not None and prev.data[1] == prev.next.data[1]:
                        skyline.remove(prev.next)
                else:
                    gap.data = 0, gap.data[1] + height2
                    skyline.remove(gap.next)
            else:
                if gap is not skyline.first:
                    prev = skyline.remove(gap)
                    next_point = prev.next
                    assert next_point is gap.next
                    next_point.data = gap.data[0], next_point.data[1]
                else:
                    gap.data = 0, gap.data[1] + height2
                    skyline.remove(gap.next)
        # if score == -1:
        #     if height1 <= height2:
        #         if gap is not skyline.first:
        #             prev = skyline.remove(gap)
        #             if prev is not None and prev.next is not None and prev.data[1] == prev.next.data[1]:
        #                 skyline.remove(prev.next)
        #         elif gap is not None:
        #             gap.data = 0, gap.data[1] + height2
        #             skyline.remove(gap.next)
        #     else:
        #         if gap is not skyline.first:
        #             prev = skyline.remove(gap)
        #             next_point = prev.next
        #             assert next_point is gap.next
        #             next_point.data = gap.data[0], next_point.data[1]
        #         elif gap is not None:
        #             gap.data = 0, gap.data[1] + height2
        #             skyline.remove(gap.next)


        elif score == 0:
            results[best_item.data[3]] = [gap.data[0], gap.data[1], rotated]
            centers_x[best_item.data[3]] = [gap.data[0] + best_item_width/2, counter]
            centers_y[best_item.data[3]] = [gap.data[1] + best_item_height/2, counter]
            sum_x += ((gap.data[0] + best_item_width/2) * best_item_mass)
            sum_y += ((gap.data[1] + best_item_height/2) * best_item_mass)
            sum_mass += best_item_mass

            skyline.insert(gap, (gap.data[0] + best_item_width, gap.data[1]))
            gap.data = gap.data[0], gap.data[1] + best_item_height

            items_list.remove(best_item)
        elif score == 1:
            if best_item_height == height1:
                results[best_item.data[3]] = [gap.data[0], gap.data[1], rotated]
                centers_x[best_item.data[3]] = [gap.data[0] + best_item_width/2, counter]
                centers_y[best_item.data[3]] = [gap.data[1] + best_item_height/2, counter]

                sum_x += ((gap.data[0] + best_item_width / 2) * best_item_mass)
                sum_y += ((gap.data[1] + best_item_height / 2) * best_item_mass)
                sum_mass += best_item_mass

                gap.data = gap.data[0] + best_item_width, gap.data[1]
            elif best_item_height == height2:
                next_point = gap.next
                if next_point is not None:
                    results[best_item.data[3]] = [next_point.data[0] - best_item_width, gap.data[1], rotated]
                    centers_x[best_item.data[3]] = [gap.data[0] + best_item_width/2, counter]
                    centers_y[best_item.data[3]] = [gap.data[1] + best_item_height/2, counter]

                    sum_x += ((gap.data[0] + best_item_width / 2) * best_item_mass)
                    sum_y += ((gap.data[1] + best_item_height / 2) * best_item_mass)
                    sum_mass += best_item_mass

                    next_point.data = next_point.data[0] - best_item_width, next_point.data[1]
                else:
                    results[best_item.data[3]] = [pallet_width - best_item_width, gap.data[1], rotated]
                    centers_x[best_item.data[3]] = [gap.data[0] + best_item_width/2, counter]
                    centers_y[best_item.data[3]] = [gap.data[1] + best_item_height/2, counter]

                    sum_x += ((gap.data[0] + best_item_width / 2) * best_item_mass)
                    sum_y += ((gap.data[1] + best_item_height / 2) * best_item_mass)
                    sum_mass += best_item_mass
                    skyline.add((pallet_width - best_item_width, gap.data[1] + best_item_height))
            else:
                results[best_item.data[3]] = [gap.data[0], gap.data[1], rotated]
                centers_x[best_item.data[3]] = [gap.data[0] + best_item_width/2, counter]
                centers_y[best_item.data[3]] = [gap.data[1] + best_item_height/2, counter]

                sum_x += ((gap.data[0] + best_item_width / 2) * best_item_mass)
                sum_y += ((gap.data[1] + best_item_height / 2) * best_item_mass)
                sum_mass += best_item_mass
                gap.data = gap.data[0], gap.data[1] + best_item_height

            items_list.remove(best_item)
        elif score == 2:
            results[best_item.data[3]] = [gap.data[0], gap.data[1], rotated]
            centers_x[best_item.data[3]] = [gap.data[0] + best_item_width/2, counter]
            centers_y[best_item.data[3]] = [gap.data[1] + best_item_height/2, counter]

            sum_x += ((gap.data[0] + best_item_width / 2) * best_item_mass)
            sum_y += ((gap.data[1] + best_item_height / 2) * best_item_mass)
            sum_mass += best_item_mass
            if best_item_height != height1:
                skyline.remove(gap.next)
                gap.data = gap.data[0], gap.data[1] + best_item_height
            elif best_item_height != height2:
                skyline.remove(gap)
            else:
                gap.data = gap.data[0] + best_item_width, gap.data[1]

            items_list.remove(best_item)
        elif score == 3:
            next_point = gap.next
            skyline.remove(gap)
            skyline.remove(next_point)

            items_list.remove(best_item)
            results[best_item.data[3]] = [gap.data[0], gap.data[1], rotated]
            centers_x[best_item.data[3]] = [gap.data[0] + best_item_width/2, counter]
            centers_y[best_item.data[3]] = [gap.data[1] + best_item_height/2, counter]

            sum_x += ((gap.data[0] + best_item_width / 2) * best_item_mass)
            sum_y += ((gap.data[1] + best_item_height / 2) * best_item_mass)
            sum_mass += best_item_mass
        counter += 1

    sum_x = sum_x/sum_mass
    sum_y = sum_y/sum_mass

    difference = 0
    difference_x = 0
    difference_y = 0
    if sum_x < (pallet_width - 2 * x_tol)/2:
        difference_x = abs(pallet_width/2 -x_tol - math.floor(sum_x))
    elif sum_x > (pallet_width - 2 * x_tol)/2 + 2*x_tol:
        difference_x =abs(math.ceil(sum_x) - pallet_width/2 + x_tol)
    if sum_y < (pallet_height - 2 * y_tol)/2:
        difference_y = abs(pallet_height/2 -y_tol - math.floor(sum_y))
    elif sum_y > (pallet_height - 2 * y_tol)/2 + 2*y_tol:
        difference_y = abs(math.ceil(sum_y) - pallet_height/2 + y_tol)

    difference = difference_x + difference_y
    packed = 0
    for i in range(len(items)):
        if results[i] is not None:
            packed += items[i].width * items[i].height

    res = pallet_height * pallet_width - packed

    out = res + fine * difference
    go = 0
    if difference > 0:
        go = 1
    return out, res, results, go, centers_x, centers_y