from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math

camera_offset = (0, -80, 50)
def get_camera_pos():
    px, py, pz = player_pos
    return (px + camera_offset[0], py + camera_offset[1], pz + camera_offset[2])


fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines
rand_var = 423

player_pos = (0, 0, 50)
player_size = 40


player_limb_size = 8
player_head_size = 12
pistol_length = 25
pistol_width = 5
player_angle = 0

# Bullet properties
bullets = []  # Each bullet: (x, y, z, angle, speed, active)
BULLET_RADIUS = 2
BULLET_LENGTH = 20
BULLET_COLOR = (1, 1, 0)  # Yellow
BULLET_SPEED = 15


GROUND_SIZE = 3000
GROUND_COLOR = (0.3, 0.6, 0.3)
WALL_COLOR = (0.5, 0.5, 0.5)
WALL_HEIGHT = 200

third_person_view = False
third_person_distance = 300



# Road properties
ROAD_WIDTH = 800
ROAD_COLOR = (0.3, 0.3, 0.3)  # Ash
ROAD_DEPTH = 1


import random

# Car properties
CAR_COUNT = 10
CAR_BODY_COLOR = (0.8, 0.2, 0.2)  # Red
CAR_UPPER_COLOR = (1,1,1)  # Lighter red
TIRE_COLOR = (0.1, 0.1, 0.1)  # Black
CAR_WIDTH = 100
CAR_LENGTH = 200
CAR_HEIGHT = 60
TIRE_RADIUS = 20

# Store car positions
CAR_SPEED = 2
car_positions = []  # Each element: (x, y, z, angle, current_corner)

# Define the rectangular track corners (clockwise)
CORNERS = [
    (GROUND_SIZE - 200 - CAR_WIDTH/2, GROUND_SIZE - 200 - CAR_WIDTH/2, 180),   # Top-right, facing west
    (-GROUND_SIZE + 200 + CAR_WIDTH/2, GROUND_SIZE - 200 - CAR_WIDTH/2, 270),  # Top-left, facing south
    (-GROUND_SIZE + 200 + CAR_WIDTH/2, -GROUND_SIZE + 200 + CAR_WIDTH/2, 0),   # Bottom-left, facing east
    (GROUND_SIZE - 200 - CAR_WIDTH/2, -GROUND_SIZE + 200 + CAR_WIDTH/2, 90)    # Bottom-right, facing north
]

# Property boundary walls
PROPERTY_SIZE = GROUND_SIZE - 800  # Smaller than road track
PROPERTY_WALL_COLOR = (0.7, 0.7, 0.7)  # Light grey
PROPERTY_WALL_HEIGHT = 350
WALL_OPENING_WIDTH = 4000  # Opening in the wall


# House properties
HOUSE1_POS = (-1000, 1000, 0)
HOUSE2_POS = (1000, -1000, 0)
HOUSE_SIZE =1500
HOUSE_HEIGHT = 250
HOUSE_WALL_COLOR = (0.4, 0.4, 0.4)  # Dark grey
HOUSE_ROOF_COLOR = (0.6, 0.3, 0.1)  # Brown
HOUSE_DOOR_COLOR = (0.6, 0.2, 0.8)  # Violet
HOUSE_DOOR_WIDTH = 20
HOUSE_DOOR_HEIGHT = 40
HOUSE_DOOR_DEPTH = 5


game_over = False
game_over_civilian = False
game_over_car = False

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_ground():
    glBegin(GL_QUADS)
    glColor3f(*GROUND_COLOR)
    glVertex3f(-GROUND_SIZE, -GROUND_SIZE, 0)
    glVertex3f(GROUND_SIZE, -GROUND_SIZE, 0)
    glVertex3f(GROUND_SIZE, GROUND_SIZE, 0)
    glVertex3f(-GROUND_SIZE, GROUND_SIZE, 0)
    glEnd()

