#!/usr/bin/env python3
"""Update tracking requirements in FoneSquare-PRD-v2.html:
1. Remove deprecated/deleted tracking rows
2. Add missing pages and events from fonesquare-login.html and fonesquare-kyc.html
3. Add missing individual events to existing pages
4. Update funnel section
5. Renumber all rows
"""

import re, sys

FILE = 'FoneSquare-PRD-v2.html'
text = open(FILE, 'r', encoding='utf-8').read()
orig_len = len(text)

# ──────────────────────────────────────────────
# 1. Remove deprecated rows
# ──────────────────────────────────────────────

# 1a. Remove "Email Pwd" section header + 2 data rows
old = '''      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative; color:#9CA3AF; text-decoration:line-through;">Email Pwd 邮箱设密码（V1.2 废弃 — 邮箱注册统一使用通用密码设置页 Set Pwd）</td></tr>
      <tr><td style="color:#9CA3AF;">31</td><td style="text-decoration:line-through;color:#9CA3AF;">Email Pwd</td><td style="color:#9CA3AF;">PV</td><td style="text-decoration:line-through;color:#9CA3AF;">email_pwd_view</td><td style="color:#9CA3AF;">已废弃 — 邮箱注册合流至通用 Set Pwd</td><td style="position: relative; color:#9CA3AF;">—</td></tr>
      <tr><td style="color:#9CA3AF;">32</td><td style="text-decoration:line-through;color:#9CA3AF;">Email Pwd</td><td style="color:#9CA3AF;">CLK</td><td style="text-decoration:line-through;color:#9CA3AF;">email_pwd_submit</td><td style="color:#9CA3AF;">已废弃</td><td style="position: relative; color:#9CA3AF;">—</td></tr>

      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">Set Password 设置密码</td></tr>'''
new = '''      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">Set Password 设置密码</td></tr>'''
assert old in text, "Email Pwd block not found"
text = text.replace(old, new)
print("[OK] Removed Email Pwd deprecated section")

# 1b. Remove set_pwd_skip row
old = '''      <tr><td>35</td><td style="text-decoration:line-through;color:#9CA3AF;">Set Password</td><td style="color:#9CA3AF;">CLK</td><td style="text-decoration:line-through;color:#9CA3AF;">set_pwd_skip</td><td style="color:#9CA3AF;">已移除 — 密码设置不可跳过</td><td style="position: relative; color:#9CA3AF;">—</td></tr>

      <tr><td colspan="6"'''
new = '''      <tr><td colspan="6"'''
assert old in text, "set_pwd_skip row not found"
text = text.replace(old, new)
print("[OK] Removed set_pwd_skip row")

# 1c. Remove profile_skip row
old = '''      <tr><td>44</td><td style="text-decoration:line-through;color:#9CA3AF;">Profile</td><td style="color:#9CA3AF;">CLK</td><td style="text-decoration:line-through;color:#9CA3AF;">profile_skip</td><td style="color:#9CA3AF;">已移除 — 注册流程不再包含 Profile 页</td><td style="position: relative; color:#9CA3AF;">—</td></tr>

      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">Registration Complete'''
new = '''      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">Registration Complete'''
assert old in text, "profile_skip row not found"
text = text.replace(old, new)
print("[OK] Removed profile_skip row")

# 1d. Remove reg_success_complete_profile row
old = '''      <tr><td style="color:#9CA3AF;">47</td><td style="text-decoration:line-through;color:#9CA3AF;">Success</td><td style="color:#9CA3AF;">CLK</td><td style="text-decoration:line-through;color:#9CA3AF;">reg_success_complete_profile</td><td style="color:#9CA3AF;">已移除</td><td style="position: relative; color:#9CA3AF;">—</td></tr>

      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">Pwd Login'''
new = '''      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">Pwd Login'''
assert old in text, "reg_success_complete_profile row not found"
text = text.replace(old, new)
print("[OK] Removed reg_success_complete_profile row")

# ──────────────────────────────────────────────
# 2. Add Homepage section to Login module
# ──────────────────────────────────────────────

# Insert before the closing </tbody> of login module table
# Anchor: after the Forgot Password section, before </tbody></table> of login module
old_anchor = '''      <tr><td>60</td><td>Forgot Pwd</td><td>CLK</td><td>forgot_pwd_close</td><td>关闭弹层（× 或点遮罩）</td><td style="position: relative;">current_step, mode</td></tr>
    </tbody>
  </table>

  <h3>二、个人中心 / KYC模块（fonesquare-kyc）</h3>'''

