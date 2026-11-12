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
    w.new_board(); w.atlas_sor_ac(); pn = w.atlas_panel
    pn.metin.setPlainText('\n'.join('%d. Adım: $\\log_3 x \\cdot \\log_3 x = 4$ olduğundan $x = 9$ ve $x = \\frac{1}{9}$ bulunur, sonuç kontrol edilir.' % i for i in range(1, 14)) + '\nCevap: C) 1', True)
def a2():
    pn = w.atlas_panel; sb = pn.metin.alan.verticalScrollBar(); app.processEvents()
    print('çubuk görünür:', sb.isVisible(), '| genişlik', sb.width(), 'px | metin resmi', pn.metin.resim.width(), '+ çubuk', sb.width(), '<= alan', pn.metin.alan.width())
    g = pn.mapToGlobal(pn.rect().topLeft()); subprocess.run(['import', '-window', 'root', '-crop', '%dx1080+%d+0' % (pn.width(), g.x()), '/tmp/onizleme/cubuk.png']); app.quit()
for t, f in ((1500, a1), (3500, a2)): QTimer.singleShot(t, f)
app.exec_()
