#!/usr/bin/env python3
"""V2.11: 重写添加商家表单 + 更新字段清单 + i18n + 版本记录"""
from pathlib import Path
import re

PRD = Path('/Users/qiaoqian/clawd-on-desk/FoneSquare-PRD-v2.html')
text = PRD.read_text(encoding='utf-8')
changes = []

# ========== 1) 重写 addView() 函数 ==========
OLD_ADD_VIEW = """  function addView(){
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
  }"""

NEW_ADD_VIEW = r"""  function addView(){
    return '<div class="wf-view" data-view="add"><div class="wf-page">'
      + '<div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;"><button class="wf-btn" data-go-view="list">← <span data-i18n="back">返回列表</span></button><span style="font-size:14px;color:#262626;font-weight:600;" data-i18n="add-title">添加商家（单页录入）</span></div>'
      + '<div class="wf-alert wf-alert-info"><span>ℹ️</span><span data-i18n="add-tip"></span></div>'

      + '<div class="wf-card"><div class="wf-card-head" data-i18n="add-basic">基本信息（个人）</div><div class="wf-card-body">'
      +   '<div class="wf-form-row">'
      +     formItem('b-type','商家类型',true,'add-type-ph','请选择 买家 / 卖家','wf-select')
      +     formItem('b-name','姓名',true,'ph-input','请输入（与证件一致）','wf-input')
      +   '</div>'
      +   '<div class="wf-form-row">'
      +     formItem('b-phone','手机号',false,'add-phone-ph','含区号，如 +852 1234 5678','wf-input')
      +     formItem('b-email','邮箱',false,'ph-optional','选填','wf-input')
      +   '</div>'
      +   '<div class="wf-form-row">'
      +     formItem('b-whatsapp','WhatsApp',false,'add-wa-ph','选填','wf-input')
      +     formItem('b-region','所在地区',true,'add-region-ph','下拉选择','wf-select')
      +   '</div>'
      +   '<div class="wf-form-row">'
      +     formItem('b-remark','备注',false,'ph-optional','选填','wf-input')
      +   '</div>'
      +   '<div class="wf-alert wf-alert-info" style="margin:6px 0 0;padding:6px 10px;font-size:11px;"><span>💡</span><span data-i18n="add-contact-hint">手机号、邮箱、WhatsApp 三选一必填</span></div>'
      + '</div></div>'

      + '<div class="wf-card"><div class="wf-card-head" data-i18n="add-kyc">KYC 认证材料（个人）</div><div class="wf-card-body">'
      +   '<div class="wf-form-row">'
      +     formItem('k-doc','证件类型',true,'add-doc-ph','HKID / 澳门ID / 身份证 / 护照','wf-select')
      +     formItem('k-num','证件号码',true,'ph-input','请输入','wf-input')
      +   '</div>'
      +   '<div class="wf-form-row">'
      +     formItem('k-name','姓名（与证件一致）',true,'ph-input','请输入','wf-input')
      +     formItem('k-valid','证件有效期',true,'add-valid-ph','不可选过去日期','wf-input')
      +   '</div>'
      +   '<div class="wf-form-item">'
      +     '<div class="wf-form-label"><span data-i18n="k-photos">证件照片</span> <span style="color:#BFBFBF;font-size:10px;" data-i18n="optional">选填</span></div>'
      +     '<div style="display:flex;gap:8px;">'
      +       '<div class="wf-upload" style="flex:1;"><div class="wf-upload-icon">📤</div><span data-i18n="k-front">证件正面</span></div>'
      +       '<div class="wf-upload" style="flex:1;"><div class="wf-upload-icon">📤</div><span data-i18n="k-back">证件反面</span></div>'
      +     '</div>'
      +     '<div style="font-size:10px;color:#8C8C8C;margin-top:4px;" data-i18n="add-photo-hint">护照仅需上传一面；JPG/PNG ≤ 5MB</div>'
      +   '</div>'
      + '</div></div>'

      + '<div class="wf-card"><div class="wf-card-head"><span data-i18n="add-corp-kyc">KYC 认证材料（企业）</span> <span style="font-size:10px;color:#BFBFBF;font-weight:400;margin-left:6px;" data-i18n="optional">选填</span></div><div class="wf-card-body">'
      +   '<div class="wf-form-row">'
      +     formItem('kc-name','企业名称',false,'ph-optional','选填','wf-input')
      +     formItem('kc-doc-type','证照类型',false,'add-corp-doc-ph','商业登记证等','wf-select')
      +   '</div>'
      +   '<div class="wf-form-row">'
      +     formItem('kc-doc-num','证照编号',false,'ph-optional','选填','wf-input')
      +     formItem('kc-rep','法定代表 / 董事',false,'ph-optional','选填','wf-input')
      +   '</div>'
      +   '<div class="wf-form-row">'
      +     formItem('kc-addr','企业地址',false,'ph-optional','选填','wf-input')
      +     formItem('kc-valid','证照有效期',false,'ph-optional','选填','wf-input')
      +   '</div>'
      +   '<div class="wf-form-item"><div class="wf-form-label"><span data-i18n="kc-photo">证照照片</span> <span style="color:#BFBFBF;font-size:10px;" data-i18n="optional">选填</span></div><div class="wf-upload"><div class="wf-upload-icon">📤</div><span data-i18n="add-corp-photo-hint">JPG / PNG / PDF ≤ 10MB</span></div></div>'
      + '</div></div>'

      + '<div style="display:flex;gap:8px;justify-content:flex-end;margin-bottom:12px;">'
      +   '<button class="wf-btn" data-go-view="list" data-i18n="add-cancel">取消</button>'
      +   '<button class="wf-btn wf-btn-primary" data-act="addSubmit" data-i18n="add-submit">✅ 提交创建</button>'
      + '</div>'
      + '</div></div>';
  }"""

