import sys, subprocess
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
w = tk.Window(); w.showFullScreen(); app.processEvents()
ham = r"Ekranda $\frac{\log(a+1)}{\log 3} = \log_{\frac{1}{2}} 4$ denkleminin çözümü ile ilgili 2. soru var. Önce tabanları eşitleyelim."
print('ilk cümle:', tk.atlas_ilk_cumle(ham)); print('eski düz yazı:', tk.latex_duz(ham)[:90])
def cek(ad): app.processEvents(); subprocess.run(['import', '-window', 'root', '/tmp/onizleme/balon-%s.png' % ad])
def a1():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    w.new_board() if hasattr(w, 'new_board') else None
def a2():
    ay = w.atlas_yuzen; ay.show(); vp = w.scroll.viewport().geometry()
    ay.move(vp.x() + 20, vp.y() + 300)   # maskot sol kenarda (fotoğraftaki durum)
    ay.balon_goster(tk.atlas_ilk_cumle(ham), ['Soruyu çöz', 'Adım adım anlat', 'Çözümü kontrol et', 'Başka bir şey sor…'])
    b = ay.balon; print('SOL KENAR: maskot', ay.geometry().getRect(), 'balon', b.geometry().getRect(), 'üst üste:', ay.geometry().intersects(b.geometry())); cek('1-sol')
    ay.move(vp.right() - 150, vp.bottom() - 150); ay.balon_goster(tk.atlas_ilk_cumle(ham), ['Soruyu çöz', 'Adım adım anlat', 'Çözümü kontrol et', 'Başka bir şey sor…'])
    print('SAĞ ALT: üst üste:', ay.geometry().intersects(b.geometry())); cek('2-sag'); app.quit()
QTimer.singleShot(1500, a1); QTimer.singleShot(3500, a2)
app.exec_()
