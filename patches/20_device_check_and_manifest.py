import sys, re
root = sys.argv[1]
p = root + '/smali_classes2/com/google/android/wearable/watchface/application/WatchFaceApplication.smali'
s = open(p).read()
i = s.index('PIXEL_WATCH_EXPERIENCE'); j = s.index('if-eqz v0, :cond_1', i); assert j - i < 400
s = s[:j] + 'const/4 v0, 0x1\n    ' + s[j:]
i = s.index('"com.google.android.wearable.watchface.koru.tubes.TubesWatchFaceService"'); j = s.index('if-eqz v12, :cond_5', i); assert j - i < 400
s = s[:j] + 'const/4 v12, 0x0\n    ' + s[j:]
open(p, 'w').write(s)
m = root + '/AndroidManifest.xml'
t = open(m).read()
def fix(mm):
    x = mm.group(0)
    return x.replace('android:exported="false"', 'android:exported="true"') if 'BIND_WALLPAPER' in x else x
t = re.sub(r'<service [^>]*>', fix, t)
old = '<category android:name="com.google.android.wearable.pixel.watchface.category.PIXEL_WATCH_FACE"/>'
t = t.replace(old, old + '\n                <category android:name="com.google.android.wearable.watchface.category.WATCH_FACE"/>')
open(m, 'w').write(t)
print('ok')
