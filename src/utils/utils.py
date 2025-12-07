#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import shutil
import hashlib
import platform
import subprocess
from datetime import datetime
from pathlib import Path

class Utils:
    """
    工具函数类，提供通用的辅助功能
    """
    @staticmethod
    def get_platform_info():
        """
        获取当前平台信息
        
        Returns:
            dict: 平台信息，包含系统类型、版本、架构等
        """
        system = platform.system()
        release = platform.release()
        version = platform.version()
        machine = platform.machine()
        python_version = platform.python_version()
        
        return {
            "system": system,
            "release": release,
            "version": version,
            "machine": machine,
            "python_version": python_version
        }
    
    @staticmethod
    def get_os_type():
        """
        获取操作系统类型
        
        Returns:
            str: 操作系统类型 (windows, macos, linux)
        """
        system = platform.system().lower()
        
        if "windows" in system:
            return "windows"
        elif "darwin" in system:
            return "macos"
        else:
            return "linux"
    
    @staticmethod
    def calculate_file_hash(file_path, algorithm='sha1', chunk_size=8192):
        """
        计算文件的哈希值
        
        Args:
            file_path (str): 文件路径
            algorithm (str): 哈希算法 (md5, sha1, sha256等)
            chunk_size (int): 分块大小
            
        Returns:
            str: 文件哈希值
        """
        try:
            hash_obj = hashlib.new(algorithm)
            
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    hash_obj.update(chunk)
                    
            return hash_obj.hexdigest()
        except Exception:
            return None
    
    @staticmethod
    def format_size(size_bytes):
        """
        格式化文件大小
        
        Args:
            size_bytes (int): 字节大小
            
        Returns:
            str: 格式化后的大小
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    @staticmethod
    def format_datetime(dt_string, input_format="%Y-%m-%dT%H:%M:%S.%fZ", output_format="%Y-%m-%d %H:%M:%S"):
        """
        格式化日期时间
        
        Args:
            dt_string (str): 日期时间字符串
            input_format (str): 输入格式
            output_format (str): 输出格式
            
        Returns:
            str: 格式化后的日期时间字符串
        """
        try:
            # 处理末尾的Z字符
            if dt_string.endswith('Z'):
                dt_string = dt_string[:-1] + '+00:00'
                input_format = "%Y-%m-%dT%H:%M:%S.%f%z"
            
            dt = datetime.strptime(dt_string, input_format)
            return dt.strftime(output_format)
        except Exception:
            return dt_string
    
    @staticmethod
    def ensure_directory(directory):
        """
        确保目录存在，如果不存在则创建
        
        Args:
            directory (str): 目录路径
        """
        os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def remove_directory(directory):
        """
        移除目录及其内容
        
        Args:
            directory (str): 目录路径
            
        Returns:
            bool: 是否成功移除
        """
        try:
            if os.path.exists(directory):
                shutil.rmtree(directory)
            return True
        except Exception:
            return False
    
    @staticmethod
    def copy_file(src, dst):
        """
        复制文件
        
        Args:
            src (str): 源文件路径
            dst (str): 目标文件路径
            
        Returns:
            bool: 是否成功复制
        """
        try:
            # 确保目标目录存在
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            return True
        except Exception:
            return False
    
    @staticmethod
    def move_file(src, dst):
        """
        移动文件
        
        Args:
            src (str): 源文件路径
            dst (str): 目标文件路径
            
        Returns:
            bool: 是否成功移动
        """
        try:
            # 确保目标目录存在
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
            return True
        except Exception:
            return False
    
    @staticmethod
    def read_json_file(file_path):
        """
        读取JSON文件
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            dict: JSON数据，如果失败返回None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    
    @staticmethod
    def write_json_file(file_path, data, indent=2):
        """
        写入JSON文件
        
        Args:
            file_path (str): 文件路径
            data (dict): 要写入的数据
            indent (int): 缩进空格数
            
        Returns:
            bool: 是否成功写入
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    @staticmethod
    def open_file(file_path):
        """
        使用默认程序打开文件
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            bool: 是否成功打开
        """
        try:
            if os.path.exists(file_path):
                if Utils.get_os_type() == "windows":
                    os.startfile(file_path)  # Windows
                elif Utils.get_os_type() == "macos":
                    subprocess.run(["open", file_path])  # macOS
                else:
                    subprocess.run(["xdg-open", file_path])  # Linux
                return True
        except Exception:
            pass
        return False
    
    @staticmethod
    def open_directory(directory_path):
        """
        打开目录
        
        Args:
            directory_path (str): 目录路径
            
        Returns:
            bool: 是否成功打开
        """
        return Utils.open_file(directory_path)
    
    @staticmethod
    def get_file_extension(file_name):
        """
        获取文件扩展名
        
        Args:
            file_name (str): 文件名
            
        Returns:
            str: 扩展名（不含点号）
        """
        _, ext = os.path.splitext(file_name)
        return ext[1:].lower() if ext else ""
    
    @staticmethod
    def get_file_name(file_path):
        """
        获取文件名（不含路径）
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            str: 文件名
        """
        return os.path.basename(file_path)
    
    @staticmethod
    def is_writable(path):
        """
        检查路径是否可写
        
        Args:
            path (str): 文件或目录路径
            
        Returns:
            bool: 是否可写
        """
        if os.path.isdir(path):
            test_file = os.path.join(path, "__test_write__.tmp")
            try:
                with open(test_file, 'w') as f:
                    f.write("")
                os.remove(test_file)
                return True
            except Exception:
                return False
        else:
            return os.access(path, os.W_OK) if os.path.exists(path) else os.access(os.path.dirname(path), os.W_OK)
    
    @staticmethod
    def get_relative_path(path, base_dir):
        """
        获取相对路径
        
        Args:
            path (str): 目标路径
            base_dir (str): 基础目录
            
        Returns:
            str: 相对路径
        """
        try:
            return os.path.relpath(path, base_dir)
        except Exception:
            return path
