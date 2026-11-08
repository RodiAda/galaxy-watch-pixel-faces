import sys, re
root = sys.argv[1]
p = root + '/smali/iug.smali'
s = open(p).read()
n = 0
def fix(m):
    global n
    head, locals_ = m.group(1), int(m.group(2))
    a, b = locals_, locals_ + 2
    n += 1
    return (f'{head}.locals {locals_ + 3}\n'
            f'    const-wide/16 v{a}, 0xfa0\n'
            f'    cmp-long v{b}, p0, v{a}\n'
            f'    if-nez v{b}, :rwf_timeout_keep\n'
            f'    const-wide/16 p0, 0x3a98\n'
            f'    :rwf_timeout_keep\n')
s = re.sub(r'(\.method public static final [kl]\(JLipu;Lioa;\)Ljava/lang/Object;\n\s*)\.locals (\d+)\n', fix, s)
open(p, 'w').write(s)
print('patched', n)
