---
name: claude-code-local
description: 调用本地Claude Code CLI进行代码生成、分析和重构
metadata: {"clawdbot":{"emoji":"💻","requires":{"anyBins":["claude"]}}}
---

# Claude Code 本地技能

使用本地安装的 **Claude Code CLI** 进行代码生成、分析、重构和调试。

## 🚀 快速开始

### 基本用法

```bash
# 在指定目录运行Claude Code任务
bash pty:true workdir:~/project command:"claude '你的代码任务描述'"

# 后台运行（长任务）
bash pty:true workdir:~/project background:true command:"claude '重构用户认证模块，添加OAuth支持'"
```

### 为什么需要 PTY？

Claude Code 是交互式终端应用，需要伪终端（PTY）才能正常工作：
- ✅ **正确**：`bash pty:true command:"claude '任务'"`
- ❌ **错误**：`bash command:"claude '任务'"`（可能输出异常或挂起）

## 📁 工作目录管理

始终指定 `workdir` 参数，将Claude限制在特定项目目录：

```bash
# 安全：限制在项目目录
bash pty:true workdir:~/myapp command:"claude '添加用户注册表单'"

# 危险：无工作目录限制
bash pty:true command:"claude '添加用户注册表单'"  # Claude可能访问系统文件
```

## 🔧 常用模式

### 1. 代码生成
```bash
# 生成新功能
bash pty:true workdir:~/project command:"claude '创建REST API端点处理用户CRUD操作'"

# 添加测试
bash pty:true workdir:~/project command:"claude '为UserService添加单元测试'"
```

### 2. 代码分析
```bash
# 代码审查
bash pty:true workdir:~/project command:"claude '审查src/auth目录的代码质量，找出潜在问题'"

# 性能优化
bash pty:true workdir:~/project command:"claude '分析数据库查询性能，提出优化建议'"
```

### 3. 重构任务
```bash
# 后台运行重构
bash pty:true workdir:~/project background:true command:"claude '将class组件重构为React函数组件，使用hooks'"
```

### 4. 调试帮助
```bash
# 错误诊断
bash pty:true workdir:~/project command:"claude '分析这个错误：TypeError: Cannot read properties of undefined'"
```

## ⚙️ Bash工具参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `command` | string | shell命令，如 `"claude '任务描述'"` |
| `pty` | boolean | **必须启用**！为交互式CLI分配伪终端 |
| `workdir` | string | 工作目录（Claude只看到此文件夹内容） |
| `background` | boolean | 后台运行，返回sessionId用于监控 |
| `timeout` | number | 超时时间（秒） |
| `elevated` | boolean | 在主机而非沙箱中运行（如果允许） |

## 📊 进程管理（后台任务）

后台任务可通过 `process` 工具管理：

```bash
# 启动后台任务
bash pty:true workdir:~/project background:true command:"claude '实现购物车功能'"
# 返回: {"sessionId": "abc123"}

# 查看运行中的会话
process action:list

# 获取输出日志
process action:log sessionId:abc123

# 发送输入（如Claude提问时）
process action:submit sessionId:abc123 data:"是的，继续"

# 终止任务
process action:kill sessionId:abc123
```

## 🎯 最佳实践

### 1. 明确的任务描述
```bash
# ✅ 明确
claude '创建用户模型：字段包括id、email、name、createdAt，使用TypeScript接口'

# ❌ 模糊
claude '做用户相关的东西'
```

### 2. 提供上下文
```bash
# 附加当前文件状态
bash pty:true workdir:~/project command:"claude '修复这个函数：$(cat src/utils.ts | head -20)'"
```

### 3. 迭代式改进
```bash
# 第一步：生成基础代码
bash pty:true workdir:~/project command:"claude '创建登录页面组件'"

# 第二步：基于反馈改进
bash pty:true workdir:~/project command:"claude '添加表单验证和错误处理到上一步创建的登录页面'"
```

## ⚠️ 注意事项

1. **Git仓库要求**：Claude Code通常需要在git仓库中运行。如遇错误，可创建临时仓库：
   ```bash
   TEMP_DIR=$(mktemp -d) && cd $TEMP_DIR && git init && claude '你的任务'
   ```

2. **会话管理**：Claude Code会记住对话上下文。使用新目录或明确要求新会话。

3. **输出处理**：Claude的输出可能包含ANSI颜色代码。PTY模式可确保正确显示。

4. **资源限制**：长时间运行的任务应使用`background:true`并定期检查进度。

## 🔍 故障排除

### 常见问题

**Q: Claude Code没有响应或输出异常**
- ✅ 确保启用 `pty:true`
- ✅ 检查工作目录是否存在且为git仓库
- ✅ 验证Claude CLI安装：`claude --version`

**Q: 任务被中断**
- 增加 `timeout` 参数
- 使用后台模式并手动监控

**Q: Claude无法访问特定文件**
- 确认 `workdir` 正确设置
- 检查文件路径在指定工作目录内

