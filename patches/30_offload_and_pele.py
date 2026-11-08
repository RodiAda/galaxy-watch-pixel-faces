import sys, re
root = sys.argv[1]
p = root + '/smali_classes2/gwl.smali'
s = open(p).read()
ctor = '''.method public constructor <init>(Landroid/content/Context;)V
    .locals 2
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    iput-object p1, p0, Lgwl;->c:Landroid/content/Context;
    new-instance v1, Lgwi;
    invoke-direct {v1}, Lgwi;-><init>()V
    iput-object v1, p0, Lgwl;->b:Lgwi;
    new-instance v1, Ljava/util/ArrayList;
    invoke-direct {v1}, Ljava/util/ArrayList;-><init>()V
    iput-object v1, p0, Lgwl;->d:Ljava/util/List;
    :try_start_0
    const-class v0, Lcom/google/wear/displayoffload/DisplayOffloadManager;
    invoke-static {p1, v0}, Lcom/google/wear/Sdk;->getWearManager(Landroid/content/Context;Ljava/lang/Class;)Ljava/lang/Object;
    move-result-object v0
    check-cast v0, Lcom/google/wear/displayoffload/DisplayOffloadManager;
    iput-object v0, p0, Lgwl;->a:Lcom/google/wear/displayoffload/DisplayOffloadManager;
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0
    :catch_0
    return-void
.end method'''
s, n1 = re.subn(r'\.method public constructor <init>\(Landroid/content/Context;\)V.*?\.end method', ctor, s, count=1, flags=re.S)
guard_a = '''    iget-object v1, p0, Lgwl;->a:Lcom/google/wear/displayoffload/DisplayOffloadManager;
    if-nez v1, :gwl_has_dom
    const/4 v1, 0x0
    invoke-static {v1}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;
    move-result-object v1
    new-instance v0, Lils;
    invoke-direct {v0, v1, v1}, Lils;-><init>(Ljava/lang/Object;Ljava/lang/Object;)V
    return-object v0
    :gwl_has_dom
'''
s, n2 = re.subn(r'(\.method public final a\(\)Lils;\n\s*\.locals \d+\n)', lambda m: m.group(1) + guard_a, s, count=1)
guard_b = '''    iget-object v1, p0, Lgwl;->a:Lcom/google/wear/displayoffload/DisplayOffloadManager;
    if-nez v1, :gwl_has_dom_b
    return-void
    :gwl_has_dom_b
'''
s, n3 = re.subn(r'(\.method public final b\(Lipq;\)V\n\s*\.locals \d+\n)', lambda m: m.group(1) + guard_b, s, count=1)
open(p, 'w').write(s)

f = root + '/smali_classes2/fbk.smali'
t = open(f).read()
t, n4 = re.subn(r'(\.method public static final az\(Landroid/content/Context;\)Z\n\s*\.locals \d+\n)', lambda m: m.group(1) + '    const/4 v0, 0x1\n    return v0\n', t, count=1)
open(f, 'w').write(t)
print(n1, n2, n3, n4)
