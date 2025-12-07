# TMCL 启动器

**TMCL** 是一个功能丰富的《我的世界》(Minecraft)启动器，专为中文用户设计，提供简单易用的界面和强大的功能。

## 功能特点

- 🎮 **游戏启动**: 一键启动《我的世界》游戏，支持自定义内存分配和启动参数
- 🔄 **版本管理**: 浏览、下载、安装和切换不同的Minecraft版本
- 📂 **文件管理**: 查看和管理游戏文件、资源包、模组等
- ⚙️ **个性化设置**: 自定义启动器外观和行为
- 🔧 **技术支持**: 详细的日志记录和错误报告功能

## 系统要求

- **操作系统**: Windows 7/8/10/11
- **Python版本**: 3.6 或更高版本
- **Java**: 需要安装Java运行时环境(JRE) 8 或更高版本
- **存储**: 至少500MB可用空间

## 安装方法

### 方法一：使用已编译的可执行文件

1. 从[发布页面](https://example.com/tmcl/releases)下载最新版本的TMCL启动器
2. 解压下载的压缩包
3. 运行 `TMCL.exe` 启动启动器

### 方法二：从源代码运行

1. 确保已安装Python 3.6+和pip
2. 克隆或下载本仓库
3. 安装依赖项：
   ```bash
   pip install -r requirements.txt
   ```
4. 运行启动器：
   ```bash
   python src/main.py
   ```

## 使用说明

### 游戏启动

1. 在主界面选择要启动的Minecraft版本
2. 输入您的游戏用户名
3. 根据需要调整内存分配设置
4. 点击「启动游戏」按钮开始游戏

### 版本管理

1. 切换到「游戏版本」选项卡
2. 浏览可用的游戏版本
3. 点击「下载」按钮下载您想要的版本
4. 下载完成后，该版本将出现在启动界面的版本列表中

### 设置

1. 切换到「设置」选项卡
2. 根据需要调整启动器设置
3. 点击「保存」按钮应用更改

## 开发指南

如果您想参与TMCL启动器的开发，请按照以下步骤操作：

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request

## 打包发布

如果您想自己构建可执行文件，可以使用提供的构建脚本：

```bash
python build.py
```

构建完成后，可执行文件将位于 `dist` 目录中。

## 许可证

本项目采用MIT许可证 - 详情请参阅LICENSE文件

## 贡献者

- [TMCL Team](https://github.com/tmcl-team)

## 反馈与支持

如果您在使用过程中遇到任何问题，或者有任何建议，请：

- 提交[Issue](https://github.com/tmcl-team/tmcl/issues)报告问题
- 联系我们的技术支持 team@tmcl.example.com

---

© 2024 TMCL Team. 保留所有权利。
