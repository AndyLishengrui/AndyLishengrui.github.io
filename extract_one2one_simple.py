#!/usr/bin/env python3
"""
一对一门徒训练简化提取工具 - 修复版

先提取基本内容，然后逐步生成HTML页面
"""

import pdfplumber
import json
import re
import os

def extract_pdf_pages(pdf_path="一对一（大字版）.pdf"):
    """提取所有PDF页面内容"""
    print(f"🔍 开始提取PDF内容: {pdf_path}")
    
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                print(f"📄 提取第{i+1}页...")
                pages.append({
                    "page_num": i + 1,
                    "content": text.strip(),
                    "lines": [line.strip() for line in text.split('\n') if line.strip()]
                })
    
    return pages

def extract_preface(pages):
    """提取前言故事（第2-3页）"""
    print("📖 提取前言故事...")
    
    preface_lines = []
    
    # 从第2-3页提取，过滤目录内容
    for page in pages:
        if 2 <= page["page_num"] <= 3:
            skip_keywords = ['目 录', '前言', '新起点', '新主人', '新方向', '新生命', '新操练', '新关系', '新使命']
            
            for line in page["lines"]:
                if (not any(keyword in line for keyword in skip_keywords) and 
                    not line.isdigit() and 
                    len(line) > 3):
                    preface_lines.append(line)
    
    return {
        "title": "前言 - 一对一的故事",
        "content": '\n'.join(preface_lines),
        "type": "preface"
    }

def extract_steps(pages):
    """提取5个步骤（第4-5页）"""
    print("📚 提取门徒训练5个步骤...")
    
    steps_lines = []
    in_steps = False
    
    for page in pages:
        if 4 <= page["page_num"] <= 5:
            for line in page["lines"]:
                if "开始作门徒" in line:
                    in_steps = True
                    continue
                
                if in_steps and len(line) > 3 and not line.isdigit():
                    steps_lines.append(line)
    
    return {
        "title": "开始作门徒 - 五个步骤",
        "content": '\n'.join(steps_lines),
        "type": "steps"
    }

def extract_lessons(pages):
    """提取7课内容（第6页开始）"""
    print("📑 提取7课内容...")
    
    lessons = []
    chapter_keywords = {
        1: ["新起点", "得救"],
        2: ["新主人", "主权"],
        3: ["新方向", "悔改"],
        4: ["新生命", "洗礼"],
        5: ["新操练", "灵修"],
        6: ["新关系", "教会"],
        7: ["新使命", "带门徒"]
    }
    
    current_chapter = None
    content_lines = []
    
    for page in pages:
        if page["page_num"] >= 6:
            for line in page["lines"]:
                # 检查是否是新章节
                new_chapter = None
                for num, keywords in chapter_keywords.items():
                    if any(keyword in line for keyword in keywords):
                        new_chapter = num
                        break
                
                if new_chapter:
                    # 保存前一章
                    if current_chapter and content_lines:
                        lessons.append({
                            "chapter": current_chapter,
                            "title": f"第{current_chapter}课 - " + " ".join([k for k in chapter_keywords[current_chapter]]),
                            "content": '\n'.join(content_lines),
                            "type": "lesson"
                        })
                        print(f"📖 第{current_chapter}课内容提取完成")
                    
                    # 开始新章
                    current_chapter = new_chapter
                    content_lines = [line]
                elif current_chapter and len(line) > 3 and not line.isdigit():
                    content_lines.append(line)
    
    # 保存最后一章
    if current_chapter and content_lines:
        lessons.append({
            "chapter": current_chapter,
            "title": f"第{current_chapter}课 - " + " ".join([k for k in chapter_keywords[current_chapter]]),
            "content": '\n'.join(content_lines),
            "type": "lesson"
        })
        print(f"📖 第{current_chapter}课内容提取完成")
    
    return lessons

def find_verses_in_text(text):
    """在文本中查找经文引用"""
    verse_pattern = re.compile(r'([一二三约翰马太马可路加使徒行传罗马哥林多加拉太以弗所腓立比歌罗西帖撒罗尼迦提摩太提多腓利门希伯来雅各彼得犹大启示录创世记出埃及记利未记民数记申命记约书亚记士师记路得记撒母耳塞缪尔列王历代志以斯拉尼希米以斯帖约伯诗篇箴言传道书雅歌以赛亚耶利米哀歌以西结但以理何西阿约珥阿摩司俄巴底亚约拿弥迦那鸿哈巴谷西番雅哈该撒迦利亚玛拉基]+(?:福音|书|记|篇)*\\s*\\d+:\\d+(?:[-,]\\d+)*)')
    
    return verse_pattern.findall(text)

