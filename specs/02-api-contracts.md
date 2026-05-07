# FoneSquare API 端点契约

> 所有 API 遵循 RESTful 规范，JSON 格式请求/响应。  
> 时间字段统一使用 ISO 8601 格式（UTC+8）。  
> 认证方式：Bearer JWT Token（有效期 90 天）。

---

## 通用约定

### 分页参数

```typescript
interface PaginationQuery {
  /** 页码，从 1 开始，默认 1 */
  page?: number;
  /** 每页条数，默认 10，最大 100 */
  pageSize?: number;
}

interface PaginatedResponse<T> {
  /** 数据列表 */
  items: T[];
  /** 总条数 */
  total: number;
  /** 当前页码 */
  page: number;
  /** 每页条数 */
  pageSize: number;
}
```

### 通用错误响应

```typescript
interface ErrorResponse {
  /** HTTP 状态码 */
  statusCode: number;
  /** 错误码（业务码） */
  errorCode: string;
  /** 错误描述 */
  message: string;
  /** 错误详情（校验失败时返回字段级错误） */
  details?: Array<{
    field: string;
    message: string;
  }>;
}
```

### 通用错误码

| 错误码 | HTTP 状态码 | 说明 |
|--------|-------------|------|
| `AUTH_TOKEN_EXPIRED` | 401 | Token 已过期 |
| `AUTH_TOKEN_INVALID` | 401 | Token 无效 |
| `AUTH_FORBIDDEN` | 403 | 无权限访问 |
| `RESOURCE_NOT_FOUND` | 404 | 资源不存在 |
| `VALIDATION_ERROR` | 400 | 参数校验失败 |
| `RATE_LIMIT_EXCEEDED` | 429 | 请求频率超限 |
| `INTERNAL_ERROR` | 500 | 服务内部错误 |

---

## 一、Auth — 认证模块

### POST /auth/otp/send

发送 OTP 验证码（支持 SMS / WhatsApp / Email 三个通道）。

| 项目 | 内容 |
|------|------|
| **描述** | 向指定手机号/WhatsApp/邮箱发送一次性验证码 |
| **权限** | 无需登录（公开接口） |
| **限流** | 同一账号 60 秒内不可重发；每小时上限 10 次；每日上限 20 次 |

**Request Body:**

```typescript
interface SendOTPRequest {
  /**
   * OTP 接收通道
   * sms: 短信（京东云）
   * whatsapp: WhatsApp Business API
   * email: 邮件
   */
  channel: 'sms' | 'whatsapp' | 'email';

  /**
   * 接收地址
   * sms/whatsapp: 含国际区号的手机号，如 +852 91234567
   * email: 邮箱地址
   */
  target: string;
}
```

**Response 200:**

```typescript
interface SendOTPResponse {
  /** 是否发送成功 */
  success: boolean;
  /** OTP 有效期（秒），默认 300 */
  expiresIn: number;
  /** 下次可重发的倒计时（秒） */
  retryAfter: number;
}
```

**错误码:**

| 错误码 | 说明 |
|--------|------|
| `OTP_RATE_LIMITED` | 发送过于频繁，请等待 {retryAfter} 秒 |
| `OTP_DAILY_LIMIT` | 当日发送次数已达上限 |
| `OTP_INVALID_TARGET` | 目标地址格式不正确 |
| `OTP_SEND_FAILED` | 发送失败（通道异常） |

---

### POST /auth/otp/verify

验证 OTP 验证码，登录或注册。

| 项目 | 内容 |
|------|------|
| **描述** | 校验 OTP 验证码，若用户不存在则自动注册；返回 JWT Token |
| **权限** | 无需登录 |
| **业务规则** | 登录注册一体化；验证码 5 分钟有效；错误 5 次后锁定 30 分钟 |

**Request Body:**

```typescript
interface VerifyOTPRequest {
  /** OTP 通道 */
  channel: 'sms' | 'whatsapp' | 'email';
  /** 接收地址（与发送时一致） */
  target: string;
  /** 用户输入的验证码，6 位数字 */
  code: string;
}
```

**Response 200:**

