#!/usr/bin/python
#filename aa_control.py

import Tkinter
from aa_model import CanvasManager
from aa_view  import View

class Controler:
	"""class Controler

	MVC's control model.
	"""
	def __init__(self, col, row):
		"""__init__

		create modle and view. create button and bind event.
		"""
		self.m_root = Tkinter.Tk(className='AsciiArt')
		self.m_model = CanvasManager(col, row)
		self.m_view  = View(self.m_root, self.m_model, col, row)
		self.m_model.AttachObserver(self.m_view)
		self.m_state = 'ST_SELECT'
		self.m_selectRectStartPos = [-1, -1]
		self.m_selectRowColData    = []
		self.m_dragMoveStart = [-1, -1]
		self.m_drawStartPos = [-1, -1]
		self._InitWidget()
		self._InitKeyEvent()

	def Start(self):
		"""start the tkinter's main loop
		"""
		self.m_root.mainloop()

	def _InitWidget(self):
		"""create button and bind click event
		"""
		self.m_btSelect         = {}
		self.m_btLines          = {}
		self.m_btLinesWithArrow = {}
		self.m_btLineRect       = {}
		self.m_btText           = {}
		self.m_btDelRect        = {}
		self.m_btOutFile        = {}
		buttonTable = [
			[self.m_btSelect        , 'Select'          , self._CbSelect        ],
			[self.m_btLines         , 'Lines'           , self._CbLines         ],
			[self.m_btLinesWithArrow, 'Lines with arrow', self._CbLinesWithArrow],
			[self.m_btLineRect      , 'Line rect'       , self._CbLineRect      ],
			[self.m_btText          , 'Text'            , self._CbText          ],
			[self.m_btDelRect       , 'Del rect'        , self._CbDelRect       ],
			[self.m_btOutFile       , 'Create file'     , self._CbCreateFile    ]
		]
		labelFrame = Tkinter.LabelFrame(self.m_root)
		labelFrame.pack(side = Tkinter.LEFT, fill=Tkinter.Y, padx=5, pady=5)
		for [val, title, cbFunc] in buttonTable:
			val = Tkinter.Button(labelFrame, text = title, command=cbFunc, width=15, height=1, bg='#ffffff')
			val.pack(padx=4, pady=2)

	def _InitKeyEvent(self):
		"""bind mouse click, press move and release event
		"""
		keyEventTable = [
			['<Button-1>'       , self._MouseLeftClickCallback  ],
			['<B1-Motion>'      , self._MousePressMoveCallback  ],
			['<ButtonRelease-1>', self._MouseLeftReleaseCallback],
			['<Key>'            , self._KeyboardAsciiCallback   ]
		]
		for [ev, cbFunc] in keyEventTable:
			self.m_view.m_cv.bind(ev, cbFunc)
		self.m_view.m_cv.focus_set()

	def _CbSelect(self):
		"""select button's callback func
		"""
		self.m_model.DisItemByDataOnce('M_BACK_WHITE', self.m_selectRowColData)
		self.m_selectRowColData = []
		self.m_model.DisableCursor()
		self.m_state = 'ST_SELECT'

	def _CbLines(self):
		"""draw line button's callback func
		"""
		self.m_model.DisItemByDataOnce('M_BACK_WHITE', self.m_selectRowColData)
		self.m_selectRowColData = []
		self.m_model.DisableCursor()
		self.m_state = 'ST_DRAW_LINES'

	def _CbLinesWithArrow(self):
		"""draw lines arrow button's callback func
		"""
		self.m_model.DisItemByDataOnce('M_BACK_WHITE', self.m_selectRowColData)
		self.m_selectRowColData = []
		self.m_model.DisableCursor()
		self.m_state = 'ST_DRAW_LINES_WITH_ARROW'

	def _CbLineRect(self):
		"""draw rect button's callback func
		"""
		self.m_model.DisItemByDataOnce('M_BACK_WHITE', self.m_selectRowColData)
		self.m_selectRowColData = []
		self.m_model.DisableCursor()
		self.m_state = 'ST_DRAW_LINE_RECT'

	def _CbText(self):
		"""write text button's callback func

		additional, you can use left, right, up, down and backspace to edit text
		"""
		self.m_model.DisItemByDataOnce('M_BACK_WHITE', self.m_selectRowColData)
		self.m_selectRowColData = []
		self.m_model.EnableCursor()
		self.m_state = 'ST_TEXT'

	def _CbDelRect(self):
		"""delete rect area button's callback func
		"""
		self.m_model.DisItemByDataOnce('M_BACK_WHITE', self.m_selectRowColData)
		self.m_selectRowColData = []
		self.m_model.DisableCursor()
		self.m_state = 'ST_DEL_RECT'

	def _MouseLeftClickCallback(self, event):
		"""mouse left click callback func

		i use state matchine. aa_statematchine.pdf is provide which give a detial description
		"""
		clickPos = self.m_view.XYToRowCol(event.x, event.y)
		if self.m_state == 'ST_SELECT':
			self.m_selectRectStartPos[0] = clickPos[0]
			self.m_selectRectStartPos[1] = clickPos[1]	
			self.m_state = 'ST_SELECT_SELECTING'
		elif self.m_state == 'ST_SELECT_SELECTED':
			if clickPos in [[r, c] for [r, c, ch] in self.m_selectRowColData]:
				self.m_dragMoveStart[0] = clickPos[0]
				self.m_dragMoveStart[1] = clickPos[1]
				self.m_model.DelItemByDataMiddle(self.m_selectRowColData)
				self.m_state = 'ST_SELECT_DRAGING'
			else:
				self.m_model.DisItemByDataOnce('M_BACK_WHITE', self.m_selectRowColData)
				self.m_selectRowColData = []
				self.m_selectRectStartPos[0] = clickPos[0]
				self.m_selectRectStartPos[1] = clickPos[1]
				self.m_state = 'ST_SELECT_SELECTING'
		elif self.m_state == 'ST_DRAW_LINES' or self.m_state == 'ST_DRAW_LINES_WITH_ARROW' or self.m_state == 'ST_DRAW_LINE_RECT' or self.m_state == 'ST_DEL_RECT':
			self.m_drawStartPos[0] = clickPos[0]
			self.m_drawStartPos[1] = clickPos[1]
		elif self.m_state == 'ST_TEXT':
			self.m_model.EnableCursor()
			self.m_model.SetCursor(clickPos[0], clickPos[1])			

	def _MousePressMoveCallback(self, event):
		"""mouse press move callback func.

		see left click callback func.
		"""
		if self.m_state == 'ST_SELECT_SELECTING':
			[r0, c0] = [self.m_selectRectStartPos[0], self.m_selectRectStartPos[1]]
			[r1, c1] = self.m_view.XYToRowCol(event.x, event.y)
			self.m_model.DisItemByDesContinue('M_FILLED_RECT_BLUE_ALPHA_100', [[r0, c0], [r1, c1]])
		elif self.m_state == 'ST_SELECT_DRAGING':
			[r1, c1] = self.m_view.XYToRowCol(event.x, event.y)
			detR = r1 - self.m_dragMoveStart[0]
			detC = c1 - self.m_dragMoveStart[1]
			tempSelectRowColData = [[r + detR, c + detC, ch] for [r, c, ch] in self.m_selectRowColData]
			self.m_model.DisItemByDataContinue('M_BACK_BLUE', tempSelectRowColData)
		elif self.m_state == 'ST_DRAW_LINES':
			[r1, c1] = self.m_view.XYToRowCol(event.x, event.y)
			self.m_model.DisItemByDesContinue('M_LINES', [self.m_drawStartPos, [r1, c1]])
		elif self.m_state == 'ST_DRAW_LINES_WITH_ARROW':
			[r1, c1] = self.m_view.XYToRowCol(event.x, event.y)
			self.m_model.DisItemByDesContinue('M_LINES_WITH_ARROW', [self.m_drawStartPos, [r1, c1]])
		elif self.m_state == 'ST_DRAW_LINE_RECT':
			[r1, c1] = self.m_view.XYToRowCol(event.x, event.y)
			self.m_model.DisItemByDesContinue('M_LINE_RECT', [self.m_drawStartPos, [r1, c1]])
		elif self.m_state == 'ST_DEL_RECT':
			[r1, c1] = self.m_view.XYToRowCol(event.x, event.y)
			self.m_model.DisItemByDesContinue('M_FILLED_RECT_BLUE_ALPHA_0', [self.m_drawStartPos, [r1, c1]])


	def _MouseLeftReleaseCallback(self, event):
		"""mouse left release callback func.

		see left click common.
		"""
		if self.m_state == 'ST_SELECT_SELECTING':
			[r0, c0] = [self.m_selectRectStartPos[0], self.m_selectRectStartPos[1]]
			[r1, c1] = self.m_view.XYToRowCol(event.x, event.y)
			self.m_selectRowColData = self.m_model.GetRectCharPosList([[r0, c0], [r1, c1]])
			self.m_model.DisItemByDataContinue('M_BACK_BLUE', self.m_selectRowColData)
			if (len(self.m_selectRowColData)):
				self.m_state = 'ST_SELECT_SELECTED'
			else:
				self.m_state = 'ST_SELECT'
		elif self.m_state == 'ST_SELECT_DRAGING':
			[r1, c1] = self.m_view.XYToRowCol(event.x, event.y)
			detR = r1 - self.m_dragMoveStart[0]
			detC = c1 - self.m_dragMoveStart[1]
			self.m_selectRowColData = [[r + detR, c + detC, ch] for [r, c, ch] in self.m_selectRowColData]
			self.m_model.AddItemByData(self.m_selectRowColData)
			self.m_state = 'ST_SELECT_SELECTED'
		elif self.m_state == 'ST_DRAW_LINES':
			[r1, c1] = self.m_view.XYToRowCol(event.x, event.y)
			self.m_model.AddItemByDes('M_LINES', [self.m_drawStartPos, [r1, c1]])
		elif self.m_state == 'ST_DRAW_LINES_WITH_ARROW':
			[r1, c1] = self.m_view.XYToRowCol(event.x, event.y)
			self.m_model.AddItemByDes('M_LINES_WITH_ARROW', [self.m_drawStartPos, [r1, c1]])
		elif self.m_state == 'ST_DRAW_LINE_RECT':
			[r1, c1] = self.m_view.XYToRowCol(event.x, event.y)
			self.m_model.AddItemByDes('M_LINE_RECT', [self.m_drawStartPos, [r1, c1]])
		elif self.m_state == 'ST_DEL_RECT':
			[r1, c1] = self.m_view.XYToRowCol(event.x, event.y)
			self.m_model.DelRectItemByDes([self.m_drawStartPos, [r1, c1]])
			self.m_model.DisItemByDesOnce('M_FILLED_RECT_WHITE_ALPHA_0', [self.m_drawStartPos, [r1, c1]])

	def _KeyboardAsciiCallback(self, event):
		"""keyboard callback func.

		you can type ascii char. and left, right, up, down, backspace is give out for convience
		"""
		if self.m_state == 'ST_TEXT':
			[row, col] = self.m_model.GetCursor()
			self.m_model.AddText(row, col, event.char, event.keycode)

	def _CbCreateFile(self):
		"""generate output file output.text

		you can edit this file later.
		"""
		self.m_model.CreateFile()


controler = Controler(80, 30)
controler.Start()