def create_fill_blanks(text, verse_refs):
    """为经文创建填空"""
    key_words = ["神", "主", "耶稣", "基督", "爱", "信", "救", "永生", "真理", "生命"]
    
    processed_verses = []
    
    for verse_ref in verse_refs[:3]:  # 最多3个经文
        # 查找经文内容
        lines = text.split('\n')
        verse_content = ""
        
        for i, line in enumerate(lines):
            if verse_ref in line:
                # 查找前后的经文内容
                for j in range(max(0, i-2), min(len(lines), i+3)):
                    if len(lines[j]) > 20 and verse_ref not in lines[j]:
                        verse_content = lines[j]
                        break
                break
        
        if verse_content:
            # 创建填空
            blanks = []
            hints = []
            result_text = verse_content
            
            for word in key_words:
                if word in verse_content and len(blanks) < 3:
                    result_text = result_text.replace(word, "___", 1)
                    blanks.append(word)
                    hints.append(word[0] + "_" * (len(word) - 1))
            
            if blanks:
                processed_verses.append({
                    "reference": verse_ref,
                    "text": result_text,
                    "blanks": blanks,
                    "hints": hints
                })
    
    return processed_verses

def generate_simple_html(data, filename):
    """生成简单的HTML页面"""
    title = data["title"]
    content = data["content"].replace('\n', '<br><br>')
    
    # 突出显示经文引用
    verse_pattern = re.compile(r'([一二三约翰马太马可路加使徒行传罗马哥林多加拉太以弗所腓立比歌罗西帖撒罗尼迦提摩太提多腓利门希伯来雅各彼得犹大启示录创世记出埃及记利未记民数记申命记约书亚记士师记路得记撒母耳塞缪尔列王历代志以斯拉尼希米以斯帖约伯诗篇箴言传道书雅歌以赛亚耶利米哀歌以西结但以理何西阿约珥阿摩司俄巴底亚约拿弥迦那鸿哈巴谷西番雅哈该撒迦利亚玛拉基]+(?:福音|书|记|篇)*\\s*\\d+:\\d+(?:[-,]\\d+)*)')
    content = verse_pattern.sub(r'<strong style="color: #2b6cb0;">\\1</strong>', content)
    
    # 查找经文并创建填空练习
    verse_refs = find_verses_in_text(data["content"])
    verses = create_fill_blanks(data["content"], verse_refs)
    
    # 生成经文练习HTML
    verses_section = ""
    if verses:
        verses_html = ""
        for i, verse in enumerate(verses):
            verse_id = f"verse_{i+1}"
            verse_input_html = verse["text"]
            
            # 替换___为输入框
            for j, blank in enumerate(verse["blanks"]):
                width = max(60, len(blank) * 12 + 20)
                input_html = f'<input type="text" class="blank-input" style="width:{width}px;" data-answer="{blank}" />'
                verse_input_html = verse_input_html.replace("___", input_html, 1)
            
            verses_html += f'''
            <div class="verse-container">
                <div class="verse-reference">{verse["reference"]}</div>
                <div class="verse-content" id="{verse_id}">
                    {verse_input_html}
                </div>
                <div class="verse-controls">
                    <button onclick="showHints('{verse_id}')" class="hint-btn">💡 提示</button>
                    <button onclick="checkAnswers('{verse_id}')" class="check-btn">✅ 检查</button>
                    <button onclick="showAnswers('{verse_id}')" class="answer-btn">📖 答案</button>
                </div>
            </div>'''
        
        verses_section = f'''
        <section class="content-section">
            <h2 class="section-title">✏️ 经文练习</h2>
            {verses_html}
        </section>'''
    
    # 导航设置
    nav_links = {
        "preface.html": {"prev": "index.html", "next": "steps.html"},
        "steps.html": {"prev": "preface.html", "next": "one2one_C1.html"},
    }
    
    # 课程页面导航
    if "chapter" in data:
        chapter_num = data["chapter"]
        prev_link = "steps.html" if chapter_num == 1 else f"one2one_C{chapter_num-1}.html"
        next_link = f"one2one_C{chapter_num+1}.html" if chapter_num < 7 else "index.html"
    else:
        prev_link = nav_links.get(filename, {}).get("prev", "index.html")
        next_link = nav_links.get(filename, {}).get("next", "index.html")
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 一对一门徒训练</title>
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
            max-width: 1000px;
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
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }}
        
        .section-title {{
            font-size: 1.5rem;
            color: #2d3748;
            margin-bottom: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .main-content {{
            font-size: 1.1rem;
            line-height: 1.9;
            color: #2d3748;
        }}
        
        .verse-container {{
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        
        .verse-reference {{
            font-weight: bold;
            color: #2b6cb0;
            margin-bottom: 10px;
            font-size: 1.1rem;
        }}
        
        .verse-content {{
            font-size: 1.1rem;
            line-height: 1.8;
            margin-bottom: 15px;
        }}
        
        .blank-input {{
            display: inline-block;
            min-width: 60px;
            border: none;
            border-bottom: 2px solid #667eea;
            background: transparent;
            text-align: center;
            font-size: 1.1rem;
            font-weight: bold;
            color: #2d3748;
            padding: 2px 8px;
            margin: 0 2px;
        }}
        
        .blank-input:focus {{
            outline: none;
            border-bottom-color: #764ba2;
            background: rgba(102, 126, 234, 0.1);
        }}
        
        .blank-input.correct {{
            border-bottom-color: #48bb78;
            background: rgba(72, 187, 120, 0.1);
        }}
        
        .blank-input.incorrect {{
            border-bottom-color: #f56565;
            background: rgba(245, 101, 101, 0.1);
        }}
        
        .verse-controls {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .verse-controls button {{
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .hint-btn {{
            background: #fbb6ce;
            color: #702459;
        }}
        
        .check-btn {{
            background: #9ae6b4;
            color: #22543d;
        }}
        
        .answer-btn {{
            background: #90cdf4;
            color: #1a365d;
        }}
        
        .verse-controls button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }}
        
        .navigation {{
            text-align: center;
            margin-top: 30px;
        }}
        
        .nav-btn {{
            background: rgba(255, 255, 255, 0.9);
            color: #2d3748;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            margin: 0 10px;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }}
        
        .nav-btn:hover {{
            background: white;
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
            
            .verse-controls {{
                justify-content: center;
            }}
            
            .nav-btn {{
                display: block;
                margin: 10px auto;
                width: 200px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="page-title">{title}</h1>
            <p class="page-subtitle">一对一门徒训练系列</p>
        </header>
        
        <section class="content-section">
            <h2 class="section-title">📖 内容</h2>
            <div class="main-content">{content}</div>
        </section>
        
        {verses_section}
        
        <div class="navigation">
            <a href="{prev_link}" class="nav-btn">⬅️ 上一页</a>
            <a href="index.html" class="nav-btn">🏠 主页</a>
            <a href="{next_link}" class="nav-btn">下一页 ➡️</a>
        </div>
    </div>
    
    <script>
        const versesData = {json.dumps(verses, ensure_ascii=False)};
        
        function showHints(verseId) {{
            const verseIndex = parseInt(verseId.split('_')[1]) - 1;
            const verse = versesData[verseIndex];
            const inputs = document.querySelectorAll(`#${{verseId}} .blank-input`);
            
            inputs.forEach((input, index) => {{
                if (verse.hints && verse.hints[index]) {{
                    input.placeholder = verse.hints[index];
                }}
            }});
            
            showMessage('💡 已显示提示', 'info');
        }}
        
        function checkAnswers(verseId) {{
            const verseIndex = parseInt(verseId.split('_')[1]) - 1;
            const verse = versesData[verseIndex];
            const inputs = document.querySelectorAll(`#${{verseId}} .blank-input`);
            let correct = 0;
            let total = inputs.length;
            
            inputs.forEach((input, index) => {{
                const userAnswer = input.value.trim();
                const correctAnswer = verse.blanks[index];
                
                input.classList.remove('correct', 'incorrect');
                
                if (userAnswer === correctAnswer) {{
                    input.classList.add('correct');
                    correct++;
                }} else if (userAnswer !== '') {{
                    input.classList.add('incorrect');
                }}
            }});
            
            const percentage = Math.round((correct / total) * 100);
            let message = `检查完成！正确率: ${{correct}}/${{total}} (${{percentage}}%)`;
            
            if (percentage === 100) {{
                showMessage('🎉 完全正确！' + message, 'success');
            }} else if (percentage >= 80) {{
                showMessage('👍 很棒！' + message, 'success');
            }} else {{
                showMessage('📚 继续努力！' + message, 'warning');
            }}
        }}
        
        function showAnswers(verseId) {{
            const verseIndex = parseInt(verseId.split('_')[1]) - 1;
            const verse = versesData[verseIndex];
            const inputs = document.querySelectorAll(`#${{verseId}} .blank-input`);
            
            inputs.forEach((input, index) => {{
                input.value = verse.blanks[index];
                input.classList.remove('incorrect');
                input.classList.add('correct');
            }});
            
            showMessage('📖 已显示所有答案', 'info');
        }}
        
        function showMessage(text, type = 'info') {{
            const messageDiv = document.createElement('div');
            messageDiv.textContent = text;
            messageDiv.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 12px 20px;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                z-index: 1000;
                ${{type === 'success' ? 'background: #48bb78;' :
                  type === 'warning' ? 'background: #ed8936;' :
                  'background: #4299e1;'}}
            `;
            
            document.body.appendChild(messageDiv);
            setTimeout(() => messageDiv.remove(), 3000);
        }}
    </script>
</body>
</html>'''
    
    return html_content

def main():
    """主函数"""
    print("🚀 开始简化提取一对一PDF内容...")
    
    # 创建目录
    os.makedirs("one2one/data", exist_ok=True)
    
    # 提取PDF页面
    pages = extract_pdf_pages()
    
    if not pages:
        print("❌ 无法提取PDF内容")
        return
    
    # 1. 提取并生成前言
    print("\n📖 1. 处理前言故事...")
    preface_data = extract_preface(pages)
    
    # 保存JSON
    with open("one2one/data/preface.json", "w", encoding="utf-8") as f:
        json.dump(preface_data, f, ensure_ascii=False, indent=2)
    
    # 生成HTML
    preface_html = generate_simple_html(preface_data, "preface.html")
    with open("one2one/preface.html", "w", encoding="utf-8") as f:
        f.write(preface_html)
    
    print(f"✅ 前言页面生成完成: one2one/preface.html")
    print(f"   内容长度: {len(preface_data['content'])} 字符")
    
    # 2. 提取并生成步骤
    print("\n📚 2. 处理5个步骤...")
    steps_data = extract_steps(pages)
    
    # 保存JSON  
    with open("one2one/data/steps.json", "w", encoding="utf-8") as f:
        json.dump(steps_data, f, ensure_ascii=False, indent=2)
    
    # 生成HTML
    steps_html = generate_simple_html(steps_data, "steps.html")
    with open("one2one/steps.html", "w", encoding="utf-8") as f:
        f.write(steps_html)
    
    print(f"✅ 步骤页面生成完成: one2one/steps.html")
    print(f"   内容长度: {len(steps_data['content'])} 字符")
    
    # 3. 提取并生成7课
    print("\n📑 3. 处理7课内容...")
    lessons = extract_lessons(pages)
    
    print(f"📚 找到 {len(lessons)} 课内容")
    
    for lesson in lessons:
        chapter_num = lesson["chapter"]
        
        # 保存JSON
        with open(f"one2one/data/chapter{chapter_num}.json", "w", encoding="utf-8") as f:
            json.dump(lesson, f, ensure_ascii=False, indent=2)
        
        # 生成HTML
        lesson_html = generate_simple_html(lesson, f"one2one_C{chapter_num}.html")
        with open(f"one2one/one2one_C{chapter_num}.html", "w", encoding="utf-8") as f:
            f.write(lesson_html)
        
        print(f"✅ 第{chapter_num}课生成完成: one2one/one2one_C{chapter_num}.html")
        print(f"   内容长度: {len(lesson['content'])} 字符")
    
    print("\n🎉 简化提取完成！")
    print("\n📋 生成的页面:")
    print("   📖 前言故事: one2one/preface.html")  
    print("   📚 五个步骤: one2one/steps.html")
    for lesson in lessons:
        print(f"   📑 第{lesson['chapter']}课: one2one/one2one_C{lesson['chapter']}.html")

if __name__ == "__main__":
    main()