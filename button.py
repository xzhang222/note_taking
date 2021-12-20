import pygame, time

class Button:
	def __init__(self, main_window, loc, txt, cmd=None):
		self.type = 'Button'
		self.mw = main_window
		self.loc = loc
		self.txt = txt
		self.cmd = cmd
		self.screen = main_window.screen
		self.font = self.mw.font  
		self.color = (230,230,230)   # usual background color
		self.color_clicked = (200,200,200) # background color when clicked
		self.bg = self.color # background color to be used
		w,h = self.font.size(self.txt)
		dw,dh = 5,3
		self.w, self.h = w+dw+dw, h+dh+dh
		self.font_loc = loc[0]+dw, loc[1]+dh
		self.rect = pygame.Rect(self.loc, (self.w,self.h))

	def show(self):
		pygame.draw.rect(self.screen, self.bg, self.rect)
		txt_img = self.font.render(self.txt, True, (0,0,0))
		self.screen.blit(txt_img, self.font_loc)

	def buttondown(self, button, pos):
		if self.cmd and self.rect.collidepoint(pos):
			self.bg = self.color_clicked
			self.mw.update_display()
			self.cmd()
			time.sleep(0.3)
			self.bg =self.color 
			self.mw.update_display()

	def buttonup(self, button, pos):
		pass

	def mousemove(self, buttons, pos, rel):
		pass

	def keydown(self, event):
		pass

	def keyup(self, event):
		pass
