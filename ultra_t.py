import sys, os, subprocess, datetime, json
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
tk.KELEBEK_URLS = (); tk.KELEBEK_FOTO_URLS = ()
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
# K-544 sınaması: sahte (uydurma) ders programı — gerçek öğretmen adı yok
D = ['Matematik', 'Matematik', 'Türk Dili ve Edebiyatı', 'Fizik', 'İngilizce', 'İngilizce', 'Biyoloji', 'Tarih']
H = ['Deneme Öğretmen BİR', 'Deneme Öğretmen BİR', 'Örnek Hoca İKİ', 'Test Öğretmen ÜÇ', 'Deneme DÖRT', 'Deneme DÖRT', 'Örnek BEŞ', 'Test ALTI']
prog = {'9-A': {'%d-%d' % (g, n + 1): dict(ders=D[(n + g*3) % 8], ogretmen=[H[(n + g*3) % 8]]) for g in range(5) for n in range(8)}}
open('/tmp/dp.json', 'w').write(json.dumps(dict(siniflar=prog), ensure_ascii=False))
tk.LESSON_FILE = '/tmp/dp.json'; tk._LESSON_TABLE.clear()
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
w = tk.Window(); w.showFullScreen(); app.processEvents()
SAAT = datetime.datetime(2026, 11, 16, 10, 24)
w.exam_clock = lambda: SAAT; w.exams = []; w.upcoming_plans = lambda *a, **k: []
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
def a5(): cek('program-cuma'); app.quit()
for t, f in ((1500, a1), (3500, a2), (5000, a3), (6500, a4), (8000, a5)): QTimer.singleShot(t, f)
app.exec_()
