# -*- coding: utf-8 -*-
from typing import List, Tuple
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt
from PIL import Image
import math3d
from math3d import Vec2, Vec3, Mat4x4, Vec4
import pyrender


class L61GouraudShader(object):
	def __init__(self, model, light_dir, mvpvp: Mat4x4, qp: QPainter, zbuffer: List[float], width, height):
		self.model = model
		self.light_dir = light_dir
		self.mvpvp = mvpvp
		self.qp = qp
		self.zbuffer = zbuffer
		self.size = (width, height)

		self.intensity = Vec3()
		self.uv = [Vec2(), Vec2(), Vec2()]

	def render(self):
		screen_coords = [Vec3(), Vec3(), Vec3()]
		qp = self.qp
		zbuffer = self.zbuffer
		size = self.size

		triangle = pyrender.triangle61
		for i in range(len(self.model.faces)):
			for j in range(3):
				screen_coords[j] = self.vertex(i, j)
			triangle(screen_coords, self, qp, zbuffer, size)

	def vertex(self, iface: int, nth_vert: int):
		vert, uv, normal = self.model.vert_uv_normal_by_face(iface, nth_vert)
		self.uv[nth_vert] = uv
		self.intensity[nth_vert] = max(0.0, normal.dot(self.light_dir))
		return self.mvpvp.mul_vec3(vert)

	def fragment(self, barycentric):
		uv = self.uv[0] * barycentric.x + self.uv[1] * barycentric.y + self.uv[2] * barycentric.z
		diffuse = self.model.diffuse(uv.x, uv.y)
		intensity = self.intensity.dot(barycentric)
		return True, [i * intensity for i in diffuse]
