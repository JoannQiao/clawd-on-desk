# FoneSquare 数据模型

> 所有实体使用 TypeScript interface 定义，字段注释说明校验规则与业务含义。

---

## 通用枚举定义

```typescript
/** 商家类型 */
type MerchantType = 'buyer' | 'seller';

/** 商家状态 */
type MerchantStatus = 'active' | 'disabled';

/** 认证状态 */
type AuthStatus = 'verified' | 'unverified' | 'restricted';

/** 证件类型 — 按地区动态展示 */
type IdDocumentType = 'HKID' | 'MOID' | 'CNIDCard' | 'Passport';

/** KYC 审核状态 */
type KYCStatus = 'pending' | 'verified' | 'rejected' | 'frozen';

/** 企业KYC审核状态 */
type CompanyKYCStatus = 'pending' | 'verified' | 'rejected';

/** 保证金状态 */
type DepositStatus = 'pending' | 'confirmed' | 'rejected';

/** 导出文件状态 */
type ExportFileStatus = 'generating' | 'ready' | 'expired';

/** 后台用户角色 */
type UserRole = 'admin' | 'operator' | 'advisor';

/** 用户状态 */
type UserStatus = 'active' | 'disabled';

/** OTP 通道 */
type OTPChannel = 'sms' | 'whatsapp' | 'email';

/** 制裁名单来源 */
type SanctionSource = 'OFAC' | 'UN' | 'EU';
```

---

## 实体定义

### User — 后台管理员 / 运营 / 维护人

```typescript
interface User {
  /** 用户唯一标识，UUID 格式 */
  id: string;

  /** 手机号，含国际区号，格式如 +852 9123 4567 */
  phone: string | null;

  /** 邮箱地址，格式校验 RFC 5322 */
  email: string | null;

  /** WhatsApp 号码，含区号 */
  whatsapp: string | null;

  /** 密码哈希，使用 bcrypt 加密，cost factor ≥ 10 */
  passwordHash: string | null;

  /** 用户角色：admin（超管）/ operator（运营）/ advisor（维护人/顾问） */
  role: UserRole;

  /** 用户名/显示名称 */
  displayName: string;

  /** OB 账号编号（关联现有 OB 账号体系） */
  obAccountId: string | null;

  /** 账号状态：active（正常）/ disabled（禁用） */
  status: UserStatus;

  /** 最后登录时间，ISO 8601 格式，UTC+8 */
  lastLoginAt: string | null;

  /** 创建时间，ISO 8601 格式，UTC+8 */
  createdAt: string;

  /** 更新时间 */
  updatedAt: string;
}
```

### Merchant — 商家

```typescript
interface Merchant {
  /** 商家唯一标识，系统自增 ID 或 UUID */
  id: string;

  /** 商家名称，必填，1-200 字符 */
  name: string;

  /**
   * 商家类型，数组形式，可多选
   * 有效值：['buyer'] / ['seller'] / ['buyer', 'seller']
   * 至少选择一项
   */
  type: MerchantType[];

  /** 商家状态：active（使用中）/ disabled（已停用） */
  status: MerchantStatus;

  /**
   * 认证状态：
   * - verified: 已身份认证（KYC 通过 + 制裁名单通过）
   * - unverified: 未身份认证（未提交或被拒/过期）
   * - restricted: 账号受限（制裁命中等）
   */
  authStatus: AuthStatus;

  /**
   * 联系手机号，含国际区号
   * 与 email、whatsapp 三选一必填
   */
  phone: string | null;

  /**
   * 邮箱地址
   * 与 phone、whatsapp 三选一必填
   */
  email: string | null;

  /**
   * WhatsApp 号码
   * 与 phone、email 三选一必填
   */
  whatsapp: string | null;

  /**
   * 所在地区，三级联动：国家/省份/城市
   * 必填项
   */
  region: {
    /** 国家代码，如 HK, MO, CN */
    country: string;
    /** 省份/地区 */
    province: string | null;
    /** 城市 */
    city: string | null;
  };

  /** 备注信息，选填，最大 500 字符 */
  remark: string | null;

  /**
   * 当前维护人（顾问/销售）的用户 ID
   * 销售添加商家时自动绑定；管理员添加时默认 null
   */
  advisorId: string | null;

  /** 创建时间，ISO 8601 格式，UTC+8 */
  createdAt: string;

  /** 更新时间 */
  updatedAt: string;
}
```

### KYCRecord — 个人 KYC 认证记录