homepage_section = '''      <tr><td>60</td><td>Forgot Pwd</td><td>CLK</td><td>forgot_pwd_close</td><td>关闭弹层（× 或点遮罩）</td><td style="position: relative;">current_step, mode</td></tr>

      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">Homepage 首页（注册完成/登录成功后落地页）</td></tr>
      <tr><td>61</td><td>Homepage</td><td>PV</td><td>homepage_view</td><td>APP首页曝光（注册/登录成功后落地）</td><td style="position: relative;">source (registration_complete / login_success)</td></tr>
      <tr><td>62</td><td>Homepage</td><td>CLK</td><td>homepage_category_browse</td><td>点击分类入口（Phones/Accessories/Audio等）</td><td style="position: relative;">category_name</td></tr>
      <tr><td>63</td><td>Homepage</td><td>CLK</td><td>homepage_hot_deal_click</td><td>点击热门优惠商品卡片</td><td style="position: relative;">product_id, product_name</td></tr>
      <tr><td>64</td><td>Homepage</td><td>CLK</td><td>homepage_tab_switch</td><td>点击底部导航Tab（Home/Cart/Me）</td><td style="position: relative;">target_tab</td></tr>
    </tbody>
  </table>

  <h3>二、个人中心 / KYC模块（fonesquare-kyc）</h3>'''

assert old_anchor in text, "Login module closing anchor not found"
text = text.replace(old_anchor, homepage_section)
print("[OK] Added Homepage section to Login module")

# ──────────────────────────────────────────────
# 3. Add missing events to existing KYC sections
# ──────────────────────────────────────────────

# 3a. My Center: Add restricted_banner click after tab_switch row (67)
old = '''      <tr><td>67</td><td>My Center</td><td>CLK</td><td>my_center_tab_switch</td><td>点击底部Tab（Home/Cart/Me）</td><td style="position: relative;">target_tab</td></tr>

      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">Profile 身份认证'''
new = '''      <tr><td>67</td><td>My Center</td><td>CLK</td><td>my_center_tab_switch</td><td>点击底部Tab（Home/Cart/Me）</td><td style="position: relative;">target_tab</td></tr>
      <tr><td>67a</td><td>My Center</td><td>CLK</td><td>my_center_restricted_banner</td><td>账号受限用户点击红色横幅（跳转WhatsApp客服）</td><td style="position: relative;">account_status</td></tr>

      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">Profile 身份认证'''
assert old in text, "My Center tab_switch anchor not found"
text = text.replace(old, new)
print("[OK] Added my_center_restricted_banner event")

# 3b. Orders: Add order_card click after tab_filter row (76)
old = '''      <tr><td>76</td><td>My Orders</td><td>CLK</td><td>orders_tab_filter</td><td>切换订单筛选Tab</td><td style="position: relative;">filter_type (all/pending/pickup/aftersales/completed)</td></tr>

      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">Settings 设置</td></tr>'''
new = '''      <tr><td>76</td><td>My Orders</td><td>CLK</td><td>orders_tab_filter</td><td>切换订单筛选Tab</td><td style="position: relative;">filter_type (all/pending/pickup/aftersales/completed)</td></tr>
      <tr><td>76a</td><td>My Orders</td><td>CLK</td><td>orders_card_click</td><td>点击订单卡片进入订单详情</td><td style="position: relative;">order_id, order_status</td></tr>

      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">Settings 设置</td></tr>'''
assert old in text, "Orders tab_filter anchor not found"
text = text.replace(old, new)
print("[OK] Added orders_card_click event")

# 3c. Settings: Add login_methods click after identity_verify (78) — insert before change_pwd (79)
old = '''      <tr><td>78</td><td>Settings</td><td>CLK</td><td>settings_identity_verify</td><td>点击 Identity Verification</td><td style="position: relative;">kyc_status</td></tr>
      <tr><td>79</td><td>Settings</td><td>CLK</td><td>settings_change_pwd</td><td>点击 Change Password</td><td style="position: relative;">—</td></tr>'''
new = '''      <tr><td>78</td><td>Settings</td><td>CLK</td><td>settings_identity_verify</td><td>点击 Identity Verification</td><td style="position: relative;">kyc_status</td></tr>
      <tr><td>78a</td><td>Settings</td><td>CLK</td><td>settings_login_methods</td><td>点击 Login Methods（管理登录方式）</td><td style="position: relative;">—</td></tr>
      <tr><td>79</td><td>Settings</td><td>CLK</td><td>settings_change_pwd</td><td>点击 Change Password</td><td style="position: relative;">—</td></tr>'''
assert old in text, "Settings identity_verify anchor not found"
text = text.replace(old, new)
print("[OK] Added settings_login_methods event")

