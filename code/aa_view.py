#!/usr/bin/python
#filename aa_view.py

import Tkinter

class View:
	"""mvc's view model

	i use tkinter to draw.
	"""
	def __init__(self, parent, model, col, row):
		"""create canvas for drawing
		"""
		self.m_parent = parent
		self.m_model = model
		[canvasWidth, canvasHeight] = self.RowColToXY(row, col)
		#use 'highlightthickness' to hide about 2 px border.(borderwidth can't erase this 'border')
		self.m_cv = Tkinter.Canvas(self.m_parent, width = canvasWidth, height = canvasHeight, borderwidth=0, highlightthickness=1, bg='#ffffff')
		self.m_cv.pack(side=Tkinter.RIGHT, padx=5, pady=5)

	def XYToRowCol(self, x, y):
		"""coordinate trans
		"""
		return [y / 13, x / 8]

	def RowColToXY(self, row, col):
		"""coordinate trans
		"""
		return [col * 8, row * 13] #5*1.6, 10*1.3

	def _DrawTextXY(self, x, y, char):
		"""draw char in x,y pos. x, y is pixel pos
		"""
		self.m_cv.create_text((x, y), text = char, anchor='nw', font='courier 10')

	def _DrawCubeXYWhite(self, x, y):
		"""draw a white cube which like a space 
		"""
		self.m_cv.create_rectangle(x, y, x + 8, y + 13 + 2, width = 0, fill='#ffffff')

	def _DrawCubeXYBlue(self, x, y):
		"""draw a blue cube, same size as space char
		"""
		self.m_cv.create_rectangle(x, y, x + 8, y + 13 + 2, width = 0, fill='#b5d5ff')

	def _UpdateCharAlpha0White(self, data):
		"""draw char with white background

		data type is [[row, col, char], [row, col, char], ...]
		"""
		for [r, c, ch] in data:
			(x, y) = self.RowColToXY(r, c)
			self._DrawCubeXYWhite(x, y)
			self._DrawTextXY(x, y, ch)

	def _UpdateCharAlpha0Blue(self, data):
		"""draw char with blue background

		data type is [[row, col, char], [row, col, char], ...]
		"""
		for [r, c, ch] in data:
			(x, y) = self.RowColToXY(r, c)
			self._DrawCubeXYBlue(x, y)
			self._DrawTextXY(x, y, ch)		

	def _UpdateCharAlpha100(self, data):
		"""draw char, doesn't draw background. 

		data type is [[row, col, char], [row, col, char], ...]
		"""
		for [r, c, ch] in data:
			(x, y) = self.RowColToXY(r, c)
			self._DrawTextXY(x, y, ch)		

	def _UpdateCubeColorWhite(self, data):
		"""draw white cube. 

		data type is [[row, col, char], [row, col, char], ...], in which 'char' is not care
		"""
		for [r, c, ch] in data:
			(x, y) = self.RowColToXY(r, c)
			self._DrawCubeXYWhite(x, y)

	def _UpdateCubeColorBlue(self, data):
		"""draw blue cube. 

		data type is [[row, col, char], [row, col, char], ...], in which 'char' is not care
		"""
		for [r, c, ch] in data:
			(x, y) = self.RowColToXY(r, c)
			self._DrawCubeXYBlue(x, y)		

	def Update(self, cmd, data):
		"""update view func.

		type is V_CHAR_ALPHA_0_BACK_WHITE, V_CHAR_ALPHA_0_BACK_BLUE, V_CHAR_ALPHA_100, V_CUBE_COLOR_WHITE, V_CUBE_COLOR_BLUE
		"""
		if cmd == 'V_CHAR_ALPHA_0_BACK_WHITE':
			self._UpdateCharAlpha0White(data)
		elif cmd == 'V_CHAR_ALPHA_0_BACK_BLUE':
			self._UpdateCharAlpha0Blue(data)
		elif cmd == 'V_CHAR_ALPHA_100':
			self._UpdateCharAlpha100(data)
		elif cmd == 'V_CUBE_COLOR_WHITE':
			self._UpdateCubeColorWhite(data)
		elif cmd == 'V_CUBE_COLOR_BLUE':
			self._UpdateCubeColorBlue(data)
		else:
			print 'warning:view\' update cmd is not vaild!'


if __name__ == '__main__':
	print 'this is aa_view file. please run aa_control.py'