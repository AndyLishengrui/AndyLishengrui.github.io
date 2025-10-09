#!/usr/bin/env python3
"""
最终版一对一PDF内容提取器
按照用户要求提取三个部分：
1. 前言故事 (pages 2-3)
2. 五个门徒训练步骤 (pages 4-5)
3. 七课一对一内容 (page 6+)
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
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def extract_pdf_content():
    """提取PDF内容"""
    pdf_file = "一对一（大字版）.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"❌ 找不到文件: {pdf_file}")
        return None
    
    content = {
        'preface': [],
        'steps': [],
        'lessons': {}
    }
    
    with pdfplumber.open(pdf_file) as pdf:
        print(f"📖 开始处理PDF文件，共 {len(pdf.pages)} 页")
        
        # 前言 - 页面 2-3
        print("📖 提取前言故事...")
        for page_num in [1, 2]:  # PDF页面从0开始
            if page_num < len(pdf.pages):
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text:
                    content['preface'].append(clean_text(text))
        
        # 五个步骤 - 页面 4-5
        print("📚 提取五个门徒训练步骤...")
        for page_num in [3, 4]:  # PDF页面从0开始
            if page_num < len(pdf.pages):
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text:
                    content['steps'].append(clean_text(text))
        
        # 七课内容 - 页面 6+
        print("📑 提取七课内容...")
        lesson_pages = []
        for page_num in range(5, len(pdf.pages)):  # 从第6页开始
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                lesson_pages.append(clean_text(text))
        
        # 按课程分组
        current_lesson = 1
        lesson_content = []
        
        for text in lesson_pages:
            # 检测课程标题
            lesson_match = re.search(r'第\s*([一二三四五六七1-7])\s*课', text)
            if lesson_match:
                # 保存之前的课程
                if lesson_content and current_lesson <= 7:
                    content['lessons'][f'lesson_{current_lesson}'] = lesson_content
                    lesson_content = []
                
                # 开始新课程
                lesson_num = lesson_match.group(1)
                if lesson_num in ['一', '1']:
                    current_lesson = 1
                elif lesson_num in ['二', '2']:
                    current_lesson = 2
                elif lesson_num in ['三', '3']:
                    current_lesson = 3
                elif lesson_num in ['四', '4']:
                    current_lesson = 4
                elif lesson_num in ['五', '5']:
                    current_lesson = 5
                elif lesson_num in ['六', '6']:
                    current_lesson = 6
                elif lesson_num in ['七', '7']:
                    current_lesson = 7
            
            lesson_content.append(text)
        
        # 保存最后一课
        if lesson_content and current_lesson <= 7:
            content['lessons'][f'lesson_{current_lesson}'] = lesson_content
    
    return content

def create_preface_page(content):
    """生成前言页面"""
    preface_text = ' '.join(content['preface'])
    
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
    
    print(f"✅ 前言页面生成完成: one2one/preface.html")

def create_steps_page(content):
    """生成五个步骤页面"""
    steps_text = ' '.join(content['steps'])
    
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
    
    print(f"✅ 步骤页面生成完成: one2one/steps.html")

def create_lesson_pages(content):
    """生成课程页面"""
    for lesson_key, lesson_texts in content['lessons'].items():
        lesson_num = lesson_key.split('_')[1]
        lesson_content = ' '.join(lesson_texts)
        
        # 提取课程标题
        title_match = re.search(r'第\s*[一二三四五六七1-7]\s*课\s*([^\n]+)', lesson_content)
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
        
        print(f"✅ 第{lesson_num}课生成完成: one2one/one2one_C{lesson_num}.html")

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

def update_index_page():
    """更新首页，添加一对一门徒训练的导航"""
    index_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>一对一门徒训练 - 目录</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Microsoft YaHei', 'SimSun', Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            padding: 30px 20px;
            margin-bottom: 30px;
        }
        
        .page-title {
            font-size: 2.5rem;
            color: #2d3748;
            margin-bottom: 10px;
        }
        
        .page-subtitle {
            font-size: 1.2rem;
            color: #667eea;
            font-weight: 500;
        }
        
        .section {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        
        .section-title {
            font-size: 1.5rem;
            color: #2d3748;
            margin-bottom: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .nav-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .nav-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 20px;
            border-radius: 10px;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: block;
            text-align: center;
        }
        
        .nav-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        .intro-text {
            font-size: 1.1rem;
            color: #4a5568;
            margin-bottom: 20px;
            line-height: 1.8;
        }
        
        @media (max-width: 768px) {
            .page-title {
                font-size: 2rem;
            }
            
            .nav-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="page-title">一对一门徒训练</h1>
            <p class="page-subtitle">跟随耶稣，带领门徒</p>
        </div>
        
        <div class="section">
            <h2 class="section-title">📖 开始学习</h2>
            <p class="intro-text">
                一对一门徒训练是基于圣经的个人跟进和门徒培养系统。通过系统的学习和实践，
                帮助每一位基督徒成长为成熟的门徒，并学会带领其他人跟随耶稣。
            </p>
            <div class="nav-grid">
                <a href="preface.html" class="nav-btn">📚 前言：一对一的故事</a>
                <a href="steps.html" class="nav-btn">🎯 五个门徒训练步骤</a>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">📑 七课内容</h2>
            <p class="intro-text">
                系统性的七课门徒训练内容，每课都包含圣经学习、实践练习和生活应用。
            </p>
            <div class="nav-grid">
                <a href="one2one_C1.html" class="nav-btn">第一课：新起点</a>
                <a href="one2one_C2.html" class="nav-btn">第二课：新生命</a>
                <a href="one2one_C3.html" class="nav-btn">第三课：新关系</a>
                <a href="one2one_C4.html" class="nav-btn">第四课：新身份</a>
                <a href="one2one_C5.html" class="nav-btn">第五课：新目标</a>
                <a href="one2one_C6.html" class="nav-btn">第六课：新能力</a>
                <a href="one2one_C7.html" class="nav-btn">第七课：新使命</a>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">🔗 相关资源</h2>
            <div class="nav-grid">
                <a href="../foundation/" class="nav-btn">🏗️ 建立根基课程</a>
                <a href="../bible-study/" class="nav-btn">📖 圣经研读</a>
                <a href="../index.html" class="nav-btn">🏠 返回主站</a>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    with open('one2one/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print("✅ 首页更新完成: one2one/index.html")

def main():
    """主函数"""
    print("🚀 开始最终版PDF提取和页面生成...")
    
    # 创建目录
    create_directories()
    
    # 提取PDF内容
    content = extract_pdf_content()
    if not content:
        return
    
    # 生成页面
    print("\n📄 生成网页...")
    create_preface_page(content)
    create_steps_page(content)
    create_lesson_pages(content)
    update_index_page()
    
    print(f"\n🎉 所有页面生成完成！")
    print(f"📋 生成的文件：")
    print(f"   📖 前言故事: one2one/preface.html")
    print(f"   📚 五个步骤: one2one/steps.html")
    print(f"   📑 首页导航: one2one/index.html")
    
    for i in range(1, 8):
        if os.path.exists(f'one2one/one2one_C{i}.html'):
            print(f"   📑 第{i}课: one2one/one2one_C{i}.html")

if __name__ == "__main__":
    main()