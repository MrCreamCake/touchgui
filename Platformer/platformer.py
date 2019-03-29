#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Name: Simen Solberg
# Username: MrCreamCake
# Mail: mrlulul@hotmail.com

import touchgui
from sprites import *
from settings import *
from os import path
import pygame
import random


class Platformer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        # Loads in background music, sets the volume and plays it in a loop
        touchgui.load_data('sp00ky_music.wav', 'music')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)
        touchgui.set_resolution(width, height)
        touchgui.set_background(colour=blue)
        self.screen = touchgui.screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.mouseOrTabletImages = ['mouse32x50.bmp', 'tablet32x50.bmp']
        self.mT_TActive = False
        self.mT_Image = self.mouseOrTabletImages[1]

        self.muteOrUnmuteImages = ['soundOn32x50.bmp', 'soundOff32x50.bmp']
        self.mute = False
        self.muteOrUnmuteImage = self.muteOrUnmuteImages[0]

        self.playerSpawn = vector(0, 0)
        self.playerAlive = False
        self.playerLives = 3
        self.score = 0

        self.starCount = 0
        self.starSpawn = []

        self.firstStart = True
        self.restart = False
        self.restartButton = None
        self.load_mapdata()

    def load_mapdata(self):
        # Sets what path the file maplayout.txt is going to be located at
        # Once open loops through information which is appended to self.map_data.
        folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(folder, 'maplayout.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        self.playerLives = 3
        self.score = 0
        self.starCount = 0
        # Creates sprite groups which the sprites are placed into.
        self.all_sprites = pygame.sprite.Group()
        self.object_sprites = pygame.sprite.Group()
        self.star_sprite = pygame.sprite.Group()

        # Loops through the data in self.map_data and places sprites according to the
        # Sign it finds in the file
        for row, objects in enumerate(self.map_data):
            for col, object in enumerate(objects):
                if object == '1':
                    Mapobject(self, col, row)
                if object == 'P':
                    self.player = Player(self, col, row)
                    self.playerSpawn = (col, row)
                if object == 'S':
                    self.starSpawn.append((col, row))
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            # Tracks mouse position and if mouse buttons are pressed
            touchgui.mousepos = pygame.mouse.get_pos()
            touchgui.mouseclick = pygame.mouse.get_pressed()
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()

            # If any of the buttons has been clicked these functions will fire and execute commands
            if self.mouseOrTabletButton:
                self.swapMouseTablet()
            if self.muteOrUnmuteButton:
                self.swapMuteUnmute()
            if self.moveLeftButton and self.playerAlive:
                # Calulates players velocity, acceleration, which then is used to
                # update the position of the player
                self.player.velocity.x = -playerAccel
                self.player.accel += self.player.velocity * playerFriction
                self.player.velocity += self.player.accel
                self.player.pos += self.player.velocity + 0.5 * self.player.accel
                self.player.rect.midbottom = self.player.pos
            if self.moveRightButton and self.playerAlive:
                # Calulates players velocity, acceleration, which then is used to
                # update the position of the player
                self.player.velocity.x = playerAccel
                self.player.accel += self.player.velocity * playerFriction
                self.player.velocity += self.player.accel
                self.player.pos += self.player.velocity + 0.5 * self.player.accel
                self.player.rect.midbottom = self.player.pos
            if self.jumpButton:
                # Calulates players velocity, acceleration, which then is used to
                # update the position of the player
                self.player.velocity.y = -15
                self.playerAlive = True
                self.player.accel += self.player.velocity * playerFriction
                self.player.velocity += self.player.accel
                self.player.pos += self.player.velocity + 0.5 * self.player.accel
                self.player.rect.midbottom = self.player.pos


    def draw(self):
        # Draws objects onto the screen
        self.screen.fill(blue)
        self.all_sprites.draw(self.screen)
        self.scoreDisplay = touchgui.text(str(self.score), touchgui.unitX(0.5), touchgui.unitY(0.0417), 32, red)
        self.livesDisplay = touchgui.text(str(self.playerLives), touchgui.unitX(0.2), touchgui.unitY(0.0417), 32, red)
        self.mouseOrTabletButton = touchgui.image_Button(touchgui.unitX(0.9), 32, touchgui.unitY(0.0105), 50,
                                                        self.mT_Image, action='swap')
        self.muteOrUnmuteButton = touchgui.image_Button(touchgui.unitX(0.8), 32, touchgui.unitY(0.0105), 50,
                                                        self.muteOrUnmuteImage, action='muteOrUnmute')
        self.screen.blit(touchgui.load_data('heart.png', 'image'), (touchgui.unitX(0.15), touchgui.unitY(0.0208)))

        if self.mT_TActive:
            # If the touchscreen mode is active it will display the buttons underneath
            self.moveLeftButton = touchgui.image_Button(touchgui.unitX(0.1), 100, touchgui.unitY(0.9), 64,
                                                        'arrowLeft100x64.bmp', action='moveleft')
            self.moveRightButton = touchgui.image_Button(touchgui.unitX(0.25), 100, touchgui.unitY(0.9), 64,
                                                        'arrowRight100x64.bmp', action='moveright')
            self.jumpButton = touchgui.image_Button(touchgui.unitX(0.75), 64, touchgui.unitY(0.9), 64,
                                                    'arrowUp64x64.bmp', action='jump')

        else:
            self.moveLeftButton = None
            self.moveRightButton = None
            self.jumpButton = None

        if self.starCount == 0:
            # Spawns new stars once star count hits 0
            self.spawnStars()

        if self.playerLives == 0:
            # When the player reaches 0 lives the player is killed
            self.player.kill()
            touchgui.text('GAME OVER', touchgui.unitX(0.5), touchgui.unitY(0.45), 50, red)
            touchgui.text(str(self.score), touchgui.unitX(0.5), touchgui.unitY(0.55), 50, red)
            if self.mT_TActive:
                self.restartButton = touchgui.text_button('Restart', touchgui.unitX(0.5), touchgui.unitY(0.9), 120, 64, red,
                                                     red,
                                                     32, action='restart')
                touchgui.text('Press Restart To Play Again', touchgui.unitX(0.5), touchgui.unitY(0.70), 30, red)
                if self.restartButton:
                    # If the restart button is pressed the playerAlive value will be set to False
                    # self.restart to True
                    self.playerAlive = False
                    self.restart = True
                if self.restart:
                    # Sets self.restart to False
                    # Respawn the player at player spawn, and starts a new game.
                    self.restart = False
                    self.player = Player(self, self.playerSpawn[0], self.playerSpawn[1])
                    self.starSpawn = []
                    self.new()
            else:
                touchgui.text('Press Enter To Play Again', touchgui.unitX(0.5), touchgui.unitY(0.70), 30, red)
                if self.restart:
                    # Sets self.restart to False
                    # Respawn the player at player spawn, and starts a new game.
                    self.restart = False
                    self.player = Player(self, self.playerSpawn[0], self.playerSpawn[1])
                    self.starSpawn = []
                    self.new()

        pygame.display.flip()

    def events(self):
        # Checks for any events that happens
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If the X in the corner is pressed it will close the program
                self.running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Will close the program if Escape is pressed
                    self.running = False
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    self.restart = True

    def update(self):
        self.all_sprites.update()

        if pygame.sprite.spritecollide(self.player, self.object_sprites, False) and self.playerLives != 0:
            # Checks for collisions between the player and sprites in the self.object_sprites group
            # Teleports the player back to the spawn point and sets the speed to 0
            self.playerLives -= 1
            self.playerAlive = False
            self.player.pos = vector(self.playerSpawn[0], self.playerSpawn[1]) * objectSize
            self.player.velocity = vector(0, 0)
            self.player.accel = vector(0, 0)

        if pygame.sprite.spritecollide(self.player, self.star_sprite, True):
            # Checks for collisions between the player and sprites in the self.star_sprite group
            # Removes the star sprite if collide
            self.score += 1
            self.starCount -= 1

    def swapMouseTablet(self):
        if self.mT_TActive:
            self.mT_TActive = False
            self.mT_Image = self.mouseOrTabletImages[1]
            # Makes the cursor appear as it usually is
            pygame.mouse.set_cursor((16, 16), (0, 0),
                                    (0, 0, 64, 0, 96, 0, 112, 0, 120, 0, 124, 0, 126, 0, 127, 0, 127, 128, 124, 0, 108,
                                     0, 70, 0, 6, 0, 3, 0, 3, 0, 0, 0),
                                    (192, 0, 224, 0, 240, 0, 248, 0, 252, 0, 254, 0, 255, 0, 255, 128, 255, 192, 255,
                                     224, 254, 0, 239, 0, 207, 0, 135, 128, 7, 128, 3, 0))
        else:
            self.mT_TActive = True
            # Makes the cursur invisible
            pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
            self.mT_Image = self.mouseOrTabletImages[0]

    def swapMuteUnmute(self):
        if self.mute:
            # Unpauses the background music
            pygame.mixer.music.unpause()
            self.muteOrUnmuteImage = self.muteOrUnmuteImages[0]
            self.mute = False
        else:
            # Pauses the background music
            pygame.mixer.music.pause()
            self.muteOrUnmuteImage = self.muteOrUnmuteImages[1]
            self.mute = True

    def spawnStars(self):
        for i in range(0, 5):
            # Creates 5 stars with random spawn location
            spawnCords = random.choice(self.starSpawn)
            self.starSpawn.remove(spawnCords)
            Star(self, spawnCords[0], spawnCords[1])
            self.starCount += 1


p = Platformer()
while p.running:
    p.new()
