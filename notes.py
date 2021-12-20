# GUI using pygame

import pygame, time, sys
from notes_gui import MyGUI
import json

class MainWindow:
	def __init__(self):
		pygame.font.init()
		font_file = pygame.font.match_font('timesnewroman')
		self.font = pygame.font.Font(font_file, 22) # adjust to match your screen
		pygame.display.init()
		w, h = 800, 600 # adjust to fit your screen
		#self.screen = pygame.display.set_mode((w,h)) # use specified screen size
		self.screen = pygame.display.set_mode() # full screen mode
		self.w, self.h = self.screen.get_rect().size
		self.bg_color = (255, 255, 255) # white background
		pygame.display.set_caption('Notes')
		self.gui = []  # list of GUI elements
		self.mygui = MyGUI(self)
		self.mygui.add()  # add GUI elements
		self.mygui.open_note(False)
		self.mygui.previous_page()
		self.update_display()

	def add(self, g):
		self.gui += [g]

	def run_window(self):
		# main loop
		while True:
			self.run_cycle()

	def run_cycle(self):
		time.sleep(0.001)
		# process keyboard and mouse events:
		for event in pygame.event.get():
			self.process_event(event)

	def process_event(self, event):
		if event.type == pygame.QUIT:
			self.Exit()
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			self.Exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.mygui.buttondown(event.button, event.pos)
		elif event.type == pygame.MOUSEBUTTONUP:
			self.mygui.buttonup(event.button, event.pos)
		elif event.type == pygame.MOUSEMOTION:
			self.mygui.mousemove(event.buttons, event.pos, event.rel)
		elif event.type == pygame.KEYDOWN:
			self.mygui.keydown(event)
		elif event.type == pygame.KEYUP:
			self.mygui.keyup(event)

	def update_display(self):
		self.screen.fill(self.bg_color) # erase everything
		self.show()
		pygame.display.flip() # make redraw visible

	def show(self):
		self.mygui.show()
		for g in self.gui:
			g.show()

	def Exit(self):
		# do something before exit if need
		self.mygui.save_as = False
		self.mygui.save_note()
		with open(self.mygui.lastnotefile, 'w') as f:
			json.dump(self.mygui.file.txt, f)
		sys.exit()

if __name__ == '__main__':
	# make a window instance and run it
	mw = MainWindow()
	mw.run_window()