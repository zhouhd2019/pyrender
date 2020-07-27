# -*- coding: utf-8 -*-
import math3d
from math3d import Vec3, Vec2
from PIL import Image


class Model(object):
	def __init__(self):
		self.verts = [Vec3(), ]
		self.vtex = [Vec2(), ]
		self.vnorm = [Vec3(), ]

		self.faces = []
		self.face_norms_cache = {}

		self.diffuse_tex = None

	def vert_uv_normal_by_face(self, iface, nth_vert):
		info = self.faces[iface][nth_vert]
		return self.verts[info[0]], self.vtex[info[1]], self.vnorm[info[2]]

	def face_normal(self, iface):
		if iface in self.face_norms_cache:
			return self.face_norms_cache[iface]
		face = self.faces[iface]
		pt0 = self.verts[face[0][0]]
		pt1 = self.verts[face[1][0]]
		pt2 = self.verts[face[2][0]]
		p01 = pt1 - pt0
		p02 = pt2 - pt0
		normal = p01.cross(p02)
		normal.normalize()
		self.face_norms_cache[iface] = normal
		return normal

	def diffuse(self, u, v):
		tex_width, tex_height = self.diffuse_tex.size
		return self.diffuse_tex.getpixel((u * tex_width, v * tex_height))

	def __str__(self):
		return "'verts: {}, faces: {}".format(len(self.verts), len(self.faces))

	def read_from_file(self, model_file_name, diffuse_file_name=None):
		with open(model_file_name, 'r') as f:
			try:
				words = []
				for line in f:
					words = line.split()
					if words and words[0] in MODEL_READ_FUNC:
						MODEL_READ_FUNC[words[0]](self, words)
			except:
				import traceback
				traceback.print_exc()
				print('error: ', line)
				print('words: ', words)

		if diffuse_file_name:
			tex = Image.open(diffuse_file_name)
			self.diffuse_tex = tex.transpose(Image.FLIP_TOP_BOTTOM)

	def read_face(self, words):
		verts = []
		for w in words[1:]:
			v, vt, vn = w.split('/')[:3]
			verts.append((int(v), int(vt), int(vn)))
		self.faces.append(verts)


MODEL_READ_FUNC = {
	'v': lambda self, words: self.verts.append(Vec3(float(words[1]), float(words[2]), float(words[3]))),
	'f': Model.read_face,
	'vt': lambda self, words: self.vtex.append(Vec2(float(words[1]), float(words[2]))),
	'vn': lambda self, words: self.vnorm.append(Vec3(float(words[1]), float(words[2]), float(words[3]))),
}


TEST_TRIANGLE = Model()
TEST_TRIANGLE.verts = [Vec3(), Vec3(0, 0, 0), Vec3(1, 0, 0), Vec3(0, 1, 0)]
TEST_TRIANGLE.vtex = [Vec2(), Vec2(0, 0), Vec2(1, 0), Vec2(0, 1)]
TEST_TRIANGLE.faces = [((1, 1), (2, 2), (3, 3))]


if __name__ == '__main__':
	m = Model()
	m.read_from_file('./obj/african_head.obj')
	print('verts ', len(m.verts), ' faces ', len(m.faces))
