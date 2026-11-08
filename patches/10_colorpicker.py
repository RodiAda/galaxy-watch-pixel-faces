import sys, re, glob, os, shutil
orig, out = sys.argv[1], sys.argv[2]
for f in glob.glob(orig + '/res/xml*/watch_face_*.xml'):
    shutil.copy(f, out + f[len(orig):])

def attrs(tag):
    return dict(re.findall(r'(app:\w+|android:\w+)="([^"]*)"', tag))

def setting_from_file(name):
    s = open(f'{orig}/res/xml/{name}.xml').read()
    m = re.search(r'<ColorUserStyleSetting\b(.*?)>(.*)</ColorUserStyleSetting>', s, re.S)
    return attrs(m.group(1)), m.group(2)

colors = set()
def build(a, body, indent):
    opts = []
    for o in re.findall(r'<ColorOption\b[^>]*/>', body):
        oa = attrs(o)
        c = oa['app:colors'].lstrip('#').upper()
        colors.add(c)
        opts.append(f'{indent}    <ListOption android:icon="@drawable/rwf_swatch_{c.lower()}" app:displayName="{oa["app:displayName"]}" app:id="{oa["app:id"]}" />')
    keys = ['app:affectedWatchFaceLayers', 'app:defaultOptionIndex', 'app:description', 'app:displayName', 'app:id']
    head = ' '.join(f'{k}="{a[k]}"' for k in keys if k in a)
    return f'{indent}<ListUserStyleSetting {head}>\n' + '\n'.join(opts) + f'\n{indent}</ListUserStyleSetting>\n'

n = 0
for f in glob.glob(out + '/res/xml*/watch_face_*.xml'):
    s = open(f).read()
    def rep_self(m):
        indent, tag = m.group(1), m.group(2)
        a = attrs(tag)
        pa, body = setting_from_file(a.pop('app:parent').split('/')[-1])
        pa.update(a)
        return build(pa, body, indent)
    def rep_inline(m):
        return build(attrs(m.group(2)), m.group(3), m.group(1))
    t = re.sub(r'([ \t]*)<ColorUserStyleSetting\b([^>]*app:parent[^>]*)/>\n', rep_self, s)
    t = re.sub(r'([ \t]*)<ColorUserStyleSetting\b([^>]*[^/])>(.*?)</ColorUserStyleSetting>\n', rep_inline, t, flags=re.S)
    if t != s:
        open(f, 'w').write(t); n += 1
os.makedirs(out + '/res/drawable', exist_ok=True)
for c in colors:
    open(f'{out}/res/drawable/rwf_swatch_{c.lower()}.xml', 'w').write(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="oval">\n'
        f'    <solid android:color="#FF{c}" />\n    <size android:width="48dp" android:height="48dp" />\n</shape>\n')
print('files', n, 'swatches', len(colors))
