import math
import sys
import Bodies
import pygame


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
        raise ValueError("Invalid input")
    
    if mass1 <= 0 or mass2 <= 0 or distance < 0:
        raise ValueError("Invalid input")
    
    return (6.674 * (10 ** -11)) * ((mass1 * mass2) / (distance ** 2))

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
    for i in range(len(point1)):
        distance += (point1[i] - point2[i]) ** 2
    return math.sqrt(distance)

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
    for i in range(len(body.pos)):
        new_position.append(body.pos[i] + (body.vel[i] * time))
    return new_position

#Calculate the new velocity of a body
def calculate_new_velocity(body: Bodies.body, time: float, acceleration: list[float]) -> list[float]:
    """
    Returns the new velocity of a body after a given time.
    
    Args:
        body (Bodies.body): The body to calculate the new velocity of.
        time (float): The time to calculate the new velocity for.
    """
    #print(type(body), isinstance(body, Bodies.body))
    #print(type(time), isinstance(time, float))
    #print(type(acceleration), isinstance(acceleration, list))
    if not isinstance(body, Bodies.body) or not isinstance(time, float) or not isinstance(acceleration, list):
        raise ValueError("Invalid input")
    
    if time < 0:
        raise ValueError("Invalid input")
    
    new_velocity = []
    new_velocity.append(body.vel[0] + (acceleration[0] * time))
    new_velocity.append(body.vel[1] + (acceleration[1] * time))
    new_velocity.append(body.vel[2] + (acceleration[2] * time))
    return new_velocity

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
    acceleration.append((direction[0] * change) / body.mas)
    acceleration.append((direction[1] * change) / body.mas)
    acceleration.append((direction[2] * change) / body.mas)
    return acceleration
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
    direction.append(body2.pos[0] - body1.pos[0])
    direction.append(body2.pos[1] - body1.pos[1])
    direction.append(body2.pos[2] - body1.pos[2])
    NormalizedDirection = []
    #Make it so that the direction has a magnitude of 1
    for i in range(len(direction)):
        NormalizedDirection.append(direction[i] / calculate_distance(body1.pos, body2.pos))
    return NormalizedDirection

def draw_body(screen, body, color):
    pygame.draw.circle(screen, color, (int((body.pos[0] / 400000) + 960), int((body.pos[1] / 400000) + 960)), BODY_RADIUS)

pygame.init()

WIDTH, HEIGHT = 1920, 1920
BODY_RADIUS = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

def main():

    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    body1 = Bodies.body("Earth", 5.972 * (10 ** 24), [0, 0, 0], [0, -12.3, 0])
    body2 = Bodies.body("Moon", 7.348 * (10 ** 22), [3.844 * (10 ** 8), 0, 0], [0, 1000, 0])
    
    print(body1.name + " Mas = " + str(body1.mas) + " Pos = " + str(body1.pos) + " Vel = " + str(body1.vel))
    print(body2.name + " Mas = " + str(body2.mas) + " Pos = " + str(body2.pos) + " Vel = " + str(body2.vel))
    simSpeed = 1000.0
    
    i = 0
    while True:
        i += 1
        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the bodies
        draw_body(screen, body1, RED)
        draw_body(screen, body2, BLUE)

        # Update the display
        pygame.display.flip()

        # Delay to control the speed of the simulation
        #pygame.time.delay(10)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
        gravity = apply_gravity(body1.mas, body2.mas, calculate_distance(body1.pos, body2.pos))

        direction = calculate_direction(body1, body2)
        acceleration = calculate_acceleration(body1, gravity, direction)

        body1.vel = calculate_new_velocity(body1, simSpeed, acceleration)
        body1.pos = calculate_new_position(body1, simSpeed)

        direction = calculate_direction(body2, body1)
        acceleration = calculate_acceleration(body2, gravity, direction)
        body2.vel = calculate_new_velocity(body2, simSpeed, acceleration)
        body2.pos = calculate_new_position(body2, simSpeed)
        """        
        print("Iteration " + str(i))
        print(body1.name + " Pos = " + str(body1.pos) + " Vel = " + str(body1.vel))
        print(body2.name + " Pos = " + str(body2.pos) + " Vel = " + str(body2.vel))
        print("")
        """
    
    



    

    




if __name__ == "__main__":
    main()