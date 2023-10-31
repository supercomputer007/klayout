from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen
from .shape import GraphicType


class GraphicsView(QGraphicsView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setStyleSheet("padding: 0px; border: 0px;")
        self.zoom_in = 1.2
        self.zoom_out = 1.0 / 1.2
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

    def resize_shape_pen_width(self):
        pen_width = int(self.mapToScene(0, 0, 1, 1)[2].x() - self.mapToScene(0, 0, 1, 1)[0].x())
        shape_types = [GraphicType.Rectangle, GraphicType.Polygon]
        for item in [item for item in self.scene().items() if item.type() in shape_types]:
            pen = QPen(item.pen().color(), pen_width)
            item.setPen(pen)

    def resize_line_pen_width(self):
        pen_width = int(self.mapToScene(0, 0, 1, 1)[2].x() - self.mapToScene(0, 0, 1, 1)[0].x())
        for item in [item for item in self.scene().items() if item.type() == GraphicType.Line]:
            pen = QPen(item.pen().color(), pen_width)
            item.setPen(pen)

    def center_display(self, layout_scene):
        self.resetTransform()
        width = layout_scene.width()
        height = layout_scene.height()
        if width > height:
            scale = (self.width()/width)
        else:
            scale = (self.height() / height)
        self.scale(scale, scale)
        self.resize_shape_pen_width()
        self.resize_line_pen_width()

    def keyPressEvent(self, event):

        if hasattr(self, "key_press_{}".format(event.text())):
            exec('self.key_press_{}(event)'.format(event.text()))
        elif hasattr(self, "key_press_uppercase_{}".format(event.text().lower())):
            exec('self.key_press_uppercase_{}(event)'.format(event.text().lower()))
        return super(GraphicsView, self).keyPressEvent(event)

    def wheelEvent(self, event) -> None:
        if len(self.scene().items()) > 0:
            wheel_delta_value = event.angleDelta().y()
            if wheel_delta_value > 0:
                self.scale(self.zoom_in, self.zoom_in)
            else:
                self.scale(self.zoom_out, self.zoom_out)
            self.update()
            self.resize_shape_pen_width()
            self.resize_line_pen_width()