#!/usr/bin/env python3
"""
V2.7 改造：
  1) 列表列重整：去掉「联系人」；拆分「状态」=「商家状态」+「认证状态」（已认证 / 未认证 / 账号受限）
     筛选区也对应新增「认证状态」下拉。
  2) 三页各只保留一张交互图：
        删除「商家列表页」内的旧静态深色 mockup（含 dark theme 顶栏 + 静态表格 + 静态分页）
        删除「添加商家页」内的旧静态 mockup（标题为「Mockup: 添加商家 — 单页（无分步）」）
  3) 原型比例变扁：shell height 从 clamp(720,90vh,980) → clamp(560px, 65vh, 720px)
     侧边菜单宽度从 200px → 220px（贴近截图）
  4) 商家详情页头部 → Tab 紧凑：head card margin-bottom:6px；wf-page padding 调小，
     wf-tabs 内边距 0；panel 区 wf-page padding-top:10px
  5) 排查并消除潜在 NaN：在原型 JS 里所有读取 contenteditable 数字的位置加 Number.isFinite 兜底，
     拼接消息时若 deposit/limit 为 NaN，直接显示 0；版本记录 V2.7。
"""
from pathlib import Path
import sys, re

PRD = Path('/Users/qiaoqian/clawd-on-desk/FoneSquare-PRD-v2.html')
text = PRD.read_text(encoding='utf-8')

# ---------- 1) 删除列表页静态 mockup（line 3214 起，深色顶栏 + 静态表格 + 静态分页） ----------
LIST_MOCKUP_HEAD = "  <!-- Mockup: 商家列表页 -->\n"
LIST_MOCKUP_TAIL = "  <h4>列表字段规格</h4>"
i = text.find(LIST_MOCKUP_HEAD)
j = text.find(LIST_MOCKUP_TAIL, i if i >= 0 else 0)
if i < 0 or j < 0:
    print('ERROR: 列表页静态 Mockup 边界未找到'); sys.exit(1)
text = text[:i] + text[j:]
print('removed list-page legacy mockup, chars:', j - i)

# ---------- 2) 删除添加商家页静态 mockup ----------
ADD_MOCKUP_HEAD = "  <!-- Mockup: 添加商家 — 单页（无分步） -->\n"
ADD_MOCKUP_TAIL = "  <!-- ===== 三、添加商家字段规格 ===== -->"
i = text.find(ADD_MOCKUP_HEAD)
j = text.find(ADD_MOCKUP_TAIL, i if i >= 0 else 0)
if i < 0 or j < 0:
    print('ERROR: 添加页静态 Mockup 边界未找到'); sys.exit(1)
text = text[:i] + text[j:]
print('removed add-page legacy mockup, chars:', j - i)

# ---------- 3) 比例变扁 + 侧边菜单加宽 ----------
text = text.replace(
    ".wf-prototype-shell { width:100%; height:clamp(720px, 90vh, 980px);",
    ".wf-prototype-shell { width:100%; aspect-ratio:16/10; height:auto; max-height:760px; min-height:520px;"
)
text = text.replace(
    ".wf-prototype-shell .wf-sider { width:200px;",
    ".wf-prototype-shell .wf-sider { width:220px;"
)

# ---------- 4) 详情头部 → Tab 紧凑（修改 detailView 函数里的 padding/margin） ----------
text = text.replace(
    "'<div class=\"wf-view\" data-view=\"detail\">'\n    + '<div class=\"wf-page\" style=\"padding-bottom:0;\">'",
    "'<div class=\"wf-view\" data-view=\"detail\">'\n    + '<div class=\"wf-page\" style=\"padding:14px 20px 6px;\">'"
)
text = text.replace(
    "+ '<div class=\"wf-card\"><div class=\"wf-card-body\" style=\"display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;\">'",
    "+ '<div class=\"wf-card\" style=\"margin-bottom:0;\"><div class=\"wf-card-body\" style=\"display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;padding:10px 14px;\">'"
)
text = text.replace(
    "+   '<div class=\"wf-page\" style=\"padding-top:14px;\">'\n    +     panelBasic()",
    "+   '<div class=\"wf-page\" style=\"padding:10px 20px 16px;\">'\n    +     panelBasic()"
)

# ---------- 5) 列表列重整 + 状态拆分 + 认证状态筛选 + listRow 数据新增字段 ----------

