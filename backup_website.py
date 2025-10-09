#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
圣经学习网站完整备份脚本
创建整个网站的阶段性备份，包括所有文件和数据
"""

import os
import shutil
import json
from datetime import datetime
import zipfile

def get_current_timestamp():
    """获取当前时间戳"""
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def create_backup_info():
    """创建备份信息文件"""
    backup_info = {
        "backup_time": datetime.now().isoformat(),
        "backup_type": "complete_website_backup",
        "description": "路加福音经文校验完成后的阶段性备份",
        "version": "v2.1",
        "features": [
            "经文练习系统（5节分组）",
            "智能空白算法",
            "在线经文编辑功能",
            "批量经文管理工具",
            "自动备份系统",
            "路加福音经文校验完成",
            "压缩布局优化",
            "动态按钮切换"
        ],
        "files_included": [
            "所有HTML文件",
            "所有JSON数据文件",
            "Python服务器脚本",
            "验证和修正脚本",
            "备份文件",
            "文档和报告"
        ],
        "data_status": {
            "luke.json": "已完成校验和修正",
            "other_books": "正常状态",
            "config.json": "正常配置"
        }
    }
    return backup_info

def create_complete_backup():
    """创建完整的网站备份"""
    timestamp = get_current_timestamp()
    backup_name = f"web2Lord_complete_backup_{timestamp}"
    backup_dir = f"../backups/{backup_name}"
    
    print(f"🚀 开始创建完整网站备份: {backup_name}")
    
    # 创建备份目录
    os.makedirs(backup_dir, exist_ok=True)
    
    # 获取当前工作目录
    current_dir = os.getcwd()
    
    # 需要备份的文件和目录
    items_to_backup = [
        # HTML文件
        "index.html",
        "practice.html",
        "verse_editor.html",
        "romans_study.html",
        "ephesians_study.html",
        "study.html",
        "checkin.html",
        
        # Python脚本
        "bible_server.py",
        "extract_data.py",
        "extract_ephesians_only.py",
        "extract_romans_only.py",
        "fix_luke_verses.py",
        "validate_luke.py",
        "validate_key_verses.py",
        "read_pdf.py",
        
        # 数据目录
        "data/",
        "backup_original/",
        
        # 文档文件
        "README.md",
        "路加福音校验报告.md",
        "章节添加手册.md",
        
        # 其他重要文件
        "*.json"  # 根目录下的JSON文件
    ]
    
    backup_count = 0
    
    for item in items_to_backup:
        source_path = os.path.join(current_dir, item)
        
        if item.endswith('*'):
            # 处理通配符
            import glob
            for file_path in glob.glob(source_path):
                if os.path.exists(file_path):
                    filename = os.path.basename(file_path)
                    dest_path = os.path.join(backup_dir, filename)
                    shutil.copy2(file_path, dest_path)
                    backup_count += 1
                    print(f"  ✅ 已备份: {filename}")
        elif os.path.exists(source_path):
            dest_path = os.path.join(backup_dir, item)
            
            if os.path.isdir(source_path):
                # 复制目录
                shutil.copytree(source_path, dest_path)
                file_count = sum([len(files) for r, d, files in os.walk(source_path)])
                backup_count += file_count
                print(f"  📁 已备份目录: {item} ({file_count} 个文件)")
            else:
                # 复制文件
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(source_path, dest_path)
                backup_count += 1
                print(f"  ✅ 已备份: {item}")
        else:
            print(f"  ⚠️  文件不存在，跳过: {item}")
    
    # 创建备份信息文件
    backup_info = create_backup_info()
    backup_info["files_count"] = backup_count
    backup_info["backup_path"] = backup_dir
    
    info_file = os.path.join(backup_dir, "backup_info.json")
    with open(info_file, 'w', encoding='utf-8') as f:
        json.dump(backup_info, f, ensure_ascii=False, indent=2)
    
    print(f"  📝 已创建备份信息文件: backup_info.json")
    
    # 创建ZIP压缩包
    zip_path = f"{backup_dir}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(backup_dir))
                zipf.write(file_path, arcname)
    
    # 获取压缩包大小
    zip_size = os.path.getsize(zip_path) / (1024 * 1024)  # MB
    
    print(f"\n🎉 备份完成!")
    print(f"📦 备份目录: {backup_dir}")
    print(f"🗜️  压缩包: {zip_path} ({zip_size:.1f} MB)")
    print(f"📊 备份文件数: {backup_count}")
    print(f"⏰ 备份时间: {backup_info['backup_time']}")
    
    return backup_dir, zip_path

def create_backup_readme():
    """创建备份说明文件"""
    timestamp = get_current_timestamp()
    readme_content = f"""# 圣经学习网站备份 - {timestamp}

## 备份概述
这是圣经学习网站在路加福音经文校验完成后的完整阶段性备份。

## 备份内容

### 核心功能文件
- `index.html` - 主页面
- `practice.html` - 经文练习页面（支持在线编辑）
- `verse_editor.html` - 批量经文编辑工具
- `romans_study.html` - 罗马书学习页面
- `ephesians_study.html` - 以弗所书学习页面

### 服务器和脚本
- `bible_server.py` - Bible服务器（支持经文编辑API）
- `fix_luke_verses.py` - 路加福音修正脚本
- `validate_luke.py` - 经文验证脚本
- `validate_key_verses.py` - 关键经文验证脚本

### 数据文件
- `data/` - 所有圣经书卷的JSON数据
- `backup_original/` - 原始数据备份
- `路加福音校验报告.md` - 校验工作报告

## 主要成就

### ✅ 已完成功能
1. **经文练习系统优化**
   - 5节经文分组显示
   - 智能空白数量算法（1-3个）
   - 压缩布局，节省空间
   - 动态按钮文本切换

2. **在线编辑系统**
   - 练习中实时编辑经文
   - 批量经文管理工具
   - 自动备份机制
   - Python API服务器支持

3. **路加福音经文校验**
   - 修正了主祷文版本错误
   - 统一了标点符号使用
   - 修正了关键经文7处
   - 通过了全面验证测试

### 🔧 技术特性
- 响应式网页设计
- RESTful API支持
- 实时数据更新
- 自动备份系统
- 错误处理和验证

## 使用说明

### 启动网站
```bash
cd web2Lord
python3 -m http.server 8001
```
访问: http://localhost:8001

### 启动编辑服务器
```bash
python3 bible_server.py
```

### 恢复备份
1. 解压备份文件
2. 复制所有文件到web服务器目录
3. 启动服务器

## 版本信息
- 版本: v2.1
- 备份日期: {timestamp}
- 状态: 路加福音校验完成

---
*此备份包含完整的功能代码和数据，可直接部署使用*
"""
    
    with open("../BACKUP_README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"📄 已创建备份说明: ../BACKUP_README.md")

def main():
    """主备份流程"""
    print("🌟 圣经学习网站完整备份工具")
    print("=" * 50)
    
    try:
        # 创建上级目录的backups文件夹
        os.makedirs("../backups", exist_ok=True)
        
        # 创建完整备份
        backup_dir, zip_path = create_complete_backup()
        
        # 创建备份说明
        create_backup_readme()
        
        print("\n" + "=" * 50)
        print("🎯 备份任务全部完成!")
        print("📂 可以安全地继续开发新功能了")
        
    except Exception as e:
        print(f"❌ 备份过程中出现错误: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()