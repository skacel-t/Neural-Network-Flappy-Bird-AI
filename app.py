import pygame
from sys import exit
import components
import config
import population


pygame.init()
clock = pygame.time.Clock()
population = population.Population(40)

def generate_pipes():
	config.pipes.append(components.Pipes(config.win_width))

def quit_game():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

def main():
	# get_info = True
	pipes_spawn_time = 10
	timer = 0

	while True:
		quit_game()
		timer += 1
		config.window.fill((0, 0, 0))
		# spawn ground
		config.ground.draw(config.window)
		# spawn pipes
		if pipes_spawn_time <= 0:
			generate_pipes()
			pipes_spawn_time = 200
		pipes_spawn_time -= 1
		rem = []
		for p in config.pipes:
			p.draw(config.window)
			p.update()
			if p.off_screen:
				rem.append(p)
		for r in rem:
			config.pipes.remove(r)

		# AI
		if not population.extinct():
			population.update_live_players()
		else:
			config.pipes.clear()
			population.natural_selection()
			pipes_spawn_time = 10
			timer = 0

		if timer == 18000:
			print("TIMER!")
			config.pipes.clear()
			population.natural_selection()
			pipes_spawn_time = 10
			timer = 0

		clock.tick(60)
		pygame.display.flip()


if __name__ == "__main__":
	main()
