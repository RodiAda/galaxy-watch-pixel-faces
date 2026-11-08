import sys, re
root = sys.argv[1]
p = root + '/assets/widgets/complication.defs'
s = open(p).read()
start = s.index("<symbol id='ComplicationLinear'")
end = s.index('</symbol>', start)
sym = s[start:end]
for a in ("  <transform id='title-expression' attributeName='ComplicationLinear.title'/>\n",
          "  <transform id='text-expression' attributeName='ComplicationLinear.text'/>\n"):
    assert a in sym
    sym = sym.replace(a, '')
sym, n1 = re.subn(r"(<text id='title'>\n)(\s*)",
                  lambda m: m.group(1) + m.group(2) + "<transform id='title-expression' attributeName='text-buffer'/>\n" + m.group(2), sym)
sym, n2 = re.subn(r"(<text id='comp-text' class='foreground-color'>\n)(\s*)",
                  lambda m: m.group(1) + m.group(2) + "<transform id='text-expression' attributeName='text-buffer'/>\n" + m.group(2), sym)
assert n1 >= 1 and n2 >= 1, (n1, n2)
open(p, 'w').write(s[:start] + sym + s[end:])
print('linear expressions', n1, n2)
