#COMMAND 0xFFFF - only command
#COMMAND 0x0000 - no command
#COMMAND 0x0001-0xFFFE - command with data

#[NOP amount (2 bytes)][DATA]
#[SWRESET amount (2 bytes)][DATA]
#[SLPIN amount (2 bytes)][DATA]
#[SLPOUT amount (2 bytes)][DATA]
#[PTLON amount (2 bytes)][DATA]
#[NORON amount (2 bytes)][DATA]
#[INVOFF amount (2 bytes)][DATA]
#[INVON amount (2 bytes)][DATA]
#[GAMSET amount (2 bytes)][DATA]
#[DISPOFF amount (2 bytes)][DATA]
#[DISPON amount (2 bytes)][DATA]
#[CASET amount (2 bytes)][DATA]
#[RASET amount (2 bytes)][DATA]
#[RAMWR amount (2 bytes)][DATA]
#[RAMRD amount (2 bytes)][DATA]
#[PTLAR amount (2 bytes)][DATA]
#[SCRLAR amount (2 bytes)][DATA]
#[TEOFF amount (2 bytes)][DATA]
#[TEON amount (2 bytes)][DATA]
#[MADCTL amount (2 bytes)][DATA]
#[VSCSAD amount (2 bytes)][DATA]
#[IDMOFF amount (2 bytes)][DATA]
#[IDMON amount (2 bytes)][DATA]
#[COLMOD amount (2 bytes)][DATA]
#[FRMCTR1 amount (2 bytes)][DATA]
#[FRMCTR2 amount (2 bytes)][DATA]
#[FRMCTR3 amount (2 bytes)][DATA]
#[INVCTR amount (2 bytes)][DATA]
#[PWCTR1 amount (2 bytes)][DATA]
#[PWCTR2 amount (2 bytes)][DATA]
#[PWCTR3 amount (2 bytes)][DATA]
#[PWCTR4 amount (2 bytes)][DATA]
#[PWCTR5 amount (2 bytes)][DATA]
#[VMCTR1 amount (2 bytes)][DATA]
#[VMOFCTR amount (2 bytes)][DATA]
#[WRID1 amount (2 bytes)][DATA]
#[WRID2 amount (2 bytes)][DATA]
#[WRID3 amount (2 bytes)][DATA]
#[NVFCTR1 amount (2 bytes)][DATA]
#[RDID1 amount (2 bytes)][DATA]
#[RDID2 amount (2 bytes)][DATA]
#[RDID3 amount (2 bytes)][DATA]
#[NVFCTR2 amount (2 bytes)][DATA]
#[NVFCTR3 amount (2 bytes)][DATA]
#[GMCTRP1 amount (2 bytes)][DATA]
#[GMCTRN1 amount (2 bytes)][DATA]
#[GCV amount (2 bytes)][DATA]

import PyQt6.QtCore as QtCore
import PyQt6.QtWidgets as QtWidgets, PyQt6.QtGui as QtGui


class ConfigFile:
    datakeys = ["NOP", "SWRESET", "SLPIN", "SLPOUT", "PTLON", "NORON", \
                "INVOFF", "INVON", "GAMSET", "DISPOFF", "DISPON", "CASET", \
                "RASET", "RAMWR", "RAMRD", "PTLAR", "SCRLAR", "TEOFF", \
                "TEON", "MADCTL", "VSCSAD", "IDMOFF", "IDMON", "COLMOD", \
                "FRMCTR1", "FRMCTR2", "FRMCTR3", "INVCTR", "PWCTR1", "PWCTR2", \
                "PWCTR3", "PWCTR4", "PWCTR5", "VMCTR1", "VMOFCTR", "WRID1", \
                "WRID2", "WRID3", "NVFCTR1", "RDID1", "RDID2", "RDID3", \
                "NVFCTR2", "NVFCTR3", "GMCTRP1", "GMCTRN1", "GCV"]

    def __init__(self, filename:str):
        self.filename = filename
        self.config = {}
        self.read_config()

    def read_config(self):
        try:
            with open(self.filename, 'rb') as file:
                raw_data = file.read()
            index = 0
            while raw_data:
                length_raw = raw_data[:2]
                length = int.from_bytes(length_raw, byteorder='big')
                command = None
                data = None
                match length_raw:
                    case b'\x00\x00':
                        length = 0
                    case b'\xFF\xFF':
                        command = True
                        length = 0
                    case _:
                        command = True
                        data = raw_data[2:length+2]
                self.config[self.datakeys[index]] = (command, data)
                raw_data = raw_data[length+2:]
                index += 1
        except FileNotFoundError:
            print("File not found")
            return
        
    def get_config_value(self, key:str):
        assert key in self.datakeys, "Invalid key"
        return self.config.get(key, None)
    
    def set_config_value(self, key:str, command:bool, data:bytes):
        assert key in self.datakeys, "Invalid key"
        self.config[key] = (command, data)

    def write_config(self):
        with open(self.filename, 'wb+') as file:
            for key in self.datakeys:
                command, data = self.config.get(key, (None, None))
                if command == None:
                    length = 0
                else:
                    if data == None:
                        length = 0
                        data = b''
                    else:
                        length = len(data)
                if length > 0:
                    file.write(length.to_bytes(2, byteorder='big'))
                    file.write(data)
                else:
                    if command:
                        file.write(b'\xFF\xFF')
                    else:
                        file.write(b'\x00\x00')

    def __str__(self):
        return str(self.config)

    def __repr__(self):
        return str(self.config)

