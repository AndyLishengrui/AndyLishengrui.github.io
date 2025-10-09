#!/usr/bin/env python3
"""
一对一大字版PDF内容提取器 - 改进版
专门处理新的PDF格式，正确识别章节结构
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
    # 重新格式化段落
    text = re.sub(r'([。！？])\s+', r'\1\n\n', text)
    return text

def format_content_for_html(text):
    """格式化内容为HTML友好格式"""
    if not text:
        return ""
    
    # 分段落
    paragraphs = text.split('\n\n')
    formatted_paragraphs = []
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        # 检测圣经经文引用
        if re.search(r'[\u4e00-\u9fff]+书?\s*\d+[:：]\d+', para):
            formatted_paragraphs.append(f'<div class="verse-container"><div class="verse-content">{para}</div></div>')
        # 检测问题
        elif para.startswith('问题：') or '？' in para:
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
        
        # 保存提取的文本到文件进行调试
        with open('debug_pdf_content.txt', 'w', encoding='utf-8') as f:
            f.write(all_text)
        
        print("📝 已保存调试文件: debug_pdf_content.txt")
        
        # 分析内容结构
        lines = all_text.split('\n')
        current_section = 'none'
        current_lesson = None
        temp_content = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('==='):
                continue
            
            # 检测前言部分
            if '前言' in line and current_section == 'none':
                current_section = 'preface'
                continue
            
            # 检测步骤部分
            if re.search(r'带门徒的.*步骤|五个步骤', line) and current_section != 'lessons':
                if current_section == 'preface' and temp_content:
                    content['preface'] = temp_content.copy()
                    temp_content = []
                current_section = 'steps'
                continue
            
            # 检测课程开始
            lesson_match = re.search(r'第\s*([一二三四五六七1-7])\s*课', line)
            if lesson_match:
                # 保存之前的内容
                if current_section == 'steps' and temp_content:
                    content['steps'] = temp_content.copy()
                    temp_content = []
                elif current_lesson and temp_content:
                    content['lessons'][f'lesson_{current_lesson}'] = temp_content.copy()
                    temp_content = []
                
                current_section = 'lessons'
                lesson_num = lesson_match.group(1)
                current_lesson = convert_chinese_number(lesson_num)
                temp_content = [line]  # 包含标题
                continue
            
            # 添加内容到当前部分
            if line:
                temp_content.append(line)
        
        # 保存最后的内容
        if current_section == 'preface' and temp_content:
            content['preface'] = temp_content
        elif current_section == 'steps' and temp_content:
            content['steps'] = temp_content
        elif current_lesson and temp_content:
            content['lessons'][f'lesson_{current_lesson}'] = temp_content
    
    return content

def convert_chinese_number(chinese_num):
    """转换中文数字为阿拉伯数字"""
    mapping = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7,
        '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7
    }
    return mapping.get(chinese_num, 1)

def create_preface_page(content):
    """生成前言页面"""
    preface_text = format_content_for_html(' '.join(content['preface']))
    
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
    steps_text = format_content_for_html(' '.join(content['steps']))
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>五个门徒训练步骤 - 一对一门徒训练</title>
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
            <h1 class="page-title">五个门徒训练步骤</h1>
            <p class="page-subtitle">一对一门徒训练系列</p>
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
    for lesson_key, lesson_texts in content['lessons'].items():
        lesson_num = lesson_key.split('_')[1]
        lesson_content = format_content_for_html(' '.join(lesson_texts))
        
        # 提取课程标题
        first_line = lesson_texts[0] if lesson_texts else ""
        title_match = re.search(r'第\s*[一二三四五六七1-7]\s*课[：:]\s*([^\n]+)', first_line)
        lesson_title = title_match.group(1).strip() if title_match else f"第{lesson_num}课"
        
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
    print("🚀 开始从新PDF重新提取内容...")
    
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
    
    # 生成页面
    print(f"\n📄 重新生成网页...")
    create_preface_page(content)
    create_steps_page(content)
    create_lesson_pages(content)
    
    print(f"\n🎉 所有页面重新生成完成！")
    print(f"📋 生成的文件：")
    print(f"   📖 前言故事: one2one/preface.html")
    print(f"   📚 五个步骤: one2one/steps.html")
    
    for i in range(1, 8):
        if os.path.exists(f'one2one/one2one_C{i}.html'):
            print(f"   📑 第{i}课: one2one/one2one_C{i}.html")

if __name__ == "__main__":
    main()