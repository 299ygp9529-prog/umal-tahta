import sys, subprocess, time
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QPainter, QColor
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
w = tk.Window(); w.showFullScreen(); app.processEvents()
A = ['Deniz Yıldız','Ece Kara','Mert Aksoy','Zeynep Demir','Ali Çınar','Elif Su Aydın','Kerem Polat','Nil Öztürk','Can Arslan','Defne Koç','Emir Şahin','Ada Güneş','Bora Kılıç','İpek Yavuz','Onur Tekin','Selin Acar','Kaan Erdem','Duru Bulut','Arda Özkan','Mina Çelik','Efe Doğan','Lara Kurt','Tuna Aslan','Azra Nur Tunç','Yiğit Sarı','Asya Bozkurt','Umut Keskin','Naz Uçar','Baran Ateş','Ela Turan','Çınar Özer','Derin Şen','Alp Korkmaz','Muhammed Ali Yalçınkaya']
w.proje_roster = lambda: [(str(300 + i*17), a) for i, a in enumerate(A)]
def foto(no):
    pm = QPixmap(154, 200); pm.fill(QColor('#3a4f6e')); q = QPainter(pm); q.setRenderHint(QPainter.Antialiasing); q.setPen(tk.Qt.NoPen); q.setBrush(QColor('#9fb3cc')); q.drawEllipse(47, 40, 60, 60); q.drawEllipse(17, 120, 120, 140); q.end(); return pm
tk.student_photo = foto
d = [None]
def cek(ad): app.processEvents(); subprocess.run(['import', '-window', 'root', '/tmp/onizleme/dbs-%s.png' % ad])
def a1():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    t0 = time.perf_counter(); d[0] = tk.DbsEkran(w); d[0].show(); app.processEvents(); print('açılış %.0f ms' % ((time.perf_counter() - t0)*1000))
def a2():
    cek('1-ilk'); y0 = dict(d[0].yer); t0 = time.perf_counter(); d[0].karistir(); app.processEvents(); print('yeniden karıştır %.0f ms; değişti: %s' % ((time.perf_counter() - t0)*1000, y0 != d[0].yer))
    d[0].b_kit.setChecked(True)
def a3():
    cek('2-kitapcik'); x = d[0]; x.isaret = {'300': {'tek', 'on'}, '317': {'arka'}, '334': {'tek'}, '351': {'on'}}; x.yok = {'368'}; x.karistir(); x.b_duz.setChecked(True)
def a4():
    cek('3-duzenle'); x = d[0]; x.b_duz.setChecked(False); app.processEvents(); print('durum:', x.durum_yazisi(), '| sorun', x.sorun)
    lay = x.duzen(); masa = {s: (i, dd[1]) for i, dd in enumerate(lay['desks']) for s in dd[3]}; ters = {}
    for n, s in x.yer.items(): ters.setdefault(masa[s][0], []).append(n)
    print('300 tek+ön:', len(ters[masa[x.yer['300']][0]]) == 1 and masa[x.yer['300']][1] == 0, '| 334 tek:', len(ters[masa[x.yer['334']][0]]) == 1, '| 351 önde:', masa[x.yer['351']][1] == 0, '| 368 yok:', '368' not in x.yer)
    x.onayla()
def a5():
    cek('4-onayli'); x = d[0]; y = dict(x.yer); x.accept(); app.processEvents()
    d[0] = tk.DbsEkran(w); d[0].show(); app.processEvents(); print('yeniden açınca aynı yerleşim:', d[0].yer == y, '| onaylı:', d[0].onayli)
def a6(): cek('5-yeniden'); d[0].accept(); app.processEvents(); app.quit()
for t, f in ((1500, a1), (3500, a2), (5000, a3), (6500, a4), (8000, a5), (9500, a6)): QTimer.singleShot(t, f)
app.exec_()
