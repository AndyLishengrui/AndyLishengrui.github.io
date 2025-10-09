#!/usr/bin/env python3
"""
一对一门徒训练课程提取和HTML生成工具

基于《一对一门徒训练》PDF文档，提取课程内容并生成交互式HTML页面
参考foundation模块的设计，包含经文填空、提示和答案检查功能
"""

import json
import re
import os
from typing import Dict, List, Any

class One2OneExtractor:
    def __init__(self, pdf_path: str = "一对一（大字版）.pdf"):
        self.pdf_path = pdf_path
        self.output_dir = "one2one"
        self.data_dir = os.path.join(self.output_dir, "data")
        
        # 确保目录存在
        os.makedirs(self.data_dir, exist_ok=True)
        
    def create_sample_data(self):
        """创建示例数据结构，基于一对一门徒训练的典型内容"""
        
        # 配置信息
        config = {
            "course_title": "一对一门徒训练",
            "description": "系统性门徒建造课程",
            "total_chapters": 12,
            "version": "1.0",
            "last_updated": "2024-10-09"
        }
        
        # 示例章节数据 - 第一章：救恩的确据
        chapter1_data = {
            "chapter": 1,
            "title": "救恩的确据",
            "subtitle": "Assurance of Salvation",
            "description": "帮助新信徒确认自己的救恩，建立信心基础",
            "key_verses": [
                {
                    "reference": "约翰福音3:16",
                    "text": "神爱世人，甚至将他的独生子赐给他们，叫一切信他的，不至___，反得____。",
                    "blanks": ["灭亡", "永生"],
                    "hints": ["m_w", "y_s"],
                    "explanation": "这是福音的核心经文，说明神的爱和救恩的途径"
                },
                {
                    "reference": "罗马书10:9",
                    "text": "你若口里___耶稣为主，心里___神叫他从死里复活，就必得救。",
                    "blanks": ["认", "信"],
                    "hints": ["r_n", "x_n"],
                    "explanation": "得救的两个条件：口里承认，心里相信"
                },
                {
                    "reference": "约翰一书5:13",
                    "text": "我将这些话写给你们___奉神儿子之名的人，要叫你们知道自己有___。",
                    "blanks": ["信", "永生"],
                    "hints": ["x_n", "y_s"],
                    "explanation": "救恩的确据来自神的话语"
                }
            ],
            "discussion_questions": [
                "你如何知道自己已经得救了？",
                "救恩是靠行为还是靠信心？为什么？",
                "如何向别人解释得救的条件？"
            ],
            "memory_verse": {
                "reference": "约翰福音3:16",
                "text": "神爱世人，甚至将他的独生子赐给他们，叫一切信他的，不至灭亡，反得永生。"
            }
        }
        
        # 第二章示例：祷告的生活
        chapter2_data = {
            "chapter": 2,
            "title": "祷告的生活",
            "subtitle": "Life of Prayer",
            "description": "建立日常祷告习惯，学习如何与神交通",
            "key_verses": [
                {
                    "reference": "马太福音6:9-11",
                    "text": "所以，你们祷告要这样说：我们在天上的___，愿人都尊你的名为圣。愿你的___降临；愿你的___行在地上，如同行在天上。我们日用的___，今日赐给我们。",
                    "blanks": ["父", "国", "旨意", "饮食"],
                    "hints": ["f_", "g_o", "z_y_", "y_n_s_"],
                    "explanation": "主祷文是耶稣教导门徒的祷告模式"
                },
                {
                    "reference": "腓立比书4:6-7",
                    "text": "应当一无___，只要凡事藉着___、___，和___，将你们所要的告诉神。神所赐、出人意外的___必在基督耶稣里保守你们的心怀意念。",
                    "blanks": ["挂虑", "祷告", "祈求", "感谢", "平安"],
                    "hints": ["g_l_", "d_g_o", "q_q_", "g_x_", "p_a_"],
                    "explanation": "祷告能带来神的平安"
                }
            ],
            "discussion_questions": [
                "为什么祷告很重要？",
                "你通常为什么事情祷告？",
                "如何建立稳定的祷告生活？"
            ],
            "memory_verse": {
                "reference": "腓立比书4:6",
                "text": "应当一无挂虑，只要凡事藉着祷告、祈求，和感谢，将你们所要的告诉神。"
            }
        }
        
        # 保存数据文件
        with open(os.path.join(self.data_dir, "config.json"), "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
            
        with open(os.path.join(self.data_dir, "chapter1.json"), "w", encoding="utf-8") as f:
            json.dump(chapter1_data, f, ensure_ascii=False, indent=2)
            
        with open(os.path.join(self.data_dir, "chapter2.json"), "w", encoding="utf-8") as f:
            json.dump(chapter2_data, f, ensure_ascii=False, indent=2)
            
        print("✅ 创建示例数据完成")
        return [chapter1_data, chapter2_data]
    
    def generate_html_template(self, chapter_data: Dict[str, Any]) -> str:
        """生成HTML页面模板，参考foundation模块的设计"""
        
        chapter_num = chapter_data["chapter"]
        title = chapter_data["title"]
        subtitle = chapter_data["subtitle"]
        
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
        
        # 生成讨论问题HTML
        questions_html = ""
        for i, question in enumerate(chapter_data["discussion_questions"]):
            questions_html += f'<li class="discussion-item">{question}</li>'
        
        html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>第{chapter_num}章: {title} - 一对一门徒训练</title>
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
            color: #718096;
            margin-bottom: 15px;
            font-style: italic;
        }}
        
        .chapter-description {{
            color: #4a5568;
            font-size: 1rem;
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
        
        .verse-explanation {{
            color: #718096;
            font-size: 0.9rem;
            font-style: italic;
            margin-bottom: 15px;
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
        
        .discussion-list {{
            list-style: none;
            padding: 0;
        }}
        
        .discussion-item {{
            background: #f0f4f8;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        
        .memory-verse {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
        }}
        
        .memory-verse .reference {{
            font-weight: bold;
            margin-bottom: 10px;
            font-size: 1.1rem;
        }}
        
        .memory-verse .text {{
            font-size: 1.2rem;
            line-height: 1.8;
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
            <h1 class="chapter-title">第{chapter_num}章: {title}</h1>
            <p class="chapter-subtitle">{subtitle}</p>
            <p class="chapter-description">{chapter_data["description"]}</p>
        </header>
        
        <section class="content-section">
            <h2 class="section-title">📖 核心经文练习</h2>
            {verses_html}
        </section>
        
        <section class="content-section">
            <h2 class="section-title">💬 讨论问题</h2>
            <ul class="discussion-list">
                {questions_html}
            </ul>
        </section>
        
        <section class="content-section">
            <h2 class="section-title">🎯 背诵经文</h2>
            <div class="memory-verse">
                <div class="reference">{chapter_data["memory_verse"]["reference"]}</div>
                <div class="text">{chapter_data["memory_verse"]["text"]}</div>
            </div>
        </section>
        
        <div class="navigation">
            <button onclick="location.href='index.html'" class="nav-btn">🏠 返回主页</button>
            <button onclick="location.href='one2one_C{chapter_num-1 if chapter_num > 1 else 12}.html'" class="nav-btn">⬅️ 上一章</button>
            <button onclick="location.href='one2one_C{chapter_num+1 if chapter_num < 12 else 1}.html'" class="nav-btn">下一章 ➡️</button>
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
                if (verse.hints[index]) {{
                    input.placeholder = verse.hints[index];
                }}
            }});
            
            // 显示提示消息
            showMessage('💡 已显示提示，请根据提示填写答案', 'info');
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
                showMessage('🎉 ' + message + ' 全部正确！', 'success');
            }} else if (percentage >= 80) {{
                showMessage('👍 ' + message + ' 很好！', 'success');
            }} else {{
                showMessage('📚 ' + message + ' 继续努力！', 'warning');
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
            // 创建消息提示
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
                animation: slideIn 0.3s ease-out;
                ${{type === 'success' ? 'background: #48bb78;' :
                  type === 'warning' ? 'background: #ed8936;' :
                  'background: #4299e1;'}}
            `;
            
            document.body.appendChild(messageDiv);
            
            setTimeout(() => {{
                messageDiv.remove();
            }}, 3000);
        }}
        
        // 添加CSS动画
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {{
                from {{
                    transform: translateX(100%);
                    opacity: 0;
                }}
                to {{
                    transform: translateX(0);
                    opacity: 1;
                }}
            }}
        `;
        document.head.appendChild(style);
        
        // 自动保存进度
        function saveProgress() {{
            const inputs = document.querySelectorAll('.blank-input');
            const progress = {{}};
            
            inputs.forEach((input, index) => {{
                if (input.value.trim()) {{
                    progress[`input_${{index}}`] = input.value;
                }}
            }});
            
            localStorage.setItem('one2one_chapter_{chapter_num}_progress', JSON.stringify(progress));
        }}
        
        // 加载进度
        function loadProgress() {{
            const saved = localStorage.getItem('one2one_chapter_{chapter_num}_progress');
            if (saved) {{
                const progress = JSON.parse(saved);
                const inputs = document.querySelectorAll('.blank-input');
                
                inputs.forEach((input, index) => {{
                    if (progress[`input_${{index}}`]) {{
                        input.value = progress[`input_${{index}}`];
                    }}
                }});
            }}
        }}
        
        // 页面加载完成后
        document.addEventListener('DOMContentLoaded', function() {{
            loadProgress();
            
            // 为所有输入框添加自动保存
            document.querySelectorAll('.blank-input').forEach(input => {{
                input.addEventListener('input', saveProgress);
            }});
        }});
    </script>
</body>
</html>'''
        
        return html_content
    
    def create_blanks_html(self, verse_data: Dict[str, Any], verse_id: str) -> str:
        """将经文文本转换为带填空的HTML"""
        text = verse_data["text"]
        blanks = verse_data["blanks"]
        
        # 替换下划线为输入框
        blank_index = 0
        result = ""
        i = 0
        
        while i < len(text):
            if text[i:i+3] == "___" or text[i:i+4] == "____":
                # 确定下划线长度
                underscores = 3 if text[i:i+3] == "___" else 4
                
                if blank_index < len(blanks):
                    width = max(60, len(blanks[blank_index]) * 12 + 20)
                    result += f'<input type="text" class="blank-input" style="width:{width}px;" data-answer="{blanks[blank_index]}" />'
                    blank_index += 1
                else:
                    result += "_" * underscores
                
                i += underscores
            else:
                result += text[i]
                i += 1
        
        return result

def main():
    """主函数"""
    print("🚀 开始创建一对一门徒训练系统...")
    
    extractor = One2OneExtractor()
    
    # 创建示例数据
    chapters_data = extractor.create_sample_data()
    
    # 为每个章节生成HTML页面
    for chapter_data in chapters_data:
        chapter_num = chapter_data["chapter"]
        html_content = extractor.generate_html_template(chapter_data)
        
        output_file = os.path.join(extractor.output_dir, f"one2one_C{chapter_num}.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ 生成第{chapter_num}章页面: {output_file}")
    
    print("\n🎉 一对一门徒训练系统创建完成！")
    print(f"📁 项目目录: {extractor.output_dir}")
    print("🌐 请创建主页 index.html 来导航各章节")

if __name__ == "__main__":
    main()