#!/usr/bin/env python3
"""
一对一门徒训练真实内容提取工具

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
        
        # 经文引用正则模式
        self.verse_pattern = re.compile(r'([一二三约翰马太马可路加使徒行传罗马哥林多加拉太以弗所腓立比歌罗西帖撒罗尼迦提摩太提多腓利门希伯来雅各彼得犹大启示录]+(?:福音|书)*\s*\d+:\d+(?:-\d+)*)', re.UNICODE)
        
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
    
    def identify_chapters(self, pages_content: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """识别和分割章节"""
        chapters = []
        current_chapter = None
        chapter_patterns = [
            r'第?\s*([一二三四五六七八九十]+)\s*课',
            r'(\d+)\s*新\s*(\w+)',
            r'第\s*(\d+)\s*章',
        ]
        
        for page_data in pages_content:
            content = page_data["content"]
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # 检查是否是章节标题
                for pattern in chapter_patterns:
                    match = re.search(pattern, line)
                    if match:
                        # 保存前一章
                        if current_chapter and current_chapter.get("content"):
                            chapters.append(current_chapter)
                        
                        # 开始新章
                        current_chapter = {
                            "title": line,
                            "content": [],
                            "page_start": page_data["page"]
                        }
                        print(f"📚 发现章节: {line}")
                        break
                
                # 添加内容到当前章节
                if current_chapter is not None:
                    current_chapter["content"].append(line)
        
        # 保存最后一章
        if current_chapter and current_chapter.get("content"):
            chapters.append(current_chapter)
            
        return chapters
    
    def extract_verses_from_text(self, text: str) -> List[Dict[str, str]]:
        """从文本中提取经文引用"""
        verses = []
        
        # 查找经文引用模式
        verse_matches = self.verse_pattern.findall(text)
        
        for verse_ref in verse_matches:
            # 尝试在文本中找到这个经文引用附近的内容
            verse_context = self.find_verse_context(text, verse_ref)
            if verse_context:
                verses.append({
                    "reference": verse_ref,
                    "text": verse_context,
                    "original": verse_context
                })
        
        return verses
    
    def find_verse_context(self, text: str, verse_ref: str) -> str:
        """找到经文引用的上下文内容"""
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if verse_ref in line:
                # 尝试获取经文内容（通常在引用之前或之后）
                context_lines = []
                
                # 检查前后几行
                start = max(0, i - 3)
                end = min(len(lines), i + 4)
                
                for j in range(start, end):
                    context_line = lines[j].strip()
                    if context_line and not context_line.isdigit():
                        # 过滤掉纯数字行（页码等）
                        if len(context_line) > 10:  # 经文通常较长
                            context_lines.append(context_line)
                
                if context_lines:
                    return ' '.join(context_lines)
        
        return ""
    
    def create_fill_blanks(self, verse_text: str) -> Tuple[str, List[str], List[str]]:
        """将经文转换为填空形式"""
        # 关键词列表（需要填空的重要词汇）
        key_words = [
            "神", "主", "耶稣", "基督", "圣灵", "天父", 
            "爱", "信", "救", "永生", "天国", "恩典",
            "祷告", "赞美", "敬拜", "顺服", "谦卑",
            "喜乐", "平安", "盼望", "信心", "爱心",
            "道", "真理", "生命", "光", "门徒"
        ]
        
        blanks = []
        hints = []
        result_text = verse_text
        
        # 为关键词创建填空
        for word in key_words:
            if word in verse_text:
                # 创建提示（首字母 + 下划线）
                if len(word) == 1:
                    hint = word[0] + "_"
                else:
                    hint = word[0] + "_" * (len(word) - 1)
                
                # 替换第一个出现的词
                if word not in blanks:  # 避免重复
                    result_text = result_text.replace(word, "___", 1)
                    blanks.append(word)
                    hints.append(hint)
                
                # 限制填空数量
                if len(blanks) >= 3:
                    break
        
        return result_text, blanks, hints
    
    def process_real_chapter(self, chapter_data: Dict[str, Any], chapter_num: int) -> Dict[str, Any]:
        """处理真实章节数据"""
        content_text = '\n'.join(chapter_data["content"])
        
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
                    "explanation": f"这是{verse['reference']}的重要经文"
                })
        
        # 构建章节数据
        processed_chapter = {
            "chapter": chapter_num,
            "title": chapter_data["title"],
            "subtitle": f"Chapter {chapter_num}",
            "content": content_text,
            "key_verses": processed_verses,
            "page_start": chapter_data.get("page_start", 1)
        }
        
        return processed_chapter
    
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
        
        .chapter-title {{
            font-size: 2.2rem;
            color: #2d3748;
            margin-bottom: 20px;
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
            line-height: 1.8;
            color: #2d3748;
            white-space: pre-line;
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
        </header>
        
        <section class="content-section">
            <h2 class="section-title">📖 课程内容</h2>
            <div class="original-content">{formatted_content}</div>
        </section>
        
        """ + (f'''
        <section class="content-section">
            <h2 class="section-title">✏️ 经文练习</h2>
            {verses_html}
        </section>
        ''' if verses_html else '') + """
        
        <div class="navigation">
            <button onclick="location.href='index.html'" class="nav-btn">🏠 返回主页</button>
            <button onclick="location.href='one2one_C{chapter_num-1 if chapter_num > 1 else 12}.html'" class="nav-btn">⬅️ 上一课</button>
            <button onclick="location.href='one2one_C{chapter_num+1 if chapter_num < 12 else 1}.html'" class="nav-btn">下一课 ➡️</button>
        </div>
    </div>
    
    <script>
        // 经文填空交互功能
        const chapterData = {json.dumps(chapter_data, ensure_ascii=False)};
        
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
                showMessage('🎉 ' + message, 'success');
            }} else if (percentage >= 80) {{
                showMessage('👍 ' + message, 'success');
            }} else {{
                showMessage('📚 ' + message, 'warning');
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
    
    def format_content_html(self, content: str) -> str:
        """格式化内容为HTML，保持原文格式"""
        # 简单的格式化：保持换行，突出显示经文引用
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 突出显示经文引用
            line = self.verse_pattern.sub(r'<strong style="color: #2b6cb0;">\1</strong>', line)
            
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

def main():
    """主函数"""
    print("🚀 开始提取一对一真实PDF内容...")
    
    extractor = One2OneRealExtractor()
    
    # 提取PDF内容
    pages_content = extractor.extract_full_pdf_content()
    
    if not pages_content:
        print("❌ 无法提取PDF内容")
        return
    
    # 识别章节
    chapters = extractor.identify_chapters(pages_content)
    
    print(f"📚 找到 {len(chapters)} 个章节")
    
    # 处理前几章作为示例
    for i, chapter_raw in enumerate(chapters[:3], 1):
        print(f"\n📝 处理第{i}章: {chapter_raw['title']}")
        
        # 处理章节数据
        chapter_data = extractor.process_real_chapter(chapter_raw, i)
        
        # 生成JSON数据
        json_file = os.path.join(extractor.data_dir, f"chapter{i}.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(chapter_data, f, ensure_ascii=False, indent=2)
        
        # 生成HTML页面
        html_content = extractor.generate_html_with_real_content(chapter_data)
        html_file = os.path.join(extractor.output_dir, f"one2one_C{i}.html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ 生成文件: {json_file}, {html_file}")
    
    print("\n🎉 一对一真实内容提取完成！")

if __name__ == "__main__":
    main()