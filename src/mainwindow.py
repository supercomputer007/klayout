from ui.mainwindow_ui import Ui_MainWindow
from PySide6 import QtWidgets
from .graphics_layout import GraphicsLayout
from .graphics_scene import GraphicsScene
from PySide6.QtGui import QStandardItemModel, QStandardItem, Qt, QIntValidator
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QStringListModel
import shutil
import os


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.graphics_layout = GraphicsLayout()
        self.graphics_scene = GraphicsScene()
        self.ui.graphicsView.setScene(self.graphics_scene)
        self.cell_stack = []
        self.cells_item_model = QStandardItemModel()
        self.layers_item_model = QStandardItemModel()
        self.setup()

    @property
    def graphics_view(self):
        return self.ui.graphicsView

    def key_press_f(self, event):
        self.graphics_view.center_display(self.graphics_scene)

    @staticmethod
    def model_items_select_all(model):
        for row in range(model.rowCount()):
            model.item(row, 0).setCheckState(Qt.CheckState.Checked)

    def update_cells_item_view(self):
        for cell_name in self.graphics_scene.get_all_reference_cell_name():
            item = QStandardItem(cell_name)
            self.cells_item_model.appendRow(item)

    def update_layers_item_view(self):
        item = QStandardItem('ALL')
        item.setCheckable(True)
        self.layers_item_model.appendRow(item)
        for layer_id in self.graphics_scene.get_all_layer_id():
            item = QStandardItem(layer_id)
            item.setCheckable(True)
            self.layers_item_model.appendRow(item)

    def open(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        if file_path:
            self.graphics_layout.open(file_path)
            graphics_cell = self.graphics_layout.get_data(self.graphics_layout.top_cell)
            self.graphics_scene.setup_data(graphics_cell)
            self.graphics_scene.show()
            self.graphics_view.center_display(self.graphics_scene)
            self.update_cells_item_view()
            self.update_layers_item_view()
            self.model_items_select_all(self.layers_item_model)

    def on_clicked_view_cell(self):
        pass

    def on_clicked_layer_cell(self, item):
        select_item = self.layers_item_model.item(item.row(), item.column())
        if select_item.text() == 'ALL':
            if select_item.checkState() == Qt.CheckState.Checked:
                for row in range(self.layers_item_model.rowCount()):
                    if row != 0:
                        self.layers_item_model.item(row, 0).setCheckState(Qt.CheckState.Checked)
                        self.graphics_scene.show_polygons_by_layer(self.layers_item_model.item(row, 0).text())
                        self.graphics_scene.show_labels_by_layer(self.layers_item_model.item(row, 0).text())
            else:
                for row in range(self.layers_item_model.rowCount()):
                    if row != 0:
                        self.layers_item_model.item(row, 0).setCheckState(Qt.CheckState.Unchecked)
                        self.graphics_scene.hide_polygons_by_layer(self.layers_item_model.item(row, 0).text())
                        self.graphics_scene.hide_labels_by_layer(self.layers_item_model.item(row, 0).text())
        else:
            if select_item.checkState() == Qt.CheckState.Checked:
                self.graphics_scene.show_polygons_by_layer(select_item.text())
                self.graphics_scene.show_labels_by_layer(select_item.text())
            else:
                self.graphics_scene.hide_polygons_by_layer(select_item.text())
                self.graphics_scene.hide_labels_by_layer(select_item.text())

    def setup(self):
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.listViewCells.setModel(self.cells_item_model)
        self.ui.listViewLayers.setModel(self.layers_item_model)
        self.ui.listViewCells.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.listViewLayers.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.listViewCells.clicked.connect(self.on_clicked_view_cell)
        self.ui.listViewLayers.clicked.connect(self.on_clicked_layer_cell)

    def keyPressEvent(self, event):

        if hasattr(self, "key_press_{}".format(event.text())):
            exec('self.key_press_{}(event)'.format(event.text()))
        elif hasattr(self, "key_press_uppercase_{}".format(event.text().lower())):
            exec('self.key_press_uppercase_{}(event)'.format(event.text().lower()))

        return super(MainWindow, self).keyPressEvent(event)