```typescript
interface KYCRecord {
  /** 记录唯一标识 */
  id: string;

  /** 关联商家 ID，外键 */
  merchantId: string;

  /**
   * 证件类型：
   * - HKID: 香港身份证
   * - MOID: 澳门身份证
   * - CNIDCard: 中国居民身份证
   * - Passport: 护照
   * 按用户所在地区动态展示可选类型
   */
  idType: IdDocumentType;

  /**
   * 证件号码（加密存储）
   * 展示时脱敏：中间位替换为 ***
   * 同一证件号全局唯一，不允许重复注册
   * 校验规则按证件类型不同：
   * - HKID: X123456(7) 格式
   * - CNIDCard: 18位
   * - Passport: 各国格式不同
   */
  idNumber: string;

  /** 证件上的姓名全称，与证件一致 */
  fullName: string;

  /** 出生日期，格式 YYYY-MM-DD */
  dateOfBirth: string | null;

  /**
   * 证件有效期，格式 YYYY-MM-DD
   * 不可为过去日期
   */
  expiryDate: string;

  /**
   * OCR 识别置信度，0-1 之间的浮点数
   * 由 OCR 服务返回
   */
  ocrConfidence: number | null;

  /**
   * 制裁名单校验结果
   * 包含各名单（OFAC/UN/EU）的匹配结果
   */
  sanctionCheckResult: {
    /** 是否通过（未命中任何名单） */
    passed: boolean;
    /** 各名单校验详情 */
    details: Array<{
      source: SanctionSource;
      matched: boolean;
      matchedName: string | null;
      checkedAt: string;
    }>;
  } | null;

  /**
   * 自拍照 URL（活体检测用）
   * 存储在 OSS，返回签名 URL
   */
  selfieUrl: string | null;

  /**
   * 证件正面照片 URL
   * JPG/PNG，≤ 5MB
   */
  idFrontUrl: string | null;

  /**
   * 证件反面照片 URL
   * 护照无反面，此时为 null
   * JPG/PNG，≤ 5MB
   */
  idBackUrl: string | null;

  /**
   * KYC 审核状态：
   * - pending: 待审核（提交后等待 OCR + 风控）
   * - verified: 已通过
   * - rejected: 已拒绝（OCR 失败或制裁命中）
   * - frozen: 已冻结（后续风控发现问题）
   */
  status: KYCStatus;

  /**
   * 验证类型：首次提交 / 重新提交
   */
  verificationType: 'initial' | 'resubmit';

  /** 失败原因描述（status 为 rejected 时填充） */
  rejectReason: string | null;

  /** 创建时间 */
  createdAt: string;

  /** 更新时间 */
  updatedAt: string;
}
```

### CompanyKYC — 企业 KYC 认证

```typescript
interface CompanyKYC {
  /** 记录唯一标识 */
  id: string;

  /** 关联商家 ID */
  merchantId: string;

  /** 企业全称，OCR 识别或手动填写 */
  companyName: string;

  /**
   * 证照类型
   * 如：商业登记证、营业执照等
   */
  licenseType: string;

  /** 证照编号/企业注册 ID */
  businessRegNo: string;

  /** 法定代表/董事姓名 */
  representative: string | null;

  /** 企业注册地址 */
  address: string | null;

  /** 证照有效期，格式 YYYY-MM-DD */
  expiryDate: string | null;

  /**
   * 证照照片 URL
   * JPG/PNG/PDF，≤ 10MB
   */
  licenseUrl: string | null;

  /** 审核状态 */
  status: CompanyKYCStatus;

  /** 创建时间 */
  createdAt: string;

  /** 更新时间 */
  updatedAt: string;
}
```

### DepositRecord — 保证金记录

```typescript
interface DepositRecord {
  /** 记录唯一标识 */
  id: string;

  /** 关联商家 ID */
  merchantId: string;

  /**
   * 保证金金额，正整数
   * 该金额 × 10 = 每日下单限额上限
   */
  amount: number;

  /**
   * 币种，当前仅支持 HKD
   * 后续新增店铺时按店铺维度配置
   */
  currency: 'HKD';

  /**
   * 转账凭证图片 URL 数组
   * JPG/PNG，单张 ≤ 5MB，最多 3 张
   */
  proofImageUrls: string[];

  /**
   * 保证金状态：
   * - pending: 未提交 / 已提交待确认
   * - confirmed: 已确认（运营确认转账后，限额上限生效）
   * - rejected: 已拒绝
   */
  status: DepositStatus;

  /** 确认人（运营人员用户 ID） */
  confirmedBy: string | null;

  /** 确认时间 */
  confirmedAt: string | null;

  /** 创建时间 */
  createdAt: string;
}
```

### LimitConfig — 每日下单限额配置

