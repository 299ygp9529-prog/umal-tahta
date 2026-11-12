import sys, subprocess, glob
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
w = tk.Window(); w.showFullScreen(); app.processEvents()
def cek(ad): app.processEvents(); subprocess.run(['import', '-window', 'root', '-crop', '300x1080+0+0', '/tmp/onizleme/saatp-%s.png' % ad])
pn = [None]
def a1():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    w.new_board()
def a2():
    p = [x for x in w.findChildren(tk.QWidget) if hasattr(x, 'bolumler') and hasattr(x, 'i_atlas')][0]; pn[0] = p
    sa = [x for x in w.findChildren(tk.QWidget) if type(x).__name__ in ('SaatWidget', 'PanelSaat', 'Saat') or (hasattr(x, '_kadran') and hasattr(x, 'tik'))]
    print('saat widget:', [(type(x).__name__, x.width(), x.height()) for x in sa]); cek('1-kapali')
    p.bolumler[0][0].setChecked(True)
def a3():
    sa = [x for x in w.findChildren(tk.QWidget) if hasattr(x, '_kadran') and hasattr(x, 'tik')]
    print('Akıllı araçlar açık → saat:', [(x.width(), x.height(), x.isVisible()) for x in sa]); cek('2-acik'); print('düğmeler:', [(b.text().strip(), b.width(), b.fontMetrics().horizontalAdvance(b.text()) + 22 + 20) for b in pn[0].bolumler[0][1].findChildren(tk.QPushButton)]); app.quit()
for t, f in ((1500, a1), (4000, a2), (5200, a3)): QTimer.singleShot(t, f)
app.exec_()
