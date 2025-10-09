#!/usr/bin/env python3
"""
一对一大字版PDF内容提取器 - 修正版
正确识别新PDF的章节结构
"""

import pdfplumber
import os
import re
import json
from pathlib import Path

def create_directories():
    """创建必要的目录"""
    Path("one2one").mkdir(exist_ok=True)
    Path("one2one/data").mkdir(exist_ok=True)

def clean_text(text):
    """清理文本，移除多余空格和换行"""
    if not text:
        return ""
    # 移除多余的空白字符，但保持段落结构
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def format_content_for_html(text):
    """格式化内容为HTML友好格式"""
    if not text:
        return ""
    
    # 分段落
    paragraphs = text.split('\n')
    formatted_paragraphs = []
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        # 检测圣经经文引用
        if re.search(r'[\u4e00-\u9fff]+书?\s*\d+[:：]\d+', para):
            formatted_paragraphs.append(f'<div class="verse-container"><div class="verse-content">{para}</div></div>')
        # 检测问题
        elif para.startswith('问题：') or para.endswith('？'):
            formatted_paragraphs.append(f'<div class="question-box"><strong>{para}</strong></div>')
        # 检测个人应用
        elif para.startswith('个人应用') or para.startswith('应用'):
            formatted_paragraphs.append(f'<div class="application-section"><h3>个人应用</h3><p>{para}</p></div>')
        # 普通段落
        else:
            formatted_paragraphs.append(f'<p>{para}</p>')
    
    return '\n'.join(formatted_paragraphs)

def extract_pdf_content():
    """提取新PDF内容"""
    pdf_file = "/Users/andyshengruilee/Documents/website/web2Lord/one2one/一对一大字版.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"❌ 找不到文件: {pdf_file}")
        return None
    
    content = {
        'preface': [],
        'steps': [],
        'lessons': {}
    }
    
    with pdfplumber.open(pdf_file) as pdf:
        print(f"📖 开始处理新PDF文件，共 {len(pdf.pages)} 页")
        
        all_text = ""
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                all_text += f"\n=== 第{i+1}页 ===\n" + text
                print(f"📄 处理第{i+1}页...")
        
        # 分析内容结构
        sections = all_text.split('=== 第')
        current_section = 'none'
        preface_content = []
        steps_content = []
        lessons_content = {
            '1': [],  # 新起点 得救
            '2': [],  # 新主人 主权
            '3': [],  # 新方向 悔改
            '4': [],  # 新生命 洗礼
            '5': [],  # 新操练 灵修
            '6': [],  # 新关系 教会
            '7': []   # 新使命 带门徒
        }
        
        current_lesson = None
        
        for i, section in enumerate(sections):
            if i == 0:  # 跳过空的第一部分
                continue
                
            lines = section.split('\n')
            page_content = '\n'.join(lines[1:])  # 跳过页码行
            
            # 检测前言部分（页面4-7）
            if '4页' in lines[0] or '5页' in lines[0] or '6页' in lines[0] or '7页' in lines[0]:
                if '前言' in page_content:
                    current_section = 'preface'
                if current_section == 'preface':
                    preface_content.append(page_content)
                    continue
            
            # 检测开始作门徒部分（页面8-10）
            if '8页' in lines[0] or '9页' in lines[0] or '10页' in lines[0]:
                if '开始作门徒' in page_content or '五个步骤' in page_content or '步骤能够帮助' in page_content:
                    current_section = 'steps'
                if current_section == 'steps':
                    steps_content.append(page_content)
                    continue
            
            # 检测各课程开始
            lesson_titles = {
                '新起点': '1',
                '新主人': '2', 
                '新方向': '3',
                '新生命': '4',
                '新操练': '5',
                '新关系': '6',
                '新使命': '7'
            }
            
            # 检查是否是新课程开始
            for title, lesson_num in lesson_titles.items():
                if title in page_content and ('得救' in page_content or '主权' in page_content or '悔改' in page_content or 
                    '洗礼' in page_content or '灵修' in page_content or '教会' in page_content or '带门徒' in page_content):
                    current_lesson = lesson_num
                    current_section = 'lessons'
                    break
            
            # 添加内容到相应课程
            if current_section == 'lessons' and current_lesson:
                lessons_content[current_lesson].append(page_content)
        
        # 清理并保存内容
        content['preface'] = [clean_text(' '.join(preface_content))]
        content['steps'] = [clean_text(' '.join(steps_content))]
        
        for lesson_num, lesson_texts in lessons_content.items():
            if lesson_texts:  # 只保存有内容的课程
                content['lessons'][f'lesson_{lesson_num}'] = [clean_text(' '.join(lesson_texts))]
    
    return content

