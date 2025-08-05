import subprocess
import sys
import re
from packaging import version
import json

def get_installed_version(package_name):
    """获取当前安装的包版本"""
    try:
        output = subprocess.check_output(
            [sys.executable, "-m", "pip", "show", package_name],
            text=True,
            stderr=subprocess.STDOUT
        )
        # 从输出中提取版本号
        match = re.search(r'^Version:\s+(.+)$', output, re.MULTILINE)
        return match.group(1).strip() if match else None
    except subprocess.CalledProcessError:
        return None

def downgrade_package(package_name, target_version):
    """降级包到指定版本"""
    try:
        print(f"⏳ 正在降级 {package_name} 到版本 {target_version}...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", f"{package_name}=={target_version}"],
            stdout=subprocess.DEVNULL
        )
        print(f"✅ {package_name} 已成功降级到 {target_version}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 降级失败: {e}")
        return False

def main():
    # 获取用户输入
    package_name = input("请输入要降级的包名称: ").strip()
    target_version = input("请输入目标版本号: ").strip()
    
    # 验证输入
    if not package_name or not target_version:
        print("错误：包名称和版本号不能为空")
        return
    
    # 获取当前版本
    current_version = get_installed_version(package_name)
    
    if not current_version:
        print(f"❌ 未找到已安装的 {package_name} 包")
        return
    
    print(f"ℹ️ 当前安装版本: {current_version}")
    print(f"ℹ️ 目标降级版本: {target_version}")
    
    # 比较版本
    try:
        if version.parse(current_version) == version.parse(target_version):
            print("✅ 当前版本已是目标版本，无需操作")
            return
            
        elif version.parse(current_version) < version.parse(target_version):
            print("⚠️ 警告：当前版本低于目标版本，这是升级操作！")
            confirm = input("是否继续？(y/n): ").lower()
            if confirm != 'y':
                print("操作已取消")
                return
    except Exception as e:
        print(f"版本解析错误: {e}")
        return
    
    # 执行降级
    downgrade_package(package_name, target_version)
    def downgrade_packages_from_json(json_file):
        """
        遍历JSON文件中的各个包并降级到指定版本。
        JSON文件格式示例:
        {
            "package1": "1.2.3",
            "package2": "4.5.6"
        }
        """
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                packages = json.load(f)
            for pkg, ver in packages.items():
                print(f"\n处理包: {pkg}, 目标版本: {ver}")
                current_version = get_installed_version(pkg)
                if not current_version:
                    print(f"❌ 未找到已安装的 {pkg} 包")
                    continue
                print(f"当前安装版本: {current_version}")
                try:
                    if version.parse(current_version) == version.parse(ver):
                        print("✅ 当前版本已是目标版本，无需操作")
                        continue
                    elif version.parse(current_version) < version.parse(ver):
                        print("⚠️ 当前版本低于目标版本，这是升级操作！")
                        confirm = input(f"{pkg}: 是否继续？(y/n): ").lower()
                        if confirm != 'y':
                            print("操作已取消")
                            continue
                except Exception as e:
                    print(f"版本解析错误: {e}")
                    continue
                downgrade_package(pkg, ver)
        except Exception as e:
            print(f"读取或处理JSON文件失败: {e}")
if __name__ == "__main__":
    main()
