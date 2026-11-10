import sys, os, threading, time, traceback, collections, runpy
T0=time.time(); ana=threading.main_thread(); say=collections.Counter(); ornek={}
_ic = [False]
def kanca(ev, args):
    if _ic[0] or threading.current_thread() is not ana or time.time()-T0 < float(os.environ.get('IZ_BAS','25')): return
    if ev in ('open','os.listdir','os.scandir','os.remove','os.rename','os.mkdir','subprocess.Popen','socket.connect','os.system','shutil.copyfile','os.truncate','os.utime'):
        if ev=='open' and args and isinstance(args[0],str) and (args[0].startswith('/proc') or args[0].endswith('.pyc') or '/site-packages/' in args[0] or '/usr/lib/python' in args[0]): return
        _ic[0] = True
        try:
            st=[]; f=sys._getframe(1)
            while f is not None:
                if 'tahta_kalem' in f.f_code.co_filename: st.append(f.f_code.co_name)
                f=f.f_back
            k=(ev,' > '.join(reversed(st[:3]))); say[k]+=1; ornek.setdefault(k,str(args[0])[:80] if args else '')
        finally: _ic[0] = False
sys.addaudithook(kanca)
def bitir():
    time.sleep(float(os.environ.get('IZ_SURE','150')))
    with open(os.environ.get('IZ_CIKTI','/tmp/iz.out'),'w') as f:
        for k,n in say.most_common(): f.write('%5d %s | %s | %s\n'%(n,k[0],k[1],ornek[k]))
    os._exit(0)
threading.Thread(target=bitir,daemon=True).start()
sys.argv=[sys.argv[1]]+sys.argv[2:]
runpy.run_path(sys.argv[0], run_name='__main__')
