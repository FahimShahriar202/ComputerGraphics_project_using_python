from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import math
import random
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
from OpenGL.GLUT import GLUT_BITMAP_TIMES_ROMAN_24

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800


PLAYER_RADIUS = 2
PLAYER_SIZE = 4
PLAYER_JUMP_FORCE = 10
GRAVITY = 1.5
PLAYER_SPEED = 8


camera_pos = [0, 60, 35]
camera_angle = 0
camera_ht = 40


COLLECT_RANGE = 8
CUBE_SIZE = 3
PLATFORM_HEIGHT = 1.5

game_state = "MENU"
player_pos = [0.0, 0.0, 10.0]
player_velocity = [0.0, 0.0, 0.0]
player_lives = 3
player_score = 0
level_number = 1
speed_boost_active = False
speed_boost_end_time = 0
level_complete_popup = False
level_complete_time = 0
level_start_time = time.time()
popup_text = ""
popup_time = 0

first_person_view = False

first_person_angle = 0


cube_touch_time = 0
cube_touch_active = False
cube_touch_platform = None

cubes = []
obstacles = []
platforms = []


clouds = []
stars = []
mountains = []


base = WINDOW_WIDTH
height = WINDOW_HEIGHT
bend_angle = 6
speed = 12
rain_list = []
for i in range(150):
    rain_list.append([random.randint(0, base), random.randint(int(height*0.5), height)])

def rain_lines():
    glColor3f(0.5, 0.5, 0.9)
    glBegin(GL_LINES)
    for i in rain_list:
        glVertex2f(i[0], i[1])
        glVertex2f(i[0] + bend_angle, i[1] - 20)
    glEnd()

def init_visuals():
    global clouds, stars, mountains

    clouds.clear()
    cloud_positions = [
        (-25, 25), (-15, 30), (20, 28), (28, 32), (-30, 35),
        (10, 40), (-5, 38), (25, 45), (-20, 42), (15, 50)
    ]
    for i, (x, y) in enumerate(cloud_positions):
        clouds.append({
            'x': x,
            'y': y,
            'z': 40,
            'width': random.uniform(4, 7),
            'height': random.uniform(1.5, 3)
        })

    stars.clear()
    for _ in range(25):
        stars.append({
            'x': random.uniform(-40, 40),
            'y': random.uniform(-40, 40),
            'z': 50,
            'size': random.uniform(0.2, 0.4)
        })

    mountains.clear()
    mountain_positions = [(-35, -30), (-15, -25), (5, -28), (25, -32)]
    for i, (x, y) in enumerate(mountain_positions):
        mountains.append({
            'x': x,
            'y': y,
            'height': random.uniform(8, 18),
            'width': random.uniform(10, 22)
        })

def init_game():

    global player_pos, player_velocity, player_lives, player_score, level_number
    global cubes, obstacles, platforms, game_state
    global speed_boost_active, speed_boost_end_time, level_complete_popup
    global level_start_time, camera_angle, camera_ht
    global cube_touch_time, cube_touch_active, cube_touch_platform

    player_pos = [0.0, 0.0, 10.0]
    player_velocity = [0.0, 0.0, 0.0]
    player_lives = 3
    player_score = 0
    level_number = 1
    speed_boost_active = False
    speed_boost_end_time = 0
    level_complete_popup = False
    camera_angle = 0
    camera_ht = 35


    cube_touch_time = 0
    cube_touch_active = False
    cube_touch_platform = None

    init_visuals()

    cubes.clear()
    obstacles.clear()
    platforms.clear()

    load_level(1)
    game_state = "PLAYING"
    level_start_time = time.time()

