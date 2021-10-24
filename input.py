# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 20:30:30 2021

@author: Dennis Miklos
"""
import pygame
import socket

pygame.init()

# INITIALIZE tcp
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT))

# Loop until the user clicks the close button.
done = False

# Initialize the joysticks.
pygame.joystick.init()

# Loop Input
while not done:
    
    for event in pygame.event.get(): # User did something.
        if event.type == pygame.QUIT: # If user clicked close.
            done = True # Flag that we are done so we exit this loop.

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    y_axis_fb = round(joystick.get_axis(1),1)
    x_axis_lr = round(joystick.get_axis(2),1)
    
    datastr = str(x_axis_lr) + ',' + str(y_axis_fb)
    
    s.sendall(bytes(datastr, 'utf-8'))
    pygame.time.delay(100)
    
s.close()