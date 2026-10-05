#!/bin/bash
# 部署前语法门：页面内所有 <script> 块逐一 node --check
set -e
python3 - <<'PY'
import re
s=open('/Users/yp1017/projects/Outie/outie-live.html').read()
blocks=re.findall(r'<script>(.*?)</script>',s,re.S)
assert blocks, "no script blocks"
for i,b in enumerate(blocks):
    open(f'/tmp/outie-script-check-{i}.js','w').write(b)
print(f"{len(blocks)} blocks")
PY
for f in /tmp/outie-script-check-*.js; do node --check "$f"; done
rm -f /tmp/outie-script-check-*.js
echo "syntax-gate: OK"
