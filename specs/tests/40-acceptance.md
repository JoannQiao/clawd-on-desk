# FoneSquare 验收标准（Gherkin）

> 海外 B2B 二手手机交易平台 — APP端 + Web后台

---

## Feature 1: 用户登录注册

```gherkin
Feature: 用户登录注册
  作为 FoneSquare 用户
  我希望通过手机号/WhatsApp/邮箱登录或注册
  以便进入平台进行交易

  Background:
    Given 系统正常运行且网络连接正常

  # --- 手机号 OTP 登录 ---

  Scenario: 手机号OTP新用户首次登录自动注册
    Given 用户输入手机号 "+6281234567890" 且该手机号未注册
    When 用户点击 "获取验证码"
    And 用户在 5 分钟内输入正确的 6 位 OTP 验证码
    Then 系统自动创建新账号
    And 用户进入 "完善资料" 页面
    And 返回有效的 JWT access_token 和 refresh_token

  Scenario: 手机号OTP老用户登录
    Given 用户输入已注册手机号 "+6281234567890"
    When 用户点击 "获取验证码"
    And 用户在 5 分钟内输入正确的 6 位 OTP 验证码
    Then 用户成功登录并进入首页
    And 返回有效的 JWT access_token 和 refresh_token

  Scenario: OTP验证码60秒内不可重复发送
    Given 用户已点击 "获取验证码" 且未超过 60 秒
    When 用户再次点击 "获取验证码"
    Then 按钮置灰并显示倒计时
    And 提示 "请等待 XX 秒后重试"

  Scenario: OTP验证码超过5分钟过期
    Given 用户已获取 OTP 验证码
    When 用户在 5 分钟后输入该验证码
    Then 系统提示 "验证码已过期，请重新获取"
    And 验证码输入框清空

  Scenario: OTP连续5次输入错误锁定30分钟
    Given 用户已获取 OTP 验证码
    When 用户连续 5 次输入错误的验证码
    Then 系统提示 "错误次数过多，请 30 分钟后再试"
    And 该手机号在 30 分钟内无法再次请求验证码
    And 无法再次输入验证码

  # --- WhatsApp OTP 登录 ---

  Scenario: WhatsApp OTP成功登录
    Given 用户选择 "WhatsApp 登录" 并输入 WhatsApp 号码
    When 用户点击 "获取验证码"
    And 系统通过 WhatsApp 发送 OTP
    And 用户在 5 分钟内输入正确的 OTP
    Then 用户成功登录

  Scenario: WhatsApp号码格式校验
    Given 用户选择 "WhatsApp 登录"
    When 用户输入无效格式的号码 "abc123"
    Then 系统提示 "请输入有效的 WhatsApp 号码"
    And "获取验证码" 按钮不可点击

  # --- 邮箱密码登录/注册 ---

  Scenario: 邮箱密码注册成功
    Given 用户选择 "邮箱注册"
    When 用户输入有效邮箱 "user@example.com"
    And 用户设置密码 "Abc12345"（8-20位，包含字母和数字）
    And 用户确认密码一致
    And 用户点击 "注册"
    Then 系统发送验证邮件
    And 用户点击邮件中的验证链接后注册成功

  Scenario: 邮箱密码登录成功
    Given 用户已注册邮箱 "user@example.com" 且已验证
    When 用户输入正确的邮箱和密码
    And 点击 "登录"
    Then 用户成功登录并进入首页

  Scenario: 密码不符合规则被拒绝
    Given 用户在注册页面
    When 用户设置密码 "12345678"（纯数字，无字母）
    Then 系统提示 "密码需包含字母和数字，长度 8-20 位"
    And 注册按钮不可点击

  Scenario: 密码长度不满足要求
    Given 用户在注册页面
    When 用户设置密码 "Ab1"（少于8位）
    Then 系统提示 "密码需包含字母和数字，长度 8-20 位"

  # --- 忘记密码 ---

  Scenario: 忘记密码重置流程
    Given 用户在登录页面点击 "忘记密码"
    When 用户输入已注册邮箱
    And 系统发送重置密码邮件
    And 用户通过邮件链接设置新密码 "NewPass123"
    Then 密码重置成功
    And 用户可用新密码登录

  # --- JWT Token ---

  Scenario: JWT Token过期后自动刷新
    Given 用户已登录且 access_token 即将过期
    When 客户端使用 refresh_token 请求新 token
    Then 系统返回新的 access_token
    And 用户无需重新登录

  Scenario: refresh_token过期强制重新登录
    Given 用户的 refresh_token 已过期
    When 客户端尝试刷新 token
    Then 系统返回 401 状态码
    And 客户端跳转至登录页面

  # --- 多设备登录 ---

  Scenario: 多设备登录互踢
    Given 用户已在设备 A 登录
    When 用户在设备 B 使用同一账号登录
    Then 设备 A 的会话失效
    And 设备 A 显示 "您的账号已在其他设备登录"
    And 设备 B 正常使用
```

