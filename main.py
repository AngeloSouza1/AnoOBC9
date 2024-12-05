import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QGraphicsScene,
    QGraphicsView, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsRectItem,
    QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtGui import QPixmap, QColor, QPolygonF, QPen
from PyQt5.QtCore import QTimer, QRectF, Qt, QPointF, QThread, pyqtSignal
from contagem_regressiva import contagem_regressiva


class ContagemThread(QThread):
    """Thread separada para executar a contagem regressiva."""
    atualizar = pyqtSignal(int)  # Sinal para atualizar o valor no QLabel
    finalizar = pyqtSignal()  # Sinal para indicar o término da contagem

    def __init__(self, segundos):
        super().__init__()
        self.segundos = segundos

    def run(self):
        """Executa a contagem regressiva usando o módulo."""
        try:
            contagem_regressiva(
                self.segundos,
                lambda valor: self.atualizar.emit(valor)  # Emite o valor através do sinal
            )
        except ValueError:
            pass
        self.finalizar.emit()  # Emite o sinal de término


class Confetti:
    """Classe que cria confetes de diferentes formas e gerencia sua posição."""

    def __init__(self, x, y, size, color, speed, shape="circle"):
        """
        Inicializa um confete com os atributos fornecidos.

        Args:
            x (int): Posição inicial no eixo x.
            y (int): Posição inicial no eixo y.
            size (int): Tamanho do confete.
            color (tuple): Cor do confete em formato RGB.
            speed (float): Velocidade vertical do confete.
            shape (str): Forma do confete ('circle', 'rect', 'triangle').
        """
        self.shape = shape
        self.color = QColor(*color)
        self.speed = speed

        if shape == "circle":
            self.item = QGraphicsEllipseItem(QRectF(x, y, size, size))
        elif shape == "rect":
            self.item = QGraphicsRectItem(QRectF(x, y, size, size))
        elif shape == "triangle":
            self.item = QGraphicsPolygonItem(self.create_triangle(x, y, size))
        else:
            self.item = QGraphicsEllipseItem(QRectF(x, y, size, size))  # Padrão: círculo

        self.item.setBrush(self.color)
        self.item.setPen(QPen(Qt.NoPen))  # Contorno invisível

    def create_triangle(self, x, y, size):
        """Cria um triângulo isósceles."""
        return QPolygonF(
            [
                QPointF(x, y),
                QPointF(x + size, y + size),
                QPointF(x - size, y + size),
            ]
        )

    def update_position(self, width, height):
        """Atualiza a posição do confete e reinicia no topo se sair da tela."""
        self.item.moveBy(0, self.speed)
        if self.item.y() > height:
            self.item.setY(-10)
            self.item.setX(random.randint(0, width))


class ContagemAnoNovoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contagem Regressiva para o Ano Novo 🎉")
        self.setGeometry(100, 100, 904, 508)
        self.contando = False

        # Background
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("assets/background.jpg"))
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, 904, 508)

        # Label para contagem regressiva
        self.contagem_label = QLabel(self)
        self.contagem_label.setStyleSheet("""
            QLabel {
                font-size: 60px;
                font-weight: bold;
                color: white;
                background-color: transparent;
            }
        """)
        self.contagem_label.setAlignment(Qt.AlignCenter)
        self.contagem_label.setGeometry(0, 50, self.width(), 70)
        self.contagem_label.hide()

        # Configuração de confetes
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 904, 508)
        self.view.setStyleSheet("background: transparent;")
        self.view.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.confetes = []
        self.timer_confetes = QTimer()
        self.timer_confetes.timeout.connect(self.atualizar_confetes)

        # Rodapé
        self.init_footer()

    def init_footer(self):
        """Configura o rodapé com o input e o botão."""
        footer_widget = QWidget(self)
        footer_widget.setGeometry(0, self.height() - 60, self.width(), 60)
        footer_layout = QHBoxLayout(footer_widget)

        # Input estilizado
        self.entrada_segundos = QLineEdit(self)
        self.entrada_segundos.setPlaceholderText("Digite os segundos (1-60)")
        self.entrada_segundos.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                padding: 5px;
                border: 2px solid #0078d7;
                border-radius: 10px;
                background-color: #f4f4f4;
                color: #333;
                text-align: center;
            }
        """)
        self.entrada_segundos.setFixedWidth(200)

        # Botão estilizado
        self.botao_iniciar = QPushButton(self)
        self.botao_iniciar.setText("Iniciar")
        self.botao_iniciar.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                color: white;
                background-color: #28a745;
                border: none;
                border-radius: 10px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        self.botao_iniciar.setFixedSize(100, 40)
        self.botao_iniciar.clicked.connect(self.iniciar_contagem)

        footer_layout.addStretch()
        footer_layout.addWidget(self.entrada_segundos)
        footer_layout.addWidget(self.botao_iniciar)
        footer_layout.addStretch()

        footer_widget.setLayout(footer_layout)

    def iniciar_contagem(self):
        if self.contando:
            return

        try:
            segundos = int(self.entrada_segundos.text())
            if not (1 <= segundos <= 60):
                self.mostrar_mensagem("Por favor, insira um número entre 1 e 60.")
                return

            self.contando = True
            self.entrada_segundos.setEnabled(False)
            self.botao_iniciar.setEnabled(False)

            self.contagem_label.setText("")
            self.contagem_label.show()

            # Configura e conecta a thread da contagem regressiva
            self.thread = ContagemThread(segundos)
            self.thread.atualizar.connect(self.atualizar_label_contagem)
            self.thread.finalizar.connect(self.finalizar_contagem)
            self.thread.start()

        except ValueError:
            self.mostrar_mensagem("Por favor, insira um número válido.")

    def atualizar_label_contagem(self, valor):
        """Atualiza o label da contagem regressiva."""
        self.contagem_label.setText(str(valor))

    def finalizar_contagem(self):
        """Finaliza a contagem e inicia os confetes."""
        self.contagem_label.setText("🎉 Feliz Ano Novo!")
        self.contagem_label.setStyleSheet("""
        QLabel {
            font-size: 60px;
            font-weight: bold;
            color: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(255, 255, 255, 255),
                stop:1 rgba(240, 240, 240, 255)
            );
            background-color: transparent;
        }
    """)
        self.iniciar_confetes()
        QTimer.singleShot(5000, self.resetar)

    def iniciar_confetes(self):
        largura = self.width()
        altura = self.height()

        self.confetes = [
            Confetti(
                random.randint(0, largura),
                random.randint(-altura, 0),
                random.randint(5, 10),
                random.choice([(255, 215, 0), (255, 69, 0), (50, 205, 50), (30, 144, 255)]),
                random.uniform(2, 5),
                random.choice(["circle", "rect", "triangle"]),
            )
            for _ in range(450)
        ]
        for confete in self.confetes:
            self.scene.addItem(confete.item)
        self.timer_confetes.start(30)

    def atualizar_confetes(self):
        largura = self.width()
        altura = self.height()
        for confete in self.confetes:
            confete.update_position(largura, altura)

    def resetar(self):
        """Reseta a aplicação."""
        self.timer_confetes.stop()
        self.scene.clear()
        self.confetes = []
        self.contagem_label.hide()
        self.entrada_segundos.setEnabled(True)
        self.botao_iniciar.setEnabled(True)
        self.entrada_segundos.clear()
        self.contando = False

    def mostrar_mensagem(self, mensagem):
        QMessageBox.warning(self, "Erro", mensagem)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = ContagemAnoNovoApp()
    janela.show()
    sys.exit(app.exec())
