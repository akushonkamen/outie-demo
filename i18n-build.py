#!/usr/bin/env python3
"""合并 4 语翻译 JSON → 注入 outie-live.html（window.__OUTIE_I18N__ / PATTERNS__）"""
import json, re, sys

FILES = {'en': '/tmp/i18n-en.json', 'fr': '/tmp/i18n-fr.json', 'ja': '/tmp/i18n-ja.json', 'de': '/tmp/i18n-de.json'}
HTML = '/Users/yp1017/projects/Outie/outie-live.html'
PLACEHOLDER = re.compile(r'\$\{\w+\}')

def to_regex(zh):
    out = ''
    groups = 0
    i = 0
    for m in PLACEHOLDER.finditer(zh):
        out += re.escape(zh[i:m.start()])
        groups += 1
        out += '([^<>「」：·。，]+)'
        i = m.end()
    out += re.escape(zh[i:])
    return out, groups

def to_repl(tr):
    out = ''
    n = 0
    i = 0
    for m in PLACEHOLDER.finditer(tr):
        out += tr[i:m.start()].replace('\\', '\\\\') + '$' + str(n + 1)
        n += 1
        i = m.end()
    out += tr[i:].replace('\\', '\\\\')
    return out

data_html = {}
patterns_html = {}
total_s = total_d = 0
for lang, path in FILES.items():
    try:
        d = json.load(open(path))
    except Exception as e:
        print(f'[warn] {lang}: {e}, skipped')
        continue
    static = d.get('static', {})
    dyn = d.get('dynamic', {})
    pats = []
    for zh, tr in dyn.items():
        rx, groups = to_regex(zh)
        repl = to_repl(tr)
        if PLACEHOLDER.sub('', tr).count('$') and '$' + str(groups + 1) in repl:
            continue
        pats.append([rx, repl])
    data_html[lang] = {'static': static}
    patterns_html[lang] = pats
    total_s += len(static)
    total_d += len(pats)

payload = 'window.__OUTIE_I18N__=' + json.dumps(data_html, ensure_ascii=False, separators=(',', ':')) + ';\n'
payload += 'window.__OUTIE_I18N_PATTERNS__=' + json.dumps(patterns_html, ensure_ascii=False, separators=(',', ':')) + ';'

html = open(HTML).read()
marker_start = '<!-- I18N-DATA-START -->'
marker_end = '<!-- I18N-DATA-END -->'
block = marker_start + '\n<script>' + payload + '</script>\n' + marker_end
if marker_start in html:
    html = re.sub(re.escape(marker_start) + r'[\s\S]*?' + re.escape(marker_end), block, html, count=1)
else:
    html = html.replace('</head>', block + '\n</head>', 1)
open(HTML, 'w').write(html)
print(f'injected: static={total_s} patterns={total_d}')
