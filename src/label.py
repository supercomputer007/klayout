from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem, QGraphicsPolygonItem


class GraphicStatus(object):
    Normal = 'Normal'
    Delete = 'Delete'


class GraphicsLabel(object):

    def __init__(self, layer_num, data_type, text, x, y):
        self.layer_num = layer_num
        self.data_type = data_type
        self.layer_id = "{}-{}".format(layer_num, data_type)
        self.text = text
        self.x = x
        self.y = y
        self.text_item = None

    def get_text_item(self, pen_brush):
        if not self.text_item:
            font = pen_brush.get_text_font()
            self.text_item = GraphicsTextItem(self.text)
            self.text_item.setFont(font)
            self.text_item.setPos(self.x - self.text_item.boundingRect().width() / 2,
                                  -self.y - self.text_item.boundingRect().height() / 2)
            self.text_item.layer_id = self.layer_id
            self.text_item.text_instance = self
        return self.text_item


class GraphicsTextItem(QGraphicsTextItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer_id = ''
        self.text_instance = None

    def delete(self):
        if self.text_instance:
            self.text_instance.status = GraphicStatus.Delete
        self.hide()

    def is_delete(self):
        return self.text_instance.status == GraphicStatus.Delete
