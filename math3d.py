# -*- coding: utf-8 -*-
import math
import traceback


class Vec2(object):
	__slots__ = ('x', 'y')

	def __init__(self, x=0.0, y=0.0):
		self.x = x
		self.y = y

	def __str__(self):
		return "({0}, {1})".format(self.x, self.y)

	def __repr__(self):
		return str(self)

	def __add__(self, other):
		return Vec2(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vec2(self.x - other.x, self.y - other.y)

	def __mul__(self, other):
		return Vec2(self.x * other, self.y * other)

	def cross2d(self, o):
		return self.x * o.y - self.y * o.x

	def dot2d(self, o):
		return self.x * o.x + self.y * o.y


class Vec3(object):
	__slots__ = ('x', 'y', 'z')

	def __init__(self, x=0.0, y=0.0, z=0.0):
		self.x = x
		self.y = y
		self.z = z

	def __str__(self):
		return "({0}, {1}, {2})".format(self.x, self.y, self.z)

	def __repr__(self):
		return str(self)

	def __add__(self, other):
		return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

	def __sub__(self, other):
		return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

	def __mul__(self, other):
		return Vec3(self.x * other, self.y * other, self.z * other)

	def __getitem__(self, item):
		if item == 0:
			return self.x
		elif item == 1:
			return self.y
		elif item == 2:
			return self.z

	def dot(self, other):
		return self.x * other.x + self.y * other.y + self.z * other.z

	def cross(self, v):
		return Vec3(self.y * v.z - self.z * v.y, self.z * v.x - self.x * v.z, self.x * v.y - self.y * v.x)

	def length(self):
		return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + 0.0)

	def normalize(self):
		inv_norm = 1.0 / self.length()
		self.x *= inv_norm
		self.y *= inv_norm
		self.z *= inv_norm
		return self


class Mat4x4(object):
	__slots__ = ['ele']

	def __init__(self, ele=None):
		if ele:
			self.ele = ele
		else:
			self.ele = [0] * 16

	def __getitem__(self, item):
		return self.ele[item]

	def __setitem__(self, key, value):
		self.ele[key] = value

	def get(self, i, j):
		return self.ele[i * 4 + j]

	def identity(self):
		self.ele = [0] * 16
		ele = self.ele
		ele[0] = ele[5] = ele[10] = ele[15] = 1
		return self

	def __mul__(self, o):
		new_ele = [0] * 16
		ele = self.ele
		o_ele = o.ele

		new_ele[0] = ele[0] * o_ele[0] + ele[1] * o_ele[4] + ele[2] * o_ele[8] + ele[3] * o_ele[12]
		new_ele[1] = ele[0] * o_ele[1] + ele[1] * o_ele[5] + ele[2] * o_ele[9] + ele[3] * o_ele[13]
		new_ele[2] = ele[0] * o_ele[2] + ele[1] * o_ele[6] + ele[2] * o_ele[10] + ele[3] * o_ele[14]
		new_ele[3] = ele[0] * o_ele[3] + ele[1] * o_ele[7] + ele[2] * o_ele[11] + ele[3] * o_ele[15]

		new_ele[4] = ele[4] * o_ele[0] + ele[5] * o_ele[4] + ele[6] * o_ele[8] + ele[7] * o_ele[12]
		new_ele[5] = ele[4] * o_ele[1] + ele[5] * o_ele[5] + ele[6] * o_ele[9] + ele[7] * o_ele[13]
		new_ele[6] = ele[4] * o_ele[2] + ele[5] * o_ele[6] + ele[6] * o_ele[10] + ele[7] * o_ele[14]
		new_ele[7] = ele[4] * o_ele[3] + ele[5] * o_ele[7] + ele[6] * o_ele[11] + ele[7] * o_ele[15]

		new_ele[8] = ele[8] * o_ele[0] + ele[9] * o_ele[4] + ele[10] * o_ele[8] + ele[11] * o_ele[12]
		new_ele[9] = ele[8] * o_ele[1] + ele[9] * o_ele[5] + ele[10] * o_ele[9] + ele[11] * o_ele[13]
		new_ele[10] = ele[8] * o_ele[2] + ele[9] * o_ele[6] + ele[10] * o_ele[10] + ele[11] * o_ele[14]
		new_ele[11] = ele[8] * o_ele[3] + ele[9] * o_ele[7] + ele[10] * o_ele[11] + ele[11] * o_ele[15]

		new_ele[12] = ele[12] * o_ele[0] + ele[13] * o_ele[4] + ele[14] * o_ele[8] + ele[15] * o_ele[12]
		new_ele[13] = ele[12] * o_ele[1] + ele[13] * o_ele[5] + ele[14] * o_ele[9] + ele[15] * o_ele[13]
		new_ele[14] = ele[12] * o_ele[2] + ele[13] * o_ele[6] + ele[14] * o_ele[10] + ele[15] * o_ele[14]
		new_ele[15] = ele[12] * o_ele[3] + ele[13] * o_ele[7] + ele[14] * o_ele[11] + ele[15] * o_ele[15]

		return Mat4x4(new_ele)

	def mul_vec3(self, v3):
		ele = self.ele
		v3x = v3.x
		v3y = v3.y
		v3z = v3.z
		x = ele[0] * v3x + ele[1] * v3y + ele[2] * v3z + ele[3]
		y = ele[4] * v3x + ele[5] * v3y + ele[6] * v3z + ele[7]
		z = ele[8] * v3x + ele[9] * v3y + ele[10] * v3z + ele[11]
		w = ele[12] * v3x + ele[13] * v3y + ele[14] * v3z + ele[15]
		if w == 0:
			traceback.print_stack()
			print('w error')
			return Vec3(math.inf, math.inf, math.inf)
		else:
			return Vec3(x / w, y / w, z / w)


def look_at(eye: Vec3, center: Vec3, up: Vec3):
	z = (eye - center).normalize()
	x = up.cross(z).normalize()
	y = z.cross(x).normalize()
	view = Mat4x4().identity()
	tr = Mat4x4().identity()
	for i in range(3):
		view[i] = x[i]
		view[4 + i] = y[i]
		view[8 + i] = z[i]
		tr[i * 4 + 3] = center[i] - eye[i]
	return tr * view


def perspective(fov, ratio, near, far):
	mat = Mat4x4()
	mat[5] = 1.0 / math.tan(fov * 0.5)
	mat[0] = mat[5] / ratio
	mat[10] = far / (far - near)
	mat[14] = far * near / (near - far)
	mat[11] = 1
	return mat


def viewport(w, h):
	mat = Mat4x4().identity()
	mat[3] = w * 0.5
	mat[7] = h * 0.5
	mat[11] = 127.5
	mat[0] = w * 0.5
	mat[5] = h * 0.5
	mat[10] = 127.5
	return mat
