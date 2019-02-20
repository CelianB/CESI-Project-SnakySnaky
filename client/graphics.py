import pygame

class Graphics:
	def __init__(self, title, frame):
		self.frame = frame
		self.windowTitle = title
		self.dir_imgs = 'assets/textures/'

	def isCollide(self, rect):
		mouse = pygame.mouse.get_pos()
		return (((mouse[0] >= rect.left) and (mouse[0] < (rect.left + rect.width))) and ((mouse[1] >= rect.top) and (mouse[1] < (rect.top + rect.height))))

	def rgb(self, ir, ig, ib):
		return ir, ig, ib

	def drawText(self, font, texte, color, topLeft, render=True):
		texteRendered = font.render(texte, True, color)
		texteRenderedRect = texteRendered.get_rect()
		texteRenderedRect.topleft = topLeft
		if render:
			self.frame.blit(texteRendered, texteRenderedRect)
		return texteRenderedRect

	def drawCenteredTextWithChangeColorDoubleRect(self, font, texte, color1, color2, topLeft, dist, size, render=True):
		tRect = self.drawText(font, texte, color1, topLeft, False)
		if not self.isCollide(tRect):
			return self.drawText(font, texte, color1, topLeft, render)
		else:
			self.drawRect(color1, (topLeft[0] - dist - size, topLeft[1]), (size,size))
			self.drawRect(color1, (topLeft[0] + tRect.width + dist, topLeft[1]), (size,size))
			return self.drawText(font, texte, color2, topLeft, render)

	def drawCenteredTextChangeColor(self, font, texte, color1, color2, posY, render=True):
		if not self.isCollide(self.drawCenteredText(font, texte, color1, posY, False)):
			return self.drawCenteredText(font, texte, color1, posY, render)
		else:
			return self.drawCenteredText(font, texte, color2, posY, render)

	def drawCenteredText(self, font, texte, color, posY, render=True):
		return self.drawText(font, texte, color, (self.frame.get_size()[0] / 2 - font.size(texte)[0] / 2, posY), render)

	def drawRect(self, color, topLeft, size, render=True):
		rect = pygame.Rect((topLeft), (size))
		if render:
			pygame.draw.rect(self.frame, color, (topLeft[0], topLeft[1], size[0], size[1]))
		return rect

	def drawRectChangeColor(self, color1, color2, topLeft, size):
		if not self.isCollide(self.drawRect(color1, topLeft, size, False)):
			return self.drawRect(color1, topLeft, size, True)
		else:
			return self.drawRect(color2, topLeft, size, True)

	def drawRectWithText(self, color, font, text, colorT, topLeft, size, render=True):
		rec = self.drawRect(color, topLeft, size, True)
		sizeT = self.drawText(font, text, colorT, (topLeft[0], topLeft[1]), False)
		self.drawText(font, text, colorT, (topLeft[0] + (size[0] / 2 - sizeT.width / 2), topLeft[1] + (size[1] / 2 - sizeT.height / 2)))
		return rec

	def drawRectChangeColorWithText(self, color1, color2, font, text, colorT1, colorT2, topLeft, size):
		if not self.isCollide(self.drawRect(color1, topLeft, size, False)):
			return self.drawRectWithText(color1, font, text, colorT1, topLeft, size, True)
		else:
			return self.drawRectWithText(color2, font, text, colorT2, topLeft, size, True)

	def drawText3D(self, font, texte, color1, color2, topLeft, render=True):
		self.drawText(font, texte, color1, (topLeft[0]-3, topLeft[1]-3))
		return self.drawText(font, texte, color2, topLeft)

	def drawTextChangeColor(self, font, texte, color1, color2, topLeft, render=True):
		if not self.isCollide(self.drawText(font, texte, color1, topLeft, False)):
			return self.drawText(font, texte, color1, topLeft, render)
		else:
			return self.drawText(font, texte, color2, topLeft, render)

	def rotateImage(self, image, degrees):
		return pygame.transform.rotate(image, degrees)

	def displayBackground(self, image):
		self.frame.blit(image, (0, 0))

	def drawImage(self, img, pos):
		rect = img.get_rect()
		rect.topleft = pos
		self.frame.blit(img, rect)
		return rect

	def loadImage(self, image):
		return pygame.image.load(self.dir_imgs + image)

	def loadFont(self, filename, height):
		return pygame.font.Font(filename, height)

	def loadBackground(self, img):
		return pygame.transform.scale(self.loadImage(img), (self.frame.get_size()[0], self.frame.get_size()[1]))

	def setWindowTitle(self):
		pygame.display.set_caption(self.windowTitle + ' - ' + str(s))