def load_level(level_num):

    global cubes, obstacles, platforms, level_number, level_start_time
    global level_complete_popup, cube_touch_time, cube_touch_active, cube_touch_platform

    level_number = level_num
    level_start_time = time.time()
    level_complete_popup = False

    cube_touch_time = 0
    cube_touch_active = False
    cube_touch_platform = None

    cubes.clear()
    obstacles.clear()
    platforms.clear()

    global PLAYER_JUMP_FORCE, GRAVITY
    if level_num == 1:
        PLAYER_JUMP_FORCE = 10
        GRAVITY = 1.5
        PLATFORM_W, PLATFORM_D, PLATFORM_H = 8, 8, PLATFORM_HEIGHT
        platforms.extend([
            {"x": 0, "y": 0, "z": 0, "width": 40, "depth": 60, "height": PLATFORM_HEIGHT, "color": (0.5, 0.4, 0.3)},
            {"x": 12, "y": 12, "z": 8, "width": PLATFORM_W, "depth": PLATFORM_D, "height": PLATFORM_H, "color": (0.6, 0.6, 0.6)},
            {"x": -10, "y": 8, "z": 6, "width": PLATFORM_W, "depth": PLATFORM_D, "height": PLATFORM_H, "color": (0.6, 0.6, 0.6)},
        ])

        cubes.extend([
            {"x": 12, "y": 12, "z": 8 + PLATFORM_HEIGHT, "color": (1, 0, 0), "collected": False, "rotation": 0},
            {"x": -10, "y": 8, "z": 6 + PLATFORM_HEIGHT, "color": (0, 0, 1), "collected": False, "rotation": 0},
            {"x": 0, "y": -5, "z": 2, "color": (0, 1, 0), "collected": False, "rotation": 0},
        ])

        obstacles.extend([
            {"x": 5, "y": 0, "z": 2, "type": "bouncing", "base_z": 2, "radius": 1.5, "speed": 1.5, "start_time": time.time()},
            {"x": -5, "y": 15, "z": 2, "type": "cone_bouncing", "base_z": 2, "radius": 2, "speed": 1.8, "start_time": time.time()},
        ])

    elif level_num == 2:
        PLAYER_JUMP_FORCE = 10
        GRAVITY = 1.5
        PLATFORM_W, PLATFORM_D, PLATFORM_H = 8, 8, PLATFORM_HEIGHT
        platforms.extend([
            {"x": 0, "y": 0, "z": 0, "width": 40, "depth": 60, "height": PLATFORM_HEIGHT, "color": (0.4, 0.3, 0.2)},
            {"x": 15, "y": 0, "z": 10, "width": PLATFORM_W, "depth": PLATFORM_D, "height": PLATFORM_H, "color": (0.5, 0.5, 0.7)},
            {"x": -15, "y": 0, "z": 10, "width": PLATFORM_W, "depth": PLATFORM_D, "height": PLATFORM_H, "color": (0.5, 0.5, 0.7)},
            {"x": 15, "y": 18, "z": 10, "width": PLATFORM_W, "depth": PLATFORM_D, "height": PLATFORM_H, "color": (0.5, 0.5, 0.7)},
            {"x": -15, "y": 18, "z": 10, "width": PLATFORM_W, "depth": PLATFORM_D, "height": PLATFORM_H, "color": (0.5, 0.5, 0.7)},
        ])

        cubes.extend([
            {"x": 15, "y": 0, "z": 10 + PLATFORM_HEIGHT, "color": (1, 0, 0), "collected": False, "rotation": 0},
            {"x": -15, "y": 0, "z": 10 + PLATFORM_HEIGHT, "color": (1, 0, 0), "collected": False, "rotation": 0},
            {"x": 0, "y": 0, "z": 2, "color": (0, 0, 1), "collected": False, "rotation": 0},
            {"x": 15, "y": 18, "z": 10 + PLATFORM_HEIGHT, "color": (1, 0, 0), "collected": False, "rotation": 0},
            {"x": -15, "y": 18, "z": 10 + PLATFORM_HEIGHT, "color": (1, 0, 0), "collected": False, "rotation": 0},
        ])

        obstacles.extend([
            {"x": 8, "y": 8, "z": 4, "type": "bouncing", "base_z": 4, "radius": 1.5, "speed": 2, "start_time": time.time()},
            {"x": -8, "y": -8, "z": 4, "type": "spinning", "radius": 2, "rotation": 0, "speed": 60, "start_time": time.time()},
            {"x": 0, "y": 10, "z": 4, "type": "sliding", "start_x": 0, "range": 8, "radius": 1.5, "speed": 2, "start_time": time.time()},
            {"x": -15, "y": 15, "z": 4, "type": "cone_bouncing", "base_z": 4, "radius": 2.2, "speed": 2.5, "start_time": time.time()},

            {"x": 18, "y": 0, "z": 13, "type": "bouncing", "base_z": 12, "radius": 0.4, "speed": 2.5, "start_time": time.time()},
            {"x": -19, "y": 0, "z": 13, "type": "cone_bouncing", "base_z": 12, "radius": 1, "speed": 2.5, "start_time": time.time()},
            {"x": 17, "y": 22, "z": 11, "type": "sliding", "start_x": 17, "range": 2, "radius": 0.8, "speed": 2, "start_time": time.time()},
            {"x": -17, "y": 16, "z": 11, "type": "spinning", "radius": 1, "rotation": 0, "speed": 70, "start_time": time.time()},
        ])

    elif level_num == 3:
        PLAYER_JUMP_FORCE = 10
        GRAVITY = 1.5
        PLATFORM_W, PLATFORM_D, PLATFORM_H = 8, 8, PLATFORM_HEIGHT
        platforms.extend([
            {"x": 0, "y": 0, "z": 0, "width": 40, "depth": 60, "height": PLATFORM_HEIGHT, "color": (0.3, 0.2, 0.1)},
            {"x": 12, "y": 12, "z": 15, "width": PLATFORM_W, "depth": PLATFORM_D, "height": PLATFORM_H, "color": (0.4, 0.4, 0.4)},
            {"x": -12, "y": 12, "z": 15, "width": PLATFORM_W, "depth": PLATFORM_D, "height": PLATFORM_H, "color": (0.4, 0.4, 0.4)},
            {"x": 0, "y": 0, "z": 15, "width": 6, "depth": 6, "height": PLATFORM_HEIGHT, "color": (0.5, 0.5, 0.5), "type": "moving_y", "start_y": 0, "range": 15, "speed": 1.5, "start_time": time.time()},
        ])

        cubes.extend([
            {"x": 12, "y": 12, "z": 15 + PLATFORM_HEIGHT, "color": (1, 0, 0), "collected": False, "rotation": 0},
            {"x": -12, "y": 12, "z": 15 + PLATFORM_HEIGHT, "color": (1, 0, 0), "collected": False, "rotation": 0},
            {"x": 0, "y": 0, "z": 2, "color": (0, 0, 1), "collected": False, "rotation": 0},
            {"x": 0, "y": 0, "z": 15 + PLATFORM_HEIGHT, "color": (1, 0, 0), "collected": False, "rotation": 0, "special_cube": True},
        ])

        obstacles.extend([
            {"x": 6, "y": 0, "z": 6, "type": "bouncing", "base_z": 6, "radius": 2, "speed": 3, "start_time": time.time()},
            {"x": -8, "y": -8, "z": 4, "type": "spinning", "radius": 2.5, "rotation": 0, "speed": 80, "start_time": time.time()},
            {"x": 0, "y": 10, "z": 6, "type": "sliding", "start_x": 0, "range": 10, "radius": 1.5, "speed": 2, "start_time": time.time()},
            {"x": 10, "y": -10, "z": 8, "type": "bouncing", "base_z": 8, "radius": 1.8, "speed": 2.5, "start_time": time.time()},
            {"x": -10, "y": 15, "z": 5.5, "type": "sliding", "start_x": -10, "range": 12, "radius": 1.7, "speed": 2.5, "start_time": time.time()},
        ])


