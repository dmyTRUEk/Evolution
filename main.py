'''
This is main file of evolution
'''



import glfw

from OpenGL.GL import *
#import OpenGL.GL as gl
#import OpenGL.GLU as glu
#import OpenGL.GLUT as glut

#import time

from consts import *
from world_and_cells import *





world = World()

zoom = 1 / 100
camera_x, camera_y = 0, 0

delta_time = 1



def main ():
    global world
    world = World(food_amount)

    for i in range(cells_amount):
        world.add_cell(Cell(
            random.randint(-bounds_spawn_cell, bounds_spawn_cell),
            random.randint(-bounds_spawn_cell, bounds_spawn_cell),
            1000,
        ))

    #world.init_random()

    start_glfw_window()



def update ():
    if delta_time != 0:
        world.update(delta_time)

    print(f'cells_amount = {len(world.cells)}')
    print('Cell energies = {')
    for cell in world.cells:
        print(cell.energy, end=' ')
    print('\n}\n\n')

    render_frame()



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
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, glfw.FALSE)
        elif key == glfw.KEY_SPACE:
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
    window = glfw.create_window(window_w, window_h, 'Yeah, Science!', None, None) 
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window) # Make the window's context current

    glfw.set_key_callback(window, callback_keyboard)
    glfw.set_cursor_pos_callback(window, callback_cursor_position)
    glfw.set_scroll_callback(window, callback_scroll)

    while (glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS) and (not glfw.window_should_close(window)):
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

    glfw.terminate()



if __name__ == '__main__':
    main()





'''
print(glfw.get_time())
glRotatef(glfw.get_time() * 50, 0, 0, 1)


















'''
