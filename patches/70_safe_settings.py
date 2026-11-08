import sys, os, re
root = sys.argv[1]
helper_dir = root + '/smali_classes2/rwfcompat'; os.makedirs(helper_dir, exist_ok=True)
kinds = ['Global', 'Secure', 'System']
methods = []
for k in kinds:
    for name, sig, ret, mv, dflt in [
        ('getInt', '(Landroid/content/ContentResolver;Ljava/lang/String;I)I', 'I', 'move-result v0', 'return p2'),
        ('getLong', '(Landroid/content/ContentResolver;Ljava/lang/String;J)J', 'J', 'move-result-wide v0', 'return-wide p2'),
        ('getFloat', '(Landroid/content/ContentResolver;Ljava/lang/String;F)F', 'F', 'move-result v0', 'return p2'),
        ('getString', '(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;', 'Ljava/lang/String;', 'move-result-object v0', 'const/4 v0, 0x0\n    return-object v0'),
    ]:
        args = '{p0, p1, p2}' if name in ('getInt','getFloat') else ('{p0, p1, p2, p3}' if name=='getLong' else '{p0, p1}')
        retop = {'I':'return v0','J':'return-wide v0','F':'return v0','Ljava/lang/String;':'return-object v0'}[ret]
        methods.append(f'''.method public static {k}_{name}{sig}
    .locals 2
    :try_start_0
    invoke-static {args}, Landroid/provider/Settings${k};->{name}{sig}
    {mv}
    :try_end_0
    .catch Ljava/lang/Throwable; {{:try_start_0 .. :try_end_0}} :catch_0
    {retop}
    :catch_0
    {dflt}
.end method
''')
open(helper_dir + '/SafeSettings.smali', 'w').write('.class public final Lrwfcompat/SafeSettings;\n.super Ljava/lang/Object;\n\n' + '\n'.join(methods))
pat = re.compile(r'invoke-static (\{[^}]*\}), Landroid/provider/Settings\$(Global|Secure|System);->(getInt|getLong|getFloat|getString)(\(Landroid/content/ContentResolver;Ljava/lang/String;(?:I|J|F)?\)(?:I|J|F|Ljava/lang/String;))')
valid = {('getInt','(Landroid/content/ContentResolver;Ljava/lang/String;I)I'),('getLong','(Landroid/content/ContentResolver;Ljava/lang/String;J)J'),('getFloat','(Landroid/content/ContentResolver;Ljava/lang/String;F)F'),('getString','(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;')}
n = 0
for d, _, fs in os.walk(root):
    if '/smali' not in d or 'rwfcompat' in d: continue
    for fn in fs:
        if not fn.endswith('.smali'): continue
        p = os.path.join(d, fn); s = open(p).read()
        def rep(m):
            global n
            if (m.group(3), m.group(4)) not in valid: return m.group(0)
            n += 1
            return f'invoke-static {m.group(1)}, Lrwfcompat/SafeSettings;->{m.group(2)}_{m.group(3)}{m.group(4)}'
        t = pat.sub(rep, s)
        if t != s: open(p, 'w').write(t)
print('replaced', n)
