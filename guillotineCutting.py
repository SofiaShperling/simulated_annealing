import random
from collections import deque


def guillotine_cutting(pallet_width: int, pallet_height: int, x_tol: int, y_tol: int,
                       n_rect=10, min_side=3, side_choice='equal', seed=1):
    # each rectangle is cut randomly by width or height
    random.seed(seed)
    items_xywh = deque([(0, 0, pallet_width, pallet_height)])
    pass_cnt = 0
    while len(items_xywh) < n_rect:
        old_x, old_y, old_w, old_h = items_xywh.popleft()
        if old_w > min_side*2 or old_h > min_side*2:
            pass_cnt = 0
            w_prop = 0.5 if 'equal' == side_choice else old_w / (old_w + old_h)
            side = 'w' if random.random() < w_prop else 'h'
            if 'w' == side and old_w > min_side*2: #cut by width
                new_w1 = random.randint(min_side, old_w - min_side)
                items_xywh.append((old_x, old_y, new_w1, old_h))
                items_xywh.append((old_x + new_w1, old_y,
                                   old_w - new_w1, old_h))
            elif 'h' == side and old_h > min_side*2:
                new_h1 = random.randint(min_side, old_h - min_side)
                items_xywh.append((old_x, old_y, old_w, new_h1))
                items_xywh.append((old_x, old_y + new_h1,
                                   old_w, old_h - new_h1))
            else:
                items_xywh.append((old_x, old_y, old_w, old_h))
        else:
            items_xywh.append((old_x, old_y, old_w, old_h))
            pass_cnt += 1
        if pass_cnt >= len(items_xywh):
            break

    masses = [1/(item[2]*item[3]) for item in items_xywh]
    mass = 0
    xci = [x + w / 2 for x, y, w, h in items_xywh]
    yci = [y + h / 2 for x, y, w, h in items_xywh]

    xi = 0
    yi = 0
    for i in range(len(items_xywh)):
        xi += xci[i] * masses[i]
        yi += yci[i] * masses[i]
        mass += masses[i]

    cen_x = xi / mass
    cen_y = yi / mass

    while cen_x < pallet_width/2 - x_tol or cen_x > pallet_width/2 + x_tol \
            or cen_y < pallet_height/2 - y_tol or cen_y > pallet_height/2 + y_tol:
        while cen_x < pallet_width/2 - x_tol:
            for i in range(len(xci)):
                if xci[i] > pallet_width/2 + x_tol:
                    masses[i] += 0.1
                    mass = 0
                    xi = 0
                    yi = 0
                    for j in range(len(items_xywh)):
                        xi += xci[j] * masses[j]
                        yi += yci[j] * masses[j]
                        mass += masses[j]

                    cen_x = xi / mass
                    cen_y = yi / mass
                    if cen_x >= pallet_width/2 - x_tol:
                        break

        while cen_x > pallet_width/2 + x_tol:
            for i in range(len(xci)):
                if xci[i] < pallet_width/2 - x_tol:
                    masses[i] += 0.1
                    mass = 0
                    xi = 0
                    yi = 0
                    for j in range(len(items_xywh)):
                        xi += xci[j] * masses[j]
                        yi += yci[j] * masses[j]
                        mass += masses[j]

                    cen_x = xi / mass
                    cen_y = yi / mass
                    if cen_x <= pallet_width/2 + x_tol:
                        break

        while cen_y < pallet_height/2 - y_tol:
            for i in range(len(yci)):
                if yci[i] > pallet_height/2 + y_tol:
                    masses[i] += 0.1
                    mass = 0
                    xi = 0
                    yi = 0
                    for j in range(len(items_xywh)):
                        xi += xci[j] * masses[j]
                        yi += yci[j] * masses[j]
                        mass += masses[j]

                    cen_x = xi / mass
                    cen_y = yi / mass
                    if cen_y >= pallet_height/2 - y_tol:
                        break

        while cen_y > pallet_height/2 + y_tol:
            for i in range(len(yci)):
                if yci[i] < pallet_height/2 - y_tol:
                    masses[i] += 0.1
                    mass = 0
                    xi = 0
                    yi = 0
                    for j in range(len(items_xywh)):
                        xi += xci[j] * masses[j]
                        yi += yci[j] * masses[j]
                        mass += masses[j]

                    cen_x = xi / mass
                    cen_y = yi / mass
                    if cen_y <= pallet_height/2 + y_tol:
                        break

    masses = [mass * 100 for mass in masses]

    return list(items_xywh), list(masses)
