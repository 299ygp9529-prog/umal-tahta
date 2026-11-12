import sys, os, time, datetime, base64, io, random, json
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
tk.KELEBEK_URLS = []; tk.KELEBEK_FOTO_URLS = []
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QBuffer, QIODevice, QPoint
from PyQt5.QtGui import QImage, QPainter, QColor
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
w = tk.Window(); w.showFullScreen(); app.processEvents(); w.board_info = lambda: {'sinif': '9-A'}
rnd = random.Random(3)
def foto(i):
    im = QImage(120, 155, QImage.Format_RGB32); im.fill(QColor(200 + i % 40, 210, 225)); q = QPainter(im); q.setBrush(QColor(90 + i % 120, 70 + (i*7) % 100, 60)); q.drawEllipse(25, 20, 70, 85); q.setBrush(QColor(30, 40 + i % 90, 80)); q.drawRect(10, 115, 100, 40)
    for _ in range(60): q.setPen(QColor(rnd.randrange(255), rnd.randrange(255), rnd.randrange(255))); q.drawPoint(rnd.randrange(120), rnd.randrange(155))
    q.end(); b = QBuffer(); b.open(QIODevice.WriteOnly); im.save(b, 'JPG', 85); return base64.b64encode(bytes(b.data())).decode()
SAL = ['%d-%s' % (g, c) for g, cs in ((9, 'ABCD'), (10, 'ABCDEFGH'), (11, 'ABCDEFGHI'), (12, 'ABCDEFGHI')) for c in cs]
AD = ['Deniz Yıldız', 'Muhammed Ali Yalçınkaya', 'Ece Kara', 'Zeynep Ela Kürekçi', 'Furkan Mehmet Levendoğlu', 'Ali Çınar']
ogr = [dict(no=str(1000 + i), ad=AD[i % 6].upper() + ' %d' % i, sinif=SAL[i % 30]) for i in range(1100)]
rnd.shuffle(ogr); salonlar = {s: [] for s in SAL}; siniflar = {s: [] for s in SAL}
for i, o in enumerate(ogr):
    s = SAL[i % 30]; sira = len(salonlar[s]) + 1; r = dict(sira=sira, ad=o['ad'], sinif=o['sinif'], no=o['no'], ders='İNGİLİZCE'); salonlar[s].append(r); siniflar[o['sinif']].append(dict(ad=o['ad'], salon=s, sira=sira, no=o['no'], ders='İNGİLİZCE'))
yarin = datetime.date.today() + datetime.timedelta(days=1)
FD = {o['no']: foto(i) for i, o in enumerate(ogr)}
KB = dict(planlar=[dict(tarih=yarin.isoformat(), ders='7. Ders', sinav='İNGİLİZCE', gozcu={}, salonlar=salonlar, siniflar=siniflar)], ogrenciler=ogr)
olc = dict(es=[], yd=[]); 
def sar(cls, ad):
    eski = cls.paintEvent
    def pe(self, e, eski=eski): t0 = time.perf_counter(); eski(self, e); olc[ad].append((time.perf_counter(), (time.perf_counter() - t0)*1000))
    cls.paintEvent = pe
sar(tk.ExamScreen, 'es'); sar(tk.YerimDialog, 'yd')
def bekle(ms):
    t0 = time.perf_counter()
    while (time.perf_counter() - t0)*1000 < ms: app.processEvents(); time.sleep(.005)
