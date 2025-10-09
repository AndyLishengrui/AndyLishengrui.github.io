#!/bin/bash
# 圣经学习网站 - 一键发布到 GitHub Pages 脚本

echo "🌟 圣经学习网站 GitHub Pages 一键发布工具"
echo "=================================================="

# 检查是否在发布目录
if [ ! -f "index.html" ]; then
    echo "❌ 请先切换到 github_release 目录:"
    echo "cd github_release"
    exit 1
fi

echo "📋 发布步骤:"
echo "1. 在 GitHub 上创建新仓库"
echo "2. 配置 Git 并上传代码"
echo "3. 启用 GitHub Pages"
echo ""

# 获取用户输入
read -p "🔗 请输入你的 GitHub 用户名: " USERNAME
read -p "📚 请输入仓库名 (建议: bible-study-website): " REPO_NAME

if [ -z "$USERNAME" ] || [ -z "$REPO_NAME" ]; then
    echo "❌ 用户名和仓库名不能为空"
    exit 1
fi

echo ""
echo "🚀 开始发布到 GitHub..."

# 初始化 Git
echo "1️⃣ 初始化 Git 仓库..."
git init

# 配置 Git（如果需要）
echo "2️⃣ 检查 Git 配置..."
if ! git config user.name > /dev/null 2>&1; then
    read -p "📝 请输入你的 Git 用户名: " GIT_USERNAME
    git config user.name "$GIT_USERNAME"
fi

if ! git config user.email > /dev/null 2>&1; then
    read -p "📧 请输入你的 Git 邮箱: " GIT_EMAIL
    git config user.email "$GIT_EMAIL"
fi

# 添加文件
echo "3️⃣ 添加文件到 Git..."
git add .

# 提交
echo "4️⃣ 提交更改..."
git commit -m "Initial commit: Bible study website for GitHub Pages"

# 设置默认分支
echo "5️⃣ 设置主分支..."
git branch -M main

# 添加远程仓库
echo "6️⃣ 添加 GitHub 远程仓库..."
REPO_URL="https://github.com/$USERNAME/$REPO_NAME.git"
git remote add origin "$REPO_URL"

# 推送到 GitHub
echo "7️⃣ 推送到 GitHub..."
echo "⚠️  如果这是第一次推送，可能需要输入 GitHub 用户名和密码/token"
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 代码上传成功!"
    echo ""
    echo "📋 现在需要在 GitHub 上启用 Pages:"
    echo "1. 访问: https://github.com/$USERNAME/$REPO_NAME"
    echo "2. 点击 'Settings' 选项卡"
    echo "3. 在左侧菜单找到 'Pages'"
    echo "4. Source 选择 'Deploy from a branch'"
    echo "5. 分支选择 'main'，文件夹选择 '/ (root)'"
    echo "6. 点击 'Save'"
    echo ""
    echo "🌐 网站将在以下地址可用:"
    echo "https://$USERNAME.github.io/$REPO_NAME/"
    echo ""
    echo "⏰ 首次部署可能需要几分钟时间"
else
    echo ""
    echo "❌ 推送失败，请检查:"
    echo "1. GitHub 仓库是否已创建"
    echo "2. 用户名和仓库名是否正确"
    echo "3. 是否有推送权限"
    echo ""
    echo "💡 你也可以手动执行以下命令:"
    echo "git remote set-url origin $REPO_URL"
    echo "git push -u origin main"
fi