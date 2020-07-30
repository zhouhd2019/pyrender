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

		triangle = pyrender.triangle6
		fragment = self.fragment
		for i in range(len(self.model.faces)):
			for j in range(3):
				screen_coords[j] = self.vertex(i, j)
			triangle(screen_coords, fragment, qp, zbuffer, size)

	def vertex(self, iface: int, nth_vert: int):
		vert, uv, normal = self.model.vert_uv_normal_by_face(iface, nth_vert)
		self.uv[nth_vert] = uv
		self.intensity[nth_vert] = max(0.0, normal.dot(self.light_dir))
		return self.mvpvp.mul_vec3(vert)

	def fragment(self, barycentric):
		uv = self.uv[0] * barycentric.x + self.uv[1] * barycentric.y + self.uv[2] * barycentric.z
		diffuse = self.model.diffuse(uv.x, uv.y)
		intensity = self.intensity.dot(barycentric)
		return True, diffuse * intensity


class L62NormalMapping(object):
	def __init__(self, model, light_dir, mvpvp: Mat4x4, qp: QPainter, zbuffer: List[float], width, height):
		self.model = model
		self.light_dir = light_dir
		self.mvpvp = mvpvp
		self.qp = qp
		self.zbuffer = zbuffer
		self.size = (width, height)

		self.uv = [Vec2(), Vec2(), Vec2()]
		self.tangentLightDir = [Vec3(), Vec3(), Vec3()]

	def render(self):
		screen_coords = [Vec3(), Vec3(), Vec3()]
		qp = self.qp
		zbuffer = self.zbuffer
		size = self.size

		triangle = pyrender.triangle6
		fragment = self.fragment
		for i in range(len(self.model.faces)):
			for j in range(3):
				screen_coords[j] = self.vertex(i, j)
			triangle(screen_coords, fragment, qp, zbuffer, size)

	def vertex(self, iface: int, nth_vert: int):
		vert, uv, normal = self.model.vert_uv_normal_by_face(iface, nth_vert)
		self.uv[nth_vert] = uv

		tangent = self.model.face_tangent[iface]
		tangent = tangent - normal * tangent.dot(normal)
		tangent.normalize()
		bitangent = normal.cross(tangent)

		tbn = Mat4x4().mat_by_col(tangent, bitangent, normal).transpose()
		self.tangentLightDir[nth_vert] = tbn.mul_vec3(self.light_dir).normalize()

		return self.mvpvp.mul_vec3(vert)

	def fragment(self, barycentric):
		uv = self.uv
		uv = uv[0] * barycentric.x + uv[1] * barycentric.y + uv[2] * barycentric.z
		light = self.tangentLightDir
		light = light[0] * barycentric.x + light[1] * barycentric.y + light[2] * barycentric.z
		light.normalize()

		normal = self.model.normal_map(uv.x, uv.y)
		intensity = max(0.0, normal.dot(light))
		diffuse = self.model.diffuse(uv.x, uv.y)
		return True, diffuse * intensity