```typescript
interface VerifyOTPResponse {
  /** JWT Token，有效期 90 天 */
  accessToken: string;
  /** Token 过期时间 */
  expiresAt: string;
  /** 是否为新注册用户 */
  isNewUser: boolean;
  /** 是否已设置密码（未设置时前端引导设置） */
  hasPassword: boolean;
  /** 用户基本信息 */
  user: {
    id: string;
    phone: string | null;
    email: string | null;
    whatsapp: string | null;
  };
}
```

**错误码:**

| 错误码 | 说明 |
|--------|------|
| `OTP_INVALID` | 验证码错误 |
| `OTP_EXPIRED` | 验证码已过期 |
| `OTP_ATTEMPTS_EXCEEDED` | 错误次数过多，账号已锁定 |

---

### POST /auth/password/set

首次设置密码。

| 项目 | 内容 |
|------|------|
| **描述** | OTP 登录后首次设置密码 |
| **权限** | 需登录（Bearer Token） |
| **业务规则** | 密码 8-20 位，需包含字母和数字；bcrypt 加密存储 |

**Request Body:**

```typescript
interface SetPasswordRequest {
  /** 新密码，8-20 位，需包含字母和数字 */
  password: string;
  /** 确认密码，需与 password 一致 */
  confirmPassword: string;
}
```

**Response 200:**

```typescript
interface SetPasswordResponse {
  success: boolean;
}
```

**错误码:**

| 错误码 | 说明 |
|--------|------|
| `PASSWORD_TOO_WEAK` | 密码强度不足 |
| `PASSWORD_MISMATCH` | 两次密码不一致 |
| `PASSWORD_ALREADY_SET` | 密码已设置过 |

---

### POST /auth/login

密码登录。

| 项目 | 内容 |
|------|------|
| **描述** | 使用手机号/邮箱 + 密码登录 |
| **权限** | 无需登录 |
| **业务规则** | 错误 5 次锁定 30 分钟；支持多设备登录 |

**Request Body:**

```typescript
interface LoginRequest {
  /** 登录账号（手机号或邮箱） */
  account: string;
  /** 密码 */
  password: string;
}
```

**Response 200:**

```typescript
interface LoginResponse {
  /** JWT Token */
  accessToken: string;
  expiresAt: string;
  user: {
    id: string;
    phone: string | null;
    email: string | null;
    whatsapp: string | null;
  };
}
```

**错误码:**

| 错误码 | 说明 |
|--------|------|
| `LOGIN_INVALID_CREDENTIALS` | 账号或密码错误 |
| `LOGIN_ACCOUNT_LOCKED` | 账号已锁定，请 {minutes} 分钟后重试 |
| `LOGIN_ACCOUNT_DISABLED` | 账号已被禁用 |

---

### POST /auth/password/reset

重置密码（通过 OTP 验证后重置）。

| 项目 | 内容 |
|------|------|
| **描述** | 忘记密码时，先发送 OTP 验证身份，再设置新密码 |
| **权限** | 需先完成 OTP 验证（携带临时 Token） |

**Request Body:**

```typescript
interface ResetPasswordRequest {
  /** OTP 验证后获取的临时 Token */
  resetToken: string;
  /** 新密码 */
  newPassword: string;
  /** 确认密码 */
  confirmPassword: string;
}
```

**Response 200:**

```typescript
interface ResetPasswordResponse {
  success: boolean;
}
```

---

## 二、KYC — 实名认证模块

### POST /kyc/submit

提交 KYC 认证（APP 端）。

| 项目 | 内容 |
|------|------|
| **描述** | 用户拍照上传证件，提交个人 KYC 认证申请 |
| **权限** | 需登录（APP 用户） |
| **业务规则** | 提交后自动触发 OCR 识别 + 制裁名单校验；证件号全局唯一 |

**Request Body (multipart/form-data):**

```typescript
interface SubmitKYCRequest {
  /** 证件类型 */
  idType: 'HKID' | 'MOID' | 'CNIDCard' | 'Passport';
  /** 证件正面照片文件 */
  idFrontImage: File;
  /** 证件反面照片文件（护照可不传） */
  idBackImage?: File;
  /** 自拍照文件（活体检测） */
  selfieImage?: File;
}
```

**Response 200:**

