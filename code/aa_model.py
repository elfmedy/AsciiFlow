#!/usr/bin/python
#filename aa_model.py

class ItemDesToData:
	"""calss ItemDesToData.

	create data by description. data type is [[row, col, ch], [row, col, ch], ...]
	"""
	def __init__(self):
		self.m_arrowCase = ('>', '<', 'v', '^', '+')

	def Lines(self, des):
		"""return lines data
		"""
		(r0, c0, r1, c1) = (des[0][0], des[0][1], des[1][0], des[1][1])
		re = [[r1, c1, '+']]
		[re.append(i) for i in [[r1, c0, '+'], [r0, c0, '+']] if not i in re]
		[re.append([i, c0, '|']) for i in range(min(r0, r1) + 1, max(r0, r1))]
		[re.append([r1, i, '-']) for i in range(min(c0, c1) + 1, max(c0, c1))]
		return re

	def LinesWithArrow(self, des):
		"""return lines whith arrow data
		"""
		re = self.Lines(des)
		(r0, c0, r1, c1) = (des[0][0], des[0][1], des[1][0], des[1][1])
		arrowIdx = 0
		if c1 > c0: arrowIdx = 0
		elif c1 < c0: arrowIdx = 1
		else:
			if r1 > r0: arrowIdx = 2
			elif r1 < r0: arrowIdx = 3
			else: arrowIdx = 4
		re[0][2] = self.m_arrowCase[arrowIdx]
		return re

	def LineRect(self, des):
		"""return lines rect data
		"""
		(r0, c0, r1, c1) = (des[0][0], des[0][1], des[1][0], des[1][1])
		if r0 == r1 or c0 == c1:
			return self.Lines(des)
		re = [[r1, c1, '+']]
		[re.append(i) for i in [[r0, c0, '+'], [r0, c1, '+'], [r1, c0, '+']] if not i in re]
		[re.append([i, c0, '|']) for i in range(min(r0, r1) + 1, max(r0, r1))]
		[re.append([i, c1, '|']) for i in range(min(r0, r1) + 1, max(r0, r1))]
		[re.append([r0, i, '-']) for i in range(min(c0, c1) + 1, max(c0, c1))]
		[re.append([r1, i, '-']) for i in range(min(c0, c1) + 1, max(c0, c1))]
		return re

	def FilledRect(self, des, fillData):
		"""return fill rect data. char in data is space
		"""
		(r0, c0, r1, c1) = (des[0][0], des[0][1], des[1][0], des[1][1])
		re = []
		for i in range(min(r0, r1), max(r0, r1) + 1):
			for j in range(min(c0, c1), max(c0, c1) + 1): 
				re.append([i, j, fillData])
		return re


class ObserverInterface:
	"""observers class. 

	have basic func for observers, attach, deattch, and notify
	"""
	def __init__(self):
		self.m_observers = []

	def AttachObserver(self, ob):
		"""attach observers
		"""
		self.m_observers.append(ob)

	def DetachObserver(self, ob):
		"""deattach observers
		"""
		self.m_observers = [i for i in self.m_observers if i != ob]

	def ClearObserver(self):
		"""clear observers
		"""
		self.m_observers = []

	def Notify(self, cmd, data):
		"""notify all listens.

		call theirs's 'Update' func.
		"""
		for view in self.m_observers:
				view.Update(cmd, data)


