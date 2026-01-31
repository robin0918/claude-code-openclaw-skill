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