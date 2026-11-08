import sys, os
root = sys.argv[1]
d = root + '/smali_classes2/rwfcompat'; os.makedirs(d, exist_ok=True)
open(d + '/SafeTap.smali', 'w').write('''.class public final Lrwfcompat/SafeTap;
.super Ljava/lang/Object;

.field public static processed:Ljava/lang/Object;

.method public static hit(Ldib;Landroid/graphics/Rect;II)Z
    .locals 4
    :try_start_0
    iget-object v0, p0, Ldib;->q:Ldlq;
    iget-object v0, v0, Ldlq;->a:Ljava/util/Map;
    iget-object v1, p0, Ldib;->E:Lizg;
    invoke-interface {v1}, Lizg;->getValue()Ljava/lang/Object;
    move-result-object v1
    check-cast v1, Ldlv;
    iget-object v1, v1, Ldlv;->a:Ldmk;
    invoke-interface {v0, v1}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;
    move-result-object v0
    check-cast v0, Landroid/graphics/RectF;
    if-eqz v0, :cond_0
    iget v1, p1, Landroid/graphics/Rect;->left:I
    sub-int v1, p2, v1
    int-to-float v1, v1
    invoke-virtual {p1}, Landroid/graphics/Rect;->width()I
    move-result v2
    int-to-float v2, v2
    div-float/2addr v1, v2
    iget v2, p1, Landroid/graphics/Rect;->top:I
    sub-int v2, p3, v2
    int-to-float v2, v2
    invoke-virtual {p1}, Landroid/graphics/Rect;->height()I
    move-result v3
    int-to-float v3, v3
    div-float/2addr v2, v3
    invoke-virtual {v0, v1, v2}, Landroid/graphics/RectF;->contains(FF)Z
    move-result v0
    return v0
    :try_end_0
    .catch Ljava/lang/Throwable; {:try_start_0 .. :try_end_0} :catch_0
    :catch_0
    :cond_0
    const/4 v0, 0x0
    return v0
.end method
''')
p = root + '/smali_classes2/hbo.smali'
s = open(p).read()
sig = '.method public final a(Ldib;Landroid/graphics/Rect;IIZ)Z'
assert s.count(sig) == 1 and 'hitTest(complicationSlot:' in s
s = s.replace(sig, '.method public final rwfOrigA(Ldib;Landroid/graphics/Rect;IIZ)Z')
anchor = '''    invoke-virtual {v0}, Landroid/view/MotionEvent;->recycle()V'''
i = s.index('rwfOrigA'); j = s.index(anchor, i)
assert s.rfind(':cond_1', i, j) > 0
s = s[:j] + '    sput-object v1, Lrwfcompat/SafeTap;->processed:Ljava/lang/Object;\n' + s[j:]
s += '''
.method public final a(Ldib;Landroid/graphics/Rect;IIZ)Z
    .locals 2
    invoke-virtual/range {p0 .. p5}, Lhbo;->rwfOrigA(Ldib;Landroid/graphics/Rect;IIZ)Z
    move-result v0
    if-nez v0, :cond_0
    sget-object v1, Lrwfcompat/SafeTap;->processed:Ljava/lang/Object;
    sget-object p5, Ljava/lang/Boolean;->TRUE:Ljava/lang/Boolean;
    if-eq v1, p5, :cond_0
    iget-object v1, p0, Lhbo;->a:Lhbp;
    iget-object v1, v1, Lhbp;->p:Ljava/lang/Integer;
    if-nez v1, :cond_0
    invoke-static {p1, p2, p3, p4}, Lrwfcompat/SafeTap;->hit(Ldib;Landroid/graphics/Rect;II)Z
    move-result v0
    :cond_0
    return v0
.end method
'''
open(p, 'w').write(s)
print('patched hbo')
