import sys, subprocess, time, shutil, types, gc
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication, QDialog, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
print('sayfa önbelleği sınırı MB', tk.SAYFA_OB_SINIR//1024//1024, 'bellek kB', tk._bellek_kb())
tk._pencere_temizligi()
class D(tk.OgrenciAraDialog if False else QDialog): pass
olen = []
def ac():
    d = D(); d.destroyed.connect(lambda: olen.append(1)); QTimer.singleShot(200, d.accept); r = d.exec_(); print('exec döndü', r, 'hâlâ kullanılabilir:', d.result())
def son():
    print('PENCERE SILINDI' if olen else 'PENCERE DURUYOR', len(olen))
    # bellek boşaltma
    for i in range(40): tk.SAYFA_OB[i] = QImage(1920, 1080, QImage.Format_RGB888)
    r0 = tk._bellek_kb()[2]; tk.bellek_bosalt('deneme'); r1 = tk._bellek_kb()[2]
    print('Atlas belleği MB: önce %d, sonra %d' % (r0//1024, r1//1024), 'önbellek', len(tk.SAYFA_OB))
    w = types.SimpleNamespace(board=types.SimpleNamespace(active=None)); gercek = tk._bellek_kb
    tk._bellek_kb = lambda: (4000000, 200000, 500000); tk.bellek_bekcisi(w); print('bekçi (boş bellek az) çalıştı:', tk._BELLEK_SON[1])
    tk._bellek_kb = lambda: (4000000, 2000000, 300000); tk._BELLEK_SON[0] = 0; tk.bellek_bekcisi(w); print('bekçi (bellek bol) çalışmadı:', tk._BELLEK_SON[1])
    tk._bellek_kb = gercek
    # klavye: bilinmeyen adlı ama sınıfında keyboard geçen pencere
    open('/tmp/k.py', 'w').write("import sys\nfrom PyQt5.QtWidgets import QApplication, QLabel\napp = QApplication(['yeni-keyboard-x']); w = QLabel('K'); w.setWindowTitle('Baska'); w.setGeometry(400,600,900,300); w.show(); app.exec_()\n")
    p = subprocess.Popen(['python3', '/tmp/k.py']); time.sleep(3)
    gor = lambda: subprocess.run(['xdotool', 'search', '--onlyvisible', '--pid', str(p.pid)], capture_output=True, text=True).stdout.split()
    a = gor(); tk.sistem_klavyesini_gizle(); time.sleep(2.5); b = gor(); print('klavye önce', a, 'sonra', b, 'GIZLENDI' if a and not b else 'SORUN'); p.kill(); app.quit()
QTimer.singleShot(300, ac); QTimer.singleShot(5000, son); app.exec_()
