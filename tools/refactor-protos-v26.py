#!/usr/bin/env python3
"""
V2.6 改造：
  1) 列表页内旧的「四、可交互原型 — 后台统一原型」整段删除（含 style + #wfAdmin + script）。
  2) 详情/添加页内「四、可交互原型（已统一到列表页）」info-box 删除。
  3) 在 列表/详情/添加 三页的「页面定位 info-box」紧下方各插入：
        <h3>四、可交互原型 — 商家XXX</h3>
        <p> 描述 </p>
        <div class="wf-prototype-shell" data-prototype="merchant-admin" data-init-view="..."> </div>
  4) 文件末尾（</body> 之前）注入：CSS + JS 模板渲染器（包含侧边菜单 + 4 视图：list / detail / add / myfiles + 中英切换 + 全部交互）。
  5) 版本记录新增 V2.6 行。
"""
from pathlib import Path
import re, sys

PRD = Path('/Users/qiaoqian/clawd-on-desk/FoneSquare-PRD-v2.html')
text = PRD.read_text(encoding='utf-8')

# ---- 1) 删除列表页内的旧统一原型整段 ----
OLD_PROTO_HEAD = '  <!-- ===== 四、可交互原型 — 后台统一原型（List ↔ Detail ↔ Add） ===== -->'
OLD_PROTO_TAIL = '  </script>'  # 该段结尾 </script>
ih = text.find(OLD_PROTO_HEAD)
if ih < 0:
    print('ERROR: 未找到旧统一原型起点'); sys.exit(1)
# 在 OLD_PROTO_HEAD 之后查找最近的 `</script>\n`（注意是该段尾部，不能误抓后面的全局 script）
# 旧段以 `<script>(function(){... })();\n  </script>` 结束，紧接其后是空行 + `<h4>📖 列表页产品说明</h4>`
it = text.find('</script>\n\n  <h4>📖 列表页产品说明', ih)
if it < 0:
    print('ERROR: 未找到旧统一原型终点（依赖 列表页产品说明 锚点）'); sys.exit(1)
it_end = it + len('</script>\n\n')  # 删到 `</script>\n\n` 之后（保留 `<h4>` 起始空行结构）
text = text[:ih] + text[it_end:]
print('removed old prototype block, chars:', it_end - ih)

# ---- 2) 删除详情/添加页内"原型已统一到列表页" info-box ----
DETAIL_OLD = '''  <!-- ===== 四、可交互原型（原型已统一到列表页） ===== -->
  <div class="info-box info" style="margin:14px 0;">
    <span class="ib-icon">🎮</span>
    <div>本页对应的<strong>可交互原型</strong>已统一收纳到「<strong>商家列表 → 后台统一原型（List ↔ Detail ↔ Add）</strong>」内。点击列表行的「查看」即可在<strong>同一原型容器内</strong>切换到本页视图，完整支持<strong>中/英切换、Tab 切换、销售更换、保证金 × 10 限额校验</strong>等交互；不再跳转新窗口。</div>
  </div>

'''
n_old = text.count(DETAIL_OLD)
text = text.replace(DETAIL_OLD, '')
print('removed legacy info-boxes:', n_old)

# ---- 3) 在三页页面定位 info-box 后插入新的交互原型占位 ----
def proto_section(view, title_zh, desc_zh, anchor_id):
    return f'''  <!-- ===== 四、可交互原型 — {title_zh}（含侧边菜单 / 中英切换 / 完整交互） ===== -->
  <h3 id="{anchor_id}">四、可交互原型 — {title_zh}</h3>
  <p style="font-size:13px;color:#595959;margin:-8px 0 12px;">
    {desc_zh}本原型在文档内直接交互，<strong>不再跳转新窗口</strong>；右上角 <strong>中 / EN</strong> 切换语言；左侧菜单仅保留<strong>「商家管理 → 商家列表」</strong>与<strong>「下载中心 → 我的文件」</strong>两组（参考截图设计）；商家详情 / 添加商家 入口在「商家列表」页面顶部按钮和列表行操作中触发。
  </p>
  <div class="wf-prototype-shell" data-prototype="merchant-admin" data-init-view="{view}"></div>

'''

# 列表页注入：在 page-web-merchant-list 内的「页面定位」info-box 后
LIST_ANCHOR = '''  <h3 id="anchor-list">二、商家列表页</h3>
  <div class="info-box info">
    <span class="ib-icon">📋</span>
    <div><strong>页面定位</strong>：登录后默认首页。展示所有商家（管理员视角）或已绑定商家（销售视角）的概览列表，支持搜索、筛选、分页。管理员可从此页进入「添加商家」流程。</div>
  </div>

'''
if LIST_ANCHOR not in text or text.count(LIST_ANCHOR) != 1:
    print('ERROR: list page anchor not unique'); sys.exit(1)
text = text.replace(
    LIST_ANCHOR,
    LIST_ANCHOR + proto_section('list', '商家列表', '面向<strong>登录后默认首页</strong>的列表 + 筛选 + 分页 + 导出 + 「添加商家」入口；点击列表行末「查看」可<strong>在容器内切换至商家详情视图</strong>，点击右上「➕ 添加商家」可切换至添加视图。', 'anchor-list-proto')
)

# 详情页注入：在 page-web-merchant-detail 内的「页面定位」info-box 后
DETAIL_ANCHOR = '''  <div class="info-box info">
    <span class="ib-icon">👤</span>
    <div><strong>页面定位</strong>：从商家列表点击「查看」进入。展示单个商家的完整信息，采用 Tab 页签组织 —— 基本信息、KYC 认证材料、限额与保证金（仅买家展示）、销售绑定、操作日志。<br>
      <strong>权限策略</strong>：销售默认只能看到<em>自己维护的商家</em>详情且<em>只读</em>；管理员看到<em>全量数据</em>，并按 OB 账号被授予的功能权限点（编辑信息 / 配置限额 / 分配销售）打开相应写操作。
    </div>
  </div>

'''
if DETAIL_ANCHOR not in text or text.count(DETAIL_ANCHOR) != 1:
    print('ERROR: detail page anchor not unique'); sys.exit(1)
text = text.replace(
    DETAIL_ANCHOR,
    DETAIL_ANCHOR + proto_section('detail', '商家详情', '面向<strong>从商家列表点击「查看」</strong>后的详情视图：5 个 Tab 全部可点击切换；销售 Tab 可展开「更换销售」表单；限额与保证金 Tab 含限额输入框 / 保证金输入框 / 转账凭证上传 / 实时校验「保证金 × 10 = 限额上限」。', 'anchor-detail-proto')
)

# 添加页注入：在 page-web-merchant-add 内的「页面定位」info-box 后
ADD_ANCHOR = '''  <div class="info-box info">
    <span class="ib-icon">➕</span>
    <div><strong>页面定位</strong>：管理员与销售在后台<strong>单页纵向表单</strong>录入新商家：基本信息 + KYC + 企业信息（选填）顺序排列、同页滚动填写，<em>不使用分步向导</em>。提交后系统自动校验证件唯一性、触发风控制裁名单核查；成功后 Toast / 页面内提示并可跳转详情。<br>
      <strong>归属规则</strong>：销售添加 → 自动绑定到当前销售；管理员添加 → 默认未分配，需在「商家详情 → 销售绑定」中手动分配。
    </div>
  </div>

'''
if ADD_ANCHOR not in text or text.count(ADD_ANCHOR) != 1:
    print('ERROR: add page anchor not unique'); sys.exit(1)
text = text.replace(
    ADD_ANCHOR,
    ADD_ANCHOR + proto_section('add', '添加商家', '面向<strong>单页纵向表单</strong>的添加视图：基本信息 + KYC + 企业信息（选填）顺序滚动填写；销售添加自动绑定本人，管理员添加默认未分配；提交时演示证件唯一性校验与制裁名单核查。', 'anchor-add-proto')
)

