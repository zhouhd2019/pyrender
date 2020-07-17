# -*- coding: utf-8 -*-
import math3d
from math3d import Vec3


class Model(object):
	def __init__(self):
		self.verts = [Vec3(), ]
		self.faces = []

	def __str__(self):
		return "'verts: {}, faces: {}".format(len(self.verts), len(self.faces))

	def read_from_file(self, file_name):
		with open(file_name, 'r') as f:
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

	def read_face(self, words):
		v1 = words[1]
		verts = []
		for w in words[1:]:
			verts.append(int(w.split('/')[0]))
		self.faces.append(verts)


MODEL_READ_FUNC = {
	'v': lambda self, words: self.verts.append(Vec3(float(words[1]), float(words[2]), float(words[3]))),
	'f': Model.read_face,
}


if __name__ == '__main__':
	m = Model()
	m.read_from_file('./obj/african_head.obj')
	print('verts ', len(m.verts), ' faces ', len(m.faces))