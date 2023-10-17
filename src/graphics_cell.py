from gdspy.library import Cell, CellReference
from typing import Dict, List
from .shape import GraphicsPolygon
from .label import GraphicsLabel


class BaseCell(object):

    @staticmethod
    def get_bbox(polygons: Dict[str, List[GraphicsPolygon]]):
        x_list = []
        y_list = []
        for pg_list in polygons.values():
            for pg in pg_list:
                x_list.extend([pg.bbox[0], pg.bbox[2]])
                y_list.extend([pg.bbox[1], pg.bbox[3]])
        bbox = [
            min(x_list),
            min(y_list),
            max(x_list),
            max(y_list),
        ]
        return bbox


class GraphicsCell(BaseCell):

    def __init__(self, name: str, gds_cell: Cell, polygons: Dict[str, List[GraphicsPolygon]],
                 labels: Dict[str, List[GraphicsLabel]]):
        self.name = name
        self.gds_cell = gds_cell
        self.polygons = polygons
        self.labels = labels
        self.bbox = self.get_bbox(self.polygons)
        self.references: List[GraphicsCellReference] = []
        self.run()

    def run(self):
        print('build  graphics cell')


class GraphicsCellReference(BaseCell):

    def __init__(self, name: str, gds_cell_reference: CellReference, polygons: Dict[str, List[GraphicsPolygon]],
                 labels: Dict[str, List[GraphicsLabel]]):
        self.name = name
        self.gds_cell_reference = gds_cell_reference
        self.polygons = polygons
        self.labels = labels
        self.bbox = self.get_bbox(self.polygons)
        self.run()

    def run(self):
        print('build  graphics cell reference')
