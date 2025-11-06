#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
罗马书网站生成器 V2 - 增强版
- 每章细分为多个主题,每个主题独立页面
- 增强内容结构:标题层级、引用块、列表
- 紧凑型经文样式
"""

import os
import re
from pathlib import Path

def extract_romans_structure(file_path):
    """
    提取罗马书的层级结构
    - 章节(1, 2, 3...)
    - 主题(1.  主题标题, 2.  主题标题...)
    - 小标题(一、二、三...)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    structure = {
        'title': '《罗马书》系列 - 八部曲',
        'chapters': []
    }
    
    current_chapter = None
    current_topic = None
    current_content = []
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # 章节标题: 纯数字 + 空格 + 标题
        chapter_match = re.match(r'^(\d+)\s+(.+)$', line_stripped)
        if chapter_match and len(line_stripped) < 30:
            # 保存前一个主题
            if current_topic:
                current_topic['content'] = current_content
                if current_chapter:
                    current_chapter['topics'].append(current_topic)
                current_content = []
            
            # 保存前一章
            if current_chapter:
                structure['chapters'].append(current_chapter)
            
            # 新章节
            chapter_num = chapter_match.group(1)
            chapter_title = chapter_match.group(2)
            current_chapter = {
                'number': chapter_num,
                'title': chapter_title,
                'topics': []
            }
            current_topic = None
            continue
        
        # 主题标题: 数字. + 空格 + 标题
        topic_match = re.match(r'^(\d+)\.\s+(.+)$', line_stripped)
        if topic_match and len(line_stripped) < 50:
            # 保存前一个主题
            if current_topic:
                current_topic['content'] = current_content
                if current_chapter:
                    current_chapter['topics'].append(current_topic)
            
            # 新主题
            topic_num = topic_match.group(1)
            topic_title = topic_match.group(2)
            current_topic = {
                'number': topic_num,
                'title': topic_title,
                'content': []
            }
            current_content = []
            continue
        
        # 内容
        if line_stripped:
            current_content.append(line_stripped)
    
    # 保存最后一个主题和章节
    if current_topic:
        current_topic['content'] = current_content
        if current_chapter:
            current_chapter['topics'].append(current_topic)
    if current_chapter:
        structure['chapters'].append(current_chapter)
    
    return structure

def is_scripture_reference(text):
    """检测是否为经文引用"""
    # 匹配格式: (书卷名 章:节)
    scripture_pattern = r'\([^)]*(?:书|福音|行传|启示录)\s*\d+:\d+[^)]*\)'
    return bool(re.search(scripture_pattern, text))

def is_subtitle(text):
    """检测是否为小标题"""
    # 一、二、三、或者以？结尾的短文本
    return (re.match(r'^[一二三四五六七八九十]+、', text) or 
            (text.endswith('？') and len(text) < 40) or
            (text.endswith('?') and len(text) < 40))

def process_inline_scripture(text):
    """
    处理段内经文标记,将{{inline-scripture}}标记转换为HTML
    """
    # 将标记的段内经文转换为带样式的span
    def replace_inline(match):
        scripture = match.group(1)
        return f'<span class="inline-scripture">{scripture}</span>'
    
    # 替换所有标记的段内经文
    text = re.sub(r'\{\{inline-scripture\}\}(.*?)\{\{/inline-scripture\}\}', replace_inline, text)
    return text

