import sys, datetime, subprocess
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer
app = QApplication(sys.argv)
salon = [dict(sira=i, ad='ÖĞRENCİ %d' % i, no=str(5000 + i), sinif='11-I', ders='DİN KÜLTÜRÜ VE AHLAK BİLGİSİ') for i in range(1, 39)]
m = QWidget(); m.setGeometry(0, 60, 1920, 1000); m.show()   # tahta tam ekranda değil (üstte çubuk)
d = tk.YerimDialog(m, dict(tur='salon', sinif='11-I', liste=salon), '7. Ders', datetime.date(2026, 11, 11), 13); d.show()
def bitir():
    g = d.frameGeometry(); print('YERIM pencere', g.x(), g.y(), g.width(), g.height(), 'ekran', app.primaryScreen().geometry().getRect(), 'TAM' if (g.y() <= 0 and g.height() >= 1080) else 'KAYIK')
    subprocess.run(['import', '-window', 'root', '/tmp/onizleme/yerim-konum.png']); app.quit()
QTimer.singleShot(1500, bitir); app.exec_()
