import sys, time, subprocess, glob
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
import os, shutil
dd = os.path.expanduser('~/.local/share/umal-tahta')
for ad in os.listdir(dd) if os.path.isdir(dd) else []:
    if ad != 'tahta.json':
        yol = os.path.join(dd, ad); (shutil.rmtree(yol, ignore_errors=True) if os.path.isdir(yol) else os.remove(yol))
QMessageBox.warning = staticmethod(lambda *a, **k: print('UYARI', a[1:]))
w = tk.Window(); w.resize(1200, 700); w.show(); app.processEvents()
QTimer.singleShot(700, w.showFullScreen)
def cek(ad): app.processEvents(); subprocess.run(['import', '-window', 'root', '/tmp/onizleme/cozum-%s.png' % ad])
def bilgi(ad):
    c = w.solution_origin['card']; k = w.board.scale; vp = w.scroll.viewport()
    print('%s: kart %dx%d birim (x0=%d) → ekranda %dx%d px; görünen alan %dx%d; yakınlık %.2f; düğme görünür %s' % (ad, c[2]-c[0], c[3]-c[1], c[0], (c[2]-c[0])*k, (c[3]-c[1])*k, vp.width(), vp.height(), w.zoom, w.soru_buyut_b.isVisible()))
def a1():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    w.open_pdf_path(sorted(glob.glob('pdf/*.pdf'))[0])
def a2():
    vp = w.scroll.viewport(); print('ALT ÇUBUK: görünen alan altı %d, çubuğun altı %d, fark %d px' % (vp.geometry().bottom(), w.nav.geometry().bottom(), vp.geometry().bottom() - w.nav.geometry().bottom()))
    pr = w.doc[w.page].rect
    w.make_solution([(pr.width*0.07, pr.height*0.12), (pr.width*0.49, pr.height*0.62)])   # uzun (dikey) soru
def a3(): bilgi('UZUN SORU'); cek('1-uzun'); w.soru_buyut()
def a4(): print('büyütülmüş: yakınlık %.2f, düğme: %s' % (w.zoom, w.soru_buyut_b.text())); cek('2-buyuk'); w.soru_buyut()
def a5(): print('geri: yakınlık %.2f, düğme: %s' % (w.zoom, w.soru_buyut_b.text())); w.return_to_pdf()
def a6():
    print('kitaba dönüş: düğme görünür %s' % w.soru_buyut_b.isVisible()); pr = w.doc[w.page].rect
    w.make_solution([(pr.width*0.07, pr.height*0.12), (pr.width*0.93, pr.height*0.24)])   # geniş (yatay) soru
def a7(): bilgi('GENİŞ SORU'); cek('3-genis'); app.quit()
for t, f in ((1500, a1), (4500, a2), (6500, a3), (8000, a4), (9500, a5), (11000, a6), (13000, a7)): QTimer.singleShot(t, f)
app.exec_()