def convert_to_html(content_lines):
    """
    将内容转换为HTML,增强结构
    """
    html_parts = []
    i = 0
    in_list = False
    
    while i < len(content_lines):
        line = content_lines[i].strip()
        
        if not line:
            i += 1
            continue
        
        # 经文引用 - 紧凑样式(独立成段的)
        if is_scripture_reference(line) and not '{{inline-scripture}}' in line:
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            
            # 分离经文内容和引用
            scripture_match = re.search(r'(.+?)(\([^)]*(?:书|福音|行传|启示录)\s*\d+:\d+[^)]*\))$', line)
            if scripture_match:
                verse_text = scripture_match.group(1).strip()
                reference = scripture_match.group(2)
                html_parts.append(f'''
                <div class="scripture-block">
                    <div class="scripture-text">{verse_text}</div>
                    <div class="scripture-ref">{reference}</div>
                </div>''')
            else:
                html_parts.append(f'<div class="scripture-block">{line}</div>')
            i += 1
            continue
        
        # 小标题
        if is_subtitle(line):
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            html_parts.append(f'<h3 class="sub-title">{line}</h3>')
            i += 1
            continue
        
        # 列表项 (以数字、或短句开头)
        if re.match(r'^[一二三四五六七八九十]+、', line):
            if not in_list:
                html_parts.append('<ul class="point-list">')
                in_list = True
            # 移除列表标记
            content = re.sub(r'^[一二三四五六七八九十]+、\s*', '', line)
            # 处理列表项中的段内经文
            content = process_inline_scripture(content)
            html_parts.append(f'<li>{content}</li>')
            i += 1
            continue
        
        # 关闭列表
        if in_list and not re.match(r'^[一二三四五六七八九十]+、', line):
            html_parts.append('</ul>')
            in_list = False
        
        # 引用块(带引号的内容)
        if line.startswith('"') or line.startswith('"'):
            line = process_inline_scripture(line)
            html_parts.append(f'<blockquote class="quote-block">{line}</blockquote>')
            i += 1
            continue
        
        # 普通段落
        line = process_inline_scripture(line)
        html_parts.append(f'<p class="content-paragraph">{line}</p>')
        i += 1
    
    if in_list:
        html_parts.append('</ul>')
    
    return '\n'.join(html_parts)

