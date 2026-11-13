import sys, subprocess, time
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
tk.KELEBEK_URLS = (); tk.KELEBEK_FOTO_URLS = ()
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QPainter, QColor
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
w = tk.Window(); w.showFullScreen(); app.processEvents()
A = ['Deniz Yıldız','Ece Kara','Mert Aksoy','Zeynep Demir','Ali Çınar','Elif Su Aydın','Kerem Polat','Nil Öztürk','Can Arslan','Defne Koç','Emir Şahin','Ada Güneş','Bora Kılıç','İpek Yavuz','Onur Tekin','Selin Acar','Kaan Erdem','Duru Bulut','Arda Özkan','Mina Çelik','Efe Doğan','Lara Kurt','Tuna Aslan','Azra Nur Tunç','Yiğit Sarı','Asya Bozkurt','Umut Keskin','Naz Uçar']
w.proje_roster = lambda: [(str(300 + i*17), a) for i, a in enumerate(A)]
def foto(no):
    pm = QPixmap(154, 200); pm.fill(QColor('#3a4f6e')); q = QPainter(pm); q.setRenderHint(QPainter.Antialiasing); q.setPen(tk.Qt.NoPen); q.setBrush(QColor('#9fb3cc')); q.drawEllipse(47, 40, 60, 60); q.drawEllipse(17, 120, 120, 140); q.end(); return pm
tk.student_photo = foto
d = [None]
def cek(ad): app.processEvents(); subprocess.run(['import', '-window', 'root', '/tmp/onizleme/u-%s.png' % ad])
def a1():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    d[0] = tk.DbsEkran(w); d[0].show(); app.processEvents()
    print('sürüm adı:', tk.version_label('4-ultra1'), tk.version_label('3-pro100'))
    try:
        n = tk.docx_yedek_pdf('/tmp/ornek.docx', '/tmp/onizleme/ornek-docx.pdf'); print('docx sayfa', n)
    except Exception as e: print('docx HATA', e)
    try:
        pm = tk.formul_pixmap(r'\frac{1}{\log_x(ab)} = \log_x\left(ab\right)', 44); pm.save('/tmp/onizleme/u-formul.png'); print('formül', pm.width(), pm.height())
    except Exception as e: print('formül HATA', e)
def a2(): cek('1-kendiliginden'); d[0].sayac.secim = time.monotonic() + 30*60; d[0].sayac.update()
def a3(): cek('2-30dk'); d[0].sayac.secim = time.monotonic() + 4*60 + 10; d[0].sayac.update()
def a4(): cek('3-4dk'); d[0].sayac.secim = time.monotonic() - 1; d[0].sayac.update()
def a5(): cek('4-doldu'); d[0].accept(); app.processEvents(); app.quit()
for t, f in ((1500, a1), (3500, a2), (4500, a3), (5500, a4), (6500, a5)): QTimer.singleShot(t, f)
app.exec_()
