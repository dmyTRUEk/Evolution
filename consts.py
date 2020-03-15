'''
This file contains CONSTs, so you can change it and see
  difference in evolution ;)
'''



from random import randint




# WINDOW SETTINGS:
window_w, window_h = 1500, 800
window_name = 'Yeah, Evolution!'

zoom_speed = 1.1
camera_speed = 0.2



# WORLD SETTINGS:
world_size = 1000

world_area = world_size**2 * window_w // window_h 



# FOOD SETTINGS:
food_init_spawn_destiny = 0.001
food_spawn_per_step_destiny = 0.00005

max_food_amount = 20000

food_spawn_per_step = int( food_spawn_per_step_destiny * world_area )

bounds_spawn_food = world_size // 2
food_spawn_x = lambda: randint(-bounds_spawn_food*window_w//window_h, bounds_spawn_food*window_w//window_h)
food_spawn_y = lambda: randint(-bounds_spawn_food, bounds_spawn_food)

food_init_amount = int( food_init_spawn_destiny * world_area )

#energy_per_food = lambda: 300
energy_per_food = lambda: randint(300, 500)
energy_per_dead_cell = lambda: randint(10, 50)



# CELL SETTINGS:
cells_init_destiny = 0.001

#cells_init_amount = 100
cells_init_amount = int( cells_init_destiny * world_area / 4 )
max_cells_amount = 10000

cell_init_energy = lambda: 1000
energy_to_die = 0
energy_to_reproduct = 2000

bounds_spawn_cell = world_size // 4
cell_spawn_x = lambda: randint(-bounds_spawn_cell*window_w//window_h, bounds_spawn_cell*window_w//window_h)
cell_spawn_y = lambda: randint(-bounds_spawn_cell, bounds_spawn_cell)

cell_mass = lambda: randint(1, 5)
cell_speed = lambda: randint(1, 5) * randint(1, 5)
cell_angry = lambda: randint(0, 255)
cell_sensibility_dist = lambda: randint(1, 10) * randint(1, 10)
cell_eat_dist = lambda: randint(2, 5) * randint(2, 5)



# EVOLUTION SETTINGS:
evolution_speed = lambda: randint(1, 3)









