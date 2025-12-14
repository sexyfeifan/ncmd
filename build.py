#!/usr/bin/env python3
"""
网易云音乐下载器 v2.4.0 构建脚本
"""

import os
import sys
import shutil
import subprocess
import plistlib
from pathlib import Path

def build_with_pyinstaller():
    """使用PyInstaller构建应用"""
    print("开始构建网易云音乐下载器 v2.4.0...")
    
    app_name = "网易云音乐下载器"
    
    # 清理之前的构建目录
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # PyInstaller命令
    cmd = [
        "pyinstaller",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录而不是单个文件
        "--name", app_name,
        "main.py"
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("PyInstaller 构建完成")
        if result.stdout:
            print(f"stdout: {result.stdout}")
        if result.stderr:
            print(f"stderr: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"PyInstaller 构建失败: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)

def fix_app_bundle():
    """修复应用包"""
    app_path = "dist/网易云音乐下载器.app"
    if not os.path.exists(app_path):
        print(f"错误: 应用包 {app_path} 不存在")
        return False
    
    print(f"修复应用包: {app_path}")
    
    # 修复 Info.plist
    info_plist_path = os.path.join(app_path, "Contents", "Info.plist")
    if os.path.exists(info_plist_path):
        with open(info_plist_path, 'rb') as f:
            plist_data = plistlib.load(f)
        
        # 更新版本号
        plist_data['CFBundleShortVersionString'] = '2.4.0'
        plist_data['CFBundleVersion'] = '2.4.0'
        
        # 添加必要的键值
        plist_data['LSMinimumSystemVersion'] = '10.12'
        plist_data['NSHumanReadableCopyright'] = '© 2025 网易云音乐下载器'
        
        with open(info_plist_path, 'wb') as f:
            plistlib.dump(plist_data, f)
        
        print("Info.plist 修复完成")
    
    # 确保可执行文件有正确的权限
    exe_path = os.path.join(app_path, "Contents", "MacOS", "网易云音乐下载器")
    if os.path.exists(exe_path):
        os.chmod(exe_path, 0o755)
        print("可执行文件权限修复完成")
    
    return True

def fix_code_signing():
    """修复代码签名"""
    app_path = "dist/网易云音乐下载器.app"
    if not os.path.exists(app_path):
        print(f"错误: 应用包 {app_path} 不存在")
        return False
    
    print("修复代码签名...")
    
    # 清理扩展属性
    try:
        subprocess.run(["xattr", "-cr", app_path], check=True)
        print("扩展属性清理完成")
    except subprocess.CalledProcessError as e:
        print(f"清理扩展属性失败: {e}")
    
    # 尝试进行临时签名
    try:
        subprocess.run(["codesign", "--force", "--deep", "--sign", "-", app_path], check=True)
        print("代码签名完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"代码签名失败: {e}")
        return False

def create_final_release():
    """创建最终发布版本"""
    source_app = "dist/网易云音乐下载器.app"
    final_dir = "netease_music_downloader_v2.4.0"
    
    # 创建发布目录
    if os.path.exists(final_dir):
        shutil.rmtree(final_dir)
    os.makedirs(final_dir)
    
    # 复制应用
    dest_app = os.path.join(final_dir, "网易云音乐下载器.app")
    shutil.copytree(source_app, dest_app)
    
    # 复制必要的文件
    files_to_copy = [
        "README.md",
        "README_v2.4.0.md",
        "requirements.txt",
        "cookie.txt"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, final_dir)
    
    # 创建版本说明
    version_info = """网易云音乐下载器 v2.4.0

更新内容：
1. 版本号升级至 v2.4.0
2. 优化了下载性能和稳定性
3. 修复了已知问题

主要特性：
- 完整的歌曲搜索功能
- 歌手页面跳转和专辑页面查看
- 批量下载歌曲
- 多种音质选择（支持智能降级）
- 完善的元数据嵌入（包括FLAC封面）
- 可调节的并发下载（1-5个并发）
- 实时下载进度显示
- 暂停/继续/取消功能
- 已下载歌曲识别

使用说明：
1. 首次运行需要登录网易云音乐账号
2. 解析歌单后选择要下载的歌曲
3. 可以选择音质和下载设置
4. 支持批量下载和断点续传

注意事项：
1. 下载的音乐仅供个人学习和欣赏，请尊重版权
2. 请遵守相关法律法规，勿用于商业用途
"""
    
    with open(os.path.join(final_dir, "version_info.txt"), "w", encoding="utf-8") as f:
        f.write(version_info)
    
    print(f"最终发布版本已创建: {final_dir}")
    return final_dir

def create_zip_package(release_dir):
    """创建ZIP压缩包"""
    zip_name = "网易云音乐下载器_v2.4.0_macOS.zip"
    
    try:
        subprocess.run([
            "zip", "-r", zip_name, 
            "网易云音乐下载器.app",
            "README.md",
            "README_v2.4.0.md",
            "requirements.txt",
            "version_info.txt",
            "cookie.txt"
        ], cwd=release_dir, check=True)
        print(f"ZIP 包创建完成: {zip_name}")
    except subprocess.CalledProcessError as e:
        print(f"创建 ZIP 包失败: {e}")

def main():
    """主函数"""
    print("开始构建网易云音乐下载器 v2.4.0...")
    
    # 1. 使用PyInstaller构建
    build_with_pyinstaller()
    
    # 2. 修复应用包
    if not fix_app_bundle():
        print("应用包修复失败")
        sys.exit(1)
    
    # 3. 修复代码签名
    fix_code_signing()
    
    # 4. 创建最终发布版本
    release_dir = create_final_release()
    
    # 5. 创建ZIP压缩包
    create_zip_package(release_dir)
    
    print("网易云音乐下载器 v2.4.0 构建完成!")

if __name__ == "__main__":
    main()