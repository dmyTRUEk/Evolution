'''
This file contains Cells and World classes
'''



import random
import colorsys
#import numpy as np

import time
import sys

from utils import *
import consts
from consts import *





class Cell ():
    def __init__ (self, x, y, energy, seed=None):
        self.x = x
        self.y = y
        self.energy = energy

        self.move_x = 0
        self.move_y = 0

        self.init_random(seed)



    def print (self):
        print(f'self = ')
        print(f'self.x = ')
        print(f'self.y = ')
        print(f'self.energy = ')
        print(f'self.move_x = ')
        print(f'self.move_y = ')
        print(f'self.mass = ')
        print(f'self.speed = ')
        print(f'self.angry = ')
        print(f'self.sensibility_dist = ')
        print(f'self.eat_dist = ')
        print(f'')



    def set_params (self, mass, speed, angry, sensibility_dist, eat_dist):
        self.mass = mass if mass >= 1 else 1
        self.speed = speed
        self.sensibility_dist = sensibility_dist
        self.eat_dist = eat_dist
        self.angry = angry

        self.color = colorsys.hls_to_rgb(self.angry/255, 0.5, 1.0)

        self.sensibility_dist2 = self.sensibility_dist**2
        self.eat_dist2 = self.eat_dist**2



    def init_random (self, seed=None):
        if seed:
            random.seed(seed)

        self.set_params(
            cell_mass(),
            cell_speed(),
            cell_angry(),
            cell_sensibility_dist(),
            cell_eat_dist(),
        )



    def evolve (self, evolve_speed):
        self.set_params(
            self.mass + rand_m1_p1()*evolve_speed,
            self.speed + rand_m1_p1()*evolve_speed,
            self.angry + rand_m1_p1()*evolve_speed,
            self.sensibility_dist + rand_m1_p1()*evolve_speed,
            self.eat_dist + rand_m1_p1()*evolve_speed,
        )



    def search_for_food (self, food):
        dist_min = float('inf')

        for f in food:
            if abs(dx := self.x-f.x) < self.sensibility_dist and abs(dy := self.y-f.y) < self.sensibility_dist:
                if (dist := (dx)**2 + (dy)**2) < dist_min:
                    dist_min = dist
                    closest_food = f

        if dist_min <= self.eat_dist2:
            if not closest_food.eated:
                self.energy += closest_food.energy
                closest_food.eated = True

        elif dist_min <= self.sensibility_dist2:
            self.move_x = -1 if self.x > closest_food.x else +1
            self.move_y = -1 if self.y > closest_food.y else +1

        else:
            if random.randint(0, 1) == 0: 
                self.move_x = random.choice((-1, 0, +1))
                self.move_y = 0
            else:
                self.move_x = 0
                self.move_y = random.choice((-1, 0, +1))



    def update (self, delta_time):
        if delta_time == 0:
            return

        dx = self.move_x * self.speed * delta_time
        dy = self.move_y * self.speed * delta_time

        self.x += int(dx)
        self.y += int(dy)

        self.energy -= self.mass*(dx**2 + dy**2) + self.sensibility_dist//7 + 3*self.eat_dist





class Food ():
    def __init__ (self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy
        self.eated = False





class World ():
    def __init__ (self):
        self.cells = []
        self.food = []

        self.init_random()



    def init_random (self, seed=None):
        for i in range(food_init_amount):
            self.add_food_at_random_point()

        for i in range(cells_init_amount):
            self.add_cell_at_random_point()



    def add_cell (self, cell):
        self.add_cell_at_begin(cell)

    def add_cell_at_begin (self, cell):
        self.cells.insert(0, cell)

    def add_cell_at_end (self, cell):
        self.cells.append(cell)

    def add_cells (self, cells):
        for cell in self.cells:
            self.add_cell(cell)

    def add_cell_at_random_point (self):
        self.add_cell(Cell(cell_spawn_x(), cell_spawn_y(), cell_init_energy()))



    def add_food (self, food):
        self.food.append(food)

    def add_food_at_random_point (self):
        self.add_food(Food(food_spawn_x(), food_spawn_y(), energy_per_food()))



    def update (self, delta_time):
        #print(self.cells)

        for cell in self.cells:
            cell.update(delta_time)

            if cell.energy < energy_to_die:   # DIE:
                self.add_food(Food(cell.x, cell.y, energy_per_dead_cell()))
                self.cells.remove(cell)

            elif cell.energy > energy_to_reproduct:   # REPRODUCT
                cell.energy //= 2

                new_cell = Cell(cell.x, cell.y, cell.energy//2)
                new_cell.evolve(evolution_speed())

                self.add_cell(new_cell)

            else:   # ALIVE:
                cell.search_for_food(self.food)

        # delete eated food
        for food in self.food:
            if food.eated:
                self.food.remove(food)

        # add some food at random point
        for i in range(consts.food_spawn_per_step):
            self.add_food_at_random_point()



    def statistics (self):
        ans = ''

        cells_amount = len(self.cells)
        food_amount = len(self.food)

        sum_speed = 0
        for cell in self.cells:
            sum_speed += cell.speed

        avg_speed = sum_speed / cells_amount if cells_amount > 0 else float('nan')
        ans += f'avarage speed = {avg_speed}'

        return ans









'''
Old code pieces:


# BY NUMPY:

#def search_for_food (self, food, np_array_food_xy):
    ...

# in world.update -> # ALIVE:
list_food = []
for f in self.food:
    list_food.append((f.x, f.y))
np_array_food_xy = np.array(list_food)
cell.search_for_food(self.food, np_array_food_xy)

# in search_for_food:
np_array_dist_xy = np.abs( np_array_food_xy - np.asarray((self.x, self.y)) )
i_min = None
for i in range(np_array_food_xy.shape[0]):
    if (dx := np_array_dist_xy[i][0] < self.sensibility_dist) and (dy := np_array_dist_xy[i][1] < self.sensibility_dist):
        if (dist := dx**2 + dy**2) < dist_min:
            dist_min = dist
            i_min = i
if i_min != None:
    closest_food = food[i_min]










'''




