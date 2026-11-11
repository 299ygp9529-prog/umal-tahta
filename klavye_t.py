import sys, os, datetime, subprocess
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer
app = QApplication(sys.argv)
etiket = sys.argv[1]
class M(QWidget):
    kelebek = {'planlar': [{'tarih': '2026-11-11', 'ders': '7. Ders', 'gozcu': {'12-A': 'FATMA BİÇER'}, 'sinav': 'din kültürü ve ahlak bilgisi', 'salonlar': {}}]}
    data_dir = '/tmp'
    board = type('B', (), {'finish': lambda s: None})()
    def ogrenci_ara(self, q):
        if not q.strip(): return []
        day = datetime.date(2026, 11, 11); r = {'ad': 'CEYDA TÜRKSEVEN', 'no': '4', 'sinif': '10-G'}
        ws = [((day, 0), '11 Kasım Çar', True, '7. Ders', '12-A', 6, 'Din Kültürü ve Ahlak Bilgisi'),
              ((day + datetime.timedelta(1), 0), '12 Kasım Per', False, '4. Ders', '11-B', 12, 'Matematik')]
        return [(r, ws)]
m = M(); m.showFullScreen()
d = tk.OgrenciAraDialog(m)
def bitir():
    scr = app.primaryScreen().availableGeometry(); g = d.frameGeometry(); kb = d._kb
    alt = kb.mapToGlobal(kb.rect().bottomLeft()).y()
    print(etiket, 'ekran', scr.width(), scr.height(), 'pencere', g.x(), g.y(), g.width(), g.height(), 'klavye_alt', alt, 'bilet_h', d.kart.height(), 'tus', getattr(kb, '_H', 56),
          'SIGIYOR' if alt <= scr.bottom() - 30 and g.y() >= scr.top() else 'TASIYOR')
    subprocess.run(['import', '-window', 'root', '/tmp/onizleme/klavye-%s.png' % etiket]); app.quit()
d.show(); QTimer.singleShot(1200, lambda: d.edit.setText('4')); QTimer.singleShot(3500, bitir)
app.exec_()
