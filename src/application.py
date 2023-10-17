from PySide6.QtWidgets import QApplication
from .mainwindow import MainWindow


class Application(QApplication):

    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = MainWindow()

    def exec(self) -> int:
        self.main_window.show()
        return super(Application, self).exec()






