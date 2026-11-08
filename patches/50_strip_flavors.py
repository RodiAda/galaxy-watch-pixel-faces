import sys, re, glob
root = sys.argv[1]; n = 0
for f in glob.glob(root + '/res/xml*/watch_face_*.xml'):
    s = open(f).read()
    t = re.sub(r'[ \t]*<UserStyleFlavors>.*?</UserStyleFlavors>\n', '', s, flags=re.S)
    if t != s: open(f, 'w').write(t); n += 1
m = root + '/AndroidManifest.xml'; s = open(m).read()
s2 = s.replace('android:name="androidx.wear.watchface.FLAVORS_SUPPORTED" android:value="true"', 'android:name="androidx.wear.watchface.FLAVORS_SUPPORTED" android:value="false"')
open(m, 'w').write(s2)
print('xml', n, 'manifest', s.count('FLAVORS_SUPPORTED" android:value="true"'))
