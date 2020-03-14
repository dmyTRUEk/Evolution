'''
This file contains Cells and World classes
'''



import random
import colorsys

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
        self.mass = mass
        self.speed = speed
        self.sensibility_dist = sensibility_dist
        self.eat_dist = eat_dist
        self.angry = angry

        self.color = colorsys.hls_to_rgb(self.angry/255, 0.5, 1.0)



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



    def search_for_food (self, food):
        dist_min = float('inf')
        for f in food:
            dist = (self.x-f.x)**2 + (self.y-f.y)**2
            if dist < dist_min:
                dist_min = dist
                closest_food = f

        if dist_min < self.eat_dist**2:
            self.energy += closest_food.energy
            closest_food.eated = True

        if dist_min < self.sensibility_dist**2:
            self.move_x = +1 if self.x > closest_food.x else -1
            self.move_y = +1 if self.y > closest_food.y else -1

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

        self.energy -= self.mass*(dx**2 + dy**2) + self.sensibility_dist





class Food ():
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.energy = energy_per_food()
        self.eated = False





class World ():
    def __init__ (self, food_amount=100):
        self.cells = []
        self.food = []

        for i in range(food_amount):
            self.add_food(Food(
                random.randint(-bounds_spawn_food, bounds_spawn_food),
                random.randint(-bounds_spawn_food, bounds_spawn_food),
            ))



    #def init_random (self, seed=None):
    #    for cell in self.cells:
    #        cell.init_random(seed)



    def add_cell (self, cell):
        self.cells.append(cell)
        #print(f'add_cell: {self.cells = }')
        #print(self.cells)



    def add_cells (self, cells):
        for cell in self.cells:
            self.add_cell(cell)



    def add_food (self, food):
        self.food.append(food)



    def update (self, delta_time):
        #print(self.cells)
        for cell in self.cells:
            cell.update(delta_time)

            if cell.energy < energy_to_die:
                self.cells.remove(cell)

            elif cell.energy > energy_to_reproduct:
                cell.energy //= 2
                self.add_cell(Cell( cell.x, cell.y, cell.energy//2))

            else:
                cell.search_for_food(self.food)

        for food in self.food:
            if food.eated:
                self.food.remove(food)









