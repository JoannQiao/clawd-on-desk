#!/usr/bin/env python3
"""
V2.8 改造：
  1) 筛选区改为 grid 布局，禁止 label 换行错位；按钮组单独一行靠右；
     去掉「(仅管理员)」长 label 提示，避免占两行错位（保留在 hint 标签）。
  2) 列表去掉「联系方式」列：表头 / 单元 / listRow 签名同步精简。
  3) 「所属销售」→「维护人」，单元值改为「姓名（工号）」格式。
"""
from pathlib import Path
import sys

PRD = Path('/Users/qiaoqian/clawd-on-desk/FoneSquare-PRD-v2.html')
text = PRD.read_text(encoding='utf-8')

# ---------- 1) CSS：filter-bar 改 grid + label nowrap + 增加 actions 行 ----------
OLD_CSS = ".wf-prototype-shell .wf-filter-bar { display:flex; gap:12px; flex-wrap:wrap; align-items:flex-end; }"
NEW_CSS = (
    ".wf-prototype-shell .wf-filter-bar { display:grid; grid-template-columns:repeat(auto-fill, minmax(190px, 1fr)); gap:10px 12px; align-items:end; }\n"
    ".wf-prototype-shell .wf-filter-bar .wf-form-item { width:auto; flex:none; min-width:0; }\n"
    ".wf-prototype-shell .wf-filter-bar .wf-form-label { white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }\n"
    ".wf-prototype-shell .wf-filter-actions { display:flex; justify-content:flex-end; gap:6px; margin-top:10px; }\n"
    ".wf-prototype-shell .wf-filter-hint { font-size:10px; color:#8C8C8C; margin-top:6px; }"
)
if OLD_CSS not in text:
    print('ERROR: filter-bar css not found'); sys.exit(1)
text = text.replace(OLD_CSS, NEW_CSS)

# ---------- 2) 替换 filter-bar 模板：拆出按钮区为单独一行 ----------
OLD_FILTER_HTML = (
    "+       '<div class=\"wf-filter-bar\">'\n"
    "    +         '<div class=\"wf-form-item\"><div class=\"wf-form-label\" data-i18n=\"f-name\">商家名称</div><div class=\"wf-input\" data-i18n=\"ph-name\">请输入名称关键词</div></div>'\n"
    "    +         '<div class=\"wf-form-item w120\"><div class=\"wf-form-label\" data-i18n=\"f-type\">商家类型</div><div class=\"wf-select\" data-i18n=\"all\">全部</div></div>'\n"
    "    +         '<div class=\"wf-form-item w120\"><div class=\"wf-form-label\" data-i18n=\"f-status\">商家状态</div><div class=\"wf-select\" data-i18n=\"all\">全部</div></div>'\n"
    "    +         '<div class=\"wf-form-item w120\"><div class=\"wf-form-label\" data-i18n=\"f-auth\">认证状态</div><div class=\"wf-select\" data-i18n=\"all\">全部</div></div>'\n"
    "    +         '<div class=\"wf-form-item\"><div class=\"wf-form-label\" data-i18n=\"f-sales\">所属销售（仅管理员）</div><div class=\"wf-select\" data-i18n=\"all\">全部</div></div>'\n"
    "    +         '<div class=\"wf-form-item\" style=\"flex:none;width:auto;\"><div class=\"wf-form-label\">&nbsp;</div><div style=\"display:flex;gap:4px;\"><button class=\"wf-btn wf-btn-primary\" data-i18n=\"search\">🔍 查询</button><button class=\"wf-btn\" data-i18n=\"reset\">↺ 重置</button></div></div>'\n"
    "    +       '</div>'\n"
)
NEW_FILTER_HTML = (
    "+       '<div class=\"wf-filter-bar\">'\n"
    "    +         '<div class=\"wf-form-item\"><div class=\"wf-form-label\" data-i18n=\"f-name\">商家名称</div><div class=\"wf-input\" data-i18n=\"ph-name\">请输入名称关键词</div></div>'\n"
    "    +         '<div class=\"wf-form-item\"><div class=\"wf-form-label\" data-i18n=\"f-type\">商家类型</div><div class=\"wf-select\" data-i18n=\"all\">全部</div></div>'\n"
    "    +         '<div class=\"wf-form-item\"><div class=\"wf-form-label\" data-i18n=\"f-status\">商家状态</div><div class=\"wf-select\" data-i18n=\"all\">全部</div></div>'\n"
    "    +         '<div class=\"wf-form-item\"><div class=\"wf-form-label\" data-i18n=\"f-auth\">认证状态</div><div class=\"wf-select\" data-i18n=\"all\">全部</div></div>'\n"
    "    +         '<div class=\"wf-form-item\"><div class=\"wf-form-label\" data-i18n=\"f-owner\">维护人</div><div class=\"wf-select\" data-i18n=\"all\">全部</div></div>'\n"
    "    +       '</div>'\n"
    "    +       '<div class=\"wf-filter-hint\" data-i18n=\"f-hint\">维护人筛选仅管理员可见；销售自动锁定为本人。</div>'\n"
    "    +       '<div class=\"wf-filter-actions\">'\n"
    "    +         '<button class=\"wf-btn\" data-i18n=\"reset\">↺ 重置</button>'\n"
    "    +         '<button class=\"wf-btn wf-btn-primary\" data-i18n=\"search\">🔍 查询</button>'\n"
    "    +       '</div>'\n"
)
if OLD_FILTER_HTML not in text:
    print('ERROR: filter html not found'); sys.exit(1)
