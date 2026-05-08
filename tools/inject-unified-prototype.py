#!/usr/bin/env python3
"""
将统一可交互原型 HTML 块注入 FoneSquare-PRD-v2.html。
注入点：mermaid 块 `D --> G2["添加商家（自动绑定自己）"]` 后的空行
       与 `<h4>📖 列表页产品说明</h4>` 之间。
"""
from pathlib import Path
import re, sys

PRD = Path('/Users/qiaoqian/clawd-on-desk/FoneSquare-PRD-v2.html')

ANCHOR = '''  D --> G2["添加商家（自动绑定自己）"]
  </pre>

  <h4>📖 列表页产品说明</h4>'''

PROTO = '''  D --> G2["添加商家（自动绑定自己）"]
  </pre>

  <!-- ===== 四、可交互原型 — 后台统一原型（List ↔ Detail ↔ Add） ===== -->
  <h3>四、可交互原型 — 后台统一原型（List ↔ Detail ↔ Add，全在本页内交互）</h3>
  <p style="font-size:13px;color:#595959;margin:-8px 0 12px;">
    本原型直接在文档内交互，<strong>不再跳转新窗口</strong>；右上角 <strong>中 / EN</strong> 切换界面语言；<strong>仅保留「商家列表」一个主页面</strong>，去除左侧侧边菜单 ——「<strong>添加商家</strong>」与「<strong>商家详情</strong>」入口都在列表页面的按钮上：点击列表行的「查看」进入详情；点击右上「➕ 添加商家」进入录入页；详情页 5 个 Tab 均可点击切换；保证金 Tab 可以输入限额、保证金金额、上传转账凭证并实时校验<strong>限额上限 = 保证金 × 10</strong> 规则。
  </p>

  <style>
  /* ==== 统一原型局部样式（仅 #wfAdmin 内生效） ==== */
  #wfAdmin.wf-shell { aspect-ratio: auto; height: clamp(720px, 90vh, 980px); }
  #wfAdmin .wf-body { display:block; overflow:hidden; height:100%; }
  #wfAdmin .wf-content { padding:0; height:100%; }
  #wfAdmin .wf-view { display:none; flex-direction:column; flex:1; min-height:100%; overflow-y:auto; }
  #wfAdmin .wf-view.active { display:flex; }
  #wfAdmin .wf-table-list { table-layout:auto; min-width:880px; }
  #wfAdmin .wf-table-list th, #wfAdmin .wf-table-list td { white-space:nowrap; }
  #wfAdmin .wf-table-list td:nth-child(2) { white-space:normal; min-width:160px; }
  #wfAdmin .wf-table-list-wrap { overflow-x:auto; -webkit-overflow-scrolling:touch; }
  #wfAdmin .wf-lang { display:inline-flex; border:1px solid #D9D9D9; border-radius:4px; overflow:hidden; margin-right:8px; user-select:none; height:22px; line-height:22px; }
  #wfAdmin .wf-lang-btn { padding:0 8px; font-size:10px; cursor:pointer; color:#595959; background:white; }
  #wfAdmin .wf-lang-btn.active { background:#1677FF; color:white; }
  #wfAdmin .wf-input-edit { color:#262626 !important; }
  #wfAdmin .wf-input[contenteditable="true"]:focus { outline:none; border-color:#1677FF; box-shadow:0 0 0 2px rgba(22,119,255,.15); }
  </style>

  <div class="wf-shell" id="wfAdmin">
    <!-- TopBar -->
    <div class="wf-topbar">
      <div class="wf-topbar-left">
        <span data-i18n="brand">FoneSquare 商家管理后台</span>
        <span style="margin:0 6px;color:#D9D9D9;">/</span>
        <strong data-i18n="crumb" style="color:#262626;">商家列表</strong>
      </div>
      <div class="wf-topbar-right">
        <div class="wf-lang" title="切换中英文">
          <span class="wf-lang-btn active" data-lang="zh">中</span>
          <span class="wf-lang-btn" data-lang="en">EN</span>
        </div>
        <span>🔔</span>
        <div class="wf-topbar-avatar">Q</div>
        <span style="color:#595959;" data-i18n="user">乔谦</span>
      </div>
    </div>
    <!-- Body（无侧边菜单） -->
    <div class="wf-body">
      <div class="wf-content">
        <!-- ============ View: List ============ -->
        <div class="wf-view active" data-view="list">
          <div class="wf-page">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
              <span style="font-size:16px;font-weight:700;color:#262626;" data-i18n="list-title">商家列表</span>
              <div style="display:flex;gap:6px;">
                <button class="wf-btn" data-i18n="export">📥 导出</button>
                <button class="wf-btn wf-btn-primary" data-go-view="add" data-i18n="add">➕ 添加商家</button>
              </div>
            </div>
            <div class="wf-card">
              <div class="wf-card-body" style="padding:12px 16px;">
                <div class="wf-filter-bar">
                  <div class="wf-form-item"><div class="wf-form-label" data-i18n="f-name">商家名称</div><div class="wf-input" data-i18n="ph-name">请输入名称关键词</div></div>
                  <div class="wf-form-item w120"><div class="wf-form-label" data-i18n="f-type">商家类型</div><div class="wf-select" data-i18n="all">全部</div></div>
                  <div class="wf-form-item w120"><div class="wf-form-label" data-i18n="f-status">状态</div><div class="wf-select" data-i18n="all">全部</div></div>
                  <div class="wf-form-item"><div class="wf-form-label" data-i18n="f-sales">所属销售（仅管理员）</div><div class="wf-select" data-i18n="all">全部</div></div>
                  <div class="wf-form-item" style="flex:none;width:auto;">
                    <div class="wf-form-label">&nbsp;</div>
                    <div style="display:flex;gap:4px;">
                      <button class="wf-btn wf-btn-primary" data-i18n="search">🔍 查询</button>
                      <button class="wf-btn" data-i18n="reset">↺ 重置</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="wf-card">
              <div class="wf-card-head">
                <span data-i18n="result">查询结果</span>
                <span style="font-size:10px;color:#8C8C8C;font-weight:400;" data-i18n="total86">共 86 条</span>
              </div>
              <div class="wf-table-list-wrap">
              <table class="wf-table wf-table-list" style="position:relative;">
                <thead><tr>
                  <th style="width:50px;">ID</th>
                  <th data-i18n="th-name">商家名称</th>
                  <th style="width:60px;" data-i18n="th-type">类型</th>
                  <th style="width:60px;" data-i18n="th-status">状态</th>
                  <th style="width:80px;" data-i18n="th-contact">联系人</th>
                  <th style="width:140px;" data-i18n="th-phone">联系方式</th>
                  <th style="width:80px;" data-i18n="th-sales">所属销售</th>
                  <th style="width:90px;" data-i18n="th-time">创建时间</th>
                  <th style="width:120px;" data-i18n="th-op">操作</th>
                </tr></thead>
                <tbody>
                  <tr>
                    <td>1001</td>
                    <td style="font-weight:500;color:#262626;">HK Mobile Trade Co.</td>
                    <td><span class="wf-tag wf-tag-cyan" data-i18n="t-buyer">买家</span></td>
                    <td><span class="wf-tag wf-tag-green" data-i18n="s-active">使用</span></td>
                    <td>陈先生</td>
                    <td>+852 9123 4567</td>
                    <td>张三</td>
                    <td style="font-size:10px;color:#8C8C8C;">2026-04-10</td>
                    <td>
                      <button class="wf-btn-link" data-go-view="detail" data-merchant="1001" data-i18n="view">查看</button>
                      <button class="wf-btn-link" data-i18n="edit">编辑</button>
                    </td>
                  </tr>
                  <tr>
                    <td>1002</td>
                    <td style="font-weight:500;color:#262626;">Macau Phones Ltd.</td>
                    <td><span class="wf-tag wf-tag-purple" data-i18n="t-seller">卖家</span></td>
                    <td><span class="wf-tag wf-tag-green" data-i18n="s-active">使用</span></td>
                    <td>李小姐</td>
                    <td>+853 6234 5678</td>
                    <td>李四</td>
                    <td style="font-size:10px;color:#8C8C8C;">2026-04-12</td>
                    <td>
                      <button class="wf-btn-link" data-go-view="detail" data-merchant="1002" data-i18n="view">查看</button>
                      <button class="wf-btn-link" data-i18n="edit">编辑</button>
                    </td>
                  </tr>
                  <tr>
                    <td>1003</td>
                    <td style="font-weight:500;color:#262626;">SG Recycle Hub</td>
                    <td><span class="wf-tag wf-tag-cyan" data-i18n="t-buyer">买家</span></td>
                    <td><span class="wf-tag wf-tag-default" data-i18n="s-inactive">停用</span></td>
                    <td>王先生</td>
                    <td>+65 8345 6789</td>
                    <td style="color:#BFBFBF;" data-i18n="unassigned">未分配</td>
                    <td style="font-size:10px;color:#8C8C8C;">2026-04-15</td>
                    <td>
                      <button class="wf-btn-link" data-go-view="detail" data-merchant="1003" data-i18n="view">查看</button>
                      <button class="wf-btn-link" data-i18n="edit">编辑</button>
                    </td>
                  </tr>
                  <tr>
                    <td>1004</td>
                    <td style="font-weight:500;color:#262626;">TW Digital Trade</td>
                    <td><span class="wf-tag wf-tag-purple" data-i18n="t-seller">卖家</span></td>
                    <td><span class="wf-tag wf-tag-green" data-i18n="s-active">使用</span></td>
                    <td>林先生</td>
                    <td>+886 912 345678</td>
                    <td>张三</td>
                    <td style="font-size:10px;color:#8C8C8C;">2026-04-08</td>
                    <td>
                      <button class="wf-btn-link" data-go-view="detail" data-merchant="1004" data-i18n="view">查看</button>
                      <button class="wf-btn-link" data-i18n="edit">编辑</button>
                    </td>
                  </tr>
                  <tr>
                    <td>1005</td>
                    <td style="font-weight:500;color:#262626;">JP Phone Market</td>
                    <td><span class="wf-tag wf-tag-cyan" data-i18n="t-buyer">买家</span></td>
                    <td><span class="wf-tag wf-tag-green" data-i18n="s-active">使用</span></td>
                    <td>田中</td>
                    <td>+81 80 1234 5678</td>
                    <td>王五</td>
                    <td style="font-size:10px;color:#8C8C8C;">2026-04-06</td>
                    <td>
                      <button class="wf-btn-link" data-go-view="detail" data-merchant="1005" data-i18n="view">查看</button>
                      <button class="wf-btn-link" data-i18n="edit">编辑</button>
                    </td>
                  </tr>
                </tbody>
              </table>
              </div>
              <div class="wf-pagination">
                <span style="margin-right:6px;" data-i18n="total86">共 86 条</span>
                <div class="wf-pg">&lt;</div><div class="wf-pg active">1</div><div class="wf-pg">2</div><div class="wf-pg">3</div><div class="wf-pg">…</div><div class="wf-pg">9</div><div class="wf-pg">&gt;</div>
                <span style="margin-left:6px;" data-i18n="per-page">10 条/页</span>
              </div>
            </div>
          </div>
        </div>

        <!-- ============ View: Detail ============ -->
        <div class="wf-view" data-view="detail">
          <div class="wf-page" style="padding-bottom:0;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
              <button class="wf-btn" data-go-view="list">← <span data-i18n="back">返回列表</span></button>
              <span style="font-size:13px;color:#8C8C8C;">商家 ID：<span id="dMid">1001</span></span>
            </div>
            <div class="wf-card">
              <div class="wf-card-body" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                <div>
                  <div style="font-size:15px;font-weight:600;color:#262626;">
                    <span id="dName">HK Mobile Trade Co.</span>
                    <span class="wf-tag wf-tag-cyan" id="dType" style="margin-left:6px;" data-i18n="t-buyer">买家</span>
                    <span class="wf-tag wf-tag-green" data-i18n="s-active">使用</span>
                  </div>
                  <div style="font-size:11px;color:#8C8C8C;margin-top:4px;">
                    <span data-i18n="d-mid">商家 ID</span>：<span id="dMid2">1001</span>
                    &nbsp;·&nbsp; <span data-i18n="d-sales">所属销售</span>：张三
                    &nbsp;·&nbsp; <span data-i18n="d-since">入驻日期</span>：2026-04-10
                  </div>
                </div>
                <div style="display:flex;gap:6px;">
                  <button class="wf-btn wf-btn-primary" data-i18n="d-edit">✏️ 编辑信息</button>
                  <button class="wf-btn" data-i18n="d-disable">⏸️ 停用</button>
                </div>
              </div>
            </div>
          </div>
          <!-- Tabs -->
          <div class="wf-tabs">
            <div class="wf-tab active" data-tab="basic" data-i18n="tab-basic">基本信息</div>
            <div class="wf-tab" data-tab="kyc" data-i18n="tab-kyc">KYC 认证材料</div>
            <div class="wf-tab" data-tab="quota" data-i18n="tab-quota">限额与保证金</div>
            <div class="wf-tab" data-tab="sales" data-i18n="tab-sales">销售绑定</div>
            <div class="wf-tab" data-tab="log" data-i18n="tab-log">操作日志</div>
          </div>
          <div class="wf-page" style="padding-top:14px;">
            <!-- Panel basic -->
            <div class="wf-tab-panel active" data-panel="basic">
              <div class="wf-card"><div class="wf-card-head" data-i18n="p-basic">基本信息</div><div class="wf-card-body">
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="b-name">商家名称</div><div class="wf-desc-value">HK Mobile Trade Co.</div></div>
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="b-type">商家类型</div><div class="wf-desc-value"><span class="wf-tag wf-tag-cyan" data-i18n="t-buyer">买家</span></div></div>
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="b-contact">联系人</div><div class="wf-desc-value">陈先生</div></div>
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="b-phone">联系方式</div><div class="wf-desc-value">+852 9123 4567</div></div>
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="b-email">邮箱</div><div class="wf-desc-value">chen@hkmobile.com</div></div>
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="b-region">所在地区</div><div class="wf-desc-value" data-i18n="region-hk">香港</div></div>
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="b-status">状态</div><div class="wf-desc-value"><span class="wf-tag wf-tag-green" data-i18n="s-active">使用</span></div></div>
              </div></div>
            </div>
            <!-- Panel kyc -->
            <div class="wf-tab-panel" data-panel="kyc">
              <div class="wf-card"><div class="wf-card-head" data-i18n="p-kyc">KYC 认证材料</div><div class="wf-card-body">
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="k-doc">证件类型</div><div class="wf-desc-value">HK ID</div></div>
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="k-num">证件号</div><div class="wf-desc-value">A***456(7)</div></div>
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="k-name">证件姓名</div><div class="wf-desc-value">陈大文</div></div>
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="k-front">证件正面</div><div class="wf-desc-value">📷 <a href="#" onclick="return false">view</a></div></div>
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="k-back">证件反面</div><div class="wf-desc-value">📷 <a href="#" onclick="return false">view</a></div></div>
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="k-status">审核状态</div><div class="wf-desc-value"><span class="wf-tag wf-tag-green" data-i18n="k-passed">已通过</span></div></div>
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="k-time">审核时间</div><div class="wf-desc-value">2026-04-10 14:23</div></div>
              </div></div>
            </div>
            <!-- Panel quota — 仅买家 -->
            <div class="wf-tab-panel" data-panel="quota">
              <div class="wf-alert wf-alert-info">
                <span>ℹ️</span>
                <span data-i18n="q-rule">业务规则：保证金由<strong>买家</strong>缴纳；每日下单限额上限 = 保证金 × 10。<strong>未提交转账凭证前</strong>，限额仅可设置为业务默认最小值；上传凭证、运营确认后，限额可在<strong>默认最小值 ~ 保证金 × 10</strong> 范围内自由配置。</span>
              </div>
              <div class="wf-card">
                <div class="wf-card-head" data-i18n="q-hk">香港店每日下单限额配置（仅买家）</div>
                <div class="wf-card-body">
                  <div class="wf-form-row">
                    <div class="wf-form-item">
                      <div class="wf-form-label"><span class="req">*</span><span data-i18n="q-limit">每日下单限额（HKD）</span></div>
                      <div class="wf-input wf-input-edit" id="qInputLimit" contenteditable="true" spellcheck="false">50000</div>
                      <div style="font-size:10px;color:#8C8C8C;margin-top:3px;" data-i18n="q-limit-hint">默认最小值由业务配置；上限 = 当前保证金 × 10</div>
                    </div>
                    <div class="wf-form-item">
                      <div class="wf-form-label"><span class="req">*</span><span data-i18n="q-deposit">保证金金额（HKD）</span></div>
                      <div class="wf-input wf-input-edit" id="qInputDeposit" contenteditable="true" spellcheck="false">5000</div>
                      <div style="font-size:10px;color:#8C8C8C;margin-top:3px;" data-i18n="q-deposit-hint">运营录入；保证金 × 10 = 限额上限</div>
                    </div>
                  </div>
                  <div class="wf-form-item">
                    <div class="wf-form-label"><span class="req">*</span><span data-i18n="q-proof">保证金转账记录（图片上传）</span></div>
                    <div class="wf-upload" id="qUpload">
                      <div class="wf-upload-icon">⬆️</div>
                      <div data-i18n="q-upload-hint" id="qUploadText">点击上传转账凭证（JPG/PNG，单张 ≤ 5MB，最多 3 张）</div>
                    </div>
                    <div style="font-size:10px;color:#8C8C8C;margin-top:3px;" data-i18n="q-proof-hint">未提交凭证前限额无法调高，仅可保留默认最小值</div>
                  </div>
                  <div class="wf-form-row">
                    <div class="wf-form-item">
                      <div class="wf-form-label" data-i18n="q-status">保证金状态</div>
                      <div><span class="wf-tag wf-tag-default" id="qStatus" data-i18n="q-st-pending">未提交</span></div>
                    </div>
                    <div class="wf-form-item">
                      <div class="wf-form-label" data-i18n="q-confirm">确认时间 / 确认人</div>
                      <div style="font-size:11px;color:#262626;">— / —</div>
                    </div>
                  </div>
                  <div style="display:flex;gap:6px;margin-top:8px;">
                    <button class="wf-btn wf-btn-primary" id="qBtnSave" data-i18n="q-save">💾 校验并保存</button>
                    <button class="wf-btn" data-i18n="q-cancel">取消</button>
                  </div>
                  <div class="wf-alert" id="qResult" style="display:none;margin-top:10px;"></div>
                </div>
              </div>
            </div>
            <!-- Panel sales -->
            <div class="wf-tab-panel" data-panel="sales">
              <div class="wf-card"><div class="wf-card-head" data-i18n="p-sales">销售绑定</div><div class="wf-card-body">
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="sa-current">当前销售</div><div class="wf-desc-value">张三 (sales01@fonesquare.com)</div></div>
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="sa-since">绑定时间</div><div class="wf-desc-value">2026-04-10 14:23</div></div>
                <div class="wf-desc-row"><div class="wf-desc-label" data-i18n="sa-by">绑定人</div><div class="wf-desc-value">admin01</div></div>
                <div style="margin-top:10px;display:flex;gap:6px;">
                  <button class="wf-btn wf-btn-primary" id="saReassignBtn" data-i18n="sa-reassign">🔄 更换销售</button>
                  <button class="wf-btn" data-i18n="sa-history">📜 查看变更历史</button>
                </div>
                <div id="saReassignBox" style="display:none;margin-top:12px;border:1px dashed #1677FF;border-radius:6px;padding:12px;background:#F0F8FF;">
                  <div class="wf-form-item">
                    <div class="wf-form-label"><span class="req">*</span><span data-i18n="sa-new">选择新销售</span></div>
                    <div class="wf-select" data-i18n="sa-new-ph">从 OB 销售列表选择…</div>
                  </div>
                  <div class="wf-form-item">
                    <div class="wf-form-label"><span class="req">*</span><span data-i18n="sa-reason">变更原因</span></div>
                    <div class="wf-textarea" data-i18n="sa-reason-ph">请填写变更原因（必填，将记录到操作日志）</div>
                  </div>
                  <div style="display:flex;gap:6px;justify-content:flex-end;">
                    <button class="wf-btn" id="saCancelBtn" data-i18n="sa-cancel">取消</button>
                    <button class="wf-btn wf-btn-primary" data-i18n="sa-confirm">确认变更</button>
                  </div>
                </div>
              </div></div>
            </div>
            <!-- Panel log -->
            <div class="wf-tab-panel" data-panel="log">
              <div class="wf-card"><div class="wf-card-head" data-i18n="p-log">操作日志</div><div class="wf-card-body">
                <div class="wf-timeline">
                  <div class="wf-tl-item"><div class="wf-tl-time">2026-04-10 14:23</div><div class="wf-tl-text" data-i18n="lg-1">admin01 创建商家 HK Mobile Trade Co.（自动绑定销售：张三）</div></div>
                  <div class="wf-tl-item"><div class="wf-tl-time">2026-04-10 14:25</div><div class="wf-tl-text" data-i18n="lg-2">admin01 完成 KYC 审核 → 已通过</div></div>
                  <div class="wf-tl-item"><div class="wf-tl-time">2026-04-12 10:08</div><div class="wf-tl-text" data-i18n="lg-3">admin02 编辑联系方式 +852 9*** 4567</div></div>
                  <div class="wf-tl-item"><div class="wf-tl-time">2026-04-15 16:40</div><div class="wf-tl-text" data-i18n="lg-4">admin01 配置每日下单限额 50,000 HKD（保证金 5,000 已确认）</div></div>
                </div>
              </div></div>
            </div>
          </div>
        </div>

        <!-- ============ View: Add ============ -->
        <div class="wf-view" data-view="add">
          <div class="wf-page">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
              <button class="wf-btn" data-go-view="list">← <span data-i18n="back">返回列表</span></button>
              <span style="font-size:14px;color:#262626;font-weight:600;" data-i18n="add-title">添加商家（单页录入）</span>
            </div>
            <div class="wf-alert wf-alert-info">
              <span>ℹ️</span>
              <span data-i18n="add-tip">销售添加 → 自动绑定为本人；管理员添加 → 默认未分配，需在「商家详情 → 销售绑定」中手动分配。</span>
            </div>
            <div class="wf-card">
              <div class="wf-card-head" data-i18n="add-basic">基本信息</div>
              <div class="wf-card-body">
                <div class="wf-form-row">
                  <div class="wf-form-item"><div class="wf-form-label"><span class="req">*</span><span data-i18n="b-name">商家名称</span></div><div class="wf-input" data-i18n="ph-input">请输入</div></div>
                  <div class="wf-form-item"><div class="wf-form-label"><span class="req">*</span><span data-i18n="b-type">商家类型</span></div><div class="wf-select" data-i18n="add-type-ph">请选择 买家 / 卖家</div></div>
                </div>
                <div class="wf-form-row">
                  <div class="wf-form-item"><div class="wf-form-label"><span class="req">*</span><span data-i18n="b-contact">联系人</span></div><div class="wf-input" data-i18n="ph-input">请输入</div></div>
                  <div class="wf-form-item"><div class="wf-form-label"><span class="req">*</span><span data-i18n="b-phone">联系方式</span></div><div class="wf-input">+852 ...</div></div>
                </div>
                <div class="wf-form-row">
                  <div class="wf-form-item"><div class="wf-form-label" data-i18n="b-email">邮箱</div><div class="wf-input" data-i18n="ph-optional">选填</div></div>
                  <div class="wf-form-item"><div class="wf-form-label"><span class="req">*</span><span data-i18n="b-region">所在地区</span></div><div class="wf-select" data-i18n="add-region-ph">国家 / 省份 / 城市 三级联动</div></div>
                </div>
              </div>
            </div>
            <div class="wf-card">
              <div class="wf-card-head" data-i18n="add-kyc">KYC 认证</div>
              <div class="wf-card-body">
                <div class="wf-form-row">
                  <div class="wf-form-item"><div class="wf-form-label"><span class="req">*</span><span data-i18n="k-doc">证件类型</span></div><div class="wf-select" data-i18n="add-doc-ph">按地区动态展示（HK ID / 护照 / 身份证…）</div></div>
                  <div class="wf-form-item"><div class="wf-form-label"><span class="req">*</span><span data-i18n="k-num">证件号</span></div><div class="wf-input" data-i18n="ph-input">请输入</div></div>
                </div>
                <div class="wf-form-row">
                  <div class="wf-form-item"><div class="wf-form-label"><span class="req">*</span><span data-i18n="k-name">证件姓名</span></div><div class="wf-input" data-i18n="ph-input">请输入</div></div>
                  <div class="wf-form-item"><div class="wf-form-label"><span class="req">*</span><span data-i18n="k-valid">证件有效期</span></div><div class="wf-input" data-i18n="add-valid-ph">不可选过去日期</div></div>
                </div>
                <div class="wf-form-item">
                  <div class="wf-form-label"><span class="req">*</span><span data-i18n="k-photos">证件照片</span></div>
                  <div style="display:flex;gap:8px;">
                    <div class="wf-upload" style="flex:1;"><div class="wf-upload-icon">📤</div><span data-i18n="k-front">证件正面</span></div>
                    <div class="wf-upload" style="flex:1;"><div class="wf-upload-icon">📤</div><span data-i18n="k-back">证件反面</span></div>
                    <div class="wf-upload" style="flex:1;"><div class="wf-upload-icon">📤</div><span data-i18n="k-hand">手持证件</span></div>
                  </div>
                </div>
              </div>
            </div>
            <div class="wf-card">
              <div class="wf-card-head"><span data-i18n="add-corp">企业信息</span> <span style="font-size:10px;color:#BFBFBF;font-weight:400;margin-left:6px;" data-i18n="optional">选填</span></div>
              <div class="wf-card-body">
                <div class="wf-form-row">
                  <div class="wf-form-item"><div class="wf-form-label" data-i18n="c-name">公司名称</div><div class="wf-input" data-i18n="ph-optional">选填</div></div>
                  <div class="wf-form-item"><div class="wf-form-label" data-i18n="c-num">商业登记号</div><div class="wf-input" data-i18n="ph-optional">选填</div></div>
                </div>
                <div class="wf-form-item"><div class="wf-form-label" data-i18n="c-license">营业执照照片</div><div class="wf-upload"><div class="wf-upload-icon">📤</div><span data-i18n="c-license-hint">JPG / PNG / PDF ≤ 10MB，提交可获更高交易额度</span></div></div>
              </div>
            </div>
            <div style="display:flex;gap:8px;justify-content:flex-end;margin-bottom:12px;">
              <button class="wf-btn" data-go-view="list" data-i18n="add-cancel">取消</button>
              <button class="wf-btn wf-btn-primary" id="addSubmit" data-i18n="add-submit">✅ 提交创建</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
  (function(){
    var shell = document.getElementById('wfAdmin');
    if (!shell) return;
    var I18N = {
      'brand':['FoneSquare 商家管理后台','FoneSquare Admin'],
      'crumb-list':['商家列表','Merchant List'],
      'crumb-detail':['商家详情','Merchant Detail'],
      'crumb-add':['添加商家','Add Merchant'],
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
      'add-submit':['✅ 提交创建','✅ Submit']
    };
    var lang = 'zh';
    var hasProof = false;

    function setCrumb(view){
      var crumb = shell.querySelector('[data-i18n="crumb"]');
      if (!crumb) return;
      var k = view==='list' ? 'crumb-list' : (view==='detail' ? 'crumb-detail' : 'crumb-add');
      crumb.textContent = I18N[k][lang==='zh'?0:1];
    }
    function go(view){
      shell.querySelectorAll('.wf-view').forEach(function(v){ v.classList.toggle('active', v.dataset.view===view); });
      setCrumb(view);
    }
    shell.querySelectorAll('[data-go-view]').forEach(function(el){
      el.addEventListener('click', function(){
        var v = el.dataset.goView;
        if (v==='detail' && el.dataset.merchant){
          var mid = el.dataset.merchant;
          var mname = el.closest('tr').children[1].textContent.trim();
          var mtype = el.closest('tr').querySelector('.wf-tag-cyan, .wf-tag-purple');
          var typeKey = mtype && mtype.classList.contains('wf-tag-cyan') ? 't-buyer' : 't-seller';
          var dMid = document.getElementById('dMid');  if (dMid) dMid.textContent = mid;
          var dMid2 = document.getElementById('dMid2'); if (dMid2) dMid2.textContent = mid;
          var dName = document.getElementById('dName'); if (dName) dName.textContent = mname;
          var dType = document.getElementById('dType');
          if (dType){
            dType.className = 'wf-tag ' + (typeKey==='t-buyer' ? 'wf-tag-cyan' : 'wf-tag-purple');
            dType.dataset.i18n = typeKey;
            dType.textContent = I18N[typeKey][lang==='zh'?0:1];
          }
        }
        go(v);
      });
    });

    // Tab switch
    shell.querySelectorAll('.wf-tab').forEach(function(t){
      t.addEventListener('click', function(){
        shell.querySelectorAll('.wf-tab').forEach(function(x){ x.classList.remove('active'); });
        t.classList.add('active');
        shell.querySelectorAll('.wf-tab-panel').forEach(function(p){ p.classList.toggle('active', p.dataset.panel===t.dataset.tab); });
      });
    });

    // Quota & Deposit interactive
    var qResult = document.getElementById('qResult');
    var qStatus = document.getElementById('qStatus');
    var qUpload = document.getElementById('qUpload');
    var qUploadText = document.getElementById('qUploadText');
    function refreshUploadUi(){
      qUpload.style.borderStyle = hasProof ? 'solid' : 'dashed';
      qUpload.style.borderColor = hasProof ? '#52C41A' : '#D9D9D9';
      qUpload.style.background = hasProof ? '#F6FFED' : '#FAFAFA';
      qUploadText.dataset.i18n = hasProof ? 'q-upload-done' : 'q-upload-hint';
      qUploadText.textContent = I18N[qUploadText.dataset.i18n][lang==='zh'?0:1];
      qStatus.className = 'wf-tag ' + (hasProof ? 'wf-tag-blue' : 'wf-tag-default');
      qStatus.dataset.i18n = hasProof ? 'q-st-submitted' : 'q-st-pending';
      qStatus.textContent = I18N[qStatus.dataset.i18n][lang==='zh'?0:1];
    }
    if (qUpload) qUpload.addEventListener('click', function(){ hasProof = !hasProof; refreshUploadUi(); });

    var qBtnSave = document.getElementById('qBtnSave');
    if (qBtnSave) qBtnSave.addEventListener('click', function(){
      var DEFAULT_MIN = 1000;
      var limitTxt = (document.getElementById('qInputLimit')||{}).textContent || '0';
      var depositTxt = (document.getElementById('qInputDeposit')||{}).textContent || '0';
      var limit = parseInt(String(limitTxt).replace(/[^0-9]/g,''),10)||0;
      var deposit = parseInt(String(depositTxt).replace(/[^0-9]/g,''),10)||0;
      var msg = '', lvl = 'wf-alert-info';
      if (!hasProof) {
        if (limit > DEFAULT_MIN) {
          msg = lang==='zh' ? ('❌ 未提交保证金转账凭证，限额最大仅可设置为业务默认最小值 ' + DEFAULT_MIN + ' HKD') : ('Without deposit proof, daily limit cannot exceed default minimum ' + DEFAULT_MIN + ' HKD');
          lvl = 'wf-alert-warning';
        } else {
          msg = lang==='zh' ? '✅ 已保存（限额采用默认最小值；保证金未提交，状态保持「未提交」）' : 'Saved (limit at default minimum; deposit not submitted)';
        }
      } else {
        var maxLimit = deposit * 10;
        if (deposit <= 0) {
          msg = lang==='zh' ? '❌ 保证金金额必须大于 0' : 'Deposit must be greater than 0';
          lvl = 'wf-alert-warning';
        } else if (limit > maxLimit) {
          msg = lang==='zh' ? ('❌ 限额超过保证金 × 10 = ' + maxLimit + ' HKD，请调低限额或提高保证金') : ('Limit exceeds deposit × 10 = ' + maxLimit + ' HKD');
          lvl = 'wf-alert-warning';
        } else if (limit < DEFAULT_MIN) {
          msg = lang==='zh' ? ('❌ 限额低于业务默认最小值 ' + DEFAULT_MIN + ' HKD') : ('Limit below default minimum ' + DEFAULT_MIN + ' HKD');
          lvl = 'wf-alert-warning';
        } else {
          msg = lang==='zh' ? ('✅ 校验通过：保证金 ' + deposit + ' HKD × 10 = ' + maxLimit + ' HKD（当前限额 ' + limit + ' HKD ≤ 上限）已保存') : ('OK: deposit ' + deposit + ' × 10 = ' + maxLimit + '; current limit ' + limit + ' saved');
        }
      }
      qResult.className = 'wf-alert ' + lvl;
      qResult.textContent = msg;
      qResult.style.display = 'flex';
    });

    // Reassign sales toggle
    var saReassignBtn = document.getElementById('saReassignBtn');
    var saReassignBox = document.getElementById('saReassignBox');
    var saCancelBtn = document.getElementById('saCancelBtn');
    if (saReassignBtn && saReassignBox) saReassignBtn.addEventListener('click', function(){ saReassignBox.style.display = 'block'; });
    if (saCancelBtn && saReassignBox) saCancelBtn.addEventListener('click', function(){ saReassignBox.style.display = 'none'; });

    // Add submit demo
    var addSubmit = document.getElementById('addSubmit');
    if (addSubmit) addSubmit.addEventListener('click', function(){
      var msg = lang==='zh' ? '✅ 创建成功（演示）— 实际提交时校验证件唯一性 / 制裁名单核查 / 触发归属规则' : '✅ Created (demo) — real submit will check ID uniqueness, sanction list and ownership rules';
      alert(msg);
      go('list');
    });

    // i18n apply
    function applyI18n(){
      shell.querySelectorAll('[data-i18n]').forEach(function(el){
        var k = el.getAttribute('data-i18n');
        if (k==='crumb') return;
        var pair = I18N[k];
        if (!pair) return;
        var v = pair[lang==='zh'?0:1];
        if (/<\\w+/.test(v)) el.innerHTML = v;
        else el.textContent = v;
      });
      // crumb 用当前 view 决定
      var activeView = shell.querySelector('.wf-view.active');
      setCrumb(activeView ? activeView.dataset.view : 'list');
    }
    shell.querySelectorAll('.wf-lang-btn').forEach(function(b){
      b.addEventListener('click', function(){
        shell.querySelectorAll('.wf-lang-btn').forEach(function(x){ x.classList.remove('active'); });
        b.classList.add('active');
        lang = b.dataset.lang;
        applyI18n();
      });
    });
  })();
  </script>

  <h4>📖 列表页产品说明</h4>'''

text = PRD.read_text(encoding='utf-8')
if ANCHOR not in text:
    print('ERROR: anchor not found', file=sys.stderr); sys.exit(1)
count = text.count(ANCHOR)
if count != 1:
    print(f'ERROR: anchor matched {count} times', file=sys.stderr); sys.exit(1)
new = text.replace(ANCHOR, PROTO, 1)
PRD.write_text(new, encoding='utf-8')
print('Injected unified prototype OK; new file lines =', new.count('\n'))
