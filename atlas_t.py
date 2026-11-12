import sys, time, subprocess, glob
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
w = tk.Window(); w.showFullScreen(); app.processEvents()
def cek(ad): app.processEvents(); subprocess.run(['import', '-window', 'root', '/tmp/onizleme/atlas-%s.png' % ad])
def a1():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    w.open_pdf_path(sorted(glob.glob('pdf/*.pdf'))[0])
def a2():
    w.fit_page(); app.processEvents(); cek('0-once')
    pr = w.doc[w.page].rect; print('sayfa', pr.width, pr.height, 'zoom %.2f' % w.zoom, 'viewport', w.scroll.viewport().width())
    # sayfanın sol üst çeyreğinden küçük bir soru çerçevesi
    w.atlas_cerceve([(pr.width*0.08, pr.height*0.14), (pr.width*0.48, pr.height*0.30)])
def a3():
    pn = w.atlas_panel; vp = w.scroll.viewport()
    g = vp.mapTo(w, vp.rect().topLeft()); print('KENAR: panel x=%d, tahta alanı sağ kenarı=%d, örtüşme=%s' % (pn.x(), g.x() + vp.width(), pn.x() < g.x() + vp.width()), 'zoom %.2f' % w.zoom)
    r = w.atlas_son_cerceve[1]; k = w.board.scale
    print('soru ekranda %dx%d px, kalan alan %dx%d' % (r.width()*k, r.height()*k, vp.width(), vp.height()))
    cek('1-kenar'); pn.tam_ekran(True)
def a4():
    pn = w.atlas_panel; pm = pn.onizleme.pixmap(); print('TAM EKRAN önizleme %dx%d (eskiden en çok 900x230)' % (pm.width(), pm.height())); cek('2-tam'); pn.tam_ekran(False)
def a5():
    cek('3-geri-kenar'); w.atlas_panel.kapat()
def a6():
    print('kapandıktan sonra zoom %.2f, boşluk görünür: %s' % (w.zoom, w.atlas_bosluk.isVisible())); cek('4-kapali'); app.quit()
for t, f in ((1500, a1), (4000, a2), (5500, a3), (7000, a4), (8500, a5), (10000, a6)): QTimer.singleShot(t, f)
app.exec_()
