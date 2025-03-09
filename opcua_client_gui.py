import asyncio
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QPlainTextEdit, QLabel, QLineEdit
)
from asyncua import Client

class OPCUAClientGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('OPC UA Client')
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        self.url_label = QLabel("OPC UA Server URL:")
        layout.addWidget(self.url_label)

        self.url_input = QLineEdit("opc.tcp://localhost:4840")
        layout.addWidget(self.url_input)

        self.connect_button = QPushButton('Connect and Read')
        self.connect_button.clicked.connect(self.connect_and_read)
        layout.addWidget(self.connect_button)

        self.output_text = QPlainTextEdit()
        layout.addWidget(self.output_text)

        self.setLayout(layout)
        self.show()

    def connect_and_read(self):
        url = self.url_input.text()
        self.output_text.clear()
        asyncio.run(self.read_opcua_data(url))

    async def read_opcua_data(self, url):
        try:
            async with Client(url=url) as client:
                uri = "http://example.com"
                idx = await client.get_namespace_index(uri)

                sensor_folder = await client.nodes.objects.get_child(
                    ["2:SensorValues"]
                )

                children = await sensor_folder.get_children()

                for child in children:
                    if await child.read_node_class() == 2:
                        value = await child.read_value()
                        node_name = await child.read_browse_name()
                        self.output_text.appendPlainText(f"{node_name.Name}: {value}")

        except Exception as e:
            self.output_text.appendPlainText(f"Error: {e}")

if __name__ == '__main__':
    app = QApplication([])
    client_gui = OPCUAClientGUI()
    app.exec_()
