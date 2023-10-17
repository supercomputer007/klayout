from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QPen, QFont


class PenBrush(object):

    def __init__(self):
        self.pen_brush_map = {}
        self.colors = [
            Qt.GlobalColor.blue,
            Qt.GlobalColor.green,
            Qt.GlobalColor.red,
            Qt.GlobalColor.yellow,
            Qt.GlobalColor.cyan,
            Qt.GlobalColor.darkMagenta,
            Qt.GlobalColor.darkBlue,
            Qt.GlobalColor.darkGray,
            Qt.GlobalColor.darkGreen,
            Qt.GlobalColor.darkYellow,
        ]
        self.colors_index = 0
        self.layer_to_color = {}
        self.layer_to_pen_brush = {}

    def get_color(self, layer_id):

        if layer_id not in self.layer_to_color:
            if len(self.colors) == self.colors_index:
                self.colors_index = 0
            color = self.colors[self.colors_index]
            self.colors_index += 1
            self.layer_to_color[layer_id] = color
        return self.layer_to_color[layer_id]

    def get_pen_brush(self, layer_id):
        if layer_id not in self.layer_to_pen_brush:
            color = self.get_color(layer_id)
            pen = QPen()
            brush = QBrush()
            brush.setStyle(Qt.BrushStyle.BDiagPattern)
            brush.setColor(color)
            pen.setColor(color)
            self.layer_to_pen_brush[layer_id] = (pen, brush)

        return self.layer_to_pen_brush[layer_id]

    @staticmethod
    def get_text_font(size=200):
        font = QFont()
        font.setPointSize(size)
        return font