---

## Feature 2: KYC 身份认证

```gherkin
Feature: KYC 身份认证
  作为 FoneSquare 商家
  我希望完成 KYC 身份认证
  以便获得平台交易资格

  Background:
    Given 用户已登录且未完成 KYC 认证

  Scenario: 个人认证-印尼地区提交KTP证件成功
    Given 用户选择地区 "印尼"
    And 系统显示可用证件类型 "KTP"
    When 用户上传 KTP 正面照片
    And OCR 识别成功并自动填充姓名、证件号、有效期
    And 用户确认信息无误并提交
    Then 系统提示 "认证材料已提交，等待审核"
    And KYC 状态变更为 "审核中"

  Scenario: 个人认证-香港地区提交HKID
    Given 用户选择地区 "香港"
    And 系统显示可用证件类型 "HKID / Passport"
    When 用户上传 HKID 正面照片
    And OCR 识别成功
    And 用户确认信息并提交
    Then KYC 状态变更为 "审核中"

  Scenario: OCR识别失败用户手动修正
    Given 用户上传证件照片
    When OCR 识别结果中姓名为空或明显错误
    Then 系统允许用户手动修正各字段
    And 用户修正后点击 "确认提交"
    Then 认证材料正常提交

  Scenario: 制裁名单命中拒绝认证
    Given 用户提交 KYC 材料
    When 系统调用制裁名单检查接口
    And 返回结果为 "命中"
    Then 系统拒绝认证
    And KYC 状态变更为 "认证失败"
    And 显示原因 "身份信息异常，请联系客服"

  Scenario: 制裁名单检查超时降级处理
    Given 用户提交 KYC 材料
    When 系统调用制裁名单检查接口超时（>10秒）
    Then 系统标记为 "待人工复核"
    And KYC 状态变更为 "审核中"
    And 通知运营人员人工审核

  Scenario: 证件照片模糊无法识别
    Given 用户上传证件照片
    When 系统检测到照片模糊度低于阈值
    Then 系统提示 "照片不清晰，请重新拍摄"
    And 不允许提交

  Scenario: 证件已过期拒绝提交
    Given 用户上传证件照片且 OCR 识别有效期
    When 有效期早于当前日期
    Then 系统提示 "证件已过期，请使用有效证件"
    And 不允许提交

  Scenario: 企业认证提交营业执照
    Given 用户选择 "企业认证"
    When 用户上传营业执照照片
    And 填写公司名称、注册号、法人代表等信息
    And 点击 "提交认证"
    Then 系统提示 "企业认证材料已提交，等待审核"
    And KYC 状态变更为 "审核中"

  Scenario: 重新提交KYC认证
    Given 用户 KYC 状态为 "认证失败"
    When 用户点击 "重新认证"
    And 重新上传有效证件并提交
    Then KYC 状态变更为 "审核中"

  Scenario: KYC认证审核通过
    Given 运营人员在后台审核 KYC 材料
    When 运营人员点击 "通过"
    Then 用户 KYC 状态变更为 "已认证"
    And 系统发送通知告知用户认证通过
```

