# 圣经学习网站 - GitHub 发布指南

## 📋 发布步骤总览

### 1. 准备工作
- [ ] 创建 GitHub 仓库
- [ ] 配置本地 Git
- [ ] 优化网站代码（移除Python服务器依赖）
- [ ] 上传代码到 GitHub

### 2. 配置 GitHub Pages
- [ ] 启用 GitHub Pages
- [ ] 配置自定义域名（可选）
- [ ] 测试在线访问

## 🚀 详细实施步骤

### 步骤1: 创建 GitHub 仓库

1. **登录 GitHub**: https://github.com
2. **创建新仓库**:
   - 点击右上角 "+" → "New repository"
   - 仓库名建议: `bible-study-website` 或 `web2Lord`
   - 设为 Public（公开仓库才能使用 GitHub Pages 免费版）
   - 勾选 "Add a README file"
   - 点击 "Create repository"

### 步骤2: 本地 Git 配置

```bash
# 在项目目录下初始化 Git
cd /Users/andyshengruilee/Documents/website/web2Lord
git init

# 添加 GitHub 远程仓库（替换为你的实际仓库地址）
git remote add origin https://github.com/你的用户名/bible-study-website.git

# 设置默认分支
git branch -M main

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Bible study website with Luke Gospel verification"

# 推送到 GitHub
git push -u origin main
```

### 步骤3: 网站优化（支持静态托管）

由于 GitHub Pages 是静态网站托管，我们需要：

1. **移除 Python 服务器依赖**
2. **优化文件结构**
3. **确保所有功能在静态环境下工作**

### 步骤4: 启用 GitHub Pages

1. 进入你的 GitHub 仓库页面
2. 点击 "Settings" 选项卡
3. 在左侧菜单找到 "Pages"
4. 在 "Source" 下选择 "Deploy from a branch"
5. 选择 "main" 分支，文件夹选择 "/ (root)"
6. 点击 "Save"

### 步骤5: 访问网站

GitHub Pages 会自动生成网站链接：
`https://你的用户名.github.io/仓库名/`

例如：`https://username.github.io/bible-study-website/`

## 🔧 需要的代码优化

### 1. 移除编辑功能的服务器依赖
- 将编辑功能改为前端实现
- 使用 localStorage 保存编辑结果
- 或者提供导出功能

### 2. 优化文件结构
- 确保所有资源路径正确
- 优化加载性能
- 添加移动端适配

### 3. 创建 GitHub Pages 配置文件

## 📱 移动端优化建议

为了更好的跨设备体验：
- 响应式设计优化
- 触屏操作友好
- 加载速度优化

## 🔗 自定义域名（可选）

如果你有自己的域名：
1. 在仓库根目录创建 `CNAME` 文件
2. 文件内容写入你的域名，如：`bible.yourdomain.com`
3. 在域名服务商配置 CNAME 记录指向：`你的用户名.github.io`

## ⚠️ 注意事项

1. **静态限制**: GitHub Pages 只支持静态网站，Python 服务器功能需要改为前端实现
2. **文件大小**: 单个文件不超过 100MB，整个仓库不超过 1GB
3. **访问限制**: 每月 100GB 流量，每小时 10 次构建
4. **HTTPS**: GitHub Pages 自动提供 HTTPS 支持

## 🎯 推荐的发布策略

1. **保留原始版本**: 在本地保持完整功能版本
2. **创建静态版本**: 专门为 GitHub Pages 优化的版本
3. **定期同步**: 将新功能更新到在线版本

---

是否需要我帮你创建优化后的静态版本代码？