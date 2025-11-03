#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为罗马书八部曲生成动态网站
参考 one2one 的设计风格
"""

import os
import re
from pathlib import Path

def extract_romans_content(file_path):
    """提取罗马书内容并按章节组织"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 存储结构化内容
    structure = {
        'title': '《罗马书》系列 - 八部曲',
        'subtitle': '晨祷录音整理',
        'preface': [],
        'chapters': []
    }
    
    current_chapter = None
    current_content = []
    in_preface = False
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # 检测章节标题 (数字 + 空格 + 标题)
        chapter_match = re.match(r'^(\d+)\s+(.+)$', line_stripped)
        
        if line_stripped in ['前言', '序言']:
            in_preface = True
            current_content = []
            continue
        
        if chapter_match and len(line_stripped) < 30:
            # 保存前一章节
            if in_preface:
                structure['preface'] = current_content
                in_preface = False
            elif current_chapter:
                current_chapter['content'] = current_content
                structure['chapters'].append(current_chapter)
            
            # 开始新章节
            chapter_num = chapter_match.group(1)
            chapter_title = chapter_match.group(2)
            current_chapter = {
                'number': chapter_num,
                'title': chapter_title,
                'content': []
            }
            current_content = []
        elif line_stripped:
            current_content.append(line_stripped)
    
    # 保存最后一章
    if current_chapter:
        current_chapter['content'] = current_content
        structure['chapters'].append(current_chapter)
    
    return structure

def format_scripture(text):
    """
    检测并格式化经文引用
    紧凑型设计：经文和引用在同一行
    """
    # 匹配经文引用格式：(书卷名 章:节)
    scripture_pattern = r'\(([^)]+书|使徒行传|启示录|马太福音|马可福音|路加福音|约翰福音|使徒行传)\s*\d+:\d+[-\d,:]*\)'
    
    if re.search(scripture_pattern, text):
        # 将经文引用标记为特殊样式
        text = re.sub(scripture_pattern, r'<span class="verse-ref">\g<0></span>', text)
        return f'<div class="scripture-block">{text}</div>'
    
    return None

def convert_content_to_html(content_lines):
    """将内容转换为HTML"""
    html_parts = []
    i = 0
    
    while i < len(content_lines):
        line = content_lines[i].strip()
        
        if not line:
            i += 1
            continue
        
        # 尝试格式化为经文
        scripture_html = format_scripture(line)
        if scripture_html:
            html_parts.append(scripture_html)
            i += 1
            continue
        
        # 检测是否为小标题(短且有特殊标记)
        if len(line) < 40 and (line.endswith('？') or line.endswith('。') or 
                               line.startswith('一、') or line.startswith('二、') or 
                               line.startswith('三、') or line.startswith('四、')):
            html_parts.append(f'<h3 class="sub-title">{line}</h3>')
            i += 1
            continue
        
        # 普通段落
        html_parts.append(f'<p class="content-paragraph">{line}</p>')
        i += 1
    
    return '\n'.join(html_parts)

def generate_chapter_html(chapter, prev_chapter, next_chapter, output_dir):
    """生成单个章节的HTML页面"""
    chapter_num = chapter['number']
    chapter_title = chapter['title']
    content_html = convert_content_to_html(chapter['content'])
    
    # 导航按钮
    prev_btn = ''
    if prev_chapter:
        prev_num = prev_chapter['number']
        prev_btn = f'<a href="chapter_{prev_num}.html" class="nav-btn btn-secondary">← 上一章</a>'
    else:
        prev_btn = '<a href="index.html" class="nav-btn btn-secondary">← 返回首页</a>'
    
    next_btn = ''
    if next_chapter:
        next_num = next_chapter['number']
        next_btn = f'<a href="chapter_{next_num}.html" class="nav-btn btn-primary">下一章 →</a>'
    else:
        next_btn = '<span></span>'
    
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
            margin-bottom: 10px;
            font-size: 2em;
        }}

        .subtitle {{
            color: #666;
            font-size: 1.1em;
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
            padding: 12px 20px;
            margin: 15px 0;
            font-size: 1.02em;
            line-height: 1.7;
            color: #2d3748;
            font-style: italic;
            border-radius: 4px;
        }}

        .verse-ref {{
            color: #667eea;
            font-weight: 600;
            font-style: normal;
            margin-left: 8px;
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
                font-size: 1.6em;
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
                <a href="index.html">罗马书首页</a> &gt; 第{chapter_num}章
            </div>
            <h1>第{chapter_num}章 - {chapter_title}</h1>
            <p class="subtitle">《罗马书》系列 - 八部曲</p>
        </header>

        <div class="content">
            {content_html}
        </div>

        <div class="navigation">
            {prev_btn}
            {next_btn}
        </div>
    </div>
</body>
</html>'''
    
    # 保存文件
    output_file = output_dir / f'chapter_{chapter_num}.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"已生成: chapter_{chapter_num}.html")

def generate_index_html(structure, output_dir):
    """生成主页索引"""
    chapters = structure['chapters']
    
    # 生成章节卡片
    chapter_cards = []
    for chapter in chapters:
        chapter_num = chapter['number']
        chapter_title = chapter['title']
        # 获取章节简介(前100个字符)
        content_preview = ' '.join(chapter['content'][:2])[:100] + '...'
        
        card_html = f'''
            <div class="chapter-card" onclick="window.location.href='chapter_{chapter_num}.html'">
                <div class="chapter-number">第{chapter_num}章</div>
                <h3 class="chapter-title">{chapter_title}</h3>
                <p class="chapter-preview">{content_preview}</p>
                <div class="read-more">开始阅读 →</div>
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
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
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
            padding: 6px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-bottom: 15px;
        }}

        .chapter-title {{
            color: #333;
            font-size: 1.4em;
            margin-bottom: 12px;
            line-height: 1.4;
        }}

        .chapter-preview {{
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
    
    # 保存文件
    output_file = output_dir / 'index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"已生成: index.html")

def main():
    """主函数"""
    # 输入输出路径
    input_file = 'BooksofRoman/romans_content.txt'
    output_dir = Path('romans')
    
    # 创建输出目录
    output_dir.mkdir(exist_ok=True)
    
    print("正在提取罗马书内容...")
    structure = extract_romans_content(input_file)
    
    print(f"\n找到 {len(structure['chapters'])} 个章节:")
    for chapter in structure['chapters']:
        print(f"  第{chapter['number']}章: {chapter['title']}")
    
    print("\n开始生成HTML页面...")
    
    # 生成主页
    generate_index_html(structure, output_dir)
    
    # 生成各章节页面
    chapters = structure['chapters']
    for i, chapter in enumerate(chapters):
        prev_chapter = chapters[i-1] if i > 0 else None
        next_chapter = chapters[i+1] if i < len(chapters)-1 else None
        generate_chapter_html(chapter, prev_chapter, next_chapter, output_dir)
    
    print(f"\n✅ 完成! 所有文件已保存到 {output_dir}/ 目录")
    print(f"📖 共生成 {len(chapters)} 个章节页面 + 1 个主页")
    print(f"🌐 打开 {output_dir}/index.html 查看网站")

if __name__ == '__main__':
    main()
