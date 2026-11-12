import sys, subprocess, glob, os, shutil
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
dd = os.path.expanduser('~/.local/share/umal-tahta')
for ad in os.listdir(dd) if os.path.isdir(dd) else []:
    if ad != 'tahta.json':
        yol = os.path.join(dd, ad); (shutil.rmtree(yol, ignore_errors=True) if os.path.isdir(yol) else os.remove(yol))
QMessageBox.warning = staticmethod(lambda *a, **k: print('UYARI', a[1:]))
w = tk.Window(); w.showFullScreen(); app.processEvents()
def cek(ad): app.processEvents(); subprocess.run(['import', '-window', 'root', '/tmp/onizleme/sig-%s.png' % ad])
def durum(ad):
    pn = w.atlas_panel; vp = w.scroll.viewport(); k = w.board.scale; px = vp.mapFromGlobal(pn.mapToGlobal(tk.QPoint(0, 0))).x()
    acik = min(vp.width(), px) if px > 0 else vp.width()
    s = '%s: yakınlık %.2f; açık alan %dx%d' % (ad, w.zoom, acik, vp.height())
    o = getattr(w, 'solution_origin', None)
    if o and o.get('card') and ((w.doc.metadata or {}).get('keywords') or '') == 'UMAL-solution':
        c = o['card']; sol = c[0]*k - w.scroll.horizontalScrollBar().value(); ust = c[1]*k - w.scroll.verticalScrollBar().value()
        gw = (c[2]-c[0])*k; gh = (c[3]-c[1])*k
        s += '; soru kartı ekranda x %d..%d, y %d..%d → %s' % (sol, sol+gw, ust, ust+gh, 'TAM GÖRÜNÜYOR' if sol >= 0 and ust >= 0 and sol+gw <= acik and ust+gh <= vp.height() else 'KESİK')
    print(s)
def a1():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    w.open_pdf_path(sorted(glob.glob('pdf/*.pdf'))[0])
def a2():
    pr = w.doc[w.page].rect; w.fit_page()
    w.atlas_cerceve([(pr.width*0.08, pr.height*0.14), (pr.width*0.30, pr.height*0.20)])   # önce küçük bir çerçeve (eski seçim)
def a3(): durum('1) ÇERÇEVE (kitap)'); cek('1-cerceve'); w.atlas_panel.kapat()
def a4():
    pr = w.doc[w.page].rect; print('panel kapandı: yakınlık %.2f' % w.zoom)
    w.make_solution([(pr.width*0.07, pr.height*0.12), (pr.width*0.93, pr.height*0.24)])
def a5():
    ay = w.atlas_yuzen; ay.istek_gonder = lambda: None; ay.dokundu()
def a6(): w.atlas_yuzen.secildi('Başka bir şey sor…')
def a7(): durum('2) ÇÖZÜM ALANI + Atlas (hatanın olduğu durum)'); cek('2-cozum'); w.atlas_panel.kapat()
def a8():
    print('kapandı: yakınlık %.2f' % w.zoom); w.atlas_sor_ac()   # yazarak sorma: görünüm değişmemeli
def a9(): durum('3) yazarak sor'); w.atlas_panel.kapat()
def a10(): app.quit()
for t, f in ((1500, a1), (4500, a2), (6000, a3), (7000, a4), (9000, a5), (10000, a6), (11500, a7), (12500, a8), (13500, a9), (14200, a10)): QTimer.singleShot(t, f)
app.exec_()
