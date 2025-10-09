#!/bin/bash
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
