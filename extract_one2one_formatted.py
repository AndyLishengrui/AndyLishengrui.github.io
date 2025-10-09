#!/usr/bin/env python3
"""
一对一PDF内容提取器 - 格式化版本
正确处理段落、圣经经文和页面布局
"""

import pdfplumber
import os
import re
from pathlib import Path

def create_directories():
    """创建必要的目录"""
    Path("one2one").mkdir(exist_ok=True)
    Path("one2one/data").mkdir(exist_ok=True)

def clean_and_format_text(text):
    """清理并格式化文本，保持良好的段落结构"""
    if not text:
        return ""
    
    # 移除多余空白，但保持段落结构
    text = re.sub(r'\s+', ' ', text.strip())
    
    # 处理中文标点后的段落分隔
    text = re.sub(r'([。！？])\s+', r'\1\n\n', text)
    
    # 处理圣经经文引用的格式
    text = re.sub(r'([一-九十\d]+\s*[看哪但是要知道因为神使基督]\S+.*?)([一-九十\d]+:\d+[一-九十\d]*)', r'\1\n\2', text)
    
    return text

def format_bible_verse(text):
    """格式化圣经经文"""
    # 检测圣经书卷名和章节
    verse_pattern = r'([\u4e00-\u9fff]+书?)\s*(\d+):(\d+[,-\d]*)\s*（([^）]+)）'
    if re.search(verse_pattern, text):
        return f'<div class="verse-container"><div class="verse-reference">{text}</div></div>'
    return text

def extract_pdf_content_structured():
    """结构化提取PDF内容"""
    pdf_file = "/Users/andyshengruilee/Documents/website/web2Lord/one2one/一对一大字版.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"❌ 找不到文件: {pdf_file}")
        return None
    
    content = {
        'preface': "",
        'steps': "",
        'lessons': {}
    }
    
    with pdfplumber.open(pdf_file) as pdf:
        print(f"📖 开始结构化处理PDF文件，共 {len(pdf.pages)} 页")
        
        # 提取前言部分（页面4-7）
        preface_pages = []
        for page_num in range(3, 7):  # 页面4-7
            if page_num < len(pdf.pages):
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text and '前言' in text:
                    preface_pages.append(text)
                    print(f"📄 提取前言页面 {page_num+1}")
        
        # 清理前言内容
        preface_raw = ' '.join(preface_pages)
        preface_clean = clean_and_format_text(preface_raw)
        
        # 移除页眉页脚和无关内容
        preface_clean = re.sub(r'=== 第\d+页 ===', '', preface_clean)
        preface_clean = re.sub(r'前言\s*', '', preface_clean)
        
        content['preface'] = preface_clean.strip()
        
        # 提取开始作门徒部分（页面8-10）
        steps_pages = []
        for page_num in range(7, 10):  # 页面8-10
            if page_num < len(pdf.pages):
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text:
                    steps_pages.append(text)
                    print(f"📄 提取步骤页面 {page_num+1}")
        
        steps_raw = ' '.join(steps_pages)
        steps_clean = clean_and_format_text(steps_raw)
        content['steps'] = steps_clean.strip()
        
        # 提取各课内容 - 更智能的方法
        lesson_ranges = {
            1: (10, 20),   # 第1课：新起点
            2: (21, 30),   # 第2课：新主人
            3: (31, 40),   # 第3课：新方向
            4: (41, 50),   # 第4课：新生命
            5: (51, 60),   # 第5课：新操练
            6: (61, 70),   # 第6课：新关系
            7: (71, 79)    # 第7课：新使命
        }
        
        for lesson_num, (start_page, end_page) in lesson_ranges.items():
            lesson_pages = []
            for page_num in range(start_page-1, min(end_page, len(pdf.pages))):
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text:
                    lesson_pages.append(text)
            
            if lesson_pages:
                lesson_raw = ' '.join(lesson_pages)
                lesson_clean = clean_and_format_text(lesson_raw)
                content['lessons'][f'lesson_{lesson_num}'] = lesson_clean.strip()
                print(f"📑 提取第{lesson_num}课内容")
    
    return content

def format_content_for_html(content):
    """将内容格式化为HTML"""
    if not content:
        return ""
    
    paragraphs = content.split('\n\n')
    formatted_parts = []
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        # 检测圣经经文
        if re.search(r'[\u4e00-\u9fff]+书?\s*\d+:\d+', para):
            formatted_parts.append(f'<div class="verse-container"><div class="verse-text">{para}</div></div>')
        # 检测小标题（如"得救 1"）
        elif re.search(r'^[一-九十\u4e00-\u9fff]{1,3}\s+\d+$', para):
            formatted_parts.append(f'<h3 class="section-title">{para}</h3>')
        # 检测问题
        elif para.startswith('问题：') or para.endswith('？'):
            formatted_parts.append(f'<div class="question-box">{para}</div>')
        # 检测个人应用
        elif '个人应用' in para:
            formatted_parts.append(f'<div class="application-section">{para}</div>')
        # 普通段落
        else:
            formatted_parts.append(f'<p class="content-paragraph">{para}</p>')
    
    return '\n'.join(formatted_parts)