```typescript
interface SubmitKYCResponse {
  /** KYC 记录 ID */
  kycRecordId: string;
  /**
   * OCR 识别结果
   * 前端展示供用户确认
   */
  ocrResult: {
    fullName: string;
    idNumber: string;
    dateOfBirth: string | null;
    expiryDate: string | null;
    confidence: number;
  };
  /** 校验结果 */
  verificationResult: {
    /** 是否通过 */
    passed: boolean;
    /** 认证状态 */
    status: 'verified' | 'rejected';
    /** 拒绝原因（未通过时） */
    rejectReason: string | null;
  };
}
```

**错误码:**

| 错误码 | 说明 |
|--------|------|
| `KYC_DUPLICATE_ID` | 该证件号已关联其他账号 |
| `KYC_OCR_FAILED` | OCR 识别失败，请重新拍照 |
| `KYC_SANCTION_HIT` | 制裁名单命中，认证被拒 |
| `KYC_IMAGE_INVALID` | 图片格式不支持或超过大小限制 |
| `KYC_ALREADY_VERIFIED` | 已完成认证，无需重复提交 |

---

### GET /kyc/status

查询当前用户的 KYC 认证状态。

| 项目 | 内容 |
|------|------|
| **描述** | 返回当前登录用户的 KYC 认证状态和详情 |
| **权限** | 需登录（APP 用户） |

**Response 200:**

```typescript
interface KYCStatusResponse {
  /** 认证状态 */
  authStatus: 'verified' | 'unverified' | 'restricted';
  /** 最新 KYC 记录（如有） */
  latestRecord: {
    id: string;
    idType: string;
    idNumber: string;       // 脱敏展示
    fullName: string;       // 脱敏展示
    expiryDate: string;
    status: 'pending' | 'verified' | 'rejected' | 'frozen';
    rejectReason: string | null;
    createdAt: string;
  } | null;
  /** 企业认证信息（如有） */
  companyKYC: {
    companyName: string;
    businessRegNo: string;
    status: string;
  } | null;
}
```

---

### PUT /kyc/resubmit

重新提交 KYC 认证信息。

| 项目 | 内容 |
|------|------|
| **描述** | 修改认证信息后重新提交，重新走 OCR + 风控流程 |
| **权限** | 需登录 |
| **业务规则** | 修改期间保持之前的认证状态；重新校验通过后保持已认证，失败则变为未认证 |

**Request Body (multipart/form-data):**

```typescript
// 同 SubmitKYCRequest
```

**Response 200:**

```typescript
// 同 SubmitKYCResponse
```

---

## 三、Merchant — 商家管理模块（Web 后台）

### GET /merchants

商家列表查询（支持筛选+分页）。

| 项目 | 内容 |
|------|------|
| **描述** | 查询商家列表，支持多维度筛选和分页 |
| **权限** | 需登录（admin / operator / advisor） |
| **数据权限** | admin/operator 查看全量；advisor 仅查看自己绑定的商家 |

**Query Parameters:**

```typescript
interface MerchantListQuery extends PaginationQuery {
  /** 商家名称关键词（模糊搜索） */
  name?: string;
  /** 商家类型筛选 */
  type?: 'buyer' | 'seller';
  /** 商家状态筛选 */
  status?: 'active' | 'disabled';
  /** 认证状态筛选 */
  authStatus?: 'verified' | 'unverified' | 'restricted';
  /**
   * 维护人 ID 筛选
   * 仅 admin/operator 可见此筛选项
   * advisor 自动锁定为自己
   */
  advisorId?: string;
  /** 排序字段，默认 createdAt */
  sortBy?: 'createdAt' | 'name' | 'status';
  /** 排序方向，默认 desc */
  sortOrder?: 'asc' | 'desc';
}
```

**Response 200:**

```typescript
interface MerchantListResponse extends PaginatedResponse<MerchantListItem> {}

interface MerchantListItem {
  id: string;
  name: string;
  type: MerchantType[];
  status: MerchantStatus;
  authStatus: AuthStatus;
  advisor: {
    id: string;
    displayName: string;
    obAccountId: string;
  } | null;
  createdAt: string;
}
```

---

### GET /merchants/:id

商家详情。

| 项目 | 内容 |
|------|------|
| **描述** | 获取商家完整详情（基本信息、KYC、限额、保证金、维护人） |
| **权限** | admin / operator / advisor（需数据权限） |

**Response 200:**

