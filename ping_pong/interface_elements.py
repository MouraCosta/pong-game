import random

import pygame
import pygame.sprite as sprite
import pygame.font as font


class ScoreBoard(sprite.Sprite):
	""""The game scoreboard. It shows the user the points, every time
	the ball hits a target."""

	def __init__(self, screen):
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.points = 0
		self.font = font.SysFont("Arial", bold=True, size=12)
		self.text_format = f"POINTS: {self.points}"
		self.colour = (255, 255, 255)
		self.image = self.font.render(self.text_format, True, self.colour)
		self.rect = self.image.get_rect()

		# ScoreBoard Positioning
		self.rect.bottomleft = self.screen_rect.bottomleft

	def draw(self):
		"""Draws the scoreboard on the screen."""
		self.screen.blit(self.image, self.rect)

	def update(self):
		"""Updates the score and the scoreboard everytime the user make
		points."""
		self.text_format = f"POINTS: {self.points}"
		self.image = self.font.render(self.text_format, True, self.colour)


class LifeRemaining(sprite.Sprite):
	"""A dynamic label that shows the user how many lives the paddle
	has. And it's a necessary condition to end the game when necessary.
	"""

	class LifeUnit(sprite.Sprite):
		"""A simple life unit."""

		def __init__(self, screen):
			super().__init__()
			self.screen = screen
			self.screen_rect = screen.get_rect()
			self.image = pygame.Surface((15, 15))
			self.image.fill((167, 0, 0))
			self.rect = self.image.get_rect()

		def draw(self):
			"""Draws the life unit."""

			self.screen.blit(self.image, self.rect)

	def __init__(self, screen):
		super().__init__()
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.group = []
		self.fill()

	def draw(self):
		"""Draws the remaining life on the screen."""
		padding = 2
		row = 30
		for life in self.group:
			life.rect.x = self.screen.get_width() - (row + padding)
			life.rect.y = self.screen.get_height() - (30 + padding)
			life.draw()
			row += 30

	def poll(self):
		"""Take out one unit of life. It will self update."""
		self.group.pop(0)

	def fill(self):
		"""Fill the group with three lives."""
		for c in range(3):
			life_unit = self.LifeUnit(self.screen)
			self.group.append(life_unit)


class Button(sprite.Sprite):

	def __init__(self, screen, colour, text, x, y, *actions):
		self.screen = screen
		self.screen_rect = screen.get_rect()

		self.font = font.SysFont("Arial", bold=True, size=16)
		self.text = self.font.render(text, False, (200,200,200))
		self.text_rect = self.text.get_rect()
		self.colour = colour or (68, 68, 98)
		self.rect = self.text_rect.inflate(15, 15)

		self.rect.x = x
		self.rect.y = y
		self.text_rect.centerx = self.rect.centerx
		self.text_rect.centery = self.rect.centery

		self.actions = actions

	def draw(self):
		"""Draw the button on the screen."""

		pygame.draw.rect(self.screen, self.colour, self.rect, border_radius=10)
		self.screen.blit(self.text, self.text_rect)

	def update(self):
		"""Gets the mouse position and execute actions."""

		mouse_pos = pygame.mouse.get_pos()
		mouse_pressed = pygame.mouse.get_pressed()
		if self.rect.collidepoint(mouse_pos) and mouse_pressed[0]:
			for action in self.actions:
				action()


class BlockRain():
	"""A quick block rain for the main menu."""

	def __init__(self, screen):
		self.screen = screen
		self.screen_rect = screen.get_rect()

		self.blocks = []
		self.maximum_x = screen.get_width() - 30
		for c in range(10):
			block = pygame.Surface((30, 30))
			block.fill([random.randrange(0, 255) for c in range(3)])

			block_rect = block.get_rect()
			block_rect.x = random.randrange(0, self.maximum_x)
			block_rect.y = 0
			self.blocks.append([block, block_rect])

	def draw(self):
		"""Draws all the fallen squares."""
		for fallen_square in self.blocks:
			self.screen.blit(fallen_square[0], fallen_square[1])

	def update(self):
		"""Updates and animates the fallen squares."""
		for pos, fallen_square in enumerate(self.blocks):
			fallen_square[1].y += random.randrange(1, 7)
			fallen_square[1].x += random.randrange(-2, 2)
			if fallen_square[1].bottom > self.screen_rect.bottom:
				fallen_square[1].y = 0
				fallen_square[1].x = random.randrange(0, self.maximum_x)