# 5.1 替换 listView 中的 filter-bar：把单个「状态」改为两个；filter 区按钮排版略调
OLD_FILTER = (
    "+         '<div class=\"wf-form-item w120\"><div class=\"wf-form-label\" data-i18n=\"f-type\">商家类型</div><div class=\"wf-select\" data-i18n=\"all\">全部</div></div>'\n"
    "    +         '<div class=\"wf-form-item w120\"><div class=\"wf-form-label\" data-i18n=\"f-status\">状态</div><div class=\"wf-select\" data-i18n=\"all\">全部</div></div>'\n"
    "    +         '<div class=\"wf-form-item\"><div class=\"wf-form-label\" data-i18n=\"f-sales\">所属销售（仅管理员）</div><div class=\"wf-select\" data-i18n=\"all\">全部</div></div>'\n"
)
NEW_FILTER = (
    "+         '<div class=\"wf-form-item w120\"><div class=\"wf-form-label\" data-i18n=\"f-type\">商家类型</div><div class=\"wf-select\" data-i18n=\"all\">全部</div></div>'\n"
    "    +         '<div class=\"wf-form-item w120\"><div class=\"wf-form-label\" data-i18n=\"f-status\">商家状态</div><div class=\"wf-select\" data-i18n=\"all\">全部</div></div>'\n"
    "    +         '<div class=\"wf-form-item w120\"><div class=\"wf-form-label\" data-i18n=\"f-auth\">认证状态</div><div class=\"wf-select\" data-i18n=\"all\">全部</div></div>'\n"
    "    +         '<div class=\"wf-form-item\"><div class=\"wf-form-label\" data-i18n=\"f-sales\">所属销售（仅管理员）</div><div class=\"wf-select\" data-i18n=\"all\">全部</div></div>'\n"
)
if OLD_FILTER not in text:
    print('ERROR: list filter bar block not found'); sys.exit(1)
text = text.replace(OLD_FILTER, NEW_FILTER)

# 5.2 替换 listView 表头：去掉「联系人」；拆分「状态」=「商家状态」+「认证状态」
OLD_THEAD = (
    "+           '<thead><tr>'\n"
    "    +             '<th style=\"width:50px;\">ID</th>'\n"
    "    +             '<th data-i18n=\"th-name\">商家名称</th>'\n"
    "    +             '<th style=\"width:60px;\" data-i18n=\"th-type\">类型</th>'\n"
    "    +             '<th style=\"width:60px;\" data-i18n=\"th-status\">状态</th>'\n"
    "    +             '<th style=\"width:80px;\" data-i18n=\"th-contact\">联系人</th>'\n"
    "    +             '<th style=\"width:140px;\" data-i18n=\"th-phone\">联系方式</th>'\n"
    "    +             '<th style=\"width:80px;\" data-i18n=\"th-sales\">所属销售</th>'\n"
    "    +             '<th style=\"width:90px;\" data-i18n=\"th-time\">创建时间</th>'\n"
    "    +             '<th style=\"width:120px;\" data-i18n=\"th-op\">操作</th>'\n"
    "    +           '</tr></thead>'\n"
)
NEW_THEAD = (
    "+           '<thead><tr>'\n"
    "    +             '<th style=\"width:50px;\">ID</th>'\n"
    "    +             '<th data-i18n=\"th-name\">商家名称</th>'\n"
    "    +             '<th style=\"width:60px;\" data-i18n=\"th-type\">类型</th>'\n"
    "    +             '<th style=\"width:70px;\" data-i18n=\"th-status\">商家状态</th>'\n"
    "    +             '<th style=\"width:90px;\" data-i18n=\"th-auth\">认证状态</th>'\n"
    "    +             '<th style=\"width:140px;\" data-i18n=\"th-phone\">联系方式</th>'\n"
    "    +             '<th style=\"width:80px;\" data-i18n=\"th-sales\">所属销售</th>'\n"
    "    +             '<th style=\"width:90px;\" data-i18n=\"th-time\">创建时间</th>'\n"
    "    +             '<th style=\"width:110px;\" data-i18n=\"th-op\">操作</th>'\n"
    "    +           '</tr></thead>'\n"
)
if OLD_THEAD not in text:
    print('ERROR: list thead block not found'); sys.exit(1)
text = text.replace(OLD_THEAD, NEW_THEAD)

