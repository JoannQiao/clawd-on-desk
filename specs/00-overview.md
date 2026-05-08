# FoneSquare 系统总览

## 项目概要

FoneSquare 是一个**海外 B2B 二手手机交易平台**：

- **APP 端**：面向海外商家（买家/卖家），提供注册登录、KYC 实名认证、浏览商品、下单购买等功能
- **Web 管理后台**：面向 FoneSquare 运营管理团队，使用 OB 账号体系登录，覆盖商家全生命周期管理：商家录入、KYC 资质查看、每日限额配置、维护人（销售/顾问）绑定与数据权限隔离
- **核心业务**：海外回收商通过 APP 在 FoneSquare 平台下单采购二手手机，平台通过 KYC 认证、保证金机制、每日限额等手段进行风控管理

---

## 系统架构图

```mermaid
graph TB
    subgraph 客户端["客户端 Client"]
        APP["📱 FoneSquare APP<br/>商家端（买家/卖家）"]
        WEB["🖥️ Web 管理后台<br/>运营管理团队"]
    end

    subgraph 后端服务["后端服务 Backend"]
        API["🔧 API Gateway<br/>统一接口网关"]
        AUTH["🔐 Auth 服务<br/>OTP / 密码 / JWT"]
        BIZ["📦 业务服务<br/>商家 / KYC / 限额 / 保证金"]
        EXPORT["📥 导出服务<br/>异步文件生成"]
    end

    subgraph 数据层["数据层 Data"]
        DB[("🗄️ PostgreSQL<br/>主数据库")]
        CACHE[("⚡ Redis<br/>OTP / 会话 / 限额缓存")]
        OSS["☁️ OSS 文件存储<br/>证件照 / 凭证 / 导出文件"]
    end

    subgraph 外部依赖["外部依赖 External"]
        OCR["🔍 OCR 服务<br/>证件识别（含置信度）"]
        SMS["📨 SMS 网关<br/>京东云短信"]
        WHATSAPP["💬 WhatsApp Business API<br/>OTP 验证"]
        EMAIL["📧 邮件服务<br/>OTP 验证"]
        SANCTION["🛡️ 制裁名单<br/>OFAC / UN / EU"]
        RISK["⚠️ 风控系统<br/>反欺诈校验"]
    end

    APP --> API
    WEB --> API
    API --> AUTH
    API --> BIZ
    API --> EXPORT
    AUTH --> CACHE
    AUTH --> SMS
    AUTH --> WHATSAPP
    AUTH --> EMAIL
    BIZ --> DB
    BIZ --> CACHE
    BIZ --> OSS
    BIZ --> OCR
    BIZ --> SANCTION
    BIZ --> RISK
    EXPORT --> DB
    EXPORT --> OSS
```

---

## 实体关系图

```mermaid
erDiagram
    User ||--o{ Merchant : "维护(advisor)"
    User ||--o{ OperationLog : "操作"
    User ||--o{ ExportFile : "导出"
    User ||--o{ AdvisorBinding : "作为维护人"
    Merchant ||--o{ KYCRecord : "个人认证"
    Merchant ||--o| CompanyKYC : "企业认证"
    Merchant ||--o{ DepositRecord : "保证金"
    Merchant ||--o| LimitConfig : "限额配置"
    Merchant ||--o{ AdvisorBinding : "被维护"
    Merchant ||--o{ OperationLog : "被操作"

    User {
        string id PK "用户ID"
        string phone "手机号（含区号）"
        string email "邮箱"
        string whatsapp "WhatsApp号码"
        string passwordHash "密码哈希(bcrypt)"
        enum role "角色: admin/operator/advisor"
        enum status "状态: active/disabled"
        datetime lastLoginAt "最后登录时间"
        datetime createdAt "创建时间"
    }

    Merchant {
        string id PK "商家ID"
        string name "商家名称"
        array type "类型: buyer/seller 数组"
        enum status "状态: active/disabled"
        enum authStatus "认证: verified/unverified/restricted"
        string phone "联系手机号"
        string email "邮箱"
        string whatsapp "WhatsApp"
        json region "地区(country/province/city)"
        string remark "备注"
        string advisorId FK "当前维护人ID"
        datetime createdAt "创建时间"
        datetime updatedAt "更新时间"
    }

    KYCRecord {
        string id PK "记录ID"
        string merchantId FK "商家ID"
        enum idType "证件类型: HKID/MOID/CNIDCard/Passport"
        string idNumber "证件号(脱敏存储)"
        string fullName "证件姓名"
        date dateOfBirth "出生日期"
        date expiryDate "有效期"
        float ocrConfidence "OCR置信度"
        json sanctionCheckResult "制裁名单校验结果"
        string selfieUrl "自拍照URL"
        string idFrontUrl "证件正面URL"
        string idBackUrl "证件反面URL"
        enum status "状态: pending/verified/rejected/frozen"
        datetime createdAt "创建时间"
    }

    CompanyKYC {
        string id PK "记录ID"
        string merchantId FK "商家ID"
        string companyName "企业名称"
        string businessRegNo "证照编号"
        string licenseType "证照类型"
        string representative "法定代表/董事"
        string address "企业地址"
        date expiryDate "证照有效期"
        string licenseUrl "证照照片URL"
        enum status "状态: pending/verified/rejected"
    }

    DepositRecord {
        string id PK "记录ID"
        string merchantId FK "商家ID"
        decimal amount "保证金金额"
        string currency "币种(HKD)"
        array proofImageUrls "凭证图片(最多3张)"
        enum status "状态: pending/confirmed/rejected"
        string confirmedBy "确认人"
        datetime confirmedAt "确认时间"
        datetime createdAt "创建时间"
    }

    LimitConfig {
        string id PK "配置ID"
        string merchantId FK "商家ID"
        integer dailyLimit "每日下单限额(HKD)"
        decimal depositAmount "关联保证金金额"
        datetime effectiveFrom "生效时间"
    }

    AdvisorBinding {
        string id PK "绑定ID"
        string merchantId FK "商家ID"
        string advisorUserId FK "维护人用户ID"
        string reason "绑定/变更原因"
        datetime boundAt "绑定时间"
        datetime unboundAt "解绑时间"
        string operatorId "操作人ID"
    }

    OperationLog {
        string id PK "日志ID"
        string merchantId FK "商家ID"
        string operatorUserId FK "操作人ID"
        string operationType "操作类型"
        json changeDetail "变更详情JSON"
        datetime createdAt "创建时间"
    }

    ExportFile {
        string id PK "文件ID"
        string userId FK "导出人ID"
        string fileName "文件名"
        integer fileSize "文件大小(bytes)"
        enum status "状态: generating/ready/expired"
        string fileUrl "下载地址"
        datetime createdAt "创建时间"
        datetime expiresAt "过期时间(30天)"
    }
```

