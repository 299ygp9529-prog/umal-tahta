import sys, subprocess, time, shutil
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
app = QApplication(sys.argv)
open('/tmp/sahte.py', 'w').write("import sys\nfrom PyQt5.QtWidgets import QApplication, QLabel\napp = QApplication(['xyzpanel']); w = QLabel('KLAVYE'); w.setWindowTitle('Bilinmeyen'); w.setGeometry(400,600,900,300); w.show(); app.exec_()\n")
shutil.copy('/tmp/sahte.py', '/tmp/eta-keyboard')
p = subprocess.Popen(['python3', '/tmp/eta-keyboard']); time.sleep(3)
gor = lambda: subprocess.run(['xdotool', 'search', '--onlyvisible', '--pid', str(p.pid)], capture_output=True, text=True).stdout.split()
print('önce (adı bilinmeyen pencere, süreç eta-keyboard):', gor())
tk.sistem_klavyesini_gizle(); time.sleep(2)
v = gor(); print('sonra:', v, 'GIZLENDI' if not v else 'GORUNUYOR'); p.kill()
