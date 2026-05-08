#!/usr/bin/env python3
"""V2.10: 删除冗余流程图 + 详情页改造 + 更新版本记录"""
from pathlib import Path
import re

PRD = Path('/Users/qiaoqian/clawd-on-desk/FoneSquare-PRD-v2.html')
text = PRD.read_text(encoding='utf-8')

changes = []

# ========== 1) 删除「页面结构关系」整块 (h4 + svg pre) ==========
m1 = re.search(r'  <h4>页面结构关系</h4>\n  <pre class="mermaid"[^<]*<svg[^>]*>.*?</svg></pre>\n?', text, re.DOTALL)
if m1:
    text = text[:m1.start()] + text[m1.end():]
    changes.append('删除「页面结构关系」Mermaid 图')

# ========== 2) 删除「管理员操作流程」(h4 + svg pre) ==========
m2 = re.search(r'  <h4>管理员操作流程</h4>\n  <pre class="mermaid"[^<]*<svg[^>]*>.*?</svg></pre>\n?', text, re.DOTALL)
if m2:
    text = text[:m2.start()] + text[m2.end():]
    changes.append('删除「管理员操作流程」Mermaid 图')

# ========== 3) 删除「销售操作流程」(h4 + p + svg pre) ==========
m3 = re.search(r'  <h4>销售操作流程</h4>\n  <p>[^<]*</p>\n  <pre class="mermaid"[^<]*<svg[^>]*>.*?</svg></pre>\n?', text, re.DOTALL)
if m3:
    text = text[:m3.start()] + text[m3.end():]
    changes.append('删除「销售操作流程」Mermaid 图')

# ========== 4) 删除「添加商家业务流程」(h4 + svg pre) ==========
m4 = re.search(r'  <h4>添加商家业务流程</h4>\n  <pre class="mermaid"[^<]*<svg[^>]*>.*?</svg></pre>\n?', text, re.DOTALL)
if m4:
    text = text[:m4.start()] + text[m4.end():]
    changes.append('删除「添加商家业务流程」Mermaid 图')

# ========== 5) 删除「限额配置」sequence 图 (line ~3344) ==========
m5 = re.search(r'\n  <pre class="mermaid" data-processed="true"><svg id="mermaid-1777436219777"[^>]*>.*?</svg></pre>\n', text, re.DOTALL)
if m5:
    text = text[:m5.start()] + '\n' + text[m5.end():]
    changes.append('删除限额配置 sequence 图')

# ========== 6) 详情页：去掉头部「编辑信息」按钮（JS 模板） ==========
old_edit_btn = (
    "    +       '<div style=\"display:flex;gap:6px;\">'\n"
    "    +         '<button class=\"wf-btn wf-btn-primary\" data-i18n=\"d-edit\">✏️ 编辑信息</button>'\n"
    "    +         '<button class=\"wf-btn\" data-i18n=\"d-disable\">⏸️ 停用</button>'\n"
    "    +       '</div>'"
)
new_edit_btn = (
    "    +       '<div style=\"display:flex;gap:6px;\">'\n"
    "    +         '<button class=\"wf-btn\" data-i18n=\"d-disable\">⏸️ 停用</button>'\n"
    "    +       '</div>'"
)
if old_edit_btn in text:
    text = text.replace(old_edit_btn, new_edit_btn)
    changes.append('详情页 JS 模板：去掉「编辑信息」按钮')

# ========== 7) 详情页：去掉头部「编辑信息」按钮（静态 HTML prototype） ==========
old_static_edit = '<button class="wf-btn wf-btn-primary" data-i18n="d-edit">✏️ 编辑信息</button>'
text = text.replace(old_static_edit, '')
changes.append('详情页静态 HTML：去掉「编辑信息」按钮')

# ========== 8) 详情页头部卡片示意 → 去掉编辑按钮 ==========
old_head_card_edit = '<div style="background:#1677ff;color:#fff;padding:5px 14px;border-radius:6px;font-size:12px;">✏️ 编辑</div>'
text = text.replace(old_head_card_edit, '')
changes.append('头部卡片示意：去掉「编辑」按钮')

