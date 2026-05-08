#!/usr/bin/env python3
"""
V2.9 改造：
  1) 列表操作列：删「编辑」，改为「查看 + 停用/启用」（按 status 动态显示）。
  2) 详情头部信息卡：第二行改为「ID · 维护人：姓名(OB号) · 注册日期：YYYY-MM-DD」；
     右侧操作按钮保留「编辑信息」+「停用/启用」（保留现有，文案已合规）。
  3) Tab 4 改名「销售绑定」→「维护人绑定」（仅文案，data-tab 保留 sales）。
  4) Tab 1 基本信息重构：个人信息卡（姓名/手机号/邮箱/WhatsApp/地区/备注）
     + 企业信息卡（企业名称/营业执照号 — 选填）；卡内右上角「编辑」按钮（演示）。
  5) Tab 2 KYC 重构：个人 KYC 卡（证件类型/号/姓名/有效期/照片）
     + 企业 KYC 卡（企业名称/证照类型/证照编号/法定代表/企业地址/证照有效期/证照照片 — 选填）；
     卡内「编辑」按钮（与脱敏号「点击查看」按钮）。
  6) Tab 4 panelSales 重构为「维护人绑定」：当前绑定（姓名/OB账号/绑定时间/操作人）
     + 绑定/解绑/更换 + 历史绑定列表。
  7) Tab 5 操作日志：新增日志条目（创建/KYC审核/限额修改/绑定变更/停用启用），
     带操作人 / 操作时间 / 变更前后值。
  8) i18n 字典批量补全。
"""
from pathlib import Path
import sys, re

PRD = Path('/Users/qiaoqian/clawd-on-desk/FoneSquare-PRD-v2.html')
text = PRD.read_text(encoding='utf-8')

# ============ 1) listRow：去掉编辑，新增停用/启用 ============
OLD = '''  function listRow(id, name, type, status, authStatus, owner, ownerCode, time){
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
NEW = '''  function listRow(id, name, type, status, authStatus, owner, ownerCode, time){
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
    var toggleKey = status==='active' ? 'op-disable' : 'op-enable';
    var toggleTxt = status==='active' ? '停用' : '启用';
    var toggleColor = status==='active' ? '#FA8C16' : '#52C41A';
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
      +   '<button class="wf-btn-link" data-act="toggleStatus" data-merchant-id="' + id + '" data-status="' + status + '" data-i18n="' + toggleKey + '" style="color:' + toggleColor + ';">' + toggleTxt + '</button>'
      + '</td>'
      + '</tr>';
  }
'''
if OLD not in text:
    print('ERROR: listRow function not found'); sys.exit(1)
text = text.replace(OLD, NEW)

# ============ 2) 详情头部第二行：所属销售/入驻日期 → 维护人(OB号) / 注册日期 ============
OLD = '''+         '<div style="font-size:11px;color:#8C8C8C;margin-top:4px;">'
    +           '<span data-i18n="d-mid">商家 ID</span>：<span data-bind="dMid2">1001</span> · '
    +           '<span data-i18n="d-sales">所属销售</span>：张三 · '
    +           '<span data-i18n="d-since">入驻日期</span>：2026-04-10'
    +         '</div>'
'''
NEW = '''+         '<div style="font-size:11px;color:#8C8C8C;margin-top:4px;">'
    +           '<span data-i18n="d-mid">商家 ID</span>：<span data-bind="dMid2">1001</span> · '
    +           '<span data-i18n="d-owner">维护人</span>：<span data-bind="dOwner">张三</span> <span style="color:#BFBFBF;" data-bind="dOwnerCode">(OB1001)</span> · '
    +           '<span data-i18n="d-since">注册日期</span>：<span data-bind="dSince">2026-04-10</span>'
    +         '</div>'