text = text.replace(OLD_FILTER_HTML, NEW_FILTER_HTML)

# ---------- 3) 表头：去掉 联系方式 列；所属销售 → 维护人 ----------
OLD_THEAD = (
    "+             '<th style=\"width:50px;\">ID</th>'\n"
    "    +             '<th data-i18n=\"th-name\">商家名称</th>'\n"
    "    +             '<th style=\"width:60px;\" data-i18n=\"th-type\">类型</th>'\n"
    "    +             '<th style=\"width:70px;\" data-i18n=\"th-status\">商家状态</th>'\n"
    "    +             '<th style=\"width:90px;\" data-i18n=\"th-auth\">认证状态</th>'\n"
    "    +             '<th style=\"width:140px;\" data-i18n=\"th-phone\">联系方式</th>'\n"
    "    +             '<th style=\"width:80px;\" data-i18n=\"th-sales\">所属销售</th>'\n"
    "    +             '<th style=\"width:90px;\" data-i18n=\"th-time\">创建时间</th>'\n"
    "    +             '<th style=\"width:110px;\" data-i18n=\"th-op\">操作</th>'\n"
)
NEW_THEAD = (
    "+             '<th style=\"width:50px;\">ID</th>'\n"
    "    +             '<th data-i18n=\"th-name\">商家名称</th>'\n"
    "    +             '<th style=\"width:60px;\" data-i18n=\"th-type\">类型</th>'\n"
    "    +             '<th style=\"width:70px;\" data-i18n=\"th-status\">商家状态</th>'\n"
    "    +             '<th style=\"width:90px;\" data-i18n=\"th-auth\">认证状态</th>'\n"
    "    +             '<th style=\"width:160px;\" data-i18n=\"th-owner\">维护人</th>'\n"
    "    +             '<th style=\"width:90px;\" data-i18n=\"th-time\">创建时间</th>'\n"
    "    +             '<th style=\"width:110px;\" data-i18n=\"th-op\">操作</th>'\n"
)
if OLD_THEAD not in text:
    print('ERROR: thead not found'); sys.exit(1)
text = text.replace(OLD_THEAD, NEW_THEAD)

