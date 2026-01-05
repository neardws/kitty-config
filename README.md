# Kitty 终端配置

我的 Kitty 终端配置文件和使用指南。

## 文件说明

| 文件 | 说明 |
|------|------|
| `kitty.conf` | Kitty 主配置文件 |
| `kitty-keybindings-guide.md` | Kitty 快捷键配置指南 (macOS) |
| `kitty-install-themes-guide.md` | Kitty 安装与主题配置指南 |
| `kitten-ssh-tmux-guide.md` | kitten ssh + tmux 使用指南 |

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

- **主题**: Dracula
- **字体**: BerkeleyMapleMono 14pt
- **远程控制**: 已启用
- **布局**: splits, stack

## 快捷键概览

| 功能 | 快捷键 |
|------|--------|
| 分屏 (上/下/左/右) | `cmd+u` / `cmd+d` / `cmd+l` / `cmd+r` |
| 焦点切换 (左/下/上/右) | `cmd+j` / `cmd+m` / `cmd+i` / `cmd+k` |
| Tab 切换 | `cmd+1-9` 或 `cmd+shift+[` / `cmd+shift+]` |
| 新建/关闭 Tab | `cmd+t` / `cmd+w` |
| 关闭窗口 | `cmd+shift+w` |
| 调整窗口大小 | `cmd+shift+r` |

详细配置见 [kitty-keybindings-guide.md](kitty-keybindings-guide.md)

## 相关链接

- [Kitty 官网](https://sw.kovidgoyal.net/kitty/)
- [kitty-themes](https://github.com/dexpota/kitty-themes)
- [BerkeleyMono 字体](https://berkeleygraphics.com/typefaces/berkeley-mono/)
