#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GitHub Pages 发布准备脚本
优化网站代码，使其适合在 GitHub Pages 上运行
"""

import os
import json
import shutil
from datetime import datetime

def create_github_optimized_version():
    """创建适合 GitHub Pages 的优化版本"""
    print("🚀 正在准备 GitHub Pages 发布版本...")
    
    # 创建发布目录
    release_dir = "github_release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # 需要复制的核心文件
    core_files = [
        "index.html",
        "practice.html", 
        "verse_editor.html",
        "romans_study.html",
        "ephesians_study.html",
        "study.html"
    ]
    
    # 复制 HTML 文件
    for file in core_files:
        if os.path.exists(file):
            shutil.copy2(file, release_dir)
            print(f"  ✅ 复制: {file}")
    
    # 复制数据目录
    if os.path.exists("data"):
        shutil.copytree("data", os.path.join(release_dir, "data"))
        print(f"  📁 复制: data/ 目录")
    
    # 复制文档文件
    doc_files = ["README.md", "GitHub发布指南.md"]
    for file in doc_files:
        if os.path.exists(file):
            shutil.copy2(file, release_dir)
            print(f"  📝 复制: {file}")
    
    return release_dir

def optimize_for_static_hosting(release_dir):
    """优化代码以适应静态托管"""
    print("\n🔧 优化代码以适应静态托管...")
    
    # 1. 修改 practice.html，移除服务器编辑功能
    practice_file = os.path.join(release_dir, "practice.html")
    if os.path.exists(practice_file):
        with open(practice_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 注释掉编辑功能（保留UI但禁用服务器调用）
        content = content.replace(
            'fetch("http://localhost:8001/api/save-verse"',
            '// 静态版本暂不支持在线编辑\n            // fetch("http://localhost:8001/api/save-verse"'
        )
        
        # 添加静态版本提示
        static_notice = '''
        <!-- GitHub Pages 静态版本提示 -->
        <div id="static-notice" style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 10px 0; border-radius: 5px; font-size: 14px;">
            📋 <strong>静态版本说明</strong>: 此为 GitHub Pages 托管版本，在线编辑功能已禁用。如需编辑经文，请下载完整版本在本地使用。
        </div>
        '''
        
        content = content.replace('<div class="container">', '<div class="container">' + static_notice)
        
        with open(practice_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("  ✅ 优化 practice.html")
    
    # 2. 优化 verse_editor.html
    editor_file = os.path.join(release_dir, "verse_editor.html")
    if os.path.exists(editor_file):
        with open(editor_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 添加静态版本说明
        static_notice = '''
        <div style="background: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; margin: 20px; border-radius: 5px;">
            <h4>⚠️ 静态版本限制</h4>
            <p>此为 GitHub Pages 静态托管版本，无法保存编辑结果到服务器。</p>
            <p><strong>建议</strong>: 下载完整版本到本地使用，或将编辑结果手动复制保存。</p>
        </div>
        '''
        
        content = content.replace('<div class="container">', '<div class="container">' + static_notice)
        
        with open(editor_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("  ✅ 优化 verse_editor.html")

def create_github_files(release_dir):
    """创建 GitHub 相关文件"""
    print("\n📝 创建 GitHub 配置文件...")
    
    # 1. 创建 .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# 本地开发文件
bible_server.py
validate_*.py
fix_*.py
extract_*.py
backup_*.py
backup_original/
"""
    
    with open(os.path.join(release_dir, ".gitignore"), 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    print("  ✅ 创建 .gitignore")
    
    # 2. 更新 README.md
    readme_content = f"""# 圣经学习练习网站

一个基于网页的圣经经文学习和练习系统，帮助用户通过填空练习加深对圣经的记忆和理解。

## 🌟 在线访问

**GitHub Pages**: [点击访问在线版本](https://你的用户名.github.io/仓库名/)

## ✨ 主要功能

- 📖 **多书卷支持**: 支持新约各书卷的学习练习
- 🎯 **智能练习**: 5节经文分组，智能空白数量算法
- 📱 **响应式设计**: 支持桌面和移动设备
- 🔍 **经文搜索**: 快速定位和练习特定经文
- 📊 **学习统计**: 记录学习进度和答题情况

## 📚 支持的书卷

- 四福音书: 马太福音、马可福音、路加福音、约翰福音
- 保罗书信: 罗马书、哥林多前后书、加拉太书、以弗所书等
- 其他新约书卷

## 🚀 使用方法

1. 访问在线网站
2. 选择要学习的书卷
3. 开始填空练习
4. 查看答案和经文解释

## 💻 本地开发

如需完整功能（包括在线编辑），请克隆仓库到本地：

```bash
git clone https://github.com/你的用户名/仓库名.git
cd 仓库名
python3 -m http.server 8001
```

## 🔧 技术栈

- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **数据**: JSON 格式的经文数据
- **托管**: GitHub Pages

## 📄 版本信息

- 当前版本: v2.1 (GitHub Pages 静态版)
- 更新时间: {datetime.now().strftime('%Y年%m月%d日')}
- 特色: 路加福音经文已完成校验和修正

## 🤝 贡献

欢迎提交 Issues 和 Pull Requests 来改进这个项目。

## 📞 联系方式

如有问题或建议，请通过 GitHub Issues 联系。

---

*愿神的话语成为我们脚前的灯，路上的光。*
"""
    
    with open(os.path.join(release_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("  ✅ 更新 README.md")
    
    # 3. 创建 GitHub Actions 工作流（可选）
    github_dir = os.path.join(release_dir, ".github", "workflows")
    os.makedirs(github_dir, exist_ok=True)
    
    workflow_content = """name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Pages
      uses: actions/configure-pages@v3
      
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v2
      with:
        path: '.'
        
    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v2

permissions:
  contents: read
  pages: write
  id-token: write
"""
    
    with open(os.path.join(github_dir, "pages.yml"), 'w', encoding='utf-8') as f:
        f.write(workflow_content)
    print("  ✅ 创建 GitHub Actions 工作流")

def create_deployment_script(release_dir):
    """创建部署脚本"""
    print("\n🚀 创建部署脚本...")
    
    deploy_script = f"""#!/bin/bash
# GitHub Pages 部署脚本

echo "🚀 开始部署到 GitHub Pages..."

# 检查是否在正确的目录
if [ ! -f "index.html" ]; then
    echo "❌ 错误: 请在包含 index.html 的目录运行此脚本"
    exit 1
fi

# 初始化 Git 仓库
if [ ! -d ".git" ]; then
    echo "📝 初始化 Git 仓库..."
    git init
    git branch -M main
fi

# 添加所有文件
echo "📁 添加文件到 Git..."
git add .

# 提交更改
echo "💾 提交更改..."
git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')"

# 推送到 GitHub（需要先添加远程仓库）
echo "🌐 推送到 GitHub..."
echo "⚠️  请先运行以下命令添加远程仓库:"
echo "git remote add origin https://github.com/你的用户名/你的仓库名.git"
echo ""
echo "然后运行:"
echo "git push -u origin main"

echo "✅ 部署脚本准备完成!"
echo "🔗 部署成功后，网站将在以下地址可用:"
echo "https://你的用户名.github.io/你的仓库名/"
"""
    
    script_path = os.path.join(release_dir, "deploy.sh")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(deploy_script)
    
    # 设置执行权限
    os.chmod(script_path, 0o755)
    print("  ✅ 创建 deploy.sh")

def main():
    """主发布流程"""
    print("🌟 GitHub Pages 发布准备工具")
    print("=" * 40)
    
    # 1. 创建优化版本
    release_dir = create_github_optimized_version()
    
    # 2. 优化代码
    optimize_for_static_hosting(release_dir)
    
    # 3. 创建 GitHub 文件
    create_github_files(release_dir)
    
    # 4. 创建部署脚本
    create_deployment_script(release_dir)
    
    print("\n" + "=" * 40)
    print("🎉 GitHub Pages 版本准备完成!")
    print(f"📂 发布目录: {release_dir}/")
    print("\n📋 下一步操作:")
    print("1. 进入发布目录: cd " + release_dir)
    print("2. 在 GitHub 创建新仓库")
    print("3. 运行部署脚本: ./deploy.sh")
    print("4. 在 GitHub 仓库设置中启用 Pages")
    print("\n🔗 详细步骤请参考: GitHub发布指南.md")

if __name__ == "__main__":
    main()