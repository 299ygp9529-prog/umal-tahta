import sys
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QPainter, QColor
app = QApplication(sys.argv)
m = "1. ln(x+1) = 2 ⇒ x+1 = e^{2}\n2. x değerini yalnız bırakalım: x = e^2 - 1\nSonuç: (x+1)^2 = 9 ve \\frac{7}{2}\nCevap: D) e^{2} - 1"
pm = tk.atlas_cevap_resmi(m, 900, 34, '#eef6ff', True, dict(cevap='#3ef08a', baslik='#7ff6ff'))
im = QPixmap(pm.width() + 40, pm.height() + 40); im.fill(QColor('#0a1628')); q = QPainter(im); q.drawImage(20, 20, pm); q.end(); im.save('/tmp/onizleme/ustel.png'); print('resim', pm.width(), pm.height())
