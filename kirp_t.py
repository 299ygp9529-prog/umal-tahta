import sys, time
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt, QRect
app = QApplication(sys.argv)
def ornek(zemin, cizgi, yazi, kart=True):
    pm = QPixmap(1150, 720); pm.fill(QColor(zemin)); p = QPainter(pm)
    p.setPen(QPen(QColor(cizgi), 2))
    for x in range(0, 1150, 42): p.drawLine(x, 0, x, 720)
    for y in range(0, 720, 42): p.drawLine(0, y, 1150, y)
    if kart: p.fillRect(QRect(250, 20, 430, 520), QColor('#ffffff'))
    p.setPen(QColor(yazi)); p.setFont(QFont('DejaVu Sans', 11)); p.drawText(310, 150, 'Dik üçgende verilenlere göre aşağıdaki'); p.drawText(310, 172, 'trigonometrik oranları bulunuz.')
    p.drawText(312, 205, 'a) sin B ='); p.drawText(450, 205, 'c) tan B ='); p.drawText(312, 300, 'b) cos C ='); p.drawText(450, 300, 'd) cot B =')
    p.setBrush(QColor('#f0f080')); p.setPen(QColor('#555555')); p.drawPolygon(*[tk.QPointF(*q) for q in ((380, 110), (410, 60), (520, 110))])
    p.drawRect(330, 440, 320, 60); p.end(); return pm
for ad, pm in (('kareli beyaz + kart', ornek('#ffffff', '#9fb0ff', '#111111')), ('düz beyaz', ornek('#ffffff', '#ffffff', '#111111', False)), ('kareli kara tahta', ornek('#1d262d', '#2b3a44', '#ffffff', False))):
    t0 = time.perf_counter(); k = tk.atlas_soru_kirp(pm); ms = (time.perf_counter() - t0)*1000
    print('%s: 1150x720 -> %dx%d (%.0f ms) beklenen yaklaşık 370x470' % (ad, k.width(), k.height(), ms)); k.save('/tmp/onizleme/kirp-%s.png' % ad.split()[0])