# ---------- 4) listRow 调用：移除 phone 实参，sales 改写为 姓名（工号） ----------
OLD_CALLS = (
    "+             listRow('1001','HK Mobile Trade Co.','buyer','active','authed','+852 9123 4567','张三','2026-04-10')\n"
    "    +             listRow('1002','Macau Phones Ltd.','seller','active','authed','+853 6234 5678','李四','2026-04-12')\n"
    "    +             listRow('1003','SG Recycle Hub','buyer','inactive','restricted','+65 8345 6789','—','2026-04-15')\n"
    "    +             listRow('1004','TW Digital Trade','seller','active','unauthed','+886 912 345678','张三','2026-04-08')\n"
    "    +             listRow('1005','JP Phone Market','buyer','active','authed','+81 80 1234 5678','王五','2026-04-06')\n"
)
NEW_CALLS = (
    "+             listRow('1001','HK Mobile Trade Co.','buyer','active','authed','张三','OB1001','2026-04-10')\n"
    "    +             listRow('1002','Macau Phones Ltd.','seller','active','authed','李四','OB1002','2026-04-12')\n"
    "    +             listRow('1003','SG Recycle Hub','buyer','inactive','restricted','—','','2026-04-15')\n"
    "    +             listRow('1004','TW Digital Trade','seller','active','unauthed','张三','OB1001','2026-04-08')\n"
    "    +             listRow('1005','JP Phone Market','buyer','active','authed','王五','OB1003','2026-04-06')\n"
)
if OLD_CALLS not in text:
    print('ERROR: listRow calls not found'); sys.exit(1)
text = text.replace(OLD_CALLS, NEW_CALLS)

# ---------- 5) listRow 函数：签名 (id, name, type, status, authStatus, owner, ownerCode, time) ----------
OLD_FN = '''  function listRow(id, name, type, status, authStatus, phone, sales, time){
    var typeTag = type==='buyer' ? 'wf-tag-cyan' : 'wf-tag-purple';
    var typeKey = type==='buyer' ? 't-buyer' : 't-seller';
    var statusTag = status==='active' ? 'wf-tag-green' : 'wf-tag-default';
    var statusKey = status==='active' ? 's-active' : 's-inactive';
    var authTagMap = { authed:'wf-tag-green', unauthed:'wf-tag-default', restricted:'wf-tag-orange' };
    var authKeyMap = { authed:'a-authed', unauthed:'a-unauthed', restricted:'a-restricted' };
    var authTag = authTagMap[authStatus] || 'wf-tag-default';
    var authKey = authKeyMap[authStatus] || 'a-unauthed';
    var salesCell = sales==='—'
      ? '<span style="color:#BFBFBF;" data-i18n="unassigned">未分配</span>'
      : sales;
    return '<tr>'
      + '<td>' + id + '</td>'
      + '<td style="font-weight:500;color:#262626;">' + name + '</td>'
      + '<td><span class="wf-tag ' + typeTag + '" data-i18n="' + typeKey + '"></span></td>'
      + '<td><span class="wf-tag ' + statusTag + '" data-i18n="' + statusKey + '"></span></td>'
      + '<td><span class="wf-tag ' + authTag + '" data-i18n="' + authKey + '"></span></td>'
      + '<td>' + phone + '</td>'
      + '<td>' + salesCell + '</td>'
      + '<td style="font-size:10px;color:#8C8C8C;">' + time + '</td>'
      + '<td>'
      +   '<button class="wf-btn-link" data-go-view="detail" data-merchant-id="' + id + '" data-merchant-name="' + name + '" data-merchant-type="' + type + '" data-merchant-auth="' + authStatus + '" data-i18n="view">查看</button> '
      +   '<button class="wf-btn-link" data-i18n="edit">编辑</button>'
      + '</td>'
      + '</tr>';
  }
'''
NEW_FN = '''  function listRow(id, name, type, status, authStatus, owner, ownerCode, time){
    var typeTag = type==='buyer' ? 'wf-tag-cyan' : 'wf-tag-purple';
    var typeKey = type==='buyer' ? 't-buyer' : 't-seller';
    var statusTag = status==='active' ? 'wf-tag-green' : 'wf-tag-default';
    var statusKey = status==='active' ? 's-active' : 's-inactive';
    var authTagMap = { authed:'wf-tag-green', unauthed:'wf-tag-default', restricted:'wf-tag-orange' };
    var authKeyMap = { authed:'a-authed', unauthed:'a-unauthed', restricted:'a-restricted' };
    var authTag = authTagMap[authStatus] || 'wf-tag-default';
    var authKey = authKeyMap[authStatus] || 'a-unauthed';
    var ownerCell = owner === '—'
      ? '<span style="color:#BFBFBF;" data-i18n="unassigned">未分配</span>'
      : (owner + (ownerCode ? '<span style="color:#8C8C8C;font-size:10px;margin-left:4px;">(' + ownerCode + ')</span>' : ''));
    return '<tr>'
      + '<td>' + id + '</td>'
      + '<td style="font-weight:500;color:#262626;">' + name + '</td>'
      + '<td><span class="wf-tag ' + typeTag + '" data-i18n="' + typeKey + '"></span></td>'
      + '<td><span class="wf-tag ' + statusTag + '" data-i18n="' + statusKey + '"></span></td>'
      + '<td><span class="wf-tag ' + authTag + '" data-i18n="' + authKey + '"></span></td>'
      + '<td>' + ownerCell + '</td>'
      + '<td style="font-size:10px;color:#8C8C8C;">' + time + '</td>'
      + '<td>'
      +   '<button class="wf-btn-link" data-go-view="detail" data-merchant-id="' + id + '" data-merchant-name="' + name + '" data-merchant-type="' + type + '" data-merchant-auth="' + authStatus + '" data-i18n="view">查看</button> '
      +   '<button class="wf-btn-link" data-i18n="edit">编辑</button>'
      + '</td>'
      + '</tr>';
  }
'''
if OLD_FN not in text:
    print('ERROR: listRow fn not found'); sys.exit(1)
