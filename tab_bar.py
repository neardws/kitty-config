from enum import Enum
from typing import Callable
from kitty.fast_data_types import Screen, add_timer, get_boss, get_options
from kitty.tab_bar import (
    DrawData, TabBarData, ExtraData, TabAccessor, as_rgb
)
from kitty.utils import color_as_int
import os
import datetime
import subprocess
from pathlib import Path

opts = get_options()

BG = as_rgb(color_as_int(opts.color19))
FG = as_rgb(color_as_int(opts.color7))
COLOR_1 = as_rgb(color_as_int(opts.color3))
COLOR_2 = as_rgb(color_as_int(opts.color5))
COLOR_3 = as_rgb(color_as_int(opts.color4))
COLOR_4 = as_rgb(color_as_int(opts.color4))

# 未激活 Tab 颜色（暗淡，低饱和度）
TAB_COLORS = [
    as_rgb(0x7c6f8a),  # 1. Dim Mauve
    as_rgb(0x9a7a8e),  # 2. Dim Pink
    as_rgb(0x5a8a82),  # 3. Dim Teal
    as_rgb(0x6a8a68),  # 4. Dim Green
    as_rgb(0x9a7a5a),  # 5. Dim Peach
    as_rgb(0x9a8a6a),  # 6. Dim Yellow
    as_rgb(0x9a5a6a),  # 7. Dim Red
    as_rgb(0x5a7a9a),  # 8. Dim Blue
    as_rgb(0x7a7a9a),  # 9. Dim Lavender
    as_rgb(0x9a7a7a),  # 10. Dim Flamingo
]

# 激活 Tab 颜色（明亮，高饱和度）
TAB_COLORS_ACTIVE = [
    as_rgb(0xcba6f7),  # 1. Bright Mauve
    as_rgb(0xf5c2e7),  # 2. Bright Pink
    as_rgb(0x94e2d5),  # 3. Bright Teal
    as_rgb(0xa6e3a1),  # 4. Bright Green
    as_rgb(0xfab387),  # 5. Bright Peach
    as_rgb(0xf9e2af),  # 6. Bright Yellow
    as_rgb(0xf38ba8),  # 7. Bright Red
    as_rgb(0x89b4fa),  # 8. Bright Blue
    as_rgb(0xb4befe),  # 9. Bright Lavender
    as_rgb(0xf2cdcd),  # 10. Bright Flamingo
]

REFRESH_TIME = 15
MAX_LENGTH_PATH = 3

# Nerd Font 图标（已验证 BerkeleyMapleMono 支持）
folder_icon = "\uf07b "    # U+F07B folder
time_icon = "\uf017 "      # U+F017 clock
session_icon = "\ue795 "   # U+E795 terminal
git_icon = "\ue725 "       # U+E725 git-branch
user_icon = "\uf007 "      # U+F007 user

# 圆角边框（Powerline 字符）
ROUND_LEFT = "\ue0b6"      # U+E0B6 
ROUND_RIGHT = "\ue0b4"     # U+E0B4 

class Cell:
    def __init__(
        self,
        icon: str,
        text_fn: Callable[[int, TabBarData], str | None],
        tab: TabBarData = None,
        bg: str = BG,
        fg: str = FG,
        color: int = COLOR_1,
        separator: str = "",
        border: tuple[str, str] = ("",""),
    ) -> None:
        
        self.tab: TabBarData = tab
        self.fg: str = fg
        self.bg: str = bg
        self.color: int = color
        self.icon: str = icon
        self.text_fn: Callable[[int, TabBarData], str | None] = text_fn
        self.border: tuple[str, str] = border
        self.separator: str = separator
        self.text_length_overhead = len(self.border[0] + self.border[1] + self.separator + self.icon) + 1
        
    def draw(self, screen: Screen, max_size: int) -> None:
        text = self.text_fn(max_size - self.text_length_overhead, self.tab)
        
        if text is None:
            return

        screen.cursor.dim = False
        screen.cursor.bold = False
        screen.cursor.italic = False
        
        screen.cursor.bg = 0
        screen.cursor.fg = self.color
        screen.draw(self.border[0])

        screen.cursor.bg = self.color
        screen.cursor.fg = self.bg
        screen.cursor.bold = True
        screen.draw(self.icon)
        screen.cursor.bold = False
        
        if text == "":
            screen.cursor.bg = 0
            screen.cursor.fg = self.color
            screen.draw(self.border[1])
        else:
            screen.cursor.bg = self.bg
            screen.cursor.fg = self.color
            screen.draw(self.separator)
            
            # 文字也使用 tab 对应的颜色
            screen.cursor.fg = self.color
            screen.draw(f" {text}")
            
            screen.cursor.fg = self.bg
            screen.cursor.bg = 0
            screen.draw(self.border[1])
            
    def length(self, max_size: int) -> int:
        text = self.text_fn(max_size - self.text_length_overhead, self.tab)
        
        if text is None:
            return 0
        elif text ==  "":
            return len(self.icon + self.border[0] + self.border[1])
        else:
            return len(text) + self.text_length_overhead

