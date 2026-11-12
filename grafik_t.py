import sys, time, subprocess
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
ad = sys.argv[1]
w = tk.Window(); w.resize(1920, 1080); w.show(); app.processEvents()
def say(pix):
    im = pix.toImage(); W, H = im.width(), im.height(); sol = sag = 0
    for y in range(0, H, 3):
        for x in range(0, W, 3):
            c = im.pixelColor(x, y)
            if c.red() < 90 and c.green() > 190 and c.blue() > 210:
                if x < W//2: sol += 1
                else: sag += 1
    return sol, sag
def basla():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    tk.grafik_tahtaya(w, dict(f=['x^2-4x+3', '', ''], param={}, isaret=None), canlandir=True)
def ortada():   # canlandırma sürerken hazır görüntü istenir (K-436 boşta hazırlama / kalem basışı gibi)
    try: w.board.ensure_base()
    except Exception as e: print('ensure', e)
    print(ad, 'canlandırma sırasında hazır görüntü alındı mı:', w.board.base is not None)
def son():
    w.board.repaint(); app.processEvents()
    r = w.board.visibleRegion().boundingRect(); pix = w.board.grab(r)
    sol, sag = say(pix); print(ad, 'eğri pikselleri sol=%d sag=%d' % (sol, sag), 'TAM' if sag > sol*0.5 else 'KESIK')
    b = w.board.base
    if b is not None: s2 = say(b); print(ad, 'hazır görüntüde sol=%d sag=%d' % s2, 'TAM' if s2[1] > s2[0]*0.5 else 'KESIK')
    subprocess.run(['import', '-window', 'root', '/tmp/onizleme/grafik-%s.png' % ad]); app.quit()
QTimer.singleShot(1500, basla); QTimer.singleShot(2100, ortada); QTimer.singleShot(5000, son)
app.exec_()
