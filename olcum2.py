# Pro 73 doğrulaması (gerçek Qt): bölge onarımı piksel karşılaştırması, büyük PDF açma, sayfa önbelleği, hızlı yakınlaştırma.
# Kullanım: olcum2.py <tahta_kalem.py yolu> <etiket> <senaryo>     senaryo: onar | pdf | zoom | kitap-uret
import sys, os, time, json, math, random, statistics, filecmp, importlib.util, traceback
MOD, ETIKET, SENARYO = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, '/usr/lib/umal-tahta/python')
spec = importlib.util.spec_from_file_location('tk', MOD); tk = importlib.util.module_from_spec(spec); spec.loader.exec_module(tk)
KITAP, NOTLU = '/tmp/kitap.pdf', '/tmp/notlu.pdf'
def cikti(**k): print('SONUC ' + json.dumps(dict(etiket=ETIKET, senaryo=SENARYO, **k), ensure_ascii=False), flush=True)
def ozet(L):
    if not L: return dict(n=0)
    s = sorted(L); return dict(n=len(L), ort=round(statistics.mean(L), 2), medyan=round(statistics.median(L), 2), en_buyuk=round(max(L), 2))
if SENARYO == 'kitap-uret':
    def uret(path, n, notlu):
        d = tk.fitz.open()
        for i in range(n):
            pg = d.new_page(width=595, height=842); pg.insert_text((50, 60), 'Sayfa %d' % (i + 1), fontsize=20)
            sh = pg.new_shape()
            for k in range(900): sh.draw_line((40 + (k*7 + i*3) % 500, 100 + (k*13) % 700), (60 + (k*11) % 500, 120 + (k*17 + i) % 700))
            sh.finish(width=0.4, color=(.2, .3, .5)); sh.commit()
            if notlu and i in (3, 120, n - 1):
                s = dict(tool='pen', color='#1d3fa8', width=2.4, points=[[100 + j*3, 300 + (j % 5)*4] for j in range(40)])
                a = pg.add_ink_annot([[tuple(q) for q in s['points']]]); a.set_info(title=tk.TAG, content=json.dumps(s)); a.update()
        d.save(path); d.close()
    uret(KITAP, 400, False); uret(NOTLU, 400, True); print('kitaplar', os.path.getsize(KITAP)//1024, 'KB'); sys.exit(0)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QImage
QApplication.setAttribute(Qt.AA_CompressHighFrequencyEvents, False)
app = QApplication(sys.argv[:1]); app.setApplicationName(tk.PRODUCT)
w = tk.Window(); w.resize(1920, 1080); w.show()
SURE = {}
def olc(ad, f, *a):
    t = time.perf_counter(); r = f(*a); SURE.setdefault(ad, []).append((time.perf_counter() - t)*1000); return r
def don(ms):
    t = time.perf_counter()
    while (time.perf_counter() - t)*1000 < ms: app.processEvents(); time.sleep(0.005)
def bosalt():
    try: tk.arka_dosya().bosalt()
    except Exception: pass
def taze(pg=None):
    """Şu anki sayfa ve ölçek için sıfırdan çizilmiş görüntü (önbellek kullanılmadan)."""
    page = w.doc[w.page]; clip = tk.fitz.Rect(0, 0, page.rect.width, min(page.rect.height, 800)) if w.board.pattern else page.rect
    scale = min(w.zoom, math.sqrt(14000000/(clip.width*clip.height)))
    pix = page.get_pixmap(matrix=tk.fitz.Matrix(scale, scale), clip=clip, colorspace=tk.fitz.csRGB, alpha=False)
    return QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888).copy()
def yazilar(): return {str(p): len(v) for p, v in sorted(w.marks.items()) if v}