# ========== 9) 替换「详情页结构与 Tab 设计」表格 ==========
NEW_TAB_TABLE = """  <!-- ===== 一、详情页结构与 Tab 设计 ===== -->
  <h3>一、详情页结构与 Tab 设计</h3>
  <p>详情页采用<strong>「头部信息卡 + 5 个 Tab」</strong>结构。头部展示商家关键标识（名称、ID、类型、状态、维护人、注册日期）；Tab 内容按业务域分组（基本信息 / KYC 认证材料 / 限额与保证金 / 维护人绑定 / 操作日志）。</p>

  <table style="position: relative;">
    <thead><tr><th style="width:120px;">区域</th><th>展示内容</th><th style="width:160px;">权限说明</th></tr></thead>
    <tbody>
      <tr><td><strong>头部信息卡</strong></td><td style="position: relative;">商家名称、ID、类型 Tag（买家/卖家）、状态 Tag（使用/停用）、认证状态 Tag（未认证/已认证/账号受限）维护人、注册日期；</td><td style="position: relative;">所有可见角色均展示</td></tr>
      <tr><td><strong>头部右侧操作</strong></td><td style="position: relative;">停用 / 启用</td><td style="position: relative;">需对应功能权限点</td></tr>
      <tr><td><strong>Tab 1 — 基本信息</strong></td><td style="position: relative;">个人信息（姓名、手机号、邮箱、WhatsApp、地区、备注）— 选填</td><td style="position: relative;">查看通用；编辑需「编辑商家信息」功能权限</td></tr>
      <tr><td><strong>Tab 2 — KYC 认证材料</strong></td><td style="position: relative;">证件类型 / 号码 / 姓名（脱敏）/ 有效期 / 证件照片（正面 / 背面 / 护照只一面）+ 选填内容：企业名称、证照类型、证照编号、法定代表/董事、企业地址、证照有效期、证照照片</td><td style="position: relative;">查看通用；证件号默认脱敏，原值需特定权限点击查看</td></tr>
      <tr><td><strong>Tab 3 — 限额与保证金</strong>（仅买家）</td><td style="position: relative;">香港店每日下单限额（店铺币种）输入框 + 保证金金额（店铺币种）输入框 + 保证金转账凭证图片上传；展示状态 / 确认时间 / 确认人</td><td style="position: relative;">查看通用；编辑需「配置限额 / 保证金」功能权限点（沿用既有权限）</td></tr>
      <tr><td><strong>Tab 4 — 维护人绑定</strong></td><td style="position: relative;">当前绑定维护人（姓名、OB 账号、绑定时间、操作人）+ 绑定/解绑/更换 操作 + 历史绑定列表</td><td style="position: relative;">查看通用；写操作需「分配 / 更换 / 解绑销售」功能权限</td></tr>
      <tr><td><strong>Tab 5 — 操作日志</strong></td><td style="position: relative;">时间线展示创建、KYC 审核、限额修改、销售绑定变更、停用/启用 等所有操作；含操作人、操作时间、变更前后值</td><td style="position: relative;">数据权限按角色裁剪（销售仅看自己范围）</td></tr>
    </tbody>
  </table>"""

old_tab_section = re.search(
    r'  <!-- ===== 一、详情页结构与 Tab 设计 ===== -->\n  <h3>一、详情页结构与 Tab 设计</h3>.*?</table>',
    text, re.DOTALL
)
if old_tab_section:
    text = text[:old_tab_section.start()] + NEW_TAB_TABLE + text[old_tab_section.end():]
    changes.append('替换「详情页结构与 Tab 设计」表格（去掉编辑信息、基本信息不含企业信息）')

# ========== 10) 删除头部卡片示意 ==========
m_head_card = re.search(
    r'\n  <h4>头部卡片示意</h4>\n  <div style="margin:12px 0;border:1px solid.*?</div>\n  </div>\n',
    text, re.DOTALL
)
if m_head_card:
    text = text[:m_head_card.start()] + '\n' + text[m_head_card.end():]
    changes.append('删除头部卡片示意静态 mockup')

# ========== 11) JS 模板 panelBasic：去掉企业信息卡片 ==========
old_basic_corp = (
    "      + '<div class=\"wf-card\">'\n"
    "      +   '<div class=\"wf-card-head\">'\n"
    "      +     '<span><span data-i18n=\"p-basic-corp\">企业信息</span> <span class=\"wf-card-optional\" data-i18n=\"optional\">选填</span></span>'\n"
    "      +     '<button class=\"wf-btn-link wf-card-edit\" data-act=\"editBasicCorp\" data-i18n=\"edit\">编辑</button>'\n"
    "      +   '</div>'\n"
    "      +   '<div class=\"wf-card-body\">'\n"
    "      +     descRow('b-corp-name','企业名称','—')\n"
    "      +     descRow('b-corp-license','营业执照号','—')\n"
    "      +   '</div>'\n"
    "      + '</div>'"
)
if old_basic_corp in text:
    text = text.replace(old_basic_corp, '')
    changes.append('JS panelBasic：去掉企业信息卡片')