---

## 技术栈建议

| 层级 | 技术选型 | 说明 |
|------|----------|------|
| **APP 前端** | React Native / Flutter | 跨平台 APP，支持 iOS + Android |
| **Web 前端** | React + TypeScript + Ant Design | 管理后台，支持中英文 i18n |
| **后端框架** | Node.js (NestJS) / Java (Spring Boot) / Go | RESTful API，JWT 鉴权 |
| **数据库** | PostgreSQL | 主数据库，JSONB 支持 |
| **缓存** | Redis | OTP 验证码、会话、限额计数、防刷限流 |
| **文件存储** | 阿里云 OSS / AWS S3 | 证件照、保证金凭证、导出文件 |
| **OCR** | 第三方 OCR 服务 | 证件识别，返回置信度 |
| **SMS** | 京东云短信 | Phone OTP |
| **消息推送** | WhatsApp Business API / 邮件服务 | WhatsApp OTP / Email OTP |
| **风控** | 制裁名单 API（OFAC/UN/EU） | KYC 合规校验 |

---

## MVP 功能范围清单

### P0 核心功能（MVP 必须）

| 模块 | 功能 | 说明 |
|------|------|------|
| **APP - 登录注册** | Phone OTP 登录 | 手机号 + 短信验证码登录/注册一体化 |
| **APP - 登录注册** | WhatsApp OTP 登录 | WhatsApp 验证码登录/注册 |
| **APP - 登录注册** | Email OTP 登录 | 邮箱验证码登录/注册 |
| **APP - 登录注册** | 密码设置 | 首次登录后引导设置密码，后续密码+OTP双通道 |
| **APP - KYC** | 个人实名认证 | 证件拍照 → OCR 识别 → 制裁名单校验 → 自动认证 |
| **APP - KYC** | 企业认证（选填） | 营业执照上传，OCR 识别 |
| **Web - 商家管理** | 商家列表 | 列表+筛选+分页+导出，维护人数据隔离 |
| **Web - 商家管理** | 商家详情 | 基本信息、KYC材料、限额保证金、维护人绑定、操作日志 |
| **Web - 商家管理** | 添加商家 | 单页表单录入，含 KYC 信息，证件唯一性校验 |
| **Web - 限额管理** | 每日下单限额 | 配置每日限额（HKD），保证金×10=上限 |
| **Web - 保证金** | 保证金管理 | 填写金额、上传凭证、确认状态 |
| **Web - 权限** | 功能权限+数据权限 | 管理员全量，维护人仅绑定商家 |
| **Web - 维护人** | 维护人绑定/解绑/更换 | 含变更原因，记录操作日志 |
| **Web - 日志** | 操作日志 | 所有变更记录，含修改前后值 |

### P1 增强功能

| 模块 | 功能 | 说明 |
|------|------|------|
| **APP - KYC** | KYC 重新提交 | 修改认证信息后重新走 OCR + 风控流程 |
| **APP - KYC** | 重复证件引导 | 检测到证件已注册时引导至已有账号 |
| **Web - 导出** | 下载中心 | 异步导出，30 天有效，支持重新生成 |
| **Web - 国际化** | 中英文切换 | 管理后台支持简体中文 + English |
| **Web - 商家管理** | 商家启用/停用 | 状态切换，停用后不可下单 |
| **Web - 资质** | KYC 验证记录 | 认证日志，含验证类型/结果/失败原因 |
| **通用** | 多语言本地化 | APP 端 EN/zh-CN/zh-HK |
| **通用** | 时区处理 | 后端 UTC+8 存储，APP 端展示本地时区 |

---

## 全局业务规则

1. **认证状态影响下单**：未认证 → 不可下单；已认证 → 可正常下单
2. **保证金与限额关联**：保证金金额 × 10 = 每日下单限额上限
3. **每日限额计算**：当日累计（已支付+未支付，不含取消）订单金额（HKD）≥ 限额时禁止下单
4. **证件唯一性**：同一证件号只能关联一个商家账号，不做账号合并，引导至已有账号
5. **OTP 防刷**：同一号码 60 秒内不可重发，每小时/每日有发送上限
6. **JWT Token**：有效期 90 天，支持多设备登录
7. **密码加密**：bcrypt 加密存储
8. **操作日志**：所有关键操作（编辑、状态变更、绑定变更、限额修改）均记录操作人、修改前后值、时间
