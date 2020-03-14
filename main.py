'''
This is main file of evolution
'''



import glfw

from OpenGL.GL import *
#import OpenGL.GL as gl
#import OpenGL.GLU as glu
#import OpenGL.GLUT as glut

#import time

from world_and_cells import *





window_w, window_h = 1600, 900

world = World()
zoom = 1 / 100

delta_time = 1



def main ():
    global world
    world = World()

    bounds = 100
    for i in range(100):
        world.add_cell(Cell(
            random.randint(-bounds, bounds),
            random.randint(-bounds, bounds),
        ))

    world.init_random()

    start_glfw_window()



def draw_frame ():
    world.update(delta_time)

    render_frame()



def render_frame ():
    for cell in world.cells:
        x1 = (cell.x) * zoom
        y1 = (cell.y) * zoom
        x2 = (cell.x+1) * zoom
        y2 = (cell.y+1) * zoom

        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 0.5)
        glVertex2f(x1, y1)
        glVertex2f(x2, y1)
        glVertex2f(x2, y2)
        glVertex2f(x1, y2)
        glEnd()



def callback_keyboard (window, key, scancode, action, mods):
    #print(f'{key = }')
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, glfw.FALSE)
    elif key == glfw.KEY_SPACE and action == glfw.PRESS:
        global delta_time
        delta_time = 0 if delta_time == 1 else 1



def callback_cursor_position (window, pos_x, pos_y):
    #print(f'{pos_x = }, {pos_y = }')
    pass



def callback_scroll (window, offset_x, offset_y):
    global zoom
    delta_zoom = 1.1
    if offset_y > 0:
        zoom *= delta_zoom
    elif offset_y < 0:
        zoom /= delta_zoom
    #print(f'{zoom = }')



def start_glfw_window ():
    if not glfw.init(): # Initialize the library
        return
    
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(window_w, window_h, 'Hello World', None, None) 
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

        draw_frame()

        glfw.swap_buffers(window) # Swap front and back buffers
        glfw.poll_events() # Poll for and process events

    glfw.terminate()



if __name__ == '__main__':
    main()





'''
print(glfw.get_time())
glRotatef(glfw.get_time() * 50, 0, 0, 1)


















'''
