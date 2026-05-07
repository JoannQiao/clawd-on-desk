# 32-analytics — 埋点事件清单

> **来源**：FoneSquare PRD v2 — 埋点需求  
> **状态**：Draft  
> **最后更新**：2026-05-07

---

## 概述

### 埋点范围

覆盖 **APP 端**（登录注册 + 个人中心/KYC）和 **Web 后台**（商家管理 + 下载中心 + 系统级）两端的全部页面与核心交互。

### 埋点类型

| 类型 | 代码 | 说明 |
|---|---|---|
| 页面曝光 | `PV` | 页面展示时触发 |
| 点击事件 | `CLK` | 用户主动点击时触发 |
| 输入/提交 | `INPUT` | 用户输入完成或提交表单时触发 |
| 结果回调 | `RESULT` | 异步操作返回结果时触发 |

### 公共参数（所有事件默认携带）

| 参数 | 类型 | 说明 |
|---|---|---|
| `event_id` | string | 唯一事件 ID |
| `event_name` | string | 事件名称 |
| `event_type` | enum | PV / CLK / INPUT / RESULT |
| `timestamp` | string | 事件触发时间（ISO 8601 + 偏移量） |
| `user_id` | string | 用户 ID（未登录为匿名 ID） |
| `session_id` | string | 会话 ID |
| `platform` | enum | `ios` / `android` / `web` |
| `app_version` | string | APP 版本号（Web 端为部署版本） |
| `device_os` | string | 操作系统及版本 |
| `locale` | string | 当前语言设置 |
| `screen_name` | string | 当前页面标识 |

---

## 一、AUTH — 登录注册模块（APP 端）

### 1.1 Splash 开屏页

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| AUTH-001 | `splash_view` | PV | APP 启动，开屏页曝光 | `app_version`, `device_os` | APP |
| AUTH-002 | `splash_tap_continue` | CLK | 用户点击屏幕跳过开屏 | `stay_duration_ms` | APP |

### 1.2 Login 登录首页

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| AUTH-003 | `login_view` | PV | 登录页曝光 | `default_tab` (phone/pwd), `locale` | APP |
| AUTH-004 | `login_tab_switch` | CLK | 切换 Phone / Password Tab | `target_tab` | APP |
| AUTH-005 | `login_lang_switch` | CLK | 切换语言 | `from_lang`, `to_lang` | APP |
| AUTH-006 | `login_country_picker_open` | CLK | 打开国家/区号选择器 | `current_code` | APP |
| AUTH-007 | `login_country_select` | CLK | 选择国家/区号 | `country_code`, `country_name` | APP |
| AUTH-008 | `login_btn_phone` | CLK | 点击 LOGIN / SIGN UP（手机号） | `phone_country_code` | APP |
| AUTH-009 | `login_btn_whatsapp` | CLK | 点击 WhatsApp 登录入口 | — | APP |
| AUTH-010 | `login_btn_email` | CLK | 点击 Email 登录入口 | — | APP |
| AUTH-011 | `login_btn_pwd_login` | CLK | 密码 Tab 点击 LOGIN | — | APP |
| AUTH-012 | `login_btn_forgot_pwd` | CLK | 点击「Forgot password?」 | — | APP |
| AUTH-013 | `login_terms_click` | CLK | 点击 Terms of Service / Privacy Policy | `link_type` (terms/privacy) | APP |

### 1.3 SMS OTP 短信验证

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| AUTH-014 | `sms_otp_view` | PV | 短信验证码页曝光 | `phone_masked` | APP |
| AUTH-015 | `sms_otp_input_complete` | INPUT | 用户输入完 6 位验证码 | `input_duration_ms` | APP |
| AUTH-016 | `sms_otp_verify` | CLK | 点击 VERIFY & CONTINUE | — | APP |
| AUTH-017 | `sms_otp_result` | RESULT | 验证码校验结果回调 | `success` (bool), `error_code` | APP |
| AUTH-018 | `sms_otp_resend` | CLK | 点击重新发送验证码 | `resend_count` | APP |

