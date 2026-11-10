# Sanal tahtada gerçek Qt ile Atlas önizlemeleri: panel, tam ekran, tahtaya yazılan el yazısı, grafik çizici etiketi.
import sys, os, importlib.util
sys.path.insert(0, '/usr/lib/umal-tahta/python')
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
spec = importlib.util.spec_from_file_location('tk', '/usr/share/tahta-kalem/tahta_kalem.py'); tk = importlib.util.module_from_spec(spec); spec.loader.exec_module(tk)
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QImage, QPainter, QColor, QPen, QPainterPath
from PyQt5.QtCore import Qt, QPointF
import traceback as _tb
sys.excepthook = lambda t, v, b: _tb.print_exception(t, v, b)   # uygulamadaki gibi: hata Qt'yi düşürmesin
app = QApplication(sys.argv); tk.ui_fonts()
CEVAP = r"""y = 2x doğrusunu inceleyelim:
• Bu doğru orijinden geçer ve eğimi $m = 2$'dir.
• $x = 0$ için $y = 0$; $x = 1$ için $y = 2$ olur.

1. Eğim:
• $m = \frac{\Delta y}{\Delta x} = \frac{2 - 0}{1 - 0} = 2$
• Eğim pozitif olduğu için doğru soldan sağa yükselir.

2. Parabolle karşılaştırma:
• $f(x) = x^{2} - 4x + 3$ için tepe noktası $r = -\frac{b}{2a} = 2$
• Kökler: $x_{1} = 1$, $x_{2} = 3$; $\sqrt{x^{2} + 9} = 5$

Cevap: $y = 2x$, orijinden geçen ve eğimi $2$ olan bir doğrudur."""
class Ana(QWidget):
    data_dir = '/tmp/atlas-onizleme'
    def board_info(self): return {'sinif': '9-A'}
    def exam_clock(self): return None
    def run_havuz(self, *a): pass
os.makedirs('/tmp/onizleme', exist_ok=True)
ana = Ana(); ana.resize(1920, 1080); ana.setAutoFillBackground(True); pal = ana.palette(); pal.setColor(ana.backgroundRole(), QColor('#0d1726')); ana.setPalette(pal)
pn = tk.AtlasPanel(ana); ana.atlas_panel = pn; pn.ac(None)
pn.cevap = CEVAP; pn.metin.setPlainText(CEVAP, True); pn.yaz_b.setEnabled(True); pn.tekrar_b.setEnabled(True); pn.derin_b.setEnabled(True)
pn.grafik = ['2*x']; pn.grafik_b.show(); pn.maskot.ifade('konusma'); pn.durum.setText('Bugün 4 / 30')
pn.yerlestir(); ana.show(); app.processEvents(); app.processEvents()
ana.grab().save('/tmp/onizleme/panel.png')
gk = tk.GenisKlavye(ana); gk.ac(pn.giris); pn.giris.setText('Fonksiyonun grafiğini çiz ve kök'); gk.esitle(); app.processEvents(); app.processEvents(); ana.grab().save('/tmp/onizleme/panel-klavye.png'); gk.kb.matematik(True); app.processEvents(); app.processEvents(); ana.grab().save('/tmp/onizleme/panel-klavye-mat.png'); gk.kb.matematik(False); gk.hide(); pn.giris.clear(); app.processEvents()
pn.tam_ekran(True); app.processEvents(); app.processEvents(); pn.metin._ciz(); app.processEvents()
ana.grab().save('/tmp/onizleme/tam-ekran.png')
# Tahtaya yaz: gerçek kalem çizgileri
cz, h = tk.murekkep_cizgileri(CEVAP, 900, 30, '#1d3fa8', 2.4, os.path.join(tk.UI_FONT_DIR, 'ReliefSingleLineSVG-Regular.svg'), tk.atlas_guzel)
im = QImage(980, int(h) + 60, QImage.Format_RGB32); im.fill(QColor('#ffffff')); p = QPainter(im); p.setRenderHint(QPainter.Antialiasing)
for s in cz:
    p.setPen(QPen(QColor(s['color']), s['width'], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)); pts = s['points']
    path = QPainterPath(QPointF(pts[0][0] + 40, pts[0][1] + 30))
    for x, y in pts[1:]: path.lineTo(x + 40, y + 30)
    p.drawPath(path)