def generate_topic_html(chapter, topic, prev_link, next_link, output_dir):
    """生成单个主题页面"""
    chapter_num = chapter['number']
    chapter_title = chapter['title']
    topic_num = topic['number']
    topic_title = topic['title']
    
    content_html = convert_to_html(topic['content'])
    
    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic_title} | 罗马书八部曲</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}

        header {{
            background: white;
            border-radius: 15px 15px 0 0;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .breadcrumb {{
            color: #888;
            font-size: 0.9em;
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
            color: #333;
            margin-bottom: 5px;
            font-size: 1.8em;
        }}

        .chapter-info {{
            color: #666;
            font-size: 0.95em;
            margin-bottom: 10px;
        }}

        .content {{
            background: white;
            padding: 40px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .content-paragraph {{
            font-size: 1.05em;
            line-height: 1.9;
            margin-bottom: 16px;
            color: #333;
            text-align: justify;
        }}

        .sub-title {{
            color: #667eea;
            font-size: 1.2em;
            margin: 30px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #e8e8ff;
        }}

        /* 紧凑型经文样式 */
        .scripture-block {{
            background: linear-gradient(135deg, #f0f7ff 0%, #e8f4ff 100%);
            border-left: 4px solid #667eea;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}

        .scripture-text {{
            font-size: 1.05em;
            line-height: 1.8;
            color: #2d3748;
            font-style: italic;
            margin-bottom: 8px;
        }}

        .scripture-ref {{
            color: #667eea;
            font-weight: 600;
            font-size: 0.95em;
            text-align: right;
            font-style: normal;
        }}

        /* 段内经文样式 - 内联显示 */
        .inline-scripture {{
            color: #667eea;
            font-weight: 500;
            font-size: 0.95em;
            text-decoration: underline;
            text-decoration-color: rgba(102, 126, 234, 0.3);
            text-underline-offset: 3px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
            padding: 2px 6px;
            border-radius: 3px;
            white-space: nowrap;
        }}

        .quote-block {{
            border-left: 4px solid #fbbf24;
            padding: 15px 20px;
            margin: 20px 0;
            background: #fffbeb;
            font-style: italic;
            color: #78350f;
        }}

        .point-list {{
            margin: 20px 0 20px 30px;
            line-height: 1.8;
        }}

        .point-list li {{
            margin-bottom: 12px;
            color: #333;
        }}

        .navigation {{
            background: white;
            border-radius: 0 0 15px 15px;
            padding: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .nav-btn {{
            padding: 12px 28px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s;
            font-weight: 500;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}

        .btn-secondary {{
            background: #f0f0f0;
            color: #333;
        }}

        .btn-secondary:hover {{
            background: #e0e0e0;
        }}

        @media (max-width: 768px) {{
            header, .content, .navigation {{
                padding: 20px;
            }}

            h1 {{
                font-size: 1.5em;
            }}

            .sub-title {{
                font-size: 1.1em;
            }}

            .content-paragraph {{
                font-size: 1em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="breadcrumb">
                <a href="index.html">罗马书首页</a> &gt; 
                <a href="chapter_{chapter_num}_index.html">第{chapter_num}章</a> &gt; 
                主题{topic_num}
            </div>
            <h1>{topic_title}</h1>
            <div class="chapter-info">第{chapter_num}章: {chapter_title} · 主题{topic_num}</div>
        </header>

        <div class="content">
            {content_html}
        </div>

        <div class="navigation">
            {prev_link}
            {next_link}
        </div>
    </div>
</body>
</html>'''
    
    # 保存文件
    filename = f'chapter_{chapter_num}_topic_{topic_num}.html'
    output_file = output_dir / filename
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    return filename

def generate_chapter_index(chapter, output_dir):
    """生成章节索引页(主题列表)"""
    chapter_num = chapter['number']
    chapter_title = chapter['title']
    topics = chapter['topics']
    
    # 生成主题卡片
    topic_cards = []
    for topic in topics:
        topic_num = topic['number']
        topic_title = topic['title']
        # 获取预览(前100字符)
        preview = ' '.join(topic['content'][:2])[:100] + '...' if topic['content'] else ''
        
        card_html = f'''
            <div class="topic-card" onclick="window.location.href='chapter_{chapter_num}_topic_{topic_num}.html'">
                <div class="topic-number">主题 {topic_num}</div>
                <h3 class="topic-title">{topic_title}</h3>
                <p class="topic-preview">{preview}</p>
                <div class="read-more">开始阅读 →</div>
            </div>'''
        topic_cards.append(card_html)
    
    topics_html = '\n'.join(topic_cards)
    
    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>第{chapter_num}章 - {chapter_title} | 罗马书八部曲</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            color: white;
            padding: 40px 20px;
            margin-bottom: 40px;
        }}

        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .subtitle {{
            font-size: 1.2em;
            opacity: 0.95;
        }}

        .topics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 25px;
            padding: 20px;
        }}

        .topic-card {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }}

        .topic-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }}

        .topic-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }}

        .topic-number {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 6px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-bottom: 15px;
        }}

        .topic-title {{
            color: #333;
            font-size: 1.4em;
            margin-bottom: 12px;
            line-height: 1.4;
        }}

        .topic-preview {{
            color: #666;
            font-size: 0.95em;
            line-height: 1.6;
            margin-bottom: 15px;
            max-height: 4.8em;
            overflow: hidden;
        }}

        .read-more {{
            color: #667eea;
            font-weight: 600;
            font-size: 0.9em;
            padding-top: 10px;
            border-top: 1px solid #eee;
        }}

        .back-home {{
            text-align: center;
            margin-top: 40px;
            padding-bottom: 40px;
        }}

        .back-home a {{
            display: inline-block;
            background: white;
            color: #667eea;
            padding: 15px 40px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 600;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }}

        .back-home a:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(255, 255, 255, 0.3);
        }}

        @media (max-width: 768px) {{
            h1 {{
                font-size: 2em;
            }}

            .topics-grid {{
                grid-template-columns: 1fr;
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>第{chapter_num}章 - {chapter_title}</h1>
            <p class="subtitle">{len(topics)} 个主题</p>
        </header>

        <div class="topics-grid">
            {topics_html}
        </div>

        <div class="back-home">
            <a href="index.html">← 返回章节列表</a>
        </div>
    </div>
</body>
</html>'''
    
    output_file = output_dir / f'chapter_{chapter_num}_index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

def generate_main_index(structure, output_dir):
    """生成主页"""
    chapters = structure['chapters']
    
    # 生成章节卡片
    chapter_cards = []
    for chapter in chapters:
        chapter_num = chapter['number']
        chapter_title = chapter['title']
        topic_count = len(chapter['topics'])
        
        card_html = f'''
            <div class="chapter-card" onclick="window.location.href='chapter_{chapter_num}_index.html'">
                <div class="chapter-number">第{chapter_num}章</div>
                <h3 class="chapter-title">{chapter_title}</h3>
                <p class="chapter-stats">{topic_count} 个主题</p>
                <div class="read-more">进入学习 →</div>
            </div>'''
        chapter_cards.append(card_html)
    
    chapters_html = '\n'.join(chapter_cards)
    
    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>罗马书八部曲 | 晨祷录音整理</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            color: white;
            padding: 40px 20px;
            margin-bottom: 40px;
        }}

        h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .subtitle {{
            font-size: 1.3em;
            opacity: 0.95;
            margin-bottom: 10px;
        }}

        .description {{
            font-size: 1em;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
        }}

        .chapters-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
            padding: 20px;
        }}

        .chapter-card {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }}

        .chapter-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }}

        .chapter-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }}

        .chapter-number {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            margin-bottom: 15px;
        }}

        .chapter-title {{
            color: #333;
            font-size: 1.5em;
            margin-bottom: 12px;
            line-height: 1.4;
        }}

        .chapter-stats {{
            color: #666;
            font-size: 0.95em;
            margin-bottom: 15px;
        }}

        .read-more {{
            color: #667eea;
            font-weight: 600;
            font-size: 0.95em;
            padding-top: 10px;
            border-top: 1px solid #eee;
        }}

        .back-home {{
            text-align: center;
            margin-top: 40px;
            padding-bottom: 40px;
        }}

        .back-home a {{
            display: inline-block;
            background: white;
            color: #667eea;
            padding: 15px 40px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 600;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }}

        .back-home a:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(255, 255, 255, 0.3);
        }}

        @media (max-width: 768px) {{
            h1 {{
                font-size: 2em;
            }}

            .subtitle {{
                font-size: 1.1em;
            }}

            .chapters-grid {{
                grid-template-columns: 1fr;
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>《罗马书》系列</h1>
            <p class="subtitle">八部曲 · 晨祷录音整理</p>
            <p class="description">本套罗马书解经丛书的目标不是"把罗马书给掌握了"，而是"被罗马书给掌握了"</p>
        </header>

        <div class="chapters-grid">
            {chapters_html}
        </div>

        <div class="back-home">
            <a href="../index.html">← 返回主页</a>
        </div>
    </div>
</body>
</html>'''
    
    output_file = output_dir / 'index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

def main():
    """主函数"""
    input_file = 'BooksofRoman/romans_content.txt'
    output_dir = Path('romans')
    
    # 创建输出目录
    output_dir.mkdir(exist_ok=True)
    
    print("正在提取罗马书结构...")
    structure = extract_romans_structure(input_file)
    
    print(f"\n找到 {len(structure['chapters'])} 个章节:")
    total_topics = 0
    for chapter in structure['chapters']:
        topic_count = len(chapter['topics'])
        total_topics += topic_count
        print(f"  第{chapter['number']}章: {chapter['title']} ({topic_count}个主题)")
        for topic in chapter['topics']:
            print(f"    {topic['number']}. {topic['title']}")
    
    print(f"\n总共: {total_topics} 个主题")
    print("\n开始生成HTML页面...")
    
    # 生成主页
    generate_main_index(structure, output_dir)
    print(f"✓ 已生成主页")
    
    # 生成各章节
    file_count = 0
    for chapter in structure['chapters']:
        chapter_num = chapter['number']
        
        # 生成章节索引
        generate_chapter_index(chapter, output_dir)
        file_count += 1
        
        # 生成各主题页面
        topics = chapter['topics']
        for i, topic in enumerate(topics):
            # 确定上一页和下一页链接
            if i == 0:
                prev_link = f'<a href="chapter_{chapter_num}_index.html" class="nav-btn btn-secondary">← 章节目录</a>'
            else:
                prev_topic_num = topics[i-1]['number']
                prev_link = f'<a href="chapter_{chapter_num}_topic_{prev_topic_num}.html" class="nav-btn btn-secondary">← 上一主题</a>'
            
            if i == len(topics) - 1:
                # 最后一个主题,链接到下一章或返回主页
                next_chapter_idx = int(chapter_num)
                if next_chapter_idx < len(structure['chapters']):
                    next_link = f'<a href="chapter_{int(chapter_num)+1}_index.html" class="nav-btn btn-primary">下一章 →</a>'
                else:
                    next_link = f'<a href="index.html" class="nav-btn btn-primary">返回首页 →</a>'
            else:
                next_topic_num = topics[i+1]['number']
                next_link = f'<a href="chapter_{chapter_num}_topic_{next_topic_num}.html" class="nav-btn btn-primary">下一主题 →</a>'
            
            generate_topic_html(chapter, topic, prev_link, next_link, output_dir)
            file_count += 1
        
        print(f"✓ 第{chapter_num}章完成 ({len(topics)} 个主题)")
    
    print(f"\n✅ 完成! ")
    print(f"📖 共生成 {file_count} 个页面")
    print(f"   - 1 个主页")
    print(f"   - {len(structure['chapters'])} 个章节索引页")
    print(f"   - {total_topics} 个主题内容页")
    print(f"🌐 打开 {output_dir}/index.html 查看网站")

if __name__ == '__main__':
    main()
