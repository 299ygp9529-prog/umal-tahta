import sys
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QEvent, QPointF, Qt, QSizeF
from PyQt5.QtGui import QTouchEvent, QTouchDevice
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
w = tk.Window(); w.showFullScreen(); app.processEvents()
dev = QTouchDevice(); dev.setType(QTouchDevice.TouchScreen); dev.setCapabilities(QTouchDevice.Position | QTouchDevice.Area)
durum = {}   # id → (x, y)
def olay(tur, degisen):
    b = w.board; tps = []; st = 0
    for i, (x, y) in list(durum.items()):
        tp = QTouchEvent.TouchPoint(i); tp.setPos(QPointF(x, y)); tp.setScreenPos(QPointF(b.mapToGlobal(QPointF(x, y).toPoint())))
        s_ = degisen.get(i, Qt.TouchPointStationary); tp.setState(s_); tp.setEllipseDiameters(QSizeF(8, 8)); tps.append(tp); st |= int(s_)
    e = QTouchEvent(tur, dev, Qt.NoModifier, Qt.TouchPointStates(st), tps); b.event(e)
    for i, s_ in degisen.items():
        if s_ == Qt.TouchPointReleased: durum.pop(i, None)
def kalem(i, x0, y0, n=12, dx=8):
    durum[i] = (x0, y0); return i
def senaryo():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    w.new_board(); app.processEvents(); w.set_tool('pen'); b = w.board; sayfa = lambda: len(w.marks.get(w.page, []))
    print('başta çizgi', sayfa())
    durum[1] = (200, 200); olay(QEvent.TouchBegin, {1: Qt.TouchPointPressed})
    for k in range(1, 8): durum[1] = (200 + k*10, 200 + k*3); olay(QEvent.TouchUpdate, {1: Qt.TouchPointMoved})
    durum[2] = (900, 600); durum[3] = (950, 620); durum[4] = (1000, 640)   # üç öğrenci dokunuyor
    olay(QEvent.TouchUpdate, {2: Qt.TouchPointPressed, 3: Qt.TouchPointPressed, 4: Qt.TouchPointPressed})
    for k in range(8, 20):
        durum[1] = (200 + k*10, 200 + k*3); durum[2] = (900 + k, 600 - k)
        olay(QEvent.TouchUpdate, {1: Qt.TouchPointMoved, 2: Qt.TouchPointMoved})
    print('öğrenciler dokunurken çizgi sürüyor:', b.active is not None, '| nokta', len((b.active or {}).get('points', [])))
    olay(QEvent.TouchUpdate, {1: Qt.TouchPointReleased})   # öğretmen kalemi kaldırdı, öğrenciler hâlâ dokunuyor
    print('kalem kalkınca çizgi bitti:', b.active is None, '| sayfadaki çizgi', sayfa())
    durum[5] = (300, 400); olay(QEvent.TouchUpdate, {5: Qt.TouchPointPressed})   # öğretmen yeniden yazıyor
    for k in range(1, 12): durum[5] = (300 + k*9, 400); olay(QEvent.TouchUpdate, {5: Qt.TouchPointMoved})
    print('öğrenciler dokunurken yeni çizgi başladı:', b.active is not None)
    olay(QEvent.TouchUpdate, {5: Qt.TouchPointReleased})
    olay(QEvent.TouchEnd, {2: Qt.TouchPointReleased, 3: Qt.TouchPointReleased, 4: Qt.TouchPointReleased})
    ms = w.marks.get(w.page, [])
    print('SONUÇ: çizgi sayısı', len(ms), '(beklenen 2) | öğrenci bölgesinde çizgi:', any(any(x > 800 for x, y in s_.get('points', [])) for s_ in ms))
    # yumruk: aynı anda 3 temas → hiç çizgi yok
    durum.update({7: (500, 500), 8: (520, 505), 9: (540, 510)}); olay(QEvent.TouchBegin, {7: Qt.TouchPointPressed, 8: Qt.TouchPointPressed, 9: Qt.TouchPointPressed})
    for k in range(5): durum[7] = (500 + k*10, 500); olay(QEvent.TouchUpdate, {7: Qt.TouchPointMoved})
    olay(QEvent.TouchEnd, {7: Qt.TouchPointReleased, 8: Qt.TouchPointReleased, 9: Qt.TouchPointReleased})
    print('yumruk (aynı anda 3 temas) yok sayıldı:', len(w.marks.get(w.page, [])) == 2)
    app.quit()
QTimer.singleShot(2500, senaryo)
app.exec_()