text = text.replace(OLD_FN, NEW_FN)

# ---------- 6) i18n 字典：新增 / 改写 ----------
# 6.1 改 f-sales 文案为「维护人」
text = text.replace(
    "    'f-sales':['所属销售（仅管理员）','Sales Owner (Admin)'],",
    "    'f-sales':['维护人（仅管理员）','Account Owner (Admin)'],"
)
# 6.2 新增 f-owner / th-owner / f-hint
text = text.replace(
    "    'th-status':['商家状态','Merchant Status'],",
    (
        "    'th-status':['商家状态','Merchant Status'],\n"
        "    'f-owner':['维护人','Account Owner'],\n"
        "    'th-owner':['维护人','Account Owner'],\n"
        "    'f-hint':['维护人筛选仅管理员可见；销售自动锁定为本人。','Owner filter is admin-only; sales reps see only their own merchants.'],"
    )
)
# 6.3 删除原有 th-phone 字典项（不再使用，避免误用）— 仅在没有其他引用时安全删除
# 我们只是把列删了，i18n key 留着不会有副作用，跳过删除以降风险

# ---------- 7) 版本记录 V2.8 ----------
V27_KEY = '<tr><td>2026-04-28</td><td>V2.7 列表与原型精修'
V28_ROW = '<tr><td>2026-04-29</td><td>V2.8 列表筛选 / 字段精修：① 筛选区改为 <strong>grid 自适应布局</strong>（最小列 190px），label <code>nowrap</code> 防错行；查询/重置按钮独立成行右对齐，过长 label 「(仅管理员)」迁移到行尾 hint 提示；② 列表去掉<strong>「联系方式」</strong>列；③ <strong>「所属销售」→「维护人」</strong>，单元格展示「姓名（工号）」，未分配显示灰字「未分配」。</td><td style="position: relative;">乔谦</td></tr>\n      '
if V27_KEY not in text:
    print('ERROR: V2.7 row missing'); sys.exit(1)
text = text.replace(V27_KEY, V28_ROW + V27_KEY)

PRD.write_text(text, encoding='utf-8')
print('Done. lines:', text.count('\n'))
