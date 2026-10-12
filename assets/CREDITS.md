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
- 只展示已核实项目中出现的技术，见 [STACK-SOURCES.md](./STACK-SOURCES.md)。没有标准图标的依赖保留在依据文档中。

## 其他素材

- `daniya.gif` 是用户提供的原始 400 × 400、129 帧 GIF，文件未改动；`daniya-still.png` 是用户提供的同画面静态图。未提供原作者信息，故不虚构署名。
- `section-*.svg`、`project-*.svg`、按钮及蓝色分隔与页脚动效均为原创界面素材，由 `scripts/build_blue_profile.cjs` 生成。
- 重新生成：安装 Node.js 与 sharp >= 0.35 后运行 `node scripts/build_blue_profile.cjs`。
- 贡献图沿用本仓库原有工作流。

## 内容组织参考

- [innng](https://github.com/innng/innng)：个人介绍与侧边角色图。
- [yuna0x0](https://github.com/yuna0x0/yuna0x0)：简短正文与少量链接。