```typescript
interface MerchantDetailResponse {
  /** 基本信息 */
  merchant: Merchant;
  /** 个人 KYC 记录 */
  kycRecord: KYCRecord | null;
  /** 企业 KYC */
  companyKYC: CompanyKYC | null;
  /** 限额配置 */
  limitConfig: LimitConfig | null;
  /** 最新保证金记录 */
  deposit: DepositRecord | null;
  /** 当前维护人信息 */
  advisor: {
    id: string;
    displayName: string;
    obAccountId: string;
    boundAt: string;
  } | null;
  /** KYC 验证记录列表（时间倒序） */
  kycVerificationLogs: Array<{
    verifiedAt: string;
    verificationType: 'initial' | 'resubmit';
    success: boolean;
    failureReason: string | null;
  }>;
}
```

**错误码:**

| 错误码 | 说明 |
|--------|------|
| `MERCHANT_NOT_FOUND` | 商家不存在 |
| `MERCHANT_ACCESS_DENIED` | 无权访问该商家（数据权限不足） |

---

### POST /merchants

添加商家（Web 后台单页录入）。

| 项目 | 内容 |
|------|------|
| **描述** | 录入新商家信息（基本信息+KYC+企业信息），提交后自动校验证件唯一性和制裁名单 |
| **权限** | admin / advisor（需 merchant:create 权限） |
| **业务规则** | 销售添加 → 自动绑定；管理员添加 → 默认未分配 |

**Request Body:**

```typescript
interface CreateMerchantRequest {
  /** 基本信息 */
  basic: {
    /** 商家名称，必填 */
    name: string;
    /** 商家类型，必填，至少一项 */
    type: MerchantType[];
    /** 手机号（三选一必填） */
    phone?: string;
    /** 邮箱（三选一必填） */
    email?: string;
    /** WhatsApp（三选一必填） */
    whatsapp?: string;
    /** 所在地区，必填 */
    region: {
      country: string;
      province?: string;
      city?: string;
    };
    /** 备注 */
    remark?: string;
  };
  /** 个人 KYC 信息 */
  kyc: {
    /** 证件类型，必填 */
    idType: IdDocumentType;
    /** 证件号码，必填 */
    idNumber: string;
    /** 证件姓名，必填 */
    fullName: string;
    /** 证件有效期，必填，不可为过去日期 */
    expiryDate: string;
    /** 证件正面图片 URL（预上传至 OSS），选填 */
    idFrontUrl?: string;
    /** 证件反面图片 URL，选填 */
    idBackUrl?: string;
  };
  /** 企业 KYC 信息（整体选填） */
  companyKYC?: {
    companyName?: string;
    licenseType?: string;
    businessRegNo?: string;
    representative?: string;
    address?: string;
    expiryDate?: string;
    licenseUrl?: string;
  };
}
```

**Response 201:**

```typescript
interface CreateMerchantResponse {
  /** 新建商家 ID */
  merchantId: string;
  /** 认证校验结果 */
  kycResult: {
    passed: boolean;
    status: AuthStatus;
    rejectReason: string | null;
  };
  /** 自动绑定的维护人（销售添加时） */
  boundAdvisor: {
    id: string;
    displayName: string;
  } | null;
}
```

**错误码:**

| 错误码 | 说明 |
|--------|------|
| `MERCHANT_DUPLICATE_ID` | 该证件号已关联其他商家（409） |
| `MERCHANT_SANCTION_HIT` | 制裁名单命中 |
| `MERCHANT_CONTACT_REQUIRED` | 手机号/邮箱/WhatsApp 至少填写一项 |
| `MERCHANT_TYPE_REQUIRED` | 商家类型至少选择一项 |

---

### PUT /merchants/:id

编辑商家信息。

| 项目 | 内容 |
|------|------|
| **描述** | 更新商家基本信息、KYC 信息 |
| **权限** | 需 merchant:edit 权限 + 数据权限 |
| **业务规则** | 修改 KYC 信息后自动重新走 OCR + 风控流程 |

**Request Body:**

```typescript
interface UpdateMerchantRequest {
  basic?: Partial<CreateMerchantRequest['basic']>;
  kyc?: Partial<CreateMerchantRequest['kyc']>;
  companyKYC?: Partial<CreateMerchantRequest['companyKYC']>;
}
```

**Response 200:**