### 1.4 WhatsApp 登录

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| AUTH-019 | `wa_input_view` | PV | WhatsApp 号码输入页曝光 | — | APP |
| AUTH-020 | `wa_send_code` | CLK | 点击 SEND WHATSAPP CODE | `phone_country_code` | APP |
| AUTH-021 | `wa_otp_view` | PV | WhatsApp 验证码页曝光 | `phone_masked` | APP |
| AUTH-022 | `wa_otp_verify` | CLK | 点击 VERIFY & CONTINUE | — | APP |
| AUTH-023 | `wa_otp_result` | RESULT | WhatsApp OTP 校验结果 | `success` (bool), `error_code` | APP |

### 1.5 Email 登录

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| AUTH-024 | `email_input_view` | PV | 邮箱输入页曝光 | — | APP |
| AUTH-025 | `email_send_code` | CLK | 点击 SEND VERIFICATION CODE | `email_domain` | APP |
| AUTH-026 | `email_switch_pwd_login` | CLK | 点击「Login with password」 | — | APP |
| AUTH-027 | `email_otp_view` | PV | 邮箱验证码页曝光 | `email_masked` | APP |
| AUTH-028 | `email_otp_verify` | CLK | 点击 VERIFY & CONTINUE | — | APP |
| AUTH-029 | `email_otp_resend` | CLK | 点击 Resend code | `resend_count` | APP |
| AUTH-030 | `email_otp_result` | RESULT | 邮箱验证码校验结果 | `success` (bool), `error_code` | APP |

### 1.6 设置密码

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| AUTH-031 | `set_pwd_view` | PV | 设置密码页曝光 | `source` (phone/whatsapp/email) | APP |
| AUTH-032 | `set_pwd_submit` | CLK | 点击 SET PASSWORD | `pwd_strength` | APP |

### 1.7 密码登录

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| AUTH-033 | `pwd_login_view` | PV | 密码登录页曝光 | — | APP |
| AUTH-034 | `pwd_login_submit` | CLK | 点击 LOGIN | — | APP |
| AUTH-035 | `pwd_login_result` | RESULT | 密码登录结果 | `success` (bool), `error_type` | APP |

### 1.8 登录/注册成功

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| AUTH-036 | `login_ok_view` | PV | 登录成功过渡页曝光（"Welcome Back!" + 自动跳转动画） | `login_method` | APP |
| AUTH-037 | `login_ok_redirect` | RESULT | 自动跳转首页完成（~2.5s 后） | `duration_ms` | APP |
| AUTH-038 | `reg_done_view` | PV | 注册完成过渡页曝光（密码设置后展示） | `reg_method` (phone/whatsapp/email) | APP |
| AUTH-039 | `reg_done_redirect` | RESULT | 自动跳转首页完成 | `duration_ms` | APP |

### 1.9 忘记密码

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| AUTH-040 | `forgot_pwd_view` | PV | 忘记密码弹层打开 | — | APP |
| AUTH-041 | `forgot_pwd_tab_switch` | CLK | 切换验证模式 Tab（Phone / Email） | `mode` (phone/email) | APP |
| AUTH-042 | `forgot_pwd_send_code` | CLK | Step1 点击 SEND CODE | `mode` (phone/email), `phone_country_code` / `email` | APP |
| AUTH-043 | `forgot_pwd_verify` | CLK | Step2 点击 VERIFY | `mode` (phone/email) | APP |
| AUTH-044 | `forgot_pwd_otp_result` | RESULT | 忘记密码 OTP 校验结果 | `success` (bool), `mode` (phone/email) | APP |
| AUTH-045 | `forgot_pwd_change` | CLK | Step3 点击 CHANGE PASSWORD | — | APP |
| AUTH-046 | `forgot_pwd_result` | RESULT | 密码修改成功/失败 | `success` (bool) | APP |
| AUTH-047 | `forgot_pwd_close` | CLK | 关闭弹层（× 或点遮罩） | `current_step`, `mode` | APP |