def a1():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    w.start_messages(); app.processEvents(); sabit = datetime.datetime.combine(datetime.date.today(), datetime.time(10, 0, 5)); w.exam_clock = lambda: sabit; w.kelebek = KB; w.kelebek_new = None; tk._PHOTOS['data'] = FD; tk._PHOTOS['pix'].clear()
    t0 = time.perf_counter(); w.open_preview(); app.processEvents(); es = w.exam_screen
    print('sınav yerleri açılışı %.0f ms | görünür %s | koltuk %d' % ((time.perf_counter() - t0)*1000, es is not None and es.isVisible(), len(getattr(es, 'seat_rects', {}) or {})))
    import traceback, collections
    say = collections.Counter(); eu = tk.ExamScreen.update
    def upd(self, *a):
        st = traceback.extract_stack(limit=4); say[' < '.join('%s:%d' % (f.name, f.lineno) for f in st[:-1][-3:])] += 1; return eu(self, *a)
    tk.ExamScreen.update = upd
    ho = tk.HeartOverlay.setGeometry; say2 = collections.Counter()
    def sg(self, *a): say2['overlay setGeometry'] += 1; return ho(self, *a)
    tk.HeartOverlay.setGeometry = sg
    hs = tk.HeartOverlay.show
    def sh(self): say2['overlay show'] += 1; return hs(self)
    tk.HeartOverlay.show = sh
    say3 = collections.Counter()
    def sarU(cls, ad):
        u0 = cls.update
        def u1(self, *a):
            st = traceback.extract_stack(limit=5); say3[ad + ' ← ' + ' < '.join('%s:%d' % (f.name, f.lineno) for f in st[:-1][-3:])] += 1; return u0(self, *a)
        cls.update = u1
        r0 = cls.repaint
        def r1(self, *a): say3[ad + ' repaint'] += 1; return r0(self, *a)
        cls.repaint = r1
    for cls, ad in ((tk.Board, 'Board'), (type(w.scroll), 'Scroll'), (tk.Window, 'Window'), (tk.QPushButton, 'Düğme'), (tk.QLabel, 'Etiket'), (tk.QWidget, 'QWidget')): sarU(cls, ad)
    bp = tk.Board.paintEvent; bc = [0]
    def bp1(self, e): bc[0] += 1; return bp(self, e)
    tk.Board.paintEvent = bp1
    rc = collections.Counter(); pe0 = tk.ExamScreen.paintEvent
    def pe1(self, e): r = e.rect(); rc[(r.x(), r.y(), r.width(), r.height())] += 1; return pe0(self, e)
    tk.ExamScreen.paintEvent = pe1
    hp = tk.HeartOverlay.paintEvent; hc = [0]
    def hp1(self, e): hc[0] += 1; return hp(self, e)
    tk.HeartOverlay.paintEvent = hp1
    bekle(2500); n0 = len(olc['es']); bekle(3000); bos = olc['es'][n0:]
    print('boyama bölgeleri:', rc.most_common(5), '| kalp katmanı boyama', hc[0], '| ExamScreen geo', es.geometry().getRect(), 'opak', es.testAttribute(tk.Qt.WA_OpaquePaintEvent), 'ebeveyn', type(es.parent()).__name__, [(type(c).__name__, c.geometry().getRect(), c.isVisible()) for c in es.children() if isinstance(c, tk.QWidget) and c.isVisible()][:8])
    print('alttaki update:', say3.most_common(8), '| Board boyama', bc[0])
    print('update çağıranlar:', say.most_common(6)); print(say2, 'anim_timer', getattr(es, 'anim_timer', None) and (es.anim_timer.isActive(), es.anim_timer.interval()), 'faz', es.st.get('phase'))
    print('timers:', [(type(t.parent()).__name__, t.interval()) for t in w.findChildren(tk.QTimer) if t.isActive() and t.interval() < 200])
    print('boşta 3 sn: %d boyama, ort %.1f ms, en çok %.1f ms' % (len(bos), sum(d for _, d in bos)/max(1, len(bos)), max([d for _, d in bos] or [0])))
    for tur in range(0):
        sira = sorted(es.seat_rects)[3 + tur*7]; c = es.seat_rects[sira]; pos = QPoint(int(c.center().x()), int(c.center().y()))
        t0 = time.perf_counter(); es.yerim_sor(pos); t1 = time.perf_counter(); app.processEvents()
        if not getattr(es, 'yerim_bilgi', None): print('yerim_bilgi yok'); continue
        olc['yd'].clear(); kapat = [0]
        def kapa():
            d = QApplication.activeModalWidget(); kapat[0] = time.perf_counter()
            if d is not None: d.accept()
        QTimer.singleShot(2500, kapa); n1 = len(olc['es']); t2 = time.perf_counter(); es.yerim_ac(); t3 = time.perf_counter()
        ilk = olc['yd'][0] if olc['yd'] else (t2, -1); arada = olc['es'][n1:]; n2 = len(olc['es']); bekle(1500); son = olc['es'][n2:]
        print('%d) dokunuş (Yerimi bul çıkar) %.0f ms | salon açılışı: ilk çizime kadar %.0f ms (çizim %.0f ms) | pencere açıkken sınav ekranı %d kez boyandı (toplam %.0f ms) | kapanış %.0f ms | dönüşte 1,5 sn: %d boyama, en çok %.0f ms, toplam %.0f ms'
              % (tur + 1, (t1 - t0)*1000, (ilk[0] - t2)*1000, ilk[1], len(arada), sum(d for _, d in arada), (t3 - kapat[0])*1000, len(son), max([d for _, d in son] or [0]), sum(d for _, d in son)))
    print('açılmış fotoğraf', len(tk._PHOTOS['pix'])); app.quit()
QTimer.singleShot(2500, a1); app.exec_()