class L63Specular(object):
	def __init__(self, model, light_dir, mvpvp: Mat4x4, view_pos: Vec3, qp: QPainter,
				 zbuffer: List[float], width, height):
		self.model = model
		self.light_dir = light_dir
		self.mvpvp = mvpvp
		self.view_pos = view_pos
		self.qp = qp
		self.zbuffer = zbuffer
		self.size = (width, height)

		self.uv = [Vec2(), Vec2(), Vec2()]
		self.tangentLightDir = [Vec3(), Vec3(), Vec3()]
		self.tangentFragPos = [Vec3(), Vec3(), Vec3()]
		self.tangentViewPos = [Vec3(), Vec3(), Vec3()]

	def render(self):
		screen_coords = [Vec3(), Vec3(), Vec3()]
		qp = self.qp
		zbuffer = self.zbuffer
		size = self.size

		triangle = pyrender.triangle6
		fragment = self.fragment
		for i in range(len(self.model.faces)):
			for j in range(3):
				screen_coords[j] = self.vertex(i, j)
			triangle(screen_coords, fragment, qp, zbuffer, size)

	def vertex(self, iface: int, nth_vert: int):
		vert, uv, normal = self.model.vert_uv_normal_by_face(iface, nth_vert)
		self.uv[nth_vert] = uv

		tangent = self.model.face_tangent[iface]
		tangent = tangent - normal * tangent.dot(normal)
		tangent.normalize()
		bitangent = normal.cross(tangent)

		tbn = Mat4x4().mat_by_col(tangent, bitangent, normal).transpose()
		self.tangentLightDir[nth_vert] = tbn.mul_vec3(self.light_dir).normalize()
		self.tangentFragPos[nth_vert] = tbn.mul_vec3(vert)
		self.tangentViewPos[nth_vert] = tbn.mul_vec3(self.view_pos)

		return self.mvpvp.mul_vec3(vert)

	def fragment(self, barycentric):
		uv = self.uv
		uv = uv[0] * barycentric.x + uv[1] * barycentric.y + uv[2] * barycentric.z

		light = self.tangentLightDir
		light = light[0] * barycentric.x + light[1] * barycentric.y + light[2] * barycentric.z
		light.normalize()

		frag_pos = self.tangentFragPos
		frag_pos = frag_pos[0] * barycentric.x + frag_pos[1] * barycentric.y + frag_pos[2] * barycentric.z

		view_pos = self.tangentViewPos
		view_pos = view_pos[0] * barycentric.x + view_pos[1] * barycentric.y + view_pos[2] * barycentric.z

		n = self.model.normal_map(uv.x, uv.y)
		intensity = max(0.0, n.dot(light))
		diffuse = self.model.diffuse(uv.x, uv.y)

		view = view_pos - frag_pos
		view.normalize()
		h = (light + view).normalize()
		spec = pow(max(n.dot(h), 0), self.model.specular(uv.x, uv.y))

		result = Vec3()
		result.x = min(10 + diffuse.x * (intensity + spec * 0.6), 255)
		result.y = min(10 + diffuse.y * (intensity + spec * 0.6), 255)
		result.z = min(10 + diffuse.z * (intensity + spec * 0.6), 255)
		return True, result


