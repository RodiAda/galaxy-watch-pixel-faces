import sys, glob, re
root = sys.argv[1]
def find(name):
    r = glob.glob(f'{root}/smali*/{name}.smali'); assert len(r) == 1, name; return r[0]
gap = r'(?:\s*\.line \d+\n|\s*\n)*'
p = find('iht'); s = open(p).read()
pat = r'(invoke-virtual \{v0\}, Landroid/app/Service;->getApplication\(\)Landroid/app/Application;\n' + gap + r'\s*move-result-object v1\n)'
s, n1 = re.subn(pat, r'''\1    if-nez v1, :rwf_has_app
    invoke-virtual {v0}, Landroid/app/Service;->getApplicationContext()Landroid/content/Context;
    move-result-object v1
    :rwf_has_app
''', s, count=1)
open(p, 'w').write(s)
p = find('dkz'); s = open(p).read()
pat = r'(invoke-virtual \{p0, p1\}, Ldkz;->attachBaseContext\(Landroid/content/Context;\)V\n' + gap + r')(\s*return-void\n\.end method)'
s, n2 = re.subn(pat, r'''\1    :try_start_rwf
    invoke-virtual {p0}, Ldkz;->onCreate()V
    :try_end_rwf
    .catch Ljava/lang/Throwable; {:try_start_rwf .. :try_end_rwf} :catch_rwf
    :catch_rwf
\2''', s, count=1)
open(p, 'w').write(s)
assert n1 == 1 and n2 == 1, (n1, n2)
print('ok')
