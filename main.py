# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
import main_ui
import pyrender
import model


class MainWnd(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.ui = main_ui.Ui_Form()
		self.ui.setupUi(self)
		self.setWindowTitle("render")
		self.show()

	def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
		qp = QPainter()
		qp.begin(self)
		size = self.size()
		width = size.width()
		height = size.height()
		qp.translate(width * 0.5, height * 0.5)
		qp.scale(1, -1)
		self.draw(qp)
		qp.end()

	def draw(self, qp: QPainter) -> None:
		self.lesson_1(qp)

	def lesson_1(self, qp: QPainter):
		qp.setPen(Qt.blue)
		size = self.size()
		width = size.width()
		height = size.height()
		half_width = width * 0.5
		half_height = height * 0.5
		scale = min(half_height, half_width)

		m = model.Model()
		m.read_from_file('./obj/african_head.obj')

		line = pyrender.line
		verts = m.verts
		for face in m.faces:
			for i in range(3):
				v0 = verts[face[i]]
				v1 = verts[face[(i + 1) % 3]]
				x0 = v0.x * scale
				y0 = v0.y * scale
				x1 = v1.x * scale
				y1 = v1.y * scale
				line(x0, y0, x1, y1, qp)


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	wnd = MainWnd()
	sys.exit(app.exec_())