```typescript
interface UpdateMerchantResponse {
  success: boolean;
  /** KYC 重新校验结果（若修改了 KYC 信息） */
  kycResult?: {
    passed: boolean;
    status: AuthStatus;
    rejectReason: string | null;
  };
}
```

---

### PATCH /merchants/:id/status

切换商家状态（启用/停用）。

| 项目 | 内容 |
|------|------|
| **描述** | 启用或停用商家账号 |
| **权限** | 需 merchant:status 权限 + 数据权限 |
| **业务规则** | 停用后商家不可在 APP 下单 |

**Request Body:**

```typescript
interface UpdateMerchantStatusRequest {
  /** 目标状态 */
  status: 'active' | 'disabled';
}
```

**Response 200:**

```typescript
interface UpdateMerchantStatusResponse {
  success: boolean;
  /** 更新后的状态 */
  status: MerchantStatus;
}
```

---

## 四、Limit — 限额管理模块

### GET /merchants/:id/limit

查询商家限额配置。

| 项目 | 内容 |
|------|------|
| **描述** | 获取商家当前的每日下单限额和关联保证金信息 |
| **权限** | 需登录 + 数据权限 |

**Response 200:**

```typescript
interface LimitConfigResponse {
  /** 当前限额配置 */
  limitConfig: LimitConfig | null;
  /** 最新保证金记录 */
  deposit: DepositRecord | null;
  /** 限额可配置范围 */
  range: {
    /** 最小值（业务默认） */
    min: number;
    /** 最大值（保证金×10，未提交保证金时等于 min） */
    max: number;
  };
  /** 今日已用额度 */
  todayUsed: number;
}
```

---

### PUT /merchants/:id/limit

配置每日下单限额。

| 项目 | 内容 |
|------|------|
| **描述** | 设置商家的每日下单限额 |
| **权限** | 需「海外回收商户编辑权限」+ 数据权限 |
| **业务规则** | 限额 ≥ 0 且 ≤ 保证金×10；未提交保证金时仅可设为默认最小值 |

**Request Body:**

```typescript
interface UpdateLimitRequest {
  /** 每日下单限额（HKD），正整数 */
  dailyLimit: number;
}
```

**Response 200:**

```typescript
interface UpdateLimitResponse {
  success: boolean;
  /** 更新后的限额 */
  dailyLimit: number;
}
```

**错误码:**

| 错误码 | 说明 |
|--------|------|
| `LIMIT_EXCEEDS_DEPOSIT` | 限额超过保证金×10 上限 |
| `LIMIT_NO_DEPOSIT` | 未提交保证金，不可调高限额 |
| `LIMIT_INVALID_VALUE` | 限额必须为非负整数 |

---

## 五、Deposit — 保证金管理模块

### POST /merchants/:id/deposit

录入保证金信息。

| 项目 | 内容 |
|------|------|
| **描述** | 运营人员录入商家保证金金额和转账凭证 |
| **权限** | 需「海外回收商户编辑权限」+ 数据权限 |

**Request Body:**

```typescript
interface CreateDepositRequest {
  /** 保证金金额（HKD），正整数 */
  amount: number;
  /**
   * 转账凭证图片 URL 数组（预上传至 OSS）
   * JPG/PNG，单张 ≤ 5MB，最多 3 张
   */
  proofImageUrls: string[];
}
```

**Response 201:**

```typescript
interface CreateDepositResponse {
  /** 保证金记录 ID */
  depositId: string;
  /** 状态 */
  status: 'pending';
}
```

---

### PATCH /merchants/:id/deposit/:depositId/confirm

确认保证金。

| 项目 | 内容 |
|------|------|
| **描述** | 运营确认商家的保证金转账记录 |
| **权限** | 需「海外回收商户编辑权限」 |
| **业务规则** | 确认后限额上限生效（保证金×10） |

**Request Body:**

```typescript
interface ConfirmDepositRequest {
  /** 确认或拒绝 */
  action: 'confirm' | 'reject';
  /** 拒绝原因（action 为 reject 时必填） */
  rejectReason?: string;
}
```

**Response 200:**

```typescript
interface ConfirmDepositResponse {
  success: boolean;
  status: 'confirmed' | 'rejected';
  /** 确认后新的限额可配置上限 */
  newLimitMax: number | null;
}
```

---

## 六、Advisor — 维护人管理模块