def load_next_level():

    global level_number, cube_touch_time, cube_touch_active, cube_touch_platform
    if level_number < 3:
        level_number += 1
        load_level(level_number)
        player_pos[0] = 0
        player_pos[1] = 0
        player_pos[2] = 10
        player_velocity = [0, 0, 0]
    else:
        game_state = "GAME_OVER"

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):

    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_text_centered(x, y, text, font=GLUT_BITMAP_HELVETICA_18):

    text_width = sum(glutBitmapWidth(font, ord(ch)) for ch in text)
    draw_text(x - text_width/2, y, text, font)

def draw_retro_background():

    if level_number == 1:
        glClearColor(0.6, 0.8, 0.9, 1.0)
    elif level_number == 2:
        glClearColor(0.1, 0.1, 0.3, 1.0)
    else:
        glClearColor(0.3, 0.3, 0.4, 1.0)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glBegin(GL_QUADS)
    if level_number == 1:
        glColor3f(0.6, 0.8, 0.9)
        glVertex2f(0, 0)
        glVertex2f(WINDOW_WIDTH, 0)
        glColor3f(0.8, 0.9, 1.0)
        glVertex2f(WINDOW_WIDTH, WINDOW_HEIGHT)
        glVertex2f(0, WINDOW_HEIGHT)

    elif level_number == 2:
        glColor3f(0.1, 0.1, 0.3)
        glVertex2f(0, 0)
        glVertex2f(WINDOW_WIDTH, 0)
        glColor3f(0.2, 0.2, 0.4)
        glVertex2f(WINDOW_WIDTH, WINDOW_HEIGHT)
        glVertex2f(0, WINDOW_HEIGHT)

    else:
        glColor3f(0.3, 0.3, 0.4)
        glVertex2f(0, 0)
        glVertex2f(WINDOW_WIDTH, 0)
        glColor3f(0.4, 0.4, 0.5)
        glVertex2f(WINDOW_WIDTH, WINDOW_HEIGHT)
        glVertex2f(0, WINDOW_HEIGHT)
    glEnd()

    if level_number == 3:
        rain_lines()

    if level_number == 1:
        mountain_colors = [
            (0.7, 0.6, 0.45),
            (0.5, 0.5, 0.5),
            (0.6, 0.5, 0.35),
            (0.35, 0.35, 0.35)
        ]

        mountain_bases = [
            (180, 340, 220, 120),
            (340, 335, 200, 110),
            (480, 330, 220, 120),
            (620, 328, 200, 110)
        ]
        for i, (base_x, base_y, width, height) in enumerate(mountain_bases):
            glColor3f(*mountain_colors[i % len(mountain_colors)])
            glBegin(GL_TRIANGLES)
            glVertex2f(base_x, base_y)
            glVertex2f(base_x + width // 2, base_y + height)
            glVertex2f(base_x + width, base_y)
            glEnd()


        glColor3f(1.0, 1.0, 0.0)
        sun_x, sun_y = WINDOW_WIDTH - 100, WINDOW_HEIGHT - 100
        sun_radius = 40
        num_triangles = 32
        for i in range(num_triangles):
            angle1 = i * 2.0 * math.pi / num_triangles
            angle2 = (i + 1) * 2.0 * math.pi / num_triangles
            glBegin(GL_TRIANGLES)
            glVertex2f(sun_x, sun_y)
            glVertex2f(sun_x + sun_radius * math.cos(angle1), sun_y + sun_radius * math.sin(angle1))
            glVertex2f(sun_x + sun_radius * math.cos(angle2), sun_y + sun_radius * math.sin(angle2))
            glEnd()

        glColor3f(1.0, 1.0, 0.5)
        for i in range(8):
            angle = i * 45 * math.pi / 180
            ray_length = 60
            glBegin(GL_LINES)
            glVertex2f(sun_x, sun_y)
            glVertex2f(sun_x + ray_length * math.cos(angle), sun_y + ray_length * math.sin(angle))
            glEnd()

    if level_number == 1:
        glColor3f(1.0, 1.0, 1.0)
        for cloud in clouds:
            cloud_x = (cloud['x'] + 50) * 10
            cloud_y = (cloud['y'] + 50) * 7 + 200
            radius = cloud['width'] * 3

            for cx, rx, ry in [
                (cloud_x, radius, radius * 0.7),
                (cloud_x - radius * 0.7, radius * 0.8, radius * 0.6),
                (cloud_x + radius * 0.7, radius * 0.8, radius * 0.6)
            ]:
                num_triangles = 24
                for i in range(num_triangles):
                    angle1 = i * 2.0 * math.pi / num_triangles
                    angle2 = (i + 1) * 2.0 * math.pi / num_triangles
                    glBegin(GL_TRIANGLES)
                    glVertex2f(cx, cloud_y)
                    glVertex2f(cx + rx * math.cos(angle1), cloud_y + ry * math.sin(angle1))
                    glVertex2f(cx + rx * math.cos(angle2), cloud_y + ry * math.sin(angle2))
                    glEnd()

    if level_number == 2:
        glColor3f(1.0, 1.0, 1.0)
        glPointSize(2)
        glBegin(GL_POINTS)
        for star in stars:
            star_x = (star['x'] + 50) * 10
            star_y = (star['y'] + 50) * 7 + 200
            glVertex2f(star_x, star_y)
        glEnd()


    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

def draw_ground():

    glPushMatrix()

    if level_number == 1:
        glColor3f(0.0, 0.4, 0.0)
    elif level_number == 2:
       glColor3f(0.27, 0.36, 0.13)
    else:
       glColor3f(0.1, 0.3, 0.1)

    glBegin(GL_QUADS)
    glVertex3f(-150, -150, -1)
    glVertex3f(150, -150, -1)
    glVertex3f(150, 150, -1)
    glVertex3f(-150, 150, -1)
    glEnd()


    if level_number == 2:
        pipe_radius = 8
        pipe_height = 40
        cylinder_positions = [(-140, -140), (140, -140)]
        for cx, cy in cylinder_positions:
            glPushMatrix()
            glColor3f(0.5, 0.3, 0.1)
            glTranslatef(cx, cy, 0)
            gluCylinder(gluNewQuadric(), pipe_radius, pipe_radius, pipe_height, 24, 6)
            glPopMatrix()
        else:
            glColor3f(0.1, 0.3, 0.1)



    if level_number in (1, 2, 3):
        random.seed(42)
        num_patches = 500

        plat_xmin, plat_xmax = -20, 20
        plat_ymin, plat_ymax = -30, 30
        for _ in range(num_patches):
            gx = random.uniform(-130, 130)
            gy = random.uniform(-130, 130)

            if plat_xmin <= gx <= plat_xmax and plat_ymin <= gy <= plat_ymax:
                continue
            for blade in range(random.randint(3, 6)):
                offset = random.uniform(-1.2, 1.2)
                base = random.uniform(1.2, 2.2)
                height = random.uniform(2.5, 4.5)
                glColor3f(0.1, random.uniform(0.5, 0.8), 0.1)

                bx1 = gx + offset - base/2
                by1 = gy
                bx2 = gx + offset + base/2
                by2 = gy

                tx = gx + offset
                ty = gy
                tz = height
                glBegin(GL_TRIANGLES)
                glVertex3f(bx1, by1, 0.01)
                glVertex3f(bx2, by2, 0.01)
                glVertex3f(tx, ty, tz)
                glEnd()
    glPopMatrix()
def draw_platform(platform):

    glPushMatrix()
    glTranslatef(platform["x"], platform["y"], platform["z"])

    glColor3f(*platform.get("color", (0.5, 0.5, 0.5)))

    glScalef(platform["width"], platform["depth"], platform["height"])
    glutSolidCube(1)

    glPopMatrix()

def draw_cube(cube):

    if cube["collected"]:
        return

    glPushMatrix()
    glTranslatef(cube["x"], cube["y"], cube["z"])

    cube["rotation"] = (cube["rotation"] + 1) % 360
    glRotatef(cube["rotation"], 0, 1, 0)


    if cube.get("special_cube"):

        pulse = 0.8 + 0.2 * math.sin(time.time() * 5)
        glScalef(pulse, pulse, pulse)
        glColor3f(1, 0, 0)
    else:
        glColor3f(*cube["color"])

    glutSolidCube(CUBE_SIZE)

    glPopMatrix()

def draw_obstacle(obstacle):

    glPushMatrix()
    glTranslatef(obstacle["x"], obstacle["y"], obstacle["z"])

    if obstacle["type"] == "bouncing":
        glColor3f(1, 0.4, 0)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), obstacle["radius"], obstacle["radius"], 4, 8, 3)

    elif obstacle["type"] == "cone_bouncing":
        glColor3f(1.0, 0.6, 0.2)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), obstacle["radius"], 0, 6, 8, 3)

    elif obstacle["type"] == "spinning":
        glColor3f(0.7, 0.2, 0.7)
        glRotatef(obstacle["rotation"], 0, 1, 0)
        glutSolidSphere(obstacle["radius"], 8, 8)

    elif obstacle["type"] == "sliding":
        glColor3f(0.2, 0.7, 0.7)

        h = obstacle["radius"] * 2
        glBegin(GL_TRIANGLES)

        glVertex3f(-h/2, -h/2, -h/2)
        glVertex3f(h/2, -h/2, -h/2)
        glVertex3f(0, h/2, -h/2)

        glVertex3f(-h/2, -h/2, h/2)
        glVertex3f(h/2, -h/2, h/2)
        glVertex3f(0, h/2, h/2)
        glEnd()
        glBegin(GL_QUADS)

        glVertex3f(-h/2, -h/2, -h/2)
        glVertex3f(h/2, -h/2, -h/2)
        glVertex3f(h/2, -h/2, h/2)
        glVertex3f(-h/2, -h/2, h/2)

        glVertex3f(h/2, -h/2, -h/2)
        glVertex3f(0, h/2, -h/2)
        glVertex3f(0, h/2, h/2)
        glVertex3f(h/2, -h/2, h/2)

        glVertex3f(0, h/2, -h/2)
        glVertex3f(-h/2, -h/2, -h/2)
        glVertex3f(-h/2, -h/2, h/2)
        glVertex3f(0, h/2, h/2)
        glEnd()

    glPopMatrix()