if OLD_ADD_VIEW in text:
    text = text.replace(OLD_ADD_VIEW, NEW_ADD_VIEW)
    changes.append('重写 addView()：基本信息(个人) + KYC(个人) + KYC(企业·选填)')
else:
    print('⚠️  addView 旧函数未匹配，尝试正则替换')
    m = re.search(r'  function addView\(\)\{.*?\n  \}', text, re.DOTALL)
    if m:
        text = text[:m.start()] + NEW_ADD_VIEW + text[m.end():]
        changes.append('重写 addView()（正则匹配）')
    else:
        print('❌ addView 正则也未匹配')

# ========== 2) 更新 i18n 字典 ==========
# 2a) add-basic 中文更新
text = text.replace("'add-basic':['基本信息','Basic Info']", "'add-basic':['基本信息（个人）','Basic Info (Personal)']")
# 2b) add-kyc 中文更新
text = text.replace("'add-kyc':['KYC 认证','KYC']", "'add-kyc':['KYC 认证材料（个人）','KYC (Personal)']")
# 2c) add-corp → add-corp-kyc
text = text.replace("'add-corp':['企业信息','Corporate Info']", "'add-corp-kyc':['KYC 认证材料（企业）','KYC (Corporate)']")

# 新增 i18n 条目（插入在 'add-cancel' 之前）
NEW_I18N = """    'add-phone-ph':['含区号，如 +852 1234 5678','e.g. +852 1234 5678'],
    'add-wa-ph':['选填','Optional'],
    'add-contact-hint':['手机号、邮箱、WhatsApp 三选一必填','Phone, Email, or WhatsApp — at least one required'],
    'add-photo-hint':['护照仅需上传一面；JPG/PNG ≤ 5MB','Passport: one side only; JPG/PNG ≤ 5MB'],
    'add-corp-doc-ph':['商业登记证等','Business Registration etc.'],
    'add-corp-photo-hint':['JPG / PNG / PDF ≤ 10MB','JPG/PNG/PDF ≤ 10MB'],
    """
text = text.replace("    'add-cancel':", NEW_I18N + "'add-cancel':")
changes.append('更新/新增 i18n 条目')

# ========== 3) 更新详情页字段清单表格 ==========
NEW_FIELD_LIST = """  <!-- ===== 五、详情页字段清单 ===== -->
  <h3>五、详情页字段清单</h3>
  <table style="position: relative;">
    <thead><tr><th>分组</th><th>字段</th><th>必填</th><th>说明</th></tr></thead>
    <tbody>
      <tr><td rowspan="6">基本信息（个人）</td><td>姓名</td><td><span class="tag tag-p0">必填</span></td><td style="position: relative;">与证件一致</td></tr>
      <tr><td>手机号</td><td><span class="tag" style="background:#F3F4F6;color:#6B7280;">选填</span></td><td style="position: relative;">含区号，格式校验（手机、邮箱、WhatsApp三选一必填）</td></tr>
      <tr><td>邮箱</td><td><span class="tag" style="background:#F3F4F6;color:#6B7280;">选填</span></td><td style="position: relative;">格式校验</td></tr>
      <tr><td>WhatsApp</td><td><span class="tag" style="background:#F3F4F6;color:#6B7280;">选填</span></td><td style="position: relative;">类似电话号码的WhatsApp账号</td></tr>
      <tr><td>所在地区</td><td><span class="tag tag-p0">必填</span></td><td style="position: relative;">下拉选择</td></tr>
      <tr><td>备注</td><td><span class="tag" style="background:#F3F4F6;color:#6B7280;">选填</span></td><td style="position: relative;">—</td></tr>
      <tr><td rowspan="5">KYC 认证材料（个人）</td><td>证件类型</td><td><span class="tag tag-p0">必填</span></td><td style="position: relative;">HKID / 澳门ID / 身份证 / 护照</td></tr>
      <tr><td>证件号码</td><td><span class="tag tag-p0">必填</span></td><td style="position: relative;">按证件类型格式校验，存储脱敏</td></tr>
      <tr><td>姓名（与证件一致）</td><td><span class="tag tag-p0">必填</span></td><td style="position: relative;">与证件一致</td></tr>
      <tr><td>证件有效期</td><td><span class="tag tag-p0">必填</span></td><td style="position: relative;">不可选过去日期</td></tr>
      <tr><td>证件照片</td><td><span class="tag" style="background:#F3F4F6;color:#6B7280;">选填</span></td><td style="position: relative;">正面 + 背面（护照仅一面），JPG/PNG ≤ 5MB</td></tr>
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
    changes.append('更新详情页字段清单（手机号改选填、证件照片改选填、WhatsApp描述更新）')

# ========== 4) 版本记录 V2.11 ==========
V210_KEY = '<tr><td>2026-04-29</td><td>V2.10 详情页改造'
V211_ROW = '<tr><td>2026-04-29</td><td>V2.11 添加商家表单重构：① 按详情页字段清单重写表单三区：基本信息(个人)、KYC认证材料(个人)、KYC认证材料(企业·选填)；② 手机号/邮箱/WhatsApp三选一必填提示；③ 证件照片改为选填(护照仅一面)；④ 企业KYC七字段完整展示；⑤ 同步更新详情页字段清单表格。</td><td style="position: relative;">乔谦</td></tr>\n      '
if V210_KEY in text:
    text = text.replace(V210_KEY, V211_ROW + V210_KEY)
    changes.append('添加版本记录 V2.11')

PRD.write_text(text, encoding='utf-8')
print('✅ V2.11 变更完成:')
for c in changes:
    print(f'   • {c}')
