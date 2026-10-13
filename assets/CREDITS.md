# 素材与动效

## 天台插画（主视觉）

- `p3-rooftop-blue.png`：内置 image_gen 基于用户认可的像素插画调整配色，保留天台构图与角色姿态；这是同人演绎，并非官方截图。原版与蓝色调整的提示词见 [IMAGE-PROMPT.txt](./IMAGE-PROMPT.txt)。角色与原作品相关权利归对应权利人。
- `hero-rooftop.gif`：1200 × 600，144 帧 × 60 ms（8.64 秒循环），由 [`scripts/build_hero.py`](../scripts/build_hero.py) 在原画上叠加独立动效层生成，人物不重绘：
  - 结城理的胸口随呼吸轻微起伏（每个循环两次呼吸）；埃癸斯头侧的发梢随风轻摆；脸部区域逐帧像素一致，脚本会校验。
  - 像素花瓣在画框内飘落，被画框裁切，循环边界处位于画面外；远处水面有微光。
  - 所有动作都是整数周期，第 N 帧与第 0 帧相同；全片使用同一调色板与固定位置的有序抖动，静止像素逐帧完全一致，避免闪烁。
- `hero-rooftop-still.png`：系统开启“减少动态效果”时显示的静态图。
- 蓝、青、白的设计方向参考 [P3R 官方网站](https://p3re.jp/en/)，具体色值为自选搭配，不是官方色彩规范。

## 达妮娅头像

- `daniya.gif` 是用户提供的原始 400 × 400、129 帧 GIF，文件未改动；`daniya-still.png` 是用户提供的同画面静态图。未提供原作者信息，故不虚构署名。
- `denia-portrait.gif` / `denia-portrait-still.png` 由 [`scripts/build_portrait.py`](../scripts/build_portrait.py) 生成：保留原动画全部帧与时长，缩放至 336 px，并加上与页面一致的切角相框和像素猫耳。

## 界面与像素小人

- `ui/` 下的章节标题、按钮、项目卡、对话气泡、分隔线与页脚均为原创 SVG，由 [`scripts/build_ui.py`](../scripts/build_ui.py) 生成；像素小人（结城理与埃癸斯的背影、小丸、蓝蝶、花瓣）在 [`scripts/sprites.py`](../scripts/sprites.py) 中逐像素绘制。
- SVG 内的动效（蝴蝶振翅、星光、小丸奔跑、花瓣）在“减少动态效果”下自动静止。
- 标题文字已转为路径，不依赖访客字体：
  - [Barlow Condensed](https://github.com/google/fonts/tree/main/ofl/barlowcondensed)（SIL OFL 1.1）
  - [得意黑 Smiley Sans](https://github.com/atelier-anchor/smiley-sans)（SIL OFL 1.1）
- 重新生成：把上述字体（`BarlowCondensed-ExtraBoldItalic/BoldItalic/SemiBoldItalic.ttf`、`SmileySans-Oblique.ttf`）放入 `FONT_DIR`，安装 `fonttools`、`uharfbuzz`、`svgelements`，运行 `python scripts/build_ui.py`；`build_hero.py` 与 `build_portrait.py` 只需 Pillow 与 NumPy。

## 技术图标

- 每项技术只显示一个方形品牌 Logo，名称保留在替代文字与悬停提示中；没有可识别 Logo 的概念不显示。
- [Devicon](https://github.com/devicons/devicon)（MIT，许可证见 `icons/LICENSE`，下载地址见 `icons/SOURCES.json`）。
- Codex、Claude Code、Dify、Coze、LangChain、LangGraph、MCP 来自 [Lobe Icons](https://github.com/lobehub/lobe-icons)（MIT）；Pinia、Pydantic、A2A、Vite 来自各自官方仓库；ECharts 来自 [Simple Icons](https://github.com/simple-icons/simple-icons)。来源与许可证见 `icons/source/`。
- 技术信息依据见 [STACK-SOURCES.md](./STACK-SOURCES.md)。

## 贡献记录

`ui/activity-light.svg` / `ui/activity-dark.svg` 于 2026-10-12 用 [Platane/snk](https://github.com/Platane/snk)（svg-only）在本地生成，配色改为页面蓝色系，并加入减少动态效果时静止的规则。仓库中的定时工作流已停用（当前凭据没有 workflow 写入权限，且原流程会发布到额外的 output 分支），因此这是快照，仓库保持只有 main 分支。

## 内容组织参考

- [innng](https://github.com/innng/innng)：个人介绍与侧边角色图。
- [yuna0x0](https://github.com/yuna0x0/yuna0x0)：简短正文与少量链接。
