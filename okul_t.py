import sys, subprocess
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
w = tk.Window(); w.showFullScreen(); app.processEvents()
def a1():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    w.new_board()
def a2():
    p = [x for x in w.findChildren(tk.QWidget) if hasattr(x, 'bolumler') and hasattr(x, 'i_atlas')][0]; p.sekme(2); app.processEvents()
    bs = [b for b in p.yigin.currentWidget().findChildren(tk.QPushButton) if b.isVisible()]
    print('Okul sekmesi:', [(b.toolTip() or b.text()).strip()[:22] for b in bs])
    subprocess.run(['import', '-window', 'root', '-crop', '300x1080+0+0', '/tmp/onizleme/okul-sekme.png']); app.quit()
for t, f in ((1500, a1), (4000, a2)): QTimer.singleShot(t, f)
app.exec_()
