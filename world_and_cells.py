'''
This file contains Cells and World classes
'''



import random



class Cell ():
    def __init__ (self, x, y):
        self.x = x
        self.y = y

    def set_params (self, mass, speed, sensibility, angry):
        self.mass = mass
        self.speed = speed
        self.sensibility = sensibility
        self.angry = angry

    def init_random (self, seed=None):
        if seed:
            random.seed(seed)

        self.set_params(
            random.randint(1, 10),
            random.randint(1, 10),
            random.randint(1, 10),
            random.randint(1, 255),
        )

    def update (self, delta_time):
        if (direction := random.randint(0, 3)) == 0:
            move_x = +1
            move_y = 0
        elif direction == 1:
            move_x = 0
            move_y = +1
        elif direction == 2:
            move_x = -1
            move_y = 0
        elif direction == 3:
            move_x = 0
            move_y = -1
        else:
            raise Exception(f'direction not in 0..3, {direction = }')

        self.x += move_x * self.speed * delta_time
        self.y += move_y * self.speed * delta_time





class World ():
    def __init__ (self):
        self.cells = []

    def init_random (self, seed=None):
        for cell in self.cells:
            cell.init_random(seed)

    def add_cell (self, cell):
        self.cells.append(cell)
        #print(f'add_cell: {self.cells = }')
        #print(self.cells)

    def add_cells (self, cells):
        for cell in self.cells:
            self.add_cell(cell)

    def update (self, delta_time):
        #print(self.cells)
        for cell in self.cells:
            cell.update(delta_time)























