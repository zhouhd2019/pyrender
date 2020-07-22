# -*- coding: utf-8 -*-
import random
import math
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt
import main_ui
import pyrender
import model
import math3d
from math3d import Vec2, Vec3


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
		try:
			self.draw(qp)
		except:
			import traceback
			traceback.print_exc()
			traceback.print_stack()
		qp.end()

	def draw(self, qp: QPainter) -> None:
		# self.lesson_1(qp)
		# self.lesson_2_1(qp)
		# self.lesson_2_2(qp)
		self.lesson_3(qp)

	def lesson_3(self, qp: QPainter):
		size = self.size()
		width = size.width()
		height = size.height()
		half_width = int(width * 0.5)
		half_height = int(height * 0.5)
		scale = min(half_height, half_width)
		zbuffer = [-9999] * (width * height)

		m = model.Model()
		m.read_from_file('./obj/african_head.obj')

		light_dir = Vec3(0, 0, -1)

		triangle = pyrender.triangle_by_barycentric
		for i in range(len(m.faces)):
			face = m.faces[i]
			pt0 = m.verts[face[0]] * scale
			pt1 = m.verts[face[1]] * scale
			pt2 = m.verts[face[2]] * scale

			p01 = pt1 - pt0
			p02 = pt2 - pt0
			normal = p02.cross(p01)
			normal.normalize()
			intensity = normal.dot(light_dir)
			if intensity < 0:
				continue
			c = int(255 * intensity)
			qp.setPen(QColor(c, c, c))
			triangle(pt0, pt1, pt2, zbuffer, qp, (half_width, half_height))

	def lesson_2_2(self, qp: QPainter) -> None:
		size = self.size()
		width = size.width()
		height = size.height()
		half_width = int(width * 0.5)
		half_height = int(height * 0.5)
		scale = min(half_height, half_width)

		m = model.Model()
		m.read_from_file('./obj/african_head.obj')

		light_dir = Vec3(0, 0, -1)

		triangle = pyrender.triangle
		for i in range(len(m.faces)):
			face = m.faces[i]
			pt0 = m.verts[face[0]] * scale
			pt1 = m.verts[face[1]] * scale
			pt2 = m.verts[face[2]] * scale

			p01 = pt1 - pt0
			p02 = pt2 - pt0
			normal = p02.cross(p01)
			normal.normalize()
			intensity = normal.dot(light_dir)
			if intensity < 0:
				continue
			c = int(255 * intensity)
			qp.setPen(QColor(c, c, c))
			triangle(pt0, pt1, pt2, qp, (half_width, half_height))

	def lesson_2_1(self, qp: QPainter) -> None:
		qp.setPen(Qt.blue)
		pt0 = Vec2(0, 0)
		pt1 = Vec2(-200, 0)
		pt2 = Vec2(0, 100)
		size = self.size()
		width = size.width()
		height = size.height()
		half_width = int(width * 0.5)
		half_height = int(height * 0.5)
		pyrender.triangle(pt0, pt1, pt2, qp, (half_width, half_height))

	def lesson_1(self, qp: QPainter):
		qp.setPen(Qt.blue)
		size = self.size()
		width = size.width()
		height = size.height()
		half_width = int(width * 0.5)
		half_height = int(height * 0.5)
		scale = min(half_height, half_width)

		m = model.Model()
		m.read_from_file('./obj/african_head.obj')

		line = pyrender.line
		verts = m.verts
		for face in m.faces:
			for i in range(3):
				v0 = verts[face[i]]
				v1 = verts[face[(i + 1) % 3]]
				v0 = v0 * scale
				v1 = v1 * scale
				line(v0.x, v0.y, v1.x, v1.y, qp)


if __name__ == '__main__':
	NO_PROFILE = 0
	if NO_PROFILE:
		app = QtWidgets.QApplication(sys.argv)
		wnd = MainWnd()
		sys.exit(app.exec_())
	else:
		import cProfile, pstats, io
		pr = cProfile.Profile()
		pr.enable()

		app = QtWidgets.QApplication(sys.argv)
		wnd = MainWnd()
		exit_code = app.exec_()

		pr.disable()
		s = io.StringIO()
		ps = pstats.Stats(pr, stream=s).sort_stats(pstats.SortKey.CUMULATIVE)
		# ps.dump_stats(r"F:\githubdesktop\pyrender\prof.prof")
		ps.print_stats()
		print(s.getvalue())

		sys.exit(exit_code)
