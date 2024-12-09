import sys
import serial
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QGridLayout, QWidget, QProgressBar
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtChart import QChartView, QLineSeries, QChart
from PyQt5.QtGui import QPainter


# Função para tentar conectar com o Arduino
def conectar_arduino():
    try:
        # Tentar abrir a conexão com o Arduino (substituir "COM3" pela porta correta)
        arduino = serial.Serial('COM3', 9600, timeout=1)
        return arduino
    except:
        return None


# Classe principal da interface
class DroneControl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Controle do Drone")
        self.setGeometry(100, 100, 800, 600)  # Aumentar o tamanho da janela

        # Variáveis
        self.arduino = conectar_arduino()

        # Status de conexão
        self.status_label = QLabel("Tentando conectar ao Arduino")
        if self.arduino:
            self.status_label.setText("Conectado ao Arduino")
        else:
            self.status_label.setText("Arduino não encontrado")

        # Indicador de bateria
        self.battery_label = QLabel("Bateria: Esperando resposta do Arduino")
        self.battery_bar = QProgressBar()
        self.battery_bar.setValue(0)  # Bateria inicial

        # Gráfico de telemetria
        self.telemetry_label = QLabel("Telemetria do Drone")
        self.altitude_series = QLineSeries()
        self.speed_series = QLineSeries()

        self.chart = QChart()
        self.chart.addSeries(self.altitude_series)
        self.chart.addSeries(self.speed_series)
        self.chart.createDefaultAxes()
        self.chart.setTitle("Altura e Velocidade")

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Botões
        self.btn_decolar = QPushButton("Decolar (t)")
        self.btn_pousar = QPushButton("Pousar (l)")
        self.btn_frente = QPushButton("Frente (i)")
        self.btn_tras = QPushButton("Trás (k)")
        self.btn_esquerda = QPushButton("Esquerda (a)")
        self.btn_direita = QPushButton("Direita (d)")
        self.btn_subir = QPushButton("Subir (w)")
        self.btn_descer = QPushButton("Descer (s)")

        # Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.battery_label, 0, 0, 1, 3)
        self.layout.addWidget(self.battery_bar, 1, 0, 1, 3)
        self.layout.addWidget(self.telemetry_label, 2, 0, 1, 3)
        self.layout.addWidget(self.chart_view, 3, 0, 1, 3)
        self.layout.addWidget(self.btn_subir, 4, 1)
        self.layout.addWidget(self.btn_esquerda, 5, 0)
        self.layout.addWidget(self.btn_frente, 5, 1)
        self.layout.addWidget(self.btn_direita, 5, 2)
        self.layout.addWidget(self.btn_tras, 6, 1)
        self.layout.addWidget(self.btn_pousar, 7, 1)
        self.layout.addWidget(self.btn_decolar, 7, 0)
        self.layout.addWidget(self.btn_descer, 7, 2)
        self.layout.addWidget(self.status_label, 8, 0, 1, 3)

        # Conexão dos botões
        self.btn_decolar.clicked.connect(lambda: self.enviar_comando("takeoff"))
        self.btn_pousar.clicked.connect(lambda: self.enviar_comando("land"))
        self.btn_frente.clicked.connect(lambda: self.enviar_comando("forward"))
        self.btn_tras.clicked.connect(lambda: self.enviar_comando("backward"))
        self.btn_esquerda.clicked.connect(lambda: self.enviar_comando("left"))
        self.btn_direita.clicked.connect(lambda: self.enviar_comando("right"))
        self.btn_subir.clicked.connect(lambda: self.enviar_comando("up"))
        self.btn_descer.clicked.connect(lambda: self.enviar_comando("down"))

        # Janela central
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Timer para atualizar dados periodicamente
        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_telemetria)
        self.timer.timeout.connect(self.atualizar_bateria)
        self.timer.start(1000)  # Atualiza a cada 1 segundo

        # Aplicar o estilo futurista
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2e2e2e;
                color: white;
                font-family: 'Arial', sans-serif;
            }

            QPushButton {
                background-color: #6e4b3c;
                color: white;
                border-radius: 8px;
                font-size: 14px;
                padding: 10px;
                min-width: 120px;
            }

            QPushButton:hover {
                background-color: #8c6a4f;
            }

            QLabel {
                font-size: 16px;
                color: #dcdcdc;
            }

            QProgressBar {
                background-color: #3a3a3a;
                border-radius: 5px;
                text-align: center;
                color: white;
            }

            QProgressBar::chunk {
                background-color: #a0522d;
                border-radius: 5px;
            }

            QGridLayout {
                margin: 20px;
                spacing: 10px;
            }

            QLabel, QPushButton {
                margin: 5px;
            }
        """)

    # Função para enviar comandos ao Arduino
    def enviar_comando(self, comando):
        if self.arduino and self.arduino.is_open:
            self.arduino.write(comando.encode())
            self.status_label.setText(f"Comando enviado: {comando}")
        else:
            self.status_label.setText("Arduino desconectado")

    # Função para atualizar a bateria
    def atualizar_bateria(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.write("battery".encode())  # Envia comando para verificar bateria
            resposta = self.arduino.readline().decode().strip()  # Lê a resposta
            if resposta.isdigit():  # Verifica se a resposta é um número
                bateria = int(resposta)
                self.battery_bar.setValue(bateria)
                self.battery_label.setText(f"Bateria: {bateria}%")
            else:
                self.status_label.setText("Erro ao ler bateria")

    # Função para atualizar a telemetria (altitude, velocidade, etc.)
    def atualizar_telemetria(self):
        if self.arduino and self.arduino.is_open:
            # Simulando valores de telemetria (substitua isso com dados reais)
            altitude = random.randint(0, 100)  # Simulação de altura
            speed = random.randint(0, 50)  # Simulação de velocidade

            # Adiciona novos dados ao gráfico
            self.altitude_series.append(len(self.altitude_series), altitude)
            self.speed_series.append(len(self.speed_series), speed)

            self.telemetry_label.setText(f"Altitude: {altitude} m | Velocidade: {speed} km/h")

    # Eventos de teclado
    def keyPressEvent(self, event):
        key_map = {
            Qt.Key_W: ("up", self.btn_subir),
            Qt.Key_S: ("down", self.btn_descer),
            Qt.Key_A: ("left", self.btn_esquerda),
            Qt.Key_D: ("right", self.btn_direita),
            Qt.Key_I: ("forward", self.btn_frente),
            Qt.Key_K: ("backward", self.btn_tras),
            Qt.Key_T: ("takeoff", self.btn_decolar),
            Qt.Key_L: ("land", self.btn_pousar),
        }
        if event.key() in key_map:
            comando, button = key_map[event.key()]
            self.enviar_comando(comando)
            button.setStyleSheet("background-color: lightgreen;")

    def keyReleaseEvent(self, event):
        key_map = {
            Qt.Key_W: self.btn_subir,
            Qt.Key_S: self.btn_descer,
            Qt.Key_A: self.btn_esquerda,
            Qt.Key_D: self.btn_direita,
            Qt.Key_I: self.btn_frente,
            Qt.Key_K: self.btn_tras,
            Qt.Key_T: self.btn_decolar,
            Qt.Key_L: self.btn_pousar,
        }
        if event.key() in key_map:
            button = key_map[event.key()]
            button.setStyleSheet("")

    # Finalizar conexão ao fechar
    def closeEvent(self, event):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()


# Inicialização do aplicativo
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DroneControl()
    window.show()
    sys.exit(app.exec_())
