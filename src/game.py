from grid import Grid
from blocks import LBlock, JBlock, IBlock, OBlock, SBlock, TBlock, ZBlock
import random
import pygame
from colors import Colors


class Game:
    def __init__(self) -> None:
        self.grid = Grid()
        self.blocks = [
            IBlock(),
            JBlock(),
            LBlock(),
            OBlock(),
            SBlock(),
            TBlock(),
            ZBlock(),
        ]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.paused = False
        self.main_theme_sound = pygame.mixer.Sound("src/sounds/music.ogg")
        self.rotate_sound = pygame.mixer.Sound("src/sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("src/sounds/clear.ogg")
        self.play_music()
        self.current_level = 1
        self.levels = {1: 400, 2: 350, 3: 300, 4: 250, 5: 200, 6: 150}

    def play_music(self):
        pygame.mixer.music.load("src/sounds/music.ogg")
        pygame.mixer.music.play(-1)

    def pause(self):
        if self.paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def update_score(self, lines_cleared, move_down_points):
        if not self.paused and not self.game_over:
            if lines_cleared == 1:
                self.score += 100
            elif lines_cleared == 2:
                self.score += 300
            elif lines_cleared == 3:
                self.score += 500
            self.score += move_down_points

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [
                IBlock(),
                JBlock(),
                LBlock(),
                OBlock(),
                SBlock(),
                TBlock(),
                ZBlock(),
            ]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        if not self.paused:
            self.current_block.move(0, -1)
            if not self.block_inside() or not self.block_fits():
                self.current_block.move(0, 1)

    def move_right(self):
        if not self.paused:
            self.current_block.move(0, 1)
            if not self.block_inside() or not self.block_fits():
                self.current_block.move(0, -1)

    def move_down(self):
        if not self.paused:
            self.current_block.move(1, 0)
            if not self.block_inside() or not self.block_fits():
                self.current_block.move(-1, 0)
                self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_position()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        if not self.block_fits():
            self.game_over = True

    def block_fits(self):
        # get all cells of the block
        tiles = self.current_block.get_cell_position()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self):
        if not self.paused:
            self.current_block.rotate()
            if not self.block_inside() or not self.block_fits():
                self.current_block.undo_rotation()
            else:
                self.rotate_sound.play()

    def block_inside(self):
        tiles = self.current_block.get_cell_position()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True

    def reset(self):
        self.grid.reset()
        self.blocks = [
            IBlock(),
            JBlock(),
            LBlock(),
            OBlock(),
            SBlock(),
            TBlock(),
            ZBlock(),
        ]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def draw(self, screen):
        self.grid.draw(screen)

        if not self.game_over:
            self.current_block.draw(screen, 11, 11)

            if self.next_block.id == 3:
                self.next_block.draw(screen, 255, 290)
            elif self.next_block.id == 4:
                self.next_block.draw(screen, 255, 280)
            else:
                self.next_block.draw(screen, 270, 270)

        if self.paused:
            dim_surface = pygame.Surface((500, 620), pygame.SRCALPHA)
            dim_surface.fill((0, 0, 0, 128))
            screen.blit(dim_surface, (0, 0))

            paused_font = pygame.font.Font(None, 60)
            paused_text = paused_font.render("Paused", True, Colors.white)
            paused_text_rect = paused_text.get_rect(center=(500 // 2, 620 // 2))
            screen.blit(paused_text, paused_text_rect)
