# FoneSquare 权限矩阵

> 管理后台权限分为**功能权限**和**数据权限**两个独立维度，互相正交、组合生效。  
> 实际能否操作 = 拥有该功能权限 ∧ 该商家落在数据权限范围内。

---

## 角色定义

| 角色 | 代码 | 说明 |
|------|------|------|
| **超级管理员** | `admin` | 拥有全部功能权限 + 全量数据权限，可管理所有商家和用户 |
| **运营人员** | `operator` | 可配置的功能权限 + 全量数据权限，日常运营操作 |
| **维护人/顾问** | `advisor` | 可配置的功能权限 + **仅自己绑定的商家**数据权限 |

---

## 一、功能权限表

| 权限代码 | 权限名称 | 说明 | admin | operator | advisor |
|----------|----------|------|:-----:|:--------:|:-------:|
| `merchant:view` | 查看商家 | 查看商家列表和详情 | ✅ | ✅ | ✅ |
| `merchant:create` | 添加商家 | 通过后台单页表单添加新商家 | ✅ | ✅ | ✅ |
| `merchant:edit` | 编辑商家 | 编辑商家基本信息 | ✅ | ✅ | ❌ |
| `merchant:status` | 启停商家 | 启用/停用商家账号 | ✅ | ✅ | ❌ |
| `kyc:view` | 查看KYC | 查看KYC认证材料（脱敏展示） | ✅ | ✅ | ✅ |
| `kyc:view-raw` | 查看KYC原值 | 点击查看证件号等敏感信息原值 | ✅ | ✅ | ❌ |
| `kyc:edit` | 编辑KYC | 修改认证信息（触发重新校验） | ✅ | ✅ | ❌ |
| `limit:view` | 查看限额 | 查看限额和保证金信息 | ✅ | ✅ | ✅ |
| `limit:config` | 配置限额 | 编辑每日下单限额值 | ✅ | ✅ | ❌ |
| `deposit:view` | 查看保证金 | 查看保证金记录和凭证 | ✅ | ✅ | ✅ |
| `deposit:manage` | 管理保证金 | 录入/修改保证金金额、上传凭证、确认状态 | ✅ | ✅ | ❌ |
| `advisor:manage` | 管理维护人 | 绑定/解绑/更换商家的维护人 | ✅ | ❌ | ❌ |
| `advisor:view` | 查看维护人 | 查看维护人绑定信息和历史 | ✅ | ✅ | ✅ |
| `export:create` | 创建导出 | 导出商家列表等数据文件 | ✅ | ✅ | ✅ |
| `export:view` | 查看导出 | 查看我的导出文件列表 | ✅ | ✅ | ✅ |
| `log:view` | 查看日志 | 查看操作日志 | ✅ | ✅ | ✅ |
| `user:manage` | 管理用户 | 管理后台用户账号（CRUD） | ✅ | ❌ | ❌ |

> **注意**: `limit:config` 和 `deposit:manage` 对应 PRD 中的「海外回收商户编辑权限」，单独管控限额和保证金功能，与现有回收商编辑权限独立。

---

## 二、数据权限

数据权限控制用户可见的**数据范围**，仅决定"能看什么"，不决定"能做什么"。

| 维度 | admin | operator | advisor |
|------|:-----:|:--------:|:-------:|
| 商家列表范围 | 全量海外商家 | 全量海外商家 | **仅自己绑定的商家** |
| 维护人筛选下拉 | ✅ 可见，可选任意维护人 | ✅ 可见，可选任意维护人 | ❌ 不可见，自动锁定为本人 |
| 商家详情访问 | 任意商家 | 任意商家 | **仅自己绑定的商家** |
| 操作日志查看 | 全量 | 全量 | 仅自己绑定的商家的日志 |
| 导出数据范围 | 按筛选条件（全量） | 按筛选条件（全量） | 按筛选条件（仅自己绑定） |

### 数据权限 SQL 示例

