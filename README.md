<div align="center">
<a href="https://github.com/PCL-Community/PCL2-Python">
    <img src="Plain_Craft_Launcher_2/Images/icon.ico" alt="Logo" width="80" height="80">
</a>

# PCL2-Python

[![Hits](https://hits.zkitefly.eu.org/?tag=https://github.com/PCL-Community/PCL2-Python)](https://hits.zkitefly.eu.org/?tag=https://github.com/PCL-Community/PCL2-Python&web=true) 
</div>

=======

使用 Python 语言制作的 PCL2 仿制版本，UI 框架使用`PyQt5`，minecraft 启动框架使用`minecraft-launcher-lib`，微软登录使用`msal`（设备流）。  
由于作者技术不精、学业紧张，目前正在早期开发阶段徘徊。

## 使用

### 使用二进制分发版本
1. 打开仓库目录。
2. 下载 releases 中的二进制分发文件（`.exe`或者`.app`）。

### 自行编译
1. 执行`git clone https://github.com/PCL-Community/PCL2-Python.git main`，将仓库克隆到本地。
2. 执行`cd PCL2-Python/Plain_Craft_Launcher_2`（Windows 用户请注意正反斜杠），切换到项目包目录。
3. 运行`build.cmd`（Windows）或`build_mac.sh`（MacOS)，编译为可执行文件。
4. 打开`PCL2-Python/Plain_Craft_Launcher_2/dist`（Windows 用户请注意正反斜杠），找到编译完成后的`Application.*`文件。
> [!IMPORTANT]
> 运行时会产生大量终端日志输出，并占用一些性能。  
> 如果电脑的性能不好，或是 Python 版本过低，请使用上一种方法。  
> 使用 `Nuitka` 编译。  

## 贡献者

[![Contributors](https://contrib.rocks/image?repo=PCL-Community/PCL2-Python)](https://github.com/PCL-Community/PCL2-Python/graphs/contributors)
