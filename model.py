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
		self.face_tangent = {}

		self.diffuse_tex = None
		self.normal_tex = None

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
		pix = self.diffuse_tex.getpixel((u * tex_width, v * tex_height))
		return Vec3(*pix)

	def normal_map(self, u, v):
		tex_width, tex_height = self.normal_tex.size
		normal = self.normal_tex.getpixel((u * tex_width, v * tex_height))
		normal = Vec3(*normal) * (2.0 / 255.0)
		normal.x -= 1
		normal.y -= 1
		normal.z -= 1
		normal.normalize()
		return normal

	def __str__(self):
		return "'verts: {}, faces: {}".format(len(self.verts), len(self.faces))

	def read_from_file(self, model_file_name, diffuse_file=None, normal_file=None):
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
		self.read_tex(diffuse_file, normal_file)

	def read_tex(self, diffuse_file=None, normal_file=None):
		if diffuse_file:
			tex = Image.open(diffuse_file)
			self.diffuse_tex = tex.transpose(Image.FLIP_TOP_BOTTOM)
		if normal_file:
			tex = Image.open(normal_file)
			self.normal_tex = tex.transpose(Image.FLIP_TOP_BOTTOM)
			self.generate_TB()

	def generate_TB(self):
		if not self.normal_tex or not self.vnorm:
			return
		vert_uv_normal_by_face = self.vert_uv_normal_by_face
		face_tangent = self.face_tangent
		for i in range(len(self.faces)):
			v0, uv0, _ = vert_uv_normal_by_face(i, 0)
			v1, uv1, _ = vert_uv_normal_by_face(i, 1)
			v2, uv2, _ = vert_uv_normal_by_face(i, 2)
			edge1 = v1 - v0
			e1x = edge1.x
			e1y = edge1.y
			e1z = edge1.z
			edge2 = v2 - v0
			e2x = edge2.x
			e2y = edge2.y
			e2z = edge2.z
			deltaUV1 = uv1 - uv0
			duv1x = deltaUV1.x
			duv1y = deltaUV1.y
			deltaUV2 = uv2 - uv0
			duv2x = deltaUV2.x
			duv2y = deltaUV2.y

			invf = duv1x*duv2y - duv2x*duv1y
			if invf != 0:
				f = 1.0 / invf
				tangent = Vec3(f * (duv2y*e1x - duv1y*e2x), f * (duv2y*e1y - duv1y*e2y), f * (duv2y*e1z - duv1y*e2z))
				tangent.normalize()
				# bitangent = Vec3(f * (duv1x*e2x - duv2x*e1x), f * (duv1x*e2y - duv2x*e1y), f * (duv1x*e2z - duv2x*e1z))
				# bitangent.normalize()
			else:
				tangent = edge1.normalize()
				# bitangent = normal.cross(tangent)

			face_tangent[i] = tangent

	def read_face(self, words):
		verts = []
		for w in words[1:]:
			v, vt, vn = w.split('/')[:3]
			verts.append((int(v), int(vt), int(vn)))
		self.faces.append(tuple(verts))


MODEL_READ_FUNC = {
	'v': lambda self, words: self.verts.append(Vec3(float(words[1]), float(words[2]), float(words[3]))),
	'f': Model.read_face,
	'vt': lambda self, words: self.vtex.append(Vec2(float(words[1]), float(words[2]))),
	'vn': lambda self, words: self.vnorm.append(Vec3(float(words[1]), float(words[2]), float(words[3]))),
}


TEST_TRIANGLE = Model()
TEST_TRIANGLE.verts = [Vec3(), Vec3(-1, -1, 0), Vec3(1, -1, 0), Vec3(1, 1, 0)]
TEST_TRIANGLE.vtex = [Vec2(), Vec2(0, 0), Vec2(1, 0), Vec2(1, 1)]
TEST_TRIANGLE.faces = [((1, 1, 1), (2, 2, 2), (3, 3, 3))]
TEST_TRIANGLE.vnorm = [Vec3(), Vec3(0, 0, 1), Vec3(0, 0, 1), Vec3(0, 0, 1)]
TEST_TRIANGLE.read_tex(diffuse_file='./obj/african_head_diffuse.tga',
					   normal_file='./obj/african_head_nm_tangent.tga')


if __name__ == '__main__':
	m = Model()
	m.read_from_file('./obj/african_head.obj')
	print('verts ', len(m.verts), ' faces ', len(m.faces))
