import sys
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                             QLineEdit, QMainWindow, QPushButton, QVBoxLayout,
                             QWidget)

from controllers import projection_2d, set_axes_equal
from transformations import (cam_rotation, cam_translation, world_rotation,
                             world_translation)
from utils import Aatrox, base_3d, cam_origem, draw_arrows, origem_3d, set_plot

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_variables()
        self.setWindowTitle("Trabalho 1 de Visão Computacional João Gabriel e Lucas Tessari")
        self.setGeometry(100, 100,1280 , 720)
        self.setup_ui()

    def set_variables(self):
        self.objeto_original = Aatrox
        self.objeto = self.objeto_original
        self.camera = np.hstack((base_3d,origem_3d))
        self.referencial = self.camera
        self.px_base = 1280
        self.px_altura = 720
        self.dist_foc = 50
        self.stheta = 0
        self.ox = self.px_base/2
        self.oy = self.px_altura/2
        self.ccd = [36,24]
        self.projection_matrix = np.eye(3, 4)
        
    def setup_ui(self) -> None:
        grid_layout = QGridLayout()

        line_edit_widget1 = self.create_world_widget("Refência do mundo")
        line_edit_widget2 = self.create_cam_widget("Referência da câmera")
        line_edit_widget3 = self.create_intrinsic_widget("Parametros intrínsecos.")

        self.canvas = self.create_matplotlib_canvas()

        grid_layout.addWidget(line_edit_widget1, 0, 0)
        grid_layout.addWidget(line_edit_widget2, 0, 1)
        grid_layout.addWidget(line_edit_widget3, 0, 2)
        grid_layout.addWidget(self.canvas, 1, 0, 1, 3)

        reset_widget = QWidget()
        reset_layout = QHBoxLayout()
        reset_widget.setLayout(reset_layout)

        reset_button = QPushButton("Reset")
        reset_button.setFixedSize(50, 30)
        style_sheet = """
            QPushButton {
                color : white ;
                background: rgba(255, 127, 130,128);
                font: inherit;
                border-radius: 5px;
                line-height: 1;
            }
        """
        reset_button.setStyleSheet(style_sheet)
        reset_button.clicked.connect(self.reset_canvas)

        camera_button = QPushButton("Camera")
        camera_button.setFixedSize(80, 30)
        camera_button.setStyleSheet(style_sheet)
        camera_button.clicked.connect(self.posicionar_cam)

        # Adicionar os botões de reset e de setar câmera ao layout
        reset_layout.addWidget(reset_button)
        reset_layout.addWidget(camera_button)

        grid_layout.addWidget(reset_widget, 2, 0, 1, 3)

        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        
        self.setCentralWidget(central_widget)

    def create_intrinsic_widget(self, title: str) -> QGroupBox:
        """
        Create a widget to group the QLineEdit
        Args:
            title (str): Title of the widget
        Returns:
            QGroupBox: Widget with QLineEdit and update button
        """
        
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        grid_layout = QGridLayout()

        line_edits = []
        labels = ['n_pixels_base:', 'n_pixels_altura:', 'ccd_x:', 'ccd_y:', 'dist_focal:', 'sθ:']  # Texto a ser exibido antes de cada QLineEdit
        values = [self.px_base, self.px_altura, self.ccd[0], self.ccd[1], self.dist_foc, self.stheta]
        
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            line_edit.setText(str(values[i-1]))
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        update_button = QPushButton("Atualizar intrisecos")

        update_button.clicked.connect(lambda: self.update_params_intrinsc(line_edits))

        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        return line_edit_widget
    
    def create_world_widget(self, title: str) -> QLineEdit:
        """
        Create a widget to group the QLineEdit
        Args:
            title (str): Title of the widget
        Returns:
            QGroupBox: Widget with QLineEdit and update button
        """
        
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        grid_layout = QGridLayout()

        line_edits = []
        labels = ['X(move):', 'X(angle):', 'Y(move):', 'Y(angle):', 'Z(move):', 'Z(angle):']  # Texto a ser exibido antes de cada QLineEdit

        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        update_button = QPushButton("Atualizar Mundo")

        print("Perfoming Update World")
        update_button.clicked.connect(lambda: self.update_world(line_edits))

        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        return line_edit_widget

    def create_cam_widget(self, title: str) -> QLineEdit:
        """Create a widget to group the QLineEdit
        Args:
            title (str): Title of the widget
        Returns:
            QGroupBox: Widget with QLineEdit and update button
        """

        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        grid_layout = QGridLayout()

        line_edits = []
        labels = ['X(move):', 'X(angle):', 'Y(move):', 'Y(angle):', 'Z(move):', 'Z(angle):']  # Texto a ser exibido antes de cada QLineEdit

        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        update_button = QPushButton("Atualizar Camera")
        update_button.clicked.connect(lambda: self.update_cam(line_edits))

        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        return line_edit_widget

    def create_matplotlib_canvas(self) -> QWidget:
        """Create a widget to display the 2D and 3D plots
        Args:
            None
        Returns:
            QWidget: Widget with the 2D and 3D plots
        """

        canvas_widget = QWidget()
        canvas_layout = QHBoxLayout()
        canvas_widget.setLayout(canvas_layout)

        self.fig1, self.ax1 = plt.subplots()
        self.ax1.set_title("Imagem")
        self.canvas1 = FigureCanvas(self.fig1)

        self.ax1.set_xlim([0, self.px_base])
        self.ax1.set_ylim([self.px_altura, 0])

        object_2d = projection_2d(
            camera = self.camera, objeto = self.objeto, projection_matrix = self.projection_matrix, 
            px_base = self.px_base, px_altura = self.px_altura, 
            focal_length = self.dist_foc, stheta = self.stheta, ccd = self.ccd
        )

        self.ax1.plot(object_2d[0, :], object_2d[1, :])
        self.ax1.grid('True')
        self.ax1.set_aspect('equal')  
        canvas_layout.addWidget(self.canvas1)

        self.fig2 = plt.figure()
        self.ax2 = self.fig2.add_subplot(111, projection='3d')
        self.ax2 = set_plot(ax=self.ax2, lim=[-150, 100])
        
        self.ax2.plot(self.objeto[0,:],self.objeto[1,:],self.objeto[2,:],'r')
        draw_arrows(self.camera[:, -1], self.camera[:, 0:3], self.ax2)
        # Referencial no mundo
        draw_arrows(self.referencial[:, -1], self.referencial[:, 0:3], self.ax2)
        
        set_axes_equal(self.ax2)

        self.canvas2 = FigureCanvas(self.fig2)
        canvas_layout.addWidget(self.canvas2)
        
        return canvas_widget


    def update_params_intrinsc(self, line_edits: List[QLineEdit]) -> None:
        """Updates the intrinsic parameters of the camera based on user input.
        Args:
            line_edits (List[Any]): A list of QLineEdit objects or similar, 
                                    containing user input for intrinsic parameters.
        Returns:
            None
        """

        _data = [
            self.px_base,
            self.px_altura,
            self.ccd[0],
            self.ccd[1],
            self.dist_foc,
            self.stheta,
        ]

        
        data = [
            float(line_edits[i].text()) if line_edits[i].text().strip() else _data[i]
            for i in range(len(_data))
        ]

        self.px_base, self.px_altura, self.ccd[0], self.ccd[1], self.dist_foc, self.stheta = data
        self.update_canvas()
        
        return 

    @staticmethod
    def clear_line_edit(line_edits: List[QLineEdit]) -> None:
        """
        Clears the text from all QLineEdit objects in the list.
        """
        for i in line_edits:
            i.clear()

    def update_world(self, line_edits: List[QLineEdit]) -> None:
        """
        Updates the world transformation matrix based on input values.

        Args:
            line_edits (List[QLineEdit]): A list of QLineEdit objects containing user inputs for translation and rotation.
        """
        
        data = [
            int(edit.text()) if edit.text().strip() else 0.0
            for edit in line_edits
        ]

        print(f"----- data: {data}")

        x_move, x_angle = data[0], data[1]
        y_move, y_angle = data[2], data[3]
        z_move, z_angle = data[4], data[5]

        T = world_translation(x_move, y_move, z_move)
        Rx = world_rotation('x', x_angle)
        Ry = world_rotation('y', y_angle)
        Rz = world_rotation('z', z_angle)
        
        # Ordem escolhida
        R = Rx @ Ry @ Rz
        M = T @ R

        self.camera = np.dot(M, self.camera)
        self.update_canvas()
        self.clear_line_edit(line_edits)

        return

    def update_cam(self, line_edits: List[QLineEdit]) -> None:
        """
        Updates the cam transformation matrix based on input values.

        Args:
            line_edits (List[QLineEdit]): A list of QLineEdit objects containing user inputs for translation and rotation.
        """
        
        data = [
            int(edit.text()) if edit.text().strip() else 0.0
            for edit in line_edits
        ]

        print(f"----- data: {data}")

        x_move, x_angle = data[0], data[1]
        y_move, y_angle = data[2], data[3]
        z_move, z_angle = data[4], data[5]

        T = cam_translation(self.camera, x_move, y_move, z_move)
        
        Rx = cam_rotation(self.camera, 'x', x_angle)
        Ry = cam_rotation(self.camera, 'y', y_angle)
        Rz = cam_rotation(self.camera, 'z', z_angle)

        # Ordem escolhida
        R = Rx @ Ry @ Rz
        M = T @ R

        self.camera = M @ self.camera
        self.update_canvas()
        self.clear_line_edit(line_edits)

        return 

    def update_canvas(self) -> None:
        """
        Update the 2D and 3D plots with the new object and camera positions.
        Args:
            None
        Returns:
            None
        """
        plt.close('all')

        object_2d = projection_2d(
            camera = self.camera, objeto = self.objeto, projection_matrix = self.projection_matrix, 
            px_base = self.px_base, px_altura = self.px_altura, 
            focal_length = self.dist_foc, stheta = self.stheta, ccd = self.ccd
        )
        self.ax1.clear()
        self.ax1.set_xlim([0, self.px_base])
        self.ax1.set_ylim([self.px_altura, 0])
        self.ax1.plot(object_2d[0, :], object_2d[1, :])
        self.ax1.grid(True)
        self.ax1.set_aspect('equal')

        self.ax2.clear()
        self.ax2 = set_plot(ax=self.ax2, lim=[-150, 100])
        self.ax2.plot3D(self.objeto[0, :], self.objeto[1, :], self.objeto[2, :], 'b')
        draw_arrows(self.camera[:, -1], self.camera[:, 0:3], self.ax2)
        draw_arrows(self.referencial[:, -1], self.referencial[:, 0:3], self.ax2)

        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas.layout().itemAt(1).widget().draw()
        
        return


    def reset_canvas(self) -> None:
        """Reset the canvas to its original state."""
        self.set_variables()
        self.update_canvas()
        return
    
    def posicionar_cam(self) -> None:
        """Set the camera to a specific position."""
        T = world_translation(0, 0, 0)
        self.camera = T @ self.referencial
        R = cam_rotation(self.camera, 'y', -90)
        self.camera = R @ self.camera
        R = cam_rotation(self.camera, 'z', 90)
        self.camera = R @ self.camera
        self.update_canvas()
        return