### POST /merchants/:id/advisor/bind

绑定维护人。

| 项目 | 内容 |
|------|------|
| **描述** | 为商家绑定维护人（顾问/销售） |
| **权限** | 需 advisor:manage 权限 |
| **业务规则** | 绑定后维护人可查看该商家数据 |

**Request Body:**

```typescript
interface BindAdvisorRequest {
  /** 维护人用户 ID（从 OB 账号列表选择） */
  advisorUserId: string;
  /** 绑定原因，必填 */
  reason: string;
}
```

**Response 200:**

```typescript
interface BindAdvisorResponse {
  success: boolean;
  binding: {
    id: string;
    advisorUserId: string;
    advisorName: string;
    boundAt: string;
  };
}
```

**错误码:**

| 错误码 | 说明 |
|--------|------|
| `ADVISOR_ALREADY_BOUND` | 该商家已绑定维护人，请先解绑或使用更换 |
| `ADVISOR_USER_NOT_FOUND` | 维护人用户不存在 |
| `ADVISOR_INVALID_ROLE` | 目标用户角色不是 advisor |

---

### DELETE /merchants/:id/advisor

解绑维护人。

| 项目 | 内容 |
|------|------|
| **描述** | 解除商家与维护人的绑定关系 |
| **权限** | 需 advisor:manage 权限 |
| **业务规则** | 解绑后维护人**立即**失去该商家的数据访问权 |

**Request Body:**

```typescript
interface UnbindAdvisorRequest {
  /** 解绑原因，必填 */
  reason: string;
}
```

**Response 200:**

```typescript
interface UnbindAdvisorResponse {
  success: boolean;
}
```

---

### PUT /merchants/:id/advisor

更换维护人。

| 项目 | 内容 |
|------|------|
| **描述** | 原子操作：解绑旧维护人 + 绑定新维护人 |
| **权限** | 需 advisor:manage 权限 |
| **业务规则** | 记录变更原因到操作日志；旧维护人立即失去访问权 |

**Request Body:**

```typescript
interface ReassignAdvisorRequest {
  /** 新维护人用户 ID */
  newAdvisorUserId: string;
  /** 变更原因，必填 */
  reason: string;
}
```

**Response 200:**

```typescript
interface ReassignAdvisorResponse {
  success: boolean;
  /** 旧维护人 */
  previousAdvisor: {
    id: string;
    displayName: string;
  };
  /** 新维护人 */
  newAdvisor: {
    id: string;
    displayName: string;
    boundAt: string;
  };
}
```

---

## 七、Export — 导出模块

### POST /exports

创建导出任务。

| 项目 | 内容 |
|------|------|
| **描述** | 创建异步导出任务（商家列表等） |
| **权限** | 需 export:create 权限 |
| **业务规则** | 异步生成，文件 30 天有效 |

**Request Body:**

```typescript
interface CreateExportRequest {
  /** 导出来源页面标识 */
  sourcePage: 'merchant-list';
  /** 当前筛选条件（与列表查询一致，按条件导出） */
  filters?: Partial<MerchantListQuery>;
}
```

**Response 202:**

```typescript
interface CreateExportResponse {
  /** 导出任务 ID */
  exportId: string;
  /** 状态 */
  status: 'generating';
  /** 预计完成时间（秒） */
  estimatedSeconds: number;
}
```

---

### GET /exports

查询我的导出文件列表。

| 项目 | 内容 |
|------|------|
| **描述** | 查询当前用户的导出文件列表 |
| **权限** | 需登录 |

**Response 200:**

```typescript
interface ExportListResponse {
  items: ExportFile[];
}
```

---

## 八、Operation Log — 操作日志（内嵌）

操作日志不单独暴露 CRUD API，而是在商家详情接口中返回。日志由后端在每次变更操作时自动记录。

### GET /merchants/:id/logs

查询商家操作日志。

| 项目 | 内容 |
|------|------|
| **描述** | 获取商家的操作日志列表，按时间倒序 |
| **权限** | 需登录 + 数据权限 |

**Query Parameters:**

```typescript
interface LogQuery extends PaginationQuery {
  /** 操作类型筛选 */
  operationType?: string;
}
```

**Response 200:**

```typescript
interface LogListResponse extends PaginatedResponse<OperationLog> {}
```
