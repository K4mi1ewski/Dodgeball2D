import pygame
import os
from math import sqrt


class Player(pygame.sprite.Sprite):
    VEL = 4

    def __init__(self, team, x, y, bench=False):
        pygame.sprite.Sprite.__init__(self)
        self.team = int(team)
        self.bench = bench

        player_img = pygame.image.load(os.path.join('scripts/Assets', 'players', 'superswinka.png')).convert_alpha()
        player_img_scaled = pygame.transform.scale_by(player_img, 0.4)

        player_img_left_direction = pygame.transform.flip(player_img_scaled, True, False)
        player_img_right_direction = player_img_scaled
        player_img_up_direction = pygame.transform.rotate(player_img_scaled, 90)
        player_img_down_direction = pygame.transform.rotate(player_img_scaled, -90)
        self.player_images = (player_img_right_direction, player_img_left_direction,
                              player_img_up_direction, player_img_down_direction)

        if team:
            self.color = 'Red'
            self.direction = "left"
            self.image = player_img_left_direction
        else:
            self.color = 'Blue'
            self.direction = "right"
            self.image = player_img_right_direction

        self.rect = self.image.get_rect(center=(x, y))

    def __rotate__(self, keys):
        if keys[pygame.K_a] and self.direction != "left":
            self.direction = "left"
            self.image = self.player_images[1]
            self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
        if keys[pygame.K_d] and self.direction != "right":
            self.direction = "right"
            self.image = self.player_images[0]
            self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
        if keys[pygame.K_s] and self.direction != "down":
            self.direction = "down"
            self.image = self.player_images[3]
            self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
        if keys[pygame.K_w] and self.direction != "up":
            self.direction = "up"
            self.image = self.player_images[2]
            self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))

    def move(self, obstacles, team):
        keys = pygame.key.get_pressed()

        current_x = self.rect.x
        current_y = self.rect.y
        prev_rect = self.rect
        prev_img = self.image
        prev_direction = self.direction

        self.__rotate__(keys)

        x_movement = 0
        y_movement = 0

        if keys[pygame.K_RIGHT] and self.direction == "right":
            x_movement += self.VEL
        elif keys[pygame.K_RIGHT]:
            x_movement += 0.8 * self.VEL

        if keys[pygame.K_LEFT] and self.direction == "left":
            x_movement -= self.VEL
        elif keys[pygame.K_LEFT]:
            x_movement -= 0.8 * self.VEL

        if keys[pygame.K_UP] and self.direction == "up":
            y_movement -= self.VEL
        elif keys[pygame.K_UP]:
            y_movement -= 0.8 * self.VEL

        if keys[pygame.K_DOWN] and self.direction == "down":
            y_movement += self.VEL
        elif keys[pygame.K_DOWN]:
            y_movement += 0.8 * self.VEL

        self.rect.x += x_movement
        self.rect.y += y_movement

        obstacle_collision = pygame.sprite.spritecollide(self, obstacles, False, pygame.sprite.collide_mask)
        player_collision = pygame.sprite.spritecollide(self, team, False, pygame.sprite.collide_mask)

        player_collision.remove(self)

        if obstacle_collision or player_collision:
            self.rect.x, self.rect.y = current_x, current_y
            self.direction = prev_direction
            self.image = prev_img
            self.rect = prev_rect


    def catch_ball(self, ball):
        key = pygame.key.get_pressed()
        x = self.rect.centerx
        y = self.rect.centery
        ball_player_distance = sqrt((x - ball.rect.centerx)**2+(y-ball.rect.centery)**2)

        if key[pygame.K_SPACE] and (ball_player_distance <= 50):
            ball.vel = pygame.math.Vector2(0, 0)
            return 0
        return 1

