import sys, os, time, datetime, json, hashlib, hmac, random, base64
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer, QEvent, QObject, QPoint, QBuffer, QIODevice
from PyQt5.QtGui import QImage, QPainter, QColor
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
# --- sahte kelebek planı (gerçek okul verisi yok): 1100 öğrenci, 8 sınav günü, ~1,7 MB
rnd = random.Random(5)
SAL = ['%d-%s' % (g, c) for g, cs in ((9, 'ABCD'), (10, 'ABCDEFGH'), (11, 'ABCDEFGHI'), (12, 'ABCDEFGHI')) for c in cs]
ogr = [dict(no=str(1000 + i), ad='ÖĞRENCİ ADI SOYADI %d' % i, sinif=SAL[i % 30]) for i in range(1100)]
bugun = datetime.date.today(); planlar = []
for gun in range(-6, 2):
    d = bugun + datetime.timedelta(days=gun); sal = {s: [] for s in SAL}; sn = {s: [] for s in SAL}; rnd.shuffle(ogr)
    for i, o in enumerate(ogr):
        s = SAL[i % 30]; r = dict(sira=len(sal[s]) + 1, ad=o['ad'], sinif=o['sinif'], no=o['no'], ders='İNGİLİZCE'); sal[s].append(r); sn[o['sinif']].append(dict(ad=o['ad'], salon=s, sira=r['sira'], no=o['no'], ders='İNGİLİZCE'))
    planlar.append(dict(tarih=d.isoformat(), ders='7. Ders', sinav='DENEME SINAVI', gozcu={s: 'Öğretmen Adı' for s in SAL}, salonlar=sal, siniflar=sn))
veri = json.dumps(dict(planlar=planlar, ogrenciler=ogr, anketler=[]), ensure_ascii=False).encode()
K = tk.KELEBEK_KEY; nonce = os.urandom(16); n = len(veri); h0 = hashlib.sha256(K + nonce); ks = bytearray()
for i in range((n + 31)//32): h = h0.copy(); h.update(i.to_bytes(8, 'big')); ks += h.digest()
ct = (int.from_bytes(veri, 'big') ^ int.from_bytes(bytes(ks[:n]), 'big')).to_bytes(n, 'big')
blob = b'UK1' + nonce + hmac.new(K, nonce + ct, hashlib.sha256).digest() + ct
open('/tmp/plan-sahte.bin', 'wb').write(blob); print('sahte plan %.1f MB' % (len(blob)/1e6))
tk.KELEBEK_URLS = ('file:///tmp/plan-sahte.bin',); tk.KELEBEK_FOTO_URLS = ('file:///tmp/yok.bin',)
w = tk.Window(); w.showFullScreen(); app.processEvents(); w.board_info = lambda: {'sinif': '9-A'}
sabit = datetime.datetime.combine(datetime.date.today(), datetime.time(10, 0, 5)); w.exam_clock = lambda: sabit
w.start_messages(); w.start_state_reports() if hasattr(w, 'start_state_reports') else None
# --- ölçüm araçları: boyama sayısı (bütün pencereler), CPU, ekran iş parçacığının en uzun takılması
class Say(QObject):
    def __init__(s): super().__init__(); s.n = 0; s.alan = 0
    def eventFilter(s, o, e):
        if e.type() == QEvent.Paint and isinstance(o, QWidget): s.n += 1; r = e.rect(); s.alan += r.width()*r.height()
        return False
say = Say(); app.installEventFilter(say)
nab = dict(son=time.perf_counter(), en=0.0, n50=0)
def tik():
    t = time.perf_counter(); g = (t - nab['son'])*1000; nab['son'] = t
    if g > nab['en']: nab['en'] = g
    if g > 60: nab['n50'] += 1
nt = QTimer(); nt.timeout.connect(tik); nt.start(10)
def bekle(ms):
    t0 = time.perf_counter()
    while (time.perf_counter() - t0)*1000 < ms: app.processEvents(); time.sleep(.003)
def olc(ad, ms, once=None):
    if once: once()
    say.n = 0; say.alan = 0; nab['en'] = 0; nab['n50'] = 0; nab['son'] = time.perf_counter(); c0 = time.process_time(); t0 = time.perf_counter()
    bekle(ms)
    dt = time.perf_counter() - t0; cpu = (time.process_time() - c0)/dt*100
    print('%-34s | boyama %5.0f/sn | boyanan alan %6.1f ekran/sn | CPU %%%5.1f | en uzun takılma %4.0f ms | >60 ms takılma %d' % (ad, say.n/dt, say.alan/(1920*1080)/dt, cpu, nab['en'], nab['n50']))
def senaryo():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    w.new_board(); bekle(1500)
    # kelebek: ilk indirme (çözülür) ve sonraki iki indirme (plan aynı)
    w.kelebek = None; w.kelebek_new = None; w.kelebek_busy = False; w.kelebek_tick(); bekle(4000); w.take_kelebek()
    print('plan yüklendi:', len((w.kelebek or {}).get('planlar', [])), 'sınav')
    w.exam_tick(); bekle(500)
    olc('1) boş tahta, sınav haftası', 10000)
    def indir(): w.kelebek_busy = False; w.kelebek_tick()
    olc('2) 2 dk\'lık kelebek indirmesi', 4000, indir)
    olc('3) indirme tekrar (plan aynı)', 4000, indir)
    w.open_preview(); bekle(800); es = w.exam_screen
    if es is None: print('sınav yerleri açılmadı'); app.quit(); return
    olc('4) sınav yerleri ekranı açık', 8000)
    def yer():
        sira = sorted(es.seat_rects)[5]; c = es.seat_rects[sira]; es.yerim_sor(QPoint(int(c.center().x()), int(c.center().y()))); app.processEvents()
        if not getattr(es, 'yerim_bilgi', None): return
        if hasattr(tk, 'YerimEkran'):
            es.yerim_ac(); bekle(2000)
            for x in w.findChildren(tk.YerimEkran): x.kapat()
        else:
            def kapa():
                d = QApplication.activeModalWidget()
                if d is not None: d.accept()
            QTimer.singleShot(2000, kapa); es.yerim_ac()
    olc('5) Yerimi bul aç-kapa + 4 sn', 6000, yer)
    w.hide_exam() if hasattr(w, 'hide_exam') else None; bekle(500)
    app.quit()
QTimer.singleShot(2500, senaryo); app.exec_()