# 5.3 替换 listView 表体调用：旧 listRow 5 行 → 新 listRow（去掉 contact，加 authStatus）
OLD_TBODY = (
    "+             listRow('1001','HK Mobile Trade Co.','buyer','active','陈先生','+852 9123 4567','张三','2026-04-10')\n"
    "    +             + listRow('1002','Macau Phones Ltd.','seller','active','李小姐','+853 6234 5678','李四','2026-04-12')\n"
    "    +             + listRow('1003','SG Recycle Hub','buyer','inactive','王先生','+65 8345 6789','—','2026-04-15')\n"
    "    +             + listRow('1004','TW Digital Trade','seller','active','林先生','+886 912 345678','张三','2026-04-08')\n"
    "    +             + listRow('1005','JP Phone Market','buyer','active','田中','+81 80 1234 5678','王五','2026-04-06')\n"
)
NEW_TBODY = (
    "+             listRow('1001','HK Mobile Trade Co.','buyer','active','authed','+852 9123 4567','张三','2026-04-10')\n"
    "    +             + listRow('1002','Macau Phones Ltd.','seller','active','authed','+853 6234 5678','李四','2026-04-12')\n"
    "    +             + listRow('1003','SG Recycle Hub','buyer','inactive','restricted','+65 8345 6789','—','2026-04-15')\n"
    "    +             + listRow('1004','TW Digital Trade','seller','active','unauthed','+886 912 345678','张三','2026-04-08')\n"
    "    +             + listRow('1005','JP Phone Market','buyer','active','authed','+81 80 1234 5678','王五','2026-04-06')\n"
)
if OLD_TBODY not in text:
    print('ERROR: list tbody calls not found'); sys.exit(1)
text = text.replace(OLD_TBODY, NEW_TBODY)

# 5.4 替换 listRow 函数体：参数签名 (id,name,type,status,authStatus,phone,sales,time) + 新单元格
OLD_LISTROW = '''  function listRow(id, name, type, status, contact, phone, sales, time){
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
'''
NEW_LISTROW = '''  function listRow(id, name, type, status, authStatus, phone, sales, time){
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
if OLD_LISTROW not in text:
    print('ERROR: listRow function body not found'); sys.exit(1)
text = text.replace(OLD_LISTROW, NEW_LISTROW)

# 5.5 详情页头部去掉 contact 透传，新增 authStatus 显示在头部 Tag
OLD_DETAIL_HEAD_TPL = '''        '<div style="font-size:15px;font-weight:600;color:#262626;">'
    +           '<span data-bind="dName">HK Mobile Trade Co.</span> '
    +           '<span class="wf-tag wf-tag-cyan" data-bind="dType" data-i18n="t-buyer" style="margin-left:6px;">买家</span> '
    +           '<span class="wf-tag wf-tag-green" data-i18n="s-active">使用</span>'
    +         '</div>'
'''
NEW_DETAIL_HEAD_TPL = '''        '<div style="font-size:15px;font-weight:600;color:#262626;display:flex;align-items:center;flex-wrap:wrap;gap:6px;">'
    +           '<span data-bind="dName">HK Mobile Trade Co.</span>'
    +           '<span class="wf-tag wf-tag-cyan" data-bind="dType" data-i18n="t-buyer">买家</span>'
    +           '<span class="wf-tag wf-tag-green" data-i18n="s-active">使用</span>'
    +           '<span class="wf-tag wf-tag-green" data-bind="dAuth" data-i18n="a-authed">已认证</span>'
    +         '</div>'
