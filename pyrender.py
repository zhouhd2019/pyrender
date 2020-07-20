# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt


def line(x0: int, y0: int, x1: int, y1: int, qp: QPainter):
	x0 = int(x0)
	y0 = int(y0)
	x1 = int(x1)
	y1 = int(y1)

	if abs(x0 - x1) < abs(y0 - y1):  # 保证斜率小于1
		steep = True
		x0, y0 = y0, x0
		x1, y1 = y1, x1
	else:
		steep = False
	if x0 > x1:
		x0, x1 = x1, x0
		y0, y1 = y1, y0

	dx = x1 - x0
	dy = y1 - y0

	if y1 > y0:
		derror2 = dy * 2
		ddy = 1
	else:
		derror2 = - dy * 2
		ddy = -1
	error2 = 0

	y = y0
	for x in range(x0, x1 + 1):
		if steep:
			qp.drawPoint(y, x)
		else:
			qp.drawPoint(x, y)
		error2 += derror2
		if error2 > dx:
			y += ddy
			error2 -= dx * 2
