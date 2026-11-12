import sys, subprocess, os, datetime, time
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
try: os.remove(os.path.expanduser('~/.local/share/umal-tahta/kelebek-duyuru.json'))
except OSError: pass
w = tk.Window(); w.showFullScreen(); app.processEvents()
yarin = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
def a1():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    w.last_touch = 0
    w.kelebek_new = dict(planlar=[dict(tarih=yarin, ders='7. Ders', sinav='İNGİLİZCE', salonlar={}, siniflar={})]); t0 = time.perf_counter(); w.take_kelebek(); print('sınıf', w.board_info().get('sinif'))
def a2():
    st = tk.exam_now(w.exam_clock(), getattr(w, 'exams', None)); print('durum', st and st.get('phase'), 'meşgul', tk.kalem_mesgul(w), 'sınavda', getattr(w, '_sinav_su_an', None), 'grade', tk.class_grade(w.board_info().get('sinif')))
    w.kelebek_duyuru_denetle(); app.processEvents()
    d = getattr(w, 'kelebek_duyuru', None); print('duyuru açıldı:', d is not None and d.isVisible())
    subprocess.run(['import', '-window', 'root', '/tmp/onizleme/kelebek-duyuru.png'])
    t0 = time.perf_counter(); d.update(); app.processEvents(); print('yeniden boyama %.1f ms' % ((time.perf_counter() - t0)*1000)); d.b_kapat.click(); app.processEvents()
    w.kelebek_new = dict(planlar=[dict(tarih=yarin, ders='7. Ders', sinav='İNGİLİZCE', salonlar={}, siniflar={})]); w.take_kelebek()
def a3():
    d = getattr(w, 'kelebek_duyuru', None)
    try: v = d is not None and d.isVisible()
    except RuntimeError: v = False
    print('aynı plan ikinci kez gösterilmedi:', not v); app.quit()
for t, f in ((1500, a1), (6000, a2), (11000, a3)): QTimer.singleShot(t, f)
app.exec_()