---

## Feature 3: 重复身份处理

```gherkin
Feature: 重复身份处理
  作为系统
  我需要在KYC认证时检测重复身份
  以防止一人多号和欺诈行为

  Background:
    Given 用户已提交 KYC 认证材料

  Scenario: 检测到重复身份-选择绑定主账号
    Given 系统检测到当前证件号已被账号 "A" 使用
    When 系统弹出 "检测到该证件已绑定其他账号" 提示
    And 用户选择 "绑定到已有账号"
    And 用户通过已有账号的 OTP 验证
    Then 当前账号与主账号 "A" 关联
    And 当前账号继承主账号的 KYC 状态

  Scenario: 检测到重复身份-选择使用新账号
    Given 系统检测到当前证件号已被账号 "A" 使用
    When 系统弹出 "检测到该证件已绑定其他账号" 提示
    And 用户选择 "使用当前新账号"
    Then 系统标记为人工复核
    And 通知运营人员处理重复身份

  Scenario: 重复身份绑定需OTP二次验证
    Given 用户选择 "绑定到已有账号"
    When 系统向已有账号的手机号发送 OTP
    And 用户输入正确的 OTP
    Then 绑定成功

  Scenario: 重复身份绑定OTP验证失败
    Given 用户选择 "绑定到已有账号"
    When 用户连续 3 次输入错误的 OTP
    Then 提示 "验证失败，请稍后再试"
    And 本次绑定操作取消

  Scenario: 未检测到重复身份正常通过
    Given 系统检测当前证件号未被任何账号使用
    When 制裁名单检查也通过
    Then KYC 认证流程正常继续
    And 不弹出重复身份提示
```

---

## Feature 4: 商家列表

```gherkin
Feature: 商家列表
  作为 Web 后台管理人员
  我希望查看和管理所有商家
  以便进行日常运营操作

  Background:
    Given 管理员已登录 Web 后台

  Scenario: 按商家名称搜索
    Given 商家列表页面已加载
    When 管理员在搜索框输入 "TechMobile"
    And 点击 "搜索"
    Then 列表仅显示名称包含 "TechMobile" 的商家

  Scenario: 按商家类型筛选
    Given 商家列表页面已加载
    When 管理员在类型筛选中选择 "个人商家"
    Then 列表仅显示类型为 "个人商家" 的记录

  Scenario: 按状态筛选
    Given 商家列表页面已加载
    When 管理员在状态筛选中选择 "已停用"
    Then 列表仅显示状态为 "已停用" 的商家

  Scenario: 按KYC认证状态筛选
    Given 商家列表页面已加载
    When 管理员在认证状态筛选中选择 "已认证"
    Then 列表仅显示 KYC 状态为 "已认证" 的商家

  Scenario: 按维护人筛选
    Given 管理员角色为 admin 或 operator
    When 管理员在维护人筛选中选择 "张三"
    Then 列表仅显示维护人为 "张三" 的商家

  Scenario: 分页切换
    Given 商家列表共 150 条数据，每页 20 条
    When 管理员点击第 3 页
    Then 列表显示第 41-60 条数据
    And 分页控件高亮第 3 页

  Scenario: 导出商家列表
    Given 管理员在商家列表页面
    When 管理员设置筛选条件后点击 "导出"
    Then 系统提示 "导出任务已提交"
    And 导出文件生成后出现在下载中心

  Scenario: Advisor仅可见自己维护的商家
    Given 当前登录角色为 advisor "李四"
    When advisor 进入商家列表页面
    Then 列表仅显示维护人为 "李四" 的商家
    And 维护人筛选器不可见
```

---

## Feature 5: 商家详情