### 1.10 Homepage 首页

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| AUTH-048 | `homepage_view` | PV | APP 首页曝光（注册/登录成功后落地） | `source` (registration_complete / login_success) | APP |
| AUTH-049 | `homepage_category_browse` | CLK | 点击分类入口（Phones/Accessories/Audio 等） | `category_name` | APP |
| AUTH-050 | `homepage_hot_deal_click` | CLK | 点击热门优惠商品卡片 | `product_id`, `product_name` | APP |
| AUTH-051 | `homepage_tab_switch` | CLK | 点击底部导航 Tab（Home/Cart/Me） | `target_tab` | APP |

---

## 二、KYC — 身份认证模块（APP 端）

### 2.1 My Center 个人中心

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| KYC-001 | `my_center_view` | PV | 个人中心页曝光 | `kyc_status` (unverified/verified) | APP |
| KYC-002 | `my_center_wa_support` | CLK | 点击右上角 WhatsApp 客服 | — | APP |
| KYC-003 | `me_kyc_entry` | CLK | 点击 KYC 认证入口（Me 页面） | `kyc_status` | APP |
| KYC-004 | `my_center_view_orders` | CLK | 点击 View All 查看订单 | — | APP |
| KYC-005 | `my_center_order_stat` | CLK | 点击订单状态数字（Unpaid/Paid/Cancelled） | `order_status_type` | APP |
| KYC-006 | `my_center_settings` | CLK | 点击 Settings | — | APP |
| KYC-007 | `my_center_help` | CLK | 点击 Help & Support | — | APP |
| KYC-008 | `my_center_tab_switch` | CLK | 点击底部 Tab（Home/Cart/Me） | `target_tab` | APP |
| KYC-009 | `my_center_restricted_banner` | CLK | 账号受限用户点击红色横幅（跳转 WhatsApp 客服） | `account_status` | APP |

### 2.2 Profile — KYC 身份认证

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| KYC-010 | `kyc_profile_view` | PV | KYC 身份认证页曝光 | `entry_source` (banner/settings) | APP |
| KYC-011 | `kyc_region_picker_open` | CLK | 打开三级联动地区选择器 | — | APP |
| KYC-012 | `kyc_country_select` | CLK | 选择国家/地区（面包屑第一级） | `country_code` | APP |
| KYC-013 | `kyc_province_select` | CLK | 选择省份/州（面包屑第二级） | `country_code`, `province_id` | APP |
| KYC-014 | `kyc_city_select` | CLK | 选择城市/区（面包屑第三级） | `country_code`, `province_id`, `city_name` | APP |
| KYC-015 | `kyc_id_type_select` | CLK | 选择证件类型（根据地区动态展示） | `id_type` (hk_id/mo_id/cn_id/passport), `country_code` | APP |
| KYC-016 | `kyc_id_upload` | CLK | 点击上传证件照片 | `id_type`, `side` (front/back/info_page) | APP |
| KYC-017 | `kyc_ocr_result` | RESULT | OCR 识别结果 | `success` (bool), `fields_recognized` | APP |
| KYC-018 | `kyc_biz_expand` | CLK | 展开企业信息区（引导文案引导填写） | — | APP |
| KYC-019 | `kyc_submit` | CLK | 点击 SUBMIT & CONTINUE | `has_biz_info` (bool), `id_type`, `country_code` | APP |
| KYC-020 | `kyc_skip` | CLK | 点击 Skip for now | — | APP |

### 2.3 KYC 重复身份处理

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| KYC-021 | `kyc_dup_detected_view` | PV | 重复身份检测结果页曝光 | `verified_account_phone` | APP |
| KYC-022 | `kyc_dup_login_btn` | CLK | 点击「LOG IN TO VERIFIED ACCOUNT」 | — | APP |
| KYC-023 | `kyc_dup_supplement_view` | PV | 补全登录信息页曝光 | — | APP |
| KYC-024 | `kyc_dup_supplement_submit` | CLK | 点击「VERIFY & LINK」补全信息 | `supplement_type` (email/phone) | APP |
| KYC-025 | `kyc_dup_otp_view` | PV | 二次 OTP 验证页曝光 | — | APP |
| KYC-026 | `kyc_dup_otp_verify` | CLK | 输入 OTP 并验证 | `success` (bool) | APP |
| KYC-027 | `kyc_dup_done_view` | PV | 账号迁移完成页曝光 | — | APP |
| KYC-028 | `kyc_dup_done_continue` | CLK | 点击「CONTINUE」进入已认证账号 | — | APP |

