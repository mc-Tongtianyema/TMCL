#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TMCL启动器打包脚本
使用PyInstaller创建可执行文件
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent

# 输出目录
OUTPUT_DIR = PROJECT_ROOT / "dist"

# 临时构建目录
BUILD_DIR = PROJECT_ROOT / "build"

def run_command(command, cwd=None):
    """
    运行命令行命令
    
    Args:
        command: 命令字符串
        cwd: 工作目录
        
    Returns:
        bool: 命令是否成功执行
    """
    print(f"执行命令: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd or PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            print(f"命令执行失败，错误码: {result.returncode}")
            print(f"错误输出: {result.stderr}")
            return False
        
        if result.stdout:
            print(f"命令输出: {result.stdout}")
            
        return True
    except Exception as e:
        print(f"执行命令时出错: {e}")
        return False

def clean_old_builds():
    """
    清理旧的构建文件
    """
    print("清理旧的构建文件...")
    
    # 删除输出目录
    if OUTPUT_DIR.exists():
        try:
            shutil.rmtree(OUTPUT_DIR)
            print(f"已删除旧的输出目录: {OUTPUT_DIR}")
        except Exception as e:
            print(f"删除输出目录时出错: {e}")
    
    # 删除构建目录
    if BUILD_DIR.exists():
        try:
            shutil.rmtree(BUILD_DIR)
            print(f"已删除旧的构建目录: {BUILD_DIR}")
        except Exception as e:
            print(f"删除构建目录时出错: {e}")
    
    # 删除.spec文件
    spec_file = PROJECT_ROOT / "TMCL.spec"
    if spec_file.exists():
        try:
            spec_file.unlink()
            print(f"已删除旧的spec文件: {spec_file}")
        except Exception as e:
            print(f"删除spec文件时出错: {e}")

def build_executable():
    """
    使用PyInstaller构建可执行文件
    """
    print("开始构建可执行文件...")
    
    # 检查PyInstaller是否已安装
    if not run_command("pip show pyinstaller"):
        print("安装PyInstaller...")
        if not run_command("pip install pyinstaller"):
            print("安装PyInstaller失败，请手动安装")
            return False
    
    # 确保src目录存在
    src_dir = PROJECT_ROOT / "src"
    if not src_dir.exists():
        print(f"错误: 找不到源代码目录 {src_dir}")
        return False
    
    # 生成.spec文件而不是直接构建，以便更好地控制构建过程
    spec_file = PROJECT_ROOT / 'TMCL.spec'
    
    # 如果spec文件存在，先删除它
    if spec_file.exists():
        try:
            spec_file.unlink()
            print(f"已删除旧的spec文件: {spec_file}")
        except Exception as e:
            print(f"删除spec文件时出错: {e}")
    
    # 必要的hidden imports列表
    hidden_imports = [
        "PyQt5", "PyQt5.QtWidgets", "PyQt5.QtGui", "PyQt5.QtCore",
        "PyQt5.sip", "yaml", "json", "os", "sys", "shutil", "requests",
        "src.api.bmcl_api", "src.api.http_request",
        "src.config.config_manager",
        "src.core.config_manager", "src.core.constants", "src.core.game_launcher", 
        "src.core.process_manager", "src.core.version_manager",
        "src.ui.components.custom_label", "src.ui.components.custom_button", 
        "src.ui.components.panel", "src.ui.components.custom_progress_bar", 
        "src.ui.components.download_manager", "src.ui.components.version_item",
        "src.ui.components.custom_input",
        "src.ui.pages.launch_page", "src.ui.pages.version_page", 
        "src.ui.pages.settings_page", "src.ui.pages.about_page",
        "src.utils.logger", "src.utils.api_client", "src.utils.utils"
    ]
    
    # 构建命令
    cmd = [
        "pyinstaller",
        "--name=TMCL",
        "--onefile",  # 生成单个可执行文件
        "--windowed",  # 无控制台窗口
        "--icon=NONE",  # 暂时不设置图标，可以后续添加
        f"--paths={PROJECT_ROOT}",
        f"--paths={src_dir}",
        "--clean",  # 清理PyInstaller缓存
        f"--distpath={OUTPUT_DIR}",
        f"--workpath={BUILD_DIR}",
        "--add-data=requirements.txt;."  # 添加requirements.txt
    ]
    
    # 添加所有hidden imports
    for imp in hidden_imports:
        cmd.append(f"--hidden-import={imp}")
    
    # 添加主入口文件
    cmd.append(f"{src_dir / 'main.py'}")
    
    # 构建命令字符串
    build_cmd = " ".join(cmd)
    
    # 执行构建
    if not run_command(build_cmd):
        print("构建可执行文件失败")
        return False
    
    print("构建可执行文件成功!")
    print(f"可执行文件位置: {OUTPUT_DIR / 'TMCL.exe'}")
    return True

def create_release_package():
    """
    创建发布包
    """
    print("创建发布包...")
    
    if not OUTPUT_DIR.exists():
        print(f"错误: 找不到输出目录 {OUTPUT_DIR}")
        return False
    
    # 复制必要文件到输出目录
    files_to_copy = [
        "README.md",
        "requirements.txt"
    ]
    
    for file_name in files_to_copy:
        src_file = PROJECT_ROOT / file_name
        if src_file.exists():
            try:
                shutil.copy2(src_file, OUTPUT_DIR / file_name)
                print(f"已复制 {file_name} 到输出目录")
            except Exception as e:
                print(f"复制 {file_name} 时出错: {e}")
    
    print("发布包创建成功!")
    print(f"发布包位置: {OUTPUT_DIR}")
    return True

def main():
    """
    主函数
    """
    print("===== TMCL启动器打包脚本 =====")
    
    # 清理旧的构建
    clean_old_builds()
    
    # 构建可执行文件
    if not build_executable():
        print("打包失败!")
        return 1
    
    # 不再使用create_release_package()，因为我们已经使用--onefile模式
    
    print("\n===== 打包完成 =====")
    print(f"您可以在 {OUTPUT_DIR} 目录下找到打包好的程序")
    return 0

if __name__ == "__main__":
    sys.exit(main())
