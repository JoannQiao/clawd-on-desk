#!/usr/bin/env python3
"""Fix corrupted Mermaid blocks in FoneSquare-PRD-v2.html.
Mermaid diagrams were pre-rendered to inline SVG by the browser on save.
This script restores the original Mermaid source text."""
import re, sys

SRC = "/Users/qiaoqian/clawd-on-desk/FoneSquare-PRD-v2.html"

MERMAID_SOURCES = {
    "页面结构关系": """flowchart LR
  Login["OB账号登录"] --> RoleCheck{"角色判断"}
  RoleCheck -->|管理员| AdminList["商家列表（全量数据）"]
  RoleCheck -->|销售| SalesList["商家列表（仅绑定数据）"]
  AdminList --> Detail["商家详情"]
  SalesList --> Detail
  AdminList --> AddMerchant["添加商家"]
  Detail --> Tab1["基本信息 Tab"]
  Detail --> Tab2["限额与保证金 Tab"]
  Detail --> Tab3["销售绑定 Tab"]
  Detail --> Tab4["操作日志 Tab"]""",

    "商家状态机": """stateDiagram-v2
    s1 : 使用
    s2 : 停用
    [*] --> s1 : 创建商家
    s1 --> s2 : 管理员停用
    s2 --> s1 : 管理员启用""",

    "管理员操作流程": """flowchart TD
    L[商家列表] --> S[搜索+筛选+导出]
    L --> A[添加商家]
    L --> D[查看商家详情]
    A --> A1[填写基本信息+KYC]
    A1 --> A2[创建成功,状态:使用]
    D --> T1[基本信息 - 可编辑]
    D --> T2[限额与保证金 - 可配置]
    D --> T3[销售绑定 - 分配或更换]
    D --> T4[操作日志 - 全部记录]
    D --> OP[停用或启用]""",

    "销售操作流程": """flowchart TD
    L[自己的商家列表] --> S[搜索+筛选]
    L --> A[添加商家,自动绑定自己]
    L --> D[查看商家详情]
    A --> A1[填写基本信息+KYC]
    A1 --> A2[创建成功,自动绑定]
    D --> T1[基本信息 - 仅查看]
    D --> T2[限额与保证金 - 仅查看]
    D --> T4[操作日志 - 自己相关]""",

    "添加商家业务流程": """flowchart TD
    START[进入添加商家页面] --> FILL[填写基本信息+KYC+企业信息]
    FILL --> CHECK{必填校验}
    CHECK -->|不通过| ERR[高亮缺失字段提示]
    ERR --> FILL
    CHECK -->|通过| SUBMIT[提交创建]
    SUBMIT --> ROLE{当前角色}
    ROLE -->|销售| BIND[自动绑定到当前销售]
    ROLE -->|管理员| UNASSIGN[未分配销售]
    BIND --> OK[创建成功,结果页]
    UNASSIGN --> OK""",

    "整体操作流程": """flowchart TD
  A["OB账号登录"] --> B{"角色判断"}
  B -->|管理员| C["商家列表（全量数据）"]
  B -->|销售| D["商家列表（仅绑定数据）"]
  C --> E["搜索+筛选+导出"]
  C --> F["查看商家详情"]
  C --> G["添加商家"]
  D --> H["搜索+筛选"]
  D --> I["查看商家详情（只读）"]
  D --> G2["添加商家（自动绑定）"]
  F --> J["基本信息 Tab"]
  F --> K["限额与保证金 Tab"]
  F --> L["销售绑定 Tab"]
  F --> M["操作日志 Tab"]
  G --> N["填写信息"] --> O["提交创建"]""",

    "添加商家详细流程": """sequenceDiagram
  participant Admin as 管理员/销售
  participant Web as 管理后台
  participant API as 后端API
  participant Risk as 风控系统
  Admin->>Web: 点击「添加商家」
  Web->>Admin: 展示表单（基本信息+KYC+企业信息）
  Admin->>Web: 填写并上传证件照片
  Web->>Web: 前端必填校验
  alt 校验不通过
    Web->>Admin: 高亮缺失字段
  else 校验通过
    Web->>API: POST /merchant/create
    API->>Risk: 检查证件号是否重复
    alt 证件重复
      API-->>Web: 409 证件已存在
      Web->>Admin: 提示「该证件已关联其他账号」
    else 证件不重复
      API->>API: 创建商家记录
      API-->>Web: 201 Created
      Web->>Admin: 展示「创建成功」结果页
    end
  end""",

    "限额配置流程": """sequenceDiagram
  participant Admin as 管理员
  participant Web as 管理后台
  participant API as 后端API
  Admin->>Web: 进入商家详情 → 限额Tab
  Web->>API: GET /merchant/{id}/quota
  API-->>Web: 返回当前限额配置
  Web->>Admin: 展示限额信息
  Admin->>Web: 修改每日限额值
  Web->>Web: 前端校验（≤保证金×10）
  alt 校验通过
    Web->>API: PUT /merchant/{id}/quota
    API-->>Web: 200 OK
    Web->>Admin: 提示「保存成功」
  else 超过上限
    Web->>Admin: 提示「不可超过保证金×10」
  end""",

    "整体架构": """flowchart LR
    subgraph overseas[海外服务]
        A[商家管理后台]
        B[完整商家数据]
        C[对外查询接口]
    end
    subgraph domestic[国内服务]
        D[CS商家管理系统]
        E[镜像商家数据]
        F[订单+风控+支付]
    end
    A -->|创建+更新+状态变更| D
    F -->|查询海外商家详情| C
    F -->|使用国内商家ID| E""",

    "业务流程闭环": """flowchart TD
    A[海外后台创建商家] --> B[生成海外商家ID]
    B --> C[同步请求国内CS系统]
    C --> D[国内生成国内商家ID]
    D --> E[记录双ID映射关系]
    E --> F[回写国内ID到海外记录]
    F --> G[同步完成]
    G --> H[国内订单系统创建订单]
    H --> I[使用国内商家ID]
    I --> J{需要海外商家详情}
    J -->|是| K[调用海外查询接口]
    J -->|否| L[使用已同步的脱敏摘要]""",

    "KYC 账号合并流程图": """flowchart TD
    A[用户提交KYC] --> B{证件是否已存在}
    B -->|否| C[正常认证流程]
    B -->|是| D[检测到重复身份]
    D --> E[展示已认证账号信息]
    E --> F{用户选择}
    F -->|绑定到已有账号| G[补全登录方式]
    G --> H[OTP二次验证]
    H --> I[绑定完成]
    F -->|取消| J[返回认证页]""",
}