### 2.4 KYC 重复身份 — 登录方式冲突

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| KYC-029 | `kyc_dup_conflict_view` | PV | 登录方式类型冲突页曝光 | `conflict_type` (email/phone/whatsapp) | APP |
| KYC-030 | `kyc_dup_conflict_go_login` | CLK | 点击「Go to Login / 前往登录」 | — | APP |
| KYC-031 | `kyc_dup_conflict_use_other` | CLK | 点击「Use a different ID / 使用其他证件」 | — | APP |

### 2.5 订单相关

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| KYC-032 | `orders_view` | PV | 订单列表页曝光 | `total_orders` | APP |
| KYC-033 | `orders_tab_filter` | CLK | 切换订单筛选 Tab | `filter_type` (all/pending/pickup/aftersales/completed) | APP |
| KYC-034 | `orders_card_click` | CLK | 点击订单卡片进入订单详情 | `order_id`, `order_status` | APP |

### 2.6 Settings 设置

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| KYC-035 | `settings_view` | PV | 设置页曝光 | — | APP |
| KYC-036 | `settings_identity_verify` | CLK | 点击 Identity Verification | `kyc_status` | APP |
| KYC-037 | `settings_login_methods` | CLK | 点击 Login Methods（管理登录方式） | — | APP |
| KYC-038 | `settings_change_pwd` | CLK | 点击 Change Password | — | APP |
| KYC-039 | `settings_language` | CLK | 点击 Language | `current_lang` | APP |
| KYC-040 | `settings_privacy` | CLK | 点击 Privacy Policy | — | APP |
| KYC-041 | `settings_about` | CLK | 点击 About FoneSquare | — | APP |
| KYC-042 | `settings_logout` | CLK | 点击 Log Out | — | APP |

### 2.7 修改密码

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| KYC-043 | `change_pwd_view` | PV | 修改密码页曝光 | — | APP |
| KYC-044 | `change_pwd_submit` | CLK | 点击 UPDATE PASSWORD | — | APP |
| KYC-045 | `change_pwd_result` | RESULT | 密码修改结果 | `success` (bool) | APP |

### 2.8 语言选择

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| KYC-046 | `lang_select_view` | PV | 语言选择页曝光 | `current_lang` | APP |
| KYC-047 | `lang_select_change` | CLK | 选择语言 | `from_lang`, `to_lang` | APP |

### 2.9 Help & Support / Privacy / About

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| KYC-048 | `help_support_view` | PV | 帮助与支持页曝光 | — | APP |
| KYC-049 | `help_wa_support` | CLK | 点击 WhatsApp Support | — | APP |
| KYC-050 | `help_email_support` | CLK | 点击 Email Support | — | APP |
| KYC-051 | `help_faq` | CLK | 点击 FAQ 常见问题 | — | APP |
| KYC-052 | `privacy_view` | PV | 隐私政策页曝光 | — | APP |
| KYC-053 | `about_view` | PV | 关于页曝光 | `app_version` | APP |

### 2.10 登录方式管理

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| KYC-054 | `login_methods_view` | PV | 登录方式管理页曝光 | `methods_count`, `has_phone`, `has_email`, `has_whatsapp` | APP |
| KYC-055 | `login_methods_add_click` | CLK | 点击「Add Login Method」或安全提示引导 | `entry` (add_button / nudge_banner) | APP |
| KYC-056 | `add_method_view` | PV | 添加登录方式页曝光 | `available_types` | APP |
| KYC-057 | `add_method_type_select` | CLK | 选择登录方式类型（Phone/Email/WhatsApp） | `selected_type` | APP |
| KYC-058 | `add_method_send_code` | CLK | 点击 SEND VERIFICATION CODE | `method_type`, `phone_country_code` | APP |

