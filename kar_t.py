import sys, os, datetime, time, subprocess, tempfile
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtCore import QTimer, QPointF, QPoint, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import QEvent
app = QApplication(sys.argv)
day = datetime.date(2026, 11, 11)
salon = [dict(sira=i, ad='ÖĞRENCİ %d' % i, no=str(5000 + i), sinif='11-I', ders='TÜRK DİLİ VE EDEBİYATI') for i in range(1, 38)]
pl = dict(tarih='2026-11-11', ders='4. Ders', sinav='TDE', gozcu={'11-F': 'EMİNE GÜLEÇ'}, salonlar={'11-F': salon, '11-D': salon[:30]})
yazilan = []
class M(QWidget):
    data_dir = tempfile.mkdtemp()
    def exam_clock(self): return datetime.datetime(2026, 11, 11, 10, 50)
    def yok_dir(self): return self.data_dir
    def yok_all(self): return {}
    def elle_yoklama_yaz(self, v): yazilan.append(v)
    def show_toast(self, s): print('TOAST', s)
    def __getattr__(self, n): return lambda *a, **k: None
m = M(); m.setGeometry(0, 0, 1920, 1080); m.show()
QMessageBox.question = staticmethod(lambda *a, **k: QMessageBox.Yes)
kg = tk.KarargahScreen(m); kg.setGeometry(0, 0, 1920, 1080); kg.show()
kg.set_exam((pl, day, '4. Ders', 10*3600 + 30*60, 11*3600 + 10*60))
def tik(pt):
    for t in (QEvent.MouseButtonPress,): app.sendEvent(kg, QMouseEvent(t, QPointF(pt), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier))
def adim1():
    kg.detail = '11-F'; kg.relayout(); kg.repaint()
    print('Yoklama gir görünür:', kg.b_elle.isVisible(), repr(kg.b_elle.text()))
    kg.b_elle.click(); kg.repaint()
    for s_ in (11, 3):
        r = kg.seat_rects[s_]; tik(r.center().toPoint())
    kg.repaint(); print('işaretli:', sorted(kg.elle), '·', kg.b_elle_ok.text())
    subprocess.run(['import', '-window', 'root', '/tmp/onizleme/karargah-elle.png'])
    kg.b_elle_ok.click()
    print('yazılan:', [(v['salon'], [g['sira'] for g in v['gelmedi']], v['kaynak'], v['onay']) for v in yazilan]); app.quit()
QTimer.singleShot(1200, adim1); app.exec_()
