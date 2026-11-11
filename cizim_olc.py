import sys, time, math, random, types
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import QRectF
app = QApplication(sys.argv); random.seed(1)
def cizgi(nib, w=None):
    x, y = random.uniform(50, 900), random.uniform(50, 1200); pts = []
    for i in range(80): x += math.cos(i/6)*4; y += math.sin(i/9)*3; pts.append([x, y])
    s = dict(tool='pen', nib=nib, color='#1a1a1a', width=3, points=pts)
    if w: s['w'] = [1.0]*len(pts)
    return s
marks = [cizgi('fountain') for _ in range(300)] + [cizgi('round', w=True) for _ in range(300)] + [cizgi('round') for _ in range(300)]
b = types.SimpleNamespace(scale=1.0, devicePixelRatioF=lambda: 1.0)
pm = QPixmap(1000, 1400)
def tam():
    q = QPainter(pm); q.setRenderHint(QPainter.Antialiasing); t0 = time.perf_counter()
    for s in marks: tk.Board.draw_mark(b, q, s, QRectF(0, 0, 1000, 1400))
    q.end(); return (time.perf_counter() - t0)*1000
a = [tam() for _ in range(4)]
print('CIZIM %s: 900 çizgi (300 dolma kalem, 300 akıcı, 300 yuvarlak) tam sayfa: ilk %.0f ms, sonraki %.0f / %.0f / %.0f ms' % (sys.argv[1], *a))