### 2.11 验证手机号绑定

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| KYC-059 | `verify_phone_view` | PV | 验证手机号 OTP 页曝光 | `phone_masked` | APP |
| KYC-060 | `verify_phone_submit` | CLK | 点击 VERIFY 提交验证码 | — | APP |
| KYC-061 | `verify_phone_result` | RESULT | 手机号绑定结果 | `success` (bool), `error_code` | APP |
| KYC-062 | `verify_phone_resend` | CLK | 点击重新发送验证码 | `resend_count` | APP |

### 2.12 注册流程中的 Profile（下单前校验触发）

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| KYC-063 | `profile_view` | PV | Profile 页曝光 | `source` (order_check / my_center) | APP |
| KYC-064 | `profile_region_picker_open` | CLK | 打开三级联动地区选择器 | — | APP |
| KYC-065 | `profile_country_select` | CLK | 选择国家/地区（第一级） | `country_code` | APP |
| KYC-066 | `profile_province_select` | CLK | 选择省份/州（第二级） | `country_code`, `province_id` | APP |
| KYC-067 | `profile_city_select` | CLK | 选择城市/区（第三级） | `country_code`, `province_id`, `city_name` | APP |
| KYC-068 | `profile_id_type_select` | CLK | 选择证件类型（根据地区动态展示） | `id_type` (hk_id/mo_id/cn_id/passport), `country_code` | APP |
| KYC-069 | `profile_id_upload` | CLK | 点击上传证件照片 | `id_type`, `side` (front/back/info_page) | APP |
| KYC-070 | `profile_ocr_result` | RESULT | OCR 识别结果回调 | `success` (bool), `fields_recognized` | APP |
| KYC-071 | `profile_biz_expand` | CLK | 展开企业信息区 | — | APP |
| KYC-072 | `profile_biz_upload` | CLK | 上传营业执照 | — | APP |
| KYC-073 | `profile_submit` | CLK | 点击 SUBMIT & CONTINUE | `has_biz_info` (bool), `id_type` | APP |

---

## 三、MERCHANT_LIST — 商家列表（Web 后台）

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| ML-001 | `merchant_list_view` | PV | 商家列表页曝光（登录后默认首页） | `role` (admin/sales), `total_count` | Web |
| ML-002 | `merchant_search` | CLK | 点击「查询」按钮执行筛选 | `filters` (name/type/status/sales/auth_status), `result_count` | Web |
| ML-003 | `merchant_filter_change` | CLK | 修改筛选条件（切换下拉、输入关键词） | `filter_field`, `filter_value` | Web |
| ML-004 | `merchant_filter_reset` | CLK | 点击「重置」清空筛选条件 | — | Web |
| ML-005 | `merchant_export` | CLK | 点击「导出」按钮触发列表导出 | `filter_snapshot`, `total_count` | Web |
| ML-006 | `merchant_status_change` | CLK | 修改商家状态（启用/停用） | `merchant_id`, `from_status`, `to_status` | Web |
| ML-007 | `merchant_row_view_click` | CLK | 点击列表行「查看」进入详情 | `merchant_id` | Web |
| ML-008 | `merchant_page_change` | CLK | 切换分页 | `page_number`, `page_size` | Web |
| ML-009 | `merchant_add_entry` | CLK | 点击「添加商家」按钮 | — | Web |

---

