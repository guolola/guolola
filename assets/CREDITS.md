# 素材与动效

## 天台插画与 GIF

- `p3-rooftop-blue.png`：内置 image_gen 基于用户认可的像素插画调整配色，保留天台构图和角色姿态；这是同人演绎，并非官方截图。
- `p3-rooftop-blue.gif`：6.4 秒循环、64 帧、1000 × 500；在蓝色原画上叠加独立绘制的飘落花瓣与水面微光，人物保持静止。动效由 `scripts/build_blue_profile.cjs` 合成并编码，未让生成模型逐帧重画人物。
- 系统启用减少动态效果时，横幅改为静态原画。
- 原版与蓝色调整的提示词保存在 [IMAGE-PROMPT.txt](./IMAGE-PROMPT.txt)。角色与原作品相关权利归对应权利人。
- 蓝、青、白的设计方向参考 [P3R 官方网站](https://p3re.jp/en/)，本主页使用的具体色值是自选搭配，不是官方色彩规范。

## 技术图标

- 来源：[Devicon](https://github.com/devicons/devicon)，MIT 许可证保存于 `icons/LICENSE`，每个下载地址见 `icons/SOURCES.json`。
- 图标保留原有标志颜色，置于原创浅蓝底卡片；技术名称保留在图片替代文字与悬停提示中。
- 技术信息结合公开仓库核对结果和用户提供的能力截图，见 [STACK-SOURCES.md](./STACK-SOURCES.md)。

## 其他素材

- `daniya.gif` 是用户提供的原始 400 × 400、129 帧 GIF，文件未改动；`daniya-still.png` 是用户提供的同画面静态图。未提供原作者信息，故不虚构署名。
- `section-*.svg`、`project-*.svg`、按钮及蓝色分隔与页脚动效均为原创界面素材，由 `scripts/build_blue_profile.cjs` 生成。
- 重新生成：安装 Node.js 与 sharp >= 0.35 后运行 `node scripts/build_blue_profile.cjs`。
- 贡献图为保存于 main 的本地快照，自动刷新状态见下方说明。

## 内容组织参考

- [innng](https://github.com/innng/innng)：个人介绍与侧边角色图。
- [yuna0x0](https://github.com/yuna0x0/yuna0x0)：简短正文与少量链接。

## 人物动画更新

`p3-character-keyframes.png` 是内置 image_gen 基于蓝色插画生成的六帧人物动画素材；`p3-character-motion.gif` 经 `scripts/build_character_motion.cjs` 编排为 64 帧、6.4 秒循环。人物包含眨眼、轻微低头与姿态起伏；固定背景并在人物区域混合关键帧。`p3-character-still.png` 提供减少动态效果回退。

技术栈新增内容来自用户提供的技术能力截图；没有官方图标的概念使用原创蓝色文字徽标，不冒充产品官方 Logo。

贡献图保存于 main 分支的 assets。由于当前 GitHub 凭据不含 workflow 写入权限，原先发布到 output 的定时工作流已停用，以保持仓库只有 main 分支；贡献图当前为迁移时的快照。

## 当前平滑动画与图标版本

- 当前横幅为 `p3-smooth-loop.gif`：6 秒、120 帧、20fps。底图恢复为用户认可的蓝色原画；用周期函数连续驱动花瓣、微光、胸口呼吸和发梢轻微摆动，不再切换重绘的整个人物关键帧。静态替代图为 `p3-smooth-still.png`。生成脚本为 `scripts/build_smooth_motion.cjs`。
- 花瓣越过循环边界时透明度为零；人物动作均为整数周期，首尾速度连续。脚本检查循环边界变化量不高于普通帧间变化。
- Codex、Claude Code、Dify、Coze、LangChain、LangGraph、MCP 使用 [Lobe Icons](https://github.com/lobehub/lobe-icons) 收录的品牌标志（MIT）；Pinia、Pydantic、A2A 来自各自官方仓库。
- Prompt、流式输出、检索、重排等概念使用 [Lucide](https://github.com/lucide-icons/lucide) 语义图标（ISC），不将通用符号冒充产品 Logo。
- 新增资源及许可证位于 `icons/source/`，完整来源清单见 [SOURCES.json](./icons/source/SOURCES.json)。徽标合成脚本为 `scripts/build_icon_badges.py`。

## 最终技术栈展示规则

根据用户要求，当前 README 每项技术仅显示一个方形品牌 Logo，名称只用于替代文字和悬停提示；没有品牌标志的概念不显示。概念标签与通用符号已从当前技术栈移除，正文仍保留类别标题。品牌方块由 `scripts/build_brand_tiles.py` 生成。
