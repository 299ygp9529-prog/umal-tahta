import sys, os, datetime, time
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QColor
app = QApplication(sys.argv); et = sys.argv[1]
day = datetime.date(2026, 11, 11)
salon = [dict(sira=i, ad='ÖĞRENCİ ADI SOYADI %d' % i, no=str(5000 + i), sinif='11-I', ders='TÜRK DİLİ VE EDEBİYATI') for i in range(1, 39)]
# gerçek tahtadaki gibi fotoğraflı: 120x155 örnek fotoğraflar
tk._PHOTOS['data'] = {r['no']: '' for r in salon}
for i, r in enumerate(salon):
    pm = QPixmap(120, 155); pm.fill(QColor(60 + i*4, 90, 140)); tk._PHOTOS['pix'][r['no']] = pm
m = QWidget(); m.setGeometry(0, 0, 1920, 1080); m.show()
d = tk.YerimDialog(m, dict(tur='salon', sinif='11-I', liste=salon), '4. Ders', day, 13)
sure = []; orj = d.paintEvent
def pe(e):
    t = time.perf_counter(); orj(e); sure.append((time.perf_counter() - t)*1000)
d.paintEvent = pe
blok = []; son = [time.perf_counter()]
def nabiz():
    n = time.perf_counter(); blok.append((n - son[0])*1000 - 5); son[0] = n
nt = QTimer(); nt.setInterval(5); nt.timeout.connect(nabiz); nt.start()
d.show()
def bitir():
    s = sorted(sure[1:]) or [0]; b = sorted(blok)
    print('YERIM %s: çizim sayısı %d (5 sn) · ilk çizim %.1f ms · sonraki ortanca %.2f ms · en uzun %.1f ms · saniyede çizime giden %.0f ms · ekran takılması ortanca %.1f ms, en uzun %.1f ms'
          % (et, len(sure), sure[0], s[len(s)//2], s[-1], sum(sure[1:])/5.0, b[len(b)//2], b[-1]))
    app.quit()
QTimer.singleShot(5000, bitir); app.exec_()
