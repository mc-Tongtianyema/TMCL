import sys
import traceback

print("开始调试运行...")
print(f"Python版本: {sys.version}")
print(f"Python路径: {sys.path}")

try:
    # 尝试直接运行simple_main.py的内容
    import os
    import sys
    
    # 设置必要的路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(base_dir, 'src')
    
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    
    print(f"基本目录: {base_dir}")
    print(f"源代码目录: {src_dir}")
    
    # 尝试导入主模块并运行
    print("尝试导入主模块...")
    from src.main import main
    print("主模块导入成功，开始运行...")
    main()
    print("应用程序成功运行并退出")
    
except Exception as e:
    print(f"\n捕获到异常: {type(e).__name__}: {e}")
    print("\n详细堆栈跟踪:")
    traceback.print_exc(file=sys.stdout)
except KeyboardInterrupt:
    print("\n用户中断了程序")
finally:
    print("\n调试脚本结束")