def create_preface_page(content):
    """生成前言页面"""
    preface_text = format_content_for_html('\n'.join(content['preface']))
    
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
        }}
        
        .page-subtitle {{
            font-size: 1.1rem;
            color: #667eea;
            font-weight: 500;
        }}
        
        .content-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 40px 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }}
        
        .story-content {{
            font-size: 1.2rem;
            line-height: 2;
            color: #2d3748;
            text-align: justify;
        }}
        
        .story-content p {{
            margin-bottom: 15px;
        }}
        
        .verse-container {{
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
        
        .question-box {{
            background: #fff5f5;
            border: 1px solid #feb2b2;
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
            color: #c53030;
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
                padding: 20px 15px;
            }}
            
            .story-content {{
                font-size: 1.1rem;
                line-height: 1.8;
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
            <div class="story-content">
                {preface_text}
            </div>
        </div>
        
        <div class="navigation">
            <a href="index.html" class="nav-btn">返回首页</a>
            <a href="steps.html" class="nav-btn">下一步：五个步骤</a>
        </div>
    </div>
</body>
</html>"""
    
    with open('one2one/preface.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 前言页面重新生成完成: one2one/preface.html")

def create_steps_page(content):
    """生成五个步骤页面"""
    steps_text = format_content_for_html('\n'.join(content['steps']))
    
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
        }}
        
        .page-subtitle {{
            font-size: 1.1rem;
            color: #667eea;
            font-weight: 500;
        }}
        
        .content-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 40px 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }}
        
        .steps-content {{
            font-size: 1.2rem;
            line-height: 2;
            color: #2d3748;
        }}
        
        .steps-content p {{
            margin-bottom: 15px;
        }}
        
        .verse-container {{
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
        
        .question-box {{
            background: #fff5f5;
            border: 1px solid #feb2b2;
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
            color: #c53030;
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
                padding: 20px 15px;
            }}
            
            .steps-content {{
                font-size: 1.1rem;
                line-height: 1.8;
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
            <div class="steps-content">
                {steps_text}
            </div>
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
    
    print(f"✅ 步骤页面重新生成完成: one2one/steps.html")

def create_lesson_pages(content):
    """生成课程页面"""
    lesson_titles = {
        '1': '新起点 - 得救',
        '2': '新主人 - 主权',
        '3': '新方向 - 悔改',
        '4': '新生命 - 洗礼',
        '5': '新操练 - 灵修',
        '6': '新关系 - 教会',
        '7': '新使命 - 带门徒'
    }
    
    for lesson_key, lesson_texts in content['lessons'].items():
        lesson_num = lesson_key.split('_')[1]
        lesson_content = format_content_for_html('\n'.join(lesson_texts))
        lesson_title = lesson_titles.get(lesson_num, f'第{lesson_num}课')
        
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
        }}
        
        .page-subtitle {{
            font-size: 1.1rem;
            color: #667eea;
            font-weight: 500;
        }}
        
        .content-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 40px 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }}
        
        .lesson-content {{
            font-size: 1.1rem;
            line-height: 1.8;
            color: #2d3748;
        }}
        
        .lesson-content p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        
        .verse-container {{
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
        
        .verse-reference {{
            font-weight: bold;
            color: #2b6cb0;
            margin-bottom: 10px;
        }}
        
        .question-box {{
            background: #fff5f5;
            border: 1px solid #feb2b2;
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
            color: #c53030;
        }}
        
        .application-section {{
            background: #f0fff4;
            border: 1px solid #9ae6b4;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
        
        .blank-input {{
            display: inline-block;
            min-width: 60px;
            border: none;
            border-bottom: 2px solid #667eea;
            background: transparent;
            text-align: center;
            font-size: inherit;
            padding: 2px 5px;
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
                padding: 20px 15px;
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
            <div class="lesson-content">
                {lesson_content}
            </div>
        </div>
        
        <div class="navigation">
            {get_navigation_buttons(int(lesson_num))}
        </div>
    </div>
</body>
</html>"""
        
        with open(f'one2one/one2one_C{lesson_num}.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 第{lesson_num}课重新生成完成: one2one/one2one_C{lesson_num}.html")

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
    print("🚀 开始从新PDF重新提取内容（修正版）...")
    
    # 创建目录
    create_directories()
    
    # 提取PDF内容
    content = extract_pdf_content()
    if not content:
        return
    
    print(f"\n📊 提取结果统计:")
    print(f"   📖 前言内容: {len(content['preface'])} 段")
    print(f"   📚 步骤内容: {len(content['steps'])} 段") 
    print(f"   📑 课程数量: {len(content['lessons'])} 课")
    
    for lesson_key in content['lessons'].keys():
        lesson_num = lesson_key.split('_')[1]
        print(f"      - 第{lesson_num}课: {len(content['lessons'][lesson_key])} 段")
    
    # 生成页面
    print(f"\n📄 重新生成网页...")
    create_preface_page(content)
    create_steps_page(content)
    create_lesson_pages(content)
    
    print(f"\n🎉 所有页面重新生成完成！")
    print(f"📋 生成的文件：")
    print(f"   📖 前言故事: one2one/preface.html")
    print(f"   📚 开始作门徒: one2one/steps.html")
    
    for i in range(1, 8):
        if os.path.exists(f'one2one/one2one_C{i}.html'):
            print(f"   📑 第{i}课: one2one/one2one_C{i}.html")

if __name__ == "__main__":
    main()