def draw_player():

    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])


    glColor3f(0.4, 0.5, 0.5)

    glPushMatrix()
    glScalef(1.0, 0.8, 1.2)
    glutSolidCube(PLAYER_SIZE)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, PLAYER_SIZE * 0.6)
    glColor3f(0.9, 0.7, 0.5)
    glutSolidSphere(PLAYER_SIZE * 0.3, 6, 6)
    glPopMatrix()

    glColor3f(0.0, 0.2, 0.8)

    glPopMatrix()


def setupCamera():

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 500)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    global first_person_view, first_person_angle
    if first_person_view:

        px, py, pz = player_pos
        head_offset = PLAYER_SIZE * 0.6 + PLAYER_SIZE * 0.3
        cam_forward = 2.5
        angle_rad = math.radians(first_person_angle)
        cam_x = px + cam_forward * math.sin(angle_rad)
        cam_y = py + cam_forward * math.cos(angle_rad)
        cam_z = pz + head_offset
        look_x = px + (cam_forward + 10) * math.sin(angle_rad)
        look_y = py + (cam_forward + 10) * math.cos(angle_rad)
        look_z = cam_z
        gluLookAt(cam_x, cam_y, cam_z,
                  look_x, look_y, look_z,
                  0, 0, 1)
    else:

        angle_rad = math.radians(camera_angle)
        r = math.sqrt(camera_pos[0]**2 + camera_pos[1]**2)
        x = r * math.sin(angle_rad)
        y = r * math.cos(angle_rad)
        z = camera_ht
        gluLookAt(x, y, z,
                  0, 0, 10,
                  0, 0, 1)