## 🎯 预设任务模板

以下模板可直接复制使用，或根据具体需求调整：

### 1. 代码生成模板

#### 📱 前端组件生成
```bash
# React函数组件
bash pty:true workdir:~/frontend command:"claude '创建React函数组件UserProfile，包含：头像、用户名、邮箱、编辑按钮，使用TypeScript和Tailwind CSS'"

# Vue 3组件
bash pty:true workdir:~/frontend command:"claude '创建Vue 3组合式API组件LoginForm，包含：邮箱/密码输入、验证、提交处理，使用<script setup>语法'"
```

#### 🖥️ 后端API生成
```bash
# Express.js REST API
bash pty:true workdir:~/backend command:"claude '创建Express.js REST API端点：/api/users，支持GET(列表)、POST(创建)、PUT(更新)、DELETE(删除)，包含JWT验证和错误处理'"

# 数据库模型
bash pty:true workdir:~/backend command:"claude '创建User模型：id、name、email、password(加密)、createdAt，使用Prisma ORM，包含类型定义和关系'"
```

#### 🧪 测试代码生成
```bash
# 单元测试
bash pty:true workdir:~/project command:"claude '为UserService类添加完整的单元测试，覆盖所有公有方法，使用Jest和mock'"

# 集成测试
bash pty:true workdir:~/project command:"claude '创建用户注册流程的集成测试，包含：API调用、数据库验证、错误场景'"
```

### 2. 代码审查模板

#### 🔒 安全审查
```bash
bash pty:true workdir:~/project command:"claude '审查src/目录的安全漏洞：1.SQL注入 2.XSS攻击 3.认证绕过 4.敏感数据泄露 5.依赖漏洞'"
```

#### ⚡ 性能审查
```bash
bash pty:true workdir:~/project command:"claude '分析项目性能问题：1.数据库查询优化 2.内存泄漏 3.响应时间 4.打包大小 5.缓存策略'"
```

#### 🎨 代码质量审查
```bash
bash pty:true workdir:~/project command:"claude '审查代码质量：1.重复代码 2.函数复杂度 3.命名规范 4.注释完整性 5.架构一致性'"
```

### 3. 重构模板

#### 🏗️ 架构重构
```bash
bash pty:true workdir:~/project background:true command:"claude '将单体应用重构为微服务架构：用户服务、产品服务、订单服务，定义API契约和数据流'"
```

#### 🔄 技术栈迁移
```bash
bash pty:true workdir:~/project command:"claude '将JavaScript项目迁移到TypeScript：添加类型定义、配置tsconfig、修复类型错误'"
```

#### 🧹 代码清理
```bash
bash pty:true workdir:~/project command:"claude '清理代码：1.删除未使用变量 2.简化复杂函数 3.统一代码风格 4.更新过时API'"
```

### 4. 调试模板

#### 🐛 错误分析
```bash
# 捕获错误信息并分析
ERROR=$(cat error.log 2>/dev/null || echo "错误信息")
bash pty:true workdir:~/project command:"claude '分析并修复这个错误：$ERROR'"
```

#### 📊 性能调试
```bash
# 分析性能日志
PERF_LOG=$(cat performance.log 2>/dev/null || echo "响应时间: 2.5s, 内存使用: 85%")
bash pty:true workdir:~/project command:"claude '分析性能问题并给出优化建议：$PERF_LOG'"
```

### 5. 文档模板

#### 📝 API文档
```bash
bash pty:true workdir:~/project command:"claude '为项目生成OpenAPI/Swagger文档，包含所有端点、请求/响应示例、错误码'"
```

#### 🗂️ 项目文档
```bash
bash pty:true workdir:~/project command:"claude '生成完整的项目文档：1.README安装说明 2.架构设计 3.API参考 4.部署指南 5.开发规范'"
```

### 6. 配置模板

#### ⚙️ 环境配置
```bash
bash pty:true workdir:~/project command:"claude '创建项目配置文件：.env.example、docker-compose.yml、nginx.conf、CI/CD pipeline配置'"
```

#### 🧰 工具配置
```bash
bash pty:true workdir:~/project command:"claude '配置开发工具：ESLint规则、Prettier格式化、Husky git钩子、测试覆盖率配置'"
```

## 📈 进阶用法

### 并行处理多个任务
```bash
# 任务1：前端组件
bash pty:true workdir:~/frontend background:true command:"claude '创建仪表板组件'"

# 任务2：后端API
bash pty:true workdir:~/backend background:true command:"claude '实现用户数据API端点'"
```

### 自动化工作流
```bash
# 1. 生成代码
bash pty:true workdir:~/project command:"claude '创建数据模型'"

# 2. 运行测试
bash pty:true workdir:~/project command:"npm test"

# 3. 如有失败，请求修复
bash pty:true workdir:~/project command:"claude '修复测试失败：$(cat test-output.log)'"
```

---

**提示**：Claude Code功能强大，但需要明确的指令。提供越详细的上下文，得到的代码质量越高。