p.end(); im.save('/tmp/onizleme/tahtaya-yaz.png'); print('çizgi', len(cz))
# Grafik çizici
fs = []
for t, c in (('x^2 - 4*x + 3', '#2563eb'), ('1/(x-2)', '#e11d48')):
    fn, err = tk.graph_compile(t); fs.append((t, fn, c))
doc = tk.graph_build(fs, {'roots': True, 'extrema': True, 'cross': False, 'yx': False}); pix = doc[0].get_pixmap(matrix=tk.fitz.Matrix(2, 2), alpha=False); pix.save('/tmp/onizleme/grafik.png')
print('önizleme tamam')
# K-351: kara tahtalar (gerçek make_board + çerçeve parçaları + beyaz el yazısı)
from PyQt5.QtGui import QPixmap
yazi, hy = tk.murekkep_cizgileri(r"Fonksiyonlar" + "\n" + r"$f(x) = x^{2} - 4x + 3$" + "\n" + r"Kökler: $x_{1} = 1$, $x_{2} = 3$" + "\n" + r"Tepe noktası: $T(2, -1)$", 420, 26, '#ffffff', 2.0, os.path.join(tk.UI_FONT_DIR, 'ReliefSingleLineSVG-Regular.svg'), tk.atlas_guzel)
for bg in tk.KARA_TAHTALAR:
    doc = tk.make_board(bg, 960, 1080); px = doc[0].get_pixmap(matrix=tk.fitz.Matrix(2, 2), alpha=False, clip=tk.fitz.Rect(0, 0, 960, 540))
    im = QImage(px.samples, px.width, px.height, px.stride, QImage.Format_RGB888).copy()
    p = QPainter(im); p.setRenderHint(QPainter.Antialiasing)
    for s in yazi:
        p.setPen(QPen(QColor(s['color']), s['width']*2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)); pts = s['points']
        path = QPainterPath(QPointF(pts[0][0]*2 + 200, pts[0][1]*2 + 160))
        for x, y in pts[1:]: path.lineTo(x*2 + 200, y*2 + 160)
        p.drawPath(path)
    W, H = im.width(), im.height(); k, a = 7, 18
    for tur, g_ in (('ust', (0, 0, W, k)), ('sol', (0, 0, k, H)), ('sag', (W - k, 0, k, H)), ('alt', (0, H - a, W, a)), ('silgi', (W - 230, H - a - 30, 170, 40))):
        w_ = tk.KaraTahtaCerceve(None, tur); w_.resize(g_[2], g_[3]); pm = w_.grab(); p.drawPixmap(g_[0], g_[1], pm)
    p.end(); im.save('/tmp/onizleme/kara-%s.png' % bg)
