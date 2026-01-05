# Kitty 终端安装与主题配置指南

## 1. 安装 Kitty

### macOS

```bash
# 使用 Homebrew (推荐)
brew install --cask kitty

# 或者使用 curl 安装
curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin
```

### Linux

```bash
# 使用官方安装脚本 (推荐)
curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin

# Ubuntu/Debian
sudo apt install kitty

# Arch Linux
sudo pacman -S kitty

# Fedora
sudo dnf install kitty
```

安装后，`kitten` 命令会自动可用（它是 kitty 的内置工具）。

## 2. 配置 kitty-themes

### 方法一：克隆整个仓库（推荐）

```bash
# 克隆主题仓库到 kitty 配置目录
git clone --depth 1 https://github.com/dexpota/kitty-themes.git ~/.config/kitty/kitty-themes
```

### 方法二：下载单个主题

```bash
# 下载指定主题
THEME=https://raw.githubusercontent.com/dexpota/kitty-themes/master/themes/Dracula.conf
curl -o ~/.config/kitty/kitty-themes/themes/Dracula.conf --create-dirs "$THEME"
```

### 方法三：使用 Conda

```bash
conda install -c conda-forge kitty-themes
```

## 3. 应用主题

### 步骤 1：创建主题软链接

```bash
cd ~/.config/kitty

# 选择一个主题创建软链接（以 Dracula 为例）
ln -sf ./kitty-themes/themes/Dracula.conf ~/.config/kitty/theme.conf

# 其他热门主题示例：
# ln -sf ./kitty-themes/themes/gruvbox_dark.conf ~/.config/kitty/theme.conf
# ln -sf ./kitty-themes/themes/Solarized_Dark.conf ~/.config/kitty/theme.conf
# ln -sf ./kitty-themes/themes/Nord.conf ~/.config/kitty/theme.conf
# ln -sf ./kitty-themes/themes/OneDark.conf ~/.config/kitty/theme.conf
```

### 步骤 2：在 kitty.conf 中引入主题

编辑 `~/.config/kitty/kitty.conf`，添加：

```conf
include ./theme.conf
```

### 步骤 3：重新加载配置

```bash
# 方法一：使用快捷键
# 在 kitty 中按 Ctrl+Shift+F5

# 方法二：重新启动 kitty
```

## 4. 预览和切换主题

### 实时预览（需要启用 remote control）

首先在 `~/.config/kitty/kitty.conf` 中启用 remote control：

```conf
allow_remote_control yes
```

然后可以实时预览主题：

```bash
# 预览指定主题
kitty @ set-colors -a "~/.config/kitty/kitty-themes/themes/Dracula.conf"

# 预览其他主题
kitty @ set-colors -a "~/.config/kitty/kitty-themes/themes/gruvbox_dark.conf"
```

### 启动新实例预览

```bash
# 在新窗口中预览主题（不影响当前窗口）
kitty -o include="~/.config/kitty/kitty-themes/themes/Dracula.conf"
```

### 列出所有可用主题

```bash
ls ~/.config/kitty/kitty-themes/themes/
```

## 5. 快速切换主题脚本

创建 `~/bin/kitty-theme`：

```bash
#!/bin/bash
THEME_DIR=~/.config/kitty/kitty-themes/themes

if [ -z "$1" ]; then
    echo "可用主题："
    ls "$THEME_DIR" | sed 's/.conf$//'
    exit 0
fi

THEME="$THEME_DIR/$1.conf"
if [ -f "$THEME" ]; then
    ln -sf "$THEME" ~/.config/kitty/theme.conf
    echo "已切换到主题: $1"
    echo "请按 Ctrl+Shift+F5 或重启 kitty 生效"
else
    echo "主题不存在: $1"
    echo "使用 'kitty-theme' 查看可用主题"
fi
```

```bash
chmod +x ~/bin/kitty-theme

# 使用方式
kitty-theme              # 列出所有主题
kitty-theme Dracula      # 切换到 Dracula 主题
kitty-theme gruvbox_dark # 切换到 gruvbox_dark 主题
```

## 6. 热门主题推荐

| 主题名 | 风格 |
|--------|------|
| `Dracula` | 暗色，紫色调 |
| `gruvbox_dark` | 暗色，复古 |
| `gruvbox_light` | 亮色，复古 |
| `Nord` | 暗色，北欧风 |
| `OneDark` | 暗色，Atom 风格 |
| `Solarized_Dark` | 暗色，经典 |
| `Solarized_Light` | 亮色，经典 |
| `Tomorrow_Night` | 暗色，柔和 |
| `Monokai` | 暗色，经典编程风格 |
| `ayu` | 暗色，现代 |
| `ayu_light` | 亮色，现代 |

## 7. 字体配置

在 `~/.config/kitty/kitty.conf` 中配置字体：

```conf
# 字体设置
font_family BerkeleyMapleMono
font_size 14.0

# 可选：设置粗体/斜体字体
# bold_font        BerkeleyMapleMono Bold
# italic_font      BerkeleyMapleMono Italic
# bold_italic_font BerkeleyMapleMono Bold Italic
```

### 查看可用字体

```bash
# 列出系统中所有可用的等宽字体
kitty +list-fonts

# 搜索特定字体
kitty +list-fonts | grep -i "berkeley"
```

### 推荐编程字体

| 字体名 | 特点 |
|--------|------|
| `BerkeleyMapleMono` | 现代，清晰，支持连字 |
| `JetBrains Mono` | JetBrains 出品，免费 |
| `Fira Code` | 支持连字，开源 |
| `SF Mono` | macOS 系统字体 |
| `Cascadia Code` | 微软出品，支持连字 |

## 命令速查表

| 命令 | 用途 |
|------|------|
| `git clone --depth 1 https://github.com/dexpota/kitty-themes.git ~/.config/kitty/kitty-themes` | 克隆主题仓库 |
| `ln -sf ./kitty-themes/themes/主题名.conf ~/.config/kitty/theme.conf` | 切换主题 |
| `kitty @ set-colors -a "~/.config/kitty/kitty-themes/themes/主题名.conf"` | 实时预览 |
| `ls ~/.config/kitty/kitty-themes/themes/` | 列出所有主题 |
| `Ctrl+Shift+F5` | 重新加载配置 |
