import math
import sys
import Bodies
import pygame
import os
import random

#Gravity simulation
def apply_gravity(mass1: float, mass2: float, distance: float) -> float:
    """
    Returns the force of gravity between two masses.
    
    Args:
        mass1 (float): The first mass.
        mass2 (float): The second mass.
        distance (float): The distance between the two masses.
    """
    if not isinstance(mass1, float) or not isinstance(mass2, float) or not isinstance(distance, float):
        print(mass1, mass2, distance)
        raise ValueError("Invalid input")
    
    if mass1 <= 0 or mass2 <= 0 or distance < 0:
        raise ValueError("Invalid input")
    
    return (6.674 * (10 ** -11)) * ((mass1 * mass2) / (distance ** 2)) #Calculate the force of gravity between two masses

#New gravity simulation
#Calculate the total gravity on one with direction body accounting for all bodies 
def calculate_gravity_with_direction(body: Bodies.body, bodys: list[Bodies.body]) -> list[float]:
    """
    Returns the acceleration of a body after a given change in velocity.
    
    Args:
        body (Bodies.body): The body to calculate the acceleration of.
        bodys (list[Bodies.body]): The list of bodies to calculate the acceleration for.
        simSpeed (float): The simulation speed.
    """
    if not isinstance(body, Bodies.body) or not isinstance(bodys, list):
        raise ValueError("Invalid input")
    
    
    acceleration = [0, 0, 0]
    accelerationTemp = [0, 0, 0]
    for i in range(len(bodys)):
        if bodys[i] != body:
            gravity = apply_gravity(body.mas, bodys[i].mas, calculate_distance(body.pos, bodys[i].pos)) 
            direction = calculate_direction(body, bodys[i])
            accelerationTemp = calculate_acceleration(body, gravity, direction)

        for j in range(len(acceleration)):
            acceleration[j] += accelerationTemp[j]

    return acceleration #Return the acceleration of a body

#Calculate the distance between two points
def calculate_distance(point1: list[float], point2: list[float]) -> float:
    """
    Returns the distance between two points.
    
    Args:
        point1 (list[float]): The first point.
        point2 (list[float]): The second point.
    """
    if not isinstance(point1, list) or not isinstance(point2, list):
        raise ValueError("Invalid input")
    
    if len(point1) != len(point2):
        raise ValueError("Invalid input")
    
    distance = 0
    for i in range(len(point1)): #For each dimension
        distance += (point1[i] - point2[i]) ** 2 #Calculate the distance between two points
    return math.sqrt(distance)  #Return the distance between two points

#Calculate the new position of a body
def calculate_new_position(body: Bodies.body, time: float) -> list[float]:
    """
    Returns the new position of a body after a given time.
    
    Args:
        body (Bodies.body): The body to calculate the new position of.
        time (float): The time to calculate the new position for.
    """
    if not isinstance(body, Bodies.body) or not isinstance(time, float):
        raise ValueError("Invalid input")
    
    if time < 0:
        raise ValueError("Invalid input")
    
    new_position = []
    for i in range(len(body.pos)): #For each dimension
        new_position.append(body.pos[i] + (body.vel[i] * time)) #Calculate the new position of a body
    return new_position #Return the new position of a body

#Calculate the new velocity of a body
def calculate_new_velocity(body: Bodies.body, time: float, acceleration: list[float]) -> list[float]:
    """
    Returns the new velocity of a body after a given time.
    
    Args:
        body (Bodies.body): The body to calculate the new velocity of.
        time (float): The time to calculate the new velocity for.
    """
    if not isinstance(body, Bodies.body) or not isinstance(time, float) or not isinstance(acceleration, list):
        raise ValueError("Invalid input")
    
    if time < 0:
        raise ValueError("Invalid input")
    
    new_velocity = []
    #Calculate the new velocity of a body
    for i in range(len(body.vel)):
        new_velocity.append(body.vel[i] + (acceleration[i] * time)) #Calculate the new velocity of a body
    return new_velocity #Return the new velocity of a body

