#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import os
from typing import Dict, List, Optional, Tuple
from PyQt5.QtCore import QThread, pyqtSignal, QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import threading
import time
from ..utils.logger import logger

class BMCLAPIClient:
    """
    BMCL API客户端，用于与BMCL API交互
    """
    
    # BMCL API基础URL
    API_BASE_URL = "https://bmclapi2.bangbang93.com"
    
    def __init__(self):
        """
        初始化API客户端
        """
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "TMCL Launcher",
            "Accept": "application/json"
        }
        self.session.headers.update(self.headers)
    
    def get_versions(self) -> List[Dict]:
        """
        获取Minecraft版本列表
        
        Returns:
            List[Dict]: 版本信息列表
        """
        try:
            url = f"{self.API_BASE_URL}/mc/game/version_manifest.json"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            versions = data.get("versions", [])
            logger.info(f"成功获取版本列表，共{len(versions)}个版本")
            return versions
        except Exception as e:
            logger.error(f"获取版本列表失败: {str(e)}")
            return []
    
    def get_version_info(self, version_id: str) -> Optional[Dict]:
        """
        获取特定版本的详细信息
        
        Args:
            version_id (str): 版本ID
            
        Returns:
            Optional[Dict]: 版本详细信息，如果失败则返回None
        """
        try:
            # 首先获取版本清单
            versions = self.get_versions()
            
            # 查找匹配的版本
            version_data = None
            for v in versions:
                if v["id"] == version_id:
                    version_data = v
                    break
            
            if not version_data:
                logger.warning(f"未找到版本: {version_id}")
                return None
            
            # 获取版本详情
            url = version_data["url"]
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            logger.info(f"成功获取版本{version_id}的详细信息")
            return response.json()
        except Exception as e:
            logger.error(f"获取版本{version_id}详情失败: {str(e)}")
            return None
    
    def download_file(self, url: str, dest_path: str, chunk_size: int = 8192) -> bool:
        """
        下载文件
        
        Args:
            url (str): 下载URL
            dest_path (str): 目标文件路径
            chunk_size (int): 下载块大小
            
        Returns:
            bool: 是否下载成功
        """
        try:
            # 确保目标目录存在
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            # 下载文件
            with self.session.get(url, stream=True, timeout=30) as response:
                response.raise_for_status()
                total_size = int(response.headers.get("content-length", 0))
                downloaded_size = 0
                
                with open(dest_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
            
            logger.info(f"文件下载成功: {url} -> {dest_path}")
            return True
        except Exception as e:
            logger.error(f"文件下载失败: {url} -> {dest_path}. 错误: {str(e)}")
            # 如果下载失败，删除部分下载的文件
            if os.path.exists(dest_path):
                try:
                    os.remove(dest_path)
                except:
                    pass
            return False
    
    def download_client(self, version_id: str, dest_dir: str) -> bool:
        """
        下载客户端jar文件
        
        Args:
            version_id (str): 版本ID
            dest_dir (str): 目标目录
            
        Returns:
            bool: 是否下载成功
        """
        try:
            # 获取版本信息
            version_info = self.get_version_info(version_id)
            if not version_info:
                return False
            
            # 获取客户端下载URL
            client_url = f"{self.API_BASE_URL}/mc/game/{version_info['downloads']['client']['sha1']}/{version_info['downloads']['client']['url'].split('/')[-1]}"
            
            # 下载客户端jar文件
            dest_path = os.path.join(dest_dir, f"versions/{version_id}/{version_id}.jar")
            return self.download_file(client_url, dest_path)
        except Exception as e:
            logger.error(f"下载客户端{version_id}失败: {str(e)}")
            return False
    
    def download_libraries(self, version_id: str, dest_dir: str) -> bool:
        """
        下载版本所需的库文件
        
        Args:
            version_id (str): 版本ID
            dest_dir (str): 目标目录
            
        Returns:
            bool: 是否所有库下载成功
        """
        try:
            # 获取版本信息
            version_info = self.get_version_info(version_id)
            if not version_info:
                return False
            
            libraries = version_info.get("libraries", [])
            success_count = 0
            failed_count = 0
            
            for lib in libraries:
                # 获取库的下载信息
                downloads = lib.get("downloads", {})
                artifact = downloads.get("artifact", {})
                
                if not artifact:
                    continue
                
                # 构建下载URL和目标路径
                url = artifact["url"]
                path = os.path.join(dest_dir, "libraries", url.split("maven/")[-1])
                
                # 下载库文件
                maven_path = url.split('maven/')[-1]
                download_url = f"{self.API_BASE_URL}/maven/{maven_path}"
                if self.download_file(download_url, path):
                    success_count += 1
                else:
                    failed_count += 1
            
            logger.info(f"库文件下载完成: 成功{success_count}, 失败{failed_count}")
            return failed_count == 0
        except Exception as e:
            logger.error(f"下载库文件失败: {str(e)}")
            return False
    
    def download_version_json(self, version_id: str, dest_dir: str) -> bool:
        """
        下载版本JSON文件
        
        Args:
            version_id (str): 版本ID
            dest_dir (str): 目标目录
            
        Returns:
            bool: 是否下载成功
        """
        try:
            # 获取版本清单
            versions = self.get_versions()
            
            # 查找匹配的版本
            version_data = None
            for v in versions:
                if v["id"] == version_id:
                    version_data = v
                    break
            
            if not version_data:
                return False
            
            # 下载JSON文件
            url = version_data["url"]
            dest_path = os.path.join(dest_dir, f"versions/{version_id}/{version_id}.json")
            return self.download_file(url, dest_path)
        except Exception as e:
            logger.error(f"下载版本JSON文件失败: {str(e)}")
            return False

class DownloadTask(QThread):
    """
    下载任务线程，用于在后台下载文件
    """
    # 进度信号
    progress_updated = pyqtSignal(str, int, int)  # task_id, downloaded_size, total_size
    # 完成信号
    task_completed = pyqtSignal(str, bool, str)  # task_id, success, message
    
    def __init__(self, task_id: str, url: str, dest_path: str):
        """
        初始化下载任务
        
        Args:
            task_id (str): 任务ID
            url (str): 下载URL
            dest_path (str): 目标文件路径
        """
        super().__init__()
        self.task_id = task_id
        self.url = url
        self.dest_path = dest_path
        self.abort_flag = False
    
    def run(self):
        """
        运行下载任务
        """
        try:
            # 确保目标目录存在
            os.makedirs(os.path.dirname(self.dest_path), exist_ok=True)
            
            # 使用PyQt的网络请求进行下载
            nam = QNetworkAccessManager()
            request = QNetworkRequest(QUrl(self.url))
            request.setRawHeader(b"User-Agent", b"TMCL Launcher")
            
            # 发送请求
            reply = nam.get(request)
            
            # 连接信号
            reply.downloadProgress.connect(self._on_download_progress)
            reply.finished.connect(self._on_download_finished)
            
            # 等待完成或中断
            while not reply.isFinished() and not self.abort_flag:
                self.msleep(100)
            
            if self.abort_flag:
                reply.abort()
                self.task_completed.emit(self.task_id, False, "下载已取消")
                return
            
            # 写入文件
            if reply.error() == QNetworkReply.NoError:
                with open(self.dest_path, "wb") as f:
                    f.write(reply.readAll())
                self.task_completed.emit(self.task_id, True, "下载成功")
            else:
                self.task_completed.emit(self.task_id, False, f"下载失败: {reply.errorString()}")
                
        except Exception as e:
            self.task_completed.emit(self.task_id, False, f"下载失败: {str(e)}")
            # 清理部分下载的文件
            if os.path.exists(self.dest_path):
                try:
                    os.remove(self.dest_path)
                except:
                    pass
    
    def _on_download_progress(self, bytes_received: int, bytes_total: int):
        """
        下载进度更新回调
        
        Args:
            bytes_received (int): 已接收字节数
            bytes_total (int): 总字节数
        """
        self.progress_updated.emit(self.task_id, bytes_received, bytes_total)
    
    def _on_download_finished(self):
        """
        下载完成回调
        """
        pass
    
    def abort(self):
        """
        中止下载任务
        """
        self.abort_flag = True

class VersionDownloadManager:
    """
    版本下载管理器，用于管理版本下载任务
    """
    
    def __init__(self, api_client: BMCLAPIClient):
        """
        初始化下载管理器
        
        Args:
            api_client (BMCLAPIClient): API客户端实例
        """
        self.api_client = api_client
        self.download_tasks = {}
        self.max_concurrent_downloads = 3
        self.active_downloads = 0
        self.download_queue = []
        self.lock = threading.RLock()
    
    def download_version(self, version_id: str, dest_dir: str, callback=None):
        """
        下载完整版本
        
        Args:
            version_id (str): 版本ID
            dest_dir (str): 目标目录
            callback: 完成回调函数
        """
        # 获取版本信息
        version_info = self.api_client.get_version_info(version_id)
        if not version_info:
            if callback:
                callback(False, "获取版本信息失败")
            return
        
        # 创建下载任务队列
        tasks = [
            (f"{version_id}_json", 
             version_info["url"], 
             os.path.join(dest_dir, f"versions/{version_id}/{version_id}.json")),
            (f"{version_id}_client", 
             f"{self.api_client.API_BASE_URL}/mc/game/{version_info['downloads']['client']['sha1']}/{version_info['downloads']['client']['url'].split('/')[-1]}", 
             os.path.join(dest_dir, f"versions/{version_id}/{version_id}.jar"))
        ]
        
        # 添加库文件下载任务
        for lib in version_info.get("libraries", []):
            downloads = lib.get("downloads", {})
            artifact = downloads.get("artifact", {})
            
            if artifact:
                url = artifact["url"]
                task_id = f"{version_id}_lib_{artifact['path']}"
                path = os.path.join(dest_dir, "libraries", artifact["path"])
                
                # 使用BMCL API下载库文件
                bmcl_url = f"{self.api_client.API_BASE_URL}/maven/{url.split('maven/')[-1]}"
                tasks.append((task_id, bmcl_url, path))
        
        # 启动下载
        self._start_downloads(tasks, callback)
    
    def _start_downloads(self, tasks: List[Tuple[str, str, str]], callback=None):
        """
        启动下载任务队列
        
        Args:
            tasks (List[Tuple[str, str, str]]): 任务列表，每项为(task_id, url, dest_path)
            callback: 完成回调函数
        """
        self.download_queue = tasks.copy()
        
        # 启动初始下载
        for _ in range(min(self.max_concurrent_downloads, len(self.download_queue))):
            self._start_next_download()
    
    def _start_next_download(self):
        """
        启动下一个下载任务
        """
        with self.lock:
            if not self.download_queue or self.active_downloads >= self.max_concurrent_downloads:
                return
            
            # 获取下一个任务
            task_id, url, dest_path = self.download_queue.pop(0)
            self.active_downloads += 1
        
        # 创建并启动下载任务
        task = DownloadTask(task_id, url, dest_path)
        task.progress_updated.connect(self._on_progress_updated)
        task.task_completed.connect(self._on_task_completed)
        self.download_tasks[task_id] = task
        task.start()
    
    def _on_progress_updated(self, task_id: str, downloaded_size: int, total_size: int):
        """
        下载进度更新回调
        
        Args:
            task_id (str): 任务ID
            downloaded_size (int): 已下载大小
            total_size (int): 总大小
        """
        # 这里可以添加进度更新处理逻辑
        pass
    
    def _on_task_completed(self, task_id: str, success: bool, message: str):
        """
        任务完成回调
        
        Args:
            task_id (str): 任务ID
            success (bool): 是否成功
            message (str): 消息
        """
        with self.lock:
            self.active_downloads -= 1
            
            # 从任务列表中移除
            if task_id in self.download_tasks:
                del self.download_tasks[task_id]
            
            # 启动下一个任务
            if self.download_queue:
                self._start_next_download()

# 创建全局API客户端实例
bmcl_api_client = BMCLAPIClient()
version_download_manager = VersionDownloadManager(bmcl_api_client)