## 四、MERCHANT_DETAIL — 商家详情（Web 后台）

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| MD-001 | `merchant_detail_view` | PV | 商家详情页曝光 | `merchant_id`, `active_tab` | Web |
| MD-002 | `merchant_detail_tab_switch` | CLK | 切换详情页 Tab | `from_tab`, `to_tab` | Web |
| MD-003 | `merchant_edit_start` | CLK | 点击「编辑信息」按钮 | `merchant_id` | Web |
| MD-004 | `merchant_edit_save` | CLK | 编辑后点击保存 | `merchant_id`, `changed_fields` | Web |
| MD-005 | `merchant_edit_cancel` | CLK | 编辑后点击取消 | `merchant_id` | Web |
| MD-006 | `kyc_view_raw` | CLK | 查看 KYC 原始认证材料（证件照片等） | `merchant_id`, `doc_type` | Web |
| MD-007 | `limit_config_save` | CLK | 保存限额配置 | `merchant_id`, `daily_limit`, `deposit_amount` | Web |
| MD-008 | `limit_config_validate_fail` | RESULT | 限额校验失败（不满足「保证金×10 = 限额上限」规则） | `merchant_id`, `error_type` | Web |
| MD-009 | `deposit_upload` | CLK | 上传保证金转账凭证 | `merchant_id`, `file_count` | Web |
| MD-010 | `deposit_status_change` | CLK | 修改保证金状态（待确认 → 已确认） | `merchant_id`, `from_status`, `to_status` | Web |
| MD-011 | `advisor_bind` | CLK | 绑定维护人 | `merchant_id`, `advisor_id` | Web |
| MD-012 | `advisor_change` | CLK | 更换维护人 | `merchant_id`, `from_advisor_id`, `to_advisor_id` | Web |
| MD-013 | `advisor_unbind` | CLK | 解绑维护人 | `merchant_id`, `advisor_id` | Web |
| MD-014 | `merchant_disable` | CLK | 点击「停用」商家 | `merchant_id` | Web |
| MD-015 | `merchant_log_view` | PV | 查看操作日志 Tab | `merchant_id` | Web |

---

## 五、ADD_MERCHANT — 添加商家（Web 后台）

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| AM-001 | `add_merchant_view` | PV | 添加商家页曝光 | `role` (admin/sales) | Web |
| AM-002 | `add_merchant_form_fill` | INPUT | 填写表单字段 | `field_name`, `field_value_type` | Web |
| AM-003 | `add_merchant_id_upload` | CLK | 上传 KYC 证件照片 | `id_type`, `side` | Web |
| AM-004 | `add_merchant_ocr_result` | RESULT | OCR 识别结果 | `success` (bool), `fields_recognized` | Web |
| AM-005 | `add_merchant_biz_expand` | CLK | 展开企业信息区域 | — | Web |
| AM-006 | `add_merchant_submit` | CLK | 点击提交添加商家 | `has_biz_info` (bool), `id_type`, `merchant_type` | Web |
| AM-007 | `add_merchant_success` | RESULT | 添加商家成功 | `merchant_id` | Web |
| AM-008 | `add_merchant_fail` | RESULT | 添加商家失败 | `error_type` (duplicate_id/sanction_hit/validation_error) | Web |
| AM-009 | `add_merchant_sanction_check` | RESULT | 制裁名单校验结果 | `success` (bool), `hit_list` | Web |
| AM-010 | `add_merchant_cancel` | CLK | 点击取消返回列表 | `fields_filled_count` | Web |

---

## 六、DOWNLOAD — 下载中心（Web 后台）

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| DL-001 | `download_center_view` | PV | 下载中心页曝光 | `file_count`, `role` | Web |
| DL-002 | `file_download` | CLK | 点击下载文件 | `file_id`, `file_type`, `file_size` | Web |
| DL-003 | `file_regenerate` | CLK | 点击重新生成文件 | `file_id`, `file_type` | Web |
| DL-004 | `file_expired_view` | PV | 查看已过期文件提示 | `file_id`, `expired_days` | Web |

---

## 七、SYSTEM — 系统级事件（双端）

