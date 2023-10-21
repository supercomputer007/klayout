from ui.mainwindow_ui import Ui_MainWindow
from PySide6 import QtWidgets
from .graphics_layout import GraphicsLayout
from .graphics_scene import GraphicsScene
from PySide6.QtGui import QStandardItemModel, QStandardItem, Qt, QIntValidator
from PySide6.QtWidgets import QDialog, QAbstractItemView
from PySide6.QtCore import QStringListModel, QModelIndex
from .graphics_cell import GraphicsCell
from PySide6.QtGui import QMouseEvent
from .mode import ShowMode, SelectMode
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
        self.show_mode = ShowMode.Simple
        self.selected_cells = []
        self.graphics_cell: GraphicsCell = None
        self.select_mode = SelectMode.SelectMode
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
        self.cells_item_model.clear()
        for cell_name in self.graphics_cell.get_all_reference_cell_name():
            item = QStandardItem(cell_name)
            self.cells_item_model.appendRow(item)

    def update_layers_item_view(self):
        self.layers_item_model.clear()
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
            self.graphics_cell = self.graphics_layout.get_data(self.graphics_layout.top_cell)
            self.cell_stack.append(self.graphics_layout.top_cell)
            self.refresh_graphics()

    def on_clicked_view_cell(self, model_index):
        if len(self.selected_cells) == 1 and model_index in self.selected_cells:
            self.ui.listViewCells.setCurrentIndex(QModelIndex())
            self.selected_cells.clear()
        else:
            self.selected_cells = [model_index]
        # select_item:QStandardItem = self.cells_item_model.item(item.row(), item.column())
        # self.ui.listViewCells.setCurrentIndex()
        # self.ui.listViewCells.setCurrentIndex(QModelIndex())
        # self.ui.listViewCells.clearSelection()
        print()
        # current_index = self.ui.listViewCells.currentIndex()
        # self.ui.listViewCells.setCurrentIndex(current_index)

    def on_double_clicked_view_cell(self, model_index):
        next_cells = [ref.ref_cell for ref in self.graphics_cell.references if ref.name == model_index.data()]
        if next_cells:
            self.graphics_cell = self.graphics_layout.get_data(next_cells[0])
            self.graphics_scene.setup_data(self.graphics_cell)
            self.cell_stack.append(next_cells[0])
            self.refresh_graphics()

        print()

    def on_selected_cell_changed(self, selected):
        if len(self.ui.listViewCells.selectedIndexes()) > 1:
            self.selected_cells = self.ui.listViewCells.selectedIndexes()

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

    def refresh_graphics(self):
        self.graphics_scene.setup_data(self.graphics_cell)
        self.graphics_scene.create_graphics()
        self.graphics_scene.show()
        self.graphics_view.center_display(self.graphics_scene)
        self.update_cells_item_view()
        self.update_layers_item_view()
        self.model_items_select_all(self.layers_item_model)

    def key_press_ctrl_f(self, event):
        ShowMode.SelectMode = ShowMode.Simple
        self.refresh_graphics()

    def key_press_shift_f(self, event):
        ShowMode.SelectMode = ShowMode.Detail
        self.refresh_graphics()

    def key_press_shift_x(self, event):
        self.descend_next_level()

    def key_press_shift_b(self, event):
        self.return_next_level()

    def descend_next_level(self):
        pass

    def return_next_level(self):
        if len(self.cell_stack) > 1:
            self.cell_stack.pop()
            self.graphics_cell = self.graphics_layout.get_data(self.cell_stack[-1])
            self.refresh_graphics()

    def setup(self):
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.listViewCells.setModel(self.cells_item_model)
        self.ui.listViewCells.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.ui.listViewCells.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.listViewCells.clicked.connect(self.on_clicked_view_cell)
        self.ui.listViewCells.doubleClicked.connect(self.on_double_clicked_view_cell)
        self.ui.listViewCells.selectionModel().selectionChanged.connect(self.on_selected_cell_changed)
        self.ui.listViewLayers.setModel(self.layers_item_model)
        self.ui.listViewLayers.clicked.connect(self.on_clicked_layer_cell)
        self.ui.listViewLayers.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_F:
                self.key_press_ctrl_f(event)
        elif event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            func_name = "key_press_shift_{}".format(event.text().lower())
            if hasattr(self, func_name):
                exec('self.{}(event)'.format(func_name))
        elif hasattr(self, "key_press_{}".format(event.text())):
            exec('self.key_press_{}(event)'.format(event.text()))
        elif hasattr(self, "key_press_uppercase_{}".format(event.text().lower())):
            exec('self.key_press_uppercase_{}(event)'.format(event.text().lower()))

        return super(MainWindow, self).keyPressEvent(event)

    def on_mouse_left_button_double_clicked(self, event: QMouseEvent):
        print()

    def on_mouse_right_button_double_clicked(self, event):
        self.return_next_level()

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.on_mouse_left_button_double_clicked(event)
        else:
            self.on_mouse_right_button_double_clicked(event)
        super(MainWindow, self).mouseDoubleClickEvent(event)

