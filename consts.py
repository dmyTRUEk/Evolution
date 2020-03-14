'''
This file contains CONSTs, so you can change it and see
  difference in evolution ;)
'''



from random import randint




# WINDOW SETTINGS:
window_w, window_h = 1600, 900

zoom_speed = 1.1
camera_speed = 0.2



# FOOD SETTINGS:
food_init_amount = 1000
max_food_amount = 20000

bounds_spawn_food = 300
food_x = lambda: randint(-bounds_spawn_food, bounds_spawn_food)
food_y = lambda: randint(-bounds_spawn_food, bounds_spawn_food)

food_spawn_per_step = 5

#energy_per_food = lambda: 300
energy_per_food = lambda: randint(100, 500)
energy_per_dead_cell = lambda: randint(10, 50)



# CELL SETTINGS:
cells_init_amount = 100
max_cells_amount = 10000

bounds_spawn_cell = 200
cell_x = lambda: randint(-bounds_spawn_cell, bounds_spawn_cell)
cell_y = lambda: randint(-bounds_spawn_cell, bounds_spawn_cell)

cell_init_energy = lambda: 1000
energy_to_die = 0
energy_to_reproduct = 2000

cell_mass = lambda: randint(1, 5)
cell_speed = lambda: randint(1, 5) * randint(1, 5)
cell_angry = lambda: randint(0, 255)
cell_sensibility_dist = lambda: randint(1, 10) * randint(1, 10)
cell_eat_dist = lambda: randint(2, 5) * randint(2, 5)



# EVOLUTION SETTINGS:
evolution_speed = lambda: randint(1, 3)









