# -*- coding: utf-8 -*-
import math


class Vec2(object):
	def __init__(self, x=0, y=0):
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

	@property
	def u(self):
		return self.x

	@u.setter
	def u(self, value):
		self.x = value

	@property
	def v(self):
		return self.y

	@v.setter
	def v(self, value):
		self.y = value


class Vec3(object):
	def __init__(self, x=0, y=0, z=0):
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

	def dot(self, other):
		return self.x * other.x + self.y * other.y + self.z * other.z

	def cross(self, v):
		return Vec3(self.y * v.z - self.z * v.y, self.z * v.x - self.x * v.z, self.x * v.y - self.y * v.x)

	def norm(self):
		return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + 0.0)

	def normalize(self):
		inv_norm = 1.0 / self.norm()
		self.x *= inv_norm
		self.y *= inv_norm
		self.z *= inv_norm

	@property
	def ivert(self):
		return self.x

	@ivert.setter
	def ivert(self, value):
		self.x = value

	@property
	def iuv(self):
		return self.y

	@iuv.setter
	def iuv(self, value):
		self.y = value

	@property
	def inorm(self):
		return self.z

	@inorm.setter
	def inorm(self, value):
		self.z = value
