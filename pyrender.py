# -*- coding: utf-8 -*-
from typing import List, Tuple
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
import math3d
from math3d import Vec2, Vec3


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


def is_inside_triangle(pt0: Vec2, pt1: Vec2, pt2: Vec2, px, py) -> bool:
	pa_x = pt0.x - px
	pa_y = pt0.y - py
	pb_x = pt1.x - px
	pb_y = pt1.y - py
	pc_x = pt2.x - px
	pc_y = pt2.y - py
	t1 = pa_x * pb_y - pa_y * pb_x
	t2 = pb_x * pc_y - pb_y * pc_x
	t3 = pc_x * pa_y - pc_y * pa_x
	return (t1 > 0 and t2 > 0 and t3 > 0) or (t1 < 0 and t2 < 0 and t3 < 0)


def triangle(pt0, pt1, pt2, qp: QPainter, size: Tuple[int, int]):
	half_width, half_height = size
	bbox_min_x = int(max(-half_width, min(pt0.x, min(pt1.x, pt2.x))))
	bbox_min_y = int(max(-half_height, min(pt0.y, min(pt1.y, pt2.y))))
	bbox_max_x = int(min(half_width, max(pt0.x, max(pt1.x, pt2.x))))
	bbox_max_y = int(min(half_height, max(pt0.y, max(pt1.y, pt2.y))))

	drawPoint = qp.drawPoint
	for x in range(bbox_min_x, bbox_max_x + 1):
		for y in range(bbox_min_y, bbox_max_y + 1):
			is_in = is_inside_triangle(pt0, pt1, pt2, x, y)
			if is_in:
				drawPoint(x, y)


def barycentric(pts: List[Vec2], px, py) -> Vec3:
	p1 = Vec3(pts[2].x - pts[0].x, pts[1].x - pts[0].x, pts[0].x - px)
	p2 = Vec3(pts[2].y - pts[0].y, pts[1].y - pts[0].y, pts[0].y - py)
	u = p1.cross(p2)
	return Vec3(1 - (u.x + u.y)/u.z, u.y / u.z, u.x / u.z)


def triangle_by_barycentric(pt0, pt1, pt2, zbuffer: List[List[int]], qp: QPainter, size: Tuple[int, int]):
	half_width, half_height = size
	bbox_min_x = int(max(-half_width, min(pt0.x, min(pt1.x, pt2.x))))
	bbox_min_y = int(max(-half_height, min(pt0.y, min(pt1.y, pt2.y))))
	bbox_max_x = int(min(half_width, max(pt0.x, max(pt1.x, pt2.x))))
	bbox_max_y = int(min(half_height, max(pt0.y, max(pt1.y, pt2.y))))

	for x in range(bbox_min_x, bbox_max_x + 1):
		for y in range(bbox_min_y, bbox_max_y + 1):
			bc = barycentric([pt0, pt1, pt2], x, y)
			if bc.x < 0 or bc.y < 0 or bc.z < 0:
				continue
			z = bc.x * pt0.z + bc.y * pt1.z + bc.z * pt2.z
			if zbuffer[x + half_width + (y + half_height) * half_width * 2] < z:
				zbuffer[x + half_width + (y + half_height) * half_width * 2] = z
				qp.drawPoint(x, y)
