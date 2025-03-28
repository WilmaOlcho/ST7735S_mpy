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
#[RGBSET amount (2 bytes)][DATA]

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
                "NVFCTR2", "NVFCTR3", "GMCTRP1", "GMCTRN1", "GCV", "RGBSET"]

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

class DescriptionArea(QtWidgets.QTextEdit):
    def __init__(self, parent=None, text=""):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFixedHeight(80)
        self.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)
        self.setStyleSheet("background-color: light gray; border: 1px solid light gray; font-size: 12px;")
        self.setPlainText("text")        
class command_edit(QtWidgets.QWidget):
    desctriptions = {
        "NOP": "No operation, delay in ms",
        "SWRESET": "Software reset, delay in ms",
        "RDDID": "Read display ID, delay in ms",
        "RDDST": "Read display status, delay in ms",
        "RDDPM": "Read display power mode, delay in ms",
        "RDDMADCTL": "Read memory access control, delay in ms",
        "RDDCOLMOD": "Read color mode, delay in ms",
        "RDDIM": "Read display image format, delay in ms",
        "RDDSM": "Read display signal mode, delay in ms",
        "SLPIN": "Sleep in & booster off, delay in ms",
        "SLPOUT": "Sleep out & booster on, delay in ms",
        "PTLON": "Partial mode on, delay in ms",
        "NORON": "Normal mode on, delay in ms",
        "INVOFF": "Display inversion off, delay in ms",
        "INVON": "Display inversion on, delay in ms",
        "GAMSET": "Gamma set, 00h-0Fh [1 byte]",
        "DISPOFF": "Display off, delay in ms",
        "DISPON": "Display on, delay in ms",
        "CASET": "Column address set, 0000h-FFFFh for xaddress start and 0000h-FFFFh for xaddress end [4 bytes big endian total]",
        "RASET": "Row address set 0000h-FFFFh for yaddress start and 0000h-FFFFh for yaddress end [4 bytes big endian total]",
        "RAMWR": "Memory write, 00h-FFh for data for each byte [1-n byte]",
        "RGBSET": "LUT table, 00h-1Fh for each byte, 32 bytes for red, 64 bytes for green, 32 bytes for blue [128 bytes total]",
        "RAMRD": "Memory read, delay in ms",
        "PTLAR": "Partial area, 0000h-FFFFh for  partial address start and 0000h-FFFFh for partial address end [4 bytes big endian total]",
        "SCRLAR": "Scroll area 0000h-FFFFh for top fixed area, 0000h-FFFFh for variable scroll area, 0000h-FFFFh for bottom fixed area [6 bytes big endian total]",
        "TEOFF": "Tearing effect off, delay in ms",
        "TEON": "Tearing effect on, 00h mode 1, 01h mode 2",
        "MADCTL": "Memory access control, 00h-FBh FBh masked [1 byte]",
        "VSCSAD": "Vertical scroll area start address, 0000h-FFFFh for top fixed area, 0000h-FFFFh for variable scroll area, 0000h-00FFh for bottom fixed area [2 bytes big endian total]",
        "IDMOFF": "Idle mode off, delay in ms",
        "IDMON": "Idle mode on, delay in ms",
        "COLMOD": "Color mode, 00h-07h [1 byte], 03h 12 bit color RGB444, 05h 16 bit color RGB565, 06h 18 bit color RGB666, 07h not used",
        "FRMCTR1": "Frame rate control 1, 00h-0Fh Period, 00h-3Fh Front Porch, 00h-3Fh Back Porch, [3 bytes]",
        "FRMCTR2": "Frame rate control 2, 00h-0Fh Period, 00h-3Fh Front Porch, 00h-3Fh Back Porch, [3 bytes]",
        "FRMCTR3": "Frame rate control 3, 00h-0Fh Period, 00h-3Fh Front Porch, 00h-3Fh Back Porch, [3 bytes]",
        "INVCTR": "Display inversion control, 00h-03h [1 byte] //TODO, 00h no inversion, 01h line inversion, 02h full inversion, 03h partial inversion",
        "PWCTR1": "Power control 1, 00h-E0h masked with E0h AVDD || 00h-1Fh masked with 1Fh VRHP, 00h-1Fh VRHN, 00h-C0h masked with C0h || 04h for MODE [3 bytes]",
        "PWCTR2": "Power control 2, 00h-C0h masked with C0h VGH2 || 00h-0Ch masked with 0Ch VGLS || 00h-03h VGHB [1 byte]",
        "PWCTR3": "Power control 3, 00h-C0h masked with C0h DCA[8:9] || 00h-38h masked with 38h SAPA || 00h-03h APA, 00h-FFh DCA[0:7] [2 bytes]",
        "PWCTR4": "Power control 4, 00h-C0h masked with C0h DCB[8:9] || 00h-38h masked with 38h SAPB || 00h-03h APB, 00h-FFh DCB[0:7] [2 bytes]",
        "PWCTR5": "Power control 5, 00h-C0h masked with C0h DCC[8:9] || 00h-38h masked with 38h SAPC || 00h-03h APC, 00h-FFh DCC[0:7] [2 bytes]",
        "VMCTR1": "VCOM control 1, 00h-3Fh VCOM [1 byte]",
        "VMOFCTR": "VCOM offset control, 00h-1Fh VCOM offset [1 byte]",
        "WRID1": "Write ID 1, reserved [1 byte]",
        "WRID2": "Write ID 2, 00h-7Fh ID2 [1 byte]",
        "WRID3": "Write ID 3, 00h-7Fh ID3 [1 byte]",
        "NVFCTR1": "NVM Control Status, bits (VMF_EN << 6 || ID2_EN << 5 || EXT_R) && 61h [1byte]",
        "RDID1": "Read ID 1, delay in ms",
        "RDID2": "Read ID 2, delay in ms",
        "RDID3": "Read ID 3, delay in ms",
        "NVFCTR2": "NVM Read Command, F5h A5h [2 bytes]",
        "NVFCTR3": "NVM Write Command, 00h-FFh A5h [2 bytes]",
        "GMCTRP1": "Gamma curve positive, 00h-1Fh for each byte: [VRFP][VOS0P][PKP0]...[PKP9][SELV0P][SELV1P][SELV62P][SELV63P] [16 bytes total]",
        "GMCTRN1": "Gamma curve negative, 00h-1Fh for each byte: [VRF0N][VOS0N][PKN0]...[PKN9][SELV0N][SELV1N][SELV62N][SELV63N] [16 bytes total]",
        "GCV": "Gate Clock, bits (GCV_Enable0 << 7 || GCV_Enable1 << 6 || CLK_variable0 << 4 || CLK_Variable1 << 3) && D8h [1 byte]",
    }
    def __init__(self, parent=None):
        super().__init__(parent)
        self.higher = parent
        self.resize(640, 80)
        self.setFixedHeight(160)

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

        self.description = DescriptionArea()

        self.combo_line.layout = QtWidgets.QHBoxLayout()
        self.combo_line.layout.addWidget(self.command)
        self.combo_line.layout.addWidget(self.data)
        self.combo_line.setLayout(self.combo_line.layout)

        self.layout_widget = QtWidgets.QWidget()
        self.layout_widget.layout = QtWidgets.QVBoxLayout()
        self.layout_widget.layout.addWidget(self.combo_line)
        self.layout_widget.layout.addWidget(self.command_active)
        self.layout_widget.layout.addWidget(self.description)
        self.layout_widget.layout.setSpacing(0)
        self.layout_widget.setLayout(self.layout_widget.layout)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.layout_widget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def command_changed(self):
        command = self.command.currentText()
        self.description.setPlainText(self.desctriptions.get(command, ""))
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







