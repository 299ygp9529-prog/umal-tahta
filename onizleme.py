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
ana = Ana(); ana.resize(1920, 1080); ana.setStyleSheet('background:#0d1726;')
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