with open(SRC, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")
new_lines = []
i = 0
fixed = 0

while i < len(lines):
    line = lines[i]
    if 'class="mermaid"' in line and 'data-processed="true"' in line:
        heading_text = ""
        for j in range(max(0, i - 5), i):
            m = re.search(r'<h[34][^>]*>(.*?)</h[34]>', lines[j])
            if m:
                heading_text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        
        matched_key = None
        for key in MERMAID_SOURCES:
            if key in heading_text:
                matched_key = key
                break
        
        if matched_key:
            new_lines.append(f'  <pre class="mermaid">\n{MERMAID_SOURCES[matched_key]}\n  </pre>')
            fixed += 1
            print(f"  Fixed: {matched_key} (line {i+1})")
        else:
            # for KYC flowchart, check a wider range
            for j in range(max(0, i - 10), i):
                for key in MERMAID_SOURCES:
                    if key in lines[j]:
                        matched_key = key
                        break
                if matched_key:
                    break
            if matched_key:
                new_lines.append(f'  <pre class="mermaid">\n{MERMAID_SOURCES[matched_key]}\n  </pre>')
                fixed += 1
                print(f"  Fixed: {matched_key} (line {i+1}, wider search)")
            else:
                print(f"  WARNING: Could not match mermaid at line {i+1}, heading: '{heading_text}'")
                new_lines.append(line)
    else:
        new_lines.append(line)
    i += 1

result = "\n".join(new_lines)

# Also fix "海外OB" → "OB账号体系" in text (not in mermaid source)
result = result.replace("海外OB账号", "OB账号")
result = result.replace("海外 OB 账号", "OB账号")
result = result.replace("海外OB", "OB")
result = result.replace("海外运营团队使用的 Web 管理后台", "运营团队使用的 Web 管理后台")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(result)

print(f"\nDone! Fixed {fixed} Mermaid blocks.")
