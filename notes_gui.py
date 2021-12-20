import pygame
from button import Button
from label import Label, Entry
import json
from PIL import Image, ImageDraw 
from tkinter import filedialog
import tkinter as tk 
import os  

class MyGUI:
	def __init__(self, main_window):
		self.mw = main_window
		self.screen = self.mw.screen
		self.w, self.h = self.mw.w, self.mw.h 
		self.focus = None

	def add(self):
		self.lastnotefile = os.path.join(os.getcwd(), 'lastnote.txt')
		try:
			with open(self.lastnotefile) as f:
				self.lastnotepath = json.load(f)
		except:
			self.lastnotepath = None

		x, y, dx = 10, 10, 5

		self.pen = Label(self.mw, (x,y), 'pencil', self.sel_pen)
		self.mw.add(self.pen)

		x += self.pen.w + dx
		self.eraser = Label(self.mw, (x,y), 'eraser', self.sel_eraser)
		self.mw.add(self.eraser)

		x += self.eraser.w + dx
		self.k = Label(self.mw, (x,y), 'k', self.sel_k)
		self.mw.add(self.k)

		x += self.k.w + dx
		self.r = Label(self.mw, (x,y), 'r', self.sel_r)
		self.mw.add(self.r)

		x += self.r.w + dx
		self.g = Label(self.mw, (x,y), 'g', self.sel_g)
		self.mw.add(self.g)

		x += self.g.w + dx
		self.b = Label(self.mw, (x,y), 'b', self.sel_b)
		self.mw.add(self.b)

		x += self.b.w + dx
		self.size = Entry(self.mw, (x,y), '2')
		self.mw.add(self.size)

		x += self.size.w + dx
		add_p = Label(self.mw, (x,y), '+', self.add_page)
		self.mw.add(add_p)

		x += add_p.w + dx
		remove_p = Label(self.mw, (x,y), '-', self.remove_page)
		self.mw.add(remove_p)

		x += remove_p.w + dx
		back = Label(self.mw, (x,y), '<', self.previous_page)
		self.mw.add(back)

		x += back.w + dx
		self.page = Entry(self.mw, (x,y), '000', self.goto_page)
		self.mw.add(self.page)

		x += self.page.w + dx
		forward = Label(self.mw, (x,y), '>', self.next_page)
		self.mw.add(forward)

		x += forward.w + dx
		new = Button(self.mw, (x,y), 'new', self.new_note)
		self.mw.add(new)

		x += new.w + dx
		open_n = Button(self.mw, (x,y), 'open', self.open_note)
		self.mw.add(open_n)

		x += open_n.w + dx
		save = Button(self.mw, (x,y), 'save as', self.save_note)
		self.mw.add(save)

		x += save.w + dx
		pdf = Button(self.mw, (x,y), 'pdf', self.save_as_pdf)
		self.mw.add(pdf)

		x += pdf.w + dx
		self.file = Label(self.mw, (x,y), 'filename')
		self.mw.add(self.file)
		if self.lastnotepath: self.file.set_text(self.lastnotepath)

		self.move_labels(-1)

		y += save.h 
		self.tool_rect = pygame.rect.Rect((0,0),(self.w,y))

		self.tool = 'pen'  # pen or eraser
		self.color = 'b'   # k, r, g, b
		self.colors = {'k':(0,0,0), 'r':(255,0,0), 'g':(0,255,0), 'b':(0,0,255)}
		self.writing = False
		self.erasing = False
		self.pts = []
		self.note = [[]]
		self.p = 0
		self.y = 0
		self.save_as = True
		self.filetypes = (('notes', '*.note'), ('All files', '*.*'))

	def add_page(self):
		self.note.insert(self.p, [])
		self.y = 0

	def remove_page(self):
		self.note.remove(self.note[self.p])
		self.y = 0
		if len(self.note) == 0: self.note = [[]]
		if self.p == len(self.note):
			self.p -= 1 
			page = str(1000+self.p)[1:] if self.p < 1000 else str(self.p)
			self.page.set_text(page)

	def set_page(self, p):
		if p < 0: p = len(self.note)-1
		if p >= len(self.note): 
			p = len(self.note)
			self.note.append([])
		self.p = p 
		page = str(1000+p)[1:] if p < 1000 else str(p)
		self.page.set_text(page)
		self.y = 0
		self.mw.update_display()

	def previous_page(self):
		self.set_page(self.p - 1)

	def goto_page(self):
		try:
			p = int(self.page.txt)
		except:
			p = self.p
		self.set_page(p)

	def next_page(self):
		self.set_page(self.p + 1)

	def move_labels(self, s):
		for g in [self.k, self.r, self.g, self.b, self.pen, self.eraser]:
			(x,y) = g.loc 
			if s*x < 0:
				g.set_loc((x+s*3000, y))

	def sel_pen(self):
		self.tool = 'pen'

	def sel_eraser(self):
		self.tool = 'eraser'

	def sel_k(self):
		self.color = 'k'

	def sel_r(self):
		self.color = 'r'

	def sel_g(self):
		self.color = 'g'

	def sel_b(self):
		self.color = 'b'

	def new_note(self):
		self.save_as = False
		self.save_note()
		self.save_as = True
		root = tk.Tk()
		root.withdraw()
		root.update()
		path = filedialog.asksaveasfilename(filetypes=self.filetypes).split('.')[0]
		self.file.set_text(path)
		self.mw.update_display()
		root.update()
		root.destroy()
		self.note = [[]]
		self.p = 0 
		self.y = 0
		self.page.set_text('000')

	def open_note(self, selectfile=True):
		if selectfile:
			self.save_as = False
			self.save_note()
			self.save_as = True
			root = tk.Tk()
			root.withdraw()
			root.update()
			path = filedialog.askopenfilename(filetypes=self.filetypes).split('.')[0]
			self.file.set_text(path)
			self.mw.update_display()
			root.update()
			root.destroy()
		try:
			with open(f'{self.file.txt}.note') as f:
				self.note = json.load(f)
		except Exception as e:
			print(e)
			self.note = [[]]
		self.p = 0
		self.y = 0
		self.page.set_text('000')
		self.mw.update_display()

	def save_note(self):
		if self.note == [[]]: return
		if self.save_as:
			root = tk.Tk()
			root.withdraw()
			root.update()
			path = filedialog.asksaveasfilename(filetypes=self.filetypes).split('.')[0]
			self.file.set_text(path)
			self.mw.update_display()
			root.update()
			root.destroy()
		try:
			with open(f'{self.file.txt}.note', 'w') as f:
				json.dump(self.note, f)
		except Exception as e:
			print(e)

	def save_as_pdf(self):
		points = []
		for page in self.note:
			for s, c, pts in page: points += pts
		points.sort(key=lambda p:p[0])
		xmax = points[-1][0]
		xmax = int(xmax*1.1)
		imgs = []
		for page in self.note:
			points = []
			for s,c,pts in page: points += pts 
			points.sort(key=lambda p:p[1])
			ymax = points[-1][1]
			ymax = int(ymax*1.1)
			image = Image.new('RGB', (xmax, ymax), 'white')
			dr = ImageDraw.Draw(image)
			for s, c, pts in page:
				points = [(x,y) for x,y in pts]
				c = (c[0], c[1], c[2])
				dr.line(points, c, s)
			imgs.append(image)
		imgs[0].save(f'{self.file.txt}.pdf', save_all=True,
				append_images = imgs[1:])

	def show_note(self):
		if self.focus is None:
			try:
				p = int(self.page.txt)
			except:
				p = self.p 
			if p != self.p: p = self.p
			page = str(1000+p)[1:] if p < 1000 else str(p)
			self.page.set_text(page)
		for s, c, pts in self.note[self.p]:
			points = [(x,y-self.y) for x,y in pts]
			pygame.draw.lines(self.screen, c, False, points, s) # False: not close

	def show_pen(self):
		sc = self.screen
		pygame.draw.rect(sc, (255,255,255),self.pen)
		x, y = self.pen.loc 
		w, h = self.pen.w, self.pen.h 
		x0, y0 = x+5, y+int(h/2)
		x1, y1 = x+int(w/3), y+int(h/6)
		x2, y3 = x+w-5, y+int(5*h/6)
		pts = [(x0,y0),(x1,y1),(x2,y1),(x2,y3),(x1,y3)]
		pygame.draw.lines(sc, (0,0,0), True, pts, 1)

	def show_eraser(self):
		sc = self.screen
		pygame.draw.rect(sc, (255,255,255), self.eraser)
		x, y = self.eraser.loc 
		w, h = self.eraser.w, self.eraser.h 
		x0, x1, x4 = x+5, x+w-5, x+int(w/2)
		y0, y1 = y+5, y+h-5
		rect = pygame.Rect((x4,y0),(int(w/2-5),h-10))
		pygame.draw.rect(sc, (200,200,200), rect)
		pts = [(x4,y1),(x4,y0),(x1,y0),(x1,y1),(x0,y1),(x0,y0),(x4,y0)]
		pygame.draw.lines(sc, (0,0,0), True, pts, 1)

	def show_tools(self):
		t = 3
		sc = self.screen
		bg = (200,200,200)
		self.move_labels(1)
		ps = {'pen':self.pen, 'eraser':self.eraser}
		pygame.draw.rect(sc, bg, ps[self.tool], t) #use ps[] instead of 
					# ps[].rect, because attribute rect is defined in Label

		self.show_pen()
		self.show_eraser()
		pygame.draw.rect(sc, (0,0,0), self.k)
		pygame.draw.rect(sc, (255,0,0), self.r)
		pygame.draw.rect(sc, (0,255,0), self.g)
		pygame.draw.rect(sc, (0,0,255), self.b)
		cs = {'k':self.k, 'r':self.r, 'g':self.g, 'b':self.b}
		pygame.draw.rect(sc, bg, cs[self.color], t)
		self.move_labels(-1)

	def show(self):
		pass

		self.show_note()
		pygame.draw.rect(self.screen, (255,255,255), self.tool_rect)
		self.show_tools()

	def get_size_color(self):
		try:
			s = int(self.size.txt)
			if s < 1: s = 1
			if s > 9: s = 9
		except:
			s = 1
		self.size.set_text(str(s))
		c = self.colors[self.color]
		return (s, c)

	def add_pt(self, pos):
		s, c = self.get_size_color()
		pygame.draw.line(self.screen, c, self.pts[-1], pos, s)
		pygame.display.flip()
		self.pts.append(pos)
		return (s, c)

	def remove(self, pos):
		r = 5 
		new_note = []
		for stroke in self.note[self.p]:
			s, c, pts = stroke
			x0, y0 = pos
			y0 += self.y 
			keep = True
			for x, y in pts:
				if abs(x-x0)<r and abs(y-y0)<r: 
					keep = False
					break
			if keep: new_note.append(stroke)
		self.note[self.p] = new_note
		self.mw.update_display()

	def custom_buttondown(self, button, pos):
		pass

		if pos[1]<= self.pen.loc[1] + self.pen.h: return
		if self.tool == 'pen':
			self.writing = True
			self.pts = [pos]
		elif self.tool == 'eraser':
			self.erasing = True
			self.remove(pos)

	def buttondown(self, button, pos):
		self.custom_buttondown(button, pos)
		self.move_labels(1)
		for g in self.mw.gui:
			if g != self.focus: g.buttondown(button, pos)
		self.move_labels(-1)
		self.mw.update_display()

	def buttonup(self, button, pos):
		pass

		if self.tool == 'pen' and self.writing:
			(s, c) = self.add_pt(pos)
			points = [(x,y+self.y) for x,y in self.pts]
			self.note[self.p].append((s, c, points))
			self.writing = False
		elif self.tool == 'eraser' and self.erasing:
			self.remove(pos)
			self.erasing = False

	def mousemove(self, buttons, pos, rel):
		pass

		if self.tool == 'pen' and self.writing:
			self.add_pt(pos)
		elif self.tool == 'eraser' and self.erasing:
			self.remove(pos)

	def scroll(self, event):
		h = self.h - self.tool_rect.h
		page = int(h*0.9)
		line = int(h*0.1)
		tiny = int(line*0.1)
		if pygame.key.name(event.key) == 'right':
			self.y += tiny
		elif pygame.key.name(event.key) == 'left':
			self.y -= tiny
		elif pygame.key.name(event.key) == 'down':
			self.y += line
		elif pygame.key.name(event.key) == 'up':
			self.y -= line
		elif pygame.key.name(event.key) == 'page down':
			self.y += page
		elif pygame.key.name(event.key) == 'page up':
			self.y -= page
		elif pygame.key.name(event.key) == 'home':
			self.y = 0
		elif pygame.key.name(event.key) == 'end':
			points = []
			for s, c, pts in self.note[self.p]: points += pts
			points.sort(key=lambda p:p[1])
			ymax = points[-1][1]
			self.y = ymax - self.h + tiny*3
		if self.y < 0: self.y = 0
		self.mw.update_display()

	def keydown(self, event):
		self.scroll(event)
		if self.focus:
			self.focus.keydown(event)

	def keyup(self, event):
		pass
