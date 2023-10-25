from PySide6.QtWidgets import QGraphicsScene, QMessageBox
from PySide6.QtGui import Qt, QTransform
from .label import GraphicsLabel
from typing import Dict, List
from .graphics_cell import GraphicsCell
from .pen_brush import PenBrush
from .shape import GraphicsRectItem
from .label import GraphicsTextItem
from .mode import ShowMode


class GraphicsScene(QGraphicsScene):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.graphics_cell = None
        self.pen_brush = PenBrush()
        self.shape_items = {}
        self.label_items = {}
        self.bbox = []
        self.cell_bbox_items = {}
        self.cell_name_items = {}
        self.z_value = 0

    def reset_scene(self):
        self.clear()
        self.graphics_cell = None
        self.shape_items = {}
        self.label_items = {}
        self.bbox = []
        self.cell_bbox_items = {}
        self.cell_name_items = {}

    def setup_data(self, graphics_cell: GraphicsCell):
        self.reset_scene()
        self.graphics_cell = graphics_cell

    def show_polygons_by_layer(self, layer_id):
        z_value = self.z_value
        for item in self.shape_items.get(layer_id, []):
            item.setZValue(z_value)
            item.show()
        self.z_value += 1

    def hide_polygons_by_layer(self, layer_id):
        for item in self.shape_items.get(layer_id, []):
            item.hide()

    def show_labels_by_layer(self, layer_id):
        z_value = self.z_value
        for item in self.label_items.get(layer_id, []):
            item.setZValue(z_value)
            item.show()
        self.z_value += 1

    def show_cell_bbox(self, cell_name):
        self.cell_bbox_items[cell_name].show()

    def hide_cell_bbox(self, cell_name):
        self.cell_bbox_items[cell_name].hide()

    def hide_labels_by_layer(self, layer_id):
        for item in self.label_items.get(layer_id, []):
            item.hide()

    def create_graphics(self):
        self.create_polygons()
        self.create_labels()
        self.create_cell_bbox()
        self.create_cell_name()

    def show_polygons(self):
        for items in self.shape_items.values():
            for item in items:
                item.show()

    def hide_polygons(self):
        for items in self.shape_items.values():
            for item in items:
                item.hide()

    def show_labels(self):
        for items in self.label_items.values():
            for item in items:
                item.show()

    def hide_labels(self):
        for items in self.label_items.values():
            for item in items:
                item.hide()

    def show_all_cells_bbox(self):
        for item in self.cell_bbox_items.values():
            item.show()

    def hide_all_cells_bbox(self):
        for item in self.cell_bbox_items.values():
            item.hide()

    def show_all_cells_name(self):
        for item in self.cell_name_items.values():
            item.show()

    def hide_all_cells_name(self):
        for item in self.cell_name_items.values():
            item.hide()

    def show(self):
        if ShowMode.SelectMode == ShowMode.Detail:
            self.show_polygons()
            self.show_labels()
            self.hide_all_cells_bbox()
            self.hide_all_cells_name()
        else:
            self.show_all_cells_bbox()
            self.show_all_cells_name()
            self.hide_polygons()
            self.hide_labels()

    def create_polygons(self):
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
                graphics_item.hide()
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
                    graphics_item.hide()
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
        layer_id_list = list(set(list(self.shape_items.keys()) + list(self.label_items.keys())))
        layer_id_list.sort(key=lambda x: int(x.replace('-', '')))
        return layer_id_list

    def create_labels(self):
        for layer_id, label_list in self.graphics_cell.labels.items():
            if layer_id not in self.label_items:
                self.label_items[layer_id] = []
            for label in label_list:
                text_item = label.get_text_item(self.pen_brush)
                self.addItem(text_item)
                text_item.hide()
                self.label_items[layer_id].append(text_item)

    def create_cell_bbox(self):
        for ref_cell in self.graphics_cell.references:
            bbox = ref_cell.bbox
            pen = self.pen_brush.get_cell_bbox_pen()
            gri = GraphicsRectItem(bbox[0], -bbox[3], bbox[2] - bbox[0], bbox[3] - bbox[1])
            gri.setPen(pen)
            self.addItem(gri)
            gri.hide()
            self.cell_bbox_items[ref_cell.name] = gri

    def create_cell_name(self):
        for ref_cell in self.graphics_cell.references:
            bbox = ref_cell.bbox
            font = self.pen_brush.get_text_font(500)
            text_item = GraphicsTextItem(ref_cell.name)
            text_item.setFont(font)
            x = (bbox[0]+bbox[2])/2
            y = (bbox[1]+bbox[3])/2
            text_item.setPos(x - text_item.boundingRect().width() / 2, -y - text_item.boundingRect().height() / 2)
            text_item.text_instance = self
            self.cell_name_items[ref_cell.name] = text_item
            self.addItem(text_item)
            text_item.hide()

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

    def on_mouse_left_button_double_clicked(self, event):
        pass

    def on_mouse_right_button_double_clicked(self, event):
        pass

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.on_mouse_left_button_double_clicked(event)
        else:
            self.on_mouse_right_button_double_clicked(event)
        return super(GraphicsScene, self).mouseDoubleClickEvent(event)
