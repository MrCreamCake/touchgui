#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Name: Simen Solberg
# Username: MrCreamCake
# Mail: mrlulul@hotmail.com

import pygame
from settings import *
vector = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.all_sprites
        # Adding the Player to the sprite groups specified in self.groups
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface((16, 16))
        self.image.fill(red)

        # Creates an object with the dimentions of self.image
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height/2)
        self.pos = vector(x, y) * objectSize
        self.velocity = vector(0, 0)
        self.accel = vector(0, 0)

    def update(self):
        # Controlls movement of the player.
        # PlayerAlive is by default False, but will be set to True once the player presses Space.
        if self.game.playerAlive:
            # By adding playerGrav to self.accel y vector it will make the player falling down
            self.accel = vector(0, playerGrav)
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_a] and self.game.playerAlive:
            # By adding a negative value of the playerAccel the player will accelerate to the left
            self.velocity.x = -playerAccel
        if keyPressed[pygame.K_d] and self.game.playerAlive:
            # By adding a positive value of the playerAccel the player will accelerate to the right
            self.velocity.x = playerAccel
        if keyPressed[pygame.K_SPACE]:
            self.velocity.y = -5
            self.game.playerAlive = True

        # Calculates acceleration and velocity to determine speed and direction of the player
        # Updates the self.rect to move the player
        self.accel += self.velocity * playerFriction
        self.velocity += self.accel
        self.pos += self.velocity + 0.5 * self.accel
        self.rect.midbottom = self.pos


class Mapobject(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.object_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((objectSize, objectSize))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = x * objectSize
        self.rect.y = y * objectSize


class Star(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.star_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((objectSize, objectSize))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x * objectSize
        self.rect.y = y * objectSize

