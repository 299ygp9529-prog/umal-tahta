import sys, os, datetime, subprocess, types
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer, QPoint, QRectF
app = QApplication(sys.argv)
day = datetime.date(2026, 11, 11)
salon = [dict(sira=i, ad='ÖĞRENCİ %d' % i, no=str(5000 + i), sinif='11-I', ders='TÜRK DİLİ VE EDEBİYATI') for i in range(1, 39)]
salon[12] = dict(sira=13, ad='WARD JNAIDI', no='28', sinif='12-A', ders='TÜRK DİLİ VE EDEBİYATI')
class M(QWidget):
    kelebek = {'planlar': [{'tarih': '2026-11-11', 'ders': '4. Ders', 'salonlar': {'11-I': salon}}]}
    def ogrenci_ara(self, q):
        return [({'ad': 'WARD JNAIDI', 'no': '28', 'sinif': '12-A'}, [((day, 37800), 'Bugün', False, '4. Ders', '11-I', 13, 'Türk Dili ve Edebiyatı')])] if q == '28' else []
m = M(); m.resize(1920, 1080); m.show()
E = tk.ExamScreen
s = QWidget(m); s.setGeometry(0, 0, 1920, 1080); s.show(); s.main = m
for n in ('seat_at', 'yerim_sor', 'yerim_ac', 'start_fx'): setattr(s, n, types.MethodType(getattr(E, n), s))
s.update = lambda *a: None
s.seat_rects = {1: QRectF(100, 200, 300, 160)}; s.son_plan = {'liste': [dict(sira=1, ad='WARD JNAIDI', no='28', sinif='12-A', git='11-I · Sıra 13')]}
acilan = []
tk.YerimDialog.exec_ = lambda self_: (acilan.append(self_.sira), self_.show())
def adim1():
    s.yerim_sor(QPoint(200, 260)); b = s.yerim_btn
    print('dugme', b.isVisible(), repr(b.text()), b.geometry().getRect())
    subprocess.run(['import', '-window', 'root', '/tmp/onizleme/yerim-dugme.png'])
    b.click()
def adim2():
    print('YerimDialog açıldı, sıra', acilan)
    subprocess.run(['import', '-window', 'root', '/tmp/onizleme/yerim-salon.png']); app.quit()
QTimer.singleShot(800, adim1); QTimer.singleShot(2500, adim2); app.exec_()
