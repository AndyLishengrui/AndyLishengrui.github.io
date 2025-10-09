#!/usr/bin/env python3
"""
一对一门徒训练真实内容提取工具（改进版）

从《一对一（大字版）.pdf》中提取真实课程内容，保持原文不变
只将经文部分转换为可填空的交互式测试
"""

import pdfplumber
import json
import re
import os
from typing import Dict, List, Any, Tuple

class One2OneRealExtractor:
    def __init__(self, pdf_path: str = "一对一（大字版）.pdf"):
        self.pdf_path = pdf_path
        self.output_dir = "one2one"
        self.data_dir = os.path.join(self.output_dir, "data")
        
        # 确保目录存在
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 经文引用正则模式 - 更准确的模式
        self.verse_pattern = re.compile(r'([一二三约翰马太马可路加使徒行传罗马哥林多加拉太以弗所腓立比歌罗西帖撒罗尼迦提摩太提多腓利门希伯来雅各彼得犹大启示录创世记出埃及记利未记民数记申命记约书亚记士师记路得记撒母耳塞缪尔列王历代志以斯拉尼希米以斯帖约伯诗篇箴言传道书雅歌以赛亚耶利米哀歌以西结但以理何西阿约珥阿摩司俄巴底亚约拿弥迦那鸿哈巴谷西番雅哈该撒迦利亚玛拉基]+(?:福音|书|记|篇)*\\s*\\d+:\\d+(?:[-,]\\d+)*)', re.UNICODE)
        
    def extract_full_pdf_content(self) -> List[Dict[str, Any]]:
        """提取PDF的完整内容"""
        print(f"🔍 开始提取PDF内容: {self.pdf_path}")
        
        all_text = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    print(f"📄 处理第{i+1}页...")
                    all_text.append({
                        "page": i + 1,
                        "content": text.strip()
                    })
        
        return all_text
    
    def smart_chapter_extraction(self, pages_content: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """智能章节提取 - 改进版"""
        chapters = []
        
        # 从目录页面获取章节信息
        toc_page = None
        for page_data in pages_content:
            if "新起点" in page_data["content"] and "新主人" in page_data["content"]:
                toc_page = page_data
                break
        
        if toc_page:
            print("📚 找到目录页面")
            # 提取章节标题
            chapter_titles = [
                "1 新起点 得救",
                "2 新主人 主权", 
                "3 新方向 悔改",
                "4 新生命 洗礼",
                "5 新操练 灵修",
                "6 新关系 教会",
                "7 新使命 带门徒"
            ]
        
        # 寻找每个章节的实际内容
        for i, title in enumerate(chapter_titles, 1):
            chapter_content = []
            found_start = False
            
            for page_data in pages_content:
                content = page_data["content"]
                lines = content.split('\\n')
                
                # 查找章节开始
                if not found_start:
                    for line in lines:
                        if title.strip() in line:
                            found_start = True
                            print(f"📖 找到章节 {i}: {title}")
                            break
                
                # 收集内容
                if found_start:
                    # 提取这一页相关的内容
                    page_lines = []
                    in_chapter = False
                    
                    for line in lines:
                        line_clean = line.strip()
                        
                        # 开始收集内容的标志
                        if title.strip() in line_clean:
                            in_chapter = True
                            page_lines.append(line_clean)
                            continue
                        
                        # 如果遇到下一章标题，停止收集
                        if in_chapter and i < len(chapter_titles):
                            next_title = chapter_titles[i] if i < len(chapter_titles) else ""
                            if next_title and next_title.strip() in line_clean:
                                break
                        
                        # 收集章节内容
                        if in_chapter and line_clean:
                            # 过滤页码和无关信息
                            if not (line_clean.isdigit() or 
                                   len(line_clean) < 3 or
                                   line_clean in ['目 录', '前言', '开始作门徒']):
                                page_lines.append(line_clean)
                    
                    if page_lines:
                        chapter_content.extend(page_lines)
                    
                    # 如果内容足够长，可以停止搜索
                    if len('\\n'.join(chapter_content)) > 200:
                        break
            
            if chapter_content:
                chapters.append({
                    "title": title,
                    "content": chapter_content,
                    "chapter_num": i
                })
        
        return chapters
    
    def extract_verses_from_text(self, text: str) -> List[Dict[str, str]]:
        """从文本中提取经文引用"""
        verses = []
        
        # 查找经文引用模式
        verse_matches = self.verse_pattern.findall(text)
        
        for verse_ref in set(verse_matches):  # 去重
            # 尝试在文本中找到这个经文引用附近的内容
            verse_context = self.find_verse_context(text, verse_ref)
            if verse_context and len(verse_context) > 10:
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
                # 尝试获取经文内容
                context_lines = []
                
                # 检查前后几行
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                
                for j in range(start, end):
                    context_line = lines[j].strip()
                    if context_line and not context_line.isdigit():
                        # 过滤掉纯数字行（页码等）和太短的行
                        if len(context_line) > 8 and not context_line in ['前言', '目录']:
                            context_lines.append(context_line)
                
                # 返回最长的合理段落
                if context_lines:
                    longest = max(context_lines, key=len)
                    if len(longest) > 15:  # 经文通常较长
                        return longest
        
        return ""
    
    def create_fill_blanks(self, verse_text: str) -> Tuple[str, List[str], List[str]]:
        """将经文转换为填空形式"""
        # 关键词列表（需要填空的重要词汇）
        key_words = [
            "神", "主", "耶稣", "基督", "圣灵", "天父", "上帝",
            "爱", "信", "救", "永生", "天国", "恩典", "拯救",
            "祷告", "赞美", "敬拜", "顺服", "谦卑", "悔改",
            "喜乐", "平安", "盼望", "信心", "爱心", "恩赐",
            "道", "真理", "生命", "光", "门徒", "福音"
        ]
        
        blanks = []
        hints = []
        result_text = verse_text
        
        # 为关键词创建填空
        for word in key_words:
            if word in verse_text and word not in blanks:
                # 创建提示（首字母 + 下划线）
                if len(word) == 1:
                    hint = word[0] + "_"
                else:
                    hint = word[0] + "_" * (len(word) - 1)
                
                # 替换第一个出现的词
                result_text = result_text.replace(word, "___", 1)
                blanks.append(word)
                hints.append(hint)
                
                # 限制填空数量
                if len(blanks) >= 3:
                    break
        
        return result_text, blanks, hints
    
    def process_real_chapter(self, chapter_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理真实章节数据"""
        content_text = '\\n'.join(chapter_data["content"])
        chapter_num = chapter_data["chapter_num"]
        
        # 提取经文
        verses = self.extract_verses_from_text(content_text)
        
        # 处理经文填空
        processed_verses = []
        for verse in verses[:3]:  # 限制每章最多3个经文
            fill_text, blanks, hints = self.create_fill_blanks(verse["text"])
            if blanks:  # 只有当找到关键词时才添加
                processed_verses.append({
                    "reference": verse["reference"],
                    "text": fill_text,
                    "blanks": blanks,
                    "hints": hints,
                    "explanation": f"这是{verse['reference']}的重要经文，请仔细思考其含义。"
                })
        
        # 构建章节数据
        processed_chapter = {
            "chapter": chapter_num,
            "title": chapter_data["title"],
            "subtitle": f"Chapter {chapter_num}",
            "content": content_text,
            "key_verses": processed_verses,
            "page_start": 1
        }
        
        return processed_chapter
    
    def format_content_html(self, content: str) -> str:
        """格式化内容为HTML，保持原文格式"""
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
        
        # 替换下划线为输入框
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
    
    def generate_html_with_real_content(self, chapter_data: Dict[str, Any]) -> str:
        """基于真实内容生成HTML页面"""
        
        chapter_num = chapter_data["chapter"]
        title = chapter_data["title"]
        content = chapter_data["content"]
        
        # 生成经文填空HTML
        verses_html = ""
        for i, verse in enumerate(chapter_data["key_verses"]):
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
        
        # 处理正文内容，保持原文格式
        formatted_content = self.format_content_html(content)
        
        # 构建经文练习部分HTML
        verse_section = ""
        if verses_html:
            verse_section = f'''
        <section class="content-section">
            <h2 class="section-title">✏️ 经文练习</h2>
            <p class="practice-intro">通过填空练习来加深对经文的理解和记忆。请认真思考每个空格的内容。</p>
            {verses_html}
        </section>
        '''
        
        html_template = '''<!DOCTYPE html>
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
        
        .practice-intro {{
            font-size: 1rem;
            color: #4a5568;
            margin-bottom: 20px;
            padding: 15px;
            background: #f7fafc;
            border-left: 4px solid #667eea;
            border-radius: 4px;
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
            <h1 class="chapter-title">{title}</h1>
            <p class="chapter-subtitle">一对一门徒训练系列</p>
        </header>
        
        <section class="content-section">
            <h2 class="section-title">📖 课程内容</h2>
            <div class="original-content">{formatted_content}</div>
        </section>
        
        {verse_section}
        
        <div class="navigation">
            <button onclick="location.href='index.html'" class="nav-btn">🏠 返回主页</button>
            <button onclick="location.href='one2one_C{prev_chapter}.html'" class="nav-btn">⬅️ 上一课</button>
            <button onclick="location.href='one2one_C{next_chapter}.html'" class="nav-btn">下一课 ➡️</button>
        </div>
    </div>
    
    <script>
        // 经文填空交互功能
        const chapterData = {chapter_data_json};
        
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
        
        // 键盘快捷键
        document.addEventListener('keydown', function(e) {{
            if (e.ctrlKey || e.metaKey) {{
                switch(e.key) {{
                    case 'h':
                        e.preventDefault();
                        const firstVerse = document.querySelector('[id^="verse_"]');
                        if (firstVerse) showHints(firstVerse.id);
                        break;
                    case 'Enter':
                        e.preventDefault();
                        const firstVerseCheck = document.querySelector('[id^="verse_"]');
                        if (firstVerseCheck) checkAnswers(firstVerseCheck.id);
                        break;
                }}
            }}
        }});
    </script>
</body>
</html>'''
        
        # 填充模板
        html_content = html_template.format(
            title=title,
            formatted_content=formatted_content,
            verse_section=verse_section,
            prev_chapter=chapter_num-1 if chapter_num > 1 else 7,
            next_chapter=chapter_num+1 if chapter_num < 7 else 1,
            chapter_data_json=json.dumps(chapter_data, ensure_ascii=False)
        )
        
        return html_content

def main():
    """主函数"""
    print("🚀 开始提取一对一真实PDF内容...")
    
    extractor = One2OneRealExtractor()
    
    # 提取PDF内容
    pages_content = extractor.extract_full_pdf_content()
    
    if not pages_content:
        print("❌ 无法提取PDF内容")
        return
    
    # 智能章节提取
    chapters = extractor.smart_chapter_extraction(pages_content)
    
    print(f"📚 找到 {len(chapters)} 个章节")
    
    # 处理所有章节
    for chapter_raw in chapters:
        chapter_num = chapter_raw["chapter_num"]
        print(f"\\n📝 处理第{chapter_num}章: {chapter_raw['title']}")
        
        # 处理章节数据
        chapter_data = extractor.process_real_chapter(chapter_raw)
        
        # 生成JSON数据
        json_file = os.path.join(extractor.data_dir, f"chapter{chapter_num}.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(chapter_data, f, ensure_ascii=False, indent=2)
        
        # 生成HTML页面
        html_content = extractor.generate_html_with_real_content(chapter_data)
        html_file = os.path.join(extractor.output_dir, f"one2one_C{chapter_num}.html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ 生成文件: {json_file}, {html_file}")
        
        # 显示内容预览
        print(f"   内容长度: {len(chapter_data['content'])} 字符")
        print(f"   经文数量: {len(chapter_data['key_verses'])} 个")
    
    # 更新主页链接
    print("\\n🔗 更新一对一主页...")
    update_one2one_index(chapters)
    
    print("\\n🎉 一对一真实内容提取完成！")

def update_one2one_index(chapters):
    """更新一对一主页"""
    index_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>一对一门徒训练 - 个人跟进及带门徒</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Microsoft YaHei', 'SimSun', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            padding: 40px 20px;
            margin-bottom: 30px;
        }
        
        .title {
            font-size: 2.5rem;
            color: #2d3748;
            margin-bottom: 15px;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: #667eea;
            font-weight: 500;
        }
        
        .intro {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }
        
        .chapters-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .chapter-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .chapter-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15);
        }
        
        .chapter-number {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .chapter-title {
            font-size: 1.3rem;
            color: #2d3748;
            margin-bottom: 10px;
        }
        
        .chapter-summary {
            color: #718096;
            font-size: 0.95rem;
        }
        
        .navigation {
            text-align: center;
        }
        
        .nav-btn {
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
        }
        
        .nav-btn:hover {
            background: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        @media (max-width: 768px) {
            .title {
                font-size: 2rem;
            }
            
            .chapters-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="title">一对一门徒训练</h1>
            <p class="subtitle">个人跟进及带门徒</p>
        </header>
        
        <section class="intro">
            <h2 style="color: #2d3748; margin-bottom: 15px;">📖 课程简介</h2>
            <p>个人跟进和带门徒，这就是耶稣给我们的大使命。本课程将帮助你学习如何:</p>
            <ul style="margin-top: 10px; padding-left: 20px; color: #4a5568;">
                <li>建立与神的个人关系</li>
                <li>在信仰上有稳固的根基</li>
                <li>学习祷告、读经和灵修</li>
                <li>融入教会生活</li>
                <li>承担门徒训练的使命</li>
            </ul>
        </section>
        
        <section class="chapters-grid">
''' + '\\n'.join([f'''
            <div class="chapter-card" onclick="location.href='one2one_C{chapter['chapter_num']}.html'">
                <div class="chapter-number">{chapter['chapter_num']}</div>
                <div class="chapter-title">{chapter['title']}</div>
                <div class="chapter-summary">
                    {get_chapter_summary(chapter['chapter_num'])}
                </div>
            </div>''' for chapter in chapters]) + '''
        </section>
        
        <div class="navigation">
            <a href="../index.html" class="nav-btn">🏠 返回网站主页</a>
        </div>
    </div>
</body>
</html>'''

    # 写入文件
    with open("one2one/index.html", "w", encoding="utf-8") as f:
        f.write(index_content)

def get_chapter_summary(chapter_num):
    """获取章节简介"""
    summaries = {
        1: "了解救恩的意义，建立与神的关系",
        2: "认识耶稣为生命的主，学习顺服",
        3: "明白悔改的重要性，改变生活方向", 
        4: "通过洗礼见证新生命",
        5: "建立每日灵修的习惯",
        6: "融入教会生活，与肢体相交",
        7: "承担大使命，带领门徒"
    }
    return summaries.get(chapter_num, "重要的门徒训练内容")

if __name__ == "__main__":
    main()