# 3d. Help & Support: Add FAQ click after email_support (91)
old = '''      <tr><td>91</td><td>Help &amp; Support</td><td>CLK</td><td>help_email_support</td><td>点击 Email Support</td><td style="position: relative;">—</td></tr>

      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">Privacy Policy'''
new = '''      <tr><td>91</td><td>Help &amp; Support</td><td>CLK</td><td>help_email_support</td><td>点击 Email Support</td><td style="position: relative;">—</td></tr>
      <tr><td>91a</td><td>Help &amp; Support</td><td>CLK</td><td>help_faq</td><td>点击 FAQ 常见问题</td><td style="position: relative;">—</td></tr>

      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">Privacy Policy'''
assert old in text, "Help email_support anchor not found"
text = text.replace(old, new)
print("[OK] Added help_faq event")

# ──────────────────────────────────────────────
# 4. Add KYC Dup Conflict section (after existing KYC Dup section)
# ──────────────────────────────────────────────

old = '''      <tr><td>74h</td><td>KYC Dup Done</td><td>CLK</td><td>kyc_dup_done_continue</td><td>点击「CONTINUE」进入已认证账号</td><td style="position: relative;">—</td></tr>

      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">My Orders 订单列表</td></tr>'''
new = '''      <tr><td>74h</td><td>KYC Dup Done</td><td>CLK</td><td>kyc_dup_done_continue</td><td>点击「CONTINUE」进入已认证账号</td><td style="position: relative;">—</td></tr>

      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">KYC 重复身份 — 登录方式冲突（V1.4 新增）</td></tr>
      <tr><td>74i</td><td>KYC Dup Conflict</td><td>PV</td><td>kyc_dup_conflict_view</td><td>登录方式类型冲突页曝光（已认证账号已有相同类型登录方式）</td><td style="position: relative;">conflict_type (email/phone/whatsapp)</td></tr>
      <tr><td>74j</td><td>KYC Dup Conflict</td><td>CLK</td><td>kyc_dup_conflict_go_login</td><td>点击「Go to Login / 前往登录」</td><td style="position: relative;">—</td></tr>
      <tr><td>74k</td><td>KYC Dup Conflict</td><td>CLK</td><td>kyc_dup_conflict_use_other</td><td>点击「Use a different ID / 使用其他证件」</td><td style="position: relative;">—</td></tr>

      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">My Orders 订单列表</td></tr>'''
assert old in text, "KYC Dup Done anchor not found"
text = text.replace(old, new)
print("[OK] Added KYC Dup Conflict section")

# ──────────────────────────────────────────────
# 5. Add Login Methods, Add Method, Verify Phone sections
# ──────────────────────────────────────────────

# Insert after About section, before closing </tbody> of KYC table
old = '''      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">About 关于</td></tr>
      <tr><td>93</td><td>About</td><td>PV</td><td>about_view</td><td>关于页曝光</td><td style="position: relative;">app_version</td></tr>
    </tbody>
  </table>

  <h3>三、核心转化漏斗埋点</h3>'''
new = '''      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">About 关于</td></tr>
      <tr><td>93</td><td>About</td><td>PV</td><td>about_view</td><td>关于页曝光</td><td style="position: relative;">app_version</td></tr>

      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">Login Methods 登录方式管理（V1.4 新增）</td></tr>
      <tr><td>94</td><td>Login Methods</td><td>PV</td><td>login_methods_view</td><td>登录方式管理页曝光</td><td style="position: relative;">methods_count, has_phone, has_email, has_whatsapp</td></tr>
      <tr><td>95</td><td>Login Methods</td><td>CLK</td><td>login_methods_add_click</td><td>点击「Add Login Method」或安全提示引导</td><td style="position: relative;">entry (add_button / nudge_banner)</td></tr>

      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">Add Login Method 添加登录方式（V1.4 新增）</td></tr>
      <tr><td>96</td><td>Add Method</td><td>PV</td><td>add_method_view</td><td>添加登录方式页曝光</td><td style="position: relative;">available_types</td></tr>
      <tr><td>97</td><td>Add Method</td><td>CLK</td><td>add_method_type_select</td><td>选择登录方式类型（Phone/Email/WhatsApp）</td><td style="position: relative;">selected_type</td></tr>
      <tr><td>98</td><td>Add Method</td><td>CLK</td><td>add_method_send_code</td><td>点击 SEND VERIFICATION CODE</td><td style="position: relative;">method_type, phone_country_code</td></tr>

      <tr><td colspan="6" style="background: rgb(248, 250, 252); font-weight: 600; position: relative;">Verify Phone 验证手机号（V1.4 新增）</td></tr>
      <tr><td>99</td><td>Verify Phone</td><td>PV</td><td>verify_phone_view</td><td>验证手机号OTP页曝光</td><td style="position: relative;">phone_masked</td></tr>
      <tr><td>100</td><td>Verify Phone</td><td>CLK</td><td>verify_phone_submit</td><td>点击 VERIFY 提交验证码</td><td style="position: relative;">—</td></tr>
      <tr><td>101</td><td>Verify Phone</td><td>RESULT</td><td>verify_phone_result</td><td>手机号绑定结果</td><td style="position: relative;">success (bool), error_code</td></tr>
      <tr><td>102</td><td>Verify Phone</td><td>CLK</td><td>verify_phone_resend</td><td>点击重新发送验证码</td><td style="position: relative;">resend_count</td></tr>
    </tbody>
  </table>

  <h3>三、核心转化漏斗埋点</h3>'''
