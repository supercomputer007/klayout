from abc import ABC, abstractmethod
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsPolygonItem, QAbstractGraphicsShapeItem
from .pen_brush import PenBrush


class GraphicType(object):
    Rectangle = 3
    Text = 8
    Line = 6


class GraphicStatus(object):
    Normal = 'Normal'
    Delete = 'Delete'


class GraphicItemType(object):
    Shape = 'Shape'
    Text = 'Text'


class GraphicsRectItem(QGraphicsRectItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer_id = ''
        self.polygon_instance = None
        self.net_item = None
        self.is_show_net = False

    def delete(self):
        self.polygon_instance.status = GraphicStatus.Delete
        self.hide()

    def is_delete(self):
        return self.polygon_instance.status == GraphicStatus.Delete

    def show(self) -> None:
        super(GraphicsRectItem, self).show()
        self.show_net()

    def hide(self) -> None:
        super(GraphicsRectItem, self).hide()
        self.hide_net()

    def show_net(self):
        if self.net_item and self.isVisible() and self.is_show_net:
            self.net_item.show()

    def hide_net(self):
        if self.net_item:
            self.net_item.hide()


class GraphicsPolygonItem(QGraphicsPolygonItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer_id = ''
        self.polygon_instance = None
        self.net_item = None
        self.is_show_net = False

    def delete(self):
        self.polygon_instance.status = GraphicStatus.Delete
        self.hide()

    def is_delete(self):
        return self.polygon_instance.status == GraphicStatus.Delete

    def show(self) -> None:
        super(GraphicsPolygonItem, self).show()
        self.show_net()

    def hide(self) -> None:
        super(GraphicsPolygonItem, self).hide()
        self.hide_net()

    def show_net(self):
        if self.net_item and self.isVisible() and self.is_show_net:
            self.net_item.show()

    def hide_net(self):
        if self.net_item:
            self.net_item.hide()


class GraphicsPolygonSet(object):

    def __init__(self, layer_num, data_type, point_list):
        self.bbox = []
        self.layer_id = "{}-{}".format(layer_num, data_type)
        self.layer_num = layer_num
        self.data_type = data_type
        self.point_list = point_list
        self.bbox: list = self.get_bbox()
        self.graphics_item = None
        self.width = self.bbox[2] - self.bbox[0]
        self.height = self.bbox[3] - self.bbox[1]

    def get_bbox(self) -> list:
        x_list = []
        y_list = []
        for point in self.point_list:
            x_list.append(point[0])
            y_list.append(point[1])
        bbox = [
            min(x_list),
            min(y_list),
            max(x_list),
            max(y_list),
        ]
        return bbox

    @abstractmethod
    def get_graphics_item(self, pen_brush: PenBrush) -> QAbstractGraphicsShapeItem:
        pass


class GraphicsPolygon(GraphicsPolygonSet):

    def __init__(self, layer_num, data_type, point_list):
        super().__init__(layer_num, data_type, point_list)
        self.is_rectangle = self.get_is_rectangle()
        self.type = ''

    def get_is_rectangle(self):

        for b_point, a_point in zip(self.point_list[:-1], self.point_list[1:]):
            if b_point[0] != a_point[0] and b_point[1] != a_point[1]:
                return False
        return True

    def get_graphics_item(self, pen_brush: PenBrush) -> QAbstractGraphicsShapeItem:
        pen, brush = pen_brush.get_pen_brush(self.layer_id)
        if self.is_rectangle:
            self.graphics_item = GraphicsRectItem(self.bbox[0], -self.bbox[3], self.width, self.height)
        else:
            self.graphics_item = GraphicsPolygonItem(self.point_list)
        self.graphics_item.setPen(pen)
        self.graphics_item.setBrush(brush)
        self.graphics_item.layer_id = self.layer_id
        self.graphics_item.polygon_instance = self
        return self.graphics_item
