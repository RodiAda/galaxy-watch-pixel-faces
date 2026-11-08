import sys, re
root = sys.argv[1]
p = root + '/smali_classes2/gwy.smali'
s = open(p).read()
lines = []
for fld, src in [('l','Lgxi;'),('m','Lgxh;'),('n','Lgxj;'),('p','Lgxl;'),('q','Lgxm;')]:
    lines.append(f'''    iget-object v0, p0, Lgwy;->{fld}:Ligg;
    if-nez v0, :hl_{fld}
    sget-object v0, {src}->a:Lfva;
    invoke-static {{v0}}, Liie;->a(Liii;)Ligg;
    move-result-object v0
    iput-object v0, p0, Lgwy;->{fld}:Ligg;
    :hl_{fld}
''')
method = '.method public final rwfHeadlessInit()V\n    .locals 1\n' + ''.join(lines) + '    return-void\n.end method\n\n'
assert 'rwfHeadlessInit' not in s
s = s.replace('.method public final I()V', method + '.method public final I()V', 1)
s, n = re.subn(r'(\.method public final I\(\)V\n\s*\.locals )0\n', r'\g<1>1\n    invoke-virtual {p0}, Lgwy;->rwfHeadlessInit()V\n', s, count=1)
open(p, 'w').write(s); print('I patched', n)