def get_wd(max_size: int, tab: TabBarData):
    accessor = TabAccessor(tab.tab_id)

    wd = Path(accessor.active_wd)
    home = Path(os.getenv('HOME'))

    if wd.is_relative_to(home):
        wd = wd.relative_to(home)

        if wd == home:
            wd = Path("~")
        else:
            wd = Path("~") / wd
    
    parts = list(wd.parts)
    compressed = False
    if len(parts) > MAX_LENGTH_PATH:
        compressed = True
        parts = [parts[0], ".."] + parts[-MAX_LENGTH_PATH:]

    parts_cnt = 1 + compressed
    while parts_cnt != len(parts):
        wd = "/".join(parts[0:1+compressed] + parts[parts_cnt:])
        if len(wd) <= max_size:
            return wd
        parts_cnt += 1
    
    if len(parts[-1]) <= max_size:
        return parts[-1]

    return None

def get_time(max_size: int, tab: TabBarData) -> str | None:
    if max_size < 5:
        return None
    else:
        return datetime.datetime.now().strftime("%H:%M")

def get_tab(max_size: int, tab: TabBarData) -> str | None:
    accessor = TabAccessor(tab.tab_id)

    # 如果标题以 # 开头，使用自定义标题（去掉 # 前缀）
    # 否则使用当前运行的程序名
    if tab.title and len(tab.title) > 1 and tab.title[0] == "#":
        text = tab.title[1:]
    else:
        text = str(accessor.active_exe)
    
    if max_size <= len(text):
        return ""
    else:
        return text

def get_session(max_size: int, tab: TabBarData) -> str | None:
    text = tab.session_name
    if text == "":
        text = "none"
    if len(text) <= max_size:
        return text
    elif max_size >= 3:
        return text[:3]
    else:
        return None

def get_git_branch(max_size: int, tab: TabBarData) -> str | None:
    """获取当前目录的 Git 分支名"""
    if max_size < 3:
        return None
    try:
        accessor = TabAccessor(tab.tab_id)
        wd = accessor.active_wd
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=wd,
            capture_output=True,
            text=True,
            timeout=1
        )
        if result.returncode == 0:
            branch = result.stdout.strip()
            if len(branch) <= max_size:
                return branch
            elif max_size >= 6:
                return branch[:max_size-2] + ".."
            return ""
    except:
        pass
    return None

def get_user(max_size: int, tab: TabBarData) -> str | None:
    """获取当前用户名"""
    user = os.getenv('USER', '')
    if len(user) <= max_size:
        return user
    return None

def get_tab_cell(tab: TabBarData, index: int) -> Cell:
    # 根据 tab 位置选择颜色（循环色板）
    color_index = index % len(TAB_COLORS)
    if tab.is_active:
        color = TAB_COLORS_ACTIVE[color_index]
    else:
        color = TAB_COLORS[color_index]
    # 使用序号（1, 2, 3...）和圆角边框
    return Cell(str(index + 1), get_tab, tab, color=color, border=(ROUND_LEFT, ROUND_RIGHT))


def redraw_tab_bar(_):
    tm = get_boss().active_tab_manager
    if tm is not None:
        tm.mark_tab_bar_dirty()

timer_id = None

center: list[Cell] = []
active_index = 1

class CenterStrategy(Enum):
    EXPAND_ALL = 0
    EXPAND_ACTIVE = 1
    NO_EXPAND = 2
    SHOW_ACTIVE = 3
    SHOW_ACTIVE_NO_EXPAND = 4

