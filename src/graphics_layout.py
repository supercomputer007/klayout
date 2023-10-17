import gdspy
from gdspy.library import Cell, CellReference
from .graphics_cell import GraphicsCell, GraphicsCellReference
from gdspy.polygon import Rectangle, Polygon, PolygonSet
from .shape import GraphicsPolygon
from typing import Dict, List
from .label import GraphicsLabel


class GraphicsLayout(object):

    def __init__(self):
        self.gds_lib = gdspy.GdsLibrary
        self.scale = 0
        self.gds_path = ''
        self.has_layout = False
        self.top_cell = None

    @property
    def top_cell_name(self):
        if self.top_cell is not None:
            return self.top_cell.name

    def setup(self):
        self.scale = round(self.gds_lib.unit / self.gds_lib.precision)
        self.top_cell = self.gds_lib.top_level()[0]

    def open(self, file_path):
        self.gds_lib = gdspy.GdsLibrary(infile=r"{}".format(file_path))
        self.has_layout = True
        self.setup()

    @staticmethod
    def float_to_int(float_num, scale):
        return int(round(float_num * scale))

    def parse_gds_polygons(self, gds_polygons) -> Dict[str, List[GraphicsPolygon]]:
        polygon_data = {}

        for polygon in gds_polygons:
            layer_num = polygon.layers[0]
            data_type = polygon.datatypes[0]
            layer_id = "{}-{}".format(layer_num, data_type)
            if layer_id not in polygon_data:
                polygon_data[layer_id] = []
            point_list = [(self.float_to_int(point[0], self.scale),
                           self.float_to_int(point[1], self.scale)) for point in polygon.polygons[0]]
            if isinstance(polygon, Rectangle) or isinstance(polygon, Polygon):
                pg = GraphicsPolygon(layer_num, data_type, point_list)
                polygon_data[pg.layer_id].append(pg)

        return polygon_data

    def parse_gds_labels(self, gds_labels) -> Dict[str, List[GraphicsLabel]]:
        label_data = {}
        for label in gds_labels:
            layer_num = int(label.layer)
            data_type = int(label.texttype)
            text = label.text
            x = self.float_to_int(label.position[0], self.scale)
            y = self.float_to_int(label.position[1], self.scale)
            label = GraphicsLabel(layer_num, data_type, text, x, y)
            if label.layer_id not in label_data:
                label_data[label.layer_id] = []
            label_data[label.layer_id].append(label)
        return label_data

    def get_current_graphics_cell(self, current_cell) -> GraphicsCell:
        polygons = self.parse_gds_polygons(current_cell.polygons)
        labels = self.parse_gds_labels(current_cell.labels)
        gc = GraphicsCell(current_cell.name, current_cell, polygons, labels)

        return gc

    def get_reference_graphics_cell(self, reference_cell: CellReference) -> GraphicsCellReference:

        polygons = self.parse_gds_polygons(reference_cell.get_polygonsets())
        labels = self.parse_gds_labels(reference_cell.get_labels())
        gcr = GraphicsCellReference(reference_cell.ref_cell.name, reference_cell, polygons, labels)

        return gcr

    def get_data(self, cell: Cell):
        gc = self.get_current_graphics_cell(cell)
        for reference_cell in cell.references:
            gcr = self.get_reference_graphics_cell(reference_cell)
            gc.references.append(gcr)
        return gc



