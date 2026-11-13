import sys, subprocess, time, datetime
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
tk.KELEBEK_URLS = (); tk.KELEBEK_FOTO_URLS = ()
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QPainter, QColor
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
w = tk.Window(); w.showFullScreen(); app.processEvents()
A = ['Deniz Yıldız','Ece Kara','Mert Aksoy','Zeynep Demir','Ali Çınar','Elif Su Aydın','Kerem Polat','Nil Öztürk','Can Arslan','Defne Koç','Emir Şahin','Ada Güneş','Bora Kılıç','İpek Yavuz','Onur Tekin','Selin Acar','Kaan Erdem','Duru Bulut','Arda Özkan','Mina Çelik','Efe Doğan','Lara Kurt','Tuna Aslan','Azra Nur Tunç','Yiğit Sarı','Asya Bozkurt','Umut Keskin','Naz Uçar','Baran Ateş','Ela Turan','Çınar Özer','Derin Şen','Alp Korkmaz','Muhammed Ali Yalçınkaya','Ece Naz Er','Lina Su']
S = ['9-A','9-C','10-H','11-A','12-E','12-G','11-F','10-B']
def foto(no):
    pm = QPixmap(154, 200); pm.fill(QColor('#3a4f6e')); q = QPainter(pm); q.setRenderHint(QPainter.Antialiasing); q.setPen(tk.Qt.NoPen); q.setBrush(QColor('#9fb3cc')); q.drawEllipse(47, 40, 60, 60); q.drawEllipse(17, 120, 120, 140); q.end(); return pm
tk.student_photo = foto
liste = [dict(sira=i+1, no=str(500+i), ad=a.upper(), sinif=S[i % len(S)], ders='İNGİLİZCE') for i, a in enumerate(A)]
pl = dict(tarih='2026-11-13', ders='6. Ders', sinav='İNGİLİZCE', salonlar={s: liste for s in ['9-A','9-B','9-C','9-D','10-A','10-B','11-H','12-I']})
d = datetime.date(2026, 11, 13)
w.upcoming_plans = lambda *a, **k: [(pl, d, '6. Ders', 44400, 46800, 44400), (pl, d, '7. Ders', 47400, 49800, 47400), (pl, datetime.date(2026,11,14), '3. Ders', 36000, 38400, 36000)]
def cek(ad): app.processEvents(); subprocess.run(['import', '-window', 'root', '/tmp/onizleme/u-%s.png' % ad])
g = [None]
def a1():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    if not hasattr(w, 'exam_screen'): w.exam_screen = None
    try: w.open_salons(); app.processEvents()
    except Exception as e: print('salon HATA', e)
def a2():
    cek('salonlar'); w.close_salons(); app.processEvents()
    g[0] = tk.GraphDialog(w); g[0].show(); app.processEvents()
    t = g[0].fields[1]; t.clear(); g[0].target = t
    g[0].ekle('^(□)'); g[0].tus('3'); g[0].tus('▶'); g[0].tus('−'); g[0].tus('2'); g[0].tus('x')
    g[0].fields[2].clear(); g[0].target = g[0].fields[2]; g[0].ekle('e^(□)'); g[0].tus('x'); g[0].tus('−'); g[0].tus('1')
    print('alan 2:', g[0].fields[1].text(), '| derle:', tk.graph_compile(g[0].fields[1].text())[1], '| alan 3:', g[0].fields[2].text(), tk.graph_compile(g[0].fields[2].text())[1])
    print('latex:', tk.grafik_latex(g[0].fields[1].text()))
def a3():
    cek('grafik-dialog'); g[0].reject(); app.processEvents()
    w.atlas_sor_ac(); pn = w.atlas_panel; pn.grafik = ['x^2-4*x+3']; pn.cevap = 'Tepe noktası T(2, -1)'; pn.metin.setPlainText('1. Verilen fonksiyon $y = x^2 - 4x + 3$.', True); pn.tam_ekran(True); app.processEvents()
def a4(): cek('atlas-tam'); app.quit()
for t, f in ((1500, a1), (3500, a2), (5500, a3), (8000, a4)): QTimer.singleShot(t, f)
app.exec_()