```sql
-- advisor 查询商家列表时自动附加条件
SELECT m.* FROM merchants m
WHERE m.advisor_id = :currentUserId  -- advisor 仅查看自己绑定的
  AND m.status = :filterStatus       -- 其他筛选条件
ORDER BY m.created_at DESC
LIMIT :pageSize OFFSET :offset;

-- admin/operator 无此限制
SELECT m.* FROM merchants m
WHERE m.status = :filterStatus
ORDER BY m.created_at DESC
LIMIT :pageSize OFFSET :offset;
```

---

## 三、API 端点 × 权限映射表

| API 端点 | Method | 功能权限 | 数据权限 | 说明 |
|----------|--------|----------|----------|------|
| `/auth/otp/send` | POST | 无 | 无 | 公开接口 |
| `/auth/otp/verify` | POST | 无 | 无 | 公开接口 |
| `/auth/password/set` | POST | 登录即可 | 无 | 仅操作自己的密码 |
| `/auth/login` | POST | 无 | 无 | 公开接口 |
| `/auth/password/reset` | POST | 无 | 无 | 通过 OTP 验证 |
| `/kyc/submit` | POST | APP 登录 | 无 | APP 端提交自己的 KYC |
| `/kyc/status` | GET | APP 登录 | 无 | 查看自己的 KYC 状态 |
| `/kyc/resubmit` | PUT | APP 登录 | 无 | 重新提交自己的 KYC |
| `/merchants` | GET | `merchant:view` | ✅ 受限 | advisor 仅返回自己绑定的 |
| `/merchants/:id` | GET | `merchant:view` | ✅ 受限 | advisor 仅可访问自己绑定的 |
| `/merchants` | POST | `merchant:create` | 无 | 创建后按角色绑定 |
| `/merchants/:id` | PUT | `merchant:edit` | ✅ 受限 | 需有该商家的数据权限 |
| `/merchants/:id/status` | PATCH | `merchant:status` | ✅ 受限 | 需有该商家的数据权限 |
| `/merchants/:id/limit` | GET | `limit:view` | ✅ 受限 | 需有该商家的数据权限 |
| `/merchants/:id/limit` | PUT | `limit:config` | ✅ 受限 | 需「海外回收商户编辑权限」|
| `/merchants/:id/deposit` | POST | `deposit:manage` | ✅ 受限 | 需「海外回收商户编辑权限」|
| `/merchants/:id/deposit/:depositId/confirm` | PATCH | `deposit:manage` | ✅ 受限 | 需「海外回收商户编辑权限」|
| `/merchants/:id/advisor/bind` | POST | `advisor:manage` | 无 | 仅 admin |
| `/merchants/:id/advisor` | DELETE | `advisor:manage` | 无 | 仅 admin |
| `/merchants/:id/advisor` | PUT | `advisor:manage` | 无 | 仅 admin |
| `/merchants/:id/logs` | GET | `log:view` | ✅ 受限 | 需有该商家的数据权限 |
| `/exports` | POST | `export:create` | 导出范围受限 | advisor 导出仅含自己绑定的 |
| `/exports` | GET | `export:view` | 仅自己的文件 | 每人只能看自己的导出 |

---

## 四、权限校验中间件伪代码

```typescript
/**
 * 权限校验中间件
 * 同时检查功能权限和数据权限
 */
async function checkPermission(
  requiredPermission: string,
  checkDataAccess: boolean = false,
) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const user = req.currentUser;

    // 1. 功能权限校验
    if (!user.permissions.includes(requiredPermission)) {
      throw new ForbiddenError('AUTH_FORBIDDEN', '无此功能权限');
    }

    // 2. 数据权限校验（仅当需要时）
    if (checkDataAccess && req.params.id) {
      const merchantId = req.params.id;

      if (user.role === 'advisor') {
        // advisor 仅可访问自己绑定的商家
        const binding = await AdvisorBinding.findOne({
          where: {
            merchantId,
            advisorUserId: user.id,
            unboundAt: null, // 当前有效绑定
          },
        });

        if (!binding) {
          throw new ForbiddenError(
            'MERCHANT_ACCESS_DENIED',
            '无权访问该商家（非绑定维护人）',
          );
        }
      }
      // admin 和 operator 不做数据权限限制
    }

    next();
  };
}
```