| 事件ID | 事件名 | 类型 | 触发时机 | 参数 | 所属端 |
|---|---|---|---|---|---|
| SYS-001 | `language_switch` | CLK | 切换语言（APP 设置页 / Web 后台 Header） | `from_lang`, `to_lang`, `platform` | APP / Web |
| SYS-002 | `page_view` | PV | 通用页面曝光（兜底，无专属埋点的页面使用） | `page_name`, `page_path`, `referrer` | APP / Web |
| SYS-003 | `api_error` | RESULT | 接口请求返回错误 | `endpoint`, `http_status`, `error_code`, `error_message` | APP / Web |
| SYS-004 | `session_start` | RESULT | 会话开始（APP 启动 / Web 登录） | `platform`, `device_info`, `locale` | APP / Web |
| SYS-005 | `session_end` | RESULT | 会话结束（APP 退出 / Web 关闭 / 登出） | `session_duration_ms`, `pages_viewed` | APP / Web |
| SYS-006 | `network_error` | RESULT | 网络请求失败（超时 / 断网） | `endpoint`, `error_type` (timeout/offline/dns) | APP |
| SYS-007 | `app_crash` | RESULT | APP 崩溃（异常退出） | `crash_stack`, `last_screen` | APP |
| SYS-008 | `app_foreground` | PV | APP 从后台切换到前台 | `bg_duration_ms` | APP |
| SYS-009 | `app_background` | CLK | APP 切换到后台 | `fg_duration_ms` | APP |
| SYS-010 | `web_login` | RESULT | Web 后台登录 | `login_method` (ob_account), `success` (bool) | Web |
| SYS-011 | `web_logout` | CLK | Web 后台登出 | — | Web |

---

## 八、核心转化漏斗

以下漏斗事件为数据分析的关键链路，需确保**上报率 ≥ 99.9%**，支持实时看板。

### 8.1 注册转化漏斗

```
splash_view → login_view → login_btn_phone / login_btn_whatsapp / login_btn_email
→ sms_otp_verify / wa_otp_verify / email_otp_verify
→ set_pwd_submit → reg_done_view → homepage_view
```

**关键指标**：整体注册转化率、各步流失率（密码必填→注册完成→首页）

### 8.2 KYC 认证漏斗

```
me_kyc_entry / order_check_kyc → kyc_profile_view → kyc_region_picker_open
→ kyc_country_select → kyc_id_type_select → kyc_id_upload
→ kyc_ocr_result → kyc_submit
```

**关键指标**：KYC 发起率、完成率、地区选择分布、证件类型分布、OCR 成功率

### 8.3 KYC 重复身份漏斗

```
kyc_dup_detected_view → kyc_dup_login_btn → kyc_dup_supplement_submit
→ kyc_dup_otp_verify → kyc_dup_done_continue
```

**关键指标**：重复身份检出率、补全成功率、OTP 验证通过率、迁移完成率

### 8.4 登录方式分布

```
login_btn_phone / login_btn_whatsapp / login_btn_email / pwd_login_submit
```

**关键指标**：各登录方式占比

### 8.5 密码找回漏斗

```
forgot_pwd_view → forgot_pwd_send_code → forgot_pwd_verify
→ forgot_pwd_change → forgot_pwd_result
```

**关键指标**：找回完成率

### 8.6 登录方式绑定漏斗

```
login_methods_view → login_methods_add_click → add_method_view
→ add_method_type_select → add_method_send_code
→ verify_phone_view → verify_phone_submit → verify_phone_result
```

**关键指标**：绑定发起率、验证完成率、绑定成功率

---

## 九、事件汇总统计

| 模块 | 事件数量 | 所属端 |
|---|---|---|
| AUTH（登录注册） | 51 | APP |
| KYC（身份认证 / 个人中心） | 73 | APP |
| MERCHANT_LIST（商家列表） | 9 | Web |
| MERCHANT_DETAIL（商家详情） | 15 | Web |
| ADD_MERCHANT（添加商家） | 10 | Web |
| DOWNLOAD（下载中心） | 4 | Web |
| SYSTEM（系统级） | 11 | APP / Web |
| **合计** | **173** | — |

> APP 端 PRD 原文定义 102 项事件；Web 后台与系统级为本规格新增，确保全端全链路可追踪。
