from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QWidget, QVBoxLayout, QButtonGroup, QGridLayout, QPushButton, QLineEdit, QTextEdit, QSlider, QProgressBar, QComboBox, QListWidget, QRadioButton, QCheckBox, QHBoxLayout
from PySide6.QtCore import Qt     # centering the labels
from visualizer import AudioVisulaizer

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Spy Software')

        container_main = QWidget()
        self.setCentralWidget(container_main)

        layout_main = QHBoxLayout(container_main)

        self.visualizer = AudioVisulaizer()

        container_left = QWidget()
        container_right = QWidget()
        container_modes = QWidget()
        container_live_mode = QWidget()
        container_file_mode = QWidget()
        container_live_mode.setFixedWidth(250)
        container_file_mode.setFixedWidth(250)
        container_left.setFixedWidth(750)
        container_filter = QWidget()

        layout_right = QVBoxLayout(container_right)
        layout_left = QHBoxLayout(container_left)
        layout_modes = QHBoxLayout(container_modes)
        layout_live_mode = QVBoxLayout(container_live_mode)
        layout_file_mode = QVBoxLayout(container_file_mode)
        layout_filter = QVBoxLayout(container_filter)

        layout_right.addWidget(container_modes)
        

        line_A = QFrame()
        line_A.setFrameShape(QFrame.VLine)
        line_A.setFrameShadow(QFrame.Sunken)
        line_B = QFrame()
        line_B.setFrameShape(QFrame.HLine)
        line_B.setFrameShadow(QFrame.Sunken)
        line_C = QFrame()
        line_C.setFrameShape(QFrame.VLine)
        line_C.setFrameShadow(QFrame.Sunken)

        layout_modes.addWidget(container_live_mode)
        layout_modes.addWidget(line_A)
        layout_modes.addWidget(container_file_mode)

        radio_live = QRadioButton('Live Mode')
        layout_record = QHBoxLayout(container_live_mode)
        button_record = QPushButton('Record')
        button_stop = QPushButton('Stop/Save')
        layout_record.addWidget(button_record)
        layout_record.addWidget(button_stop)

        radio_file = QRadioButton('File Mode')
        button_import = QPushButton('Import')
        self.mode_group = QButtonGroup()
        self.mode_group.addButton(radio_live)
        self.mode_group.addButton(radio_file)
        radio_live.setAutoExclusive(True)
        radio_live.toggled.connect(lambda: self.update_vis())
        radio_file.setAutoExclusive(True)
        self.mode_group.setExclusive(True)

        layout_right.addWidget(line_B)
        label_filter = QLabel('Noise Filter')
        radio_filter_toggle = QRadioButton('On')

        layout_right.addWidget(container_filter)
        layout_filter.addWidget(label_filter)
        layout_filter.addWidget(radio_filter_toggle)

        layout_live_mode.addWidget(radio_live)
        layout_live_mode.addLayout(layout_record)
        layout_file_mode.addWidget(radio_file)
        layout_file_mode.addWidget(button_import)
        layout_right.addLayout(layout_live_mode)
        layout_right.addLayout(layout_file_mode)
        layout_left.addWidget(self.visualizer)
        
        layout_main.addWidget(container_left)
        layout_main.addWidget(line_C)
        layout_main.addWidget(container_right)

        layout_right.addStretch(1)

        

        label1 = QLabel('One')
        label1.setAlignment(Qt.AlignCenter)

        button = QPushButton('Filter')
        button.clicked.connect(lambda: print('Button Clicked!'))

        line_edit = QLineEdit()
        text_edit = QTextEdit()

        comboBox = QComboBox()
        comboBox.addItems(['One', 'Two', 'Three'])

        listwidget = QListWidget()
        listwidget.addItems(['One', 'Two', 'Three'])
        listwidget.itemClicked.connect(lambda item: print(f'Item clicked {item.text}'))

        checkbox1 = QCheckBox('One')
        checkbox2 = QCheckBox('Two')
        checkbox3 = QCheckBox('Three')

        radio1 = QRadioButton('One')
        radio2 = QRadioButton('Two')
        radio3 = QRadioButton('Three')

        for r in (radio1, radio2, radio3):
            r.toggled.connect(self.radio_changed)
        


        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)

        inner_container = QWidget()
        inner_layout = QHBoxLayout(inner_container)
        inner_layout.addWidget(radio1)
        inner_layout.addWidget(radio2)
        inner_layout.addWidget(radio3)

        # label2 = QLabel('Two')
        # label2.setAlignment(Qt.AlignCenter) 

        # label3 = QLabel('Three')
        # label3.setAlignment(Qt.AlignCenter)

        # label4 = QLabel('Four')
        # label4.setAlignment(Qt.AlignCenter)


        
        # layout.addWidget(label2, 0, 1)
        # layout.addWidget(label3, 1, 0)
        # layout.addWidget(label4, 1, 1)

    def radio_changed(self):
        r = self.sender()
        if r.isChecked():
            print('Radio button was selected! Value: ', r.text())

    def update_vis(self):
        self.visualizer.turnOn()
        self.visualizer.update()
    def turnOff_vis(self):
        self.visualizer.turnOff()
        self.visualizer.update()

app = QApplication()
window = MainWindow()
window.show()

app.exec()