print('kara tahtalar tamam')
# K-352: yeni Grafik çizici ve grafik sekmesi
try:
    class GA(QWidget):
        data_dir = '/tmp/atlas-onizleme'
        graph_cfg = {'f0': 'x² − 4x + 3', 'f1': 'log_2(x+1)', 'f2': '', 'isaret': 'tepe'}
        def board_info(self): return {'sinif': '9-A'}
        def exam_clock(self): return None
    ga = GA(); ga.resize(1920, 1080)
    dlg = tk.GraphDialog(ga); dlg.resize(1860, 1020); dlg.show()
    for _ in range(6): app.processEvents()
    dlg.redraw(); app.processEvents(); dlg.grab().save('/tmp/onizleme/grafik-cizici.png')
    dlg.fields[0].setText('a·x² + b·x + c'); dlg.fields[1].setText(''); app.processEvents(); dlg.redraw()
    sl = dlg.sliders.get('a')
    if sl: sl.setValue(-10)
    for _ in range(4): app.processEvents()
    dlg.redraw(); app.processEvents(); dlg.grab().save('/tmp/onizleme/grafik-kaydirici.png')
    dlg.fields[0].setText('kök(□,□)'); app.processEvents(); dlg.alan_degisti(); app.processEvents(); dlg.grab().save('/tmp/onizleme/grafik-kutu.png')
    dlg.close()
    # grafik sekmesi: kara tahta + çerçeve + İncele + Atlas
    durum = {'f': ['x² − 4x + 3', '', ''], 'param': {}, 'isaret': 'tepe'}
    bilgi = {}; doc = tk.grafik_belge(durum, bilgi)
    px = doc[0].get_pixmap(matrix=tk.fitz.Matrix(2, 2), alpha=False); im = QImage(px.samples, px.width, px.height, px.stride, QImage.Format_RGB888).copy()
    class FM: pass
    fm = FM(); fm.scroll = QWidget(); fm.scroll.resize(1920, 1080); fm.doc = doc; fm._sinav_su_an = False
    gi = tk.GrafikIncele(fm); gi.esitle(); gi.atlas.oner(durum, bilgi); gi.show(); gi.adjustSize(); gi.atlas.adjustSize(); app.processEvents()
    p = QPainter(im); W, H = im.width(), im.height()
    for tur, g_ in (('ust', (0, 0, W, 7)), ('sol', (0, 0, 7, H)), ('sag', (W - 7, 0, 7, H)), ('alt', (0, H - 18, W, 18)), ('silgi', (W - 230, H - 48, 170, 40))):
        w_ = tk.KaraTahtaCerceve(None, tur); w_.resize(g_[2], g_[3]); p.drawPixmap(g_[0], g_[1], w_.grab())
    gi.adjustSize(); gi.resize(gi.sizeHint()); g1 = gi.grab(); gy = tk.GRAFIK_H*2 + 16
    p.drawPixmap((W - g1.width())//2, gy, g1); at = gi.atlas.grab(); p.drawPixmap(W - at.width() - 24, gy - at.height() - 10, at)
    gi.dug['tablo'].setChecked(True); gi.dug['tepe'].setChecked(False)
    gi.tablo.setText('<table cellspacing="0"><tr><td style="padding:1px 10px;color:#7ff6ff"><b>x</b></td>' + ''.join('<td style="padding:1px 10px;border-left:1px solid #2a4468">%d</td>' % x for x in range(-2, 5)) + '</tr><tr><td style="padding:1px 10px;color:#7ff6ff"><b>y</b></td>' + ''.join('<td style="padding:1px 10px;border-left:1px solid #2a4468">%d</td>' % (x*x-4*x+3) for x in range(-2, 5)) + '</tr></table>')
    gi.r2.show(); app.processEvents(); gi.adjustSize(); gi.resize(gi.sizeHint()); g2 = gi.grab(); p.drawPixmap((W - g2.width())//2, gy + g1.height() + 30, g2); p.end()
    im.save('/tmp/onizleme/grafik-tahta.png')
    # grafik sekmesinin tamamı: üstte grafik, altta Atlas'ın el yazısı cevabı (üst üste binmez)
    px = doc[0].get_pixmap(matrix=tk.fitz.Matrix(1, 1), alpha=False); im2 = QImage(px.samples, px.width, px.height, px.stride, QImage.Format_RGB888).copy()
    cz2, _ = tk.murekkep_cizgileri(r"1. $y = x$ birim fonksiyondur." + "\n" + r"2. Orijinden geçer, eğimi $1$'dir." + "\n" + r"Cevap: $y = x$ birinci açıortay doğrusudur.", 820, 24, '#ffffff', 1.8, os.path.join(tk.UI_FONT_DIR, 'ReliefSingleLineSVG-Regular.svg'), tk.atlas_guzel)
    p = QPainter(im2); p.setRenderHint(QPainter.Antialiasing)
    for s_ in cz2:
        p.setPen(QPen(QColor(s_['color']), s_['width'], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)); pts = s_['points']
        path = QPainterPath(QPointF(pts[0][0] + 40, pts[0][1] + tk.GRAFIK_H + 16))
        for x, y in pts[1:]: path.lineTo(x + 40, y + tk.GRAFIK_H + 16)
        p.drawPath(path)
    p.end(); im2.save('/tmp/onizleme/grafik-sekme-tam.png')
    for k in ('kok', 'ykes', 'asimptot', 'alan', 'teget'):
        d2 = {'f': ['x² − 4x + 3' if k != 'asimptot' else '1/(x-2)', '', ''], 'isaret': k, 'ek': {}}
        dd = tk.grafik_belge(d2); px = dd[0].get_pixmap(matrix=tk.fitz.Matrix(1.2, 1.2), alpha=False); px.save('/tmp/onizleme/grafik-%s.png' % k)
    print('grafik tamam')
except Exception as e:
    import traceback; traceback.print_exc()
# K-355: uygulamanın öteki pencerelerindeki klavye (ör. öğrenci arama)
try:
    from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QLabel
    dl = QDialog(); dl.setStyleSheet('QDialog{background:#0f1c2e;} QLabel{color:white;font-size:24px;} QLineEdit{font-size:24px;padding:10px;background:#0a1628;color:white;border:2px solid #22e8ff;border-radius:12px;}')
    vv = QVBoxLayout(dl); vv.setContentsMargins(30, 24, 30, 24); vv.addWidget(QLabel('Nerede sınava gireceğim?')); ed = QLineEdit('Ayşe'); vv.addWidget(ed)
    kb = tk.attach_touch_keyboard(dl, ed, vv); kb.attach(ed); kb.show(); dl.resize(1100, 560); dl.show()
    for _ in range(4): app.processEvents()
    dl.grab().save('/tmp/onizleme/pencere-klavye.png')
except Exception:
    import traceback; traceback.print_exc()
# K-364: sayfada yer yoksa çözüm alanına
try:
    import glob, fitz
    from PyQt5.QtCore import QRectF, QTimer
    pdfler = sorted(glob.glob('pdf/*.pdf'))
    if pdfler:
        ana.hide()
        w = tk.Window(); w.resize(1920, 1080); w.show(); app.processEvents()
        for _ in range(30): app.processEvents()
        for d_ in list(getattr(w, 'findChildren')(QWidget)):
            pass
        w.start_tab('Diziler', pdfler[0]); w.replace(fitz.open(pdfler[0]), pdfler[0]); w.tabs_changed()
        for _ in range(20): app.processEvents()
        try:
            [getattr(w, n_).hide() for n_ in ('welcome', 'intro') if getattr(w, n_, None) is not None]; w.atlas_yuzen.durum(); w.place_overlays(); app.processEvents(); w.grab().save('/tmp/onizleme/panel-yeni.png')
            yp = w.yeni_panel; yp.bolumler[0][0].setChecked(True); app.processEvents(); w.grab().save('/tmp/onizleme/panel-yeni-acik.png'); yp.bolumler[0][0].setChecked(False)
            yp.sekme(1); app.processEvents(); w.grab(yp.geometry().adjusted(-4,-4,4,4) if False else w.rect()).save('/tmp/onizleme/panel-ekle.png')
            yp.sekme(2); app.processEvents(); w.grab().save('/tmp/onizleme/panel-okul.png'); yp.sekme(0)
            w.panel_daralt(True); app.processEvents(); app.processEvents(); w.place_overlays(); w.grab().save('/tmp/onizleme/panel-dar.png'); w.panel_daralt(False); app.processEvents()
            w.open_folder(w.tools_popup, w.tools_button); app.processEvents(); w.tools_popup.grab().save('/tmp/onizleme/araclar-menu.png'); w.tools_popup.hide()
            print('maskot görünür:', w.atlas_yuzen.isVisible(), w.atlas_yuzen.geometry())
            # K-367: dokununca ekrandaki yazıya bakar (gerçek Atlas çağrısı)
            w.start_tab('Boş', None) if False else None
            bos = tk.make_board('kt_kareli', 960, 1080); w.replace(bos, persist=False); w.marks = {0: []}
            import math as _m
            def cizgi(pts): w.marks[0].append(dict(tool='pen', color='#ffffff', width=3, points=[list(q) for q in pts]))
            F = '/usr/share/tahta-kalem/fonts/ReliefSingleLineSVG-Regular.svg'
            cz, _h = tk.murekkep_cizgileri('y = 2x − 3\ny = x²', 600, 56, '#ffffff', 3, F, tk.atlas_guzel)
            for c in cz: w.marks[0].append(dict(c, points=[[q[0] + 120, q[1] + 140] for q in c['points']]))
            w.board.update(); [getattr(w, n_).hide() for n_ in ('welcome', 'intro') if getattr(w, n_, None) is not None]
            for _ in range(10): app.processEvents()
            w.atlas_yuzen.durum(); w.atlas_yuzen.dokundu()
            import time as _t
            t0 = _t.time()
            while _t.time() - t0 < 25 and getattr(w.atlas_yuzen, 'bekleyen', None): app.processEvents(); _t.sleep(0.1)
            for _ in range(10): app.processEvents()
            w.atlas_yuzen.balon_goster('Tahtaya y = 2x − 3 ve y = x² yazdınız. Ne yapayım?', ['Grafiklerini çiz', 'Kesişimini bul', 'Köklerini hesapla', 'Başka bir şey sor…']); app.processEvents(); app.processEvents()
            w.grab().save('/tmp/onizleme/atlas-dokun.png'); print('balon:', w.atlas_yuzen.balon.yazi.text()[:200], [b_.text() for b_ in w.atlas_yuzen.balon.dug])
        except Exception: _tb.print_exc()
        for _ in range(20): app.processEvents()
        sy = w.doc[0].rect
        r = QRectF(sy.width*0.5, sy.height*0.80, sy.width*0.47, sy.height*0.12)   # alttaki soru: altında yer yok
        w.atlas_son_cerceve = (0, r)
        w.atlas_sor_ac(None); ap = w.atlas_panel
        ap.cevap = r"""1. Aritmetik dizide $a_{n} = a_{3} + (n - 3)d$ kullanılır.
2. $a_{5} = 7 + 2 \cdot (-2) = 3$
Cevap: C) 3"""
        ap.tahtaya_yaz()
        import time
        t0 = time.time()
        while time.time() - t0 < 3: app.processEvents(); time.sleep(0.05)
        w.grab().save('/tmp/onizleme/cozum-alani-atlas.png')
        print('cozum alanı:', (w.doc.metadata or {}).get('keywords'), len(w.marks.get(0, [])))
        # K-392: PDF sayfasındayken "Tahtaya yaz" → yeni sekme, kara tahta, beyaz kalem
        try:
            w.start_tab('Diziler', pdfler[0]); w.replace(fitz.open(pdfler[0]), pdfler[0]); w.tabs_changed()
            for _ in range(10): app.processEvents()
            w.grab().save('/tmp/onizleme/yenisekme-once.png')
            w.atlas_sor_ac(None); ap = w.atlas_panel
            ap.cevap = "Müsilaj (deniz salyası), besin elementlerinin artması ve akıntının azalması nedeniyle alglerin aşırı çoğalmasıyla oluşur.\nSu yüzeyini kaplayan bu örtü fotosentezi engeller."
            ap.tahtaya_yaz(); t0 = time.time()
            while time.time() - t0 < 3: app.processEvents(); time.sleep(0.05)
            w.grab().save('/tmp/onizleme/yenisekme-atlas.png')
            print('yeni sekme:', repr(w.source), w.background, w.color, len(w.marks.get(0, [])), [t.get('name') for t in (w.tabs or [])][:4])
        except Exception: _tb.print_exc()
except Exception:
    _tb.print_exc()
# K-382: açı şapkası · K-383: Yerimi göster
try:
    T2 = "Paralelkenarda karşılıklı açılar eşittir.\nİstenen m(\\widehat{DCB}) açısı: $m(\\widehat{DCB}) = 4x - 10 = 42$\nAyrıca $\\overline{AB} \\parallel \\overline{DC}$ ve $\\vec{u}$ vektörü."
    cz, h = tk.murekkep_cizgileri(T2, 900, 34, '#ffffff', 2.6, os.path.join(tk.UI_FONT_DIR, 'ReliefSingleLineSVG-Regular.svg'), tk.atlas_guzel)
    im = QImage(980, int(h) + 60, QImage.Format_RGB32); im.fill(QColor('#14284a')); p = QPainter(im); p.setRenderHint(QPainter.Antialiasing)
    for s in cz:
        p.setPen(QPen(QColor(s['color']), s['width'], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)); pts = s['points']
        path = QPainterPath(QPointF(pts[0][0] + 40, pts[0][1] + 30))
        for x, y in pts[1:]: path.lineTo(x + 40, y + 30)
        p.drawPath(path)
    p.end(); im.save('/tmp/onizleme/sapka.png'); print('şapka çizgi', len(cz)); print('balon:', tk.latex_duz(r'm(\widehat{DCB}) = 4x - 10'))
except Exception: _tb.print_exc()
try:
    import datetime
    adlar = ['Zeynep Acar', 'Mina Arslan', 'Mevlüt Eren Çerçi', 'Nisanur Yüksel', 'Eymen Aras Söğüt', 'Berat Barkoci', 'Yiğit Onur Sağlam', 'Bade Nur Koç', 'Açelya Aslantaş', 'Aysu Kaya']
    sv = ['10-F', '9-D', '10-H', '9-B', '11-B', '11-A', '10-C', '10-C', '10-F', '9-B']
    liste = [dict(sira=i + 1, no=str(100 + i), ad=adlar[i % 10], sinif=sv[i % 10], ders='Coğrafya' if sv[i % 10][:2] in ('9-', '10') else 'S. Coğrafya') for i in range(38)]
    ana2 = QWidget(); ana2.resize(1600, 900)
    d_ = tk.YerimDialog(ana2, dict(tur='salon', sinif='10-C', liste=liste), '4. Ders', datetime.date(2026, 11, 10), 17)
    d_.resize(1600, 900); d_.show(); app.processEvents(); app.processEvents(); d_.grab().save('/tmp/onizleme/yerim.png'); print('yerim sıra kutusu:', d_.seat_rects.get(17))
except Exception: _tb.print_exc()

# K-385: anket formu — rakam tuş takımı, biçim, yazarken görünür
try:
    import json as _j
    a = _j.load(open('anket-ornek.json'))
    ana3 = QWidget(); ana3.resize(1920, 1080); ana3.show()
    f = tk.AnketForm(ana3, a, '2765', 'Evin Polat', lambda v: None)
    f.setFixedSize(1600, 900); f.show(); app.processEvents()
    e_tc, e_dt, e_tel = f.edits[0], f.edits[1], f.edits[2]
    f.alan_sec(e_tc); app.processEvents()
    for ch in '1234567890': f.tus_bas(ch)
    app.processEvents(); f.grab().save('/tmp/onizleme/anket-tc.png')
    f.setFixedSize(1280, 720); app.processEvents(); f.grab().save('/tmp/onizleme/anket-tc-kucuk.png'); f.setFixedSize(1600, 900)
    f.alan_sec(e_dt); 
    for ch in '0305200': f.tus_bas(ch)
    app.processEvents(); f.grab().save('/tmp/onizleme/anket-tarih.png')
    for ch in '9': f.tus_bas(ch)
    f.alan_sec(e_tel)
    for ch in '05321234567': f.tus_bas(ch)
    app.processEvents(); f.grab().save('/tmp/onizleme/anket-telefon.png'); print('anket değerler:', f.vals)
except Exception: _tb.print_exc()
# K-393: LibreOffice olmadan PowerPoint → PDF (Atlas'ın kendi çeviricisi)
try:
    import shutil as _sh; _sh.copy('ornek.pptx', '/tmp/ornek.pptx')
    n_ = tk.pptx_yedek_pdf('/tmp/ornek.pptx', '/tmp/ornek.pdf'); print('pptx sayfa:', n_)
    d_ = fitz.open('/tmp/ornek.pdf')
    for i_ in range(d_.page_count): d_[i_].get_pixmap(dpi=60).save('/tmp/onizleme/pptx-%d.png' % (i_ + 1))
except Exception: _tb.print_exc()
# K-394: sekme geçişi / kapatma
try:
    w.start_tab('Deneme A'); w.replace(tk.make_board('kt_kareli', 960, 1080)); w.tabs_changed(); w.save_session()
    ids = [t['id'] for t in w.tabs]; print('sekmeler', len(ids))
    w.switch_tab(ids[-1]); app.processEvents(); w.switch_tab(ids[0]); app.processEvents()
    print('sekme geçişi tamam', w.current_tab() == ids[0])
except Exception: _tb.print_exc()
# K-402: anma klibi (pakette kurulu anma/): 4 örnek an
try:
    import os as _os
    _os.makedirs('/tmp/onizleme', exist_ok=True); w.showNormal(); w.resize(1920, 1080)
    for _ in range(5): app.processEvents()
    tm = tk.anma_tanim(); print('anma tanım:', bool(tm), tk.ANMA_DIR)
    ae = tk.AnmaEkrani(w, tm); ae.zam.stop()
    for k_, t_ in enumerate((0.5, 12.3, 33.7, 58.0)):
        ae.t0 = time.monotonic() - t_; ae.setGeometry(w.rect()); ae.repaint(); app.processEvents()
        ae.grab().scaled(960, 540, Qt.IgnoreAspectRatio, Qt.SmoothTransformation).save('/tmp/onizleme/anma-%d.png' % k_)
    ae.bitir(); print('anma tamam')
except Exception: _tb.print_exc()
# K-415: acil mesaj fotoğraflı
try:
    from PyQt5.QtGui import QImage as _QI
    im = _QI(1200, 800, _QI.Format_RGB32); im.fill(QColor('#3a3a3a')); p_ = QPainter(im); p_.setPen(QColor('white')); p_.drawText(im.rect(), Qt.AlignCenter, 'FOTOĞRAF'); p_.end(); im.save('/tmp/acil.jpg')
    ov = tk.AcilMesaj(w); ov.setGeometry(w.rect()); ov.goster(dict(id='t', baslik='Saygı Duruşu', metin="Saat 09.05'te saygı duruşu ve İstiklal Marşı", resim_yol='/tmp/acil.jpg')); ov.show(); ov.raise_()
    for _ in range(5): app.processEvents()
    ov.grab().save('/tmp/onizleme/acil-resim.png')
    ov.goster(dict(id='t2', resim_yol='/tmp/acil.jpg')); ov.repaint(); app.processEvents(); ov.grab().save('/tmp/onizleme/acil-resim2.png'); ov.hide(); print('acil resim tamam')
except Exception: _tb.print_exc()
# K-422: oturma planı çizimi önbellekli: eskiyle aynı mı, ne kadar sürüyor
try:
    import urllib.request as _ur, types as _ty
    blob = _ur.urlopen(tk.KELEBEK_URLS[0], timeout=60).read(); kb_ = tk.kelebek_open(blob)
    fot_ = tk.kelebek_open(_ur.urlopen(tk.KELEBEK_FOTO_URLS[0], timeout=60).read()).get('fotolar', {})
    pl_ = kb_['planlar'][0]; sal_ = sorted(pl_['salonlar'], key=lambda s: -len(pl_['salonlar'][s]))[0]
    plan_ = dict(sinif=sal_, liste=pl_['salonlar'][sal_], tur='salon', saat='10.30 – 11.10')
    sp_ = importlib.util.spec_from_file_location('eski', _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'eski68.py')); es_ = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(es_)
    from PyQt5.QtGui import QImage as _QI, QFont as _QF
    def _font(px, b=False):
        f = _QF(tk.ui_fonts().get('Poppins-Medium') or 'Sans'); f.setPixelSize(int(px)); f.setBold(b); return f
    res_ = {}
    for ad_, m_ in (('eski', es_), ('yeni', tk)):
        m_._PHOTOS['data'] = fot_; m_._PHOTOS['pix'] = {}; m_._PHOTOS['img'] = {}
        if ad_ == 'yeni':
            t1_ = time.perf_counter(); m_.foto_on_coz([r.get('no') for r in plan_['liste']])
            import threading as _th
            while any(t_.name != 'MainThread' and t_.is_alive() for t_ in _th.enumerate()) and time.perf_counter() - t1_ < 30: time.sleep(0.05)
            print('foto ön çözme', round(time.perf_counter() - t1_, 2), 's', len(m_._PHOTOS['img']))
        m_.time = _ty.SimpleNamespace(**{a: getattr(time, a) for a in dir(time) if not a.startswith('_')}); m_.time.time = lambda: 1000.0
        o_ = type('O', (), {})(); ts_ = []; ims_ = []
        for i_ in range(3):
            im_ = _QI(1920, 1080, _QI.Format_RGB32); p_ = QPainter(im_); t0_ = time.perf_counter()
            m_._draw_seatmap(o_, p_, 1920, 1020, 1.0, _font, plan_, '#5cc8ff', '#5cc8ff', 'Coğrafya · 10 Kasım'); p_.end(); ts_.append(round(time.perf_counter() - t0_, 3)); ims_.append(im_)
        res_[ad_] = ims_; print('seatmap', ad_, sal_, len(plan_['liste']), 'öğrenci, süre', ts_)
    res_['yeni'][0].save('/tmp/onizleme/seatmap-yeni.png'); res_['eski'][0].save('/tmp/onizleme/seatmap-eski.png')
    print('seatmap ayni:', res_['eski'][0] == res_['yeni'][0], res_['eski'][0] == res_['yeni'][2])
except Exception: _tb.print_exc()
# K-422b: gece kara tahta: noktalı çizgi ile aynı görüntü mü, uzatma ne kadar sürüyor
try:
    for ad_, m_ in (('eski', es_), ('yeni', tk)):
        for h_ in (1080, 5000, 20000):
            t0_ = time.perf_counter(); d_ = m_.make_board('kt_gece', 960, h_); t1_ = time.perf_counter()
            pm_ = d_[0].get_pixmap(clip=m_.fitz.Rect(0, 0, 960, 540)); t2_ = time.perf_counter()
            print('gece', ad_, h_, 'yap', round(t1_ - t0_, 3), 'çiz', round(t2_ - t1_, 3))
            if h_ == 1080: pm_.save('/tmp/onizleme/gece-%s.png' % ad_)
except Exception: _tb.print_exc()
# K-424: coğrafya sınav teması
try:
    import time as _t2
    for i_, tt_ in enumerate((1000.0, 1004.0)):
        im_ = _QI(1920, 1080, _QI.Format_RGB32); im_.fill(QColor('#0d1726')); p_ = QPainter(im_)
        t0_ = _t2.perf_counter(); tk.draw_exam_theme(p_, 1920, 1080, 1.0, 'harita', '#3fd0c9', tt_); print('cografya tema', round(_t2.perf_counter() - t0_, 4), 's'); p_.end(); im_.save('/tmp/onizleme/cografya-tema-%d.png' % i_)
    plc_ = next(p for p in kb_['planlar'] if p['tarih'] == '2026-11-10'); slc_ = sorted(plc_['salonlar'], key=lambda s: -len(plc_['salonlar'][s]))[0]
    tk.time = _t2; tk._PHOTOS['data'] = fot_; tk._PHOTOS['pix'] = {}
    im_ = _QI(1920, 1080, _QI.Format_RGB32); im_.fill(QColor('#0d1726')); p_ = QPainter(im_)
    tk._draw_seatmap(type('O', (), {})(), p_, 1920, 1080, 1.0, _font, dict(sinif=slc_, liste=plc_['salonlar'][slc_], tur='salon', saat='10.30 – 11.10'), '#5cc8ff', '#5cc8ff', '4. Ders · 10 Kasım'); p_.end()
    im_.save('/tmp/onizleme/cografya-salon.png'); print('cografya salon tamam', slc_)
except Exception: _tb.print_exc()
# K-425: öğrenci araması uçak bileti (örnek öğrenci)
try:
    import datetime as _dt
    plb_ = dict(tarih=_dt.date.today().isoformat(), ders='8. Ders', salonlar={'10-C': [dict(no='99999', ad='DENEME ÖĞRENCİ ADI', sinif='11-B', sira=17, ders='COĞRAFYA')]}, siniflar={})
    w.kelebek = dict(planlar=[plb_]); w.exam_clock = lambda: _dt.datetime.combine(_dt.date.today(), _dt.time(9, 0))
    d_ = tk.OgrenciAraDialog(w); d_.resize(1200, 1000); d_.show(); d_.edit.setText('99999')
    for _ in range(8): app.processEvents()
    d_.grab().save('/tmp/onizleme/bilet.png'); print('bilet tamam', d_.kart.isVisible(), d_.yer.isVisible()); d_.reject()
except Exception: _tb.print_exc()