```gherkin
Feature: 商家详情
  作为 Web 后台管理人员
  我希望查看和编辑商家的详细信息
  以便管理商家的各项配置

  Background:
    Given 管理员已登录 Web 后台并进入某商家详情页

  # --- Tab 1: 基本信息 ---

  Scenario: 查看商家基本信息
    Given 管理员在 "基本信息" Tab
    Then 页面显示商家名称、类型、联系方式、注册时间、状态

  Scenario: Admin编辑商家基本信息
    Given 当前角色为 admin
    And 管理员在 "基本信息" Tab
    When 管理员点击 "编辑"
    And 修改商家联系邮箱为 "new@example.com"
    And 点击 "保存"
    Then 信息更新成功
    And 操作日志记录本次修改

  Scenario: Operator无法编辑基本信息
    Given 当前角色为 operator
    And 管理员在 "基本信息" Tab
    Then "编辑" 按钮不可见或置灰

  # --- Tab 2: KYC 认证材料 ---

  Scenario: 查看KYC材料默认脱敏显示
    Given 管理员在 "KYC 认证材料" Tab
    Then 证件号显示为脱敏格式（如 "3201****1234"）
    And 证件照片显示缩略图

  Scenario: 点击查看原值需二次确认
    Given 管理员在 "KYC 认证材料" Tab
    When 管理员点击 "查看原值"
    Then 系统弹出确认框 "确认查看敏感信息？"
    And 管理员点击 "确认"
    Then 显示完整证件号
    And 操作日志记录本次查看

  # --- Tab 3: 限额配置 ---

  Scenario: 上传保证金凭证后配置限额
    Given 管理员在 "限额配置" Tab
    And 商家已提交保证金 $10,000
    When 管理员上传保证金到账凭证
    And 系统确认保证金金额为 $10,000
    Then 系统自动计算限额上限为 $100,000（保证金×10）
    And 管理员可配置实际限额（不超过 $100,000）

  Scenario: 未提交保证金时限额配置不可用
    Given 管理员在 "限额配置" Tab
    And 商家未提交任何保证金
    Then 限额配置区域置灰
    And 提示 "商家尚未提交保证金，暂无法配置限额"

  Scenario: 设置限额超过上限被拒绝
    Given 保证金 $10,000 已确认，限额上限为 $100,000
    When 管理员尝试设置限额为 $150,000
    Then 系统提示 "限额不可超过 $100,000（保证金×10）"
    And 保存按钮不可点击

  Scenario: 确认保证金金额
    Given 管理员上传了保证金到账凭证
    When 管理员输入确认金额 $10,000
    And 点击 "确认"
    Then 保证金状态变更为 "已确认"
    And 限额上限自动更新

  # --- Tab 4: 维护人绑定 ---

  Scenario: Admin绑定维护人
    Given 当前角色为 admin
    And 商家尚未绑定维护人
    When 管理员在 "维护人" Tab 点击 "绑定"
    And 选择维护人 "张三"
    And 点击 "确认绑定"
    Then 商家维护人变更为 "张三"
    And 操作日志记录绑定操作

  Scenario: Admin更换维护人需填写原因
    Given 当前角色为 admin
    And 商家当前维护人为 "张三"
    When 管理员点击 "更换维护人"
    And 选择新维护人 "李四"
    And 填写更换原因 "原维护人离职"
    And 点击 "确认更换"
    Then 商家维护人变更为 "李四"
    And 操作日志记录更换操作及原因

  Scenario: Admin更换维护人不填原因被拒绝
    Given 当前角色为 admin
    And 管理员点击 "更换维护人" 并选择新维护人
    When 更换原因字段为空
    And 点击 "确认更换"
    Then 系统提示 "请填写更换原因"
    And 更换操作不执行

  Scenario: Admin解绑维护人
    Given 当前角色为 admin
    And 商家当前维护人为 "张三"
    When 管理员点击 "解绑"
    And 确认解绑操作
    Then 商家维护人字段变为空
    And 操作日志记录解绑操作

  Scenario: Operator不可操作维护人
    Given 当前角色为 operator
    When 管理员在 "维护人" Tab
    Then "绑定"/"更换"/"解绑" 按钮均不可见

  # --- Tab 5: 操作日志 ---

  Scenario: 查看操作日志
    Given 管理员在 "操作日志" Tab
    Then 显示该商家所有操作记录
    And 每条记录包含：操作时间、操作人、操作类型、操作详情

  Scenario: 操作日志按时间倒序排列
    Given 管理员在 "操作日志" Tab
    Then 最新的操作记录显示在最上方
```

