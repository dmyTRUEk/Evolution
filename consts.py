'''
This file contains CONSTs, so you can change it and see
  difference in evolution ;)
'''



import random





window_w, window_h = 1600, 900

zoom_speed = 1.1
camera_speed = 0.2





cells_amount = 100
food_amount = 1000

bounds_spawn_cell = 100
bounds_spawn_food = 110

energy_to_die = 0
energy_to_reproduct = 2000

#energy_per_food = lambda: 300
energy_per_food = lambda: random.randint(100, 500)

cell_mass = lambda: random.randint(1, 5)
cell_speed = lambda: random.randint(1, 5)
cell_angry = lambda: random.randint(0, 255)
cell_sensibility_dist = lambda: random.randint(1, 30)
cell_eat_dist = lambda: random.randint(1, 7)












