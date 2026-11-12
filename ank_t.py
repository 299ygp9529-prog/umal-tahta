import sys, os

sys.path.insert(0,'/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QPainter, QColor, QFont, QPixmap
app=QApplication(sys.argv)
adlar=['Elif Özcan','Zeynep Ağaoğlu','Feyza Ecrin Alkan','Eymen Gökay Alemdaroğlu','Recep Metin Yıldırımoğlu','Muhammed Ali Sarıkaya','Mahriban Agajanova','Zeynep Ecrin Gürçay']*5
ros=[(str(100+i),a,i!=7) for i,a in enumerate(adlar[:38])]
tk.anket_roster=lambda a,s: ros
def foto(no):
    if no=='117': return None
    pm=QPixmap(300,400); pm.fill(QColor('#dfe6f2')); q=QPainter(pm); q.setBrush(QColor('#c98')); q.drawEllipse(70,40,160,220); q.setBrush(QColor('#345')); q.drawRect(40,280,220,120); q.setPen(QColor('red')); q.drawRect(2,2,295,395); q.end(); return pm
tk.student_photo=foto
W,H=1920,1080; im=QImage(W,H,QImage.Format_RGB32); im.fill(QColor('#0f1c2e')); p=QPainter(im); p.setRenderHint(QPainter.Antialiasing)
def font(s,b=False):
    f=QFont(); f.setPixelSize(int(s*1.0)); f.setBold(b); return f
tk.draw_anket_list(p,W,H,1.0,font,{'ad':'Deneme anketi','sorular':[1,2,3,4]},'11-E',{'cevaplar':{'101':1}},H)
p.end(); im.save('/tmp/onizleme/anket.png')
# K-482: yazarken maskot boyanmıyor mu; K-480: Akıllı araçlarda Atlas'a sor
import time
from PyQt5.QtCore import QTimer
w = tk.Window(); w.showFullScreen(); app.processEvents()
ms = w.atlas_yuzen.maskot; say = [0]; eski = ms.paintEvent
def pe(e): say[0] += 1; eski(e)
ms.paintEvent = pe
def b1():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    w.new_board()
def b2(): say[0] = 0
def b3(): print('MASKOT boştayken 1 sn: %d boyama' % say[0]); say[0] = 0; w.last_touch = time.time() + 1.0
def b4(): print('MASKOT yazarken 1 sn: %d boyama' % say[0]); pn = w.yan_panel if hasattr(w, 'yan_panel') else None; print('Akıllı araçlar düğmesi:', [x.i_atlas.text().strip() for x in w.findChildren(tk.QWidget) if hasattr(x, 'i_atlas')][:1])
def b5(): app.quit()
for t, f in ((1500, b1), (4000, b2), (5000, b3), (6000, b4), (6500, b5)): QTimer.singleShot(t, f)
app.exec_()
