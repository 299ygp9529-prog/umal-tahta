import sys
from PyQt5.QtWidgets import QApplication, QLabel
app = QApplication(['eta-keyboard']); w = QLabel('SAHTE PARDUS KLAVYESİ'); w.setWindowTitle('eta-keyboard'); w.setStyleSheet('background:#ccc;font-size:40px'); w.setGeometry(400, 600, 900, 300); w.show(); app.exec_()
