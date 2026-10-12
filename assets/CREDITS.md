# 素材与动效

## 角色动图

- `daniya.gif`：用户提供的原始 GIF，400 × 400，129 帧。原文件直接复制，未裁切、重绘或减帧。
- `daniya-still.png`：用户先前提供的同画面静态 PNG，用于系统减少动态效果设置下的展示。
- 这是非官方粉丝个人主页。原角色和原作品相关权利归对应权利人；用户未提供 GIF 作者或原发布地址，故不标注未经确认的作者。

## 原创界面动效

- `profile-hero.gif`：霓虹轨道、星点、高光和循环滚动条。
- `persona-select.gif`：Persona 3 / 4 / 5 三色选单。
- `save-point.gif`：循环节奏条。
- `*-still.png`：上述动画的静态首帧，用于减少动态效果设置。
- 三组动画由 `scripts/build_motion.py` 绘制，不依赖第三方动图服务，也未使用官方游戏 UI 素材。
- 重新生成：安装 Pillow 后，运行 `python scripts/build_motion.py`。默认使用 Windows 字体目录；其他系统需调整脚本的字体路径。

## 内容组织参考

- [innng](https://github.com/innng/innng)：个人介绍与侧边角色图。
- [yuna0x0](https://github.com/yuna0x0/yuna0x0)：简短正文与少量链接。
- [jefftrojan](https://github.com/jefftrojan/jefftrojan)：文字形式的爱好介绍。

当前视觉按用户的新要求改为高彩度游戏菜单风格；未复制上述主页的代码、图片或个人文案。