# ---- 4) 在 </body> 前注入 CSS + JS 模板渲染器 ----
INJECT = r'''<!-- ===== 通用可交互原型模板（含侧边菜单 / 中英切换 / 4 视图） ===== -->
<style>
.wf-prototype-shell { width:100%; height:clamp(720px, 90vh, 980px); border:1px solid #D1D5DB; border-radius:10px; overflow:hidden; background:#F0F2F5; position:relative; font-size:12px; display:flex; flex-direction:column; margin:16px 0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif; }
.wf-prototype-shell * { box-sizing:border-box; }
.wf-prototype-shell .wf-topbar { height:40px; background:white; border-bottom:1px solid #E5E7EB; display:flex; align-items:center; padding:0 16px; justify-content:space-between; flex-shrink:0; }
.wf-prototype-shell .wf-topbar-left { display:flex; align-items:center; gap:6px; font-size:11px; color:#8C8C8C; }
.wf-prototype-shell .wf-topbar-right { display:flex; align-items:center; gap:10px; font-size:11px; color:#8C8C8C; }
.wf-prototype-shell .wf-topbar-avatar { width:24px; height:24px; border-radius:50%; background:#1677FF; color:white; display:flex; align-items:center; justify-content:center; font-weight:600; }
.wf-prototype-shell .wf-lang { display:inline-flex; border:1px solid #D9D9D9; border-radius:4px; overflow:hidden; user-select:none; height:22px; line-height:22px; }
.wf-prototype-shell .wf-lang-btn { padding:0 8px; font-size:10px; cursor:pointer; color:#595959; background:white; }
.wf-prototype-shell .wf-lang-btn.active { background:#1677FF; color:white; }
.wf-prototype-shell .wf-body { display:flex; flex:1; min-height:0; overflow:hidden; }
.wf-prototype-shell .wf-sider { width:200px; flex-shrink:0; background:#001529; color:rgba(255,255,255,.85); padding:12px 0; overflow-y:auto; }
.wf-prototype-shell .wf-sider-logo { display:flex; align-items:center; gap:8px; padding:6px 16px 14px; font-size:14px; font-weight:600; color:white; border-bottom:1px solid rgba(255,255,255,.06); margin-bottom:10px; }
.wf-prototype-shell .wf-sider-logo .wf-logo-badge { width:26px; height:26px; background:#1677FF; border-radius:5px; display:inline-flex; align-items:center; justify-content:center; color:white; font-size:11px; font-weight:700; }
.wf-prototype-shell .wf-menu-group { padding:10px 16px 4px; font-size:10px; color:rgba(255,255,255,.4); text-transform:uppercase; letter-spacing:1px; }
.wf-prototype-shell .wf-menu-item { padding:9px 16px; font-size:12px; color:rgba(255,255,255,.7); cursor:pointer; display:flex; align-items:center; gap:8px; border-left:3px solid transparent; }
.wf-prototype-shell .wf-menu-item:hover { background:rgba(255,255,255,.05); color:white; }
.wf-prototype-shell .wf-menu-item.active { background:#1677FF; color:white; border-left-color:#fff; font-weight:500; }
.wf-prototype-shell .wf-content { flex:1; overflow:hidden; display:flex; flex-direction:column; min-width:0; background:#F0F2F5; }
.wf-prototype-shell .wf-view { display:none; flex-direction:column; flex:1; min-height:0; overflow-y:auto; }
.wf-prototype-shell .wf-view.active { display:flex; }
.wf-prototype-shell .wf-page { padding:16px 20px; }
.wf-prototype-shell .wf-card { background:white; border:1px solid #F0F0F0; border-radius:6px; margin-bottom:12px; }
.wf-prototype-shell .wf-card-head { padding:10px 16px; border-bottom:1px solid #F0F0F0; font-size:13px; font-weight:600; color:#262626; display:flex; align-items:center; justify-content:space-between; }
.wf-prototype-shell .wf-card-body { padding:12px 16px; }
.wf-prototype-shell .wf-btn { display:inline-flex; align-items:center; gap:4px; height:26px; padding:0 10px; border:1px solid #D9D9D9; background:white; border-radius:4px; font-size:11px; cursor:pointer; color:#262626; }
.wf-prototype-shell .wf-btn:hover { color:#1677FF; border-color:#1677FF; }
.wf-prototype-shell .wf-btn-primary { background:#1677FF; color:white; border-color:#1677FF; }
.wf-prototype-shell .wf-btn-primary:hover { color:white; background:#0958D9; border-color:#0958D9; }
.wf-prototype-shell .wf-btn-link { border:none; background:transparent; padding:0; height:auto; font-size:11px; color:#1677FF; cursor:pointer; }
.wf-prototype-shell .wf-btn-link:hover { color:#0958D9; text-decoration:underline; }
.wf-prototype-shell .wf-input, .wf-prototype-shell .wf-select, .wf-prototype-shell .wf-textarea { border:1px solid #D9D9D9; border-radius:4px; padding:5px 8px; font-size:11px; color:#BFBFBF; background:white; height:28px; line-height:18px; min-width:0; width:100%; display:flex; align-items:center; }
.wf-prototype-shell .wf-input.wf-input-edit { color:#262626; }
.wf-prototype-shell .wf-textarea { height:auto; min-height:50px; align-items:flex-start; }
.wf-prototype-shell .wf-input[contenteditable="true"]:focus, .wf-prototype-shell .wf-select:focus, .wf-prototype-shell .wf-textarea:focus { outline:none; border-color:#1677FF; box-shadow:0 0 0 2px rgba(22,119,255,.15); }
.wf-prototype-shell .wf-select::after { content:'▼'; margin-left:auto; font-size:8px; color:#BFBFBF; }
.wf-prototype-shell .wf-form-row { display:flex; gap:12px; margin-bottom:10px; }
.wf-prototype-shell .wf-form-item { flex:1; display:flex; flex-direction:column; gap:4px; min-width:0; }
.wf-prototype-shell .wf-form-item.w120 { flex:none; width:120px; }
.wf-prototype-shell .wf-form-label { font-size:11px; color:#595959; }
.wf-prototype-shell .wf-form-label .req { color:#FF4D4F; margin-right:2px; }
.wf-prototype-shell .wf-filter-bar { display:flex; gap:12px; flex-wrap:wrap; align-items:flex-end; }
.wf-prototype-shell .wf-table-list-wrap { overflow-x:auto; -webkit-overflow-scrolling:touch; border:1px solid #F0F0F0; border-radius:4px; }
.wf-prototype-shell .wf-table { width:100%; border-collapse:collapse; font-size:11px; min-width:880px; table-layout:auto; }
.wf-prototype-shell .wf-table th, .wf-prototype-shell .wf-table td { padding:8px 10px; text-align:left; border-bottom:1px solid #F0F0F0; white-space:nowrap; }
.wf-prototype-shell .wf-table thead th { background:#FAFAFA; color:#595959; font-weight:500; }
.wf-prototype-shell .wf-table-list td:nth-child(2) { white-space:normal; min-width:160px; }
.wf-prototype-shell .wf-tag { display:inline-block; padding:1px 8px; border-radius:3px; font-size:10px; line-height:16px; }
.wf-prototype-shell .wf-tag-cyan { background:#E6FFFB; color:#08979C; }
.wf-prototype-shell .wf-tag-purple { background:#F9F0FF; color:#722ED1; }
.wf-prototype-shell .wf-tag-green { background:#F6FFED; color:#52C41A; }
.wf-prototype-shell .wf-tag-blue { background:#E6F4FF; color:#1677FF; }
.wf-prototype-shell .wf-tag-orange { background:#FFF7E6; color:#FA8C16; }
.wf-prototype-shell .wf-tag-default { background:#F5F5F5; color:#8C8C8C; }
.wf-prototype-shell .wf-pagination { display:flex; align-items:center; justify-content:flex-end; gap:4px; padding:10px 16px; font-size:10px; color:#8C8C8C; }
.wf-prototype-shell .wf-pg { width:22px; height:22px; display:flex; align-items:center; justify-content:center; border:1px solid #D9D9D9; border-radius:3px; cursor:pointer; font-size:10px; color:#262626; background:white; }
.wf-prototype-shell .wf-pg.active { background:#1677FF; color:white; border-color:#1677FF; }
.wf-prototype-shell .wf-tabs { background:white; padding:0 20px; border-bottom:1px solid #F0F0F0; display:flex; gap:24px; flex-shrink:0; }
.wf-prototype-shell .wf-tab { padding:10px 0; font-size:12px; color:#595959; cursor:pointer; border-bottom:2px solid transparent; }
.wf-prototype-shell .wf-tab.active { color:#1677FF; border-bottom-color:#1677FF; font-weight:500; }
.wf-prototype-shell .wf-tab-panel { display:none; }
.wf-prototype-shell .wf-tab-panel.active { display:block; }
.wf-prototype-shell .wf-desc-row { display:flex; gap:12px; padding:8px 0; font-size:11px; border-bottom:1px solid #FAFAFA; }
.wf-prototype-shell .wf-desc-row:last-child { border-bottom:0; }
.wf-prototype-shell .wf-desc-label { width:120px; color:#8C8C8C; flex-shrink:0; }
.wf-prototype-shell .wf-desc-value { color:#262626; }
.wf-prototype-shell .wf-alert { display:flex; gap:8px; padding:8px 12px; border-radius:4px; font-size:11px; line-height:1.6; align-items:flex-start; }
.wf-prototype-shell .wf-alert-info { background:#E6F4FF; color:#0958D9; border:1px solid #91CAFF; margin-bottom:10px; }
.wf-prototype-shell .wf-alert-warning { background:#FFFBE6; color:#D48806; border:1px solid #FFE58F; }
.wf-prototype-shell .wf-alert-success { background:#F6FFED; color:#389E0D; border:1px solid #B7EB8F; }
.wf-prototype-shell .wf-upload { border:1px dashed #D9D9D9; border-radius:4px; padding:16px; text-align:center; font-size:11px; color:#8C8C8C; cursor:pointer; background:#FAFAFA; }
.wf-prototype-shell .wf-upload:hover { border-color:#1677FF; }
.wf-prototype-shell .wf-upload-icon { font-size:18px; margin-bottom:4px; }
.wf-prototype-shell .wf-timeline { position:relative; padding-left:14px; }
.wf-prototype-shell .wf-tl-item { position:relative; padding:0 0 14px 14px; border-left:1px solid #E5E7EB; }
.wf-prototype-shell .wf-tl-item::before { content:''; position:absolute; left:-4px; top:5px; width:7px; height:7px; background:#1677FF; border-radius:50%; }
.wf-prototype-shell .wf-tl-time { font-size:10px; color:#8C8C8C; }
.wf-prototype-shell .wf-tl-text { font-size:11px; color:#262626; margin-top:2px; }
</style>
<script>
(function(){
  var I18N = {
    'brand':['FoneSquare 商家管理后台','FoneSquare Admin'],
    'crumb-list':['商家列表','Merchant List'],
    'crumb-detail':['商家详情','Merchant Detail'],
    'crumb-add':['添加商家','Add Merchant'],
    'crumb-myfiles':['我的文件','My Files'],
    'home':['首页','Home'],
    'group-merchant':['商家管理','Merchant'],
    'group-download':['下载中心','Downloads'],
    'menu-list':['商家列表','Merchant List'],
    'menu-myfiles':['我的文件','My Files'],
    'user':['乔谦','Qian Q.'],
    'list-title':['商家列表','Merchant List'],
    'export':['📥 导出','📥 Export'],
    'add':['➕ 添加商家','➕ Add Merchant'],
    'f-name':['商家名称','Merchant Name'],
    'ph-name':['请输入名称关键词','Search by name…'],
    'f-type':['商家类型','Type'],
    'f-status':['状态','Status'],
    'f-sales':['所属销售（仅管理员）','Sales Owner (Admin)'],
    'all':['全部','All'],
    'search':['🔍 查询','🔍 Search'],
    'reset':['↺ 重置','↺ Reset'],
    'result':['查询结果','Result'],
    'total86':['共 86 条','86 rows'],
    'th-name':['商家名称','Merchant Name'],
    'th-type':['类型','Type'],
    'th-status':['状态','Status'],
    'th-contact':['联系人','Contact'],
    'th-phone':['联系方式','Phone'],
    'th-sales':['所属销售','Sales Owner'],
    'th-time':['创建时间','Created At'],
    'th-op':['操作','Action'],
    'view':['查看','View'],
    'edit':['编辑','Edit'],
    'per-page':['10 条/页','10 / page'],
    't-buyer':['买家','Buyer'],
    't-seller':['卖家','Seller'],
    's-active':['使用','Active'],
    's-inactive':['停用','Disabled'],
    'unassigned':['未分配','Unassigned'],
    'back':['返回列表','Back to list'],
    'd-mid':['商家 ID','Merchant ID'],
    'd-sales':['所属销售','Sales Owner'],
    'd-since':['入驻日期','Since'],
    'd-edit':['✏️ 编辑信息','✏️ Edit'],
    'd-disable':['⏸️ 停用','⏸️ Disable'],
    'tab-basic':['基本信息','Basic Info'],
    'tab-kyc':['KYC 认证材料','KYC Docs'],
    'tab-quota':['限额与保证金','Limit & Deposit'],
    'tab-sales':['销售绑定','Sales Binding'],
    'tab-log':['操作日志','Logs'],
    'p-basic':['基本信息','Basic Info'],
    'b-name':['商家名称','Merchant Name'],
    'b-type':['商家类型','Type'],
    'b-contact':['联系人','Contact'],
    'b-phone':['联系方式','Phone'],
    'b-region':['所在地区','Region'],
    'b-status':['状态','Status'],
    'b-email':['邮箱','Email'],
    'region-hk':['香港','Hong Kong'],
    'p-kyc':['KYC 认证材料','KYC Docs'],
    'k-doc':['证件类型','Doc Type'],
    'k-num':['证件号','Doc No.'],
    'k-name':['证件姓名','Doc Holder Name'],
    'k-front':['证件正面','Doc (Front)'],
    'k-back':['证件反面','Doc (Back)'],
    'k-hand':['手持证件','Hand-held Doc'],
    'k-photos':['证件照片','Doc Photos'],
    'k-valid':['证件有效期','Doc Valid Until'],
    'k-status':['审核状态','Audit Status'],
    'k-passed':['已通过','Passed'],
    'k-time':['审核时间','Audited At'],
    'q-rule':['业务规则：保证金由<strong>买家</strong>缴纳；每日下单限额上限 = 保证金 × 10。<strong>未提交转账凭证前</strong>，限额仅可设置为业务默认最小值；上传凭证、运营确认后，限额可在<strong>默认最小值 ~ 保证金 × 10</strong> 范围内自由配置。','Rule: Deposit is paid by <strong>Buyer</strong>. Daily order limit cap = Deposit × 10. <strong>Without proof submission</strong>, limit must stay at the business-defined default minimum. Once proof is uploaded and confirmed by ops, limit can be configured between <strong>default minimum ~ deposit × 10</strong>.'],
    'q-hk':['香港店每日下单限额配置（仅买家）','Hong Kong Daily Order Limit Config (Buyer only)'],
    'q-limit':['每日下单限额（HKD）','Daily Order Limit (HKD)'],
    'q-limit-hint':['默认最小值由业务配置；上限 = 当前保证金 × 10','Default minimum from config; cap = current deposit × 10'],
    'q-deposit':['保证金金额（HKD）','Deposit Amount (HKD)'],
    'q-deposit-hint':['运营录入；保证金 × 10 = 限额上限','Entered by operator; deposit × 10 = limit cap'],
    'q-proof':['保证金转账记录（图片上传）','Deposit Transfer Proof (Image)'],
    'q-upload-hint':['点击上传转账凭证（JPG/PNG，单张 ≤ 5MB，最多 3 张）','Click to upload (JPG/PNG, ≤ 5MB each, up to 3)'],
    'q-upload-done':['✅ 已上传 1 张转账凭证（点击切换示例）','✅ 1 proof uploaded (click to toggle demo)'],
    'q-proof-hint':['未提交凭证前限额无法调高，仅可保留默认最小值','Without proof, limit must stay at default minimum'],
    'q-status':['保证金状态','Deposit Status'],
    'q-st-pending':['未提交','Not submitted'],
    'q-st-submitted':['已提交待确认','Submitted, pending review'],
    'q-confirm':['确认时间 / 确认人','Confirmed At / By'],
    'q-save':['💾 校验并保存','💾 Validate & Save'],
    'q-cancel':['取消','Cancel'],
    'p-sales':['销售绑定','Sales Binding'],
    'sa-current':['当前销售','Current Sales'],
    'sa-since':['绑定时间','Bound Since'],
    'sa-by':['绑定人','Bound By'],
    'sa-reassign':['🔄 更换销售','🔄 Reassign'],
    'sa-history':['📜 查看变更历史','📜 History'],
    'sa-new':['选择新销售','Select New Sales'],
    'sa-new-ph':['从 OB 销售列表选择…','Pick from OB sales…'],
    'sa-reason':['变更原因','Reason'],
    'sa-reason-ph':['请填写变更原因（必填，将记录到操作日志）','Reason (required, written to logs)'],
    'sa-cancel':['取消','Cancel'],
    'sa-confirm':['确认变更','Confirm'],
    'p-log':['操作日志','Operation Logs'],
    'lg-1':['admin01 创建商家 HK Mobile Trade Co.（自动绑定销售：张三）','admin01 created HK Mobile Trade Co. (auto-bound to Sales: Z. San)'],
    'lg-2':['admin01 完成 KYC 审核 → 已通过','admin01 KYC review → Passed'],
    'lg-3':['admin02 编辑联系方式 +852 9*** 4567','admin02 edited phone +852 9*** 4567'],
    'lg-4':['admin01 配置每日下单限额 50,000 HKD（保证金 5,000 已确认）','admin01 set daily limit 50,000 HKD (deposit 5,000 confirmed)'],
    'add-title':['添加商家（单页录入）','Add Merchant (Single Page)'],
    'add-tip':['销售添加 → 自动绑定为本人；管理员添加 → 默认未分配，需在「商家详情 → 销售绑定」中手动分配。','Sales adds → auto-bound to self; Admin adds → unassigned by default, bind on detail page.'],
    'add-basic':['基本信息','Basic Info'],
    'ph-input':['请输入','Input…'],
    'ph-optional':['选填','Optional'],
    'optional':['选填','Optional'],
    'add-type-ph':['请选择 买家 / 卖家','Select Buyer / Seller'],
    'add-region-ph':['国家 / 省份 / 城市 三级联动','Country / Province / City'],
    'add-kyc':['KYC 认证','KYC'],
    'add-doc-ph':['按地区动态展示（HK ID / 护照 / 身份证…）','Dynamic by region (HK ID / Passport / ID…)'],
    'add-valid-ph':['不可选过去日期','Future date only'],
    'add-corp':['企业信息','Corporate Info'],
    'c-name':['公司名称','Company Name'],
    'c-num':['商业登记号','Business Reg. No.'],
    'c-license':['营业执照照片','Business License Photo'],
    'c-license-hint':['JPG / PNG / PDF ≤ 10MB，提交可获更高交易额度','JPG/PNG/PDF ≤ 10MB; raises transaction quota'],
    'add-cancel':['取消','Cancel'],
    'add-submit':['✅ 提交创建','✅ Submit'],
    'mf-title':['我的文件','My Files'],
    'mf-tip':['本页存放商家列表 / 详情 等页面通过「📥 导出」生成的文件，<strong>近 30 天</strong>有效，过期自动清理。点击「下载」获取本地副本，过期项可点「重新生成」重跑导出任务。','This page lists files generated by Export actions. Kept for <strong>30 days</strong>, then auto-purged. Click Download to fetch; click Regenerate for expired items.'],
    'mf-th-name':['文件名','File'],
    'mf-th-source':['来源页面','Source'],
    'mf-th-type':['类型','Type'],
    'mf-th-time':['创建时间','Created At'],
    'mf-th-status':['状态','Status'],
    'mf-th-size':['大小','Size'],
    'mf-th-op':['操作','Action'],
    'mf-st-ready':['可下载','Ready'],
    'mf-st-running':['处理中','Processing'],
    'mf-st-expired':['已过期','Expired'],
    'mf-download':['下载','Download'],
    'mf-regen':['重新生成','Regenerate'],
    'mf-source-list':['商家列表','Merchant List'],
    'mf-empty':['（无文件）','(empty)']
  };

  function H(strings){ return strings.join(''); }

  function tplInner(){
    return ''
      + '<div class="wf-topbar">'
      +   '<div class="wf-topbar-left">'
      +     '<span data-i18n="home">首页</span><span style="margin:0 4px;color:#D9D9D9;">/</span>'
      +     '<span data-i18n="group-merchant">商家管理</span><span style="margin:0 4px;color:#D9D9D9;">/</span>'
      +     '<strong data-i18n="crumb" style="color:#262626;">商家列表</strong>'
      +   '</div>'
      +   '<div class="wf-topbar-right">'
      +     '<div class="wf-lang" title="切换中英文">'
      +       '<span class="wf-lang-btn active" data-lang="zh">中</span>'
      +       '<span class="wf-lang-btn" data-lang="en">EN</span>'
      +     '</div>'
      +     '<span>🔔</span>'
      +     '<div class="wf-topbar-avatar">Q</div>'
      +     '<span style="color:#595959;" data-i18n="user">乔谦</span>'
      +   '</div>'
      + '</div>'
      + '<div class="wf-body">'
      +   '<div class="wf-sider">'
      +     '<div class="wf-sider-logo"><span class="wf-logo-badge">FS</span> FoneSquare</div>'
      +     '<div class="wf-menu-group" data-i18n="group-merchant">商家管理</div>'
      +     '<div class="wf-menu-item active" data-go-view="list" data-menu="merchant"><span>📋</span> <span data-i18n="menu-list">商家列表</span></div>'
      +     '<div class="wf-menu-group" data-i18n="group-download">下载中心</div>'
      +     '<div class="wf-menu-item" data-go-view="myfiles" data-menu="myfiles"><span>📥</span> <span data-i18n="menu-myfiles">我的文件</span></div>'
      +   '</div>'
      +   '<div class="wf-content">'
      +     listView() + detailView() + addView() + myFilesView()
      +   '</div>'
      + '</div>';
  }

  function listView(){
    return ''
    + '<div class="wf-view" data-view="list">'
    +   '<div class="wf-page">'
    +     '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">'
    +       '<span style="font-size:16px;font-weight:700;color:#262626;" data-i18n="list-title">商家列表</span>'
    +       '<div style="display:flex;gap:6px;">'
    +         '<button class="wf-btn" data-act="export" data-i18n="export">📥 导出</button>'
    +         '<button class="wf-btn wf-btn-primary" data-go-view="add" data-i18n="add">➕ 添加商家</button>'
    +       '</div>'
    +     '</div>'
    +     '<div class="wf-card"><div class="wf-card-body" style="padding:12px 16px;">'
    +       '<div class="wf-filter-bar">'
    +         '<div class="wf-form-item"><div class="wf-form-label" data-i18n="f-name">商家名称</div><div class="wf-input" data-i18n="ph-name">请输入名称关键词</div></div>'
    +         '<div class="wf-form-item w120"><div class="wf-form-label" data-i18n="f-type">商家类型</div><div class="wf-select" data-i18n="all">全部</div></div>'
    +         '<div class="wf-form-item w120"><div class="wf-form-label" data-i18n="f-status">状态</div><div class="wf-select" data-i18n="all">全部</div></div>'
    +         '<div class="wf-form-item"><div class="wf-form-label" data-i18n="f-sales">所属销售（仅管理员）</div><div class="wf-select" data-i18n="all">全部</div></div>'
    +         '<div class="wf-form-item" style="flex:none;width:auto;"><div class="wf-form-label">&nbsp;</div><div style="display:flex;gap:4px;"><button class="wf-btn wf-btn-primary" data-i18n="search">🔍 查询</button><button class="wf-btn" data-i18n="reset">↺ 重置</button></div></div>'
    +       '</div>'
    +     '</div></div>'
    +     '<div class="wf-card">'
    +       '<div class="wf-card-head"><span data-i18n="result">查询结果</span><span style="font-size:10px;color:#8C8C8C;font-weight:400;" data-i18n="total86">共 86 条</span></div>'
    +       '<div class="wf-table-list-wrap">'
    +         '<table class="wf-table wf-table-list">'
    +           '<thead><tr>'
    +             '<th style="width:50px;">ID</th>'
    +             '<th data-i18n="th-name">商家名称</th>'
    +             '<th style="width:60px;" data-i18n="th-type">类型</th>'
    +             '<th style="width:60px;" data-i18n="th-status">状态</th>'
    +             '<th style="width:80px;" data-i18n="th-contact">联系人</th>'
    +             '<th style="width:140px;" data-i18n="th-phone">联系方式</th>'
    +             '<th style="width:80px;" data-i18n="th-sales">所属销售</th>'
    +             '<th style="width:90px;" data-i18n="th-time">创建时间</th>'
    +             '<th style="width:120px;" data-i18n="th-op">操作</th>'
    +           '</tr></thead>'
    +           '<tbody>'
    +             listRow('1001','HK Mobile Trade Co.','buyer','active','陈先生','+852 9123 4567','张三','2026-04-10')
    +             + listRow('1002','Macau Phones Ltd.','seller','active','李小姐','+853 6234 5678','李四','2026-04-12')
    +             + listRow('1003','SG Recycle Hub','buyer','inactive','王先生','+65 8345 6789','—','2026-04-15')
    +             + listRow('1004','TW Digital Trade','seller','active','林先生','+886 912 345678','张三','2026-04-08')
    +             + listRow('1005','JP Phone Market','buyer','active','田中','+81 80 1234 5678','王五','2026-04-06')
    +           '</tbody>'
    +         '</table>'
    +       '</div>'
    +       '<div class="wf-pagination">'
    +         '<span style="margin-right:6px;" data-i18n="total86">共 86 条</span>'
    +         '<div class="wf-pg">&lt;</div><div class="wf-pg active">1</div><div class="wf-pg">2</div><div class="wf-pg">3</div><div class="wf-pg">…</div><div class="wf-pg">9</div><div class="wf-pg">&gt;</div>'
    +         '<span style="margin-left:6px;" data-i18n="per-page">10 条/页</span>'
    +       '</div>'
    +     '</div>'
    +   '</div>'
    + '</div>';
  }

  function listRow(id, name, type, status, contact, phone, sales, time){
    var typeTag = type==='buyer' ? 'wf-tag-cyan' : 'wf-tag-purple';
    var typeKey = type==='buyer' ? 't-buyer' : 't-seller';
    var statusTag = status==='active' ? 'wf-tag-green' : 'wf-tag-default';
    var statusKey = status==='active' ? 's-active' : 's-inactive';
    var salesCell = sales==='—'
      ? '<span style="color:#BFBFBF;" data-i18n="unassigned">未分配</span>'
      : sales;
    return '<tr>'
      + '<td>' + id + '</td>'
      + '<td style="font-weight:500;color:#262626;">' + name + '</td>'
      + '<td><span class="wf-tag ' + typeTag + '" data-i18n="' + typeKey + '"></span></td>'
      + '<td><span class="wf-tag ' + statusTag + '" data-i18n="' + statusKey + '"></span></td>'
      + '<td>' + contact + '</td>'
      + '<td>' + phone + '</td>'
      + '<td>' + salesCell + '</td>'
      + '<td style="font-size:10px;color:#8C8C8C;">' + time + '</td>'
      + '<td>'
      +   '<button class="wf-btn-link" data-go-view="detail" data-merchant-id="' + id + '" data-merchant-name="' + name + '" data-merchant-type="' + type + '" data-i18n="view">查看</button> '
      +   '<button class="wf-btn-link" data-i18n="edit">编辑</button>'
      + '</td>'
      + '</tr>';
  }

  function detailView(){
    return ''
    + '<div class="wf-view" data-view="detail">'
    +   '<div class="wf-page" style="padding-bottom:0;">'
    +     '<div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">'
    +       '<button class="wf-btn" data-go-view="list">← <span data-i18n="back">返回列表</span></button>'
    +       '<span style="font-size:13px;color:#8C8C8C;"><span data-i18n="d-mid">商家 ID</span>：<span data-bind="dMid">1001</span></span>'
    +     '</div>'
    +     '<div class="wf-card"><div class="wf-card-body" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">'
    +       '<div>'
    +         '<div style="font-size:15px;font-weight:600;color:#262626;">'
    +           '<span data-bind="dName">HK Mobile Trade Co.</span> '
    +           '<span class="wf-tag wf-tag-cyan" data-bind="dType" data-i18n="t-buyer" style="margin-left:6px;">买家</span> '
    +           '<span class="wf-tag wf-tag-green" data-i18n="s-active">使用</span>'
    +         '</div>'
    +         '<div style="font-size:11px;color:#8C8C8C;margin-top:4px;">'
    +           '<span data-i18n="d-mid">商家 ID</span>：<span data-bind="dMid2">1001</span> · '
    +           '<span data-i18n="d-sales">所属销售</span>：张三 · '
    +           '<span data-i18n="d-since">入驻日期</span>：2026-04-10'
    +         '</div>'
    +       '</div>'
    +       '<div style="display:flex;gap:6px;">'
    +         '<button class="wf-btn wf-btn-primary" data-i18n="d-edit">✏️ 编辑信息</button>'
    +         '<button class="wf-btn" data-i18n="d-disable">⏸️ 停用</button>'
    +       '</div>'
    +     '</div></div>'
    +   '</div>'
    +   '<div class="wf-tabs">'
    +     '<div class="wf-tab active" data-tab="basic" data-i18n="tab-basic">基本信息</div>'
    +     '<div class="wf-tab" data-tab="kyc" data-i18n="tab-kyc">KYC 认证材料</div>'
    +     '<div class="wf-tab" data-tab="quota" data-i18n="tab-quota">限额与保证金</div>'
    +     '<div class="wf-tab" data-tab="sales" data-i18n="tab-sales">销售绑定</div>'
    +     '<div class="wf-tab" data-tab="log" data-i18n="tab-log">操作日志</div>'
    +   '</div>'
    +   '<div class="wf-page" style="padding-top:14px;">'
    +     panelBasic() + panelKyc() + panelQuota() + panelSales() + panelLog()
    +   '</div>'
    + '</div>';
  }

  function panelBasic(){
    return '<div class="wf-tab-panel active" data-panel="basic">'
      + '<div class="wf-card"><div class="wf-card-head" data-i18n="p-basic">基本信息</div><div class="wf-card-body">'
      +   descRow('b-name','商家名称','HK Mobile Trade Co.')
      +   '<div class="wf-desc-row"><div class="wf-desc-label" data-i18n="b-type">商家类型</div><div class="wf-desc-value"><span class="wf-tag wf-tag-cyan" data-i18n="t-buyer">买家</span></div></div>'
      +   descRow('b-contact','联系人','陈先生')
      +   descRow('b-phone','联系方式','+852 9123 4567')
      +   descRow('b-email','邮箱','chen@hkmobile.com')
      +   '<div class="wf-desc-row"><div class="wf-desc-label" data-i18n="b-region">所在地区</div><div class="wf-desc-value" data-i18n="region-hk">香港</div></div>'
      +   '<div class="wf-desc-row"><div class="wf-desc-label" data-i18n="b-status">状态</div><div class="wf-desc-value"><span class="wf-tag wf-tag-green" data-i18n="s-active">使用</span></div></div>'
      + '</div></div></div>';
  }
  function descRow(key,label,val){
    return '<div class="wf-desc-row"><div class="wf-desc-label" data-i18n="' + key + '">' + label + '</div><div class="wf-desc-value">' + val + '</div></div>';
  }
  function panelKyc(){
    return '<div class="wf-tab-panel" data-panel="kyc">'
      + '<div class="wf-card"><div class="wf-card-head" data-i18n="p-kyc">KYC 认证材料</div><div class="wf-card-body">'
      +   descRow('k-doc','证件类型','HK ID')
      +   descRow('k-num','证件号','A***456(7)')
      +   descRow('k-name','证件姓名','陈大文')
      +   '<div class="wf-desc-row"><div class="wf-desc-label" data-i18n="k-front">证件正面</div><div class="wf-desc-value">📷 <a href="#" onclick="return false">view</a></div></div>'
      +   '<div class="wf-desc-row"><div class="wf-desc-label" data-i18n="k-back">证件反面</div><div class="wf-desc-value">📷 <a href="#" onclick="return false">view</a></div></div>'
      +   '<div class="wf-desc-row"><div class="wf-desc-label" data-i18n="k-status">审核状态</div><div class="wf-desc-value"><span class="wf-tag wf-tag-green" data-i18n="k-passed">已通过</span></div></div>'
      +   descRow('k-time','审核时间','2026-04-10 14:23')
      + '</div></div></div>';
  }
  function panelQuota(){
    return '<div class="wf-tab-panel" data-panel="quota">'
      + '<div class="wf-alert wf-alert-info"><span>ℹ️</span><span data-i18n="q-rule"></span></div>'
      + '<div class="wf-card"><div class="wf-card-head" data-i18n="q-hk">香港店每日下单限额配置（仅买家）</div><div class="wf-card-body">'
      +   '<div class="wf-form-row">'
      +     '<div class="wf-form-item">'
      +       '<div class="wf-form-label"><span class="req">*</span><span data-i18n="q-limit">每日下单限额（HKD）</span></div>'
      +       '<div class="wf-input wf-input-edit" data-bind="qInputLimit" contenteditable="true" spellcheck="false">50000</div>'
      +       '<div style="font-size:10px;color:#8C8C8C;margin-top:3px;" data-i18n="q-limit-hint"></div>'
      +     '</div>'
      +     '<div class="wf-form-item">'
      +       '<div class="wf-form-label"><span class="req">*</span><span data-i18n="q-deposit">保证金金额（HKD）</span></div>'
      +       '<div class="wf-input wf-input-edit" data-bind="qInputDeposit" contenteditable="true" spellcheck="false">5000</div>'
      +       '<div style="font-size:10px;color:#8C8C8C;margin-top:3px;" data-i18n="q-deposit-hint"></div>'
      +     '</div>'
      +   '</div>'
      +   '<div class="wf-form-item">'
      +     '<div class="wf-form-label"><span class="req">*</span><span data-i18n="q-proof">保证金转账记录（图片上传）</span></div>'
      +     '<div class="wf-upload" data-bind="qUpload">'
      +       '<div class="wf-upload-icon">⬆️</div>'
      +       '<div data-bind="qUploadText" data-i18n="q-upload-hint">点击上传转账凭证</div>'
      +     '</div>'
      +     '<div style="font-size:10px;color:#8C8C8C;margin-top:3px;" data-i18n="q-proof-hint"></div>'
      +   '</div>'
      +   '<div class="wf-form-row">'
      +     '<div class="wf-form-item"><div class="wf-form-label" data-i18n="q-status">保证金状态</div><div><span class="wf-tag wf-tag-default" data-bind="qStatus" data-i18n="q-st-pending">未提交</span></div></div>'
      +     '<div class="wf-form-item"><div class="wf-form-label" data-i18n="q-confirm">确认时间 / 确认人</div><div style="font-size:11px;color:#262626;">— / —</div></div>'
      +   '</div>'
      +   '<div style="display:flex;gap:6px;margin-top:8px;">'
      +     '<button class="wf-btn wf-btn-primary" data-act="qSave" data-i18n="q-save">💾 校验并保存</button>'
      +     '<button class="wf-btn" data-i18n="q-cancel">取消</button>'
      +   '</div>'
      +   '<div class="wf-alert" data-bind="qResult" style="display:none;margin-top:10px;"></div>'
      + '</div></div></div>';
  }
  function panelSales(){
    return '<div class="wf-tab-panel" data-panel="sales">'
      + '<div class="wf-card"><div class="wf-card-head" data-i18n="p-sales">销售绑定</div><div class="wf-card-body">'
      +   descRow('sa-current','当前销售','张三 (sales01@fonesquare.com)')
      +   descRow('sa-since','绑定时间','2026-04-10 14:23')
      +   descRow('sa-by','绑定人','admin01')
      +   '<div style="margin-top:10px;display:flex;gap:6px;">'
      +     '<button class="wf-btn wf-btn-primary" data-act="saReassign" data-i18n="sa-reassign">🔄 更换销售</button>'
      +     '<button class="wf-btn" data-i18n="sa-history">📜 查看变更历史</button>'
      +   '</div>'
      +   '<div data-bind="saReassignBox" style="display:none;margin-top:12px;border:1px dashed #1677FF;border-radius:6px;padding:12px;background:#F0F8FF;">'
      +     '<div class="wf-form-item"><div class="wf-form-label"><span class="req">*</span><span data-i18n="sa-new">选择新销售</span></div><div class="wf-select" data-i18n="sa-new-ph">从 OB 销售列表选择…</div></div>'
      +     '<div class="wf-form-item"><div class="wf-form-label"><span class="req">*</span><span data-i18n="sa-reason">变更原因</span></div><div class="wf-textarea" data-i18n="sa-reason-ph">请填写变更原因（必填，将记录到操作日志）</div></div>'
      +     '<div style="display:flex;gap:6px;justify-content:flex-end;"><button class="wf-btn" data-act="saCancel" data-i18n="sa-cancel">取消</button><button class="wf-btn wf-btn-primary" data-i18n="sa-confirm">确认变更</button></div>'
      +   '</div>'
      + '</div></div></div>';
  }
  function panelLog(){
    return '<div class="wf-tab-panel" data-panel="log">'
      + '<div class="wf-card"><div class="wf-card-head" data-i18n="p-log">操作日志</div><div class="wf-card-body">'
      +   '<div class="wf-timeline">'
      +     '<div class="wf-tl-item"><div class="wf-tl-time">2026-04-10 14:23</div><div class="wf-tl-text" data-i18n="lg-1"></div></div>'
      +     '<div class="wf-tl-item"><div class="wf-tl-time">2026-04-10 14:25</div><div class="wf-tl-text" data-i18n="lg-2"></div></div>'
      +     '<div class="wf-tl-item"><div class="wf-tl-time">2026-04-12 10:08</div><div class="wf-tl-text" data-i18n="lg-3"></div></div>'
      +     '<div class="wf-tl-item"><div class="wf-tl-time">2026-04-15 16:40</div><div class="wf-tl-text" data-i18n="lg-4"></div></div>'
      +   '</div>'
      + '</div></div></div>';
  }

  function addView(){
    return '<div class="wf-view" data-view="add"><div class="wf-page">'
      + '<div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;"><button class="wf-btn" data-go-view="list">← <span data-i18n="back">返回列表</span></button><span style="font-size:14px;color:#262626;font-weight:600;" data-i18n="add-title">添加商家（单页录入）</span></div>'
      + '<div class="wf-alert wf-alert-info"><span>ℹ️</span><span data-i18n="add-tip"></span></div>'
      + '<div class="wf-card"><div class="wf-card-head" data-i18n="add-basic">基本信息</div><div class="wf-card-body">'
      +   '<div class="wf-form-row">'
      +     formItem('b-name','商家名称',true,'ph-input','请输入','wf-input')
      +     + formItem('b-type','商家类型',true,'add-type-ph','请选择 买家 / 卖家','wf-select')
      +   '</div>'
      +   '<div class="wf-form-row">'
      +     formItem('b-contact','联系人',true,'ph-input','请输入','wf-input')
      +     + formItem('b-phone','联系方式',true,null,'+852 ...','wf-input')
      +   '</div>'
      +   '<div class="wf-form-row">'
      +     formItem('b-email','邮箱',false,'ph-optional','选填','wf-input')
      +     + formItem('b-region','所在地区',true,'add-region-ph','国家 / 省份 / 城市 三级联动','wf-select')
      +   '</div>'
      + '</div></div>'
      + '<div class="wf-card"><div class="wf-card-head" data-i18n="add-kyc">KYC 认证</div><div class="wf-card-body">'
      +   '<div class="wf-form-row">'
      +     formItem('k-doc','证件类型',true,'add-doc-ph','按地区动态展示（HK ID / 护照 / 身份证…）','wf-select')
      +     + formItem('k-num','证件号',true,'ph-input','请输入','wf-input')
      +   '</div>'
      +   '<div class="wf-form-row">'
      +     formItem('k-name','证件姓名',true,'ph-input','请输入','wf-input')
      +     + formItem('k-valid','证件有效期',true,'add-valid-ph','不可选过去日期','wf-input')
      +   '</div>'
      +   '<div class="wf-form-item">'
      +     '<div class="wf-form-label"><span class="req">*</span><span data-i18n="k-photos">证件照片</span></div>'
      +     '<div style="display:flex;gap:8px;">'
      +       '<div class="wf-upload" style="flex:1;"><div class="wf-upload-icon">📤</div><span data-i18n="k-front">证件正面</span></div>'
      +       '<div class="wf-upload" style="flex:1;"><div class="wf-upload-icon">📤</div><span data-i18n="k-back">证件反面</span></div>'
      +       '<div class="wf-upload" style="flex:1;"><div class="wf-upload-icon">📤</div><span data-i18n="k-hand">手持证件</span></div>'
      +     '</div>'
      +   '</div>'
      + '</div></div>'
      + '<div class="wf-card"><div class="wf-card-head"><span data-i18n="add-corp">企业信息</span> <span style="font-size:10px;color:#BFBFBF;font-weight:400;margin-left:6px;" data-i18n="optional">选填</span></div><div class="wf-card-body">'
      +   '<div class="wf-form-row">'
      +     formItem('c-name','公司名称',false,'ph-optional','选填','wf-input')
      +     + formItem('c-num','商业登记号',false,'ph-optional','选填','wf-input')
      +   '</div>'
      +   '<div class="wf-form-item"><div class="wf-form-label" data-i18n="c-license">营业执照照片</div><div class="wf-upload"><div class="wf-upload-icon">📤</div><span data-i18n="c-license-hint">JPG / PNG / PDF ≤ 10MB，提交可获更高交易额度</span></div></div>'
      + '</div></div>'
      + '<div style="display:flex;gap:8px;justify-content:flex-end;margin-bottom:12px;">'
      +   '<button class="wf-btn" data-go-view="list" data-i18n="add-cancel">取消</button>'
      +   '<button class="wf-btn wf-btn-primary" data-act="addSubmit" data-i18n="add-submit">✅ 提交创建</button>'
      + '</div>'
      + '</div></div>';
  }
  function formItem(labelKey, labelTxt, req, phKey, phTxt, ctrlClass){
    var phAttr = phKey ? (' data-i18n="' + phKey + '"') : '';
    return '<div class="wf-form-item">'
      + '<div class="wf-form-label">' + (req ? '<span class="req">*</span>' : '') + '<span data-i18n="' + labelKey + '">' + labelTxt + '</span></div>'
      + '<div class="' + ctrlClass + '"' + phAttr + '>' + phTxt + '</div>'
      + '</div>';
  }

  function myFilesView(){
    return '<div class="wf-view" data-view="myfiles"><div class="wf-page">'
      + '<div style="font-size:16px;font-weight:700;color:#262626;margin-bottom:12px;" data-i18n="mf-title">我的文件</div>'
      + '<div class="wf-alert wf-alert-info" style="margin-bottom:12px;"><span>📥</span><span data-i18n="mf-tip"></span></div>'
      + '<div class="wf-card"><div class="wf-table-list-wrap">'
      +   '<table class="wf-table">'
      +     '<thead><tr>'
      +       '<th data-i18n="mf-th-name">文件名</th>'
      +       '<th style="width:100px;" data-i18n="mf-th-source">来源页面</th>'
      +       '<th style="width:60px;" data-i18n="mf-th-type">类型</th>'
      +       '<th style="width:130px;" data-i18n="mf-th-time">创建时间</th>'
      +       '<th style="width:90px;" data-i18n="mf-th-status">状态</th>'
      +       '<th style="width:70px;" data-i18n="mf-th-size">大小</th>'
      +       '<th style="width:140px;" data-i18n="mf-th-op">操作</th>'
      +     '</tr></thead>'
      +     '<tbody>'
      +       mfRow('merchants_2026-04-28_1430.xlsx','mf-source-list','XLSX','2026-04-28 14:30','ready','238 KB')
      +       + mfRow('merchants_buyer_2026-04-25_0902.xlsx','mf-source-list','XLSX','2026-04-25 09:02','ready','142 KB')
      +       + mfRow('merchants_export_pending_now.xlsx','mf-source-list','XLSX','2026-04-28 18:31','running','—')
      +       + mfRow('merchants_2026-03-28_1015.xlsx','mf-source-list','XLSX','2026-03-28 10:15','expired','201 KB')
      +     '</tbody>'
      +   '</table>'
      + '</div></div>'
      + '</div></div>';
  }
  function mfRow(name, sourceKey, type, time, status, size){
    var statusTagClass = status==='ready' ? 'wf-tag-green' : (status==='running' ? 'wf-tag-blue' : 'wf-tag-default');
    var statusKey = 'mf-st-' + status;
    var op;
    if (status === 'ready') {
      op = '<button class="wf-btn-link" data-act="mfDownload" data-file="' + name + '" data-i18n="mf-download">下载</button>';
    } else if (status === 'running') {
      op = '<span style="color:#8C8C8C;font-size:11px;">…</span>';
    } else {
      op = '<button class="wf-btn-link" data-act="mfRegen" data-file="' + name + '" data-i18n="mf-regen">重新生成</button>';
    }
    return '<tr>'
      + '<td style="font-weight:500;color:#262626;">' + name + '</td>'
      + '<td><span class="wf-tag wf-tag-cyan" data-i18n="' + sourceKey + '"></span></td>'
      + '<td>' + type + '</td>'
      + '<td style="font-size:10px;color:#8C8C8C;">' + time + '</td>'
      + '<td><span class="wf-tag ' + statusTagClass + '" data-i18n="' + statusKey + '"></span></td>'
      + '<td>' + size + '</td>'
      + '<td>' + op + '</td>'
      + '</tr>';
  }

  function applyI18n(root, lang){
    root.querySelectorAll('[data-i18n]').forEach(function(el){
      var k = el.getAttribute('data-i18n');
      if (k === 'crumb') return; // crumb dynamic
      var pair = I18N[k];
      if (!pair) return;
      var v = pair[lang === 'zh' ? 0 : 1];
      if (/<\w+/.test(v)) el.innerHTML = v;
      else el.textContent = v;
    });
  }

  function setCrumb(root, view, lang){
    var crumb = root.querySelector('[data-i18n="crumb"]');
    if (!crumb) return;
    var k = 'crumb-' + view;
    crumb.textContent = I18N[k] ? I18N[k][lang==='zh'?0:1] : view;
    // 顶部第二段（商家管理 vs 下载中心）随菜单切换
    var groupSpan = root.querySelector('.wf-topbar-left [data-i18n="group-merchant"], .wf-topbar-left [data-i18n="group-download"]');
    if (groupSpan){
      var groupKey = view==='myfiles' ? 'group-download' : 'group-merchant';
      groupSpan.setAttribute('data-i18n', groupKey);
      groupSpan.textContent = I18N[groupKey][lang==='zh'?0:1];
    }
  }

  function go(root, view, state){
    root.querySelectorAll('.wf-view').forEach(function(v){
      v.classList.toggle('active', v.dataset.view === view);
    });
    // 菜单 active：myfiles 高亮我的文件，否则高亮商家列表
    root.querySelectorAll('.wf-menu-item').forEach(function(m){
      var menuFor = m.dataset.menu;
      m.classList.toggle('active', (view==='myfiles' && menuFor==='myfiles') || (view!=='myfiles' && menuFor==='merchant'));
    });
    setCrumb(root, view, state.lang);
  }

  function init(root){
    root.innerHTML = tplInner();
    var state = { lang: 'zh', hasProof: false };
    var initView = root.dataset.initView || 'list';

    // 语言切换
    root.querySelectorAll('.wf-lang-btn').forEach(function(b){
      b.addEventListener('click', function(){
        root.querySelectorAll('.wf-lang-btn').forEach(function(x){ x.classList.remove('active'); });
        b.classList.add('active');
        state.lang = b.dataset.lang;
        applyI18n(root, state.lang);
        // 重设保证金 upload 文案
        var upTxt = root.querySelector('[data-bind="qUploadText"]');
        if (upTxt){
          upTxt.setAttribute('data-i18n', state.hasProof ? 'q-upload-done' : 'q-upload-hint');
          upTxt.textContent = I18N[upTxt.getAttribute('data-i18n')][state.lang==='zh'?0:1];
        }
        var st = root.querySelector('[data-bind="qStatus"]');
        if (st){
          var k = state.hasProof ? 'q-st-submitted' : 'q-st-pending';
          st.setAttribute('data-i18n', k);
          st.textContent = I18N[k][state.lang==='zh'?0:1];
        }
        // crumb / group 重设
        var activeView = root.querySelector('.wf-view.active');
        if (activeView) setCrumb(root, activeView.dataset.view, state.lang);
      });
    });

    // 视图切换（列表行的查看 / 添加按钮 / 菜单项 / 返回按钮）
    root.addEventListener('click', function(e){
      var goBtn = e.target.closest('[data-go-view]');
      if (goBtn){
        var v = goBtn.dataset.goView;
        if (v === 'detail'){
          var mid = goBtn.dataset.merchantId;
          var mname = goBtn.dataset.merchantName;
          var mtype = goBtn.dataset.merchantType;
          if (mid){
            root.querySelectorAll('[data-bind="dMid"], [data-bind="dMid2"]').forEach(function(x){ x.textContent = mid; });
            root.querySelector('[data-bind="dName"]').textContent = mname;
            var dType = root.querySelector('[data-bind="dType"]');
            var typeKey = mtype === 'buyer' ? 't-buyer' : 't-seller';
            dType.className = 'wf-tag ' + (mtype === 'buyer' ? 'wf-tag-cyan' : 'wf-tag-purple');
            dType.setAttribute('data-i18n', typeKey);
            dType.textContent = I18N[typeKey][state.lang==='zh'?0:1];
          }
        }
        go(root, v, state);
        return;
      }
      var act = e.target.closest('[data-act]');
      if (!act) return;
      var name = act.dataset.act;
      if (name === 'export') {
        var msg = state.lang === 'zh'
          ? '导出任务已提交，完成后请到「下载中心 → 我的文件」下载（演示）'
          : 'Export job submitted. Check Downloads → My Files when ready (demo).';
        alert(msg);
        go(root, 'myfiles', state);
      } else if (name === 'qSave') {
        var DEFAULT_MIN = 1000;
        var limit = parseInt((root.querySelector('[data-bind="qInputLimit"]').textContent || '0').replace(/[^0-9]/g, ''), 10) || 0;
        var deposit = parseInt((root.querySelector('[data-bind="qInputDeposit"]').textContent || '0').replace(/[^0-9]/g, ''), 10) || 0;
        var msg = '', lvl = 'wf-alert-info';
        if (!state.hasProof) {
          if (limit > DEFAULT_MIN) {
            msg = state.lang === 'zh' ? ('❌ 未提交保证金转账凭证，限额最大仅可设置为业务默认最小值 ' + DEFAULT_MIN + ' HKD') : ('Without deposit proof, daily limit cannot exceed default minimum ' + DEFAULT_MIN + ' HKD');
            lvl = 'wf-alert-warning';
          } else {
            msg = state.lang === 'zh' ? '✅ 已保存（限额采用默认最小值；保证金未提交，状态保持「未提交」）' : 'Saved (limit at default minimum; deposit not submitted)';
            lvl = 'wf-alert-success';
          }
        } else {
          var maxLimit = deposit * 10;
          if (deposit <= 0) { msg = state.lang === 'zh' ? '❌ 保证金金额必须大于 0' : 'Deposit must be greater than 0'; lvl = 'wf-alert-warning'; }
          else if (limit > maxLimit) { msg = state.lang === 'zh' ? ('❌ 限额超过保证金 × 10 = ' + maxLimit + ' HKD，请调低限额或提高保证金') : ('Limit exceeds deposit × 10 = ' + maxLimit + ' HKD'); lvl = 'wf-alert-warning'; }
          else if (limit < DEFAULT_MIN) { msg = state.lang === 'zh' ? ('❌ 限额低于业务默认最小值 ' + DEFAULT_MIN + ' HKD') : ('Limit below default minimum ' + DEFAULT_MIN + ' HKD'); lvl = 'wf-alert-warning'; }
          else { msg = state.lang === 'zh' ? ('✅ 校验通过：保证金 ' + deposit + ' HKD × 10 = ' + maxLimit + ' HKD（当前限额 ' + limit + ' HKD ≤ 上限）已保存') : ('OK: deposit ' + deposit + ' × 10 = ' + maxLimit + '; current limit ' + limit + ' saved'); lvl = 'wf-alert-success'; }
        }
        var resBox = root.querySelector('[data-bind="qResult"]');
        resBox.className = 'wf-alert ' + lvl;
        resBox.textContent = msg;
        resBox.style.display = 'flex';
      } else if (name === 'saReassign') {
        root.querySelector('[data-bind="saReassignBox"]').style.display = 'block';
      } else if (name === 'saCancel') {
        root.querySelector('[data-bind="saReassignBox"]').style.display = 'none';
      } else if (name === 'addSubmit') {
        var m2 = state.lang === 'zh' ? '✅ 创建成功（演示）— 实际提交时校验证件唯一性 / 制裁名单核查 / 触发归属规则' : '✅ Created (demo) — real submit will check ID uniqueness, sanction list and ownership rules';
        alert(m2);
        go(root, 'list', state);
      } else if (name === 'mfDownload') {
        alert((state.lang === 'zh' ? '正在下载：' : 'Downloading: ') + act.dataset.file);
      } else if (name === 'mfRegen') {
        alert((state.lang === 'zh' ? '已重新提交导出任务（演示）：' : 'Re-submitted export job (demo): ') + act.dataset.file);
      }
    });

    // Tab 切换
    root.querySelectorAll('.wf-tab').forEach(function(t){
      t.addEventListener('click', function(){
        root.querySelectorAll('.wf-tab').forEach(function(x){ x.classList.remove('active'); });
        t.classList.add('active');
        root.querySelectorAll('.wf-tab-panel').forEach(function(p){ p.classList.toggle('active', p.dataset.panel === t.dataset.tab); });
      });
    });

    // 保证金凭证上传切换
    var qUpload = root.querySelector('[data-bind="qUpload"]');
    if (qUpload){
      qUpload.addEventListener('click', function(){
        state.hasProof = !state.hasProof;
        qUpload.style.borderStyle = state.hasProof ? 'solid' : 'dashed';
        qUpload.style.borderColor = state.hasProof ? '#52C41A' : '#D9D9D9';
        qUpload.style.background = state.hasProof ? '#F6FFED' : '#FAFAFA';
        var upTxt = root.querySelector('[data-bind="qUploadText"]');
        upTxt.setAttribute('data-i18n', state.hasProof ? 'q-upload-done' : 'q-upload-hint');
        upTxt.textContent = I18N[upTxt.getAttribute('data-i18n')][state.lang==='zh'?0:1];
        var st = root.querySelector('[data-bind="qStatus"]');
        var k = state.hasProof ? 'q-st-submitted' : 'q-st-pending';
        st.className = 'wf-tag ' + (state.hasProof ? 'wf-tag-blue' : 'wf-tag-default');
        st.setAttribute('data-i18n', k);
        st.textContent = I18N[k][state.lang==='zh'?0:1];
      });
    }

    // 初始 i18n + 视图
    applyI18n(root, state.lang);
    go(root, initView, state);
  }

  function bootAll(){
    document.querySelectorAll('[data-prototype="merchant-admin"]').forEach(init);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootAll);
  } else {
    bootAll();
  }
})();
</script>
'''

