@echo off
cd dist
TMCL.exe > error_log.txt 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 应用程序执行失败，错误代码: %ERRORLEVEL%
    echo 请查看 error_log.txt 文件以获取详细信息
) else (
    echo 应用程序执行完成
)