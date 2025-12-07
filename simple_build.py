import os
import subprocess
import sys

# 简单的构建脚本
print("===== 简单构建脚本 =====")

# 清理旧的构建文件
print("清理旧的构建文件...")
os.system("rmdir /s /q dist build 2>nul")
os.system("del *.spec 2>nul")

# 安装必要的依赖
print("安装必要依赖...")
os.system(f"{sys.executable} -m pip install pyinstaller PyQt5 requests pyyaml")

# 直接运行pyinstaller命令
print("开始构建...")
# 添加正确的路径和隐藏导入
build_cmd = f"pyinstaller --name=TMCL --onefile --console " \
           f"--paths={os.path.abspath('src')} " \
           f"--hidden-import=utils " \
           f"--hidden-import=utils.logger " \
           f"--hidden-import=src.core " \
           f"--hidden-import=src.ui " \
           f"--hidden-import=src.utils " \
           f"--hidden-import=src.utils.api_client " \
           f"--hidden-import=PyQt5.QtWidgets " \
           f"--hidden-import=PyQt5.QtGui " \
           f"--hidden-import=PyQt5.QtCore " \
           f"--hidden-import=requests " \
           f"--hidden-import=yaml " \
           f"--hidden-import=socket " \
           f"--hidden-import=json " \
           f"--hidden-import=sys " \
           f"--hidden-import=os " \
           f"src/main.py"
print(f"执行命令: {build_cmd}")

# 执行构建
result = subprocess.run(build_cmd, shell=True)

if result.returncode == 0:
    print("\n构建成功!")
    print("可执行文件位置: dist\TMCL.exe")
    print("注意: 由于使用了--console模式，运行时会显示控制台窗口用于调试")
else:
    print("\n构建失败!")
    sys.exit(1)
