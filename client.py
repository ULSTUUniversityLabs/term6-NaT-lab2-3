import os
import sys
import socket
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox

HOST = '127.0.0.1'
PORT = 12344


class ClientApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

    def initUI(self):
        self.setWindowTitle('Client')
        self.setGeometry(300, 300, 600, 400)

        self.command_input = QtWidgets.QLineEdit(self)
        self.command_input.setPlaceholderText("Введите команду...")

        self.send_button = QtWidgets.QPushButton("Отправить", self)
        self.send_button.clicked.connect(self.send_command)

        self.file_button = QtWidgets.QPushButton("Выбрать файл", self)
        self.file_button.clicked.connect(self.select_file)

        self.path_input = QtWidgets.QLineEdit(self)
        self.path_input.setPlaceholderText("Путь до файла...")

        self.output_area = QtWidgets.QTextEdit(self)
        self.output_area.setReadOnly(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.command_input)
        layout.addWidget(self.send_button)
        layout.addWidget(self.file_button)
        layout.addWidget(self.path_input)
        layout.addWidget(self.output_area)

        self.setLayout(layout)

        self.selected_file = None

    def select_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "", options=options)
        self.path_input.setText(file_name)
        if file_name:
            self.selected_file = file_name
            self.output_area.append(f"Выбран файл: {self.selected_file}")

    def clear_file(self):
        self.selected_file = None
        self.output_area.append("Файл очищен.")

    def send_command(self):
        command = self.command_input.text()
        command_type = command.lower().split()[0]
        if (command_type == "encrypt" or command_type == "decrypt") and len(command.split()) == 3 and command.split()[2] == "[file]":
            password = command.split()[1]
            
            path = self.path_input.text()
            if path is None or len(path) == 0:
                QMessageBox.warning(self, "Ошибка", "Выберите файл для отправки.")
                return
            
            with open(path, "r") as f:
                text_data = f.read()
            
            command = f"{command_type} {password} {text_data}"
        elif (command_type == "encrypt" or command_type == "decrypt") and len(command.split()) > 2:
            password = command.split()[1]
            text_data = " ".join(command.split()[2:])
            command = f"{command_type} {password} {text_data}"
        elif command_type == "encrypt" or command_type == "decrypt":
            QMessageBox.warning(self, "Ошибка", "Неверные аргументы.")
            return

        command += chr(0x10)

        self.s.sendall(command.encode())
        response = self.s.recv(1024).decode().strip()

        if command_type == "bye":
            self.s.close()
            QtWidgets.qApp.quit()

        if command_type == "encrypt" or command_type == "decrypt":
            if not all(c.isprintable() for c in response):
                self.output_area.append(f"Ответ сервера: не удалось расшифровать")
                return

            local_path = os.path.join(os.getcwd(), 'lab2') + f".{command_type}"
            with open(local_path, 'w') as f:
                f.write(response)
            self.output_area.append(f"Ответ сервера: {str(response)}")
        else:
            self.output_area.append(f"Ответ сервера: {response.decode('utf-8', errors='replace')}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    client = ClientApp()
    client.show()
    sys.exit(app.exec_())
