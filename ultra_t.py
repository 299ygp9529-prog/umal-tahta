import sys, os, subprocess, datetime, json
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
tk.KELEBEK_URLS = (); tk.KELEBEK_FOTO_URLS = ()
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor
# K-544 sınaması: sahte (uydurma) ders programı — gerçek öğretmen adı yok
D = ['Matematik', 'Matematik', 'Türk Dili ve Edebiyatı', 'Fizik', 'İngilizce', 'İngilizce', 'Biyoloji', 'Tarih']
H = ['Deneme Öğretmen BİR', 'Deneme Öğretmen BİR', 'Örnek Hoca İKİ', 'Test Öğretmen ÜÇ', 'Deneme DÖRT', 'Deneme DÖRT', 'Örnek BEŞ', 'Test ALTI']
prog = {'9-A': {'%d-%d' % (g, n + 1): dict(ders=D[(n + g*3) % 8], ogretmen=[H[(n + g*3) % 8]]) for g in range(5) for n in range(8)}}
open('/tmp/dp.json', 'w').write(json.dumps(dict(siniflar=prog), ensure_ascii=False))
tk.LESSON_FILE = '/tmp/dp.json'; tk._LESSON_TABLE.clear()
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
w = tk.Window(); w.showFullScreen(); app.processEvents()
SAAT = datetime.datetime(2026, 11, 16, 10, 24)
w.exam_clock = lambda: SAAT; w.board_info = lambda: {'sinif': '9-A'}; w.exam_hidden = None; w.exams = []; w.upcoming_plans = lambda *a, **k: []
def cek(ad): app.processEvents(); subprocess.run(['import', '-window', 'root', '/tmp/onizleme/u-%s.png' % ad])
E = [None]
def a1():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    print('sinif', w.board_info().get('sinif'), 'program var:', w.ders_programi_var())
    print('bugün:', tk.bugun_dersleri('9-A', SAAT))
    w.last_touch = 0; st = w.exam_preview(); print('faz', st and st.get('phase'), 'dersler', st and len(st['tn'].get('dersler') or []))
    E[0] = tk.ExamScreen(w); E[0].fit(w.scroll.viewport().rect()); E[0].set_state(st, '9'); E[0].show(); E[0].raise_()
def a2():
    cek('teneffus'); w.open_ders_programi(); app.processEvents()
def a3():
    cek('program'); w.ders_prog.hide(); E[0].hide(); d = tk.OkulAraclari(w); d.show(); app.processEvents(); E.append(d)
def a4():
    cek('okul'); E[-1].reject()
    tk.SAAT2 = datetime.datetime(2026, 11, 20, 13, 40)   # Cuma 7. ders sırasında
    w.open_ders_programi.__func__; w.ders_prog.ac('9-A', datetime.datetime(2026, 11, 20, 13, 40)); app.processEvents()
def a5():
    cek('program-cuma'); w.ders_prog.hide(); del w.board_info
    i_ = w.board_info(); i_['sinif'] = '9-A'; w.save_board_info(i_)
    w.cihaz_kimligi = lambda: 'abc123'
    w.run_command({'id': 'sn-baska', 'komut': 'sinif', 'cihaz': 'zzz', 'yeni': '11-C'}); print('başka cihaz sonrası:', w.board_info().get('sinif'))
    w.run_command({'id': 'sn-1', 'komut': 'sinif', 'cihaz': 'abc123', 'yeni': '10-B', 'kim': 'İdare'}); print('komut sonrası:', w.board_info().get('sinif'), w.board_info().get('sinif_gecmis'))
    w.run_command({'id': 'sn-2', 'komut': 'sinif', 'cihaz': 'abc123', 'yeni': '13-Z'}); print('geçersiz sonrası:', w.board_info().get('sinif'))
    E.append(tk.PanelSettings(w)); E[-1].show(); app.processEvents()
def a6(): cek('ayarlar'); E[-1].reject(); w.ask_class(True); app.processEvents()
def a7(): cek('ayarlar-toast')
def a8():
    pass
    from PyQt5.QtGui import QImage, QFont
    A = ['Deniz Yıldız','Ece Kara','Mert Aksoy','Zeynep Demir','Ali Çınar','Elif Su Aydın','Kerem Polat','Nil Öztürk','Can Arslan','Defne Koç','Muhammed Ali Yalçınkaya','Ada Güneş']
    ogr = [dict(no=str(700+i), ad=a) for i, a in enumerate(A)]
    a = dict(id='t1', ad='Deneme anketi', sorular=[dict(tur='secim', metin='Soru', secenekler=['Evet','Hayır'])], siniflar={'9-A': ogr})
    ans = dict(cevaplar={o['no']: dict(zaman=1, c=['Evet']) for o in ogr[::2]})
    im = QImage(1600, 900, QImage.Format_RGB32); im.fill(QColor('#0f1c2e')); p = QPainter(im); p.setRenderHint(QPainter.Antialiasing)
    fams = tk.ui_fonts(); fam = fams.get('Poppins-Medium') or 'Sans'; famb = fams.get('Poppins-Bold') or fam
    def font(px, bold=False): f = QFont(famb if bold else fam); f.setPixelSize(max(10, int(px))); return f
    try: tk.draw_anket_list(p, 1600, 900, 1.0, font, a, '9-A', ans, 900)
    except Exception as e: print('anket çizim HATA', e)
    p.end(); im.save('/tmp/onizleme/u-anket-tik.png'); app.quit()

for t, f in ((1500, a1), (3500, a2), (5000, a3), (6500, a4), (8000, a5), (9500, a6), (10500, a7), (11500, a8)): QTimer.singleShot(t, f)
app.exec_()