class L7ShadowMapping(object):
	def __init__(self, model, light_pos, mvpvp_shadow: Mat4x4, mvpvp: Mat4x4, view_pos: Vec3, qp: QPainter,
				 zbuffer: List[float], width, height):
		self.model = model
		self.light_pos = light_pos
		self.mvpvp_shadow = mvpvp_shadow
		self.mvpvp = mvpvp
		self.view_pos = view_pos
		self.qp = qp
		self.zbuffer = zbuffer
		self.size = (width, height)

		self.depth = [0, 0, 0]
		self.shadow_map = [-9999] * ((width + 1) * (height + 1))

		self.uv = [Vec2(), Vec2(), Vec2()]
		self.shadowPos = [Vec3(), Vec3(), Vec3()]
		self.tangentLightPos = [Vec3(), Vec3(), Vec3()]
		self.tangentFragPos = [Vec3(), Vec3(), Vec3()]
		self.tangentViewPos = [Vec3(), Vec3(), Vec3()]

	def render(self):
		self.render_shadow()
		self.reset()
		self.render_scene()

	def render_shadow(self):
		screen_coords = [Vec3(), Vec3(), Vec3()]
		qp = self.qp
		zbuffer = self.zbuffer
		size = self.size
		width, height = size
		shadow_map = self.shadow_map

		def draw_shadow_pixel(x, y, color: int):
			shadow_map[x + y * width] = color
			# qp.setPen(QColor(color, color, color))
			# qp.drawPoint(x, y)

		triangle = pyrender.triangle64
		fragment = self.fragment_shadow
		for i in range(len(self.model.faces)):
			for j in range(3):
				screen_coords[j] = self.vertex_shadow(i, j)
			triangle(screen_coords, fragment, draw_shadow_pixel, zbuffer, size)

	def vertex_shadow(self, iface: int, nth_vert: int):
		vert, uv, normal = self.model.vert_uv_normal_by_face(iface, nth_vert)
		pt = self.mvpvp_shadow.mul_vec3(vert)
		self.depth[nth_vert] = pt.z
		return pt

	def fragment_shadow(self, barycentric):
		depth = self.depth
		depth = depth[0] * barycentric.x + depth[1] * barycentric.y + depth[2] * barycentric.z
		depth = max(0, min(255, depth))
		return True, depth

	def reset(self):
		self.zbuffer = [-9999] * ((self.size[0] + 1) * (self.size[1] + 1))

	def render_scene(self):
		screen_coords = [Vec3(), Vec3(), Vec3()]
		qp = self.qp
		zbuffer = self.zbuffer
		size = self.size

		def draw_pixel(x, y, color: Vec3):
			qp.setPen(QColor(color.x, color.y, color.z))
			qp.drawPoint(x, y)

		triangle = pyrender.triangle64
		fragment = self.fragment
		for i in range(len(self.model.faces)):
			for j in range(3):
				screen_coords[j] = self.vertex(i, j)
			triangle(screen_coords, fragment, draw_pixel, zbuffer, size)

	def vertex(self, iface: int, nth_vert: int):
		vert, uv, normal = self.model.vert_uv_normal_by_face(iface, nth_vert)
		self.uv[nth_vert] = uv

		tangent = self.model.face_tangent[iface]
		tangent = tangent - normal * tangent.dot(normal)
		tangent.normalize()
		bitangent = normal.cross(tangent)
		tbn = Mat4x4().mat_by_col(tangent, bitangent, normal).transpose()

		self.tangentLightPos[nth_vert] = tbn.mul_vec3(self.light_pos)
		self.tangentFragPos[nth_vert] = tbn.mul_vec3(vert)
		self.tangentViewPos[nth_vert] = tbn.mul_vec3(self.view_pos)

		self.shadowPos[nth_vert] = self.mvpvp_shadow.mul_vec3(vert)

		return self.mvpvp.mul_vec3(vert)

	def fragment(self, barycentric):
		uv = self.uv
		uv = uv[0] * barycentric.x + uv[1] * barycentric.y + uv[2] * barycentric.z

		light_pos = self.tangentLightPos
		light_pos = light_pos[0] * barycentric.x + light_pos[1] * barycentric.y + light_pos[2] * barycentric.z

		frag_pos = self.tangentFragPos
		frag_pos = frag_pos[0] * barycentric.x + frag_pos[1] * barycentric.y + frag_pos[2] * barycentric.z
		light = light_pos - frag_pos
		light.normalize()

		view_pos = self.tangentViewPos
		view_pos = view_pos[0] * barycentric.x + view_pos[1] * barycentric.y + view_pos[2] * barycentric.z

		shadow_pos = self.shadowPos
		shadow_pos = shadow_pos[0] * barycentric.x + shadow_pos[1] * barycentric.y + shadow_pos[2] * barycentric.z
		shadow_idx = int(shadow_pos.x) + int(shadow_pos.y) * self.size[0]
		if self.shadow_map[shadow_idx] - 15 > shadow_pos.z:
			shadow = 0.2
		else:
			shadow = 1

		n = self.model.normal_map(uv.x, uv.y)
		intensity = max(0.0, n.dot(light))
		diffuse = self.model.diffuse(uv.x, uv.y)

		view = view_pos - frag_pos
		view.normalize()
		h = (light + view).normalize()
		spec = pow(max(n.dot(h), 0), self.model.specular(uv.x, uv.y))

		result = Vec3()
		result.x = min(10 + diffuse.x * (intensity + spec * 0.6) * shadow, 255)
		result.y = min(10 + diffuse.y * (intensity + spec * 0.6) * shadow, 255)
		result.z = min(10 + diffuse.z * (intensity + spec * 0.6) * shadow, 255)
		return True, result