def update_obstacles():

    current_time = time.time()

    for obstacle in obstacles:
        if obstacle["type"] == "bouncing":
            elapsed = current_time - obstacle["start_time"]
            obstacle["z"] = obstacle["base_z"] + math.sin(elapsed * obstacle["speed"]) * 2

        elif obstacle["type"] == "cone_bouncing":
            elapsed = current_time - obstacle["start_time"]
            obstacle["z"] = obstacle["base_z"] + math.sin(elapsed * obstacle["speed"]) * 2.5

        elif obstacle["type"] == "spinning":
            elapsed = current_time - obstacle["start_time"]
            obstacle["rotation"] = elapsed * obstacle["speed"]

        elif obstacle["type"] == "sliding":
            elapsed = current_time - obstacle["start_time"]
            obstacle["x"] = obstacle["start_x"] + math.sin(elapsed * obstacle["speed"]) * obstacle["range"]


    for platform in platforms:
        if platform.get("type") == "moving_y":
            elapsed = current_time - platform["start_time"]
            platform["y"] = platform["start_y"] + math.sin(elapsed * platform["speed"]) * platform["range"]

def check_collisions():

    global player_lives, player_score, game_state, level_number
    global speed_boost_active, speed_boost_end_time, level_complete_popup, level_complete_time
    global player_velocity, player_pos, popup_text, popup_time
    global cube_touch_time, cube_touch_active, cube_touch_platform

    current_time = time.time()

    if speed_boost_active and current_time > speed_boost_end_time:
        speed_boost_active = False

    on_platform = False
    player_on_moving_platform = None

    for platform in platforms:
        in_x = abs(player_pos[0] - platform["x"]) < platform["width"]/2 + PLAYER_RADIUS
        in_y = abs(player_pos[1] - platform["y"]) < platform["depth"]/2 + PLAYER_RADIUS

        if in_x and in_y:
            platform_top = platform["z"] + platform["height"]

            if player_pos[2] > platform_top and player_velocity[2] <= 0:
                if player_pos[2] + player_velocity[2] <= platform_top + 1:
                    player_pos[2] = platform_top + 1
                    player_velocity[2] = 0
                    on_platform = True
                    if platform.get("type") == "moving_y":
                        player_on_moving_platform = platform


    if player_pos[2] <= 1 and player_velocity[2] <= 0:
        player_pos[2] = 1
        player_velocity[2] = 0
        on_platform = True

    if not on_platform:
        player_velocity[2] -= GRAVITY


    player_pos[0] += player_velocity[0]
    player_pos[1] += player_velocity[1]
    player_pos[2] += player_velocity[2]


    if on_platform:

        snapped = False
        for platform in platforms:
            in_x = abs(player_pos[0] - platform["x"]) < platform["width"]/2 + PLAYER_RADIUS
            in_y = abs(player_pos[1] - platform["y"]) < platform["depth"]/2 + PLAYER_RADIUS
            if in_x and in_y:
                platform_top = platform["z"] + platform["height"]
                if abs(player_pos[2] - (platform_top + 1)) < 0.2:
                    player_pos[2] = platform_top + 1
                    player_velocity[2] = 0
                    snapped = True
                    if platform.get("type") == "moving_y":
                        player_on_moving_platform = platform
                    break
        if not snapped:

            player_pos[2] = 1
            player_velocity[2] = 0
            player_on_moving_platform = None


    if level_number == 3 and not cube_touch_active:
        for cube in cubes:
            if cube.get("special_cube") and not cube["collected"]:
                dx = player_pos[0] - cube["x"]
                dy = player_pos[1] - cube["y"]
                dz = player_pos[2] - cube["z"]
                distance = math.sqrt(dx*dx + dy*dy + dz*dz)


                if distance < PLAYER_RADIUS + CUBE_SIZE/2:
                    cube_touch_active = True
                    cube_touch_time = current_time
                    cube_touch_platform = player_on_moving_platform
                    popup_text = "TOUCHING SPECIAL CUBE! RIGHT-CLICK TO COLLECT!"
                    popup_time = current_time
                    break


    if cube_touch_active:
        time_left = 1.0 - (current_time - cube_touch_time)
        if time_left <= 0:

            cube_touch_active = False
            cube_touch_platform = None
            player_velocity[2] = -5
            popup_text = "TIME'S UP! FELL OFF PLATFORM!"
            popup_time = current_time
        else:

            popup_text = f"RIGHT-CLICK TO COLLECT! {time_left:.1f}s"
            popup_time = current_time

    for obstacle in obstacles:
        dx = player_pos[0] - obstacle["x"]
        dy = player_pos[1] - obstacle["y"]
        dz = player_pos[2] - obstacle["z"]
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)


        if obstacle["type"] == "sliding":

            obs_radius = obstacle.get("radius", 1.5) + 0.7
        else:
            obs_radius = obstacle.get("radius", 1.5)

        if distance <= PLAYER_RADIUS + obs_radius:
            player_lives -= 1
            popup_text = "OUCH! -1 LIFE"
            popup_time = current_time

            player_pos = [0, 0, 10]
            player_velocity = [0, 0, 0]

            if player_lives <= 0:
                game_state = "GAME_OVER"
            break


    GRASS_X_MIN = -148
    GRASS_X_MAX = 148
    GRASS_Y_MIN = -148
    GRASS_Y_MAX = 148

    outside_grass = (
        player_pos[0] < GRASS_X_MIN - PLAYER_RADIUS or
        player_pos[0] > GRASS_X_MAX + PLAYER_RADIUS or
        player_pos[1] < GRASS_Y_MIN - PLAYER_RADIUS or
        player_pos[1] > GRASS_Y_MAX + PLAYER_RADIUS
    )
    if player_pos[2] <= 1.5 and outside_grass:
        player_lives -= 1
        popup_text = "FELL OFF GRASS! -1 LIFE"
        popup_time = current_time
        player_pos = [0, 0, 10]
        player_velocity = [0, 0, 0]
        if player_lives <= 0:
            game_state = "GAME_OVER"

    red_cubes_left = [c for c in cubes if c["color"] == (1, 0, 0) and not c["collected"]]
    if not red_cubes_left and not level_complete_popup and game_state == "PLAYING":
        level_complete_popup = True
        level_complete_time = current_time

    if popup_text and current_time - popup_time > 1:
        popup_text = ""

