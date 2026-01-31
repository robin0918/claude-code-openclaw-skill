#!/usr/bin/env python3
"""
Claude Code 包装脚本 - 提供更方便的 Claude Code CLI 调用接口

功能：
1. 参数解析和验证
2. 工作目录管理
3. 错误处理和日志记录
4. 输出格式化

用法：
    python3 claude_wrapper.py --task "你的任务描述" --workdir /path/to/project [--background] [--timeout 300]

或通过 OPENCLAW bash 调用：
    bash pty:true workdir:~/project command:"python3 scripts/claude_wrapper.py --task '你的任务'"
"""

import argparse
import subprocess
import sys
import os
import json
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Any

def find_claude_path() -> str:
    """查找claude可执行文件路径"""
    # 首先尝试在PATH中查找
    claude_path = shutil.which('claude')
    if claude_path:
        return claude_path

    # 尝试常见安装路径
    common_paths = [
        "C:\\Users\\Administrator\\AppData\\Roaming\\npm\\claude",
        "C:\\Program Files\\nodejs\\claude",
        "/usr/local/bin/claude",
        "/usr/bin/claude",
        "~/.npm-global/bin/claude",
    ]

    for path in common_paths:
        expanded = os.path.expanduser(path)
        if os.path.exists(expanded):
            return expanded

    raise FileNotFoundError("未找到claude命令。请确保Claude Code CLI已安装并添加到PATH")

def run_claude(task: str, workdir: Optional[str] = None, background: bool = False, timeout: int = 300) -> Dict[str, Any]:
    """
    运行 Claude Code 命令

    Args:
        task: 任务描述
        workdir: 工作目录（如为None则使用当前目录）
        background: 是否在后台运行
        timeout: 超时时间（秒）

    Returns:
        包含结果或错误信息的字典
    """
    # 查找claude路径
    try:
        claude_path = find_claude_path()
    except FileNotFoundError as e:
        return {"error": str(e)}

    # 验证工作目录
    if workdir:
        workdir_path = Path(workdir).expanduser().resolve()
        if not workdir_path.exists():
            return {"error": f"工作目录不存在: {workdir_path}"}
        if not workdir_path.is_dir():
            return {"error": f"工作目录不是目录: {workdir_path}"}
        # 检查是否为git仓库（Claude通常需要）
        git_dir = workdir_path / ".git"
        if not git_dir.exists():
            print(f"警告: 工作目录 {workdir_path} 不是git仓库，Claude Code可能无法正常工作")
    else:
        workdir_path = Path.cwd()

    # 构建命令
    cmd = [claude_path, task]

    try:
        # 如果在后台运行，使用subprocess.Popen
        if background:
            process = subprocess.Popen(
                cmd,
                cwd=str(workdir_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            return {
                "success": True,
                "background": True,
                "pid": process.pid,
                "workdir": str(workdir_path),
                "message": "Claude任务已在后台启动"
            }
        else:
            # 前台运行，带超时
            result = subprocess.run(
                cmd,
                cwd=str(workdir_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
                universal_newlines=True
            )

            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "workdir": str(workdir_path),
                "task": task
            }

    except subprocess.TimeoutExpired:
        return {"error": f"任务超时（{timeout}秒）", "task": task}
    except FileNotFoundError:
        return {"error": "未找到claude命令。请确保Claude Code CLI已安装并添加到PATH"}
    except Exception as e:
        return {"error": f"执行Claude命令时出错: {str(e)}", "task": task}

def create_temp_git_repo() -> str:
    """创建临时git仓库用于Claude任务"""
    temp_dir = tempfile.mkdtemp(prefix="claude_temp_")
    try:
        subprocess.run(["git", "init"], cwd=temp_dir, check=True, capture_output=True)
        # 创建初始提交
        readme_path = Path(temp_dir) / "README.md"
        readme_path.write_text("# Claude临时项目\n\n此目录为Claude Code任务临时创建。")
        subprocess.run(["git", "add", "."], cwd=temp_dir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=temp_dir, check=True, capture_output=True)
        return temp_dir
    except Exception as e:
        # 清理临时目录
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise RuntimeError(f"创建临时git仓库失败: {e}")

def main():
    parser = argparse.ArgumentParser(description="Claude Code 包装脚本")
    parser.add_argument("--task", "-t", required=True, help="Claude任务描述")
    parser.add_argument("--workdir", "-w", help="工作目录（默认：当前目录）")
    parser.add_argument("--background", "-b", action="store_true", help="在后台运行")
    parser.add_argument("--timeout", type=int, default=300, help="超时时间（秒，默认300）")
    parser.add_argument("--create-temp", action="store_true", help="创建临时git仓库")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    # 处理临时目录创建
    workdir = args.workdir
    if args.create_temp:
        try:
            temp_dir = create_temp_git_repo()
            workdir = temp_dir
            print(f"已创建临时git仓库: {temp_dir}", file=sys.stderr)
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)

    # 运行Claude任务
    result = run_claude(
        task=args.task,
        workdir=workdir,
        background=args.background,
        timeout=args.timeout
    )

    # 输出结果
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if "error" in result:
            print(f"错误: {result['error']}", file=sys.stderr)
            sys.exit(1)
        elif result.get("background"):
            print(f"✓ 任务已在后台启动 (PID: {result.get('pid')})")
            print(f"工作目录: {result.get('workdir')}")
        elif result.get("success"):
            if result.get("stdout"):
                print(result["stdout"])
            if result.get("stderr"):
                print(f"警告/错误输出:\n{result['stderr']}", file=sys.stderr)
        else:
            print(f"任务失败，退出码: {result.get('returncode')}", file=sys.stderr)
            if result.get("stderr"):
                print(f"错误输出:\n{result['stderr']}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()