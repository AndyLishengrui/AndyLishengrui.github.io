#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一对一门徒训练课程提取脚本 - 精确版
使用PDF位置信息精确提取段落结构
"""

import pdfplumber
import re
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

def extract_page_with_paragraphs(page):
    """从PDF页面提取文本，保持段落结构"""
    words = page.extract_words()
    
    if not words:
        return []
    
    paragraphs = []
    current_para = []
    last_y = None
    
    for word in words:
        text = word['text'].strip()
        current_y = word['top']
        
        # 如果Y坐标跳跃超过25（表示新段落）
        if last_y is not None and (current_y - last_y) > 25:
            if current_para:
                paragraphs.append(''.join(current_para))
                current_para = []
        
        current_para.append(text)
        last_y = current_y + word['height']
    
    # 添加最后一个段落
    if current_para:
        paragraphs.append(''.join(current_para))
    
    return paragraphs

def extract_all_content():
    """提取所有内容"""
    pdf_path = "one2one/一对一大字版.pdf"
    
    print("📖 开始精确解析PDF文件...")
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"总页数: {total_pages}")
        
        content = {
            'preface': [],
            'steps': [],
            'lessons': {}
        }
        
        # 提取前言（页面4-7）
        print("\n📄 提取前言...")
        for page_num in range(3, 7):
            if page_num < total_pages:
                page = pdf.pages[page_num]
                paras = extract_page_with_paragraphs(page)
                content['preface'].extend(paras)
        
        # 提取开始作门徒（页面8-10）
        print("📄 提取开始作门徒...")
        for page_num in range(7, 10):
            if page_num < total_pages:
                page = pdf.pages[page_num]
                paras = extract_page_with_paragraphs(page)
                content['steps'].extend(paras)
        
        # 提取7课
        lesson_ranges = {
            1: (10, 19),   # 第1课
            2: (20, 29),   # 第2课
            3: (30, 39),   # 第3课
            4: (40, 49),   # 第4课
            5: (50, 59),   # 第5课
            6: (60, 69),   # 第6课
            7: (70, 79)    # 第7课
        }
        
        for lesson_num, (start, end) in lesson_ranges.items():
            print(f"📑 提取第{lesson_num}课 - {LESSON_TITLES[lesson_num]}...")
            lesson_paras = []
            for page_num in range(start-1, min(end, total_pages)):
                page = pdf.pages[page_num]
                paras = extract_page_with_paragraphs(page)
                lesson_paras.extend(paras)
            content['lessons'][lesson_num] = lesson_paras
    
    return content

def clean_paragraph(para):
    """清理段落"""
    # 移除标题和页码
    if para in ['前言', '前言 - 一对一的故事', '开始作门徒', '一对一门徒训练系列']:
        return None
    if re.match(r'^\d+$', para):
        return None
    if para in LESSON_TITLES.values():
        return None
    
    return para.strip()

def generate_preface_html(paragraphs):
    """生成前言HTML"""
    # 清理段落
    cleaned_paras = [p for p in (clean_paragraph(para) for para in paragraphs) if p]
    
    # 生成HTML段落
    html_paras = '\n'.join([
        f'            <p class="content-paragraph">{para}</p>'
        for para in cleaned_paras
    ])
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>前言 - 一对一的故事 | 一对一门徒训练</title>
    <link rel="stylesheet" href="../cs/css/foundation_style.css">
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
            margin-bottom: 18px;
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
                <a href="index.html">一对一首页</a> &gt; 前言
            </div>
            <h1>前言 - 一对一的故事</h1>
            <p class="subtitle">一对一门徒训练系列</p>
        </header>

        <div class="content">
{html_paras}
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
    
    print(f"✅ 前言页面生成完成 ({len(cleaned_paras)}个段落)")

def generate_steps_html(paragraphs):
    """生成开始作门徒HTML"""
    # 清理段落
    cleaned_paras = [p for p in (clean_paragraph(para) for para in paragraphs) if p]
    
    # 生成HTML段落
    html_paras = '\n'.join([
        f'            <p class="content-paragraph">{para}</p>'
        for para in cleaned_paras
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
            margin-bottom: 18px;
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
{html_paras}
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
    
    print(f"✅ 开始作门徒页面生成完成 ({len(cleaned_paras)}个段落)")

def generate_lesson_html(lesson_num, paragraphs):
    """生成课程HTML"""
    lesson_title = LESSON_TITLES[lesson_num]
    
    # 清理和解析段落
    cleaned_paras = []
    i = 0
    while i < len(paragraphs):
        para = paragraphs[i]
        cleaned = clean_paragraph(para)
        
        # 检查是否是节标题的第一部分（如"得救"）
        if cleaned and i + 1 < len(paragraphs):
            next_para = paragraphs[i + 1]
            # 如果下一个是数字（节编号），合并它们
            if re.match(r'^\d+$', next_para.strip()):
                cleaned_paras.append(f"{cleaned}{next_para.strip()}")
                i += 2
                continue
        
        if cleaned:
            cleaned_paras.append(cleaned)
        i += 1
    
    # 将段落分组到各个节中
    sections = []
    current_section = None
    
    for para in cleaned_paras:
        # 检测节标题（如：得救1）
        section_match = re.match(r'^([一-九十\u4e00-\u9fff]{2,4})(\d+)$', para)
        if section_match:
            if current_section:
                sections.append(current_section)
            section_name = section_match.group(1)
            section_num = section_match.group(2)
            current_section = {
                'title': f"{section_name} {section_num}",
                'content': []
            }
        elif current_section:
            # 检测圣经引用
            if re.match(r'^[\u4e00-\u9fff]+书?\s*\d+:\d+', para):
                current_section['content'].append({
                    'type': 'verse_ref',
                    'text': para
                })
            # 检测问题
            elif para.startswith('问题：') or para.endswith('？'):
                current_section['content'].append({
                    'type': 'question',
                    'text': para
                })
            else:
                current_section['content'].append({
                    'type': 'paragraph',
                    'text': para
                })
    
    if current_section:
        sections.append(current_section)
    
    # 生成sections HTML
    sections_html = []
    for section in sections:
        section_html = f'            <div class="section">\n'
        section_html += f'                <h2 class="section-title">{section["title"]}</h2>\n'
        
        for item in section['content']:
            if item['type'] == 'verse_ref':
                section_html += f'                <div class="verse-ref">{item["text"]}</div>\n'
            elif item['type'] == 'question':
                section_html += f'                <div class="question-box">{item["text"]}</div>\n'
            else:
                section_html += f'                <p class="content-paragraph">{item["text"]}</p>\n'
        
        section_html += '            </div>\n'
        sections_html.append(section_html)
    
    content_html = '\n'.join(sections_html)
    
    # 导航
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
            padding-bottom: 30px;
            border-bottom: 1px solid #e0e0e0;
        }}

        .section:last-child {{
            border-bottom: none;
        }}

        .section-title {{
            color: #667eea;
            font-size: 1.4em;
            margin-bottom: 20px;
            padding-bottom: 8px;
            border-bottom: 2px solid #667eea;
            display: inline-block;
        }}

        .content-paragraph {{
            font-size: 1.05em;
            line-height: 1.9;
            margin-bottom: 16px;
            color: #333;
            text-align: justify;
        }}

        .verse-ref {{
            background: #f0f4ff;
            border-left: 4px solid #667eea;
            padding: 15px 20px;
            margin: 20px 0;
            font-size: 1.02em;
            color: #2d3748;
            font-weight: 500;
        }}

        .question-box {{
            background: #fff5f5;
            border-left: 4px solid #f56565;
            padding: 15px 20px;
            margin: 20px 0;
            font-size: 1.02em;
            color: #c53030;
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
                font-size: 1.2em;
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
    
    print(f"✅ 第{lesson_num}课页面生成完成 ({len(sections)}个节)")

def main():
    """主函数"""
    print("="*60)
    print("📚 一对一门徒训练课程提取工具 - 精确版")
    print("="*60)
    
    # 创建目录
    Path("one2one").mkdir(exist_ok=True)
    Path("one2one/data").mkdir(exist_ok=True)
    
    # 提取内容
    content = extract_all_content()
    
    print("\n" + "="*60)
    print("🎨 生成HTML页面")
    print("="*60)
    
    # 生成页面
    generate_preface_html(content['preface'])
    generate_steps_html(content['steps'])
    
    for lesson_num in range(1, 8):
        generate_lesson_html(lesson_num, content['lessons'][lesson_num])
    
    print("\n" + "="*60)
    print("🎉 所有页面生成完成！")
    print("="*60)

if __name__ == "__main__":
    main()
