import sys, os, re
root = sys.argv[1]
d = root + '/smali_classes2/rwfcompat'; os.makedirs(d, exist_ok=True)
open(d + '/SafePele.smali', 'w').write('''.class public final Lrwfcompat/SafePele;
.super Ljava/lang/Object;

.method public static setAttribute(Lcom/google/android/clockwork/pele/Element;Ljava/lang/String;Ljava/lang/String;)V
    .locals 0
    :try_start_0
    invoke-virtual {p0, p1, p2}, Lcom/google/android/clockwork/pele/Element;->setAttribute(Ljava/lang/String;Ljava/lang/String;)V
    :try_end_0
    .catch Ljava/lang/IllegalArgumentException; {:try_start_0 .. :try_end_0} :catch_0
    :catch_0
    return-void
.end method

.method public static sendCustomEventToAll(Lcom/google/android/clockwork/pele/View;Ljava/lang/String;Z)V
    .locals 0
    :try_start_0
    invoke-virtual {p0, p1, p2}, Lcom/google/android/clockwork/pele/View;->sendCustomEventToAll(Ljava/lang/String;Z)V
    :try_end_0
    .catch Ljava/lang/IllegalArgumentException; {:try_start_0 .. :try_end_0} :catch_0
    :catch_0
    return-void
.end method
''')
subs = [
    (r'invoke-virtual (\{[^}]*\}), Lcom/google/android/clockwork/pele/Element;->setAttribute\(Ljava/lang/String;Ljava/lang/String;\)V',
     r'invoke-static \1, Lrwfcompat/SafePele;->setAttribute(Lcom/google/android/clockwork/pele/Element;Ljava/lang/String;Ljava/lang/String;)V'),
    (r'invoke-virtual (\{[^}]*\}), Lcom/google/android/clockwork/pele/View;->sendCustomEventToAll\(Ljava/lang/String;Z\)V',
     r'invoke-static \1, Lrwfcompat/SafePele;->sendCustomEventToAll(Lcom/google/android/clockwork/pele/View;Ljava/lang/String;Z)V'),
]
n = 0
for dd, _, fs in os.walk(root):
    if '/smali' not in dd or 'rwfcompat' in dd: continue
    for fn in fs:
        if not fn.endswith('.smali'): continue
        p = os.path.join(dd, fn); s = open(p).read(); t = s
        for a, b in subs:
            t, k = re.subn(a, b, t); n += k
        if t != s: open(p, 'w').write(t)
print('replaced', n)
