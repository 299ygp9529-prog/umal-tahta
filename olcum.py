# Gerçek Qt ile ekran (ana iş parçacığı) bloklanma ölçümü: disk 2 sn gecikirken kalem / silgi / geri al / sayfa değiştirme.
# Kullanım: olcum.py <tahta_kalem.py yolu> <etiket> <senaryo> <N>
#   senaryo: kontrol | ilk | kalem | sayfa | hata | kapanis
import sys, os, time, json, threading, importlib.util, statistics, resource, tempfile, traceback
MOD, ETIKET, SENARYO, N = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
GEC = 2.0
sys.path.insert(0, '/usr/lib/umal-tahta/python')
spec = importlib.util.spec_from_file_location('tk', MOD); tk = importlib.util.module_from_spec(spec); spec.loader.exec_module(tk)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer, QPointF
QApplication.setAttribute(Qt.AA_CompressHighFrequencyEvents, False)
app = QApplication(sys.argv[:1]); app.setApplicationName(tk.PRODUCT)
ANA = threading.main_thread()
def cikti(**k): print('SONUC ' + json.dumps(dict(etiket=ETIKET, senaryo=SENARYO, **k), ensure_ascii=False), flush=True)
def ozet(L):
    if not L: return dict(n=0)
    s = sorted(L); p95 = s[min(len(s) - 1, int(round(0.95 * (len(s) - 1))))]
    return dict(n=len(L), ort=round(statistics.mean(L), 2), medyan=round(statistics.median(L), 2), p95=round(p95, 2), en_buyuk=round(max(L), 2))
def rss_mb():
    with open('/proc/self/statm') as f: return round(int(f.read().split()[1]) * os.sysconf('SC_PAGE_SIZE') / 1048576, 1)
def cpu_sn(): r = resource.getrusage(resource.RUSAGE_SELF); return r.ru_utime + r.ru_stime

# ---- nabız: ekran iş parçacığında 5 ms'de bir çalışan zamanlayıcı. İki atış arası (boşluk − 5 ms) = ekranın o anda hiçbir şey yapamadığı süre.
NABIZ = []   # (zaman, önceki atıştan bu yana geçen ms)
_son = [time.perf_counter()]
def _nabiz():
    t = time.perf_counter(); NABIZ.append((t, (t - _son[0]) * 1000)); _son[0] = t
nt = QTimer(); nt.setTimerType(Qt.PreciseTimer); nt.setInterval(5); nt.timeout.connect(_nabiz)
def blok(t0, t1):
    """[t0, t1] aralığında ekranın en uzun yanıtsız kaldığı süre (ms). Aralığa taşan atış da sayılır."""
    L = [g for t, g in NABIZ if t0 <= t <= t1 + 0.05]
    son = (time.perf_counter() - _son[0]) * 1000 if _son[0] < t1 else 0
    return max(0.0, max(L + [son]) - 5) if (L or son) else -1

# ---- yavaş disk: fsync (ve istenirse ilk okuma / yer değiştirme) gerçekten GEC saniye sürer; hangi iş parçacığında, ne zaman: kaydedilir
DISK = []   # dict(t0, t1, ana)
ANA_IZ = []   # ekran tarafındaki diske yazmaların çağrı zinciri
_fsync = os.fsync
def yavas_fsync(fd):
    k = dict(t0=time.perf_counter(), t1=None, ana=threading.current_thread() is ANA); DISK.append(k)
    if k['ana']:
        f = sys._getframe(1); st = []
        while f is not None:
            if 'tahta_kalem' in f.f_code.co_filename: st.append('%s:%d' % (f.f_code.co_name, f.f_lineno))
            f = f.f_back
        ANA_IZ.append(' < '.join(st[:8]))
    time.sleep(GEC); _fsync(fd); k['t1'] = time.perf_counter()
def bekle(kosul, sonra, zaman_asimi=20.0, adim=10):
    t0 = time.perf_counter()
    def bak():
        if kosul() or time.perf_counter() - t0 > zaman_asimi: sonra()
        else: QTimer.singleShot(adim, bak)
    QTimer.singleShot(adim, bak)

w = tk.Window(); w.resize(1920, 1080); w.show()
SURE = {}   # işlem → [ms]
def olc(ad, f, *a):
    t = time.perf_counter(); r = f(*a); SURE.setdefault(ad, []).append((time.perf_counter() - t) * 1000); return r
