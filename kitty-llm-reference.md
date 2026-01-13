# Kitty 终端配置参考 (LLM Reference)

> 本文档为 LLM 提供 Kitty 终端配置的结构化参考信息。

## 1. 当前配置概览

| 配置项 | 值 |
|--------|-----|
| 主题 | `include ./theme.conf` (软链接方式) |
| 远程控制 | `allow_remote_control yes` |
| 窗口内边距 | 4px |
| 终端类型 | `xterm-kitty` |
| 字体 | BerkeleyMapleMono 14pt |
| 布局 | splits, stack |
| 鼠标隐藏 | 3秒无操作后隐藏 |

## 2. 快捷键速查 (macOS)

### 分屏
| 快捷键 | 功能 |
|--------|------|
| `cmd+d` | 水平分屏（新窗口在下方） |
| `cmd+r` | 垂直分屏（新窗口在右侧） |

### Tab 管理
| 快捷键 | 功能 |
|--------|------|
| `cmd+t` | 新建 Tab |
| `cmd+w` | 关闭当前窗口 |
| `cmd+shift+w` | 关闭当前 Tab |
| `cmd+shift+[` | 上一个 Tab |
| `cmd+shift+]` | 下一个 Tab |
| `cmd+1` ~ `cmd+9` | 切换到第 N 个 Tab |

### 焦点切换
| 快捷键 | 功能 |
|--------|------|
| `cmd+[` | 上一个窗口 |
| `cmd+]` | 下一个窗口 |
| `cmd+j` | 焦点向左 |
| `cmd+k` | 焦点向右 |
| `cmd+i` | 焦点向上 |
| `cmd+m` | 焦点向下 |

### 窗口移动
| 快捷键 | 功能 |
|--------|------|
| `cmd+shift+up/down/left/right` | 移动窗口到对应方向 |
| `cmd+shift+r` | 进入窗口调整模式 |

### 其他
| 快捷键 | 功能 |
|--------|------|
| `cmd+c` / `cmd+v` | 复制 / 粘贴 |
| `cmd+equal` / `cmd+minus` | 放大 / 缩小字体 |
| `cmd+0` | 重置字体大小 |
| `cmd+enter` | 切换全屏 |
| `cmd+n` | 新建 OS 窗口 |

## 3. SSH + tmux 集成

### 核心命令
```bash
kitten ssh user@host -t "tmux new -As session_name"
```
- `-A`: 会话存在则 attach，不存在则创建
- `-s`: 指定会话名称

### 服务器别名 (~/.zshrc)

| 别名 | 命令 | 说明 |
|------|------|------|
| `s` | `kitten ssh` | 基础 SSH |
| `ssh-vicp` | `kitten ssh neardws@11830bv51hw23.vicp.fun -p 20505` | vicp 服务器 |
| `st-vicp` | 同上 + `-t 'tmux new -As main'` | vicp + tmux |
| `ssh-frp` | `kitten ssh neardws@frp-era.com -p 61537` | frp 服务器 |
| `st-frp` | 同上 + `-t 'tmux new -As main'` | frp + tmux |
| `ssh-local` | `kitten ssh neardws@192.168.31.211` | 局域网服务器 |
| `st-local` | 同上 + `-t 'tmux new -As main'` | local + tmux |

### 指定会话函数
```bash
st-vicp-s dev   # 连接 vicp，进入 dev 会话
st-frp-s work   # 连接 frp，进入 work 会话
st-local-s main # 连接 local，进入 main 会话
```

### 远程 tmux 配置 (~/.tmux.conf)
```conf
set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",xterm-kitty:Tc"
set -g mouse on
set -gq allow-passthrough on  # 支持 kitty 图形协议 (tmux 3.3+)
```

### tmux 常用操作
| 操作 | 说明 |
|------|------|
| `Ctrl+b d` | 分离会话（保持运行） |
| `tmux ls` | 列出会话 |
| `tmux attach -t name` | 重新附加 |

## 4. 主题管理

### 安装主题仓库
```bash
git clone --depth 1 https://github.com/dexpota/kitty-themes.git ~/.config/kitty/kitty-themes
```

### 切换主题
```bash
cd ~/.config/kitty
ln -sf ./kitty-themes/themes/Dracula.conf ~/.config/kitty/theme.conf
# 按 Ctrl+Shift+F5 重新加载
```

### 实时预览
```bash
kitty @ set-colors -a "~/.config/kitty/kitty-themes/themes/Dracula.conf"
```

### 热门主题
| 主题 | 风格 |
|------|------|
| Dracula | 暗色，紫色调 |
| gruvbox_dark | 暗色，复古 |
| Nord | 暗色，北欧风 |
| OneDark | 暗色，Atom 风格 |
| Solarized_Dark | 暗色，经典 |
| Monokai | 暗色，编程风格 |

## 5. 常用命令速查

| 命令 | 用途 |
|------|------|
| `kitten ssh host -t "tmux new -As x"` | SSH 连接并进入 tmux |
| `kitten icat image.png` | 在终端显示图片 |
| `kitten icat --passthrough tmux image.png` | 在 tmux 中显示图片 |
| `kitty +list-fonts` | 列出可用字体 |
| `kitty @ set-colors -a "theme.conf"` | 实时预览主题 |
| `Ctrl+Shift+F5` | 重新加载配置 |

## 6. 配置文件位置

| 文件 | 路径 |
|------|------|
| 主配置 | `~/.config/kitty/kitty.conf` |
| 主题配置 | `~/.config/kitty/theme.conf` |
| SSH 配置 | `~/.config/kitty/ssh.conf` |
| 主题仓库 | `~/.config/kitty/kitty-themes/` |