def collect_cube_at(x, y):

    global player_score, player_lives, speed_boost_active, speed_boost_end_time
    global popup_text, popup_time

    closest_cube = None
    closest_dist = float('inf')

    for cube in cubes:
        if cube["collected"]:
            continue

        dx = player_pos[0] - cube["x"]
        dy = player_pos[1] - cube["y"]
        dz = player_pos[2] - cube["z"]
        distance = math.sqrt(dx*dx + dy*dy)


        if distance < COLLECT_RANGE and abs(dz) < PLAYER_SIZE * 0.7 and distance < closest_dist:
            closest_dist = distance
            closest_cube = cube

    if closest_cube:
        closest_cube["collected"] = True

        if closest_cube["color"] == (1, 0, 0):
            player_score += 10
            popup_text = "+10"
            popup_time = time.time()
        elif closest_cube["color"] == (0, 0, 1):
            player_lives += 1
            popup_text = "+1 LIFE"
            popup_time = time.time()
        elif closest_cube["color"] == (0, 1, 0):
            speed_boost_active = True
            speed_boost_end_time = time.time() + 5
            popup_text = "SPEED BOOST!"
            popup_time = time.time()

        return True
    return False

def collect_special_cube():

    global player_score, popup_text, popup_time, cube_touch_active, cube_touch_platform

    if cube_touch_active:
        for cube in cubes:
            if cube.get("special_cube") and not cube["collected"]:
                cube["collected"] = True
                player_score += 20
                popup_text = "+20 SPECIAL CUBE!"
                popup_time = time.time()
                cube_touch_active = False
                cube_touch_platform = None
                return True
    return False