---

## 五、边界场景说明

### 1. Advisor 被解绑后立即失去访问权

- **场景**: Admin 将 advisor A 从商家 M 解绑
- **行为**: 解绑操作写入 `AdvisorBinding.unboundAt` 后，advisor A 的后续所有请求中涉及商家 M 的均返回 `403 MERCHANT_ACCESS_DENIED`
- **实时生效**: 不依赖 Token 刷新，每次请求实时查询绑定关系
- **影响范围**: 商家详情、KYC 查看、限额查看、日志查看、导出（不含该商家数据）

### 2. Advisor 添加商家后自动绑定

- **场景**: Advisor B 通过后台添加新商家 N
- **行为**: 
  1. 创建商家记录
  2. 自动创建 `AdvisorBinding` 记录（advisorUserId=B, reason=商家创建自动绑定）
  3. 设置 `Merchant.advisorId = B`
  4. 记录操作日志
- **结果**: Advisor B 立即可访问商家 N

### 3. Admin 添加商家后默认未分配

- **场景**: Admin C 通过后台添加新商家 P
- **行为**: 
  1. 创建商家记录
  2. `Merchant.advisorId = null`
  3. 不创建 `AdvisorBinding` 记录
- **结果**: 商家 P 在维护人筛选中显示为「未分配」；任何 advisor 都无法看到该商家，直到 admin 手动绑定

### 4. 更换维护人的原子操作

- **场景**: Admin 将商家 M 的维护人从 A 更换为 B
- **行为**（需在同一事务内完成）:
  1. 旧绑定记录设置 `unboundAt = now()`
  2. 创建新绑定记录 `advisorUserId = B`
  3. 更新 `Merchant.advisorId = B`
  4. 记录操作日志（含 before: A, after: B）
- **结果**: A 立即失去访问权，B 立即获得访问权

### 5. 维护人筛选仅管理员可见

- **场景**: Advisor 登录后查看商家列表
- **行为**: 
  - 前端隐藏「维护人」筛选下拉框
  - 后端自动在查询条件中追加 `advisor_id = currentUserId`
  - 列表仅显示自己绑定的商家

### 6. 证件号脱敏与查看原值

- **场景**: 查看商家 KYC 材料中的证件号
- **行为**:
  - 默认脱敏展示：`A***456(7)`
  - 拥有 `kyc:view-raw` 权限的用户可点击「查看原值」按钮
  - 查看原值操作记录到操作日志（审计追踪）
  - Advisor 角色默认不具备 `kyc:view-raw` 权限

### 7. 导出数据的权限过滤

- **场景**: Advisor 点击「导出」按钮
- **行为**:
  - 导出任务执行时，自动按 advisor 的数据权限过滤
  - 导出文件仅包含该 advisor 绑定的商家数据
  - 不会泄露未绑定商家的信息

### 8. 商家停用后的权限影响

- **场景**: Admin 停用商家 M
- **行为**:
  - 商家状态变为 `disabled`
  - APP 端该商家不可下单（提示「账号已被停用」）
  - Web 后台仍可查看该商家信息（不影响管理操作）
  - 维护人绑定关系不变

### 9. 保证金金额下调的限额联动

- **场景**: 运营将商家保证金从 10,000 HKD 下调为 5,000 HKD，但当前限额为 80,000 HKD
- **行为**: 
  - 新限额上限 = 5,000 × 10 = 50,000 HKD
  - 当前限额 80,000 > 50,000，系统提示「请先调低每日限额至 50,000 HKD 以下」
  - 需先修改限额，再修改保证金