_cz = [0]
def cizgi(arac='pen', sonra=None):
    """Gerçek kalem yolu: Board.begin → move ×24 (8 ms arayla, olay döngüsü arada çalışır) → finish."""
    b = w.board; _cz[0] += 0 if arac == 'eraser' else 1; y = 200 + (_cz[0] % 12) * 45   # silgi bir önceki çizginin üstünden geçer
    if w.tool != arac: w.set_tool(arac)
    olc(arac + ' basış', b.begin, QPointF(400, y)); i = [0]
    def adim():
        i[0] += 1
        if i[0] <= 24: olc(arac + ' hareket', b.move, QPointF(400 + i[0] * 22, y + (i[0] % 2) * 10)); QTimer.singleShot(8, adim)
        else:
            olc(arac + ' bırakış', b.finish)
            if sonra: QTimer.singleShot(0, sonra)
    QTimer.singleShot(8, adim)
def durum_dosyasi(): return os.path.join(w.session_dir, 'durum.json')
def diskteki():
    with open(durum_dosyasi(), encoding='utf-8') as f: return json.load(f)
def bellekteki(): return json.loads(json.dumps({str(k): v for k, v in w.saved_marks().items()}, ensure_ascii=False))
def bitir(kod=0):
    nt.stop(); sys.stdout.flush(); os._exit(kod)

