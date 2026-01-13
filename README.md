# Kitty 终端配置

我的 Kitty 终端配置文件和使用指南。

## 文件说明

| 文件 | 说明 |
|------|------|
| `kitty.conf` | Kitty 主配置文件 |
| `tab_bar.py` | 自定义 Tab Bar Python 脚本（10色循环、Git分支、用户信息等） |
| `kitty-keybindings-guide.md` | Kitty 快捷键配置指南 (macOS) |
| `kitty-install-themes-guide.md` | Kitty 安装与主题配置指南 |
| `kitten-ssh-tmux-guide.md` | kitten ssh + tmux 使用指南 |
| `kitty-llm-reference.md` | Kitty LLM 配置参考 |

## 快速开始

### 1. 安装 Kitty

```bash
# macOS
brew install --cask kitty

# Linux
curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin
```

### 2. 使用配置

```bash
# 克隆仓库
git clone <repo-url> ~/kitty-config

# 复制配置文件
cp ~/kitty-config/kitty.conf ~/.config/kitty/
cp ~/kitty-config/tab_bar.py ~/.config/kitty/

# 安装主题
git clone --depth 1 https://github.com/dexpota/kitty-themes.git ~/.config/kitty/kitty-themes
ln -sf ./kitty-themes/themes/Dracula.conf ~/.config/kitty/theme.conf
```

### 3. 配置 SSH 别名

将 `kitten-ssh-tmux-guide.md` 中的别名添加到 `~/.zshrc`：

```bash
# kitten ssh 基础别名
alias s="kitten ssh"

# 服务器连接
alias ssh-vicp="kitten ssh neardws@11830bv51hw23.vicp.fun -p 20505"
alias st-vicp="kitten ssh neardws@11830bv51hw23.vicp.fun -p 20505 -t 'tmux new -As main'"
```

## 当前配置

- **主题**: Soft Pastel (Catppuccin Mocha 风格，柔和护眼)
- **字体**: BerkeleyMapleMono 14pt (支持 Nerd Font 图标)
- **远程控制**: 已启用
- **布局**: splits, stack
- **Tab Bar**: 自定义 Python 脚本 (见下方详细说明)

## Tab Bar 配置

使用 `tab_bar.py` 自定义 Tab Bar，支持以下功能：

### 布局

```
[用户名] [目录] [Git分支]    [1 Tab1] [2 Tab2] [3 Tab3]    [Session] [时间]
   左侧信息区                      中间 Tab 列表                 右侧信息区
```

### 功能特性

| 区域 | 显示内容 | 图标 |
|------|----------|------|
| 左侧 | 用户名、当前目录、Git 分支 | `` `` `` |
| 中间 | Tab 列表（序号 + 程序名） | 圆角边框 |
| 右侧 | Session 名、当前时间 | `` `` |

### 颜色系统

- **10 色循环色板**: 每个 Tab 根据位置显示不同颜色
- **激活/未激活对比**: 激活 Tab 明亮鲜艳，未激活 Tab 暗淡
- 色板: Mauve → Pink → Teal → Green → Peach → Yellow → Red → Blue → Lavender → Flamingo

### 配置要点

```conf
# kitty.conf
tab_bar_style custom              # 使用自定义 Python 脚本
tab_bar_edge bottom               # Tab Bar 在底部
tab_bar_min_tabs 1                # 始终显示
tab_bar_margin_height 5.0 0.0     # 上边距
tab_bar_background #1e1e2e        # 背景色
```

### 部署方式

```bash
# 复制到 Kitty 配置目录
cp tab_bar.py ~/.config/kitty/
cp kitty.conf ~/.config/kitty/

# 重载配置
# 方法1: 快捷键 ctrl+shift+f5
# 方法2: 重启 Kitty
```

### 依赖

- **字体**: 需要 Nerd Font 字体支持图标显示 (推荐 BerkeleyMapleMono 或 Maple Mono NF CN)
- **主题**: 需要 `~/.config/kitty/theme.conf` 定义 color0-19

## 快捷键概览

| 功能 | 快捷键 |
|------|--------|
| 水平分屏 / 垂直分屏 | `cmd+d` / `cmd+r` |
| 移动窗口 | `cmd+u`(上) / `cmd+l`(左) / `cmd+shift+方向键` |
| 焦点切换 (左/下/上/右) | `cmd+j` / `cmd+m` / `cmd+i` / `cmd+k` |
| Tab 切换 | `cmd+1-9` 或 `cmd+shift+[` / `cmd+shift+]` |
| 新建 Tab / 关闭 Tab | `cmd+t` / `cmd+shift+w` |
| 关闭窗口 | `cmd+w` |
| 调整窗口大小 | `cmd+shift+r` |

详细配置见 [kitty-keybindings-guide.md](kitty-keybindings-guide.md)

## 相关链接

- [Kitty 官网](https://sw.kovidgoyal.net/kitty/)
- [kitty-themes](https://github.com/dexpota/kitty-themes)
- [BerkeleyMono 字体](https://berkeleygraphics.com/typefaces/berkeley-mono/)
