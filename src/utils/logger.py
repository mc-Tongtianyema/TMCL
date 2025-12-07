#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import sys
from datetime import datetime
from PyQt5.QtCore import QStandardPaths

class LoggerManager:
    """
    日志管理器，用于配置和管理日志
    """
    
    # 日志级别映射
    LOG_LEVEL_MAP = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG
    }
    
    def __init__(self):
        """
        初始化日志管理器
        """
        # 获取日志目录
        self.log_dir = self._get_log_directory()
        
        # 确保日志目录存在
        self._ensure_log_directory()
        
        # 创建日志文件路径
        self.log_file = self._create_log_file()
        
        # 配置日志
        self._configure_logger()
    
    def _get_log_directory(self):
        """
        获取日志目录
        
        Returns:
            str: 日志目录路径
        """
        # 获取用户数据目录
        if os.name == "nt":  # Windows
            log_dir = os.path.join(os.environ.get("APPDATA", ""), "TMCL", "logs")
        else:
            # Linux: ~/.config/TMCL/logs, macOS: ~/Library/Application Support/TMCL/logs
            log_dir = os.path.join(
                QStandardPaths.writableLocation(QStandardPaths.AppDataLocation), 
                "TMCL", 
                "logs"
            )
        
        return log_dir
    
    def _ensure_log_directory(self):
        """
        确保日志目录存在
        """
        if not os.path.exists(self.log_dir):
            try:
                os.makedirs(self.log_dir)
            except Exception as e:
                print(f"无法创建日志目录: {str(e)}")
    
    def _create_log_file(self):
        """
        创建日志文件
        
        Returns:
            str: 日志文件路径
        """
        # 获取当前日期时间
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        
        # 创建日志文件名
        log_filename = f"tmcl-{date_str}.log"
        log_file = os.path.join(self.log_dir, log_filename)
        
        # 如果文件超过10MB，创建新文件
        if os.path.exists(log_file) and os.path.getsize(log_file) > 10 * 1024 * 1024:
            # 创建带时间戳的文件
            time_str = now.strftime("%H-%M-%S")
            log_filename = f"tmcl-{date_str}-{time_str}.log"
            log_file = os.path.join(self.log_dir, log_filename)
        
        return log_file
    
    def _configure_logger(self):
        """
        配置日志器
        """
        # 获取根日志器
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        
        # 清除现有的处理器
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # 创建文件处理器
        file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # 创建格式器
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # 设置格式器
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # 记录初始化日志
        logging.info(f"日志系统初始化完成，日志文件位于: {self.log_file}")
    
    def set_level(self, level):
        """
        设置日志级别
        
        Args:
            level: 日志级别索引或logging模块的级别常量
        """
        # 获取根日志器
        logger = logging.getLogger()
        
        # 如果是整数索引，转换为logging级别
        if isinstance(level, int) and level in self.LOG_LEVEL_MAP:
            level_value = self.LOG_LEVEL_MAP[level]
        else:
            level_value = level
        
        # 设置控制台日志级别
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(level_value)
                break
        
        logging.info(f"日志级别已设置为: {logging.getLevelName(level_value)}")

# 创建全局日志器实例
logger_manager = LoggerManager()

# 获取并导出logger对象供其他模块使用
logger = logging.getLogger("TMCL")

# 保持向后兼容性，提供setup_logger函数
def setup_logger(name, log_dir=None):
    """
    设置日志记录器（保持向后兼容）
    
    Args:
        name (str): 日志记录器名称
        log_dir (str, optional): 日志文件目录. 默认为None, 使用默认位置
    
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 直接返回命名的logger，全局日志配置已由LoggerManager处理
    return logging.getLogger(name)

# 添加常用日志方法的别名，便于使用
debug = logger.debug
info = logger.info
warning = logger.warning
warn = logger.warning
error = logger.error
critical = logger.critical
exception = logger.exception
