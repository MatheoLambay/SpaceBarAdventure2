import pygame

#button class
class Button():
	def __init__(self,screen, x, y, image, scale=1, center_pos = "topleft"):
		width = image.get_width()
		height = image.get_height()

		self.screen = screen
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		if center_pos == "topleft":
			self.rect.topleft = (x,y)
		elif center_pos == "topright":
			self.rect.topright = (x,y)
		elif center_pos == "bottomright":
			self.rect.bottomright = (x,y)
		elif center_pos == "bottomleft":
			self.rect.bottomleft = (x,y)
		elif center_pos == "center":
			self.rect.center = (x,y)
		self.clicked = False
		self.activated = None
		self.over_on = 0
		

	def draw(self):
		self.activated = True
		self.screen.blit(self.image, (self.rect.x, self.rect.y))


	def detect(self):
		if self.activated:
			action = False
			#get mouse position
			pos = pygame.mouse.get_pos()

			#check mouseover and clicked conditions
			if self.rect.collidepoint(pos):
					
				if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
					self.clicked = True
					action = True

			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False

			return action
		