def draw_player():
    glPushMatrix()
    glTranslatef(*player_pos)
    glRotatef(player_angle, 0, 0, 1)
    
    # Body (cube)
    glColor3f(0, 0, 1)
    glutSolidCube(player_size)
    
    #lower Gun barrel  (cylindrical shape pointing in facing direction)
    glPushMatrix()
    glTranslatef(-30, -player_size*1.5, 5)  # Move to front of body
    glRotatef(90, 0, 1, 0)  # Rotate to point forward
    glColor3f(.8, 0.5, 0.1)
    gluCylinder(gluNewQuadric(), 2, 2, pistol_length*3, 8, 8)
    glPopMatrix()
    
    #upper Gun barrel
    glPushMatrix()
    glTranslatef(-20, -player_size*1.5, 10)  # Move to front of body
    glRotatef(90, 0, 1, 0)  # Rotate to point forward
    glColor3f(0.1, 0.1, 0)
    gluCylinder(gluNewQuadric(), 3, 3, pistol_length*3, 8, 8)
    glPopMatrix()
    
    glPopMatrix()

def draw_walls():
    glColor3f(*WALL_COLOR)
    
    # North wall
    glPushMatrix()
    glTranslatef(0, GROUND_SIZE, WALL_HEIGHT/2)
    glScalef(GROUND_SIZE*2, 10, WALL_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    
    # South wall
    glPushMatrix()
    glTranslatef(0, -GROUND_SIZE, WALL_HEIGHT/2)
    glScalef(GROUND_SIZE*2, 10, WALL_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    
    # East wall
    glPushMatrix()
    glTranslatef(GROUND_SIZE, 0, WALL_HEIGHT/2)
    glScalef(10, GROUND_SIZE*2, WALL_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    
    # West wall
    glPushMatrix()
    glTranslatef(-GROUND_SIZE, 0, WALL_HEIGHT/2)
    glScalef(10, GROUND_SIZE*2, WALL_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()




def draw_facing_arrow():
    px, py, pz = player_pos
    arrow_length = 100
    arrow_x = px + arrow_length * math.cos(math.radians(player_angle))
    arrow_y = py + arrow_length * math.sin(math.radians(player_angle))
    
    glColor3f(1, 1, 0)  # Yellow arrow
    glLineWidth(3)
    
    # Arrow line
    glBegin(GL_LINES)
    glVertex3f(px, py, pz + 5)
    glVertex3f(arrow_x, arrow_y, pz + 5)
    glEnd()
    
    # Arrow head
    glPushMatrix()
    glTranslatef(arrow_x, arrow_y, pz + 5)
    glRotatef(player_angle, 0, 0, 1)
    glutSolidCone(10, 20, 8, 8)
    glPopMatrix()
    
    glLineWidth(1)

def draw_crosshair():
    crosshair_radius = 8
    if not third_person_view:  # Only show in first person
        px, py, pz = player_pos
        crosshair_distance = 500  # Far ahead
        crosshair_x = (px-50) + crosshair_distance * math.cos(math.radians(player_angle))
        crosshair_y = (py-50) + crosshair_distance * math.sin(math.radians(player_angle))
        crosshair_z = pz + 15  # Gun height
        
        glPushMatrix()
        glTranslatef(crosshair_x, crosshair_y, crosshair_z)
        glColor3f(1, 0, 0)
        glutSolidSphere(crosshair_radius, 10, 10)
        glPopMatrix()

def draw_road():
    global ROAD_WIDTH, ROAD_COLOR, ROAD_DEPTH
    glColor3f(*ROAD_COLOR)
    
    # Road is a rectangle inside the boundary walls
    road_margin = 200  # Distance from walls
    road_outer_x = GROUND_SIZE - road_margin
    road_outer_y = GROUND_SIZE - road_margin
    road_inner_x = GROUND_SIZE - road_margin -300
    road_inner_y = GROUND_SIZE - road_margin -300
    
    # Draw the road as a thick rectangle (filled quad)
    glBegin(GL_QUADS)
    
    # Outer rectangle (the road itself)
    glVertex3f(-road_outer_x, -road_outer_y, 1)
    glVertex3f(road_outer_x, -road_outer_y, 1)
    glVertex3f(road_outer_x, road_outer_y, 1)
    glVertex3f(-road_outer_x, road_outer_y, 1)
    
    # Inner rectangle cutout (grass area inside track)
    glColor3f(*GROUND_COLOR)  # Switch to grass color for inner area
    glVertex3f(-road_inner_x, -road_inner_y, 2)
    glVertex3f(road_inner_x, -road_inner_y, 2)
    glVertex3f(road_inner_x, road_inner_y, 2)
    glVertex3f(-road_inner_x, road_inner_y, 2)
    
    glEnd()


def generate_car_positions():
    global car_positions
    car_positions = []
    
    # Spread cars evenly around the track
    track_length = (GROUND_SIZE - 200) * 8  # Perimeter
    spacing = track_length / CAR_COUNT
    
    for i in range(CAR_COUNT):
        # Calculate position along track
        distance = i * spacing
        
        # Determine which segment the car is on
        segment_length = (GROUND_SIZE - 200) * 2
        
        if distance < segment_length:  # Top segment
            x = GROUND_SIZE - 200 - CAR_WIDTH/2 - distance
            y = GROUND_SIZE - 200 - CAR_WIDTH/2
            angle = 180
            corner = 0
        elif distance < segment_length * 2:  # Left segment
            offset = distance - segment_length
            x = -GROUND_SIZE + 200 + CAR_WIDTH/2
            y = GROUND_SIZE - 200 - CAR_WIDTH/2 - offset
            angle = 270
            corner = 1
        elif distance < segment_length * 3:  # Bottom segment
            offset = distance - segment_length * 2
            x = -GROUND_SIZE + 200 + CAR_WIDTH/2 + offset
            y = -GROUND_SIZE + 200 + CAR_WIDTH/2
            angle = 0
            corner = 2
        else:  # Right segment
            offset = distance - segment_length * 3
            x = GROUND_SIZE - 200 - CAR_WIDTH/2
            y = -GROUND_SIZE + 200 + CAR_WIDTH/2 + offset
            angle = 90
            corner = 3
        
        car_positions.append((x, y, 0, angle, corner))

def move_cars():
    global car_positions
    new_positions = []
    
    for x, y, z, angle, corner in car_positions:
        # Move based on current angle
        if angle == 180:  # West on top
            x -= CAR_SPEED
            if x <= CORNERS[1][0]:  # Reached top-left corner
                x = CORNERS[1][0]
                y = CORNERS[1][1]
                angle = 270
                corner = 1
        elif angle == 270:  # South on left
            y -= CAR_SPEED
            if y <= CORNERS[2][1]:  # Reached bottom-left corner
                x = CORNERS[2][0]
                y = CORNERS[2][1]
                angle = 0
                corner = 2
        elif angle == 0:  # East on bottom
            x += CAR_SPEED
            if x >= CORNERS[3][0]:  # Reached bottom-right corner
                x = CORNERS[3][0]
                y = CORNERS[3][1]
                angle = 90
                corner = 3
        elif angle == 90:  # North on right
            y += CAR_SPEED
            if y >= CORNERS[0][1]:  # Reached top-right corner
                x = CORNERS[0][0]
                y = CORNERS[0][1]
                angle = 180
                corner = 0
        
        new_positions.append((x, y, z, angle, corner))
    
    car_positions = new_positions

def check_collisions():
    global game_over, player_pos,game_over_car,game_over_civilian
    
    if game_over:
        return
    
    px, py, pz = player_pos
    player_radius = player_size / 2
    
    for x, y, z, angle, corner in car_positions:
        # Simple bounding box collision detection
        car_half_length = CAR_LENGTH / 2
        car_half_width = CAR_WIDTH / 2
        
        # Check if player's bounding circle intersects with car's bounding rectangle
        closest_x = max(x - car_half_length, min(px, x + car_half_length))
        closest_y = max(y - car_half_width, min(py, y + car_half_width))
        
        distance_x = px - closest_x
        distance_y = py - closest_y
        
        distance_squared = distance_x**2 + distance_y**2
        
        if distance_squared < player_radius**2:
            game_over = True
            game_over_car = True
            return

def check_bullet_car_collisions():
    global bullets, car_positions, CAR_SPEED, game_over,game_over_civilian
    
    new_bullets = []
    car_hit = False
    
    for bullet in bullets:
        bx, by, bz, bangle, bspeed, active = bullet
        
        if not active:
            continue
            
        bullet_hit = False
        
        for i, (cx, cy, cz, cangle, ccorner) in enumerate(car_positions):
            # Simple circle-circle collision detection
            car_half_length = CAR_LENGTH / 2
            distance = math.sqrt((bx - cx)**2 + (by - cy)**2)
            
            # If bullet is within car's bounding circle
            if distance < car_half_length:
                bullet_hit = True
                car_hit = True
                break
        
        if not bullet_hit:
            new_bullets.append(bullet)
    
    bullets = new_bullets
    
    # Double car speed if any car was hit
    if car_hit and CAR_SPEED < 10:
        CAR_SPEED *= 2
    elif car_hit and CAR_SPEED >10: 
        game_over = True
        game_over_civilian = True

def fire_bullet():
    if game_over:
        return
    
    px, py, pz = player_pos
    
    # Calculate bullet start position (tip of upper gun barrel)
    bullet_x = px + (+60) * math.cos(math.radians(player_angle)) - (-player_size*1.5) * math.sin(math.radians(player_angle))
    bullet_y = py + (+60) * math.sin(math.radians(player_angle)) + (-player_size*1.5) * math.cos(math.radians(player_angle))
    bullet_z = pz + 10
    
    bullets.append((bullet_x, bullet_y, bullet_z, player_angle, BULLET_SPEED, True))

def move_bullets():
    global bullets
    new_bullets = []
    
    for x, y, z, angle, speed, active in bullets:
        if not active:
            continue
            
        # Move bullet in its firing direction
        x += speed * math.cos(math.radians(angle))
        y += speed * math.sin(math.radians(angle))
        
        # Check if bullet is out of bounds
        if (abs(x) > GROUND_SIZE or abs(y) > GROUND_SIZE):
            active = False
        else:
            new_bullets.append((x, y, z, angle, speed, active))
    
    bullets = new_bullets

def draw_bullet(x, y, z, angle):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(angle, 0, 0, 1)
    glRotatef(90, 0, 1, 0)  # Rotate cylinder to point forward
    
    glColor3f(*BULLET_COLOR)
    gluCylinder(gluNewQuadric(), BULLET_RADIUS, BULLET_RADIUS, 
                BULLET_LENGTH, 8, 8)
    
    glPopMatrix()

def draw_all_bullets():
    for x, y, z, angle, speed, active in bullets:
        if active:
            draw_bullet(x, y, z, angle)

def draw_all_cars():
    for x, y, z, angle, _ in car_positions:
        draw_car(x, y, z, angle)

def draw_car(x, y, z, angle):
    
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(angle, 0, 0, 1)
    
    # Draw tires first (lowest)
    tire_offset_x = CAR_LENGTH/2 - TIRE_RADIUS
    tire_offset_y = CAR_WIDTH/2 - TIRE_RADIUS
    
    glColor3f(*TIRE_COLOR)
    
    # Front left tire (front based on rotation)
    glPushMatrix()
    glTranslatef(-tire_offset_x, -tire_offset_y, 10)
    glutSolidSphere(TIRE_RADIUS, 8, 8)
    glPopMatrix()
    
    # Front right tire
    glPushMatrix()
    glTranslatef(-tire_offset_x, tire_offset_y, 10)
    glutSolidSphere(TIRE_RADIUS, 8, 8)
    glPopMatrix()
    
    # Rear left tire
    glPushMatrix()
    glTranslatef(tire_offset_x, -tire_offset_y, 10)
    glutSolidSphere(TIRE_RADIUS, 8, 8)
    glPopMatrix()
    
    # Rear right tire
    glPushMatrix()
    glTranslatef(tire_offset_x, tire_offset_y, 10)
    glutSolidSphere(TIRE_RADIUS, 8, 8)
    glPopMatrix()
    
    # Lower body (above tires)
    glPushMatrix()
    glTranslatef(0, 0, CAR_HEIGHT/2)
    glColor3f(*CAR_BODY_COLOR)
    glScalef(CAR_LENGTH, CAR_WIDTH, CAR_HEIGHT/2)
    glutSolidCube(1)
    glPopMatrix()
    
    # Upper body (topmost)
    glPushMatrix()
    glTranslatef(0, 0, CAR_HEIGHT)
    glColor3f(*CAR_UPPER_COLOR)
    glScalef(CAR_LENGTH/2, CAR_WIDTH/1.2, CAR_HEIGHT/2)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()

def draw_property_walls():
    glColor3f(*PROPERTY_WALL_COLOR)
    
    # North wall (with opening in the middle)
    glPushMatrix()
    glTranslatef(0, PROPERTY_SIZE, 0)
    
    # Left segment of north wall
    glPushMatrix()
    glTranslatef(-(PROPERTY_SIZE)/2, 0, 0)
    glScalef(PROPERTY_SIZE, 10, PROPERTY_WALL_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    
    # Right segment of north wall
    glPushMatrix()
    glTranslatef((PROPERTY_SIZE - WALL_OPENING_WIDTH/2)/2, 0, 0)
    glScalef(PROPERTY_SIZE, 10, PROPERTY_WALL_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()
    
    # South wall (full)
    glPushMatrix()
    glTranslatef(0, -PROPERTY_SIZE, 0)
    glScalef(PROPERTY_SIZE*2, 10, PROPERTY_WALL_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    
    # East wall (full)
    glPushMatrix()
    glTranslatef(PROPERTY_SIZE, 0, 0)
    glScalef(10, PROPERTY_SIZE*2, PROPERTY_WALL_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    
    # West wall (full)
    glPushMatrix()
    glTranslatef(-PROPERTY_SIZE, 0, 0)
    glScalef(10, PROPERTY_SIZE*2, PROPERTY_WALL_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()

def draw_house(x, y, z, facing_angle):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(facing_angle, 0, 0, 1)
    glColor3f(*HOUSE_WALL_COLOR)
    
    # Front wall (with door)
    glPushMatrix()
    glTranslatef(0, HOUSE_SIZE/2, HOUSE_HEIGHT/2)
    glScalef(HOUSE_SIZE, 10, HOUSE_HEIGHT)
    glutSolidCube(1)
    
    # Door on front wall
    glPushMatrix()
    glTranslatef(0, 5, -HOUSE_HEIGHT/4)
    glColor3f(*HOUSE_DOOR_COLOR)
    glScalef(HOUSE_DOOR_WIDTH, HOUSE_DOOR_DEPTH, HOUSE_DOOR_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    glPopMatrix()
    
    # Back wall
    glPushMatrix()
    glTranslatef(0, -HOUSE_SIZE/2, HOUSE_HEIGHT/2)
    glScalef(HOUSE_SIZE, 10, HOUSE_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    
    # Left wall
    glPushMatrix()
    glTranslatef(-HOUSE_SIZE/2, 0, HOUSE_HEIGHT/2)
    glScalef(10, HOUSE_SIZE, HOUSE_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    
    # Right wall
    glPushMatrix()
    glTranslatef(HOUSE_SIZE/2, 0, HOUSE_HEIGHT/2)
    glScalef(10, HOUSE_SIZE, HOUSE_HEIGHT)
    glutSolidCube(1)
    glPopMatrix()
    
    # Roof (rectangular prism)
    glColor3f(*HOUSE_ROOF_COLOR)
    glPushMatrix()
    glTranslatef(0, 0, HOUSE_HEIGHT + 30)
    glScalef(HOUSE_SIZE + 20, HOUSE_SIZE + 20, 60)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()

def draw_all_houses():
    # House 1: facing south (180 degrees)
    draw_house(HOUSE1_POS[0], HOUSE1_POS[1], HOUSE1_POS[2], 180)
    
    # House 2: facing south (180 degrees)
    draw_house(HOUSE2_POS[0], HOUSE2_POS[1], HOUSE2_POS[2], 180)

def keyboardListener(key, x, y):
    global player_pos, player_angle, third_person_view
    if key == b'v':
        third_person_view = not third_person_view
    px, py, pz = player_pos
    
    if key == b'w':
        px += 50 * math.cos(math.radians(player_angle))
        py += 50 * math.sin(math.radians(player_angle))
    if key == b's':
        px -= 50 * math.cos(math.radians(player_angle))
        py -= 50 * math.sin(math.radians(player_angle))
    if key == b'a':
        player_angle += 10
    if key == b'd':
        player_angle -= 10
    
    # Boundary check
    boundary = GROUND_SIZE - player_size - 40
    if px > boundary:
        px = boundary
    if px < -boundary:
        px = -boundary
    if py > boundary:
        py = boundary
    if py < -boundary:
        py = -boundary
    
    player_pos = (px, py, pz)


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos
    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    # if key == GLUT_KEY_UP:

    # # Move camera down (DOWN arrow key)
    # if key == GLUT_KEY_DOWN:

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        x -= 1  # Small angle decrement for smooth movement

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        x += 1  # Small angle increment for smooth movement

    camera_pos = (x, y, z)


def mouseListener(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()

def get_camera_pos():
    px, py, pz = player_pos
    if third_person_view:
        # Third person view: behind, above, and at a height
        offset_x = -third_person_distance * math.cos(math.radians(player_angle))
        offset_y = -third_person_distance * math.sin(math.radians(player_angle))
        offset_z = third_person_distance * 0.5 + 100
        return (px + offset_x, py + offset_y, pz + offset_z)
    else:
        # First person view: in front of player at gun height
        offset_x = 30 * math.cos(math.radians(player_angle)) - 10 * math.sin(math.radians(player_angle))
        offset_y = 30 * math.sin(math.radians(player_angle)) + 10 * math.cos(math.radians(player_angle))
        return (px + offset_x, py + offset_y, pz + 40)

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1280/720, 0.1, 10000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    camera_pos = get_camera_pos()
    px, py, pz = player_pos
    
    if third_person_view:
        look_x = px
        look_y = py
        look_z = pz + 50
    else:
        look_x = px + 100 * math.cos(math.radians(player_angle))
        look_y = py + 100 * math.sin(math.radians(player_angle))
        look_z = pz + player_size/2
    
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
              look_x, look_y, look_z,
              0, 0, 1)


def idle():
    move_cars()
    move_bullets()
    check_collisions()
    check_bullet_car_collisions()
    glutPostRedisplay()


def showScreen():
    global game_over
    
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1280, 720)  # Set viewport size

    setupCamera()  # Configure camera perspective

    # Draw a random points
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # Draw the grid (game floor)
    glBegin(GL_QUADS)
    
    glColor3f(1, 1, 1)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)

    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(0, -GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(GRID_LENGTH, 0, 0)


    glColor3f(0.7, 0.5, 0.95)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, -GRID_LENGTH, 0)

    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glEnd()

    draw_text(10, 770, f"A Random Fixed Position Text")
    draw_text(10, 740, f"See how the position and variable change?: {rand_var}")
    if game_over:
        if game_over_civilian:
            draw_text(10, 710, f"GAME OVER: Civilians have become Hostile!")
        if game_over_car:
            draw_text(10, 710, f"GAME OVER: You were hit by a car!")


    draw_ground()
    draw_walls()

    draw_road()
    
      
    draw_all_cars()
    draw_property_walls()

    draw_all_houses()
    

    draw_player()
    draw_all_bullets()
    draw_crosshair()

    # draw_ground()
    # draw_road()
    # draw_all_cars()        # Draw cars first
    # draw_property_walls()  # Then draw walls on top
    # draw_walls()

    # draw_player()
    # draw_all_bullets()

    # draw_crosshair()
    
    glutSwapBuffers()




def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1280, 720)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"3D OpenGL Intro")

    glEnable(GL_DEPTH_TEST)

    generate_car_positions()

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()