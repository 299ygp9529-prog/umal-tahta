import sys, subprocess, time, shutil, os
os.environ['UMAL_XDOTOOL_YOK'] = '1'
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)
w = tk.Window(); w.show(); app.processEvents()
kod = "import sys\nfrom PyQt5.QtWidgets import QApplication, QLabel\nfrom PyQt5.QtCore import Qt\napp = QApplication(['xyzpanel']); w = QLabel('KLAVYE'); w.setWindowTitle(sys.argv[1]); w.setWindowFlags(Qt.Window | (Qt.X11BypassWindowManagerHint if sys.argv[2] == '1' else Qt.Window)); w.setGeometry(40, 40, 300, 100); w.show(); app.exec_()\n"
open('/tmp/eta-keyboard', 'w').write(kod); open('/tmp/baska', 'w').write(kod)
ps = [subprocess.Popen(['python3', '/tmp/eta-keyboard', 'Bilinmeyen', '0']), subprocess.Popen(['python3', '/tmp/eta-keyboard', 'Bilinmeyen', '1']), subprocess.Popen(['python3', '/tmp/baska', 'Ekran Klavyesi', '1']), subprocess.Popen(['python3', '/tmp/baska', 'Hesap makinesi', '0'])]
time.sleep(3); app.processEvents()
gor = lambda p: bool(subprocess.run(['xdotool', 'search', '--onlyvisible', '--pid', str(p.pid)], capture_output=True, text=True).stdout.split())
adlar = ['süreç eta-keyboard (çerçeveli)', 'süreç eta-keyboard (çerçevesiz)', 'başlığı Ekran Klavyesi', 'ilgisiz pencere (kalmalı)']
print('önce görünür:', [gor(p) for p in ps])
t0 = time.perf_counter(); n = tk._x11_klavye_gizle([])
tk.sistem_klavyesini_gizle(); time.sleep(2); app.processEvents()
for ad, p in zip(adlar, ps): print('  %s → %s' % (ad, 'görünüyor' if gor(p) else 'GİZLENDİ'))
print('Atlas penceresi görünür:', w.isVisible() and bool(subprocess.run(['xdotool', 'search', '--onlyvisible', '--pid', str(os.getpid())], capture_output=True, text=True).stdout.split()))
t0 = time.perf_counter(); tk._x11_klavye_gizle([]); print('bir tarama %.1f ms' % ((time.perf_counter() - t0)*1000))
for p in ps: p.kill()