```typescript
interface LimitConfig {
  /** 配置唯一标识 */
  id: string;

  /** 关联商家 ID */
  merchantId: string;

  /**
   * 每日下单限额（HKD），正整数
   * 校验规则：
   * - ≥ 0
   * - ≤ 保证金金额 × 10（若已提交保证金）
   * - 未提交保证金时仅可设为默认最小值
   * - 设为 0 表示不可下单
   * APP 下单时读取此值，当日累计订单金额（已支付+未支付，不含取消）≥ 限额时禁止下单
   */
  dailyLimit: number;

  /**
   * 关联的保证金金额（快照）
   * 用于计算限额上限 = depositAmount × 10
   */
  depositAmount: number;

  /** 生效时间 */
  effectiveFrom: string;

  /** 更新时间 */
  updatedAt: string;
}
```

### AdvisorBinding — 维护人绑定记录

```typescript
interface AdvisorBinding {
  /** 绑定记录唯一标识 */
  id: string;

  /** 关联商家 ID */
  merchantId: string;

  /**
   * 维护人（顾问/销售）的用户 ID
   * 关联 User 表
   */
  advisorUserId: string;

  /**
   * 绑定/变更原因，必填
   * 记录到操作日志
   * 如：商家创建自动绑定 / 销售离职转交 / 业务调整
   */
  reason: string;

  /** 绑定时间 */
  boundAt: string;

  /**
   * 解绑时间
   * 当前绑定为 null，历史绑定有值
   * 解绑后维护人立即失去该商家的数据访问权
   */
  unboundAt: string | null;

  /** 操作人 ID（谁执行的绑定/解绑操作） */
  operatorId: string;
}
```

### OperationLog — 操作日志

```typescript
interface OperationLog {
  /** 日志唯一标识 */
  id: string;

  /** 关联商家 ID */
  merchantId: string;

  /** 操作人用户 ID */
  operatorUserId: string;

  /**
   * 操作类型枚举：
   * - merchant:create  创建商家
   * - merchant:edit    编辑基本信息
   * - merchant:enable  启用商家
   * - merchant:disable 停用商家
   * - kyc:submit       提交KYC
   * - kyc:resubmit     重新提交KYC
   * - kyc:edit         后台编辑KYC信息
   * - limit:update     修改每日限额
   * - deposit:create   录入保证金
   * - deposit:confirm  确认保证金
   * - advisor:bind     绑定维护人
   * - advisor:unbind   解绑维护人
   * - advisor:reassign 更换维护人
   */
  operationType: string;

  /**
   * 变更详情 JSON，包含修改前后的值
   * 格式：{ field: string, before: any, after: any }[]
   */
  changeDetail: Array<{
    /** 变更字段名 */
    field: string;
    /** 变更前值 */
    before: unknown;
    /** 变更后值 */
    after: unknown;
  }>;

  /** 操作时间，精确到秒 */
  createdAt: string;
}
```

### ExportFile — 导出文件

```typescript
interface ExportFile {
  /** 文件唯一标识 */
  id: string;

  /** 导出人用户 ID */
  userId: string;

  /**
   * 文件名
   * 命名规则：{来源}_{筛选条件}_{时间戳}.xlsx
   * 如：merchants_2026-04-28_1430.xlsx
   */
  fileName: string;

  /** 文件大小（字节） */
  fileSize: number | null;

  /**
   * 文件状态：
   * - generating: 处理中（异步生成）
   * - ready: 可下载
   * - expired: 已过期（超过 30 天）
   */
  status: ExportFileStatus;

  /**
   * 文件下载 URL（OSS 签名地址）
   * generating 状态时为 null
   */
  fileUrl: string | null;

  /**
   * 来源页面标识
   * 如：merchant-list（商家列表）
   */
  sourcePage: string;

  /** 创建时间 */
  createdAt: string;

  /**
   * 过期时间（创建后 30 天）
   * 过期后自动清理文件并标记状态为 expired
   */
  expiresAt: string;
}
```

---

## 索引建议

| 表 | 索引 | 类型 | 说明 |
|---|------|------|------|
| Merchant | `idx_merchant_advisor` | B-tree | 维护人筛选 |
| Merchant | `idx_merchant_status_auth` | 复合 | 状态+认证筛选 |
| Merchant | `idx_merchant_name` | GIN(trigram) | 名称模糊搜索 |
| KYCRecord | `uniq_kyc_id_number` | Unique | 证件号全局唯一 |
| KYCRecord | `idx_kyc_merchant` | B-tree | 商家关联查询 |
| AdvisorBinding | `idx_binding_advisor_active` | 部分索引 | 当前有效绑定快速查询 |
| OperationLog | `idx_log_merchant_time` | 复合 | 按商家+时间查日志 |
| ExportFile | `idx_export_user_status` | 复合 | 用户文件列表查询 |
| DepositRecord | `idx_deposit_merchant` | B-tree | 商家保证金查询 |
