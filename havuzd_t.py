import sys, subprocess, os, time
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
tk.KELEBEK_URLS = (); tk.KELEBEK_FOTO_URLS = ()
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
os.makedirs(tk.HAVUZ_DIR, exist_ok=True)
for n in ('Test - 9. Sınıf Matematik · Üslü İfadeler (Örnek Öğretmen).pdf', 'Test - 12. Sınıf Fizik · Elektrik (Deneme Hoca).pdf', 'Ders kitabı.pdf'):
    open(os.path.join(tk.HAVUZ_DIR, n), 'wb').write(b'%PDF-1.4\n')
w = tk.Window(); w.showFullScreen(); app.processEvents(); w.board_info = lambda: {'sinif': 'Öğretmenler odası'}
def a1():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    w.test_havuz_tick(); print('tick hatasız, iniyor:', getattr(w, '_test_iniyor', None))
    d = tk.HavuzDialog(w); d.show(); app.processEvents(); QTimer.singleShot(1500, lambda: (subprocess.run(['import', '-window', 'root', '/tmp/onizleme/havuz.png']), d.accept(), app.quit()))
QTimer.singleShot(2000, a1); app.exec_(); print('bitti')
