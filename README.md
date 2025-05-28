1.  **安装Python**: 确保您的系统上安装了Python 3.6 或更高版本。

2.  **安装依赖**: 打开您的终端或命令行工具，运行以下命令安装所需的Python库：

    ```bash
    pip install markdown argparse playwright
    ```

3.  **安装Playwright浏览器驱动**: `Playwright` 需要浏览器驱动才能将HTML转换为PDF。运行以下命令下载它们：

    ```bash
    playwright install
    ```
    这将自动下载 Chromium, Firefox, 和 WebKit 浏览器驱动。
