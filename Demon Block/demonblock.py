#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Name: Simen Solberg
# Username: MrCreamCake
# Mail: mrlulul@hotmail.com
import pygame
from settings import *
import random
import touchgui


class Block(pygame.sprite.Sprite):
    def __init__(self, db, x, y):
        self.db = db
        self.groups = self.db.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.blockValues = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4]
        self.currentBlockValue = random.choice(self.blockValues)
        self.images = ['block1.bmp', 'block2.bmp', 'block3.bmp', 'block4.bmp']
        self.image = pygame.image.load_basic(self.images[self.currentBlockValue - 1])
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y


class DemonBlock:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        touchgui.load_data('sp00ky_music.wav',
                           'music')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)
        touchgui.set_resolution(width, height)
        touchgui.set_background(image='bg.bmp')
        pygame.display.set_caption('DEMON BLOCK')
        self.screen = touchgui.screen

        self.playBoardWidth = 522
        self.playBoardHeight = 550
        self.blockWidth = 87
        self.blockHeight = 55

        self.mouseOrTabletImages = ['mouse32x50.bmp', 'tablet32x50.bmp']
        self.mT_TActive = False
        self.mT_Image = self.mouseOrTabletImages[1]

        self.muteOrUnmuteImages = ['soundOn32x50.bmp', 'soundOff32x50.bmp']
        self.mute = False
        self.muteOrUnmuteImage = self.muteOrUnmuteImages[0]

        # Represents the play board tilted to the left
        self.play_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.row_value = {0: 9, 1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1, 9: 1}

        self.currency = 1000
        self.availableBets = [2, 5, 10, 20]
        self.betIndex = 0
        self.currentBet = self.availableBets[0]
        self.winnings = 0

        self.running = True

    def setup(self):
        # Creates a list which cointains the cords of each square
        self.board_cords = [[0 for row in range(128, 678, 55)] for col in range(256, 768, 87)]
        for index1, x in enumerate(range(256, 768, 87)):
            for index2, y in enumerate(range(128, 678, 55)):
                self.board_cords[index1][index2] = (x, y)

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.draw()
        self.running_loop()

    def draw(self):
        touchgui.set_background(image='bg.bmp')
        touchgui.text('DEMON BLOCK', touchgui.unitX(0.5), touchgui.unitY(0.1), 75, red, ttf='ANVIL.ttf')
        touchgui.draw_grid(256, 768, 87, 128, 678, 55, red)

        touchgui.text('x2', self.board_cords[5][7][0] + 43, self.board_cords[5][7][1] + 27.5, 25, red)
        touchgui.text('x3', self.board_cords[5][6][0] + 43, self.board_cords[5][6][1] + 27.5, 25, red)
        touchgui.text('x4', self.board_cords[5][5][0] + 43, self.board_cords[5][5][1] + 27.5, 25, red)
        touchgui.text('x5', self.board_cords[5][4][0] + 43, self.board_cords[5][4][1] + 27.5, 25, red)
        touchgui.text('x6', self.board_cords[5][3][0] + 43, self.board_cords[5][3][1] + 27.5, 25, red)
        touchgui.text('x7', self.board_cords[5][2][0] + 43, self.board_cords[5][2][1] + 27.5, 25, red)
        touchgui.text('x8', self.board_cords[5][1][0] + 43, self.board_cords[5][1][1] + 27.5, 25, red)
        touchgui.text('x9', self.board_cords[5][0][0] + 43, self.board_cords[5][0][1] + 27.5, 25, red)

        self.all_sprites.draw(self.screen)

        self.play_button = touchgui.text_button('PLAY', 850, 350, 100, 60, red, black, 25, action='play')
        self.balanceText = touchgui.text('BALANCE', 295, 698, 20, red)
        self.currencyText = touchgui.text(str(self.currency), 295, 718, 20, red)
        self.betText = touchgui.text('BET', 512, 698, 20, red)
        self.currentBetText = touchgui.text(str(self.currentBet), 512, 718, 20, red)
        self.betMinusButton = touchgui.text_button('-', 450, 703, 25, 25, red, black, 20, action='betminus')
        self.betPlusButton = touchgui.text_button('+', 550, 703, 25, 25, red, black, 20, action='betplus')
        self.winningsText = touchgui.text('WINNINGS', 729, 698, 20, red)
        self.currentWinnings = touchgui.text(str(self.winnings), 729, 718, 20, red)
        self.mouseOrTabletButton = touchgui.image_Button(touchgui.unitX(0.9), 32, touchgui.unitY(0.0105), 50,
                                                        self.mT_Image, action='swap')
        self.muteOrUnmuteButton = touchgui.image_Button(touchgui.unitX(0.8), 32, touchgui.unitY(0.0105), 50,
                                                        self.muteOrUnmuteImage, action='muteOrUnmute')
        pygame.display.update()

    def running_loop(self):
        self.running = True
        self.play_run = False
        while self.running:
            touchgui.mousepos = pygame.mouse.get_pos()
            touchgui.mouseclick = pygame.mouse.get_pressed()
            self.draw()
            self.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
            if self.play_button:
                self.play_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                self.play()
            if self.betMinusButton:
                self.betMinus()
            if self.betPlusButton:
                self.betPlus()
            if self.mouseOrTabletButton:
                self.swapMouseTablet()
            if self.muteOrUnmuteButton:
                self.swapMuteUnmute()

    def play(self):
        self.all_sprites.empty()
        self.winnings = 0
        self.currency -= self.currentBet
        self.draw_block(5)
        self.check_BonusBlocks()
        self.check_Winnings(9)
        self.currency += self.winnings

    def betMinus(self):
        try:
            self.currentBet = self.availableBets[self.betIndex-1]
            self.betIndex -= 1
        except IndexError:
            pass

    def betPlus(self):
        try:
            self.currentBet = self.availableBets[self.betIndex+1]
            self.betIndex += 1
        except IndexError:
            pass

    def update(self):
        self.all_sprites.update()

    def draw_block(self, block_qty):
        for block in range(block_qty):
            # Draws blocks with a random column spawn
            column = random.randrange(0, 5)
            xSpawn = self.board_cords[column][0][0]
            # Checks if a block is at the location
            if self.play_board[column][0] == 0:
                block = Block(self, xSpawn, 128)
                currenty = 0
                i = 1
                while block.y < 623:
                    # Moves the block down while checking if there is no other blocks in the square
                    if self.play_board[column][i] == 0:
                        block.y += 55
                        currenty += 1
                        i += 1
                    else:
                        self.play_board[column][currenty] = block.currentBlockValue
                        break
                self.play_board[column][currenty] = block.currentBlockValue

    def check_Winnings(self, row):
        tileWithBlock = 0
        currentWinnings = 0
        for tile in range(0, 5):
            # Checks every square at a row to see if a block is present
            # If five blocks is present at one row five more will be created
            # It then runs again for the row over
            currentSquare = self.play_board[tile][row]
            if currentSquare > 0:
                tileWithBlock += 1
                currentWinnings += (currentSquare * self.currentBet) * self.row_value[row]
            if tileWithBlock == 5:
                self.winnings += currentWinnings
                self.draw_block(5)
                try:
                    self.check_Winnings((row-1))
                except KeyError:
                    break

    def check_BonusBlocks(self):
        # Spawns extra blocks if there is a block in these bonus squares
        if self.play_board[2][8] > 0:
            self.draw_block(2)

        elif self.play_board[0][7] > 0:
            self.draw_block(1)

        elif self.play_board[4][7] > 0:
            self.draw_block(1)

        elif self.play_board[2][6] > 0:
            self.draw_block(1)

        elif self.play_board[2][4] > 0:
            self.draw_block(2)
        else:
            pass

    def swapMouseTablet(self):
        if self.mT_TActive:
            self.mT_TActive = False
            self.mT_Image = self.mouseOrTabletImages[1]
            pygame.mouse.set_cursor((16, 16), (0, 0), (0, 0, 64, 0, 96, 0, 112, 0, 120, 0, 124, 0, 126, 0, 127, 0, 127,
                                                       128, 124, 0, 108, 0, 70, 0, 6, 0, 3, 0, 3, 0, 0, 0),
                                    (192, 0, 224, 0, 240, 0, 248, 0, 252, 0, 254, 0, 255, 0, 255, 128, 255, 192, 255,
                                     224, 254, 0, 239, 0, 207, 0, 135, 128, 7, 128, 3, 0))
        else:
            self.mT_TActive = True
            pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
            self.mT_Image = self.mouseOrTabletImages[0]

    def swapMuteUnmute(self):
        if self.mute:
            pygame.mixer.music.unpause()
            self.muteOrUnmuteImage = self.muteOrUnmuteImages[0]
            self.mute = False
        else:
            pygame.mixer.music.pause()
            self.muteOrUnmuteImage = self.muteOrUnmuteImages[1]
            self.mute = True


db = DemonBlock()

db.setup()
db.new()
while db.running:
    db.draw()
    db.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            db.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

