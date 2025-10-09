# 圣经互动学习平台 - 系统架构文档

## 🎯 项目概述

本项目是一个前后端分离的圣经互动学习平台，支持66卷圣经书卷的在线学习，包含经文阅读、填空练习、进度跟踪等功能。

## 📁 文件结构

```
web2Lord/
├── index.html              # 主页面 - 圣经书卷导航
├── study.html              # 通用学习页面模板
├── data/                   # 数据目录
│   ├── config.json         # 系统配置文件
│   ├── romans.json         # 罗马书数据
│   ├── ephesians.json      # 以弗所书数据
│   └── [其他书卷].json     # 未来扩展的书卷数据
├── extract_data.py         # 数据提取脚本
├── romans_study.html       # 原始罗马书页面（已弃用）
└── ephesians_study.html    # 原始以弗所书页面（已弃用）
```

## 🏗️ 系统架构

### 前后端分离设计

- **前端**: 纯HTML + CSS + JavaScript，无服务器端依赖
- **数据存储**: JSON文件，通过fetch API加载
- **本地存储**: localStorage存储学习进度
- **主题系统**: CSS变量实现动态主题切换

### 数据结构设计

#### 1. 配置文件 (config.json)
```json
{
  "version": "1.0",
  "availableBooks": ["romans", "ephesians"],
  "books": {
    "romans": {
      "name": "罗马书",
      "englishName": "Romans", 
      "testament": "new",
      "category": "pauline_epistles",
      "chapters": 16,
      "color": "#e74c3c",
      "description": "保罗向罗马教会阐述因信称义的伟大真理"
    }
  }
}
```

#### 2. 书卷数据文件 (如romans.json)
```json
{
  "book": "romans",
  "name": "罗马书",
  "chapters": 16,
  "color": "#e74c3c",
  "verses": [
    {
      "chapter": 1,
      "verse": 1,
      "zh": "中文经文",
      "en": "English verse",
      "background": "可选背景信息"
    }
  ],
  "keyVerses": [
    {
      "chapter": 1,
      "verse": 16
    }
  ]
}
```

## 🚀 核心功能

### 1. 动态主题系统
- 每个书卷有独特的颜色主题
- CSS变量动态设置，无需重新加载页面
- 自动计算辅助色调

### 2. 智能填空练习
- 从每章的金句中随机生成填空题
- 自动选择合适的填空位置（避开标点符号）
- 智能答案检查（不区分大小写）
- 实时视觉反馈

### 3. 进度跟踪系统
- 基于localStorage的本地进度保存
- 按章节和书卷统计学习进度
- 持久化存储，刷新页面不丢失

### 4. 响应式设计
- 完全适配移动端和桌面端
- 灵活的网格布局系统
- 优雅的动画和过渡效果

## 📊 扩容架构

### 如何添加新书卷

1. **创建数据文件**
   ```bash
   # 创建新书卷的JSON文件
   cp data/romans.json data/新书卷.json
   # 编辑内容，更新书卷信息和经文数据
   ```

2. **更新配置文件**
   ```json
   {
     "availableBooks": ["romans", "ephesians", "新书卷"],
     "books": {
       "新书卷": {
         "name": "新书卷名称",
         "englishName": "English Name",
         "color": "#颜色代码"
       }
     }
   }
   ```

3. **更新主页链接**
   ```html
   <a href="study.html?book=新书卷" class="book-item available">
     新书卷名称<span class="status">✓ 可学习</span>
   </a>
   ```

### 数据提取工具

`extract_data.py` 脚本可以从现有HTML文件提取经文数据：

```python
python3 extract_data.py
# 自动提取romans_study.html和ephesians_study.html的数据
# 生成对应的JSON文件
```

## 🛠️ 技术特性

### 性能优化
- 按需加载：只加载当前需要的书卷数据
- 缓存机制：浏览器自动缓存JSON文件
- 轻量级：无外部依赖，纯原生技术栈

### 安全性
- 纯前端应用，无服务器端安全风险
- 本地数据存储，隐私保护
- XSS防护：经文内容转义处理

### 可维护性
- 模块化设计：数据、样式、逻辑分离
- 统一的数据格式和API接口
- 详细的错误处理和用户反馈

## 🔧 部署说明

### 本地开发
```bash
# 启动HTTP服务器
python3 -m http.server 8080
# 访问 http://localhost:8080
```

### 生产部署
- 上传所有文件到Web服务器
- 无需数据库或服务器端程序
- 支持GitHub Pages、Netlify等静态托管

## 📈 未来规划

### 短期目标
- [ ] 添加更多新约书卷（哥林多前后书、加拉太书等）
- [ ] 实现书签功能
- [ ] 添加搜索功能

### 中期目标  
- [ ] 添加旧约书卷
- [ ] 多语言支持
- [ ] 音频朗读功能

### 长期目标
- [ ] 用户账户系统
- [ ] 云端进度同步
- [ ] 社区分享功能

## 💡 技术亮点

1. **零依赖**: 不使用任何第三方框架或库
2. **高扩展性**: 通过配置文件轻松添加新书卷
3. **优雅设计**: 现代化的UI/UX设计
4. **智能填空**: 基于语言学规则的自动填空生成
5. **主题系统**: 每书卷独特的视觉主题
6. **进度统计**: 详细的学习进度追踪

## 📞 联系信息

项目地址: `/Users/andyshengruilee/Documents/website/web2Lord/`  
技术栈: HTML5 + CSS3 + JavaScript + JSON  
许可证: 为了神的荣耀而建 🙏