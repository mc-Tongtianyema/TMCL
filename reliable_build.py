import os
import sys
import shutil
from PyInstaller import __main__ as pyi_main

# 清理之前的构建目录
def clean_build_dirs():
    try:
        for dir_name in ['build', 'dist']:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
                print(f"已清理 {dir_name} 目录")
    except Exception as e:
        print(f"清理目录时出错: {e}")

# 主构建函数
def build_executable():
    try:
        # 清理目录
        clean_build_dirs()
        
        # 设置PyInstaller参数
        args = [
            'simple_main.py',  # 入口文件
            '--name=TMCL',     # 输出文件名
            '--onefile',       # 单个可执行文件
            '--windowed',      # 窗口模式（无控制台）
            '--add-data=src;src',  # 添加数据文件
            '--noconfirm',     # 不提示确认
            '--clean'          # 清理缓存
        ]
        
        print(f"开始构建，参数: {args}")
        
        # 调用PyInstaller
        pyi_main.run(args)
        
        # 检查是否生成了可执行文件
        exe_path = os.path.join('dist', 'TMCL.exe')
        if os.path.exists(exe_path):
            print(f"✅ 构建成功！可执行文件位于: {exe_path}")
            return True
        else:
            print(f"❌ 构建失败，未找到可执行文件: {exe_path}")
            return False
    
    except Exception as e:
        print(f"构建过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始可靠构建流程...")
    success = build_executable()
    
    if success:
        print("构建已成功完成！")
        sys.exit(0)
    else:
        print("构建失败！")
        sys.exit(1)