def s_dolu():
    """Dolu sayfa (500 çizgi × 100 nokta): kalem basışı, silgi hareketi, geri al süreleri ve ekran donması (disk normal)."""
    import random; random.seed(3)
    def cz(i):
        x0, y0 = 60 + (i % 20) * 45, 60 + (i // 20) * 38
        return dict(tool='pen', color='#1d3fa8', width=2.4, nib='round', points=[[x0 + k * 0.35, y0 + 8 * ((k % 10) / 10)] for k in range(100)])
    def a():
        w.checkpoint(); w.marks[w.page] = [cz(i) for i in range(500)]; w.changed(); w.board.update(); w.save_session(arka=False) if 'arka=True' in open(MOD, encoding='utf-8').read() else w.save_session()
        t0 = [time.perf_counter()]; n = [0]
        def tur():
            if n[0] >= N:
                cikti(islem_sureleri_ms={k: ozet(v) for k, v in SURE.items()}, ekran_blok_ms=round(blok(t0[0], time.perf_counter()), 1), rss_mb=rss_mb()); return bitir()
            n[0] += 1
            def geri(): olc('geri al', w.undo); QTimer.singleShot(400, tur)
            cizgi('pen', lambda: QTimer.singleShot(400, lambda: cizgi('eraser', lambda: QTimer.singleShot(400, lambda: cizgi('pen', geri)))))
        QTimer.singleShot(1500, tur)
    QTimer.singleShot(3000, a)

def s_kontrol():
    """Ölçümün kanıtı: ekran iş parçacığı bilerek 500 ms uyutulur → nabız ~500 ms boşluk görmeli; arka plan iş parçacığı 500 ms uyursa görmemeli."""
    def a():
        t0 = time.perf_counter(); time.sleep(0.5); t1 = time.perf_counter()
        def b():
            ana_blok = blok(t0, t1)
            t2 = time.perf_counter(); th = threading.Thread(target=lambda: time.sleep(0.5)); th.start()
            def c():
                cikti(ekran_bilerek_500ms_uyutuldu=round(ana_blok, 1), arka_plan_500ms_uyudu=round(blok(t2, time.perf_counter()), 1)); bitir()
            bekle(lambda: not th.is_alive(), c)
        QTimer.singleShot(50, b)
    QTimer.singleShot(300, a)

def s_ilk():
    """İlk dosya okuma / ilk dosya yazma; başka iş parçacığı yavaş diskteyken ekranın başka dosyayı okuması."""
    ad = tk.arka_dosya(); d = tempfile.mkdtemp(); asil_oku = ad._oku
    def yavas_oku(path, tur):
        time.sleep(GEC); return asil_oku(path, tur)
    R = {}
    hazir = os.path.join(d, 'hazir.json'); json.dump({'a': 1}, open(hazir, 'w')); ad.json(hazir)
    def a():   # 1) ekran iş parçacığında İLK okuma, disk 2 sn
        p = os.path.join(d, 'ilk.json'); json.dump({'x': 1}, open(p, 'w')); ad._oku = yavas_oku
        t0 = time.perf_counter(); v = ad.json(p); t1 = time.perf_counter(); ad._oku = asil_oku
        R['ilk_okuma_ekran_tarafinda'] = dict(cagri_ms=round((t1 - t0) * 1000, 1), dogru=v == {'x': 1}); QTimer.singleShot(60, lambda: b(t0, t1))
    def b(t0, t1):
        R['ilk_okuma_ekran_tarafinda']['ekran_blok_ms'] = round(blok(t0, t1), 1)
        # 2) başka iş parçacığı İLK okumada (disk 2 sn, kilit?) → ekran hazır dosyayı 5 ms'de bir okur
        p = os.path.join(d, 'baska.json'); json.dump({'y': 1}, open(p, 'w')); ad._oku = yavas_oku
        th = threading.Thread(target=lambda: ad.json(p)); t0 = time.perf_counter(); th.start(); okuma = []
        def oku():
            if th.is_alive():
                t = time.perf_counter(); ad.json(hazir); okuma.append((time.perf_counter() - t) * 1000); QTimer.singleShot(5, oku)
            else:
                ad._oku = asil_oku; t1 = time.perf_counter()
                R['baska_is_parcacigi_yavas_diskte'] = dict(disk_suresi_ms=round((t1 - t0) * 1000), ekran_blok_ms=round(blok(t0, t1), 1), ekranin_okuma_sayisi=len(okuma), okuma_en_uzun_ms=round(max(okuma or [0]), 3))
                QTimer.singleShot(60, c)
        QTimer.singleShot(20, oku)
    def c():   # 3) İLK yazma (yeni dosya), disk 2 sn
        p = os.path.join(d, 'yeni.json'); asil_rep = os.replace
        def yavas_rep(a_, b_):
            if threading.current_thread() is not ANA: time.sleep(GEC)
            return asil_rep(a_, b_)
        os.replace = yavas_rep; t0 = time.perf_counter(); ad.yaz_json(p, {'z': list(range(1000))}); tc = (time.perf_counter() - t0) * 1000
        def son():
            os.replace = asil_rep; t1 = time.perf_counter()
            R['ilk_yazma'] = dict(cagri_ms=round(tc, 3), disk_suresi_ms=round((t1 - t0) * 1000), ekran_blok_ms=round(blok(t0, t1), 1), diskte_dogru=json.load(open(p)) == {'z': list(range(1000))})
            cikti(**R); bitir()
        bekle(lambda: os.path.isfile(p), son)
    QTimer.singleShot(300, a)

def s_kalem(sayfa=False):
    """Disk 2 sn gecikirken: kalem + silgi + geri al (+ sayfa değiştirme). Her disk işlemi için ekranın en uzun yanıtsız kaldığı süre."""
    BLOK = []; durum = dict(i=0, rss0=None, cpu0=None, t0=None, ana_disk=0)
    if sayfa:
        try: w.open_pdf_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdf', os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdf'))[0]))
        except Exception: traceback.print_exc()
        DISK.clear()
    def tur():
        if durum['i'] >= N: return son()
        gorulen = len(DISK)
        def disk_basladi():
            if len(DISK) <= gorulen:   # 20 sn'de kayıt başlamadı
                durum['i'] += 1; BLOK.append(-1); return tur()
            k = DISK[-1]
            def islem_bitti():
                def disk_bitti():
                    t1 = k['t1'] or time.perf_counter(); BLOK.append(blok(k['t0'], t1)); durum['ana_disk'] += 1 if k['ana'] else 0; durum['i'] += 1
                    QTimer.singleShot(30, tur)
                bekle(lambda: k['t1'] is not None, disk_bitti, zaman_asimi=10)
            def geri():
                olc('geri al', w.undo)
                if sayfa: olc('sayfa ileri', w.goto, 1); olc('sayfa geri', w.goto, -1)
                QTimer.singleShot(0, islem_bitti)
            cizgi('pen', lambda: cizgi('eraser', lambda: cizgi('pen', geri)))   # disk işlemi sürerken: yaz, sil, yaz, geri al
        cizgi('pen', lambda: bekle(lambda: len(DISK) > gorulen, disk_basladi, zaman_asimi=20))
    def son():
        os.fsync = _fsync; gecen = time.perf_counter() - durum['t0']; iyi = [b for b in BLOK if b >= 0]
        cikti(disk_islemi=len(BLOK), disk_islemi_ekran_tarafinda=durum['ana_disk'], ekran_tarafi_zincir=ANA_IZ[:4], baslamayan=len(BLOK) - len(iyi), ekran_blok_ms=ozet(iyi),
              islem_sureleri_ms={k: ozet(v) for k, v in SURE.items()}, rss_mb_bas=durum['rss0'], rss_mb_son=rss_mb(),
              cpu_yuzde=round((cpu_sn() - durum['cpu0']) / gecen * 100, 1), sure_sn=round(gecen), cizgi_sayisi=sum(len(v) for v in w.marks.values()))
        bitir()
    def basla():
        w.save_session()   # sekmenin ilk kaydı her iki sürümde de doğrudan yapılır; ölçüme katılmaz (ayrıca raporlanır)
        os.fsync = yavas_fsync; DISK.clear(); durum.update(rss0=rss_mb(), cpu0=cpu_sn(), t0=time.perf_counter()); tur()
    QTimer.singleShot(3000, basla)