---

## Feature 6: 添加商家

```gherkin
Feature: 添加商家
  作为 Web 后台管理人员
  我希望新增商家信息
  以便将新合作商家录入系统

  Background:
    Given 管理员已登录 Web 后台并进入 "添加商家" 页面

  Scenario: 必填字段为空提交被拒绝
    Given 管理员在添加商家表单
    When 商家名称字段为空
    And 点击 "提交"
    Then 系统高亮显示必填字段
    And 提示 "请填写必填信息"

  Scenario: 商家类型多选
    Given 管理员在添加商家表单
    When 管理员同时选择 "批发商" 和 "零售商"
    Then 商家类型字段显示已选 2 个类型
    And 可继续填写其他字段

  Scenario: 联系方式三选一校验
    Given 管理员在添加商家表单
    When 管理员未填写手机号、WhatsApp号、邮箱中的任何一个
    And 点击 "提交"
    Then 系统提示 "请至少填写一种联系方式（手机号/WhatsApp/邮箱）"

  Scenario: 证件类型按地区动态显示-印尼
    Given 管理员在添加商家表单
    When 管理员选择地区 "印尼"
    Then 证件类型下拉框显示 "KTP"

  Scenario: 证件类型按地区动态显示-香港
    Given 管理员在添加商家表单
    When 管理员选择地区 "香港"
    Then 证件类型下拉框显示 "HKID" 和 "Passport"

  Scenario: Admin提交添加商家成功
    Given 当前角色为 admin
    When 管理员正确填写所有必填字段
    And 点击 "提交"
    Then 系统提示 "商家添加成功"
    And 跳转至商家详情页
    And 商家状态为 "待认证"

  Scenario: Advisor提交添加商家自动绑定维护人
    Given 当前角色为 advisor "张三"
    When advisor 正确填写所有必填字段并提交
    Then 商家创建成功
    And 商家维护人自动绑定为 "张三"

  Scenario: 商家名称重复检测
    Given 管理员输入商家名称 "TechMobile"
    And 系统中已存在同名商家
    When 管理员点击 "提交"
    Then 系统提示 "已存在同名商家，是否继续添加？"
    And 管理员可选择 "继续" 或 "取消"
```

---

## Feature 7: 下载中心

```gherkin
Feature: 下载中心
  作为 Web 后台管理人员
  我希望在下载中心管理导出文件
  以便获取数据报表

  Background:
    Given 管理员已登录 Web 后台并进入 "下载中心"

  Scenario: 查看文件列表
    Given 管理员有已导出的文件
    When 管理员进入下载中心
    Then 显示文件列表包含：文件名、创建时间、文件大小、状态、操作
    And 状态包括 "生成中"、"已完成"、"已过期"

  Scenario: 下载已完成的文件
    Given 文件列表中有状态为 "已完成" 的文件
    When 管理员点击 "下载"
    Then 浏览器开始下载该文件

  Scenario: 已过期文件不可下载
    Given 文件列表中有状态为 "已过期" 的文件（超过7天）
    When 管理员查看该文件操作栏
    Then "下载" 按钮不可用
    And 显示 "重新生成" 按钮

  Scenario: 重新生成已过期文件
    Given 文件状态为 "已过期"
    When 管理员点击 "重新生成"
    Then 系统提示 "文件重新生成中"
    And 文件状态变更为 "生成中"
    And 生成完成后状态变为 "已完成"

  Scenario: Advisor仅可见自己生成的文件
    Given 当前角色为 advisor "李四"
    When advisor 进入下载中心
    Then 仅显示由 "李四" 触发导出的文件
    And 不可见其他人生成的文件
```
