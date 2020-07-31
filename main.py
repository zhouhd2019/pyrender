# -*- coding: utf-8 -*-
import random
import math
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt
from PIL import Image
import main_ui
import pyrender
import model
import math3d
from math3d import Vec2, Vec3, Mat4x4
import pipeline


class MainWnd(QtWidgets.QWidget):

	def __init__(self):
		super().__init__()
		self.ui = main_ui.Ui_Form()
		self.ui.setupUi(self)
		self.setWindowTitle("render")
		palette = QtGui.QPalette()
		palette.setColor(self.backgroundRole(), Qt.black)
		self.setPalette(palette)
		self.setAutoFillBackground(True)
		self.show()

	def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
		qp = QPainter()
		qp.begin(self)
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
		# self.lesson_3(qp)
		# self.lesson_4(qp)
		# self.lesson_6_1(qp)
		# self.lesson_6_2(qp)
		# self.lesson_6_3(qp)
		# self.lesson_7(qp)
		self.lesson_8(qp)

	def lesson_8(self, qp: QPainter):
		size, width, height, zbuffer = self.init(qp)

		view_pos = Vec3(1.5, 1, 1.5)
		origin = Vec3(0, 0, 0)
		up = Vec3(0, 1, 0)
		proj_mat = math3d.perspective(1.5, 4.0 / 3, 1.0, -1.0)
		vp = math3d.viewport(width, height)
		view_mat = math3d.look_at(view_pos, origin, up)
		mvpvp = vp * proj_mat * view_mat

		m = model.Model()
		m.read_from_file('./obj/african_head.obj')

		shader = pipeline.L8AmbientOcclusion(m, mvpvp, qp, zbuffer, width, height)
		shader.render()

	def lesson_7(self, qp: QPainter):
		size, width, height, zbuffer = self.init(qp)

		light_pos = Vec3(1.5, 1.5, 1.5)
		view_pos = Vec3(0, 0, 2.5)
		origin = Vec3(0, 0, 0)
		up = Vec3(0, 1, 0)

		view_mat = math3d.look_at(light_pos, origin, up)
		proj_mat = math3d.perspective(1.5, 4.0 / 3, 1.0, -1.0)
		vp = math3d.viewport(width, height)
		mvpvp_shadow = vp * proj_mat * view_mat

		view_mat = math3d.look_at(view_pos, origin, up)
		mvpvp = vp * proj_mat * view_mat

		m = model.Model()
		m.read_from_file('./obj/african_head.obj', diffuse_file='./obj/african_head_diffuse.tga',
						 normal_file='./obj/african_head_nm_tangent.tga',
						 specular_file='./obj/african_head_spec.tga')

		shader = pipeline.L7ShadowMapping(m, light_pos, mvpvp_shadow, mvpvp, view_pos, qp, zbuffer, width, height)
		shader.render()

	def lesson_6_3(self, qp: QPainter):
		size, width, height, zbuffer = self.init(qp)

		view_pos = Vec3(0, 0, 2.5)
		view_mat = math3d.look_at(view_pos, Vec3(0, 0, 0), Vec3(0, 1, 0))
		proj_mat = math3d.perspective(1.5, 4.0 / 3, 1.0, -1.0)
		vp = math3d.viewport(width, height)
		mvpvp = vp * proj_mat * view_mat

		m = model.Model()
		m.read_from_file('./obj/african_head.obj', diffuse_file='./obj/african_head_diffuse.tga',
						normal_file='./obj/african_head_nm_tangent.tga',
						specular_file='./obj/african_head_spec.tga')

		light_dir = Vec3(0, 0, 1)

		shader = pipeline.L63Specular(m, light_dir, mvpvp, view_pos, qp, zbuffer, width, height)
		shader.render()

	def lesson_6_2(self, qp: QPainter):
		size, width, height, zbuffer = self.init(qp)

		view_mat = math3d.look_at(Vec3(0, 0, 2.5), Vec3(0, 0, 0), Vec3(0, 1, 0))
		proj_mat = math3d.perspective(1.5, 4.0 / 3, 1.0, -1.0)
		vp = math3d.viewport(width, height)
		mvpvp = vp * proj_mat * view_mat

		m = model.Model()
		m.read_from_file('./obj/african_head.obj', diffuse_file='./obj/african_head_diffuse.tga',
						normal_file='./obj/african_head_nm_tangent.tga')

		light_dir = Vec3(0, 0, 1)

		shader = pipeline.L62NormalMapping(m, light_dir, mvpvp, qp, zbuffer, width, height)
		shader.render()

	def lesson_6_1(self, qp: QPainter):
		size, width, height, zbuffer = self.init(qp)

		# model_mat = Mat4x4()
		# model_mat.identity()
		view_mat = math3d.look_at(Vec3(0, 0, 4), Vec3(0, 0, 0), Vec3(0, 1, 0))
		proj_mat = math3d.perspective(1.05, 4.0 / 3, 1.0, -1.0)
		vp = math3d.viewport(width, height)
		mvpvp = vp * proj_mat * view_mat

		m = model.Model()
		m.read_from_file('./obj/african_head.obj', diffuse_file='./obj/african_head_diffuse.tga')

		light_dir = Vec3(0, 0, 1)

		shader = pipeline.L61GouraudShader(m, light_dir, mvpvp, qp, zbuffer, width, height)
		shader.render()

	def lesson_4(self, qp: QPainter):
		size, width, height, zbuffer = self.init(qp)

		# model_mat = Mat4x4()
		# model_mat.identity()
		view_mat = math3d.look_at(Vec3(0, 0, 4), Vec3(0, 0, 0), Vec3(0, 1, 0))
		proj_mat = math3d.perspective(1.05, 4.0 / 3, 1.0, -1.0)
		vp = math3d.viewport(width, height)
		mvpvp = vp * proj_mat * view_mat

		m = model.Model()
		m.read_from_file('./obj/african_head.obj')
		tex = Image.open('./obj/african_head_diffuse.tga')
		tex = tex.transpose(Image.FLIP_TOP_BOTTOM)

		light_dir = Vec3(0, 0, 1)

		triangle = pyrender.triangle4
		for i in range(len(m.faces)):
			triangle(m, i, mvpvp, width, height, zbuffer, qp, light_dir, tex)

	def lesson_3(self, qp: QPainter):
		size, width, height, zbuffer = self.init(qp)

		half_width = int(width * 0.5)
		half_height = int(height * 0.5)
		scale = min(half_height, half_width) + 0.0

		m = model.Model()
		m.read_from_file('./obj/african_head.obj')
		tex = Image.open('./obj/african_head_diffuse.tga')
		tex = tex.transpose(Image.FLIP_TOP_BOTTOM)

		light_dir = Vec3(0, 0, 1)

		triangle = pyrender.triangle3
		for i in range(len(m.faces)):
			triangle(m, i, scale, zbuffer, qp, (width, height), light_dir, tex)

	def init(self, qp: QPainter):
		size = self.size()
		width = size.width()
		height = size.height()
		qp.translate(0, height)
		qp.scale(1, -1)
		zbuffer = [-9999] * ((width + 1) * (height + 1))
		return size, width, height, zbuffer

	def lesson_2_2(self, qp: QPainter) -> None:
		size = self.size()
		width = size.width()
		height = size.height()
		qp.translate(width * 0.5, height * 0.5)
		qp.scale(1, -1)

		half_width = int(width * 0.5)
		half_height = int(height * 0.5)
		scale = min(half_height, half_width) + 0.0

		m = model.Model()
		m.read_from_file('./obj/african_head.obj')

		light_dir = Vec3(0, 0, 1)

		triangle = pyrender.triangle2
		for i in range(len(m.faces)):
			face = m.faces[i]
			pt0 = m.verts[face[0][0]] * scale
			pt1 = m.verts[face[1][0]] * scale
			pt2 = m.verts[face[2][0]] * scale

			p01 = pt1 - pt0
			p02 = pt2 - pt0
			normal = p01.cross(p02)
			normal.normalize()
			intensity = normal.dot(light_dir)
			if intensity < 0:
				continue
			c = int(255 * intensity)
			qp.setPen(QColor(c, c, c))
			triangle(pt0, pt1, pt2, qp, (half_width, half_height))

	def lesson_2_1(self, qp: QPainter) -> None:
		size = self.size()
		width = size.width()
		height = size.height()
		qp.translate(width * 0.5, height * 0.5)
		qp.scale(1, -1)

		qp.setPen(Qt.blue)
		pt0 = Vec2(0, 0)
		pt1 = Vec2(-200, 0)
		pt2 = Vec2(0, 100)

		half_width = int(width * 0.5)
		half_height = int(height * 0.5)
		pyrender.triangle2(pt0, pt1, pt2, qp, (half_width, half_height))

	def lesson_1(self, qp: QPainter):
		size = self.size()
		width = size.width()
		height = size.height()
		qp.translate(width * 0.5, height * 0.5)
		qp.scale(1, -1)
		qp.setPen(Qt.blue)

		half_width = int(width * 0.5)
		half_height = int(height * 0.5)
		scale = min(half_height, half_width) + 0.0

		m = model.Model()
		m.read_from_file('./obj/african_head.obj')

		line = pyrender.line
		verts = m.verts
		for face in m.faces:
			for i in range(3):
				v0 = verts[face[i][0]]
				v1 = verts[face[(i + 1) % 3][0]]
				v0 = v0 * scale
				v1 = v1 * scale
				line(v0.x, v0.y, v1.x, v1.y, qp)


if __name__ == '__main__':
	NO_PROFILE = 1
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