def s_onar():
    """Silgi ve Geri al sonrası onarılmış hazır görüntü, sıfırdan çizilmiş görüntüyle piksel piksel aynı mı?"""
    random.seed(11); b = w.board; R = dict(silgi=0, silgi_onarildi=0, silgi_farkli=0, geri=0, geri_onarildi=0, geri_farkli=0, ileri=0, ileri_onarildi=0, ileri_farkli=0, farkli_ornek=[])
    stiller = ['normal'] + [k for k in tk.STYLE_SPAN if k != 'laser']
    for i in range(140):   # gerçek kalem yolundan: her üslup, uç, kalınlık, renk; birbirinin üstünden geçen çizgiler
        arac = random.choice(['pen']*6 + ['highlight', 'dash'] + (['arrow'] if i % 35 == 34 else []))
        w.set_tool(arac); w.pen_style = random.choice(stiller)
        try: w.nib.setCurrentIndex(random.randrange(w.nib.count()))
        except Exception: pass
        w.color = random.choice(['#1d3fa8', '#d32f2f', '#111111', '#00a86b', '#ff9a3a']); w.width.setValue(random.choice([1, 2, 3, 5, 9]))
        x0, y0 = random.uniform(120, 1300), random.uniform(120, 760); n = random.choice([3, 20, 45]); dx = random.uniform(2, 9)
        b.begin(QPointF(x0, y0))
        for k in range(1, n): b.move(QPointF(x0 + k*dx, y0 + 40*math.sin(k/5.0 + i) + random.uniform(-3, 3)))
        b.finish(); app.processEvents()
    app.processEvents(); R['cizgi'] = len(w.marks.get(w.page, [])); R['turler'] = sorted({(s.get('tool'), s.get('style'), s.get('nib')) for s in w.marks[w.page]}, key=str)[:40]
    def dur():
        t_ = getattr(b, '_hz_t', None)
        if t_ is not None: t_.stop()   # boşta hazırlama araya girmesin: yalnız onarımın sonucu ölçülsün
    def karsilastir(ad):
        dur(); onarildi = getattr(b, 'base', None) is not None and b.onar_hazir()
        a = b.base.toImage() if onarildi else None
        b.base = None; t = time.perf_counter(); b.ensure_base(); SURE.setdefault('bütün sayfayı baştan çizme', []).append((time.perf_counter() - t)*1000)
        ref = b.base.toImage(); R[ad] += 1
        if onarildi:
            R[ad + '_onarildi'] += 1
            if a != ref:
                R[ad + '_farkli'] += 1
                fark = sum(1 for y in range(0, a.height(), 3) for x in range(0, a.width(), 3) if a.pixel(x, y) != ref.pixel(x, y))
                if len(R['farkli_ornek']) < 6: R['farkli_ornek'].append(dict(islem=ad, farkli_nokta_ornek=fark))
    w.set_tool('eraser'); b.ensure_base()
    for i in range(45):
        ms = [s for s in w.marks.get(w.page, []) if s.get('points')]
        if not ms: break
        s = random.choice(ms); pt = s['points'][len(s['points'])//2]
        dur(); w.checkpoint(); olc('silgi (onarım dahil)', b.erase, pt); karsilastir('silgi')
    for i in range(25): dur(); olc('geri al (onarım dahil)', w.undo); dur(); karsilastir('geri')
    for i in range(12): dur(); olc('ileri al (onarım dahil)', w.redo); dur(); karsilastir('ileri')
    cikti(islem_sureleri_ms={k: ozet(v) for k, v in SURE.items()}, **R)

def s_pdf():
    R = {}; yeni = hasattr(w, 'sayfa_gorseli')
    olc('kitap açma (400 sayfa)', w.open_pdf_path, KITAP); app.processEvents(); bosalt(); don(300)
    pdf = os.path.join(w.session_dir, w.session_pdf_name or ''); R['oturum_pdf_var'] = os.path.isfile(pdf)
    R['oturum_pdf_kaynakla_ayni_dosya'] = os.path.isfile(pdf) and filecmp.cmp(pdf, KITAP, shallow=False)
    for i in range(12): olc('sayfa ileri (ilk kez)', w.goto, 1); app.processEvents()
    for i in range(12): olc('sayfa geri (görülmüş)', w.goto, -1); app.processEvents()
    for i in range(12): olc('sayfa ileri (görülmüş)', w.goto, 1); app.processEvents()
    R['onbellekteki_sayfa_dogru'] = (w.board.image == taze())
    b = w.board; w.set_tool('pen'); b.begin(QPointF(300, 300))
    for k in range(1, 30): b.move(QPointF(300 + k*6, 300 + (k % 3)*5))
    b.finish(); app.processEvents(); sekme1 = w.current_tab(); sayfa1 = w.page; yazi1 = yazilar()
    olc('yazılı kitap açma (400 sayfa, 3 sayfada eski yazı)', w.open_pdf_path, NOTLU); app.processEvents(); bosalt(); don(300)
    R['notlu_kitaptan_gelen_yazi'] = yazilar(); sekme2 = w.current_tab(); yazi2 = yazilar()
    w.goto(3); app.processEvents(); R['notlu_sayfa_4_yazi_bir_kez'] = len(w.marks.get(3, [])) == 1
    olc('sekmeye dönüş (kitap)', w.switch_tab, sekme1); app.processEvents()
    R['donuste_sayfa_ayni'] = (w.page == sayfa1); R['donuste_yazi_ayni'] = (yazilar() == yazi1); R['donuste_goruntu_dogru'] = (w.board.image == taze())
    olc('sekmeye dönüş (yazılı kitap)', w.switch_tab, sekme2); app.processEvents()
    R['notlu_donuste_yazi_ayni'] = (yazilar() == yazi2); R['notlu_donuste_goruntu_dogru'] = (w.board.image == taze())
    for i in range(6): olc('sekmeler arası gidiş geliş', w.switch_tab, sekme1 if i % 2 == 0 else sekme2); app.processEvents()
    # bayat görüntü denetimi: aynı sekmede belge değişince eski sayfanın görüntüsü gelmemeli
    w.switch_tab(sekme1); app.processEvents(); onceki = QImage(w.board.image)
    w.replace(tk.make_board('white', 960, 1080), ''); app.processEvents()
    R['belge_degisince_eski_goruntu_geldi'] = (w.board.image == onceki); R['yeni_belge_goruntu_dogru'] = (w.board.image == taze())
    bosalt(); don(200); w.goto(0); app.processEvents(); R['kayittan_sonra_goruntu_dogru'] = (w.board.image == taze())
    if yeni: R['onbellek_mb'] = round(sum(v.sizeInBytes() for v in tk.SAYFA_OB.values())/1048576, 1); R['onbellek_sayfa'] = len(tk.SAYFA_OB)
    cikti(islem_sureleri_ms={k: ozet(v) for k, v in SURE.items()}, **R)

def s_zoom():
    R = {}; yeni = hasattr(w, 'net_ciz')
    w.open_pdf_path(KITAP); app.processEvents(); bosalt(); don(300); z0 = w.zoom
    for k in range(1, 26): olc('iki parmak adımı (eski yol: her adımda net çizim)', w.set_zoom, z0*(1.035**k)); app.processEvents()
    w.set_zoom(z0); app.processEvents()
    if yeni:
        for k in range(1, 26): olc('iki parmak adımı (yeni: görüntü gerilir)', w.set_zoom, z0*(1.035**k), True); app.processEvents()
        R['hareket_sirasinda_net_bekliyor'] = bool(getattr(w, '_net_bekliyor', False)); bulanik = (w.board.image == taze())
        don(600); R['hareket_bitince_net_cizildi'] = not getattr(w, '_net_bekliyor', True); R['son_goruntu_dogru'] = (w.board.image == taze()); R['hareket_sirasinda_goruntu_zaten_net_miydi'] = bulanik
        R['olcek_dogru'] = abs(w.board.scale - w.zoom) < 1e-9 and abs(w.zoom - z0*(1.035**25)) < 1e-6
    cikti(islem_sureleri_ms={k: ozet(v) for k, v in SURE.items()}, **R)

def calis():
    try: dict(onar=s_onar, pdf=s_pdf, zoom=s_zoom)[SENARYO]()
    except Exception: traceback.print_exc(); cikti(hata=traceback.format_exc()[-600:])
    sys.stdout.flush(); os._exit(0)
QTimer.singleShot(3000, calis)
QTimer.singleShot(240000, lambda: (cikti(zaman_asimi=True), os._exit(2)))
app.exec_()
