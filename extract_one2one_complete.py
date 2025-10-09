#!/usr/bin/env python3
"""
一对一门徒训练完整内容提取工具

按照PDF结构提取内容：
1. 前言故事（第2-3页）
2. 带门徒5个步骤（第4-5页）  
3. 7课一对一内容（第6页开始）
"""

import pdfplumber
import json
import re
import os
from typing import Dict, List, Any, Tuple

class One2OneCompleteExtractor:
    def __init__(self, pdf_path: str = "一对一（大字版）.pdf"):
        self.pdf_path = pdf_path
        self.output_dir = "one2one"
        self.data_dir = os.path.join(self.output_dir, "data")
        
        # 确保目录存在
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 经文引用正则模式
        self.verse_pattern = re.compile(r'([一二三约翰马太马可路加使徒行传罗马哥林多加拉太以弗所腓立比歌罗西帖撒罗尼迦提摩太提多腓利门希伯来雅各彼得犹大启示录创世记出埃及记利未记民数记申命记约书亚记士师记路得记撒母耳塞缪尔列王历代志以斯拉尼希米以斯帖约伯诗篇箴言传道书雅歌以赛亚耶利米哀歌以西结但以理何西阿约珥阿摩司俄巴底亚约拿弥迦那鸿哈巴谷西番雅哈该撒迦利亚玛拉基]+(?:福音|书|记|篇)*\\s*\\d+:\\d+(?:[-,]\\d+)*)', re.UNICODE)
        
    def extract_all_pages(self) -> List[Dict[str, Any]]:
        """提取所有页面内容"""
        print(f"🔍 开始提取PDF所有内容: {self.pdf_path}")
        
        pages = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    print(f"📄 提取第{i+1}页...")
                    pages.append({
                        "page_num": i + 1,
                        "content": text.strip(),
                        "lines": [line.strip() for line in text.split('\\n') if line.strip()]
                    })
        
        return pages
    
    def extract_preface_story(self, pages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """提取前言故事（第2-3页）"""
        print("📖 提取前言故事...")
        
        preface_content = []
        
        # 从第2页开始，到第4页"开始作门徒"之前
        for page in pages:
            if page["page_num"] >= 2 and page["page_num"] <= 3:
                content = page["content"]
                lines = page["lines"]
                
                # 过滤掉目录相关内容
                filtered_lines = []
                skip_keywords = ['目 录', '前言', '新起点', '新主人', '新方向', '新生命', '新操练', '新关系', '新使命']
                
                for line in lines:
                    # 跳过目录行和页码
                    if (not any(keyword in line for keyword in skip_keywords) and 
                        not line.isdigit() and 
                        len(line) > 3):
                        filtered_lines.append(line)
                
                preface_content.extend(filtered_lines)
        
        # 构建前言数据
        preface_data = {
            "title": "前言 - 一对一的故事",
            "content": '\\n'.join(preface_content),
            "type": "preface"
        }
        
        return preface_data
    
    def extract_five_steps(self, pages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """提取带门徒5个步骤（第4-5页）"""
        print("📚 提取带门徒5个步骤...")
        
        steps_content = []
        
        # 从第4页"开始作门徒"开始，到第6页之前
        for page in pages:
            if page["page_num"] >= 4 and page["page_num"] <= 5:
                content = page["content"]
                lines = page["lines"]
                
                # 查找"开始作门徒"部分
                in_steps_section = False
                for line in lines:
                    if "开始作门徒" in line or in_steps_section:
                        in_steps_section = True
                        
                        # 跳过一些标记性文字，但保留内容
                        if (not line.isdigit() and 
                            len(line) > 3 and
                            line not in ['开始作门徒']):
                            steps_content.append(line)
        
        # 查找经文
        content_text = '\\n'.join(steps_content)
        verses = self.extract_verses_from_text(content_text)
        
        # 处理经文填空
        processed_verses = []
        for verse in verses[:5]:  # 最多5个经文
            fill_text, blanks, hints = self.create_fill_blanks(verse["text"])
            if blanks:
                processed_verses.append({
                    "reference": verse["reference"],
                    "text": fill_text,
                    "blanks": blanks,
                    "hints": hints,
                    "explanation": f"这是{verse['reference']}，帮助理解门徒训练的重要步骤"
                })
        
        steps_data = {
            "title": "开始作门徒 - 五个步骤",
            "content": content_text,
            "key_verses": processed_verses,
            "type": "steps"
        }
        
        return steps_data
    
    def extract_seven_lessons(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """提取7课一对一内容（第6页开始）"""
        print("📑 提取7课一对一内容...")
        
        lessons = []
        
        # 定义章节信息
        chapter_info = [
            {"num": 1, "title": "新起点 - 得救", "keywords": ["新起点", "得救"]},
            {"num": 2, "title": "新主人 - 主权", "keywords": ["新主人", "主权"]},
            {"num": 3, "title": "新方向 - 悔改", "keywords": ["新方向", "悔改"]},
            {"num": 4, "title": "新生命 - 洗礼", "keywords": ["新生命", "洗礼"]},
            {"num": 5, "title": "新操练 - 灵修", "keywords": ["新操练", "灵修"]},
            {"num": 6, "title": "新关系 - 教会", "keywords": ["新关系", "教会"]},
            {"num": 7, "title": "新使命 - 带门徒", "keywords": ["新使命", "带门徒"]}
        ]
        
        # 从第6页开始提取章节内容
        current_chapter = None
        chapter_content = []
        
        for page in pages:
            if page["page_num"] >= 6:  # 从第6页开始
                lines = page["lines"]
                
                for line in lines:
                    # 检查是否是新章节开始
                    for chapter in chapter_info:
                        if any(keyword in line for keyword in chapter["keywords"]):
                            # 保存前一章
                            if current_chapter and chapter_content:
                                lesson_data = self.process_lesson_content(
                                    current_chapter, chapter_content
                                )
                                lessons.append(lesson_data)
                            
                            # 开始新章
                            current_chapter = chapter
                            chapter_content = [line]
                            print(f"📖 找到第{chapter['num']}课: {chapter['title']}")
                            break
                    else:
                        # 添加到当前章节
                        if current_chapter and line and not line.isdigit():
                            chapter_content.append(line)
        
        # 保存最后一章
        if current_chapter and chapter_content:
            lesson_data = self.process_lesson_content(current_chapter, chapter_content)
            lessons.append(lesson_data)
        
        return lessons
    
    def process_lesson_content(self, chapter_info: Dict[str, Any], content_lines: List[str]) -> Dict[str, Any]:
        """处理单个课程内容"""
        content_text = '\\n'.join(content_lines)
        
        # 提取经文
        verses = self.extract_verses_from_text(content_text)
        
        # 处理经文填空
        processed_verses = []
        for verse in verses[:4]:  # 每课最多4个经文
            fill_text, blanks, hints = self.create_fill_blanks(verse["text"])
            if blanks:
                processed_verses.append({
                    "reference": verse["reference"],
                    "text": fill_text,
                    "blanks": blanks,
                    "hints": hints,
                    "explanation": f"这段经文帮助我们理解{chapter_info['title']}的重要真理"
                })
        
        lesson_data = {
            "chapter": chapter_info["num"],
            "title": chapter_info["title"],
            "subtitle": f"第{chapter_info['num']}课",
            "content": content_text,
            "key_verses": processed_verses,
            "type": "lesson"
        }
        
        return lesson_data
    
    def extract_verses_from_text(self, text: str) -> List[Dict[str, str]]:
        """从文本中提取经文引用"""
        verses = []
        
        # 查找经文引用模式
        verse_matches = self.verse_pattern.findall(text)
        
        for verse_ref in set(verse_matches):  # 去重
            verse_context = self.find_verse_context(text, verse_ref)
            if verse_context and len(verse_context) > 15:
                verses.append({
                    "reference": verse_ref,
                    "text": verse_context,
                    "original": verse_context
                })
        
        return verses
    
    def find_verse_context(self, text: str, verse_ref: str) -> str:
        """找到经文引用的上下文内容"""
        lines = text.split('\\n')
        
        for i, line in enumerate(lines):
            if verse_ref in line:
                # 查找经文内容
                context_lines = []
                
                # 检查前后几行
                start = max(0, i - 3)
                end = min(len(lines), i + 4)
                
                for j in range(start, end):
                    context_line = lines[j].strip()
                    if (context_line and 
                        not context_line.isdigit() and 
                        len(context_line) > 10 and
                        verse_ref not in context_line):  # 排除引用行本身
                        context_lines.append(context_line)
                
                if context_lines:
                    # 返回最长的合理经文
                    longest = max(context_lines, key=len)
                    if len(longest) > 20:
                        return longest
        
        return ""
    
    def create_fill_blanks(self, verse_text: str) -> Tuple[str, List[str], List[str]]:
        """将经文转换为填空形式"""
        key_words = [
            "神", "主", "耶稣", "基督", "圣灵", "天父", "上帝",
            "爱", "信", "救", "永生", "天国", "恩典", "拯救",
            "祷告", "赞美", "敬拜", "顺服", "谦卑", "悔改",
            "喜乐", "平安", "盼望", "信心", "爱心", "恩赐",
            "道", "真理", "生命", "光", "门徒", "福音", "洗礼"
        ]
        
        blanks = []
        hints = []
        result_text = verse_text
        
        for word in key_words:
            if word in verse_text and word not in blanks:
                hint = word[0] + "_" * (len(word) - 1) if len(word) > 1 else word[0] + "_"
                
                result_text = result_text.replace(word, "___", 1)
                blanks.append(word)
                hints.append(hint)
                
                if len(blanks) >= 3:
                    break
        
        return result_text, blanks, hints
    
    def generate_html_template(self, data: Dict[str, Any], page_type: str) -> str:
        """生成HTML页面模板"""
        
        # 根据页面类型选择不同的样式和内容
        if page_type == "preface":
            return self.generate_preface_html(data)
        elif page_type == "steps":
            return self.generate_steps_html(data)
        elif page_type == "lesson":
            return self.generate_lesson_html(data)
    
    def generate_preface_html(self, data: Dict[str, Any]) -> str:
        """生成前言页面HTML"""
        
        formatted_content = self.format_content_html(data["content"])
        
        html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data["title"]} - 一对一门徒训练</title>
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
            padding: 40px 20px;
            margin-bottom: 30px;
        }}
        
        .story-title {{
            font-size: 2.5rem;
            color: #2d3748;
            margin-bottom: 15px;
        }}
        
        .story-subtitle {{
            font-size: 1.2rem;
            color: #667eea;
            font-weight: 500;
        }}
        
        .content-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }}
        
        .story-content {{
            font-size: 1.2rem;
            line-height: 2;
            color: #2d3748;
        }}
        
        .navigation {{
            text-align: center;
        }}
        
        .nav-btn {{
            background: rgba(255, 255, 255, 0.9);
            color: #2d3748;
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            font-size: 1.1rem;
            cursor: pointer;
            margin: 0 15px;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }}
        
        .nav-btn:hover {{
            background: white;
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        }}
        
        @media (max-width: 768px) {{
            .story-title {{
                font-size: 2rem;
            }}
            
            .content-section {{
                padding: 25px 20px;
            }}
            
            .story-content {{
                font-size: 1.1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="story-title">{data["title"]}</h1>
            <p class="story-subtitle">一个改变生命的见证</p>
        </header>
        
        <section class="content-section">
            <div class="story-content">{formatted_content}</div>
        </section>
        
        <div class="navigation">
            <a href="index.html" class="nav-btn">🏠 返回主页</a>
            <a href="steps.html" class="nav-btn">下一步 ➡️</a>
        </div>
    </div>
</body>
</html>'''
        
        return html_content
    
    def generate_steps_html(self, data: Dict[str, Any]) -> str:
        """生成5个步骤页面HTML"""
        
        formatted_content = self.format_content_html(data["content"])
        
        # 生成经文填空HTML
        verses_html = ""
        for i, verse in enumerate(data["key_verses"]):
            verse_id = f"verse_steps_{i+1}"
            verses_html += f'''
            <div class="verse-container">
                <div class="verse-reference">{verse["reference"]}</div>
                <div class="verse-content" id="{verse_id}">
                    {self.create_blanks_html(verse, verse_id)}
                </div>
                <div class="verse-explanation">{verse["explanation"]}</div>
                <div class="verse-controls">
                    <button onclick="showHints('{verse_id}')" class="hint-btn">💡 提示</button>
                    <button onclick="checkAnswers('{verse_id}')" class="check-btn">✅ 检查</button>
                    <button onclick="showAnswers('{verse_id}')" class="answer-btn">📖 答案</button>
                </div>
            </div>
            '''
        
        html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data["title"]} - 一对一门徒训练</title>
    <style>
        /* 这里使用与lesson相同的样式 */
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
        
        .chapter-title {{
            font-size: 2.2rem;
            color: #2d3748;
            margin-bottom: 10px;
        }}
        
        .chapter-subtitle {{
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
        
        .original-content {{
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
        
        .verse-explanation {{
            font-size: 0.95rem;
            color: #718096;
            margin-bottom: 15px;
            font-style: italic;
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
            .chapter-title {{
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
            <h1 class="chapter-title">{data["title"]}</h1>
            <p class="chapter-subtitle">门徒训练的基础</p>
        </header>
        
        <section class="content-section">
            <h2 class="section-title">📖 五个步骤</h2>
            <div class="original-content">{formatted_content}</div>
        </section>
        
        """ + (f'''
        <section class="content-section">
            <h2 class="section-title">✏️ 经文练习</h2>
            <p class="practice-intro">通过填空练习来加深对重要经文的理解。</p>
            {verses_html}
        </section>
        ''' if verses_html else '') + """
        
        <div class="navigation">
            <a href="preface.html" class="nav-btn">⬅️ 前言</a>
            <a href="index.html" class="nav-btn">🏠 主页</a>
            <a href="one2one_C1.html" class="nav-btn">第一课 ➡️</a>
        </div>
    </div>
    
    <script>
        const chapterData = {json.dumps(data, ensure_ascii=False)};
        
        function showHints(verseId) {{
            const verseIndex = parseInt(verseId.split('_')[2]) - 1;
            const verse = chapterData.key_verses[verseIndex];
            const inputs = document.querySelectorAll(`#${{verseId}} .blank-input`);
            
            inputs.forEach((input, index) => {{
                if (verse.hints && verse.hints[index]) {{
                    input.placeholder = verse.hints[index];
                }}
            }});
            
            showMessage('💡 已显示提示', 'info');
        }}
        
        function checkAnswers(verseId) {{
            const verseIndex = parseInt(verseId.split('_')[2]) - 1;
            const verse = chapterData.key_verses[verseIndex];
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
            const verseIndex = parseInt(verseId.split('_')[2]) - 1;
            const verse = chapterData.key_verses[verseIndex];
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
    
    def generate_lesson_html(self, data: Dict[str, Any]) -> str:
        """生成课程页面HTML（与之前类似但更完善）"""
        
        chapter_num = data["chapter"]
        title = data["title"]
        content = data["content"]
        
        formatted_content = self.format_content_html(content)
        
        # 生成经文填空HTML
        verses_html = ""
        for i, verse in enumerate(data["key_verses"]):
            verse_id = f"verse_{chapter_num}_{i+1}"
            verses_html += f'''
            <div class="verse-container">
                <div class="verse-reference">{verse["reference"]}</div>
                <div class="verse-content" id="{verse_id}">
                    {self.create_blanks_html(verse, verse_id)}
                </div>
                <div class="verse-explanation">{verse["explanation"]}</div>
                <div class="verse-controls">
                    <button onclick="showHints('{verse_id}')" class="hint-btn">💡 提示</button>
                    <button onclick="checkAnswers('{verse_id}')" class="check-btn">✅ 检查</button>
                    <button onclick="showAnswers('{verse_id}')" class="answer-btn">📖 答案</button>
                </div>
            </div>
            '''
        
        # 导航逻辑
        prev_link = "steps.html" if chapter_num == 1 else f"one2one_C{chapter_num-1}.html"
        next_link = f"one2one_C{chapter_num+1}.html" if chapter_num < 7 else "index.html"
        
        # 这里使用与steps_html类似的HTML模板，但调整导航和内容
        html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 一对一门徒训练</title>
    <!-- 这里使用相同的样式，为了简洁省略 -->
    <!-- ... 样式内容与steps_html相同 ... -->
    <style>
        /* 相同的CSS样式 */
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Microsoft YaHei', 'SimSun', Arial, sans-serif; line-height: 1.8; color: #333; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        .header {{ text-align: center; background: rgba(255, 255, 255, 0.95); border-radius: 20px; box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37); backdrop-filter: blur(4px); border: 1px solid rgba(255, 255, 255, 0.18); padding: 30px 20px; margin-bottom: 30px; }}
        .chapter-title {{ font-size: 2.2rem; color: #2d3748; margin-bottom: 10px; }}
        .chapter-subtitle {{ font-size: 1.1rem; color: #667eea; font-weight: 500; }}
        .content-section {{ background: rgba(255, 255, 255, 0.95); border-radius: 15px; padding: 30px; margin-bottom: 25px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1); }}
        .section-title {{ font-size: 1.5rem; color: #2d3748; margin-bottom: 20px; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
        .original-content {{ font-size: 1.1rem; line-height: 1.9; color: #2d3748; }}
        .verse-container {{ background: #f7fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px; margin-bottom: 20px; }}
        .verse-reference {{ font-weight: bold; color: #2b6cb0; margin-bottom: 10px; font-size: 1.1rem; }}
        .verse-content {{ font-size: 1.1rem; line-height: 1.8; margin-bottom: 15px; }}
        .verse-explanation {{ font-size: 0.95rem; color: #718096; margin-bottom: 15px; font-style: italic; }}
        .blank-input {{ display: inline-block; min-width: 60px; border: none; border-bottom: 2px solid #667eea; background: transparent; text-align: center; font-size: 1.1rem; font-weight: bold; color: #2d3748; padding: 2px 8px; margin: 0 2px; }}
        .blank-input:focus {{ outline: none; border-bottom-color: #764ba2; background: rgba(102, 126, 234, 0.1); }}
        .blank-input.correct {{ border-bottom-color: #48bb78; background: rgba(72, 187, 120, 0.1); }}
        .blank-input.incorrect {{ border-bottom-color: #f56565; background: rgba(245, 101, 101, 0.1); }}
        .verse-controls {{ display: flex; gap: 10px; flex-wrap: wrap; }}
        .verse-controls button {{ padding: 8px 16px; border: none; border-radius: 6px; font-size: 0.9rem; cursor: pointer; transition: all 0.3s ease; }}
        .hint-btn {{ background: #fbb6ce; color: #702459; }}
        .check-btn {{ background: #9ae6b4; color: #22543d; }}
        .answer-btn {{ background: #90cdf4; color: #1a365d; }}
        .verse-controls button:hover {{ transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15); }}
        .navigation {{ text-align: center; margin-top: 30px; }}
        .nav-btn {{ background: rgba(255, 255, 255, 0.9); color: #2d3748; padding: 12px 24px; border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; margin: 0 10px; transition: all 0.3s ease; text-decoration: none; display: inline-block; }}
        .nav-btn:hover {{ background: white; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); }}
        @media (max-width: 768px) {{ .chapter-title {{ font-size: 1.8rem; }} .content-section {{ padding: 20px 15px; }} .verse-controls {{ justify-content: center; }} .nav-btn {{ display: block; margin: 10px auto; width: 200px; }} }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="chapter-title">{title}</h1>
            <p class="chapter-subtitle">{data["subtitle"]}</p>
        </header>
        
        <section class="content-section">
            <h2 class="section-title">📖 课程内容</h2>
            <div class="original-content">{formatted_content}</div>
        </section>
        
        {f'''
        <section class="content-section">
            <h2 class="section-title">✏️ 经文练习</h2>
            {verses_html}
        </section>
        ''' if verses_html else ''}
        
        <div class="navigation">
            <a href="{prev_link}" class="nav-btn">⬅️ 上一课</a>
            <a href="index.html" class="nav-btn">🏠 主页</a>
            <a href="{next_link}" class="nav-btn">下一课 ➡️</a>
        </div>
    </div>
    
    <script>
        const chapterData = {json.dumps(data, ensure_ascii=False)};
        // 相同的JavaScript函数...
        function showHints(verseId) {{ /* 省略实现 */ }}
        function checkAnswers(verseId) {{ /* 省略实现 */ }}
        function showAnswers(verseId) {{ /* 省略实现 */ }}
        function showMessage(text, type) {{ /* 省略实现 */ }}
    </script>
</body>
</html>'''
        
        return html_content
    
    def format_content_html(self, content: str) -> str:
        """格式化内容为HTML"""
        lines = content.split('\\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 突出显示经文引用
            line = self.verse_pattern.sub(r'<strong style="color: #2b6cb0;">\\1</strong>', line)
            
            # 突出显示重要概念
            important_words = ['耶稣', '基督', '神', '主', '拯救', '得救', '信心', '爱', '真理']
            for word in important_words:
                line = line.replace(word, f'<span style="color: #2d3748; font-weight: 600;">{word}</span>')
            
            formatted_lines.append(line)
        
        return '<br><br>'.join(formatted_lines)
    
    def create_blanks_html(self, verse_data: Dict[str, Any], verse_id: str) -> str:
        """将经文文本转换为带填空的HTML"""
        text = verse_data["text"]
        blanks = verse_data["blanks"]
        
        blank_index = 0
        result = ""
        i = 0
        
        while i < len(text):
            if text[i:i+3] == "___":
                if blank_index < len(blanks):
                    width = max(60, len(blanks[blank_index]) * 12 + 20)
                    result += f'<input type="text" class="blank-input" style="width:{width}px;" data-answer="{blanks[blank_index]}" />'
                    blank_index += 1
                else:
                    result += "___"
                i += 3
            else:
                result += text[i]
                i += 1
        
        return result

def main():
    """主函数"""
    print("🚀 开始完整提取一对一PDF内容...")
    
    extractor = One2OneCompleteExtractor()
    
    # 提取所有页面
    all_pages = extractor.extract_all_pages()
    
    if not all_pages:
        print("❌ 无法提取PDF内容")
        return
    
    # 1. 提取前言故事
    print("\\n📖 1. 处理前言故事...")
    preface_data = extractor.extract_preface_story(all_pages)
    
    # 保存前言数据和HTML
    preface_json = os.path.join(extractor.data_dir, "preface.json")
    with open(preface_json, "w", encoding="utf-8") as f:
        json.dump(preface_data, f, ensure_ascii=False, indent=2)
    
    preface_html = extractor.generate_preface_html(preface_data)
    preface_file = os.path.join(extractor.output_dir, "preface.html")
    with open(preface_file, "w", encoding="utf-8") as f:
        f.write(preface_html)
    
    print(f"✅ 前言页面生成完成: {preface_file}")
    
    # 2. 提取5个步骤
    print("\\n📚 2. 处理带门徒5个步骤...")
    steps_data = extractor.extract_five_steps(all_pages)
    
    # 保存步骤数据和HTML
    steps_json = os.path.join(extractor.data_dir, "steps.json")
    with open(steps_json, "w", encoding="utf-8") as f:
        json.dump(steps_data, f, ensure_ascii=False, indent=2)
    
    steps_html = extractor.generate_steps_html(steps_data)
    steps_file = os.path.join(extractor.output_dir, "steps.html")
    with open(steps_file, "w", encoding="utf-8") as f:
        f.write(steps_html)
    
    print(f"✅ 步骤页面生成完成: {steps_file}")
    print(f"   经文数量: {len(steps_data['key_verses'])} 个")
    
    # 3. 提取7课内容
    print("\\n📑 3. 处理7课一对一内容...")
    lessons = extractor.extract_seven_lessons(all_pages)
    
    print(f"📚 找到 {len(lessons)} 课内容")
    
    # 处理每一课
    for lesson in lessons:
        chapter_num = lesson["chapter"]
        
        # 保存课程数据
        lesson_json = os.path.join(extractor.data_dir, f"chapter{chapter_num}.json")
        with open(lesson_json, "w", encoding="utf-8") as f:
            json.dump(lesson, f, ensure_ascii=False, indent=2)
        
        # 生成课程HTML
        lesson_html = extractor.generate_lesson_html(lesson)
        lesson_file = os.path.join(extractor.output_dir, f"one2one_C{chapter_num}.html")
        with open(lesson_file, "w", encoding="utf-8") as f:
            f.write(lesson_html)
        
        print(f"✅ 第{chapter_num}课生成完成: {lesson_file}")
        print(f"   内容长度: {len(lesson['content'])} 字符")
        print(f"   经文数量: {len(lesson['key_verses'])} 个")
    
    # 4. 更新主页导航
    print("\\n🔗 4. 更新主页导航...")
    update_main_index(lessons)
    
    print("\\n🎉 一对一完整内容提取完成！")
    print("\\n📋 生成的页面:")
    print("   📖 前言故事: preface.html")  
    print("   📚 五个步骤: steps.html")
    print("   📑 七课内容: one2one_C1.html ~ one2one_C7.html")

def update_main_index(lessons):
    """更新主页，添加前言和步骤的链接"""
    
    # 读取现有的index.html
    index_file = "one2one/index.html"
    
    # 生成完整的主页内容
    lessons_cards = ""
    for lesson in lessons:
        lessons_cards += f'''
            <div class="chapter-card" onclick="location.href='one2one_C{lesson['chapter']}.html'">
                <div class="chapter-number">{lesson['chapter']}</div>
                <div class="chapter-title">{lesson['title']}</div>
                <div class="chapter-summary">
                    {get_chapter_summary(lesson['chapter'])}
                </div>
            </div>'''
    
    new_index_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>一对一门徒训练 - 个人跟进及带门徒</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Microsoft YaHei', 'SimSun', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
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
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            padding: 40px 20px;
            margin-bottom: 30px;
        }}
        
        .title {{
            font-size: 2.5rem;
            color: #2d3748;
            margin-bottom: 15px;
        }}
        
        .subtitle {{
            font-size: 1.2rem;
            color: #667eea;
            font-weight: 500;
        }}
        
        .intro-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }}
        
        .quick-start {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .quick-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            cursor: pointer;
            text-align: center;
        }}
        
        .quick-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15);
        }}
        
        .quick-icon {{
            font-size: 3rem;
            margin-bottom: 15px;
        }}
        
        .quick-title {{
            font-size: 1.4rem;
            color: #2d3748;
            margin-bottom: 10px;
        }}
        
        .quick-desc {{
            color: #718096;
            font-size: 1rem;
        }}
        
        .chapters-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }}
        
        .section-title {{
            font-size: 1.8rem;
            color: #2d3748;
            margin-bottom: 20px;
            text-align: center;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .chapters-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .chapter-card {{
            background: #f7fafc;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
            cursor: pointer;
            border: 1px solid #e2e8f0;
        }}
        
        .chapter-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
            border-color: #667eea;
        }}
        
        .chapter-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .chapter-title {{
            font-size: 1.3rem;
            color: #2d3748;
            margin-bottom: 10px;
        }}
        
        .chapter-summary {{
            color: #718096;
            font-size: 0.95rem;
        }}
        
        .navigation {{
            text-align: center;
        }}
        
        .nav-btn {{
            background: rgba(255, 255, 255, 0.9);
            color: #2d3748;
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            font-size: 1.1rem;
            cursor: pointer;
            margin: 0 15px;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }}
        
        .nav-btn:hover {{
            background: white;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        }}
        
        @media (max-width: 768px) {{
            .title {{
                font-size: 2rem;
            }}
            
            .quick-start {{
                grid-template-columns: 1fr;
            }}
            
            .chapters-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="title">一对一门徒训练</h1>
            <p class="subtitle">个人跟进及带门徒</p>
        </header>
        
        <section class="intro-section">
            <h2 style="color: #2d3748; margin-bottom: 15px; text-align: center;">📖 课程简介</h2>
            <p style="text-align: center; color: #4a5568; font-size: 1.1rem;">个人跟进和带门徒，这就是耶稣给我们的大使命。本课程将帮助你建立稳固的信仰根基，学习祷告、读经和灵修，融入教会生活，并承担门徒训练的使命。</p>
        </section>
        
        <section class="quick-start">
            <div class="quick-card" onclick="location.href='preface.html'">
                <div class="quick-icon">📚</div>
                <div class="quick-title">前言故事</div>
                <div class="quick-desc">了解一对一门徒训练的起源和见证</div>
            </div>
            
            <div class="quick-card" onclick="location.href='steps.html'">
                <div class="quick-icon">🎯</div>
                <div class="quick-title">五个步骤</div>
                <div class="quick-desc">学习门徒训练的基础五个步骤</div>
            </div>
            
            <div class="quick-card" onclick="location.href='one2one_C1.html'">
                <div class="quick-icon">🚀</div>
                <div class="quick-title">开始学习</div>
                <div class="quick-desc">从第一课开始你的门徒训练之旅</div>
            </div>
        </section>
        
        <section class="chapters-section">
            <h2 class="section-title">📑 七课内容</h2>
            <div class="chapters-grid">{lessons_cards}
            </div>
        </section>
        
        <div class="navigation">
            <a href="../index.html" class="nav-btn">🏠 返回网站主页</a>
        </div>
    </div>
</body>
</html>'''
    
    # 写入更新后的主页
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(new_index_content)
    
    print(f"✅ 主页更新完成: {index_file}")

def get_chapter_summary(chapter_num):
    """获取章节简介"""
    summaries = {
        1: "了解救恩的意义，建立与神的个人关系",
        2: "认识耶稣为生命的主，学习顺服主权",
        3: "明白悔改的重要性，改变生活方向", 
        4: "通过洗礼见证重生，表明信仰决心",
        5: "建立每日灵修的习惯，与神亲密交通",
        6: "融入教会生活，在肢体中成长",
        7: "承担大使命，学习带领门徒"
    }
    return summaries.get(chapter_num, "重要的门徒训练内容")

if __name__ == "__main__":
    main()