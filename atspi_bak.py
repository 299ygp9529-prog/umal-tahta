import sys, pyatspi
d = pyatspi.Registry.getDesktop(0)
ad = [d.getChildAtIndex(i).name for i in range(d.childCount)]
print('ATSPI', sys.argv[1], 'uygulamalar:', ad, 'ATLAS_GORUNUYOR' if any(a and ('python' in a.lower() or 'klavye' in a.lower() or 'umal' in a.lower() or 'tahta' in a.lower()) for a in ad) else 'ATLAS_GORUNMUYOR')
