#!/usr/bin/env python3
"""
删除 FoneSquare-PRD-v2.html 内 详情页 / 添加页 的旧 wf-shell 原型块。
  - 详情页 (page-web-merchant-detail)  ~4208–4273
  - 添加页 (page-web-merchant-add)     ~4401–4441
都替换成「原型已统一在商家列表页」的提示（不再跳转新窗口）。
脚本基于行号 + 锚点行内容双重校验后再执行删除。
"""
from pathlib import Path
import sys

PRD = Path('/Users/qiaoqian/clawd-on-desk/FoneSquare-PRD-v2.html')
lines = PRD.read_text(encoding='utf-8').splitlines(keepends=True)

# 找 anchors（行号是 1-based）
def find_one(needle, hint=None):
    matches = [i for i, ln in enumerate(lines, 1) if needle in ln]
    if hint is not None:
        matches = [i for i in matches if abs(i - hint) < 80]
    if len(matches) != 1:
        print(f'AMBIGUOUS for {needle!r}: {matches}', file=sys.stderr)
        sys.exit(1)
    return matches[0]

detail_h3 = find_one('<h3>四、可交互原型 — 商家详情</h3>', hint=4209)
add_h3    = find_one('<h3>四、可交互原型 — 添加商家</h3>', hint=4402)

# 详情页旧块边界：从注释行 (h3 上一行) 起，到 page 关闭 </div> 前一空行。
# 通过简单括号匹配在该范围内找 wf-shell 之后的最后一个顶级 </div>
def block_range(h3_line):
    # 注释 `<!-- ===== 四、可交互原型 ===== -->` 在 h3 上一行
    start = h3_line - 1  # comment line index
    # 寻找首个 wf-shell 行
    shell_start = None
    for i in range(start, len(lines)):
        if 'class="wf-shell"' in lines[i] and ('wfDetailV2Page' in lines[i] or 'wfAddV2Page' in lines[i]):
            shell_start = i + 1  # to 1-based
            break
    if shell_start is None:
        print('shell not found near', h3_line); sys.exit(1)
    # 从 shell_start 开始做缩进/标签计数找配对 </div>
    depth = 0
    end = None
    for i in range(shell_start - 1, len(lines)):
        s = lines[i]
        opens = s.count('<div')
        closes = s.count('</div>')
        depth += opens - closes
        if depth == 0 and i + 1 >= shell_start:
            end = i + 1  # 1-based, 这是最后包含的行（即 wf-shell 的关闭 </div>）
            break
    if end is None:
        print('matching </div> not found'); sys.exit(1)
    return start, end  # both 1-based, inclusive

d_start, d_end = block_range(detail_h3)
a_start, a_end = block_range(add_h3)

REPLACEMENT = '''  <!-- ===== 四、可交互原型（原型已统一到列表页） ===== -->
  <div class="info-box info" style="margin:14px 0;">
    <span class="ib-icon">🎮</span>
    <div>本页对应的<strong>可交互原型</strong>已统一收纳到「<strong>商家列表 → 后台统一原型（List ↔ Detail ↔ Add）</strong>」内。点击列表行的「查看」即可在<strong>同一原型容器内</strong>切换到本页视图，完整支持<strong>中/英切换、Tab 切换、销售更换、保证金 × 10 限额校验</strong>等交互；不再跳转新窗口。</div>
  </div>
'''

# 先替换更靠后的（添加页），再替换详情页，避免行号位移
def splice(start, end, replacement):
    # 用 splitlines 后没有换行符，直接拼字符串
    new_block = replacement
    head = ''.join(lines[: start - 1])
    tail = ''.join(lines[end:])
    return head + new_block + tail

text = ''.join(lines)
new = splice(a_start, a_end, REPLACEMENT)
# 重新基于新文本切分，再处理详情页（行号未变，因为 splice 在更后面）
new_lines = new.splitlines(keepends=True)

# 重新查找详情页（使用 anchor，更安全）
d_h3 = next((i for i, ln in enumerate(new_lines, 1) if '<h3>四、可交互原型 — 商家详情</h3>' in ln), None)
if d_h3 is None: print('detail h3 lost'); sys.exit(1)
# 把 lines 重设为 new_lines 后再调用 block_range
lines = new_lines
d_start2, d_end2 = block_range(d_h3)
new2 = splice(d_start2, d_end2, REPLACEMENT)

PRD.write_text(new2, encoding='utf-8')
print('Stripped old prototypes:', f'detail {d_start2}-{d_end2}', f'add {a_start}-{a_end}')
print('New file lines:', new2.count('\n'))
