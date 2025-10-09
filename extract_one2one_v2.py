#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一对一门徒训练课程提取脚本 - 参考根基课程提取方法
从PDF中提取完整的课程内容，保持段落格式和结构
"""

import pdfplumber
import re
import json
from pathlib import Path

# 7课的准确标题
LESSON_TITLES = {
    1: "新起点",
    2: "新主人", 
    3: "新方向",
    4: "新生命",
    5: "新操练",
    6: "新关系",
    7: "新使命"
}

def extract_pdf_text_with_structure():
    """从PDF中提取文本，保持段落结构"""
    
    pdf_path = "one2one/一对一大字版.pdf"
    
    print("📖 开始解析一对一PDF文件...")
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"总页数: {total_pages}")
        
        all_content = {
            'preface': [],
            'steps': [],
            'lessons': {}
        }
        
        # 提取前言（页面4-7）
        print("\n📄 提取前言部分...")
        for page_num in range(3, 7):
            if page_num < total_pages:
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text:
                    # 按行分割，保留段落
                    lines = text.split('\n')
                    all_content['preface'].extend(lines)
        
        # 提取开始作门徒部分（页面8-10）
        print("📄 提取开始作门徒部分...")
        for page_num in range(7, 10):
            if page_num < total_pages:
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text:
                    lines = text.split('\n')
                    all_content['steps'].extend(lines)
        
        # 提取各课内容
        lesson_page_ranges = {
            1: (10, 19),   # 第1课：新起点
            2: (20, 29),   # 第2课：新主人
            3: (30, 39),   # 第3课：新方向
            4: (40, 49),   # 第4课：新生命
            5: (50, 59),   # 第5课：新操练
            6: (60, 69),   # 第6课：新关系
            7: (70, 79)    # 第7课：新使命
        }
        
        for lesson_num, (start_page, end_page) in lesson_page_ranges.items():
            print(f"📑 提取第{lesson_num}课: {LESSON_TITLES[lesson_num]}...")
            
            lesson_lines = []
            for page_num in range(start_page - 1, min(end_page, total_pages)):
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text:
                    lines = text.split('\n')
                    lesson_lines.extend(lines)
            
            all_content['lessons'][lesson_num] = lesson_lines
    
    return all_content

def clean_lines(lines):
    """清理文本行，移除页眉页脚等"""
    cleaned = []
    for line in lines:
        line = line.strip()
        
        # 跳过空行
        if not line:
            continue
        
        # 跳过页码
        if re.match(r'^\d+$', line):
            continue
        
        # 跳过单独的标题（这些会在HTML中重新添加）
        if line in ['前言', '前言 - 一对一的故事', '开始作门徒', '一对一门徒训练系列']:
            continue
        
        # 跳过重复的课程标题（单独一行）
        if line in LESSON_TITLES.values():
            continue
        
        cleaned.append(line)
    
    return cleaned

def parse_lesson_content(lines):
    """解析课程内容，提取结构化信息"""
    
    content = {
        'sections': []
    }
    
    current_section = None
    current_paragraph = []
    
    for line in lines:
        line = line.strip()
        
        if not line:
            # 空行表示段落结束
            if current_paragraph and current_section:
                para_text = ' '.join(current_paragraph)
                current_section['paragraphs'].append(para_text)
                current_paragraph = []
            continue
        
        # 检测节标题（如：得救 1）
        section_match = re.match(r'^([一-九十\u4e00-\u9fff]{2,4})\s+(\d+)$', line)
        if section_match:
            # 保存上一节
            if current_section:
                if current_paragraph:
                    para_text = ' '.join(current_paragraph)
                    current_section['paragraphs'].append(para_text)
                    current_paragraph = []
                content['sections'].append(current_section)
            
            # 开始新节
            current_section = {
                'title': line,
                'paragraphs': [],
                'questions': []
            }
            continue
        
        # 检测问题（以"问题："开头或以"？"结尾）
        if line.startswith('问题：') or line.endswith('？'):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                if current_section:
                    current_section['paragraphs'].append(para_text)
                current_paragraph = []
            
            if current_section:
                current_section['questions'].append(line)
            continue
        
        # 检测圣经引用（如：约翰福音 3:16）
        if re.match(r'^[\u4e00-\u9fff]+书?\s*\d+:\d+', line):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                if current_section:
                    current_section['paragraphs'].append(para_text)
                current_paragraph = []
            
            if current_section:
                current_section['paragraphs'].append(f"<verse>{line}</verse>")
            continue
        
        # 普通文本
        current_paragraph.append(line)
    
    # 保存最后一节
    if current_section:
        if current_paragraph:
            para_text = ' '.join(current_paragraph)
            current_section['paragraphs'].append(para_text)
        content['sections'].append(current_section)
    
    return content

def generate_html_preface(content):
    """生成前言HTML页面"""
    
    lines = clean_lines(content['preface'])
    
    # 将行组合成段落
    paragraphs = []
    current_para = []
    
    for line in lines:
        if line:
            current_para.append(line)
        else:
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
    
    if current_para:
        paragraphs.append(' '.join(current_para))
    
    # 生成HTML段落
    html_paragraphs = '\n'.join([
        f'            <p class="content-paragraph">{para}</p>'
        for para in paragraphs
    ])
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>前言 - 一对一的故事 | 一对一门徒训练</title>
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
            margin-bottom: 20px;
            color: #333;
            text-align: justify;
            text-indent: 2em;
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
                <a href="index.html">一对一首页</a> &gt; 前言
            </div>
            <h1>前言 - 一对一的故事</h1>
            <p class="subtitle">一对一门徒训练系列</p>
        </header>

        <div class="content">
{html_paragraphs}
        </div>

        <div class="navigation">
            <a href="index.html" class="nav-btn btn-secondary">返回首页</a>
            <a href="steps.html" class="nav-btn btn-primary">下一步：开始作门徒 →</a>
        </div>
    </div>
</body>
</html>"""
    
    with open('one2one/preface.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ 前言页面生成完成")

def generate_html_steps(content):
    """生成开始作门徒HTML页面"""
    
    lines = clean_lines(content['steps'])
    
    # 将行组合成段落
    paragraphs = []
    current_para = []
    
    for line in lines:
        if line:
            current_para.append(line)
        else:
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
    
    if current_para:
        paragraphs.append(' '.join(current_para))
    
    # 生成HTML段落
    html_paragraphs = '\n'.join([
        f'            <p class="content-paragraph">{para}</p>'
        for para in paragraphs
    ])
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>开始作门徒 | 一对一门徒训练</title>
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
            margin-bottom: 20px;
            color: #333;
            text-align: justify;
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
                <a href="index.html">一对一首页</a> &gt; 开始作门徒
            </div>
            <h1>开始作门徒</h1>
            <p class="subtitle">五个重要步骤</p>
        </header>

        <div class="content">
{html_paragraphs}
        </div>

        <div class="navigation">
            <a href="preface.html" class="nav-btn btn-secondary">← 上一步：前言</a>
            <a href="one2one_C1.html" class="nav-btn btn-primary">开始第一课 →</a>
        </div>
    </div>
</body>
</html>"""
    
    with open('one2one/steps.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ 开始作门徒页面生成完成")

def generate_html_lesson(lesson_num, content):
    """生成课程HTML页面"""
    
    lines = clean_lines(content['lessons'][lesson_num])
    lesson_title = LESSON_TITLES[lesson_num]
    
    # 解析课程内容
    parsed_content = parse_lesson_content(lines)
    
    # 生成节的HTML
    sections_html = []
    for section in parsed_content['sections']:
        section_html = f'            <div class="section">\n'
        section_html += f'                <h2 class="section-title">{section["title"]}</h2>\n'
        
        for para in section['paragraphs']:
            if para.startswith('<verse>'):
                verse_text = para.replace('<verse>', '').replace('</verse>', '')
                section_html += f'                <div class="verse-box">{verse_text}</div>\n'
            else:
                section_html += f'                <p class="content-paragraph">{para}</p>\n'
        
        for question in section['questions']:
            section_html += f'                <div class="question-box">{question}</div>\n'
        
        section_html += '            </div>\n'
        sections_html.append(section_html)
    
    content_html = '\n'.join(sections_html)
    
    # 导航按钮
    prev_link = f'one2one_C{lesson_num-1}.html' if lesson_num > 1 else 'steps.html'
    prev_text = f'← 第{lesson_num-1}课' if lesson_num > 1 else '← 开始作门徒'
    next_link = f'one2one_C{lesson_num+1}.html' if lesson_num < 7 else 'index.html'
    next_text = f'第{lesson_num+1}课 →' if lesson_num < 7 else '返回首页'
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>第{lesson_num}课 - {lesson_title} | 一对一门徒训练</title>
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

        .section {{
            margin-bottom: 40px;
        }}

        .section-title {{
            color: #667eea;
            font-size: 1.5em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}

        .content-paragraph {{
            font-size: 1.05em;
            line-height: 1.9;
            margin-bottom: 20px;
            color: #333;
            text-align: justify;
        }}

        .verse-box {{
            background: #f0f4ff;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 25px 0;
            font-size: 1.05em;
            color: #2d3748;
            line-height: 1.8;
        }}

        .question-box {{
            background: #fff5f5;
            border-left: 4px solid #f56565;
            padding: 20px;
            margin: 20px 0;
            font-size: 1.05em;
            color: #c53030;
            line-height: 1.8;
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

            .section-title {{
                font-size: 1.3em;
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
                <a href="index.html">一对一首页</a> &gt; 第{lesson_num}课
            </div>
            <h1>第{lesson_num}课 - {lesson_title}</h1>
            <p class="subtitle">一对一门徒训练系列</p>
        </header>

        <div class="content">
{content_html}
        </div>

        <div class="navigation">
            <a href="{prev_link}" class="nav-btn btn-secondary">{prev_text}</a>
            <a href="{next_link}" class="nav-btn btn-primary">{next_text}</a>
        </div>
    </div>
</body>
</html>"""
    
    with open(f'one2one/one2one_C{lesson_num}.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 第{lesson_num}课页面生成完成")

def main():
    """主函数"""
    print("="*60)
    print("📚 一对一门徒训练课程提取工具")
    print("="*60)
    
    # 创建目录
    Path("one2one").mkdir(exist_ok=True)
    Path("one2one/data").mkdir(exist_ok=True)
    
    # 提取PDF内容
    content = extract_pdf_text_with_structure()
    
    print("\n" + "="*60)
    print("🎨 生成HTML页面")
    print("="*60)
    
    # 生成前言页面
    generate_html_preface(content)
    
    # 生成开始作门徒页面
    generate_html_steps(content)
    
    # 生成7课的页面
    for lesson_num in range(1, 8):
        generate_html_lesson(lesson_num, content)
    
    print("\n" + "="*60)
    print("🎉 所有页面生成完成！")
    print("="*60)
    print("\n📋 生成的文件清单：")
    print("   📖 前言: one2one/preface.html")
    print("   📚 开始作门徒: one2one/steps.html")
    for i in range(1, 8):
        print(f"   📑 第{i}课 - {LESSON_TITLES[i]}: one2one/one2one_C{i}.html")

if __name__ == "__main__":
    main()
