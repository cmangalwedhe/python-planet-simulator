#TODO: CONVERT CODE TO PYGLET

import pygame
import math

pygame.init()

WIDTH, HEIGHT = 900, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation Project")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GRAY = (80, 78, 81)
DARK_RED = (107, 42, 32)
PAUSE_COLOR = (77, 75, 94)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
	AU = 149.6e6 * 1000
	G = 6.67428e-11
	SCALE = 125 / AU
	TIMESTEP = 3600 * 24

	def __init__(self, name, x, y, radius, color, hovered_color, mass):
		self.name = name
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.hovered_color = hovered_color
		self.current_color = color
		self.mass = mass

		self.orbit = []
		self.sun = False
		self.distance_to_sun = 0

		self.updated_x = x
		self.updated_y = y

		self.x_vel = 0
		self.y_vel = 0

	def draw(self, win):
		x = self.x * self.SCALE + WIDTH / 2
		y = self.y * self.SCALE + HEIGHT / 2

		if len(self.orbit) >= 3 and self.orbit[-1] != self.orbit[0]:
			updated_point = []
			for point in self.orbit:
				x, y = point
				x = x * self.SCALE + WIDTH / 2
				y = y * self.SCALE + HEIGHT / 2

				self.updated_x = x
				self.updated_y = y

				updated_point.append((self.updated_x, self.updated_y))

			pygame.draw.lines(win, self.color, False, updated_point, 2)

		pygame.draw.circle(win, self.current_color, (x, y), self.radius)


	def update_color(self, win):
		pygame.draw.circle(win, self.hovered_color, (self.updated_x, self.updated_y), self.radius)
		print("HELLO WORLD")


	def attraction(self, other):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = math.sqrt(distance_x**2 + distance_y**2)

		if other.sun:
			self.distance_to_sun = distance

		force = self.G * self.mass * other.mass / distance**2
		theta = math.atan2(distance_y, distance_x)

		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force

		return force_x, force_y

	def update_position(self, planets):
		total_fx = total_fy = 0

		for planet in planets:
			if self == planet:
				continue

			fx, fy = self.attraction(planet)
			total_fx += fx
			total_fy += fy

		self.x_vel += total_fx / self.mass * self.TIMESTEP
		self.y_vel += total_fy / self.mass * self.TIMESTEP

		self.x += self.x_vel * self.TIMESTEP
		self.y += self.y_vel * self.TIMESTEP

		self.orbit.append((self.x, self.y))


class Text:
	DISTANCE_FONT = pygame.font.SysFont('comicsans', 12)

	def __init__(self, planets, win):
		self.planets = planets
		self.win = win
		self.positions_of_text = self.create_key()

	def create_key(self):
		key_text = FONT.render("KEY:", 1, WHITE)
		WIN.blit(key_text, (20, 700))

		positions_of_text = []

		increment = 15
		val = 1

		for planet in self.planets:
			pygame.draw.circle(WIN, planet.color, (30 + increment * val, 740), 10)
			planet_text = FONT.render(f"{planet.name}", 1, WHITE)
			self.win.blit(planet_text, (45 + increment * val, 730))
			positions_of_text.append((45 + increment * val, 730))
			val += 10

		return positions_of_text

	def create_distance_text(self):
		distance_sun = self.DISTANCE_FONT.render("DISTANCE FROM SUN:", 1, WHITE)
		self.win.blit(distance_sun, (20, 760))

		for i in range(len(self.planets)):
			planet = self.planets[i]

			if planet.sun:
				continue

			x, y = self.positions_of_text[i]

			distance_text = self.DISTANCE_FONT.render(f"{round(planet.distance_to_sun / 1000, 1)} km", 1, WHITE)
			self.win.blit(distance_text, (x + 5, y + 30))


def pause_game(button, planets):
	paused = True

	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if button.collidepoint(pygame.mouse.get_pos()):
					paused = False
				else:
					open_windows(planets, pygame.mouse.get_pos())	

def open_windows(planets, points):
	for planet in planets:
		x, y = points
		planet_x = planet.updated_x
		planet_y = planet.updated_y

		if planet.sun and math.sqrt((x - planet_x) ** 2 + (y - planet_y) ** 2) <= planet.radius:
			return

def main():
	run = True
	clock = pygame.time.Clock()
	
	sun = Planet("Sun", 0, 0, 30, YELLOW, (255, 255, 125), 1.99892 * 10**30)
	sun.sun = True

	mercury = Planet("Mercury", 0.387 * Planet.AU, 0, 8, DARK_GRAY, (129, 126, 130), 3.30 * 10 ** 23)
	mercury.y_vel = -47.4 * 1000

	venus = Planet("Venus", 0.723 * Planet.AU, 0, 14, WHITE, (201, 201, 201), 4.8685 * 10 ** 24)
	venus.y_vel = -35.02 * 1000

	earth = Planet("Earth", -1 * Planet.AU, 0, 16, BLUE, (123, 154, 209), 5.9742 * 10**24)
	earth.y_vel = 29.783 * 1000

	mars = Planet("Mars", -1.524 * Planet.AU, 0, 12, RED, (186, 65, 74), 6.39 * 10**23)
	mars.y_vel = 24.077 * 1000

	planets = [sun, mercury, venus, earth, mars]
	window_text = Text(planets, WIN)

	while run:
		clock.tick(60)
		WIN.fill((0, 0, 0))

		button = pygame.draw.rect(WIN, PAUSE_COLOR, [10, 10, 100, 50])
		button_font = pygame.font.SysFont("arial", 20, bold=True)
		button_text = button_font.render("PAUSE", 1, WHITE)
		WIN.blit(button_text, (button.x + 23, button.y + 13))
		window_text.create_key()
		window_text.create_distance_text()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if button.collidepoint(pygame.mouse.get_pos()):
					pause_game(button, planets)

		for planet in planets:
			planet.update_position(planets)
			planet.draw(WIN)

		pygame.display.update()

	pygame.quit()

main()