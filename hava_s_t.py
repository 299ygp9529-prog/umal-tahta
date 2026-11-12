import sys, subprocess, os, datetime, time
sys.path.insert(0, '/usr/share/tahta-kalem')
import tahta_kalem as tk
tk.KELEBEK_URLS = (); tk.KELEBEK_FOTO_URLS = ()
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
app = QApplication(sys.argv); app.setQuitOnLastWindowClosed(False)
w = tk.Window(); w.showFullScreen(); app.processEvents(); w.board_info = lambda: {'sinif': '9-A'}
d_ = os.path.join(w.data_dir, 'hava.json')
def a1():
    for nm in ('welcome', 'intro'):
        x = getattr(w, nm, None)
        if x is not None: x.hide()
    t0 = time.perf_counter(); w.hava_indir(d_, datetime.date.today().isoformat()); print('indirme %.0f ms' % ((time.perf_counter()-t0)*1000), 'kaynak', (w._hava or {}).get('kaynak'), 'saat', len((w._hava or {}).get('saatler', [])))
    sa = (w._hava or {}).get('saatler')
    if sa: print('bugün çıkış özeti', tk.hava_ozet([tuple(s) for s in sa], 15))
    tk.HAVA_URLS = (tk.HAVA_URLS[1],); w.hava_indir(d_ + '2', datetime.date.today().isoformat()); print('met.no:', (w._hava or {}).get('kaynak'), len((w._hava or {}).get('saatler', [])))
    w.hava_denetle(); print('denetle hatasız')
    oz = dict(sicaklik=14, his=13, durum='Parçalı bulutlu', ikon='parcali', yagis=10, ruzgar=15, kotu=False, uyari='')
    w.hava_kart = tk.HavaKart(w, oz); w.hava_kart.show(); w.hava_kart.raise_(); app.processEvents()
def a2():
    subprocess.run(['env','DISPLAY=:7','import', '-window', 'root', '/tmp/onizleme/hava-sakin.png'])
    t0 = time.perf_counter(); w.hava_kart.update(); app.processEvents(); print('yeniden boyama %.1f ms' % ((time.perf_counter() - t0)*1000)); w.hava_kart.kapat(); app.processEvents()
    oz = dict(sicaklik=9, his=6, durum='Yağmurlu', ikon='yagmur', yagis=85, ruzgar=22, kotu=True, uyari='Akşama yağmur bekleniyor, şemsiyenizi unutmayın')
    w.hava_kart = tk.HavaKart(w, oz); w.hava_kart.show(); w.hava_kart.raise_(); app.processEvents()
def a3():
    subprocess.run(['env','DISPLAY=:7','import', '-window', 'root', '/tmp/onizleme/hava-yagmur.png'])
    from PyQt5.QtTest import QTest
    QTest.mouseClick(w.hava_kart, 1); app.processEvents()
    try: v = w.hava_kart.isVisible()
    except RuntimeError: v = False
    print('dokununca kapandı:', not v)
    for ik, du, u in (('kar', 'Kar yağışlı', 'Kar yağışı var, sıkı giyinin, dikkatli yürüyün'), ('firtina', 'Gök gürültülü sağanak', 'Gök gürültülü sağanak var, dikkatli olun'), ('gunes', 'Açık', ''), ('sis', 'Sisli', ''), ('bulut', 'Kapalı', '')):
        k_ = tk.HavaKart(w, dict(sicaklik=2 if ik == 'kar' else 18, his=-1, durum=du, ikon=ik, yagis=90, ruzgar=30, kotu=bool(u), uyari=u)); k_.ciz(k_.width(), k_.height()).save('/tmp/onizleme/hk-%s.png' % ik); k_.close()
    app.quit()
for t, f in ((1500, a1), (6000, a2), (9000, a3)): QTimer.singleShot(t, f)
app.exec_()