def keyboardListener(key, x, y):

    global game_state
    global level_complete_popup, level_complete_time
    global player_velocity

    key = key.decode('utf-8').lower()

    global first_person_view
    if game_state == "MENU":
          if key == '\r':
            init_game()


    elif game_state == "PLAYING":
        current_speed = PLAYER_SPEED * 2 if speed_boost_active else PLAYER_SPEED
        import math

        if key == 'f':
            first_person_view = not first_person_view
            return
        if key == 'r':
            game_state = "MENU"
            first_person_view = False
            return
        elif key == ' ':
            on_ground = False
            for platform in platforms:
                platform_top = platform["z"] + platform["height"]
                if abs(player_pos[2] - platform_top) < 1.5:
                    dx = abs(player_pos[0] - platform["x"])
                    dy = abs(player_pos[1] - platform["y"])
                    if dx < platform["width"]/2 + 0.5 and dy < platform["depth"]/2 + 0.5:
                        on_ground = True
                        break
            if on_ground or player_pos[2] <= 1.5:
                player_velocity[2] = PLAYER_JUMP_FORCE

        if first_person_view:
            angle_rad = math.radians(first_person_angle)

            if key == 'w':
                player_pos[0] += math.sin(angle_rad) * current_speed * 0.2
                player_pos[1] += math.cos(angle_rad) * current_speed * 0.2
            elif key == 's':
                player_pos[0] -= math.sin(angle_rad) * current_speed * 0.2
                player_pos[1] -= math.cos(angle_rad) * current_speed * 0.2

            elif key == 'a':
                player_pos[0] -= math.cos(angle_rad) * current_speed * 0.2
                player_pos[1] += math.sin(angle_rad) * current_speed * 0.2
            elif key == 'd':
                player_pos[0] += math.cos(angle_rad) * current_speed * 0.2
                player_pos[1] -= math.sin(angle_rad) * current_speed * 0.2

        else:
            if key == 'w':
                player_pos[1] -= current_speed * 0.2
            elif key == 's':
                player_pos[1] += current_speed * 0.2
            elif key == 'a':
                player_pos[0] += current_speed * 0.2
            elif key == 'd':
                player_pos[0] -= current_speed * 0.2

    elif game_state == "GAME_OVER":
        if key == 'r':
            game_state = "MENU"
            first_person_view = False

def specialKeyListener(key, x, y):

    global camera_angle, camera_ht, camera_pos, first_person_view, first_person_angle

    if key == GLUT_KEY_UP:

        camera_ht += 10
        camera_pos[2] = camera_ht

    elif key == GLUT_KEY_DOWN:
        camera_ht -= 10
        camera_ht = max(10, camera_ht)
        camera_pos[2] = camera_ht

    elif key == GLUT_KEY_LEFT:
        if first_person_view:
            first_person_angle -= 5
        else:
            camera_angle -= 5

    elif key == GLUT_KEY_RIGHT:
        if first_person_view:
            first_person_angle += 5
        else:
            camera_angle += 5

