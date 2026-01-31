# Claude Code 本地技能

这是一个 OPENCLAW 技能，用于调用本地安装的 Claude Code CLI 进行代码生成、分析和重构。

## 功能特性

- ✅ **代码生成**：根据自然语言描述生成代码
- ✅ **代码分析**：审查代码质量，找出潜在问题
- ✅ **重构助手**：协助代码重构和优化
- ✅ **调试支持**：帮助诊断和修复错误
- ✅ **本地执行**：无需API密钥，使用本地Claude Code
- ✅ **项目隔离**：通过工作目录限制文件访问范围

## 系统要求

1. **Claude Code CLI** 已安装并配置
   ```bash
   # 验证安装
   claude --version
   # 应显示版本号，如：2.1.22 (Claude Code)
   ```

2. **Git** 仓库环境（Claude Code通常需要在git仓库中运行）

3. **OPENCLAW** 版本 2026.1.29 或更高

## 安装

此技能已包含在 OPENCLAW 技能目录中。确保技能已启用：

```bash
# 检查技能状态
openclaw skills list | grep claude-code-local

# 验证技能配置
openclaw skills check claude-code-local
```

## 基本用法

### 通过 WhatsApp 使用
```
@openclaw claude 为我的项目添加用户认证功能
```

### 通过 CLI 使用
```bash
openclaw agent --message "claude 创建React登录表单组件" --to +1234567890
```

## 配置选项

### 工作目录设置
在技能配置中可设置默认工作目录，确保Claude只在指定项目中操作。

### 超时设置
长时间任务可配置超时时间，防止任务挂起。

## 示例场景

### 场景1：快速代码生成
```bash
bash pty:true workdir:~/myapp command:"claude '创建Express.js服务器，包含/users和/products路由'"
```

### 场景2：代码审查
```bash
bash pty:true workdir:~/project command:"claude '审查src/components/Button.tsx的代码质量和TypeScript类型安全'"
```

### 场景3：错误修复
```bash
bash pty:true workdir:~/project command:"claude '修复这个TypeScript错误：$(cat error.log)'"
```

## 高级功能

### 后台任务处理
长时间运行的任务可在后台执行，不阻塞当前会话：

```bash
# 启动后台任务
bash pty:true workdir:~/large-project background:true command:"claude '重构整个代码库的模块结构'"

# 监控进度
process action:log sessionId:your_session_id

# 发送交互输入
process action:submit sessionId:your_session_id data:"继续执行"
```

### 多项目并行处理
```bash
# 项目A：前端开发
bash pty:true workdir:~/frontend background:true command:"claude '实现响应式导航栏'"

# 项目B：后端开发
bash pty:true workdir:~/backend background:true command:"claude '设计RESTful API架构'"
```

## 安全注意事项

1. **工作目录限制**：始终指定 `workdir` 参数，防止Claude访问系统文件
2. **权限管理**：Claude Code将遵循当前用户的文件权限
3. **代码审查**：生成的代码应经过人工审查后再部署到生产环境

## 故障排除

### Claude Code不响应
1. 检查Claude CLI是否安装：`claude --version`
2. 确保在git仓库中运行：`git status`
3. 启用PTY模式：`pty:true`

### 输出异常
1. 确保使用 `pty:true` 参数
2. 检查工作目录路径是否正确
3. 验证Claude Code版本兼容性

### 权限错误
1. 确认对工作目录有读写权限
2. 检查文件锁定状态
3. 尝试在临时目录测试

## 更新日志

### v1.0.0 (2026-02-01)
- 初始版本发布
- 支持基本Claude Code调用
- 包含完整的使用文档

## 贡献指南

欢迎提交问题和改进建议。请通过OPENCLAW社区渠道参与贡献。

## 许可证

MIT License