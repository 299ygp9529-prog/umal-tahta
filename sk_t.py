import sys, subprocess, time
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer
app = QApplication(sys.argv)
gor = lambda: subprocess.run(['xdotool', 'search', '--onlyvisible', '--classname', 'eta-keyboard'], capture_output=True, text=True).stdout.split()
p = subprocess.Popen(['python3', 'sahte_klavye.py']); time.sleep(3)
print('önce görünen sistem klavyesi:', gor())
class M(QWidget):
    kelebek = {'planlar': []}; data_dir = '/tmp'; board = type('B', (), {'finish': lambda s: None})()
    def ogrenci_ara(self, q): return []
m = M(); m.setGeometry(0, 0, 1920, 1080); m.show()
d = tk.OgrenciAraDialog(m); d.show()
def bitir():
    v = gor(); print('Atlas klavyesi açıkken görünen sistem klavyesi:', v, 'GIZLENDI' if not v else 'GORUNUYOR')
    print('Atlas penceresi görünür mü:', d.isVisible()); p.kill(); app.quit()
QTimer.singleShot(3000, bitir); app.exec_()
