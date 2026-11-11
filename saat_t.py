import sys, os, datetime, time, subprocess
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
app = QApplication(sys.argv)
m = QWidget(); m.setStyleSheet('background:#101d33;'); m.setGeometry(0, 0, 1000, 420); m.show()
ws = []
class T:   # ışığın üç anı
    def __init__(s, f): s.f = f
for i, f in enumerate((.3, .7, .8, .9)):
    c = tk.PanelClock(m); c.now = datetime.datetime(2026, 11, 11, 10, 0, 33); c.setGeometry(10 + i*245, 10, 240, 400); c.show(); ws.append((c, f))
def bitir():
    gercek = time.time
    for c, f in ws:
        tk.time.time = lambda f=f: 1200.0*6 + f*6.0
        c.repaint()
    tk.time.time = gercek
    c = ws[0][0]; t0 = time.perf_counter()
    for _ in range(50): c.repaint(c._logo_r)
    print('IŞIK karesi ortalaması %.2f ms (yalnız logo bölgesi)' % ((time.perf_counter() - t0)*1000/50))
    subprocess.run(['import', '-window', 'root', '/tmp/onizleme/saat.png']); app.quit()
QTimer.singleShot(1500, bitir); app.exec_()
