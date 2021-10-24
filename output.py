# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 20:31:29 2021

@author: Dennis Miklos
"""

import socket
import numpy as np
import pygame
import math

# Create Movement String
def decodeMovement(movement):
    dim = np.shape(movement)
    wheel = ''
    for i in range(dim[0]):
        for j in range(dim[1]):
            if movement[i][j] < 0:
                wheel = wheel + '[' + 'r' + str(movement[i][j]) + ']'
            else:
                wheel = wheel + '['+ 'f' + str(movement[i][j]) + ']'
    return wheel

# Create Rover Plot
pygame.init()
win = pygame.display.set_mode((500,500))
pygame.display.set_caption("Rover Movements")
clock = pygame.time.Clock()
rover = pygame.Surface((25,25))
rover.set_colorkey((0,0,0))
rover.fill((0,255,0))
img = rover.copy()
img.set_colorkey((0,0,0))
rect = img.get_rect()
rect.center = (250,250)
rot_ang = 0

# TCP Setip
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((TCP_IP,TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address:', addr)

# While Loop
while True:
    # Recieve Data
    data = conn.recv(BUFFER_SIZE)
    # Decode Recieved Data
    recv_data = data.decode('utf-8')
    try:
        axis_val = np.array(recv_data.split(','),dtype=np.float64)
    except ValueError:
        continue
    
    # Interpolate Joystick Data to PWM levels
    if axis_val[1] < 0 or axis_val[1] > 0:
        movement = np.interp(axis_val[1],[-1,1],[255,-255]) * np.ones((2,2))
    elif axis_val[0] < 0 or axis_val[0] > 0:
        xL_movement = np.interp(axis_val[0],[-1,1],[-255,255]) * np.ones((2,1))
        xR_movement = np.interp(axis_val[0],[-1,1],[255,-255]) * np.ones((2,1))
        movement = np.concatenate((xL_movement,xR_movement),axis = 1)
    else:
        movement = np.zeros((2,2))

    if not data: break
    # Print Rover Movements to Console
    print('\r'+decodeMovement(movement))
    
    # Plot Rover Movements to Visualize
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            break
            
    oldCenter = rect.center
    win.fill((0,0,0))
    AR = np.sum(movement, axis=0)
    rot_ang = (rot_ang + (AR[1] - AR[0])/255) % 360
    
    xvel =round(((AR[1] + AR[0])/255)*math.sin(rot_ang*math.pi/180),2)
    yvel =round(((AR[1] + AR[0])/255)*math.cos(rot_ang*math.pi/180),2)
    
    # Change Rover Color Based on Movement
    # The Positive direction is downwards
    # Red - Backwards
    # Yellow - Turn Left
    # Magenta - Turn Right
    # Green - Forward
    if (AR[1] + AR[0]) > 0:
        rover.fill((0,255,0))
    elif (AR[1] + AR[0] < 0):
        rover.fill((255,0,0))
    elif (AR[1] - AR[0]) > 0:
        rover.fill((255,255,0))
    elif (AR[1] - AR[0]) < 0:
        rover.fill((255,0,255))
    else:
        rover.fill((255,255,255))
        
    new_img = pygame.transform.rotate(rover,rot_ang)
    xvel = oldCenter[0] + round(xvel,0)
    yvel = oldCenter[1] + round(yvel,0)
    
    rect = new_img.get_rect()
    rect.center = (xvel, yvel)
    win.blit(new_img,rect)
    clock.tick(60)
    pygame.display.update()
    
conn.close