def center_strategy(screen: Screen) -> tuple[CenterStrategy, int]:
    n_cells = len(center)
    
    length = n_cells - 1 + sum(map(lambda x: x.length(screen.columns), center))
    if length < screen.columns:
        return CenterStrategy.EXPAND_ALL, length

    length = n_cells - 1
    for index, cell in enumerate(center):
        if index == active_index:
            length += cell.length(screen.columns)
        else:
            length += cell.length(0) 
    if length < screen.columns:
        return CenterStrategy.EXPAND_ACTIVE, length

    length = n_cells - 1+ sum(map(lambda x: x.length(0), center))
    if length < screen.columns:
        return CenterStrategy.NO_EXPAND, length

    length = center[active_index].length(screen.columns)
    if length < screen.columns:
        return CenterStrategy.SHOW_ACTIVE, length

    return CenterStrategy.SHOW_ACTIVE_NO_EXPAND, center[active_index].length(0)

def draw_center(screen: Screen, strategy: CenterStrategy):

    match strategy:
        case CenterStrategy.EXPAND_ALL:
            for idx, cell in enumerate(center):
                if idx != 0:
                    screen.draw(" ")
                cell.draw(screen, screen.columns)

        case CenterStrategy.EXPAND_ACTIVE:
            for idx, cell in enumerate(center):
                if idx != 0:
                    screen.draw(" ")
                cell.draw(screen, screen.columns * (idx == active_index))
        case CenterStrategy.NO_EXPAND:
            for idx, cell in enumerate(center):
                if idx != 0:
                    screen.draw(" ")
                cell.draw(screen, 0)
        case CenterStrategy.SHOW_ACTIVE:
            center[active_index].draw(screen, screen.columns)
        case CenterStrategy.SHOW_ACTIVE_NO_EXPAND:
            center[active_index].draw(screen, 0)

def draw_left(screen: Screen, max_length: int):
    tab = center[active_index].tab
    
    # 用户图标
    user_cell = Cell(user_icon, get_user, tab, color=COLOR_2, border=(ROUND_LEFT, ROUND_RIGHT))
    user_len = user_cell.length(max_length)
    
    # 文件夹图标 + 路径
    remaining = max_length - user_len - 1
    folder_cell = Cell(folder_icon, get_wd, tab, color=COLOR_4, border=(ROUND_LEFT, ROUND_RIGHT))
    folder_len = folder_cell.length(remaining)
    
    # Git 分支图标
    remaining2 = remaining - folder_len - 1
    git_cell = Cell(git_icon, get_git_branch, tab, color=COLOR_1, border=(ROUND_LEFT, ROUND_RIGHT))
    
    # 绘制
    user_cell.draw(screen, max_length)
    if folder_len > 0:
        screen.draw(" ")
        folder_cell.draw(screen, remaining)
    if remaining2 > 5:
        screen.draw(" ")
        git_cell.draw(screen, remaining2)

def draw_right(screen: Screen):
    max_size = screen.columns - screen.cursor.x
    tab = center[active_index].tab
    
    # 圆角样式
    time_cell = Cell(time_icon, get_time, color=COLOR_3, border=(ROUND_LEFT, ROUND_RIGHT))
    session_cell = Cell(session_icon, get_session, tab, color=COLOR_2, border=(ROUND_LEFT, ROUND_RIGHT))

    total_length = time_cell.length(max_size)
    session_length = session_cell.length(max_size - total_length - 1)

    if session_length != 0:
        total_length += 1 + session_length

    offset_length = max_size - total_length
    screen.draw(" " * offset_length)

    if session_length != 0:
        session_cell.draw(screen, session_length)
        screen.draw(" ")

    time_cell.draw(screen, max_size)

def draw_tab(
    draw_data: DrawData,
    screen: Screen,
    tab: TabBarData,
    before: int,
    max_title_length: int,
    index: int,
    is_last: bool,
    extra_data: ExtraData,
) -> int:
    global center
    global timer_id
    global active_index

    if timer_id is None:
        timer_id = add_timer(redraw_tab_bar, REFRESH_TIME, True)
    if tab.is_active:
        active_index = index - 1

    center.append(get_tab_cell(tab, index - 1))

    # Draw everything on the last tab
    if is_last:
        strategy, length = center_strategy(screen)
        
        center_start_position = (screen.columns - length) // 2
        draw_left(screen, center_start_position - 1)

        screen.cursor.x = center_start_position
        draw_center(screen, strategy)
        screen.draw(" ")

        draw_right(screen)
        center = []
    return screen.cursor.x
