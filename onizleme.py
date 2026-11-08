# Sanal tahtada gerçek Qt ile Atlas önizlemeleri: panel, tam ekran, tahtaya yazılan el yazısı, grafik çizici etiketi.
import sys, os, importlib.util
sys.path.insert(0, '/usr/lib/umal-tahta/python')
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
spec = importlib.util.spec_from_file_location('tk', '/usr/share/tahta-kalem/tahta_kalem.py'); tk = importlib.util.module_from_spec(spec); spec.loader.exec_module(tk)
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QImage, QPainter, QColor, QPen, QPainterPath
from PyQt5.QtCore import Qt, QPointF
import traceback as _tb
sys.excepthook = lambda t, v, b: _tb.print_exception(t, v, b)   # uygulamadaki gibi: hata Qt'yi düşürmesin
app = QApplication(sys.argv); tk.ui_fonts()
CEVAP = r"""y = 2x doğrusunu inceleyelim:
• Bu doğru orijinden geçer ve eğimi $m = 2$'dir.
• $x = 0$ için $y = 0$; $x = 1$ için $y = 2$ olur.

1. Eğim:
• $m = \frac{\Delta y}{\Delta x} = \frac{2 - 0}{1 - 0} = 2$
• Eğim pozitif olduğu için doğru soldan sağa yükselir.

2. Parabolle karşılaştırma:
• $f(x) = x^{2} - 4x + 3$ için tepe noktası $r = -\frac{b}{2a} = 2$
• Kökler: $x_{1} = 1$, $x_{2} = 3$; $\sqrt{x^{2} + 9} = 5$

Cevap: $y = 2x$, orijinden geçen ve eğimi $2$ olan bir doğrudur."""
class Ana(QWidget):
    data_dir = '/tmp/atlas-onizleme'
    def board_info(self): return {'sinif': '9-A'}
    def exam_clock(self): return None
    def run_havuz(self, *a): pass
os.makedirs('/tmp/onizleme', exist_ok=True)
ana = Ana(); ana.resize(1920, 1080); ana.setAutoFillBackground(True); pal = ana.palette(); pal.setColor(ana.backgroundRole(), QColor('#0d1726')); ana.setPalette(pal)
pn = tk.AtlasPanel(ana); pn.ac(None)
pn.cevap = CEVAP; pn.metin.setPlainText(CEVAP, True); pn.yaz_b.setEnabled(True); pn.tekrar_b.setEnabled(True); pn.derin_b.setEnabled(True)
pn.grafik = ['2*x']; pn.grafik_b.show(); pn.maskot.ifade('konusma'); pn.durum.setText('Bugün 4 / 30')
pn.yerlestir(); ana.show(); app.processEvents(); app.processEvents()
ana.grab().save('/tmp/onizleme/panel.png')
gk = tk.GenisKlavye(ana); gk.ac(pn.giris); pn.giris.setText('x² − 4x + 3 = 0 kökleri'); gk.esitle(); app.processEvents(); app.processEvents(); ana.grab().save('/tmp/onizleme/panel-klavye.png'); gk.kb.matematik(True); app.processEvents(); app.processEvents(); ana.grab().save('/tmp/onizleme/panel-klavye-mat.png'); gk.kb.matematik(False); gk.hide(); pn.giris.clear(); app.processEvents()
pn.tam_ekran(True); app.processEvents(); app.processEvents(); pn.metin._ciz(); app.processEvents()
ana.grab().save('/tmp/onizleme/tam-ekran.png')
# Tahtaya yaz: gerçek kalem çizgileri
cz, h = tk.murekkep_cizgileri(CEVAP, 900, 30, '#1d3fa8', 2.4, os.path.join(tk.UI_FONT_DIR, 'ReliefSingleLineSVG-Regular.svg'), tk.atlas_guzel)
im = QImage(980, int(h) + 60, QImage.Format_RGB32); im.fill(QColor('#ffffff')); p = QPainter(im); p.setRenderHint(QPainter.Antialiasing)
for s in cz:
    p.setPen(QPen(QColor(s['color']), s['width'], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)); pts = s['points']
    path = QPainterPath(QPointF(pts[0][0] + 40, pts[0][1] + 30))
    for x, y in pts[1:]: path.lineTo(x + 40, y + 30)
    p.drawPath(path)
p.end(); im.save('/tmp/onizleme/tahtaya-yaz.png'); print('çizgi', len(cz))
# Grafik çizici
fs = []
for t, c in (('x^2 - 4*x + 3', '#2563eb'), ('1/(x-2)', '#e11d48')):
    fn, err = tk.graph_compile(t); fs.append((t, fn, c))
