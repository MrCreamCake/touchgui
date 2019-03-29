#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Name: Simen Solberg
# Username: MrCreamCake
# Mail: mrlulul@hotmail.com

import pygame
from pygame.locals import *

pygame.init()

# Variables which tracks the mouse cursors current position and if any mouse button is pressed.
global mousepos
global mouseclick
mousepos = pygame.mouse.get_pos()
mouseclick = pygame.mouse.get_pressed()
buttonClick = False

# Makes global variables of the X and Y so that it can be used by other functions in this file.
def set_resolution(x, y):
    global screen_width, screen_height
    screen_width, screen_height = x, y

# Creates a game screen with the resolution of global variables screen_width and screen_height.
# It also blit a chosen image onto the screen, or fills it with a set colour
def set_background(image=None, colour=None):
    global screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    if image:
        screen.blit(load_data(image, 'image'), (0, 0))
    else:
        screen.fill(colour)

# Loads in files.
# Accepts both images and music
# If image is chosen it will return it which can be used in a variable
def load_data(file, type):
    if type == 'image':
        return pygame.image.load(file).convert_alpha()
    if type == 'music':
        pygame.mixer.music.load(open(file, "rb"))


def unitX(v):
    return int(v * screen_width)


def unitY(v):
    return int(v * screen_height)

# Take input text and coordinates and displays it on the screen.
def text(txt, x, y, size, colour, ttf='freesansbold.ttf'):
    screen_text = pygame.font.Font(ttf, size)
    textsurf = screen_text.render(txt, True, colour)
    textrect = textsurf.get_rect()
    textrect.center = (x, y)
    screen.blit(textsurf, textrect)


def text_button(txt, x, y, wt, ht, text_colour, button_colour, size=10, action=None, ttf='freesansbold.ttf'):
    global buttonClick
    # Does a check whether the current mouse position is inside the text button
    if x + wt > mousepos[0] > x and y + ht > mousepos[1] > y:
        pygame.draw.rect(screen, button_colour, (x, y, wt, ht), 1)
        # Does a check to see if the left mouse button is not pressed
        # and that the button hasn't already been clicked.
        if mouseclick[0] == 1 and not buttonClick:
            # Marks the button as clicked
            buttonClick = True
            # If there is a action present it will be returned back to the caller file
            if action:
                return action
        # Marks the button as not clicked if the left mouse button pressed
        if mouseclick[0] == 0:
            buttonClick = False
    else:
        pygame.draw.rect(screen, text_colour, (x, y, wt, ht), 1)

    button_text = pygame.font.Font(ttf, size)
    textsurf = button_text.render(txt, True, text_colour)
    textrect = textsurf.get_rect()
    textrect.center = (((wt / 2) + x), ((ht / 2) + y))
    screen.blit(textsurf, textrect)


def image_Button(x, wt, y, ht, imageButton, action=None):
    global buttonClick
    # Does a check whether the current mouse position is inside the button
    if x + wt > mousepos[0] > x and y + ht > mousepos[1] > y:
        # Does a check to see if the left mouse button is not pressed
        # and that the button hasn't already been clicked.
        if mouseclick[0] == 1 and not buttonClick:
            # Marks the button as clicked
            buttonClick = True
            # If there is a action present it will be returned back to the caller file
            if action:
                return action
        # Marks the button as not clicked if the left mouse button pressed
        if mouseclick[0] == 0:
            buttonClick = False
    # Loads in the image and displays it on the screen
    screen.blit(load_data(imageButton, 'image'), (x, y))

# Draws a grid of hallow boxes which has the size of
# (x2-x1)x(y2-y1) where each of the boxes is width x height
def draw_grid(x1, x2, width, y1, y2, height, colour):
    for x in range(x1, x2, width):
        for y in range(y1, y2, height):
            rect = pygame.Rect(x, y, width, height)
            pygame.draw.rect(screen, colour, rect, 1)

