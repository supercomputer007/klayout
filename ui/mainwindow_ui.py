# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QGraphicsView, QHBoxLayout,
    QListView, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QToolBar, QVBoxLayout, QWidget)

from src.graphics_view import GraphicsView

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(970, 721)
        MainWindow.setAutoFillBackground(False)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.actionPath = QAction(MainWindow)
        self.actionPath.setObjectName(u"actionPath")
        self.actionDelete = QAction(MainWindow)
        self.actionDelete.setObjectName(u"actionDelete")
        self.actionMove = QAction(MainWindow)
        self.actionMove.setObjectName(u"actionMove")
        self.actionView = QAction(MainWindow)
        self.actionView.setObjectName(u"actionView")
        self.actionEdit = QAction(MainWindow)
        self.actionEdit.setObjectName(u"actionEdit")
        self.actionMeasure = QAction(MainWindow)
        self.actionMeasure.setObjectName(u"actionMeasure")
        self.actionVia = QAction(MainWindow)
        self.actionVia.setObjectName(u"actionVia")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.graphicsView = GraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout.addWidget(self.graphicsView)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 970, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuMode = QMenu(self.menubar)
        self.menuMode.setObjectName(u"menuMode")
        MainWindow.setMenuBar(self.menubar)
        self.WindowCell = QDockWidget(MainWindow)
        self.WindowCell.setObjectName(u"WindowCell")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.WindowCell.sizePolicy().hasHeightForWidth())
        self.WindowCell.setSizePolicy(sizePolicy)
        self.WindowCell.setMinimumSize(QSize(144, 114))
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.horizontalLayout_2 = QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.listViewCells = QListView(self.dockWidgetContents)
        self.listViewCells.setObjectName(u"listViewCells")
        sizePolicy.setHeightForWidth(self.listViewCells.sizePolicy().hasHeightForWidth())
        self.listViewCells.setSizePolicy(sizePolicy)
        self.listViewCells.setResizeMode(QListView.Adjust)
        self.listViewCells.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.listViewCells)

        self.WindowCell.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.WindowCell)
        self.WindowLayer = QDockWidget(MainWindow)
        self.WindowLayer.setObjectName(u"WindowLayer")
        self.WindowLayer.setMinimumSize(QSize(144, 114))
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.horizontalLayout_8 = QHBoxLayout(self.dockWidgetContents_2)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.listViewLayers = QListView(self.dockWidgetContents_2)
        self.listViewLayers.setObjectName(u"listViewLayers")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.listViewLayers.sizePolicy().hasHeightForWidth())
        self.listViewLayers.setSizePolicy(sizePolicy1)
        self.listViewLayers.setResizeMode(QListView.Adjust)

        self.horizontalLayout_8.addWidget(self.listViewLayers)

        self.WindowLayer.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.WindowLayer)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuMode.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionClose)
        self.menuEdit.addAction(self.actionPath)
        self.menuEdit.addAction(self.actionDelete)
        self.menuEdit.addAction(self.actionVia)
        self.menuMode.addAction(self.actionMove)
        self.menuMode.addAction(self.actionView)
        self.menuMode.addAction(self.actionEdit)
        self.menuMode.addAction(self.actionMeasure)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionView)
        self.toolBar.addAction(self.actionMove)
        self.toolBar.addAction(self.actionEdit)
        self.toolBar.addAction(self.actionMeasure)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPath)
        self.toolBar.addAction(self.actionVia)
        self.toolBar.addAction(self.actionDelete)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Open Layout", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.actionPath.setText(QCoreApplication.translate("MainWindow", u"Path", None))
        self.actionDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.actionMove.setText(QCoreApplication.translate("MainWindow", u"Move", None))
        self.actionView.setText(QCoreApplication.translate("MainWindow", u"View", None))
        self.actionEdit.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.actionMeasure.setText(QCoreApplication.translate("MainWindow", u"Measure", None))
        self.actionVia.setText(QCoreApplication.translate("MainWindow", u"Via", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuMode.setTitle(QCoreApplication.translate("MainWindow", u"Mode", None))
#if QT_CONFIG(whatsthis)
        self.WindowCell.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(accessibility)
        self.WindowCell.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.WindowCell.setWindowTitle(QCoreApplication.translate("MainWindow", u"Cell", None))
        self.WindowLayer.setWindowTitle(QCoreApplication.translate("MainWindow", u"Layer", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

