
import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLineEdit, QWidget, QVBoxLayout, QComboBox, QPushButton, QFileDialog, QLabel, QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt
from meloTTS import load_meloTTS_model

from pathlib import Path
import threading


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Spanish Speech Synthesizer'
        self.directory = None
        self.speed = 1.0
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0; /* Set background color */
            }
            QLineEdit, QComboBox {
                background-color: white; /* Set background color */
                border: 2px solid #a0a0a0; /* Set border color */
                border-radius: 5px; /* Set border radius */
                padding: 5px; /* Add padding */
            }
            QPushButton {
                background-color: #4CAF50; /* Set background color */
                color: white; /* Set text color */
                border: none; /* Remove border */
                border-radius: 5px; /* Set border radius */
                padding: 10px 20px; /* Add padding */
            }
            QPushButton:hover {
                background-color: #45a049; /* Darken background color on hover */
            }
            QPushButton:pressed {
                background-color: #3e8e41; /* Darken background color when pressed */
            }
        """)

        # Create main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 100, 50)  # Set layout margins

        # Create horizontal layout for text box and combo box
        h_layout = QHBoxLayout()

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText("Enter some text here")
        h_layout.addWidget(self.textbox)

        # Create speed combo box
        self.speed_combo = QComboBox(self)
        self.speed_combo.addItems([f"{x/10:.1f}" for x in range(4, 21)])
        self.speed_combo.setCurrentIndex(6)
        h_layout.addWidget(self.speed_combo)

        # Add horizontal layout to main layout
        main_layout.addLayout(h_layout)

        # Label to show uploaded file path
        self.file_path_label = QLabel('', self)
        main_layout.addWidget(self.file_path_label)

        # Create directory select button
        self.dir_select_btn = QPushButton('Select Destination Directory', self)
        self.dir_select_btn.clicked.connect(self.openDirectoryDialog)
        main_layout.addWidget(self.dir_select_btn)

        # Label to show selected directory
        self.dir_path_label = QLabel('', self)
        main_layout.addWidget(self.dir_path_label)

        # Create submit button
        self.submit_btn = QPushButton('Submit', self)
        self.submit_btn.clicked.connect(self.onSubmit)
        main_layout.addWidget(self.submit_btn)

        # Set main layout
        self.setLayout(main_layout)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Text File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            self.file_path_label.setText(fileName)

    def openDirectoryDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        self.directory = QFileDialog.getExistingDirectory(self, "Select Output Directory", "", options=options)
        if self.directory:
            self.dir_path_label.setText(self.directory)

    def synthesisProcess(self, text, directory, speed, progress_dialog):
        output_name = text.split(' ')[0]+'_speed_'+str(speed) + '.wav'
        output_path = Path(directory, output_name)
        model, speakers_ids, speed = load_meloTTS_model(speed=speed)
        model.tts_to_file(text, speakers_ids['ES'], output_path, speed=speed)
        progress_dialog.close()  # Close the progress dialog when synthesis is done

    def onSubmit(self):
        # Check if the text box is empty
        text = self.textbox.text()
        if not text or not self.directory:
            QMessageBox.warning(self, "Input Error", "Text box is empty or directory not selected")
            return

        # Get selected speed
        speed = float(self.speed_combo.currentText())

        # Show progress dialog
        progress_dialog = QProgressDialog("Synthesizing...", None, 0, 0, self)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setWindowTitle("Please wait")
        progress_dialog.setCancelButton(None)
        progress_dialog.show()

        # Run synthesis in a separate thread
        threading.Thread(target=self.synthesisProcess, args=(text, self.directory, speed, progress_dialog)).start()


   

def main():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
    
if __name__=='__main__':
    main()