#Caluclate the acceleration of a body with direction
def calculate_acceleration(body: Bodies.body, change: float, direction: list[float]) -> list[float]:
    """
    Returns the acceleration of a body after a given change in velocity.
    
    Args:
        body (Bodies.body): The body to calculate the acceleration of.
        change (float): The change in velocity to calculate the acceleration for.
        direction (list[float]): The direction of the change in velocity.
    """
    if not isinstance(body, Bodies.body) or not isinstance(change, float) or not isinstance(direction, list):
        raise ValueError("Invalid input")
    
    if change < 0:
        raise ValueError("Invalid input")
    
    acceleration = []
    for i in range(len(direction)):
        acceleration.append((direction[i] * change) / body.mas) #Calculate the acceleration of a body
    return acceleration #Return the acceleration of a body

#Calculate the direction of a change in velocity
def calculate_direction(body1: Bodies.body, body2: Bodies.body) -> list[float]:
    """
    Returns the direction of a change in velocity between two bodies.
    
    Args:
        body1 (Bodies.body): The first body.
        body2 (Bodies.body): The second body.
    """
    if not isinstance(body1, Bodies.body) or not isinstance(body2, Bodies.body):
        raise ValueError("Invalid input")
    
    direction = []
    for i in range(len(body1.pos)):
        direction.append(body2.pos[i] - body1.pos[i]) #Calculate the direction of a change in velocity
    NormalizedDirection = []
    #Make it so that the direction has a magnitude of 1
    for i in range(len(direction)):
        NormalizedDirection.append(direction[i] / calculate_distance(body1.pos, body2.pos)) #Calculate the direction of a change in velocity
    return NormalizedDirection #Return the direction of a change in velocity

#Draw a body
def draw_body(screen, body):
    # Scale the 3D coordinates for rendering
    scaled_x = int((body.pos[0] / 400000) + WIDTH / 2)
    scaled_y = int((body.pos[1] / 400000) + HEIGHT / 2)
    scaled_z = int((body.pos[2] / 400000) + WIDTH / 2)

    # Calculate the size of the circle based on the z-axis
    circle_radius = int(scaled_z / 30)  # Adjust the divisor to get the desired effect
    circle_radius = circle_radius + (body.radius / 4) -20
    # Draw a sphere with the calculated radius
    pygame.draw.circle(screen, body.color, (scaled_x, scaled_y), circle_radius)
    pygame.draw.circle(screen, (0, 0, 0), (scaled_x, scaled_y), circle_radius, 1)  # Outline


def draw_input_box():
    global active
    global text
    txt_surface = font.render(text, True, WHITE)
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(screen, color, input_box, 2)

#Check if bodies are colliding
def check_collision(body1: Bodies.body, body2: Bodies.body) -> bool:
    """
    Returns whether two bodies are colliding.
    
    Args:
        body1 (Bodies.body): The first body.
        body2 (Bodies.body): The second body.
    """
    if not isinstance(body1, Bodies.body) or not isinstance(body2, Bodies.body):
        raise ValueError("Invalid input")
    
    if calculate_distance(body1.pos, body2.pos) <= ((body1.radius * (10 ** 5)) + (body2.radius * (10 ** 5))):
        return True #Return whether two bodies are colliding
    else:
        return False #Return whether two bodies are colliding
    

#Calculate the new velocity of a body accounting for the mass of the other body when they collide
def calculate_new_velocity_collision(body1: Bodies.body, body2: Bodies.body) -> list[float]:
    """
    Returns the new velocity of a body after they collide.
    
    Args:
        body (Bodies.body): The body to calculate the new velocity of.
    """
    if not isinstance(body1, Bodies.body) or not isinstance(body2, Bodies.body):
        raise ValueError("Invalid input")
    new_velocity = []
    for i in range(len(body1.vel)):
        new_velocity.append((body1.mas * body1.vel[i] + body2.mas * body2.vel[i]) / (body1.mas + body2.mas))
    return new_velocity #Return the new velocity of a body
    