# 找到 </body> 之前的位置
pos = text.rfind('</body>')
if pos < 0:
    print('ERROR: 未找到 </body>'); sys.exit(1)
text = text[:pos] + INJECT + text[pos:]

# ---- 5) 版本记录 V2.6 ----
V25_LINE = '<tr><td>2026-04-28</td><td>V2.5 精细化调整：'
if V25_LINE not in text:
    print('ERROR: V2.5 行不存在'); sys.exit(1)
V26_LINE = '<tr><td>2026-04-28</td><td>V2.6 后台原型菜单回归 + 每页页面定位下放交互图：① 「<strong>商家列表 / 商家详情 / 添加商家</strong>」三页的<strong>「页面定位」info-box 紧下方</strong>各嵌入一份完整可交互原型；② 原型保留<strong>侧边菜单</strong>（参考截图样式），但仅含两组：「<strong>商家管理 → 商家列表</strong>」与「<strong>下载中心 → 我的文件</strong>」（导出文件存放页，30 天有效）；③ 原型用 <code>data-prototype="merchant-admin"</code> + <code>data-init-view</code> 占位 + 通用模板渲染脚本 实现，三页共享同一份代码、独立状态；④ 列表页「📥 导出」会演示提交导出任务后跳转到「我的文件」；「我的文件」支持下载、重新生成（已过期）、状态展示（处理中/可下载/已过期）。</td><td style="position: relative;">乔谦</td></tr>\n      ' + V25_LINE
text = text.replace(V25_LINE, V26_LINE)

PRD.write_text(text, encoding='utf-8')
print('Done. final lines:', text.count('\n'))
