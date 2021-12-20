import pygame, time

class Label:
	def __init__(self, main_window, loc, txt, cmd=None):
		self.type = 'Label'
		self.read_only = True
		self.mw = main_window
		self.loc = loc
		self.cmd = cmd
		self.screen = main_window.screen
		self.font = self.mw.font  
		self.color = (255,255,255)   # usual background white
		self.color_clicked = (200,200,200) # color when clicked
		self.bg = self.color # color to be used

		self.set_text(txt)
		self.txt_old = ''
		self.left = ''
		self.right = ''
		chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
		chars += r'1234567890,./;[]\`-=<>?:"{}|~!@#$%^&*()_+ '
		chars += "'"
		self.char_set = list(chars)

	def set_loc(self, loc):
		self.loc = loc 
		self.set_text(self.txt)

	def set_text(self, txt):
		self.txt = txt
		w,h = self.font.size(txt)
		dw,dh = 5,3
		self.w, self.h = w+dw+dw, h+dh+dh
		self.font_loc = self.loc[0]+dw, self.loc[1]+dh
		self.rect = pygame.Rect(self.loc, (self.w,self.h))

	def show(self):
		w = 0 if self.read_only else 1
		if not self.read_only: self.bg = (200,200,200)
		pygame.draw.rect(self.screen, self.bg, self.rect, width=w)
		txt_img = self.font.render(self.txt, True, (0,0,0))
		self.screen.blit(txt_img, self.font_loc)
		if self.mw.mygui.focus == self:
			self.show_cursor()

	def buttondown(self, button, pos):
		if self.cmd and self.rect.collidepoint(pos) and self.read_only:
			self.bg = self.color_clicked
			self.mw.update_display()
			self.cmd()
			time.sleep(0.3)
			self.bg =self.color 
			self.mw.update_display()
		elif self.rect.collidepoint(pos) and not self.read_only:
			self.mw.mygui.focus = self
			self.text_old = self.txt 
			self.txt = ''
			self.left = ''
			self.right = ''
			self.mw.update_display()

	def buttonup(self, button, pos):
		pass

	def mousemove(self, buttons, pos, rel):
		pass

	def keydown(self, event):
		kname = pygame.key.name(event.key)
		if kname=='return' or kname == 'enter':
			self.mw.mygui.focus = None
			if self.cmd: self.cmd()
		elif kname=='backspace':
			self.left = self.left[:-1]
		elif kname == 'delete':
			self.right = self.right[1:]
		elif kname == 'right':
			self.move_right()
		elif kname == 'left':
			self.move_left()
		elif kname == 'home':
			self.home()
		elif kname == 'end':
			self.end()
		elif kname == 'tab':
			self.swap_old_current()
		else:
			self.add_char(event)
		self.set_text(self.left + self.right)
		self.mw.update_display()

	def add_char(self, event):
		ch = ''+event.unicode
		if ch in self.char_set:
			self.left += ch

	def home(self):
		self.right = self.left + self.right
		self.left = ''

	def end(self):
		self.left += self.right
		self.right = ''

	def swap_old_current(self):
		self.left = self.text_old
		self.right = ''
		self.text_old = self.txt

	def move_right(self):
		self.left += self.right[:1]
		self.right = self.right[1:]

	def move_left(self):
		n = len(self.left)
		if n==0: return
		self.right = self.left[n-1:] + self.right
		self.left = self.left[:n-1]

	def show_cursor(self):
		(x,y)=self.font_loc
		(w,h)=self.font.size(self.left)
		x += w-1
		rect = pygame.Rect(x,y,1,h)
		pygame.draw.rect(self.screen, (255,0,0), rect, 1)

	def keyup(self, event):
		pass

class Entry(Label):
	def __init__(self, main_window, loc, txt, cmd=None):
		super().__init__(main_window, loc, txt, cmd)
		self.type = 'Entry'
		self.read_only = False