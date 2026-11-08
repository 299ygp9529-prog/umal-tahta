# Sanal tahtada gerçek Qt ile Atlas önizlemeleri: panel, tam ekran, tahtaya yazılan el yazısı, grafik çizici etiketi.
import sys, os, importlib.util
sys.path.insert(0, '/usr/lib/umal-tahta/python')
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
spec = importlib.util.spec_from_file_location('tk', '/usr/share/tahta-kalem/tahta_kalem.py'); tk = importlib.util.module_from_spec(spec); spec.loader.exec_module(tk)
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QImage, QPainter, QColor, QPen, QPainterPath
from PyQt5.QtCore import Qt, QPointF
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