# ========== 12) 更新详情页字段清单 ==========
NEW_FIELD_LIST = """  <!-- ===== 五、详情页字段清单 ===== -->
  <h3>五、详情页字段清单</h3>
  <table style="position: relative;">
    <thead><tr><th>分组</th><th>字段</th><th>必填</th><th>说明</th></tr></thead>
    <tbody>
      <tr><td rowspan="6">基本信息（个人）</td><td>姓名</td><td><span class="tag tag-p0">必填</span></td><td style="position: relative;">与证件一致</td></tr>
      <tr><td>手机号</td><td><span class="tag tag-p0">必填</span></td><td style="position: relative;">含区号，格式校验</td></tr>
      <tr><td>邮箱</td><td><span class="tag" style="background:#F3F4F6;color:#6B7280;">选填</span></td><td style="position: relative;">格式校验</td></tr>
      <tr><td>WhatsApp</td><td><span class="tag" style="background:#F3F4F6;color:#6B7280;">选填</span></td><td style="position: relative;">—</td></tr>
      <tr><td>所在地区</td><td><span class="tag tag-p0">必填</span></td><td style="position: relative;">下拉选择</td></tr>
      <tr><td>备注</td><td><span class="tag" style="background:#F3F4F6;color:#6B7280;">选填</span></td><td style="position: relative;">—</td></tr>
      <tr><td rowspan="5">KYC 认证材料（个人）</td><td>证件类型</td><td><span class="tag tag-p0">必填</span></td><td style="position: relative;">HKID / 澳门ID / 身份证 / 护照</td></tr>
      <tr><td>证件号码</td><td><span class="tag tag-p0">必填</span></td><td style="position: relative;">按证件类型格式校验，存储脱敏</td></tr>
      <tr><td>姓名（与证件一致）</td><td><span class="tag tag-p0">必填</span></td><td style="position: relative;">与证件一致</td></tr>
      <tr><td>证件有效期</td><td><span class="tag tag-p0">必填</span></td><td style="position: relative;">不可选过去日期</td></tr>
      <tr><td>证件照片</td><td><span class="tag tag-p0">必填</span></td><td style="position: relative;">正面 + 背面（护照仅一面），JPG/PNG ≤ 5MB</td></tr>
      <tr><td rowspan="7">KYC 认证材料（企业·选填）</td><td>企业名称</td><td><span class="tag" style="background:#F3F4F6;color:#6B7280;">选填</span></td><td style="position: relative;">—</td></tr>
      <tr><td>证照类型</td><td><span class="tag" style="background:#F3F4F6;color:#6B7280;">选填</span></td><td style="position: relative;">商业登记证等</td></tr>
      <tr><td>证照编号</td><td><span class="tag" style="background:#F3F4F6;color:#6B7280;">选填</span></td><td style="position: relative;">—</td></tr>
      <tr><td>法定代表 / 董事</td><td><span class="tag" style="background:#F3F4F6;color:#6B7280;">选填</span></td><td style="position: relative;">—</td></tr>
      <tr><td>企业地址</td><td><span class="tag" style="background:#F3F4F6;color:#6B7280;">选填</span></td><td style="position: relative;">—</td></tr>
      <tr><td>证照有效期</td><td><span class="tag" style="background:#F3F4F6;color:#6B7280;">选填</span></td><td style="position: relative;">—</td></tr>
      <tr><td>证照照片</td><td><span class="tag" style="background:#F3F4F6;color:#6B7280;">选填</span></td><td style="position: relative;">JPG/PNG/PDF ≤ 10MB</td></tr>
      <tr><td rowspan="3">限额 / 保证金<br><span style="color:#8c8c8c;font-size:11px;">（仅买家）</span></td><td>每日下单限额 (HKD)</td><td>—</td><td style="position: relative;">≤ 保证金 × 10</td></tr>
      <tr><td>保证金金额 / 状态 / 凭证</td><td>—</td><td style="position: relative;">线下转账凭证 + 运营确认</td></tr>
      <tr><td>修改记录</td><td>—</td><td style="position: relative;">操作人 / 修改前后值 / 时间</td></tr>
    </tbody>
  </table>"""

old_field_list = re.search(
    r'  <!-- ===== 五、详情页字段清单 ===== -->\n  <h3>五、详情页字段清单</h3>\n  <table.*?</table>',
    text, re.DOTALL
)
if old_field_list:
    text = text[:old_field_list.start()] + NEW_FIELD_LIST + text[old_field_list.end():]
    changes.append('更新详情页字段清单（去掉基本信息里的企业信息，企业信息移到 KYC 下）')

# ========== 13) 版本记录 V2.10 ==========
V29_KEY = '<tr><td>2026-04-29</td><td>V2.9 详情页结构'
V210_ROW = '<tr><td>2026-04-29</td><td>V2.10 详情页改造 + 清理冗余流程图：① 去掉头部「编辑信息」按钮（仅保留停用/启用）；② 基本信息 Tab 去掉企业信息（企业信息归入 KYC Tab 选填区）；③ 更新「详情页结构与 Tab 设计」表格及字段清单；④ 删除 5 块冗余 Mermaid/SVG 流程图（页面结构关系 / 管理员操作 / 销售操作 / 添加商家 / 限额配置序列图）。</td><td style="position: relative;">乔谦</td></tr>\n      '
if V29_KEY in text:
    text = text.replace(V29_KEY, V210_ROW + V29_KEY)
    changes.append('添加版本记录 V2.10')

PRD.write_text(text, encoding='utf-8')

print(f'✅ 完成 {len(changes)} 项修改：')
for i, c in enumerate(changes, 1):
    print(f'  {i}. {c}')
print(f'文件总行数: {text.count(chr(10)) + 1}')