doc = tk.graph_build(fs, {'roots': True, 'extrema': True, 'cross': False, 'yx': False}); pix = doc[0].get_pixmap(matrix=tk.fitz.Matrix(2, 2), alpha=False); pix.save('/tmp/onizleme/grafik.png')
print('önizleme tamam')
# K-351: kara tahtalar (gerçek make_board + çerçeve parçaları + beyaz el yazısı)
from PyQt5.QtGui import QPixmap
yazi, hy = tk.murekkep_cizgileri(r"Fonksiyonlar" + "\n" + r"$f(x) = x^{2} - 4x + 3$" + "\n" + r"Kökler: $x_{1} = 1$, $x_{2} = 3$" + "\n" + r"Tepe noktası: $T(2, -1)$", 420, 26, '#ffffff', 2.0, os.path.join(tk.UI_FONT_DIR, 'ReliefSingleLineSVG-Regular.svg'), tk.atlas_guzel)
for bg in tk.KARA_TAHTALAR:
    doc = tk.make_board(bg, 960, 1080); px = doc[0].get_pixmap(matrix=tk.fitz.Matrix(2, 2), alpha=False, clip=tk.fitz.Rect(0, 0, 960, 540))
    im = QImage(px.samples, px.width, px.height, px.stride, QImage.Format_RGB888).copy()
    p = QPainter(im); p.setRenderHint(QPainter.Antialiasing)
    for s in yazi:
        p.setPen(QPen(QColor(s['color']), s['width']*2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)); pts = s['points']
        path = QPainterPath(QPointF(pts[0][0]*2 + 200, pts[0][1]*2 + 160))
        for x, y in pts[1:]: path.lineTo(x*2 + 200, y*2 + 160)
        p.drawPath(path)
    W, H = im.width(), im.height(); k, a = 7, 18
    for tur, g_ in (('ust', (0, 0, W, k)), ('sol', (0, 0, k, H)), ('sag', (W - k, 0, k, H)), ('alt', (0, H - a, W, a)), ('silgi', (W - 230, H - a - 30, 170, 40))):
        w_ = tk.KaraTahtaCerceve(None, tur); w_.resize(g_[2], g_[3]); pm = w_.grab(); p.drawPixmap(g_[0], g_[1], pm)
    p.end(); im.save('/tmp/onizleme/kara-%s.png' % bg)