os.environ["SDL_VIDEO_WINDOW_POS"] = "1921,-800" #Make the window open where needed
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1920, 1920
BODY_RADIUS = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Input box
input_box = pygame.Rect(100, 100, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = 'Simulation Speed'
font = pygame.font.Font(None, 32)

button_color = (50, 200, 50)  # RGB color
button_position = (500, 100)  # x, y
button_size = (250, 50)  # width, height
button_text = 'Spawn Random Body'

text_surface = font.render(button_text, True, (255, 255, 255))


def main():

    global active
    global text


    body1 = Bodies.body("Earth", 5.972 * (10 ** 24), [0, 0, 0], [0, -3.5, -12.4], RED, 400) 
    body2 = Bodies.body("Moon", 7.348 * (10 ** 22), [3.844 * (10 ** 8), 0, 0], [0, 300, 1000], BLUE, 100) 
    body3 = Bodies.body("MoonMoon", 7.348 * (10 ** 20), [-3.4 * (10 ** 8), 0, 0], [0, -800, 500], BLUE, 50)
    body4 = Bodies.body("Sun", 1.989 * (10 ** 30), [0, 2 * (10 ** 10), 0], [0, 0, 0], WHITE, 1000)

    bodys = [body1, body2, body3]
    
    for body in bodys:
        print(body.name + " Mas = " + str(body.mas) + " Pos = " + str(body.pos) + " Vel = " + str(body.vel))



    # Set the simulation speed
    simSpeed = 100.0
    
    i = 0
    while True:
        i += 1
        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the bodies
        
        for body in bodys:
            draw_body(screen, body)

        draw_input_box()
        pygame.draw.rect(screen, button_color, (*button_position, *button_size))
        # Draw the text onto the button
        screen.blit(text_surface, (button_position[0] + 10, button_position[1] + 10))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                    text = ''
                elif pygame.Rect(button_position, button_size).collidepoint(event.pos):
                    """spawn random body"""
                    mas = float(random.randint(1, 10) * (10 ** 24))
                    pos = [float(random.randint(-500000000, 500000000)), float(random.randint(-500000000, 500000000)), float(random.randint(-500000000, 500000000))]
                    vel = [float(random.randint(-1000, 1000)), float(random.randint(-1000, 1000)), float(random.randint(-1000, 1000))]
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    radius = (mas / 10 ** 24) * random.randint(1, 10)
                    bodys.append(Bodies.body("Body" + str(i), mas, pos, vel, color, radius))
                    print("Body" + str(i) + " Mas = " + str(mas) + " Pos = " + str(pos) + " Vel = " + str(vel) + " Color = " + str(color) + " Radius = " + str(radius))
                    i += 1
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        try:
                            simSpeed = float(text)
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode



        # Update the display
        pygame.display.flip()
    
        
        #Calculate the new position and velocity of the bodies
        for body in bodys:
             acceleration = calculate_gravity_with_direction(body, bodys)
             body.vel = calculate_new_velocity(body, simSpeed, acceleration)
             body.pos = calculate_new_position(body, simSpeed)
        
        for body in bodys:
            for body2 in bodys:
                if body != body2:
                    if check_collision(body, body2):
                        print("Collision")

                        if body.mas >= body2.mas:
                            body.mas += body2.mas                            
                            body.vel = calculate_new_velocity_collision(body, body2)
                            body.radius += body2.radius
                            bodys.remove(body2)
                            print("Body was removed")
                        else:
                            body2.mas =+ body.mas
                            body2.vel = calculate_new_velocity_collision(body2, body)
                            body2.radius += body.radius
                            bodys.remove(body)
                            print("Body2 was removed")
                        break

        
        """
        gravity = apply_gravity(body1.mas, body2.mas, calculate_distance(body1.pos, body2.pos))

        #Calculate the new position and velocity of body1
        direction = calculate_direction(body1, body2)
        acceleration = calculate_acceleration(body1, gravity, direction)
        body1.vel = calculate_new_velocity(body1, simSpeed, acceleration)
        body1.pos = calculate_new_position(body1, simSpeed)

        #Calculate the new position and velocity of body2
        direction = calculate_direction(body2, body1)
        acceleration = calculate_acceleration(body2, gravity, direction)
        body2.vel = calculate_new_velocity(body2, simSpeed, acceleration)
        body2.pos = calculate_new_position(body2, simSpeed)
        """
  

    




if __name__ == "__main__":
    main()