def mouseListener(button, state, x, y):

    global game_state, cube_touch_active

    if game_state == "PLAYING" and not level_complete_popup:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            if collect_cube_at(x, y):
                pass
            else:
                print("No cube in range")
        elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:

            if cube_touch_active:
                collect_special_cube()

def idle():

    global game_state, level_complete_popup, level_complete_time

    if game_state == "PLAYING":
        update_obstacles()
        check_collisions()
        if level_number == 3:
            global rain_list
            for i in rain_list:
                i[0] = i[0] % base
                i[1] = (i[1] - speed) % height

        if level_complete_popup and time.time() - level_complete_time > 3:
            level_complete_popup = False
            if level_number < 3:
                load_next_level()
            else:
                game_state = "GAME_OVER"

    glutPostRedisplay()

def showScreen():

    draw_retro_background()
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    if game_state == "MENU":
        draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 60,
                          "CUBE COLLECTOR", GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 20,
                          "Retro 3D Platformer", GLUT_BITMAP_HELVETICA_18)
        draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 20,
                          "Press ENTER to Start")
        draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 60,
                          "CONTROLS:")
        draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 90,
                          "WASD = Move, SPACE = Jump")
        draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 120,
                          "Arrow Keys = Move Camera")
        draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 150,
                          "Left Click = Collect Cubes")
        draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 180,
                           "F = First Person View")
        draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 210,
                  "R = Restart")

    elif game_state == "PLAYING":
        setupCamera()

        draw_ground()

        for platform in platforms:
            draw_platform(platform)

        for cube in cubes:
            draw_cube(cube)

        for obstacle in obstacles:
            draw_obstacle(obstacle)

        draw_player()

        glDisable(GL_DEPTH_TEST)

        draw_text(20, WINDOW_HEIGHT - 30, f"SCORE: {player_score}")

        lives_text = "LIVES: "
        for i in range(player_lives):
            lives_text += "*"
        draw_text(20, WINDOW_HEIGHT - 60, lives_text)

        draw_text(20, WINDOW_HEIGHT - 90, f"LEVEL: {level_number}")

        level_names = ["SUNNY DAY", "GALAXY", "STORMY SKY"]
        draw_text(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 30, level_names[level_number-1])

        if speed_boost_active:
            time_left = max(0, speed_boost_end_time - time.time())
            glColor3f(0, 1, 0)
            draw_text(20, WINDOW_HEIGHT - 120, f"SPEED BOOST: {time_left:.1f}s")
            glColor3f(1, 1, 1)

        current_time = time.time()
        if current_time - level_start_time < 2:
            draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2,
                              f"LEVEL {level_number}")

        if popup_text and time.time() - popup_time < 1:
            if "+10" in popup_text or "+20" in popup_text:
                glColor3f(1, 0, 0)
            elif "LIFE" in popup_text:
                glColor3f(0, 0, 1)
            elif "SPEED" in popup_text:
                glColor3f(0, 1, 0)
            elif "SPECIAL" in popup_text:
                glColor3f(1, 0.5, 0)
            elif "RIGHT-CLICK" in popup_text:
                glColor3f(1, 1, 0)
            elif "TIME'S UP" in popup_text:
                glColor3f(1, 0, 0)
            elif "FELL ON GRASS" in popup_text:
                glColor3f(0, 1, 0)
            else:
                glColor3f(1, 0.5, 0)

            draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50, popup_text)
            glColor3f(1, 1, 1)

        if level_complete_popup:
            glColor3f(0, 1, 1)
            if level_number < 3:
                draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2,
                                  f"LEVEL {level_number} COMPLETE!")

            else:
                draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2,
                                  "YOU WIN!")
                draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 40,
                                  f"Final Score: {player_score}")

            glColor3f(1, 1, 1)

        glEnable(GL_DEPTH_TEST)

    elif game_state == "GAME_OVER":
        glClearColor(0.3, 0.1, 0.1, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 60,
                          "GAME OVER", GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 20,
                          f"Final Score: {player_score}")
        draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 20,
                          f"Level Reached: {level_number}")

        if level_number == 3:
            draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 60,
                              "YOU BEAT ALL 3 LEVELS!")

        draw_text_centered(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 120,
                          "Press R to Return to Menu")

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Retro Cube Collector")

    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    init_visuals()

    print("=" * 50)
    print("RETRO CUBE COLLECTOR")
    print("=" * 50)
    print("Controls:")
    print("  WASD - Move")
    print("  SPACE - Jump")
    print("  Arrow Keys - Move Camera")
    print("  Left Click - Collect cubes (when near)")
    print("  Right Click - Collect special cube (level 3)")
    print("  ENTER - Start/Continue")
    print("  R = Restart")
    print("=" * 50)

    glutMainLoop()

if __name__ == "__main__":
    main()