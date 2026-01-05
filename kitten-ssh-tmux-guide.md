# kitten ssh + tmux 组合使用指南

## 1. 最简单的方式 - 直接连接并启动 tmux

```bash
kitten ssh user@host -t "tmux new -As main"
```

- `-A` 如果会话存在则 attach，不存在则创建
- `-s main` 指定会话名称

## 2. 创建 shell 别名（推荐）

在 `~/.zshrc` 或 `~/.bashrc` 添加：

```bash
# 普通 SSH
alias s="kitten ssh"

# SSH + tmux 自动附加
alias st="kitten ssh -t -- tmux new -As main"

# 指定服务器
alias dev="kitten ssh dev-server -t 'tmux new -As dev'"
alias prod="kitten ssh prod-server -t 'tmux new -As prod'"
```

使用：

```bash
st user@host        # 连接并进入 tmux
dev                 # 快速连接开发服务器
```

## 3. 配置 kitty 的 ssh.conf

编辑 `~/.config/kitty/ssh.conf`：

```conf
# 全局：自动同步 tmux 配置
copy .tmux.conf

# 针对特定服务器自动启动 tmux
hostname dev-server
    copy .tmux.conf .vimrc
    
hostname prod-*
    copy .tmux.conf
```

## 4. 远程 tmux 配置优化

在远程服务器的 `~/.tmux.conf` 添加：

```conf
# 支持 kitty 的真彩色
set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",xterm-kitty:Tc"

# 启用鼠标
set -g mouse on

# 支持 kitty 图形协议（需要 tmux 3.3+）
set -gq allow-passthrough on
```

## 5. 完整工作流示例

```bash
# 首次连接
kitten ssh dev-server -t "tmux new -As work"

# 在 tmux 中工作...
# 按 Ctrl+b d 分离（detach）

# 网络断开或关闭终端后，重新连接
kitten ssh dev-server -t "tmux attach -t work"
# 会话完整保留！
```

## 6. 高级：一键脚本

创建 `~/bin/sshtmux`：

```bash
#!/bin/bash
HOST=$1
SESSION=${2:-main}
kitten ssh "$HOST" -t "tmux new -As $SESSION || tmux attach -t $SESSION"
```

```bash
chmod +x ~/bin/sshtmux
sshtmux myserver        # 使用默认会话名 main
sshtmux myserver dev    # 使用会话名 dev
```

## 命令速查表

| 命令 | 用途 |
|------|------|
| `kitten ssh host -t "tmux new -As x"` | 连接并创建/附加会话 |
| `Ctrl+b d` | 分离 tmux（保持运行） |
| `kitten ssh host -t "tmux attach"` | 重新附加 |
| `kitten ssh host -t "tmux ls"` | 列出远程会话 |