class file_edit(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.higher = parent
        self.resize(640, 80)
        self.setFixedHeight(80)

        self.filename = QtWidgets.QLineEdit()
        self.filename.setReadOnly(True)
        self.filename.setText("No file selected")

        self.buttons = QtWidgets.QWidget()

        self.select_button = QtWidgets.QPushButton("Select file")
        self.select_button.clicked.connect(self.select_file)
        self.save_button = QtWidgets.QPushButton("Save file")
        self.save_button.clicked.connect(self.save_file)
        self.new_file_button = QtWidgets.QPushButton("New file")
        self.new_file_button.clicked.connect(self.new_file)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addWidget(self.select_button)
        self.buttons_layout.addWidget(self.save_button)
        self.buttons_layout.addWidget(self.new_file_button)
        self.buttons.setLayout(self.buttons_layout)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.filename)
        self.layout.addWidget(self.buttons)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
                 

    def select_file(self):
        file_input = QtWidgets.QFileDialog(parent=self,caption="Select file",directory=".",filter="Binary files (*.bin)")
        file_input.setFileMode(QtWidgets.QFileDialog.FileMode.AnyFile)
        file_input.setOption(QtWidgets.QFileDialog.Option.ReadOnly)
        file_input.setOption(QtWidgets.QFileDialog.Option.HideNameFilterDetails)
        if file_input.exec() == QtWidgets.QFileDialog.DialogCode.Accepted:
            self.filename.setText(file_input.selectedFiles()[0])
            self.higher.config = ConfigFile(file_input.selectedFiles()[0])

    def save_file(self):
        if self.filename.text() == "No file selected":
            return
        self.higher.config.write_config()
        
    def new_file(self):
        dialog = QtWidgets.QInputDialog()
        dialog.setLabelText("Enter filename")
        dialog.setTextValue("config.bin")
        ret = dialog.exec()
        if ret == QtWidgets.QDialog.DialogCode.Accepted:
            filename = dialog.textValue()
            self.filename.setText(filename)
            self.higher.config = ConfigFile(filename)
            self.higher.config.write_config()

class command_edit(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.higher = parent
        self.resize(640, 80)
        self.setFixedHeight(80)
        #self.setStyleSheet("border: 1px light gray;")

        self.combo_line = QtWidgets.QWidget()
        self.combo_line.setFixedHeight(40)

        self.command = QtWidgets.QComboBox()
        self.command.addItems(ConfigFile.datakeys)
        self.command.setCurrentText("None")
        self.command.setMaxVisibleItems(20)
        self.command.setStyleSheet("combobox-popup: 0; font-size: 12px; max-height: 300px; ")
        self.command.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.command.view().verticalScrollBar().setStyleSheet("QComboBox QAbstractItemView QScrollBar:vertical { width: 15px; margin: 0px 0px 0px 0px; }")
        self.command.currentIndexChanged.connect(self.command_changed)

        self.data = QtWidgets.QLineEdit()
        self.data.setPlaceholderText("Data")
        self.data.setMaxLength(0xFFFE*3) # 0xFFFE is the maximum data length, each byte is represented by 2 characters and a space
        self.data.setFixedWidth(400)
        self.data.editingFinished.connect(self.data_changed)

        self.command_active = QtWidgets.QCheckBox("Command active")
        self.command_active.setChecked(False)
        self.command_active.stateChanged.connect(self.data_changed)

        self.combo_line.layout = QtWidgets.QHBoxLayout()
        self.combo_line.layout.addWidget(self.command)
        self.combo_line.layout.addWidget(self.data)
        self.combo_line.setLayout(self.combo_line.layout)

        self.layout_widget = QtWidgets.QWidget()
        self.layout_widget.layout = QtWidgets.QVBoxLayout()
        self.layout_widget.layout.addWidget(self.combo_line)
        self.layout_widget.layout.addWidget(self.command_active)
        self.layout_widget.layout.setSpacing(0)
        self.layout_widget.setLayout(self.layout_widget.layout)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.layout_widget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def command_changed(self):
        command = self.command.currentText()
        if self.higher.config == None:
            self.data.setText("")
            return
        command_data = self.higher.config.get_config_value(command)
        if command_data != None and command_data[1] != None:
            if command_data[0]:
                self.command_active.setChecked(True)
                self.data.setText(' '.join([f"{byte:02X}" for byte in command_data[1]]))
            else:
                self.command_active.setChecked(False)
                self.data.setText("")
        else:
            self.data.setText("")

    def data_changed(self):
        command = self.command.currentText()
        if self.higher.config == None:
            return
        if not self.command_active.isChecked():
            self.higher.config.set_config_value(command, False, None)
            return
        data = self.data.text()
        data = bytes([int(byte, 16) for byte in data.split() if byte])
        self.higher.config.set_config_value(command, True, data)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Config file editor")
        self.width = 640
        self.height = 480
        self.setGeometry(0, 0, self.width, self.height)

        self.config = None

        self.file_edit = file_edit(parent=self)
        self.command_edit = command_edit(parent=self)
        
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.file_edit, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.command_edit, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)


        






if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())







