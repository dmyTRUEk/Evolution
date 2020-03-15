'''
This is main file of evolution
'''



import glfw

from OpenGL.GL import *
#import OpenGL.GL as gl
#import OpenGL.GLU as glu
#import OpenGL.GLUT as glut

import time

from utils import *
import consts
from consts import *
from world_and_cells import *





world = World()

delta_time = 1

zoom = 1 / 100
camera_x, camera_y = 0, 0

step = 0

working = True

list_cells_amount = []
list_food_amount = []
list_cells_speed = []

dict_cells_amount_avg = {}
dict_food_amount_avg = {}
dict_cells_speed_avg = {}



def main ():
    global world
    world = World()

    global time_start
    time_start = time.time()

    start_glfw_window()



def update ():
    global step
    global list_cells_amount, list_food_amount, list_cells_speed
    global dict_cells_amount_avg, dict_food_amount_avg, dict_cells_speed_avg

    if delta_time != 0:
        world.update(delta_time)
        step += 1

    cells_amount = len(world.cells)
    food_amount = len(world.food)

    print('STATE:')
    print('Cell energies = {')
    for cell in world.cells:
        print(cell.energy, end=' ')
    print('\n}')
    print(f'step = {step}')
    print(f'cells amount = {cells_amount}')
    print(f'food  amount = {food_amount}')
    print()
    #print(f'main -> food spawn per step = {food_spawn_per_step}')
    print(f'food spawn per step = {consts.food_spawn_per_step}')

    print('\nSTATISTICS:')
    sum_speed = 0
    for cell in world.cells:
        sum_speed += cell.speed
    cells_speed_avg = sum_speed / cells_amount if cells_amount > 0 else float('nan')
    print(f'cells_speed_avg = {round(cells_speed_avg, 3)}')
    print()
    print(f'{dict_cells_amount_avg = }')
    print(f'{dict_food_amount_avg = }')
    print(f'{dict_cells_speed_avg = }')

    print('\n\n')

    if cells_amount <= 0:
        print('No Cells survived\n\n')
        init_exit()

    if cells_amount > max_cells_amount:
        print('Too many Cells\n\n')
        init_exit()

    if food_amount > max_food_amount:
        print('Too many Food\n\n')
        init_exit()

    list_cells_amount.append(cells_amount)
    list_food_amount.append(food_amount)
    list_cells_speed.append(cells_speed_avg)
    
    if step % (steps_per_food_decrease := 100) == 0:
        cells_amount_avg = avg(list_cells_amount)
        food_amount_avg = avg(list_food_amount)
        cells_speed_avg = avg(list_cells_speed)

        dict_cells_amount_avg[consts.food_spawn_per_step] = round(cells_amount_avg, 3)
        dict_food_amount_avg[consts.food_spawn_per_step] = round(food_amount_avg, 3)
        dict_cells_speed_avg[consts.food_spawn_per_step] = round(cells_speed_avg, 3)

        list_cells_amount = []
        list_food_amount = []
        list_cells_speed = []

        consts.food_spawn_per_step = int(consts.food_spawn_per_step / 1.01)
        #if consts.food_spawn_per_step > 30:
        #    consts.food_spawn_per_step -= 3
        #if consts.food_spawn_per_step > 20:
        #    consts.food_spawn_per_step -= 2
        #elif consts.food_spawn_per_step > 1:
        #    consts.food_spawn_per_step -= 1
        #elif consts.food_spawn_per_step == 1:
        #    consts.food_spawn_per_step -= 1
        #elif consts.food_spawn_per_step < 1:
        #    pass
        #    #init_exit()

    #if step >= 1000:
    #    init_exit()

    render_frame()



def before_exit ():
    time_end = time.time()
    global time_start
    print(f'Time elapsed = {time_end-time_start}')
    print()
    for key in dict_cells_amount_avg:
        print(' ', key, dict_cells_amount_avg[key], dict_food_amount_avg[key], dict_cells_speed_avg[key])
    print('\n\n')
    print('Exiting...')



def init_exit ():
    global working
    working = False



def draw_square (x, y, color):
    x1 = (x) * zoom - camera_x
    y1 = (y) * zoom - camera_y
    x2 = (x+1) * zoom - camera_x
    y2 = (y+1) * zoom - camera_y

    glBegin(GL_QUADS)
    glColor3f(color[0], color[1], color[2])
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()



def render_frame ():
    for cell in world.cells:
        draw_square(cell.x, cell.y, cell.color)

    for food in world.food:
        draw_square(food.x, food.y, (1.0, 1.0, 1.0))



def callback_keyboard (window, key, scancode, action, mods):
    global camera_x, camera_y

    if action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            global delta_time
            delta_time = 0 if delta_time == 1 else 1
        elif key == glfw.KEY_RIGHT:
            camera_x += camera_speed
        elif key == glfw.KEY_UP:
            camera_y += camera_speed
        elif key == glfw.KEY_LEFT:
            camera_x -= camera_speed
        elif key == glfw.KEY_DOWN:
            camera_y -= camera_speed
            


def callback_cursor_position (window, pos_x, pos_y):
    #print(f'{pos_x = }, {pos_y = }')
    pass



def callback_scroll (window, offset_x, offset_y):
    global zoom
    if offset_y > 0:
        zoom *= zoom_speed
    elif offset_y < 0:
        zoom /= zoom_speed
    #print(f'{zoom = }')



def start_glfw_window ():
    if not glfw.init(): # Initialize the library
        return
    
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(window_w, window_h, window_name, None, None) 
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window) # Make the window's context current

    glfw.set_key_callback(window, callback_keyboard)
    glfw.set_cursor_pos_callback(window, callback_cursor_position)
    glfw.set_scroll_callback(window, callback_scroll)

    while (working) and (glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS) and (not glfw.window_should_close(window)):
        # Loop until the user closes the window
        # Render here, e.g. using pyOpenGL:
        width, height = glfw.get_framebuffer_size(window)
        ratio = width / float(height)
        glViewport(0, 0, width, height)
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-ratio, ratio, -1, 1, 1, -1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        update()

        glfw.swap_buffers(window) # Swap front and back buffers
        glfw.poll_events() # Poll for and process events

    before_exit()
    glfw.terminate()



if __name__ == '__main__':
    main()





'''
print(glfw.get_time())
glRotatef(glfw.get_time() * 50, 0, 0, 1)


















'''