def create_preface_page_formatted(content):
    """生成格式化的前言页面"""
    preface_html = format_content_for_html(content['preface'])
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>前言 - 一对一的故事 - 一对一门徒训练</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Microsoft YaHei', 'SimSun', Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            padding: 30px 20px;
            margin-bottom: 30px;
        }}
        
        .page-title {{
            font-size: 2.2rem;
            color: #2d3748;
            margin-bottom: 10px;
            font-weight: 600;
        }}
        
        .page-subtitle {{
            font-size: 1.1rem;
            color: #667eea;
            font-weight: 500;
        }}
        
        .content-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 40px 35px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }}
        
        .content-paragraph {{
            font-size: 1.1rem;
            line-height: 1.9;
            margin-bottom: 20px;
            color: #2d3748;
            text-align: justify;
            text-indent: 2em;
        }}
        
        .verse-container {{
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 25px;
            margin: 25px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .verse-text {{
            font-size: 1.05rem;
            color: #2b6cb0;
            font-style: italic;
            line-height: 1.7;
        }}
        
        .question-box {{
            background: #fff5f5;
            border: 1px solid #feb2b2;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            color: #c53030;
            font-weight: 500;
        }}
        
        .navigation {{
            text-align: center;
            margin: 30px 0;
        }}
        
        .nav-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 1rem;
            cursor: pointer;
            margin: 0 10px;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }}
        
        .nav-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        @media (max-width: 768px) {{
            .page-title {{
                font-size: 1.8rem;
            }}
            
            .content-section {{
                padding: 25px 20px;
            }}
            
            .content-paragraph {{
                font-size: 1rem;
                text-indent: 1.5em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="page-title">前言 - 一对一的故事</h1>
            <p class="page-subtitle">一对一门徒训练系列</p>
        </div>
        
        <div class="content-section">
            {preface_html}
        </div>
        
        <div class="navigation">
            <a href="index.html" class="nav-btn">返回首页</a>
            <a href="steps.html" class="nav-btn">下一步：开始作门徒</a>
        </div>
    </div>
</body>
</html>"""
    
    with open('one2one/preface.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 格式化前言页面生成完成: one2one/preface.html")

def create_steps_page_formatted(content):
    """生成格式化的步骤页面"""
    steps_html = format_content_for_html(content['steps'])
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>开始作门徒 - 五个步骤 - 一对一门徒训练</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Microsoft YaHei', 'SimSun', Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            padding: 30px 20px;
            margin-bottom: 30px;
        }}
        
        .page-title {{
            font-size: 2.2rem;
            color: #2d3748;
            margin-bottom: 10px;
            font-weight: 600;
        }}
        
        .page-subtitle {{
            font-size: 1.1rem;
            color: #667eea;
            font-weight: 500;
        }}
        
        .content-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 40px 35px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }}
        
        .content-paragraph {{
            font-size: 1.1rem;
            line-height: 1.9;
            margin-bottom: 20px;
            color: #2d3748;
            text-align: justify;
        }}
        
        .verse-container {{
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 25px;
            margin: 25px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .verse-text {{
            font-size: 1.05rem;
            color: #2b6cb0;
            line-height: 1.7;
            font-weight: 500;
        }}
        
        .section-title {{
            color: #4a5568;
            font-size: 1.3rem;
            margin: 25px 0 15px 0;
            font-weight: 600;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 8px;
        }}
        
        .navigation {{
            text-align: center;
            margin: 30px 0;
        }}
        
        .nav-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 1rem;
            cursor: pointer;
            margin: 0 10px;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }}
        
        .nav-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        @media (max-width: 768px) {{
            .page-title {{
                font-size: 1.8rem;
            }}
            
            .content-section {{
                padding: 25px 20px;
            }}
            
            .content-paragraph {{
                font-size: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="page-title">开始作门徒</h1>
            <p class="page-subtitle">五个重要步骤</p>
        </div>
        
        <div class="content-section">
            {steps_html}
        </div>
        
        <div class="navigation">
            <a href="preface.html" class="nav-btn">上一步：前言</a>
            <a href="one2one_C1.html" class="nav-btn">开始第一课</a>
        </div>
    </div>
</body>
</html>"""
    
    with open('one2one/steps.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 格式化步骤页面生成完成: one2one/steps.html")

def create_lesson_pages_formatted(content):
    """生成格式化的课程页面"""
    lesson_titles = {
        '1': '新起点 - 得救',
        '2': '新主人 - 主权',
        '3': '新方向 - 悔改',
        '4': '新生命 - 洗礼',
        '5': '新操练 - 灵修',
        '6': '新关系 - 教会',
        '7': '新使命 - 带门徒'
    }
    
    for lesson_key, lesson_content in content['lessons'].items():
        lesson_num = lesson_key.split('_')[1]
        lesson_title = lesson_titles.get(lesson_num, f'第{lesson_num}课')
        lesson_html = format_content_for_html(lesson_content)
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>第{lesson_num}课 - {lesson_title} - 一对一门徒训练</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Microsoft YaHei', 'SimSun', Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            padding: 30px 20px;
            margin-bottom: 30px;
        }}
        
        .page-title {{
            font-size: 2.2rem;
            color: #2d3748;
            margin-bottom: 10px;
            font-weight: 600;
        }}
        
        .page-subtitle {{
            font-size: 1.1rem;
            color: #667eea;
            font-weight: 500;
        }}
        
        .content-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 40px 35px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }}
        
        .content-paragraph {{
            font-size: 1.05rem;
            line-height: 1.8;
            margin-bottom: 18px;
            color: #2d3748;
            text-align: justify;
        }}
        
        .verse-container {{
            background: #f0f9ff;
            border: 1px solid #bae6fd;
            border-radius: 10px;
            padding: 25px;
            margin: 25px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .verse-text {{
            font-size: 1.05rem;
            color: #0369a1;
            line-height: 1.7;
            font-weight: 500;
        }}
        
        .section-title {{
            color: #1e40af;
            font-size: 1.4rem;
            margin: 30px 0 20px 0;
            font-weight: 600;
            border-bottom: 3px solid #3b82f6;
            padding-bottom: 8px;
            display: inline-block;
        }}
        
        .question-box {{
            background: #fef2f2;
            border: 1px solid #fecaca;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            color: #dc2626;
            font-weight: 500;
        }}
        
        .application-section {{
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            border-radius: 10px;
            padding: 25px;
            margin: 25px 0;
        }}
        
        .navigation {{
            text-align: center;
            margin: 30px 0;
        }}
        
        .nav-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 1rem;
            cursor: pointer;
            margin: 0 10px;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }}
        
        .nav-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        @media (max-width: 768px) {{
            .page-title {{
                font-size: 1.8rem;
            }}
            
            .content-section {{
                padding: 25px 20px;
            }}
            
            .content-paragraph {{
                font-size: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="page-title">第{lesson_num}课 - {lesson_title}</h1>
            <p class="page-subtitle">一对一门徒训练系列</p>
        </div>
        
        <div class="content-section">
            {lesson_html}
        </div>
        
        <div class="navigation">
            {get_navigation_buttons(int(lesson_num))}
        </div>
    </div>
</body>
</html>"""
        
        with open(f'one2one/one2one_C{lesson_num}.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 第{lesson_num}课格式化页面生成完成: one2one/one2one_C{lesson_num}.html")

def get_navigation_buttons(lesson_num):
    """生成导航按钮"""
    buttons = []
    
    if lesson_num > 1:
        buttons.append(f'<a href="one2one_C{lesson_num-1}.html" class="nav-btn">上一课</a>')
    else:
        buttons.append('<a href="steps.html" class="nav-btn">返回步骤</a>')
    
    buttons.append('<a href="index.html" class="nav-btn">返回首页</a>')
    
    if lesson_num < 7:
        buttons.append(f'<a href="one2one_C{lesson_num+1}.html" class="nav-btn">下一课</a>')
    
    return ' '.join(buttons)

def main():
    """主函数"""
    print("🎨 开始格式化提取PDF内容...")
    
    # 创建目录
    create_directories()
    
    # 提取并结构化内容
    content = extract_pdf_content_structured()
    if not content:
        return
    
    print(f"\n📊 提取结果统计:")
    print(f"   📖 前言字数: {len(content['preface'])} 字符")
    print(f"   📚 步骤字数: {len(content['steps'])} 字符")
    print(f"   📑 课程数量: {len(content['lessons'])} 课")
    
    # 生成格式化页面
    print(f"\n🎨 生成格式化网页...")
    create_preface_page_formatted(content)
    create_steps_page_formatted(content)
    create_lesson_pages_formatted(content)
    
    print(f"\n🎉 所有格式化页面生成完成！")
    print(f"📋 生成的文件：")
    print(f"   📖 前言故事: one2one/preface.html")
    print(f"   📚 开始作门徒: one2one/steps.html")
    
    for i in range(1, 8):
        if os.path.exists(f'one2one/one2one_C{i}.html'):
            print(f"   📑 第{i}课: one2one/one2one_C{i}.html")

if __name__ == "__main__":
    main()