def s_hata():
    """Arka plan kaydı hata verirse: ekran çalışmaya devam eder mi, sonraki kayıt düzelir mi?"""
    asil_rep = os.replace; say = [0]
    def bozuk(a_, b_):
        if str(b_).endswith('durum.json') and threading.current_thread() is not ANA: say[0] += 1; raise OSError(28, 'deneme: diskte yer yok')
        return asil_rep(a_, b_)
    R = {}
    def a():
        w.save_session(arka=False) if 'arka=True' in open(MOD, encoding='utf-8').read() else w.save_session()   # ilk kayıt (belge diske) önce
        os.replace = bozuk; t0 = time.perf_counter()
        def b():
            def c():
                R.update(arka_plan_hata_sayisi=say[0], hata_sirasinda_ekran_blok_ms=round(blok(t0, time.perf_counter()), 1), hata_sirasinda_cizgi_sayisi=sum(len(v) for v in w.marks.values()))
                os.replace = asil_rep
                def d():
                    def e():
                        try: R['sonraki_kayit_diskte_dogru'] = diskteki()['marks'] == bellekteki()
                        except Exception as x: R['sonraki_kayit_diskte_dogru'] = 'okunamadı: %s' % x
                        cikti(**R); bitir()
                    QTimer.singleShot(4500, e)
                cizgi('pen', d)
            QTimer.singleShot(4500, c)   # otomatik kayıt bu arada denenir ve hata alır
        cizgi('pen', lambda: cizgi('pen', b))
    QTimer.singleShot(3000, a)

def s_kapanis():
    """Kapanış: arka planda kayıt sürerken (disk 2 sn) son çizgi atılır ve uygulama kapanış adımları çalışır → diskte son hâl olmalı."""
    R = {}
    def a():
        w.save_session(arka=False) if 'arka=True' in open(MOD, encoding='utf-8').read() else w.save_session(); os.fsync = yavas_fsync
        gorulen = len(DISK)
        def b():
            R['kapanista_arka_kayit_suruyordu'] = len(DISK) > gorulen and DISK[-1]['t1'] is None
            def c():
                t0 = time.perf_counter(); w.board.finish(); w.save_session(); tk.arka_dosya().bosalt(); R['kapanis_suresi_ms'] = round((time.perf_counter() - t0) * 1000)
                os.fsync = _fsync
                try: d = diskteki(); R['diskte_son_hal'] = d['marks'] == bellekteki(); R['diskteki_cizgi'] = sum(len(v) for v in d['marks'].values()); R['bellekteki_cizgi'] = sum(len(v) for v in w.marks.values())
                except Exception as x: R['diskte_son_hal'] = 'okunamadı: %s' % x
                R['yarim_dosya_kaldi'] = [f for f in os.listdir(w.session_dir) if f.endswith('.arka') or (f.endswith('.json') and f not in ('durum.json', 'yedek.json', 'soru-kaynagi.json'))]
                cikti(**R); bitir()
            cizgi('pen', c)   # kayıt sürerken son çizgi, hemen ardından kapanış
        cizgi('pen', lambda: bekle(lambda: len(DISK) > gorulen, b, zaman_asimi=20))
    QTimer.singleShot(3000, a)

nt.start()
QTimer.singleShot(0, dict(dolu=s_dolu, kontrol=s_kontrol, ilk=s_ilk, kalem=s_kalem, sayfa=lambda: s_kalem(True), hata=s_hata, kapanis=s_kapanis)[SENARYO])
QTimer.singleShot(int((60 + N * 12) * 1000), lambda: (cikti(zaman_asimi=True), bitir(2)))
app.exec_()