'''
if OLD_DETAIL_HEAD_TPL not in text:
    print('ERROR: detail head template not found'); sys.exit(1)
text = text.replace(OLD_DETAIL_HEAD_TPL, NEW_DETAIL_HEAD_TPL)

# 5.6 在「视图切换 detail 处理」中新增 dAuth 同步
OLD_DETAIL_BIND = '''            dType.setAttribute('data-i18n', typeKey);
            dType.textContent = I18N[typeKey][state.lang==='zh'?0:1];
          }'''
NEW_DETAIL_BIND = '''            dType.setAttribute('data-i18n', typeKey);
            dType.textContent = I18N[typeKey][state.lang==='zh'?0:1];
            var mauth = goBtn.dataset.merchantAuth;
            var dAuth = root.querySelector('[data-bind="dAuth"]');
            if (mauth && dAuth){
              var authTagMap = { authed:'wf-tag-green', unauthed:'wf-tag-default', restricted:'wf-tag-orange' };
              var authKeyMap = { authed:'a-authed', unauthed:'a-unauthed', restricted:'a-restricted' };
              var aTag = authTagMap[mauth] || 'wf-tag-default';
              var aKey = authKeyMap[mauth] || 'a-unauthed';
              dAuth.className = 'wf-tag ' + aTag;
              dAuth.setAttribute('data-i18n', aKey);
              dAuth.textContent = I18N[aKey][state.lang==='zh'?0:1];
            }
          }'''
if OLD_DETAIL_BIND not in text:
    print('ERROR: detail goBtn bind block not found'); sys.exit(1)
text = text.replace(OLD_DETAIL_BIND, NEW_DETAIL_BIND)

# 5.7 i18n 字典补条目：商家状态 / 认证状态 / 认证三状态文案
OLD_I18N_INSERT = "    'th-status':['状态','Status'],"
NEW_I18N_INSERT = (
    "    'th-status':['商家状态','Merchant Status'],\n"
    "    'th-auth':['认证状态','Auth Status'],\n"
    "    'a-authed':['已认证','Verified'],\n"
    "    'a-unauthed':['未认证','Unverified'],\n"
    "    'a-restricted':['账号受限','Restricted'],\n"
    "    'f-auth':['认证状态','Auth Status'],"
)
if OLD_I18N_INSERT not in text:
    print('ERROR: i18n th-status not found'); sys.exit(1)
text = text.replace(OLD_I18N_INSERT, NEW_I18N_INSERT)

# 同时把 f-status 中文从「状态」改为「商家状态」
text = text.replace(
    "    'f-status':['状态','Status'],",
    "    'f-status':['商家状态','Merchant Status'],"
)

# ---------- NaN 兜底 ----------
# 现有 parseInt(... || '0') 已有 || 0 兜底；为防止 length=0 字符串 parseInt 返回 NaN，再加 isFinite 校验
OLD_QSAVE = '''        var DEFAULT_MIN = 1000;
        var limit = parseInt((root.querySelector('[data-bind="qInputLimit"]').textContent || '0').replace(/[^0-9]/g, ''), 10) || 0;
        var deposit = parseInt((root.querySelector('[data-bind="qInputDeposit"]').textContent || '0').replace(/[^0-9]/g, ''), 10) || 0;'''
NEW_QSAVE = '''        var DEFAULT_MIN = 1000;
        function readInt(sel){
          var el = root.querySelector(sel);
          if (!el) return 0;
          var raw = (el.textContent || '').replace(/[^0-9]/g, '');
          var n = raw ? parseInt(raw, 10) : 0;
          return Number.isFinite(n) ? n : 0;
        }
        var limit = readInt('[data-bind="qInputLimit"]');
        var deposit = readInt('[data-bind="qInputDeposit"]');'''
if OLD_QSAVE not in text:
    print('ERROR: qSave parseInt block not found'); sys.exit(1)
text = text.replace(OLD_QSAVE, NEW_QSAVE)

# ---------- 版本记录 V2.7 ----------
V26_LINE_KEY = '<tr><td>2026-04-28</td><td>V2.6 后台原型菜单回归'
if V26_LINE_KEY not in text:
    print('ERROR: V2.6 row missing'); sys.exit(1)
V27_ROW = '<tr><td>2026-04-28</td><td>V2.7 列表与原型精修：① 状态拆分为<strong>「商家状态」</strong>（使用/停用）+ <strong>「认证状态」</strong>（已认证 / 未认证 / 账号受限）双列双筛选；② 列表去掉<strong>「联系人」</strong>列；③ 三页各只保留一张交互图，删除「商家列表 / 添加商家」页旧静态深色 mockup；④ 原型容器比例变扁（aspect-ratio 16:10，max-height 760px），侧边菜单宽度 200 → 220px；⑤ 商家详情页头部 → Tab 紧凑（head card 0 margin、wf-page padding 收紧），头部新增「认证状态」Tag；⑥ 限额/保证金校验函数加 <code>Number.isFinite</code> 兜底，杜绝因空文本拼接出现的 NaN。</td><td style="position: relative;">乔谦</td></tr>\n      '
text = text.replace(V26_LINE_KEY, V27_ROW + V26_LINE_KEY)

PRD.write_text(text, encoding='utf-8')
print('Done. lines:', text.count('\n'))
