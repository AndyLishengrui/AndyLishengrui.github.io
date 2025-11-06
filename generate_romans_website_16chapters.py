#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
罗马书天书八部网站生成器 - 16章完整版
生成多级结构: 主页 → 16个章节索引 → 各章节主题页面
"""

import os
import re
import json
from datetime import datetime

class RomansWebsiteGenerator:
    def __init__(self):
        self.chapters_dir = "BooksofRoman/chapters_final"
        self.output_dir = "romans_16chapters"
        self.data_dir = os.path.join(self.output_dir, "data")
        
        # 16个章节标题
        self.chapter_titles = [
            "1. 序言",
            "2. 保罗与福音", 
            "3. 保罗与罗马人",
            "4. 保罗与宣教",
            "5. 外邦人的罪",
            "6. 道德主义者的罪",
            "7. 犹太人的罪",
            "8. 全人类的属灵处境",
            "9. 人如何称义?",
            "10. 称义的结果",
            "11. 圣洁与成圣",
            "12. 成圣与律法",
            "13. 与基督一同受苦得荣耀",
            "14. 永恒的荣耀",
            "15. 圣经中的末世观",
            "16. 基督徒的盼望"
        ]
    
    def extract_topics_from_chapter(self, chapter_content, chapter_num):
        """从章节内容中提取主题"""
        topics = []
        lines = chapter_content.strip().split('\n')
        current_topic = None
        current_content = []
        
        # 主题编号模式: 数字后跟点号和空格(如"1. ")或数字后跟点和汉字
        topic_pattern = re.compile(r'^(\d+)\.\s+(.+)$')
        
        for line in lines:
            match = topic_pattern.match(line.strip())
            
            if match:
                # 保存上一个主题
                if current_topic:
                    topics.append({
                        'number': current_topic['number'],
                        'title': current_topic['title'],
                        'content': '\n'.join(current_content).strip()
                    })
                
                # 开始新主题
                topic_num = match.group(1)
                topic_title = match.group(2).strip()
                current_topic = {
                    'number': topic_num,
                    'title': topic_title
                }
                current_content = []
            else:
                # 累积内容
                if line.strip():
                    current_content.append(line)
        
        # 保存最后一个主题
        if current_topic:
            topics.append({
                'number': current_topic['number'],
                'title': current_topic['title'],
                'content': '\n'.join(current_content).strip()
            })
        
        # 如果没有找到主题,将整个章节作为一个主题
        if not topics:
            topics.append({
                'number': '1',
                'title': self.chapter_titles[chapter_num - 1].split('. ', 1)[-1],
                'content': chapter_content.strip()
            })
        
        return topics
    
    def process_inline_scripture(self, text):
        """处理内联经文标记"""
        # 替换{{inline-scripture}}标记为HTML样式
        text = re.sub(
            r'\{\{inline-scripture\}\}(.+?)\{\{/inline-scripture\}\}',
            r'<span class="inline-scripture">\1</span>',
            text,
            flags=re.DOTALL
        )
        
        # 处理新的scripture-ref标记
        text = re.sub(
            r'\{\{scripture-ref\}\}(.+?)\{\{/scripture-ref\}\}',
            r'<span class="scripture-ref">\1</span>',
            text,
            flags=re.DOTALL
        )
        
        return text
    
    def clean_preview_text(self, text):
        """清理预览文本,移除所有标记"""
        # 移除所有 {{ }} 标记
        text = re.sub(r'\{\{[^}]+\}\}', '', text)
        text = re.sub(r'\{\{/[^}]+\}\}', '', text)
        # 清理多余空格
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def is_scripture_reference(self, line):
        """判断是否为经文引用"""
        scripture_patterns = [
            r'^\{\{scripture\}\}',  # {{scripture}}标记
            r'《.+?》\d+[:：]\d+',   # 《马太福音》1:1
            r'^"[^"]{20,}"\s*$',     # 长引用(可能是经文)
        ]
        for pattern in scripture_patterns:
            if re.search(pattern, line):
                return True
        return False
    
    def convert_to_html(self, content):
        """将文本内容转换为HTML"""
        # 先处理内联经文和引用标记
        content = self.process_inline_scripture(content)
        
        lines = content.split('\n')
        html_lines = []
        in_scripture_block = False
        scripture_buffer = []
        
        for line in lines:
            stripped = line.strip()
            
            if not stripped:
                if in_scripture_block:
                    scripture_buffer.append('')
                else:
                    html_lines.append('<br>')
                continue
            
            # 检测{{scripture}}标记的经文块
            if '{{scripture}}' in stripped:
                # 提取经文内容
                scripture_content = stripped.replace('{{scripture}}', '').replace('{{/scripture}}', '')
                
                # 分离经文文本和引用
                # 模式: "经文内容" (引用) 或 经文内容 (引用)
                ref_match = re.search(r'(<span class="scripture-ref">.+?</span>)$', scripture_content)
                if ref_match:
                    reference = ref_match.group(1)
                    verse_text = scripture_content[:ref_match.start()].strip()
                    html_lines.append(f'<blockquote class="scripture-block">{verse_text}{reference}</blockquote>')
                else:
                    html_lines.append(f'<blockquote class="scripture-block">{scripture_content}</blockquote>')
                continue
            
            # 检测经文块开始(无标记的情况)
            if self.is_scripture_reference(stripped) and not in_scripture_block:
                in_scripture_block = True
                scripture_buffer = [stripped]
                continue
            
            # 经文块中
            if in_scripture_block:
                # 检测经文块结束(下一个普通段落)
                if not self.is_scripture_reference(stripped):
                    # 输出经文块
                    scripture_text = ' '.join(scripture_buffer)
                    html_lines.append(f'<blockquote class="scripture-block">{scripture_text}</blockquote>')
                    in_scripture_block = False
                    scripture_buffer = []
                    # 继续处理当前行
                else:
                    scripture_buffer.append(stripped)
                    continue
            
            # 普通段落
            html_lines.append(f'<p>{stripped}</p>')
        
        # 处理最后可能的经文块
        if in_scripture_block and scripture_buffer:
            scripture_text = ' '.join(scripture_buffer)
            html_lines.append(f'<blockquote class="scripture-block">{scripture_text}</blockquote>')
        
        return '\n'.join(html_lines)
    
    def generate_topic_page(self, chapter_num, topic, topic_index, total_topics):
        """生成单个主题页面"""
        chapter_title = self.chapter_titles[chapter_num - 1]
        
        # 导航链接
        prev_link = ''
        next_link = ''
        
        if topic_index > 0:
            prev_link = f'<a href="topic_{topic_index}.html" class="nav-btn">← 上一主题</a>'
        else:
            prev_link = f'<a href="chapter_{chapter_num:02d}.html" class="nav-btn">← 返回章节</a>'
        
        if topic_index < total_topics - 1:
            next_link = f'<a href="topic_{topic_index + 2}.html" class="nav-btn">下一主题 →</a>'
        else:
            if chapter_num < 16:
                next_link = f'<a href="../chapter_{chapter_num + 1:02d}/chapter_{chapter_num + 1:02d}.html" class="nav-btn">下一章 →</a>'
            else:
                next_link = f'<a href="../index.html" class="nav-btn">返回主页 →</a>'
        
        html_content = self.convert_to_html(topic['content'])
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic['title']} - {chapter_title} - 罗马书天书八部</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            line-height: 1.8;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 3px solid #667eea;
        }}
        
        .breadcrumb {{
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
        }}
        
        .breadcrumb a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        .breadcrumb a:hover {{
            text-decoration: underline;
        }}
        
        h1 {{
            color: #2c3e50;
            font-size: 2em;
            margin-bottom: 10px;
        }}
        
        .chapter-info {{
            color: #7f8c8d;
            font-size: 1.1em;
        }}
        
        .content {{
            margin: 30px 0;
        }}
        
        .content p {{
            margin-bottom: 20px;
            text-align: justify;
            text-indent: 2em;
        }}
        
        .content br {{
            display: block;
            content: "";
            margin: 10px 0;
        }}
        
        .scripture-block {{
            background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
            border-left: 5px solid #ffa726;
            border-right: 5px solid #ffa726;
            padding: 25px 30px;
            margin: 30px 0;
            border-radius: 12px;
            font-style: italic;
            color: #e65100;
            line-height: 2;
            box-shadow: 0 4px 15px rgba(255, 167, 38, 0.2);
            position: relative;
            font-size: 1.05em;
        }}
        
        .scripture-block::before {{
            content: '"';
            position: absolute;
            left: 10px;
            top: 5px;
            font-size: 3em;
            color: #ffb74d;
            opacity: 0.3;
            font-family: Georgia, serif;
        }}
        
        .scripture-block::after {{
            content: '"';
            position: absolute;
            right: 10px;
            bottom: -10px;
            font-size: 3em;
            color: #ffb74d;
            opacity: 0.3;
            font-family: Georgia, serif;
        }}
        
        .scripture-ref {{
            display: inline;
            color: #9c27b0;
            font-size: 0.95em;
            font-weight: 600;
            font-style: italic;
            background: linear-gradient(120deg, #f3e5f5 0%, #e1bee7 100%);
            padding: 2px 8px;
            border-radius: 4px;
            margin: 0 3px;
        }}
        
        .inline-scripture {{
            color: #9c27b0;
            font-weight: 500;
            background: linear-gradient(120deg, #f3e5f5 0%, #e1bee7 100%);
            padding: 3px 8px;
            border-radius: 5px;
            border-bottom: 2px solid #ab47bc;
        }}
        
        .navigation {{
            display: flex;
            justify-content: space-between;
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #ecf0f1;
        }}
        
        .nav-btn {{
            display: inline-block;
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 600;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .nav-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 1.5em;
            }}
            
            .navigation {{
                flex-direction: column;
                gap: 15px;
            }}
            
            .nav-btn {{
                text-align: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="breadcrumb">
                <a href="../index.html">主页</a> / 
                <a href="chapter_{chapter_num:02d}.html">{chapter_title}</a> / 
                主题 {topic['number']}
            </div>
            <h1>{topic['title']}</h1>
            <div class="chapter-info">{chapter_title}</div>
        </div>
        
        <div class="content">
            {html_content}
        </div>
        
        <div class="navigation">
            <div>{prev_link}</div>
            <div>{next_link}</div>
        </div>
    </div>
</body>
</html>'''
        
        return html
    
    def generate_chapter_index(self, chapter_num, topics):
        """生成章节索引页"""
        chapter_title = self.chapter_titles[chapter_num - 1]
        
        # 生成主题卡片
        topic_cards = []
        for idx, topic in enumerate(topics, 1):
            # 清理预览文本
            preview_text = self.clean_preview_text(topic['content'][:150])
            topic_cards.append(f'''
            <a href="topic_{idx}.html" class="topic-card">
                <div class="topic-number">{topic['number']}</div>
                <div class="topic-title">{topic['title']}</div>
                <div class="topic-preview">{preview_text}...</div>
            </a>''')
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{chapter_title} - 罗马书天书八部</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}
        
        .breadcrumb {{
            font-size: 14px;
            margin-bottom: 10px;
            opacity: 0.9;
        }}
        
        .breadcrumb a {{
            color: white;
            text-decoration: none;
        }}
        
        .breadcrumb a:hover {{
            text-decoration: underline;
        }}
        
        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        
        .subtitle {{
            font-size: 1.2em;
            opacity: 0.95;
        }}
        
        .topics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .topic-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            text-decoration: none;
            color: #333;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            display: block;
        }}
        
        .topic-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}
        
        .topic-number {{
            display: inline-block;
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 50%;
            text-align: center;
            line-height: 40px;
            font-weight: bold;
            margin-bottom: 15px;
        }}
        
        .topic-title {{
            font-size: 1.3em;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        
        .topic-preview {{
            color: #7f8c8d;
            font-size: 0.95em;
            line-height: 1.6;
        }}
        
        .nav-footer {{
            display: flex;
            justify-content: space-between;
            max-width: 600px;
            margin: 0 auto;
        }}
        
        .nav-btn {{
            display: inline-block;
            padding: 15px 30px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 30px;
            font-weight: 600;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 5px 20px rgba(255,255,255,0.3);
        }}
        
        .nav-btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(255,255,255,0.4);
        }}
        
        @media (max-width: 768px) {{
            h1 {{
                font-size: 2em;
            }}
            
            .topics-grid {{
                grid-template-columns: 1fr;
            }}
            
            .nav-footer {{
                flex-direction: column;
                gap: 15px;
            }}
            
            .nav-btn {{
                text-align: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="breadcrumb">
                <a href="../index.html">主页</a> / {chapter_title}
            </div>
            <h1>{chapter_title}</h1>
            <div class="subtitle">共 {len(topics)} 个主题</div>
        </div>
        
        <div class="topics-grid">
            {''.join(topic_cards)}
        </div>
        
        <div class="nav-footer">
            <a href="../index.html" class="nav-btn">← 返回主页</a>
            <a href="topic_1.html" class="nav-btn">开始阅读 →</a>
        </div>
    </div>
</body>
</html>'''
        
        return html
    
    def generate_main_index(self, chapter_data):
        """生成主页"""
        # 统计信息
        total_topics = sum(len(data['topics']) for data in chapter_data.values())
        
        # 生成章节卡片
        chapter_cards = []
        for chapter_num in range(1, 17):
            data = chapter_data.get(chapter_num, {})
            topics = data.get('topics', [])
            chapter_title = self.chapter_titles[chapter_num - 1]
            
            chapter_cards.append(f'''
            <a href="chapter_{chapter_num:02d}/chapter_{chapter_num:02d}.html" class="chapter-card">
                <div class="chapter-number">{chapter_num}</div>
                <div class="chapter-title">{chapter_title.split('. ', 1)[-1]}</div>
                <div class="chapter-stats">{len(topics)} 个主题</div>
            </a>''')
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>罗马书天书八部 - 16章完整版</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .hero {{
            text-align: center;
            color: white;
            margin-bottom: 60px;
        }}
        
        h1 {{
            font-size: 3.5em;
            margin-bottom: 20px;
            text-shadow: 0 4px 20px rgba(0,0,0,0.3);
            animation: fadeInDown 1s ease-out;
        }}
        
        .subtitle {{
            font-size: 1.5em;
            opacity: 0.95;
            margin-bottom: 10px;
        }}
        
        .stats {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .chapters-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 60px;
        }}
        
        .chapter-card {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            text-decoration: none;
            color: #333;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            display: block;
            position: relative;
            overflow: hidden;
        }}
        
        .chapter-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            opacity: 0;
            transition: opacity 0.3s;
        }}
        
        .chapter-card:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        }}
        
        .chapter-card:hover::before {{
            opacity: 1;
        }}
        
        .chapter-number {{
            display: inline-block;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 50%;
            text-align: center;
            line-height: 60px;
            font-size: 1.8em;
            font-weight: bold;
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .chapter-title {{
            font-size: 1.4em;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 15px;
            position: relative;
        }}
        
        .chapter-stats {{
            color: #7f8c8d;
            font-size: 0.95em;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            font-size: 0.95em;
            opacity: 0.9;
            padding: 20px;
        }}
        
        @keyframes fadeInDown {{
            from {{
                opacity: 0;
                transform: translateY(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @media (max-width: 768px) {{
            h1 {{
                font-size: 2.5em;
            }}
            
            .subtitle {{
                font-size: 1.2em;
            }}
            
            .chapters-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>📖 罗马书天书八部</h1>
            <div class="subtitle">16章完整版 | 系统性圣经研读</div>
            <div class="stats">16个章节 · {total_topics} 个主题 · 深度解析</div>
        </div>
        
        <div class="chapters-grid">
            {''.join(chapter_cards)}
        </div>
        
        <div class="footer">
            <p>© {datetime.now().year} 罗马书天书八部 | 生成于 {datetime.now().strftime("%Y年%m月%d日")}</p>
        </div>
    </div>
</body>
</html>'''
        
        return html
    
    def generate_website(self):
        """生成完整网站"""
        print("=" * 60)
        print("开始生成罗马书网站(含前言,共17章)")
        print("=" * 60)
        print()
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        chapter_data = {}
        page_count = 0
        
        # 处理每个章节(1-16章)
        for chapter_num in range(1, 17):
            chapter_file = os.path.join(self.chapters_dir, f"chapter_{chapter_num:02d}.txt")
            
            if not os.path.exists(chapter_file):
                print(f"⚠️  警告: 章节文件不存在 - {chapter_file}")
                continue
            
            print(f"处理章节 {chapter_num}: {self.chapter_titles[chapter_num - 1]}")
            
            # 读取章节内容
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取主题
            topics = self.extract_topics_from_chapter(content, chapter_num)
            print(f"  提取到 {len(topics)} 个主题")
            
            # 创建章节目录
            chapter_dir = os.path.join(self.output_dir, f"chapter_{chapter_num:02d}")
            os.makedirs(chapter_dir, exist_ok=True)
            
            # 生成章节索引页
            chapter_index_html = self.generate_chapter_index(chapter_num, topics)
            index_path = os.path.join(chapter_dir, f"chapter_{chapter_num:02d}.html")
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(chapter_index_html)
            print(f"  ✓ 生成章节索引: {index_path}")
            page_count += 1
            
            # 生成主题页面
            for idx, topic in enumerate(topics):
                topic_html = self.generate_topic_page(chapter_num, topic, idx, len(topics))
                topic_path = os.path.join(chapter_dir, f"topic_{idx + 1}.html")
                with open(topic_path, 'w', encoding='utf-8') as f:
                    f.write(topic_html)
                page_count += 1
            
            print(f"  ✓ 生成 {len(topics)} 个主题页面")
            
            # 保存章节数据
            chapter_data[chapter_num] = {
                'title': self.chapter_titles[chapter_num - 1],
                'topics': topics,
                'topic_count': len(topics)
            }
            
            print()
        
        # 生成主页
        main_index_html = self.generate_main_index(chapter_data)
        index_path = os.path.join(self.output_dir, "index.html")
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(main_index_html)
        print(f"✓ 生成主页: {index_path}")
        page_count += 1
        
        # 保存数据JSON
        json_path = os.path.join(self.data_dir, "chapters_data.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(chapter_data, f, ensure_ascii=False, indent=2)
        print(f"✓ 保存数据: {json_path}")
        
        print()
        print("=" * 60)
        print("✓ 网站生成完成!")
        print("=" * 60)
        print(f"📊 统计信息:")
        print(f"   - 章节数: 16")
        print(f"   - 主题总数: {sum(len(data['topics']) for data in chapter_data.values())}")
        print(f"   - 页面总数: {page_count}")
        print(f"   - 输出目录: {self.output_dir}/")
        print(f"   - 主页路径: {index_path}")
        print()

if __name__ == "__main__":
    generator = RomansWebsiteGenerator()
    generator.generate_website()
