# -*- coding: utf-8 -*-
import math


class Vec2(object):
	__slots__ = ('x', 'y')

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

	def cross2d(self, o):
		return self.x * o.y - self.y * o.x

	def dot2d(self, o):
		return self.x * o.x + self.y * o.y


class Vec3(object):
	__slots__ = ('x', 'y', 'z')

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

	def length(self):
		return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + 0.0)

	def normalize(self):
		inv_norm = 1.0 / self.length()
		self.x *= inv_norm
		self.y *= inv_norm
		self.z *= inv_norm