class CanvasManager(ObserverInterface):
	"""mvc's model data array
	"""
	def __init__(self, col, row):
		"""create model
		"""
		ObserverInterface.__init__(self)
		self.m_width  = col
		self.m_height = row
		self.m_desToData = ItemDesToData()
		self.m_canvasBuff = [[' '] * self.m_width for i in range(self.m_height)]
		self.m_lastDisData = []
		self.m_cursorSt  = 0           #cursor state. 0 is disabled. 1 is enabled
		self.m_cursorPos = [-1, -1]    #current cursor postion.

	def _DesToData(self, type, des):
		"""description trasns to data list
		"""
		newDisData = []
		if type == 'M_LINES':
			newDisData = self.m_desToData.Lines(des)
		elif type == 'M_LINES_WITH_ARROW':
			newDisData = self.m_desToData.LinesWithArrow(des)
		elif type == 'M_LINE_RECT':
			newDisData = self.m_desToData.LineRect(des)
		elif type == 'M_FILLED_RECT_BLUE_ALPHA_0' or type == 'M_FILLED_RECT_BLUE_ALPHA_100' or type == 'M_FILLED_RECT_WHITE_ALPHA_0':
			newDisData = self.m_desToData.FilledRect(des, ' ')
		else:
			print 'warning:CanvasManager _DesToData type is not vaild!'
		return newDisData

	def DisItemByDesContinue(self, type, des):
		"""display item, but not add it in to data array.

		this func call view's func sequence. this func use shadow array to reduce draw func's calling, just draw new data.
		"""
		newDisData = self._DesToData(type, des)
		oldClearList = [[r, c, self.m_canvasBuff[r][c]] for [r, c, ch] in self.m_lastDisData if [r, c, ch] not in newDisData and r in range(self.m_height) and c in range(self.m_width)]
		self.Notify('V_CHAR_ALPHA_0_BACK_WHITE', oldClearList)	
		if type == 'M_LINES' or type == 'M_LINES_WITH_ARROW' or type == 'M_LINE_RECT':	
			newDrawList  = [i for i in newDisData if i not in self.m_lastDisData]
			self.Notify('V_CHAR_ALPHA_0_BACK_WHITE', newDrawList)
		elif type == 'M_FILLED_RECT_BLUE_ALPHA_0':
			newDrawList  = [i for i in newDisData if i not in self.m_lastDisData]
			self.Notify('V_CUBE_COLOR_BLUE', newDrawList)		
		elif type == 'M_FILLED_RECT_WHITE_ALPHA_0':
			newDrawList  = [i for i in newDisData if i not in self.m_lastDisData]
			self.Notify('V_CUBE_COLOR_WHITE', newDrawList)			
		elif type == 'M_FILLED_RECT_BLUE_ALPHA_100':
			newDrawList  = [[r, c, self.m_canvasBuff[r][c]] for [r, c, ch] in newDisData if [r, c, ch] not in self.m_lastDisData]
			self.Notify('V_CHAR_ALPHA_0_BACK_BLUE', newDrawList)
		else:
			print 'invaild DisItemByDesContinue type'
		self.m_lastDisData = newDisData

	def DisItemByDesOnce(self, type, des):
		"""disp data.

		Once mean doesn't use shadow array.
		"""
		data = self._DesToData(type, des)
		if type == 'M_FILLED_RECT_WHITE_ALPHA_0':
			self.Notify('V_CUBE_COLOR_WHITE', data)
		else:
			print 'invaild DisItemByDesOnce type'	

	def DisItemByDataContinue(self, cmd, data):
		"""disp item but not add to data array.

		use shadow to reduce draw func's call, jusr draw new data different with last drawing.
		"""
		oldClearList = [[r, c, self.m_canvasBuff[r][c]] for [r, c, ch] in self.m_lastDisData if [r, c, ch] not in data and r in range(self.m_height) and c in range(self.m_width)]
		self.Notify('V_CHAR_ALPHA_0_BACK_WHITE', oldClearList)
		self.m_lastDisData = data
		if cmd == 'M_BACK_BLUE':
			self.Notify('V_CHAR_ALPHA_0_BACK_BLUE', data)
		else:
			print 'invaild cmd int DisItemByDataContinue'		

	def DisItemByDataOnce(self, cmd, data):
		"""disp data once, dosen't use shadow array.
		"""
		if cmd == 'M_BACK_WHITE':
			self.Notify('V_CHAR_ALPHA_0_BACK_WHITE', data)
		else:
			print 'invaild cmd int DisItemByDataOnce'

	def _CheckDataInRange(self, s):
		"""give a list data [r, c, ch], check if it is out of range
		"""
		if s[0] in range(self.m_height) and s[1] in range(self.m_width):
			return True
		else:
			return False

	def AddItemByDes(self, type, des):
		"""add item to data array.
		"""
		data = self._DesToData(type, des)
		for [r, c, ch] in data:
			if self._CheckDataInRange([r, c, ch]):
				self.m_canvasBuff[r][c] = ch
		self.m_lastDisData = []

	def AddItemByData(self, data):
		"""add data to data array
		"""
		#if data[0][0] > 0 and data[0][1] > 0:
		for [r, c, ch] in data:
			if self._CheckDataInRange([r, c, ch]):
				self.m_canvasBuff[r][c] = ch
		self.m_lastDisData = []

	def DelRectItemByDes(self, des):
		"""del item.

		just del data array's data.
		"""
		data = self.m_desToData.FilledRect(des, ' ')
		for [r, c, ch] in data:
			if self._CheckDataInRange([r, c, ch]):
				self.m_canvasBuff[r][c] = ' '
		self.m_lastDisData = []


	def DelItemByDataMiddle(self, data):
		"""temp func. del data array's data
		"""
		for [r, c, ch] in data:
			if self._CheckDataInRange([r, c, ch]):
				self.m_canvasBuff[r][c] = ' '

	def AddText(self, r, c, ch, keycode):
		"""add text. left , right ,... is support
		"""
		if ch >= ' ' and ch <= '~':
			self.m_canvasBuff[r][c] = ch
			if self._CheckDataInRange([r, c + 1]):
				self.SetCursor(r, c + 1)
			else:
				self.SetCursor(r, c)
		elif keycode == 8:	#backspace
			self.m_canvasBuff[r][c] = ' '
			if self._CheckDataInRange([r, c - 1]):
				self.SetCursor(r, c - 1)
			else:
				self.SetCursor(r, c)
		elif keycode == 37: #left
			if self._CheckDataInRange([r, c - 1]):
				self.SetCursor(r, c - 1)
			else:
				self.SetCursor(r, c)
		elif keycode == 38: #up
			if self._CheckDataInRange([r - 1, c]):
				self.SetCursor(r - 1, c)
		elif keycode == 39: #right
			if self._CheckDataInRange([r, c + 1]):
				self.SetCursor(r, c + 1)
			else:
				self.SetCursor(r, c)
		elif keycode == 40: #down
			if self._CheckDataInRange([r + 1, c]):
				self.SetCursor(r + 1, c)
			else:
				self.SetCursor(r, c)


	#def GetPosVal(self, row, col):
	#	"""get data array's value of this pos
	#	"""
	#	return self.m_canvasBuff[row][col]

	def GetRectCharPosList(self, rect):
		"""give a area. return a list data in which is the data not equal to space in the area
		"""
		re = []
		selectRect = self.m_desToData.FilledRect(rect, ' ')
		for [r, c, ch] in selectRect:
			buffCh = self.m_canvasBuff[r][c]
			if buffCh != ' ':
				re.append([r, c, buffCh])
		return re

	def GetPosBuffVal(self, row, col):
		"""get data array's value of this pos
		"""
		return self.m_canvasBuff[row][col]

	def _CursorLeaveCurPos(self):
		"""cursor leave this pos.

		draw the old cursor with white color and draw data array in this pos
		"""
		(r, c) = (self.m_cursorPos[0], self.m_cursorPos[1])
		if r >= 0 or c >= 0:
			self.Notify('V_CHAR_ALPHA_0_BACK_WHITE', [[r, c, self.m_canvasBuff[r][c]]])	

	def EnableCursor(self):
		"""enable cursor. set cursor pos [-1, -1]
		"""
		if self.m_cursorSt == 0:
			self.m_cursorSt  = 1
			self.m_cursorPos = [-1, -1]

	def DisableCursor(self):
		"""enable cursor. set cursor pos [-1, -1]

		this fun will call _CursorLeaveCurPos.
		"""
		if self.m_cursorSt == 1:
			self.m_cursorSt  = 0
			self._CursorLeaveCurPos()
			self.m_cursorPos = [-1, -1]
			
	def SetCursor(self, row, col):
		"""set cusor pos
		"""
		if self._CheckDataInRange([row, col]):
			self._CursorLeaveCurPos()
			self.m_cursorPos = [row, col]
			self.Notify('V_CHAR_ALPHA_0_BACK_BLUE', [[row, col, self.m_canvasBuff[row][col]]])

	def GetCursor(self):
		"""get the pos of cursor. row and col
		"""
		return self.m_cursorPos

	def CreateFile(self):
		"""create output filename

		filename is output.txt
		"""
		f = open('ouput.txt', 'w')
		for i in range(0, self.m_height):
			for j in range(0, self.m_width):
				f.write(self.m_canvasBuff[i][j])
			f.write('\n')

if __name__ == '__main__':
	print 'this is the model file, please run aa_control.py'
