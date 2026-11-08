import sys, re, os
root = sys.argv[1] + '/assets'; files = 0; subs = 0
for d, _, fs in os.walk(root):
    for fn in fs:
        p = os.path.join(d, fn)
        try: s = open(p, encoding='utf-8').read()
        except Exception: continue
        t, n1 = re.subn(r'\btoInteractive\b', 'hipower', s)
        t, n2 = re.subn(r'\btoAmbient\b', 'lopower', t)
        if n1 + n2:
            open(p, 'w', encoding='utf-8').write(t); files += 1; subs += n1 + n2
print('files', files, 'subs', subs)
