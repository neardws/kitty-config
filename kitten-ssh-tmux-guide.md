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

## 7. 我的服务器配置

### 别名配置 (~/.zshrc)

```bash
# kitten ssh 基础别名
alias s="kitten ssh"

# 服务器 1 - vicp
alias ssh-vicp="kitten ssh neardws@11830bv51hw23.vicp.fun -p 20505"
alias st-vicp="kitten ssh neardws@11830bv51hw23.vicp.fun -p 20505 -t 'tmux new -As main'"

# 服务器 2 - frp
alias ssh-frp="kitten ssh neardws@frp-era.com -p 61537"
alias st-frp="kitten ssh neardws@frp-era.com -p 61537 -t 'tmux new -As main'"

# 服务器 3 - local (局域网)
alias ssh-local="kitten ssh neardws@192.168.31.211"
alias st-local="kitten ssh neardws@192.168.31.211 -t 'tmux new -As main'"

# 指定会话名的函数
st-vicp-s() { kitten ssh neardws@11830bv51hw23.vicp.fun -p 20505 -t "tmux new -As ${1:-main}"; }
st-frp-s() { kitten ssh neardws@frp-era.com -p 61537 -t "tmux new -As ${1:-main}"; }
st-local-s() { kitten ssh neardws@192.168.31.211 -t "tmux new -As ${1:-main}"; }
```

### 使用方式

| 命令 | 说明 |
|------|------|
| `ssh-vicp` | 普通连接 vicp 服务器 |
| `st-vicp` | 连接 vicp + 进入 main 会话 |
| `st-vicp-s dev` | 连接 vicp + 进入 dev 会话 |
| `st-vicp-s work` | 连接 vicp + 进入 work 会话 |
| `ssh-frp` | 普通连接 frp 服务器 |
| `st-frp` | 连接 frp + 进入 main 会话 |
| `st-frp-s dev` | 连接 frp + 进入 dev 会话 |
| `ssh-local` | 普通连接 local 局域网服务器 |
| `st-local` | 连接 local + 进入 main 会话 |
| `st-local-s dev` | 连接 local + 进入 dev 会话 |

## 命令速查表

| 命令 | 用途 |
|------|------|
| `kitten ssh host -t "tmux new -As x"` | 连接并创建/附加会话 |
| `Ctrl+b d` | 分离 tmux（保持运行） |
| `kitten ssh host -t "tmux attach"` | 重新附加 |
| `kitten ssh host -t "tmux ls"` | 列出远程会话 |

## 在 Kitty 中显示图片

```bash
# 显示本地图片
kitten icat image.png

# 指定宽度
kitten icat --width 50 image.jpg

# 在 tmux 中显示（需要 tmux 3.3+ 且配置 allow-passthrough）
kitten icat --passthrough tmux image.png

# 创建别名
alias icat="kitten icat"
```