assert old in text, "About section anchor not found"
text = text.replace(old, new)
print("[OK] Added Login Methods, Add Method, Verify Phone sections")

# ──────────────────────────────────────────────
# 6. Update registration funnel to include homepage_view
# ──────────────────────────────────────────────

old_funnel = '''<tr><td><strong>注册转化漏斗</strong></td><td>splash_view → login_view → login_btn_phone / login_btn_whatsapp / login_btn_email → sms_otp_verify / wa_otp_verify / email_otp_verify → set_pwd_submit → 进入首页</td><td style="position: relative;">整体注册转化率、各步流失率（密码必填，无跳过和结果页）</td></tr>'''
new_funnel = '''<tr><td><strong>注册转化漏斗</strong></td><td>splash_view → login_view → login_btn_phone / login_btn_whatsapp / login_btn_email → sms_otp_verify / wa_otp_verify / email_otp_verify → set_pwd_submit → reg_done_view → homepage_view</td><td style="position: relative;">整体注册转化率、各步流失率（密码必填→注册完成→首页）</td></tr>'''
assert old_funnel in text, "Registration funnel not found"
text = text.replace(old_funnel, new_funnel)
print("[OK] Updated registration funnel")

# Also add Login Methods funnel
old_funnel2 = '''<tr><td><strong>密码找回漏斗</strong></td><td>forgot_pwd_view → forgot_pwd_send_code → forgot_pwd_verify → forgot_pwd_change → forgot_pwd_result</td><td style="position: relative;">找回完成率</td></tr>'''
new_funnel2 = '''<tr><td><strong>密码找回漏斗</strong></td><td>forgot_pwd_view → forgot_pwd_send_code → forgot_pwd_verify → forgot_pwd_change → forgot_pwd_result</td><td style="position: relative;">找回完成率</td></tr>
      <tr><td><strong>登录方式绑定漏斗</strong></td><td>login_methods_view → login_methods_add_click → add_method_view → add_method_type_select → add_method_send_code → verify_phone_view → verify_phone_submit → verify_phone_result</td><td style="position: relative;">绑定发起率、验证完成率、绑定成功率</td></tr>'''
assert old_funnel2 in text, "Password recovery funnel not found"
text = text.replace(old_funnel2, new_funnel2)
print("[OK] Added login methods binding funnel")

# ──────────────────────────────────────────────
# 7. Update the tracking range info box
# ──────────────────────────────────────────────
old_info = '''<div><strong>埋点范围</strong>：覆盖登录注册（fonesquare-login）和个人中心/KYC（fonesquare-kyc）两个模块的全部页面与核心交互。埋点类型分为：<strong>PV</strong>（页面曝光）、<strong>CLK</strong>（点击事件）、<strong>INPUT</strong>（输入/提交事件）、<strong>RESULT</strong>（结果回调）。</div>'''
new_info = '''<div><strong>埋点范围</strong>：覆盖登录注册（fonesquare-login）和个人中心/KYC（fonesquare-kyc）两个模块的全部页面与核心交互，共计 <strong>102</strong> 项埋点事件。埋点类型分为：<strong>PV</strong>（页面曝光）、<strong>CLK</strong>（点击事件）、<strong>INPUT</strong>（输入/提交事件）、<strong>RESULT</strong>（结果回调）。已废弃的历史埋点不再展示。</div>'''
assert old_info in text, "Info box not found"
text = text.replace(old_info, new_info)
print("[OK] Updated info box")

# ──────────────────────────────────────────────
# Final: write
# ──────────────────────────────────────────────
open(FILE, 'w', encoding='utf-8').write(text)
new_len = len(text)
print(f"\n✅ Done. File: {orig_len} → {new_len} chars (diff: {new_len - orig_len:+d})")
