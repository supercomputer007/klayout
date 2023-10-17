from PySide6.QtWidgets import QGraphicsScene, QMessageBox
from PySide6.QtGui import Qt, QTransform
from .label import GraphicsLabel
from typing import Dict, List
from .graphics_cell import GraphicsCell
from .pen_brush import PenBrush


class GraphicsScene(QGraphicsScene):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.polygon_item_map = {}
        self.label_item_map = {}
        self.is_detail = False
        self.graphics_cell = None
        self.pen_brush = PenBrush()
        self.is_show_detail = True
        self.shape_items = {}
        self.label_items = {}
        self.bbox = []

    def reset_scene(self):
        self.clear()
        self.polygon_item_map = {}
        self.label_item_map = {}
        self.is_detail = False

    def setup_data(self, graphics_cell: GraphicsCell):
        self.graphics_cell = graphics_cell

    def show_polygons_by_layer(self, layer_id):
        for item in self.shape_items.get(layer_id, []):
            item.show()

    def hide_polygons_by_layer(self, layer_id):
        for item in self.shape_items.get(layer_id, []):
            item.hide()

    def show_labels_by_layer(self, layer_id):
        for item in self.label_items.get(layer_id, []):
            item.show()

    def hide_labels_by_layer(self, layer_id):
        for item in self.label_items.get(layer_id, []):
            item.hide()

    def show(self):
        self.reset_scene()
        if self.is_show_detail:
            self.show_detail()
        else:
            self.show_component_bbox()

    def show_component_bbox(self):
        pass

    def show_polygons(self):
        x_list = []
        y_list = []
        for layer_id, pg_list in self.graphics_cell.polygons.items():
            if layer_id not in self.shape_items:
                self.shape_items[layer_id] = []
            for pg in pg_list:
                x_list.extend([pg.bbox[0], pg.bbox[2]])
                y_list.extend([-pg.bbox[1], -pg.bbox[3]])
                graphics_item = pg.get_graphics_item(self.pen_brush)
                self.addItem(graphics_item)
                self.shape_items[layer_id].append(graphics_item)
        for ref_cell in self.graphics_cell.references:
            for layer_id, pg_list in ref_cell.polygons.items():
                if layer_id not in self.shape_items:
                    self.shape_items[layer_id] = []
                for pg in pg_list:
                    x_list.extend([pg.bbox[0], pg.bbox[2]])
                    y_list.extend([-pg.bbox[1], -pg.bbox[3]])
                    graphics_item = pg.get_graphics_item(self.pen_brush)
                    self.addItem(graphics_item)
                    self.shape_items[layer_id].append(graphics_item)
        min_x = min(x_list)
        min_y = min(y_list)
        max_x = max(x_list)
        max_y = max(y_list)
        width = max_x - min_x
        height = max_y - min_y
        self.bbox = [min_x, min_y, max_x, max_y]
        self.width()
        self.height()
        self.setSceneRect(min_x - width, min_y - height, width * 3, height * 3)

    def get_all_layer_id(self):
        layer_id_list = list(set(list(self.shape_items.keys())+list(self.label_items.keys())))
        layer_id_list.sort(key=lambda x: int(x.replace('-', '')))
        return layer_id_list

    def get_all_reference_cell_name(self):
        cells_name = [ref_cell.name for ref_cell in self.graphics_cell.references]
        cells_name.sort()
        return cells_name

    def show_labels(self):
        for layer_id, label_list in self.graphics_cell.labels.items():
            if layer_id not in self.label_items:
                self.label_items[layer_id] = []
            for label in label_list:
                text_item = label.get_text_item(self.pen_brush)
                self.addItem(text_item)
                self.label_items[layer_id].append(text_item)

    def show_detail(self):
        self.show_polygons()
        self.show_labels()

    def show_cell_bbox(self):
        pass

    def move(self, x, y):
        pass

    def flip_x(self):
        pass

    def flip_y(self):
        pass

    def rotate_left(self):
        self.rotate(-90)

    def rotate_right(self):
        self.rotate(90)

    def rotate(self, degree):
        pass