'''
if OLD not in text:
    print('ERROR: detail head subtitle not found'); sys.exit(1)
text = text.replace(OLD, NEW)

# 同步 i18n d-since 文案
text = text.replace(
    "    'd-since':['入驻日期','Joined'],",
    "    'd-since':['注册日期','Registered'],"
)

# ============ 3) Tab 4 文案 销售绑定 → 维护人绑定 ============
text = text.replace(
    "    'tab-sales':['销售绑定','Sales Binding'],",
    "    'tab-sales':['维护人绑定','Owner Binding'],"
)
text = text.replace(
    "    'p-sales':['销售绑定','Sales Binding'],",
    "    'p-sales':['维护人绑定','Owner Binding'],"
)

# ============ 4) panelBasic 整体重写：个人信息 + 企业信息（选填）+ 卡右上角编辑按钮 ============
OLD = '''  function panelBasic(){
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
'''
NEW = '''  function panelBasic(){
    return '<div class="wf-tab-panel active" data-panel="basic">'
      + '<div class="wf-card">'
      +   '<div class="wf-card-head"><span data-i18n="p-basic-personal">个人信息</span>'
      +     '<button class="wf-btn-link wf-card-edit" data-act="editBasic" data-i18n="edit">编辑</button>'
      +   '</div>'
      +   '<div class="wf-card-body">'
      +     descRow('b-personal-name','姓名','陈大文')
      +     descRow('b-phone','手机号','+852 9123 4567')
      +     descRow('b-email','邮箱','chen@hkmobile.com')
      +     descRow('b-whatsapp','WhatsApp','+852 9123 4567')
      +     '<div class="wf-desc-row"><div class="wf-desc-label" data-i18n="b-region">地区</div><div class="wf-desc-value" data-i18n="region-hk">香港</div></div>'
      +     descRow('b-remark','备注','—')
      +   '</div>'
      + '</div>'
      + '<div class="wf-card">'
      +   '<div class="wf-card-head">'
      +     '<span><span data-i18n="p-basic-corp">企业信息</span> <span class="wf-card-optional" data-i18n="optional">选填</span></span>'
      +     '<button class="wf-btn-link wf-card-edit" data-act="editBasicCorp" data-i18n="edit">编辑</button>'
      +   '</div>'
      +   '<div class="wf-card-body">'
      +     descRow('b-corp-name','企业名称','—')
      +     descRow('b-corp-license','营业执照号','—')
      +   '</div>'
      + '</div>'
      + '</div>';
  }
'''
if OLD not in text:
    print('ERROR: panelBasic not found'); sys.exit(1)
text = text.replace(OLD, NEW)

# ============ 5) panelKyc 整体重写：个人 KYC + 企业 KYC（选填） ============
OLD = '''  function panelKyc(){
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
'''
NEW = '''  function panelKyc(){
    return '<div class="wf-tab-panel" data-panel="kyc">'
      + '<div class="wf-card">'
      +   '<div class="wf-card-head"><span data-i18n="p-kyc-personal">个人 KYC 材料</span>'
      +     '<button class="wf-btn-link wf-card-edit" data-act="editKyc" data-i18n="edit">编辑</button>'
      +   '</div>'
      +   '<div class="wf-card-body">'
      +     descRow('k-doc','证件类型','HK ID')
      +     '<div class="wf-desc-row"><div class="wf-desc-label" data-i18n="k-num">证件号</div><div class="wf-desc-value"><span data-bind="kNumMask">A***456(7)</span> <button class="wf-btn-link" data-act="kViewRaw" data-i18n="k-view-raw">点击查看原值</button></div></div>'
      +     descRow('k-name','证件姓名','陈* 文')
      +     descRow('k-valid','有效期','2030-08-15')
      +     '<div class="wf-desc-row"><div class="wf-desc-label" data-i18n="k-photos">证件照片</div><div class="wf-desc-value"><span data-i18n="k-front">正面</span> 📷 / <span data-i18n="k-back">背面</span> 📷 <span style="color:#BFBFBF;font-size:10px;" data-i18n="k-photo-hint">（护照仅一面）</span></div></div>'
      +     '<div class="wf-desc-row"><div class="wf-desc-label" data-i18n="k-status">审核状态</div><div class="wf-desc-value"><span class="wf-tag wf-tag-green" data-i18n="k-passed">已通过</span> · <span style="color:#8C8C8C;font-size:10px;"><span data-i18n="k-time">审核时间</span> 2026-04-10 14:23</span></div></div>'
      +   '</div>'
      + '</div>'
      + '<div class="wf-card">'
      +   '<div class="wf-card-head">'
      +     '<span><span data-i18n="p-kyc-corp">企业 KYC 材料</span> <span class="wf-card-optional" data-i18n="optional">选填</span></span>'
      +     '<button class="wf-btn-link wf-card-edit" data-act="editKycCorp" data-i18n="edit">编辑</button>'
      +   '</div>'
      +   '<div class="wf-card-body">'
      +     descRow('kc-name','企业名称','HK Mobile Trade Co. Ltd.')
      +     descRow('kc-doc-type','证照类型','商业登记证')
      +     descRow('kc-doc-num','证照编号','BR-2024-XXXX-001')
      +     descRow('kc-rep','法定代表 / 董事','陈大文')
      +     descRow('kc-addr','企业地址','香港九龙观塘 ...')
      +     descRow('kc-valid','证照有效期','2027-01-01')
      +     '<div class="wf-desc-row"><div class="wf-desc-label" data-i18n="kc-photo">证照照片</div><div class="wf-desc-value">📷 <a href="#" onclick="return false" data-i18n="view">查看</a></div></div>'
      +   '</div>'
      + '</div>'
      + '</div>';
  }
'''
if OLD not in text:
    print('ERROR: panelKyc not found'); sys.exit(1)
text = text.replace(OLD, NEW)

# ============ 6) panelSales 重写：维护人绑定 ============
OLD = '''  function panelSales(){
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
'''
NEW = '''  function panelSales(){
    return '<div class="wf-tab-panel" data-panel="sales">'
      + '<div class="wf-card">'
      +   '<div class="wf-card-head"><span data-i18n="p-sales">维护人绑定</span></div>'
      +   '<div class="wf-card-body">'
      +     descRow('sa-current','当前维护人','张三')
      +     descRow('sa-ob','OB 账号','OB1001 (sales01@fonesquare.com)')
      +     descRow('sa-since','绑定时间','2026-04-10 14:23')
      +     descRow('sa-by','操作人','admin01')
      +     '<div style="margin-top:12px;display:flex;gap:6px;flex-wrap:wrap;">'
      +       '<button class="wf-btn wf-btn-primary" data-act="saReassign" data-i18n="sa-reassign">🔄 更换维护人</button>'
      +       '<button class="wf-btn" data-act="saUnbind" data-i18n="sa-unbind">⛔ 解绑</button>'
      +       '<button class="wf-btn" data-act="saBind" data-i18n="sa-bind">➕ 绑定</button>'
      +     '</div>'
      +     '<div data-bind="saReassignBox" style="display:none;margin-top:12px;border:1px dashed #1677FF;border-radius:6px;padding:12px;background:#F0F8FF;">'
      +       '<div class="wf-form-item"><div class="wf-form-label"><span class="req">*</span><span data-i18n="sa-new">选择新维护人</span></div><div class="wf-select" data-i18n="sa-new-ph">从 OB 销售列表选择…</div></div>'
      +       '<div class="wf-form-item"><div class="wf-form-label"><span class="req">*</span><span data-i18n="sa-reason">变更原因</span></div><div class="wf-textarea" data-i18n="sa-reason-ph">请填写变更原因（必填，将记录到操作日志）</div></div>'
      +       '<div style="display:flex;gap:6px;justify-content:flex-end;"><button class="wf-btn" data-act="saCancel" data-i18n="sa-cancel">取消</button><button class="wf-btn wf-btn-primary" data-i18n="sa-confirm">确认变更</button></div>'
      +     '</div>'
      +   '</div>'
      + '</div>'
      + '<div class="wf-card">'
      +   '<div class="wf-card-head" data-i18n="sa-history-title">历史绑定记录</div>'
      +   '<div class="wf-card-body" style="padding:0;">'
      +     '<table class="wf-table" style="min-width:0;">'
      +       '<thead><tr>'
      +         '<th data-i18n="sa-h-owner">维护人</th>'
      +         '<th data-i18n="sa-h-ob">OB 账号</th>'
      +         '<th data-i18n="sa-h-from">绑定时间</th>'
      +         '<th data-i18n="sa-h-to">解绑时间</th>'
      +         '<th data-i18n="sa-h-by">操作人</th>'
      +         '<th data-i18n="sa-h-reason">原因</th>'
      +       '</tr></thead>'
      +       '<tbody>'
      +         '<tr><td>张三</td><td>OB1001</td><td>2026-04-10 14:23</td><td>—</td><td>admin01</td><td><span style="color:#8C8C8C;" data-i18n="sa-r-create">商家创建自动绑定</span></td></tr>'
      +         '<tr><td>李四</td><td>OB1002</td><td>2026-03-01 09:00</td><td>2026-04-10 14:23</td><td>admin01</td><td data-i18n="sa-r-resign">销售离职转交</td></tr>'
      +       '</tbody>'
      +     '</table>'
      +   '</div>'
      + '</div>'
      + '</div>';
  }
'''
if OLD not in text:
    print('ERROR: panelSales not found'); sys.exit(1)
text = text.replace(OLD, NEW)

# ============ 7) panelLog：补全日志事件 ============
OLD = '''  function panelLog(){
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
'''
NEW = '''  function panelLog(){
    function logItem(time, actor, key, fallback, before, after){
      var diff = (before || after)
        ? '<div class="wf-tl-diff">'
            + (before ? '<span class="wf-tl-before">' + before + '</span>' : '')
            + (before && after ? '<span class="wf-tl-arrow"> → </span>' : '')
            + (after ? '<span class="wf-tl-after">' + after + '</span>' : '')
          + '</div>'
        : '';
      return '<div class="wf-tl-item">'
        + '<div class="wf-tl-time">' + time + '</div>'
        + '<div class="wf-tl-actor">' + actor + '</div>'
        + '<div class="wf-tl-text" data-i18n="' + key + '">' + fallback + '</div>'
        + diff
      + '</div>';
    }
    return '<div class="wf-tab-panel" data-panel="log">'
      + '<div class="wf-card"><div class="wf-card-head" data-i18n="p-log">操作日志</div><div class="wf-card-body">'
      +   '<div class="wf-timeline">'
      +     logItem('2026-04-10 14:23','admin01','lg-create','创建商家 HK Mobile Trade Co.（自动绑定维护人：张三 / OB1001）','','')
      +     logItem('2026-04-10 14:25','admin01','lg-kyc','完成 KYC 审核 → 已通过','待审核','已通过')
      +     logItem('2026-04-12 10:08','admin02','lg-edit-basic','编辑基本信息：手机号','+852 9000 0000','+852 9123 4567')
      +     logItem('2026-04-15 16:40','admin01','lg-quota','配置每日下单限额（保证金 5,000 已确认）','—','50,000 HKD')
      +     logItem('2026-04-18 09:15','admin01','lg-rebind','更换维护人','李四 / OB1002','张三 / OB1001')
      +     logItem('2026-04-20 11:42','admin03','lg-disable','停用商家','使用','停用')
      +     logItem('2026-04-22 10:01','admin03','lg-enable','启用商家','停用','使用')
      +   '</div>'
      + '</div></div></div>';
  }
'''
if OLD not in text:
    print('ERROR: panelLog not found'); sys.exit(1)
text = text.replace(OLD, NEW)

# ============ 8) i18n 字典补全（在 'mf-empty' 之前插入大量 key） ============
OLD = "    'mf-empty':['（无文件）','(empty)']"
NEW = '''    'mf-empty':['（无文件）','(empty)'],
    'op-disable':['停用','Disable'],
    'op-enable':['启用','Enable'],
    'd-owner':['维护人','Owner'],
    'edit':['编辑','Edit'],
    'p-basic-personal':['个人信息','Personal Info'],
    'p-basic-corp':['企业信息','Corporate Info'],
    'b-personal-name':['姓名','Name'],
    'b-whatsapp':['WhatsApp','WhatsApp'],
    'b-remark':['备注','Remark'],
    'b-corp-name':['企业名称','Company Name'],
    'b-corp-license':['营业执照号','Business Reg. No.'],
    'p-kyc-personal':['个人 KYC 材料','Personal KYC'],
    'p-kyc-corp':['企业 KYC 材料','Corporate KYC'],
    'k-valid':['有效期','Valid Until'],
    'k-photos':['证件照片','ID Photos'],
    'k-photo-hint':['（护照仅一面）','(Passport: one side)'],
    'k-view-raw':['点击查看原值','View raw'],
    'kc-name':['企业名称','Company Name'],
    'kc-doc-type':['证照类型','Document Type'],
    'kc-doc-num':['证照编号','Document No.'],
    'kc-rep':['法定代表 / 董事','Legal Rep. / Director'],
    'kc-addr':['企业地址','Company Address'],
    'kc-valid':['证照有效期','Document Valid Until'],
    'kc-photo':['证照照片','Document Photo'],
    'view':['查看','View'],
    'sa-ob':['OB 账号','OB Account'],
    'sa-bind':['➕ 绑定','➕ Bind'],
    'sa-unbind':['⛔ 解绑','⛔ Unbind'],
    'sa-history-title':['历史绑定记录','Binding History'],
    'sa-h-owner':['维护人','Owner'],
    'sa-h-ob':['OB 账号','OB Account'],
    'sa-h-from':['绑定时间','Bound At'],
    'sa-h-to':['解绑时间','Unbound At'],
    'sa-h-by':['操作人','Operator'],
    'sa-h-reason':['原因','Reason'],
    'sa-r-create':['商家创建自动绑定','Auto-bound on creation'],
    'sa-r-resign':['销售离职转交','Sales resigned, transferred'],
    'lg-create':['创建商家 HK Mobile Trade Co.（自动绑定维护人：张三 / OB1001）','Created HK Mobile Trade Co. (auto-bound to Z. San / OB1001)'],
    'lg-kyc':['完成 KYC 审核 → 已通过','KYC review completed → Passed'],
    'lg-edit-basic':['编辑基本信息：手机号','Edited basic info: phone'],
    'lg-quota':['配置每日下单限额（保证金 5,000 已确认）','Set daily limit (deposit 5,000 confirmed)'],
    'lg-rebind':['更换维护人','Reassigned owner'],
    'lg-disable':['停用商家','Disabled merchant'],
    'lg-enable':['启用商家','Enabled merchant']'''
if OLD not in text:
    print('ERROR: i18n mf-empty anchor not found'); sys.exit(1)
text = text.replace(OLD, NEW)

# ============ 9) CSS 样式补充：卡片右上角编辑按钮 + 时间线增强 ============
OLD = ".wf-prototype-shell .wf-tag-default { background:#F5F5F5; color:#8C8C8C; }"
NEW = (
    ".wf-prototype-shell .wf-tag-default { background:#F5F5F5; color:#8C8C8C; }\n"
    ".wf-prototype-shell .wf-card-head { display:flex; justify-content:space-between; align-items:center; padding:8px 14px; }\n"
    ".wf-prototype-shell .wf-card-edit { padding:0 4px; font-size:11px; }\n"
    ".wf-prototype-shell .wf-card-optional { font-size:10px; color:#BFBFBF; font-weight:400; margin-left:6px; }\n"
    ".wf-prototype-shell .wf-tl-actor { font-size:10px; color:#1677FF; margin-bottom:2px; }\n"
    ".wf-prototype-shell .wf-tl-diff { margin-top:3px; font-size:10px; color:#8C8C8C; }\n"
    ".wf-prototype-shell .wf-tl-before { background:#FFF1F0; color:#CF1322; padding:0 4px; border-radius:2px; }\n"
    ".wf-prototype-shell .wf-tl-after { background:#F6FFED; color:#389E0D; padding:0 4px; border-radius:2px; }\n"
    ".wf-prototype-shell .wf-tl-arrow { color:#BFBFBF; }"
)
if OLD not in text:
    print('ERROR: tag-default css anchor not found'); sys.exit(1)
text = text.replace(OLD, NEW)

# ============ 10) 详情视图切换：写入 dOwner / dOwnerCode / dSince ============
# 在已有 detail switch 处再注入 owner / since 同步
OLD = '''            var mauth = goBtn.dataset.merchantAuth;
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
NEW = '''            var mauth = goBtn.dataset.merchantAuth;
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
# 此处保持不变（dOwner/dSince 已在 head 模板中给了静态默认值，足够演示）

# ============ 11) 版本记录 V2.9 ============
V28_KEY = '<tr><td>2026-04-29</td><td>V2.8 列表筛选 / 字段精修'
if V28_KEY not in text:
    print('ERROR: V2.8 row missing'); sys.exit(1)
V29_ROW = '<tr><td>2026-04-29</td><td>V2.9 详情页结构按 PRD 规约重塑 + 列表操作精简：① 列表操作列删「编辑」，改为<strong>「查看 + 停用/启用」</strong>（按 status 动态切换文案与色）；② 详情头部第二行采用 <strong>「ID · 维护人：姓名(OB号) · 注册日期」</strong>；③ Tab 4 名称<strong>「销售绑定 → 维护人绑定」</strong>；④ Tab 1 基本信息拆为<strong>「个人信息」+「企业信息（选填）」</strong>双卡，卡内右上角配独立<strong>「编辑」</strong>入口；⑤ Tab 2 KYC 拆为<strong>「个人 KYC」+「企业 KYC（选填）」</strong>，证件号脱敏 + 「点击查看原值」；⑥ Tab 4 重写：当前绑定（姓名/OB账号/绑定时间/操作人）+ 绑定/解绑/更换 + 历史绑定列表；⑦ Tab 5 操作日志补全 7 类事件（创建/KYC/编辑/限额/换绑/停用/启用），每条带操作人、操作时间、变更前后值（红→绿对比）。</td><td style="position: relative;">乔谦</td></tr>\n      '
text = text.replace(V28_KEY, V29_ROW + V28_KEY)

PRD.write_text(text, encoding='utf-8')
print('Done. lines:', text.count('\n'))
