#!/bin/env python
# encoding=utf8

import os
import pywraps2 as s2
import ez.lib.ezShapefile as shapefile

def cellIds_to_shapefile(cellIds, fn):
	wr = shapefile.writer(fn, shapefile.Polygon)
	wr.addField("id")
	wr.addField("face")
	wr.addField("level")
	wr.addField("lat_min")
	wr.addField("lat_max")
	wr.addField("lon_min")
	wr.addField("lon_max")
	for cellId in cellIds:
		cell = s2.S2Cell(cellId)
		rect = cell.GetRectBound()
		lat_min, lat_max, lon_min, lon_max = rect.lat_lo().degrees(), rect.lat_hi().degrees(), rect.lng_lo().degrees(), rect.lng_hi().degrees()
		vertices = []
		for i in xrange(0, 4):
			vertex = cell.GetVertex(i)
			latlng = s2.S2LatLng(vertex)
			vertices.append((latlng.lng().degrees(),
				 latlng.lat().degrees()))
		vertices.append(vertices[0])
		wr.shapePolygon([vertices])
		wr.record((cellId.id(), cellId.face(), cellId.level(), lat_min, lat_max, lon_min, lon_max))
	wr.close()



def bbox_to_shapefile(bbox, fd):
	lat_min, lat_max, lng_min, lng_max = bbox
	lo = s2.S2LatLng(s2.S1Angle.Degrees(lat_min), s2.S1Angle.Degrees(lng_min))
	hi = s2.S2LatLng(s2.S1Angle.Degrees(lat_max), s2.S1Angle.Degrees(lng_max))
	rect = s2.S2LatLngRect(lo, hi)
	for level in range(17):
		rc = s2.S2RegionCoverer()
		rc.set_fixed_level(level)
		cells = rc.GetCovering(rect)
		cellIds_to_shapefile(cells, os.path.join(fd, 's2geometry_%02d'%level))



bbox = 39.93536, 39.96275, 116.45305, 116.4825299999999
fd = r'/home/eric/Desktop/s2shape'
bbox_to_shapefile(bbox, fd)

