import sys, os, datetime, time, subprocess
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer
app = QApplication(sys.argv); tk.install_turkish(app) if hasattr(tk, 'install_turkish') else None
m = QWidget(); m.setStyleSheet('background:#101d33;'); m.setGeometry(0, 0, 1000, 620); m.show()
ws = []
for i, (w, h, t) in enumerate(((300, 420, (10, 10, 36)), (260, 360, (9, 22, 5)), (300, 110, (9, 22, 5)), (340, 560, (15, 47, 52)))):
    c = tk.PanelClock(m); c.now = datetime.datetime(2026, 11, 11, *t); c.setGeometry(10 + sum(x.width() + 14 for x in ws), 10, w, h); c.show(); ws.append(c)
def bitir():
    c = ws[0]; t0 = time.perf_counter()
    for _ in range(50): c.repaint()
    print('SAAT çizim ortalaması %.2f ms (kadran saklı)' % ((time.perf_counter() - t0)*1000/50))
    subprocess.run(['import', '-window', 'root', '/tmp/onizleme/saat.png']); app.quit()
QTimer.singleShot(1500, bitir); app.exec_()