print('kara tahtalar tamam')
# K-352: yeni Grafik çizici ve grafik sekmesi
try:
    class GA(QWidget):
        data_dir = '/tmp/atlas-onizleme'
        graph_cfg = {'f0': 'x² − 4x + 3', 'f1': 'log_2(x+1)', 'f2': '', 'isaret': 'tepe'}
        def board_info(self): return {'sinif': '9-A'}
        def exam_clock(self): return None
    ga = GA(); ga.resize(1920, 1080)
    dlg = tk.GraphDialog(ga); dlg.resize(1860, 1020); dlg.show()
    for _ in range(6): app.processEvents()
    dlg.redraw(); app.processEvents(); dlg.grab().save('/tmp/onizleme/grafik-cizici.png')
    dlg.fields[0].setText('a·x² + b·x + c'); dlg.fields[1].setText(''); app.processEvents(); dlg.redraw()
    sl = dlg.sliders.get('a')
    if sl: sl.setValue(-10)
    for _ in range(4): app.processEvents()
    dlg.redraw(); app.processEvents(); dlg.grab().save('/tmp/onizleme/grafik-kaydirici.png')
    dlg.fields[0].setText('kök(□,□)'); app.processEvents(); dlg.alan_degisti(); app.processEvents(); dlg.grab().save('/tmp/onizleme/grafik-kutu.png')
    dlg.close()
    # grafik sekmesi: kara tahta + çerçeve + İncele + Atlas
    durum = {'f': ['x² − 4x + 3', '', ''], 'param': {}, 'isaret': 'tepe'}
    bilgi = {}; doc = tk.grafik_belge(durum, bilgi)
    px = doc[0].get_pixmap(matrix=tk.fitz.Matrix(2, 2), alpha=False); im = QImage(px.samples, px.width, px.height, px.stride, QImage.Format_RGB888).copy()
    class FM: pass
    fm = FM(); fm.scroll = QWidget(); fm.scroll.resize(1920, 1080); fm.doc = doc; fm._sinav_su_an = False
    gi = tk.GrafikIncele(fm); gi.esitle(); gi.atlas.oner(durum, bilgi); gi.show(); gi.adjustSize(); gi.atlas.adjustSize(); app.processEvents()
    p = QPainter(im); W, H = im.width(), im.height()
    for tur, g_ in (('ust', (0, 0, W, 7)), ('sol', (0, 0, 7, H)), ('sag', (W - 7, 0, 7, H)), ('alt', (0, H - 18, W, 18)), ('silgi', (W - 230, H - 48, 170, 40))):
        w_ = tk.KaraTahtaCerceve(None, tur); w_.resize(g_[2], g_[3]); p.drawPixmap(g_[0], g_[1], w_.grab())
    gi.adjustSize(); gi.resize(gi.sizeHint()); g1 = gi.grab(); gy = tk.GRAFIK_H*2 + 16
    p.drawPixmap((W - g1.width())//2, gy, g1); at = gi.atlas.grab(); p.drawPixmap(W - at.width() - 24, gy - at.height() - 10, at)
    gi.dug['tablo'].setChecked(True); gi.dug['tepe'].setChecked(False)
    gi.tablo.setText('<table cellspacing="0"><tr><td style="padding:1px 10px;color:#7ff6ff"><b>x</b></td>' + ''.join('<td style="padding:1px 10px;border-left:1px solid #2a4468">%d</td>' % x for x in range(-2, 5)) + '</tr><tr><td style="padding:1px 10px;color:#7ff6ff"><b>y</b></td>' + ''.join('<td style="padding:1px 10px;border-left:1px solid #2a4468">%d</td>' % (x*x-4*x+3) for x in range(-2, 5)) + '</tr></table>')
    gi.r2.show(); app.processEvents(); gi.adjustSize(); gi.resize(gi.sizeHint()); g2 = gi.grab(); p.drawPixmap((W - g2.width())//2, gy + g1.height() + 30, g2); p.end()
    im.save('/tmp/onizleme/grafik-tahta.png')
    # grafik sekmesinin tamamı: üstte grafik, altta Atlas'ın el yazısı cevabı (üst üste binmez)
    px = doc[0].get_pixmap(matrix=tk.fitz.Matrix(1, 1), alpha=False); im2 = QImage(px.samples, px.width, px.height, px.stride, QImage.Format_RGB888).copy()
    cz2, _ = tk.murekkep_cizgileri(r"1. $y = x$ birim fonksiyondur." + "\n" + r"2. Orijinden geçer, eğimi $1$'dir." + "\n" + r"Cevap: $y = x$ birinci açıortay doğrusudur.", 820, 24, '#ffffff', 1.8, os.path.join(tk.UI_FONT_DIR, 'ReliefSingleLineSVG-Regular.svg'), tk.atlas_guzel)
    p = QPainter(im2); p.setRenderHint(QPainter.Antialiasing)
    for s_ in cz2:
        p.setPen(QPen(QColor(s_['color']), s_['width'], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)); pts = s_['points']
        path = QPainterPath(QPointF(pts[0][0] + 40, pts[0][1] + tk.GRAFIK_H + 16))
        for x, y in pts[1:]: path.lineTo(x + 40, y + tk.GRAFIK_H + 16)
        p.drawPath(path)
    p.end(); im2.save('/tmp/onizleme/grafik-sekme-tam.png')
    for k in ('kok', 'ykes', 'asimptot', 'alan', 'teget'):
        d2 = {'f': ['x² − 4x + 3' if k != 'asimptot' else '1/(x-2)', '', ''], 'isaret': k, 'ek': {}}
        dd = tk.grafik_belge(d2); px = dd[0].get_pixmap(matrix=tk.fitz.Matrix(1.2, 1.2), alpha=False); px.save('/tmp/onizleme/grafik-%s.png' % k)
    print('grafik tamam')
except Exception as e:
    import traceback; traceback.print_exc()
# K-355: uygulamanın öteki pencerelerindeki klavye (ör. öğrenci arama)
try:
    from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QLabel
    dl = QDialog(); dl.setStyleSheet('QDialog{background:#0f1c2e;} QLabel{color:white;font-size:24px;} QLineEdit{font-size:24px;padding:10px;background:#0a1628;color:white;border:2px solid #22e8ff;border-radius:12px;}')
    vv = QVBoxLayout(dl); vv.setContentsMargins(30, 24, 30, 24); vv.addWidget(QLabel('Nerede sınava gireceğim?')); ed = QLineEdit('Ayşe'); vv.addWidget(ed)
    kb = tk.attach_touch_keyboard(dl, ed, vv); kb.attach(ed); kb.show(); dl.resize(1100, 560); dl.show()
    for _ in range(4): app.processEvents()
    dl.grab().save('/tmp/onizleme/pencere-klavye.png')
except Exception:
    import traceback; traceback.print_exc()
