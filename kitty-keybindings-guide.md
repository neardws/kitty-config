# Kitty 快捷键配置指南 (macOS)

## 布局设置

使用分屏功能需要在 `kitty.conf` 中启用 `splits` 布局：

```conf
enabled_layouts splits,stack
```

## 快捷键速查表

### 分屏

| 快捷键 | 功能 | 命令 |
|--------|------|------|
| `cmd+d` | 水平分屏（新窗口在下方） | `launch --location=hsplit --cwd=current` |
| `cmd+r` | 垂直分屏（新窗口在右侧） | `launch --location=vsplit --cwd=current` |

### 移动窗口位置

| 快捷键 | 功能 | 命令 |
|--------|------|------|
| `cmd+u` | 移动窗口到上方 | `move_window up` |
| `cmd+l` | 移动窗口到左侧 | `move_window left` |
| `cmd+shift+up` | 移动窗口到上方 | `move_window up` |
| `cmd+shift+down` | 移动窗口到下方 | `move_window down` |
| `cmd+shift+left` | 移动窗口到左侧 | `move_window left` |
| `cmd+shift+right` | 移动窗口到右侧 | `move_window right` |

### Tab 管理

| 快捷键 | 功能 | 命令 |
|--------|------|------|
| `cmd+t` | 新建 Tab | `new_tab` |
| `cmd+w` | 关闭当前分屏窗口 | `close_window` |
| `cmd+shift+[` | 上一个 Tab | `previous_tab` |
| `cmd+shift+]` | 下一个 Tab | `next_tab` |
| `cmd+1` ~ `cmd+9` | 切换到第 1-9 个 Tab | `goto_tab N` |

### 焦点切换

| 快捷键 | 功能 | 命令 |
|--------|------|------|
| `cmd+[` | 上一个窗口 | `previous_window` |
| `cmd+]` | 下一个窗口 | `next_window` |
| `cmd+j` | 焦点向左 | `neighboring_window left` |
| `cmd+m` | 焦点向下 | `neighboring_window down` |
| `cmd+i` | 焦点向上 | `neighboring_window up` |
| `cmd+k` | 焦点向右 | `neighboring_window right` |

### 窗口管理

| 快捷键 | 功能 | 命令 |
|--------|------|------|
| `cmd+shift+w` | 关闭当前 Tab | `close_tab` |
| `cmd+shift+r` | 进入窗口调整模式 | `start_resizing_window` |

### 其他常用

| 快捷键 | 功能 | 命令 |
|--------|------|------|
| `cmd+c` | 复制 | `copy_to_clipboard` |
| `cmd+v` | 粘贴 | `paste_from_clipboard` |
| `cmd+equal` | 放大字体 | `change_font_size all +1.0` |
| `cmd+minus` | 缩小字体 | `change_font_size all -1.0` |
| `cmd+0` | 重置字体大小 | `change_font_size all 0` |
| `cmd+enter` | 切换全屏 | `toggle_fullscreen` |
| `cmd+n` | 新建 OS 窗口 | `new_os_window` |

## 完整配置代码

```conf
# ===== 布局设置 =====
enabled_layouts splits,stack


# ===== 快捷键配置 (macOS) =====

# --- 分屏 ---
# cmd+d: 水平分屏（上下，新窗口在下方）
# cmd+r: 垂直分屏（左右，新窗口在右侧）
map cmd+d launch --location=hsplit --cwd=current
map cmd+r launch --location=vsplit --cwd=current

# --- 移动窗口位置 ---
map cmd+u move_window up
map cmd+l move_window left
map cmd+shift+up move_window up
map cmd+shift+down move_window down
map cmd+shift+left move_window left
map cmd+shift+right move_window right

# --- Tab 管理 ---
map cmd+t new_tab
map cmd+w close_window
map cmd+shift+[ previous_tab
map cmd+shift+] next_tab
map cmd+1 goto_tab 1
map cmd+2 goto_tab 2
map cmd+3 goto_tab 3
map cmd+4 goto_tab 4
map cmd+5 goto_tab 5
map cmd+6 goto_tab 6
map cmd+7 goto_tab 7
map cmd+8 goto_tab 8
map cmd+9 goto_tab 9

# --- 焦点切换 ---
map cmd+[ previous_window
map cmd+] next_window
map cmd+j neighboring_window left
map cmd+m neighboring_window down
map cmd+i neighboring_window up
map cmd+k neighboring_window right

# --- 窗口管理 ---
map cmd+shift+w close_tab
map cmd+shift+r start_resizing_window

# --- 其他常用 ---
map cmd+c copy_to_clipboard
map cmd+v paste_from_clipboard
map cmd+equal change_font_size all +1.0
map cmd+minus change_font_size all -1.0
map cmd+0 change_font_size all 0
map cmd+enter toggle_fullscreen
map cmd+n new_os_window
```

## 自定义快捷键

### 基本语法

```conf
map 快捷键 动作
```

### 修饰键

| 修饰键 | macOS | 说明 |
|--------|-------|------|
| `cmd` | Command (⌘) | macOS 主修饰键 |
| `ctrl` | Control (⌃) | |
| `alt` / `opt` | Option (⌥) | |
| `shift` | Shift (⇧) | |

### 组合示例

```conf
map cmd+shift+t new_tab_with_cwd
map ctrl+alt+enter new_window
map cmd+alt+l next_layout
```

### 取消默认快捷键

```conf
map ctrl+shift+t no_op
```

## 相关链接

- [Kitty Actions 文档](https://sw.kovidgoyal.net/kitty/actions/)
- [Kitty Launch 命令](https://sw.kovidgoyal.net/kitty/launch/)
- [Kitty Layouts](https://sw.kovidgoyal.net/kitty/layouts/)
