#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成第一课的交互式HTML文件
保留Word文档完整内容,在经文处添加填空
"""

import json
import re

# HTML模板
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | 一对一门徒训练</title>
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
            line-height: 1.8;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 40px;
        }}

        .breadcrumb {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
        }}

        .breadcrumb a {{
            color: white;
            text-decoration: none;
        }}

        .breadcrumb a:hover {{
            text-decoration: underline;
        }}

        h1 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}

        .section-info {{
            font-size: 0.95em;
            opacity: 0.9;
        }}

        .content {{
            padding: 40px;
        }}

        .section-title {{
            font-size: 1.6em;
            color: #667eea;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid #667eea;
        }}

        .text-block {{
            margin-bottom: 25px;
            font-size: 1.05em;
            line-height: 2;
            color: #333;
            text-indent: 2em;
        }}

        .subtitle {{
            font-size: 1.3em;
            font-weight: 600;
            color: #764ba2;
            margin: 30px 0 20px 0;
        }}

        .verse-container {{
            background: #f8f9ff;
            padding: 25px;
            border-radius: 10px;
            margin: 25px 0;
            border-left: 4px solid #667eea;
        }}

        .verse-text {{
            font-size: 1.1em;
            line-height: 2.2;
            color: #333;
            margin-bottom: 15px;
        }}

        .blank {{
            display: inline-block;
            min-width: 60px;
            padding: 2px 10px;
            border-bottom: 2px solid #667eea;
            margin: 0 3px;
            font-weight: 600;
            color: #667eea;
            cursor: pointer;
            transition: all 0.3s;
        }}

        .blank:hover {{
            background: #e8ebff;
        }}

        .blank.filled {{
            background: #e8ebff;
            border-bottom-color: #10b981;
        }}

        .blank.correct {{
            background: #d1fae5;
            border-bottom-color: #10b981;
            color: #065f46;
        }}

        .blank.wrong {{
            background: #fee2e2;
            border-bottom-color: #ef4444;
            color: #991b1b;
        }}

        .verse-reference {{
            text-align: right;
            font-style: italic;
            color: #888;
            font-size: 0.95em;
            margin-top: 10px;
        }}

        .input-section {{
            position: sticky;
            bottom: 0;
            background: white;
            padding: 20px;
            border-top: 2px solid #e8e8e8;
            box-shadow: 0 -5px 20px rgba(0,0,0,0.05);
        }}

        .input-controls {{
            display: flex;
            gap: 15px;
            align-items: center;
            max-width: 900px;
            margin: 0 auto;
        }}

        #answer-input {{
            flex: 1;
            padding: 12px 20px;
            border: 2px solid #667eea;
            border-radius: 8px;
            font-size: 1em;
        }}

        .btn {{
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }}

        .btn-check {{
            background: #667eea;
            color: white;
        }}

        .btn-check:hover {{
            background: #5568d3;
            transform: translateY(-2px);
        }}

        .btn-reset {{
            background: #94a3b8;
            color: white;
        }}

        .btn-submit {{
            background: #10b981;
            color: white;
        }}

        .score-display {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 15px 25px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            font-weight: 600;
            z-index: 1000;
        }}

        .score-number {{
            font-size: 2em;
            color: #667eea;
        }}

        .navigation {{
            display: flex;
            justify-content: space-between;
            padding: 25px 40px;
            background: #f8f9fa;
            border-top: 2px solid #e8e8e8;
        }}

        .nav-btn {{
            padding: 12px 30px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 8px;
            border: 2px solid #667eea;
            font-weight: 600;
            transition: all 0.3s;
        }}

        .nav-btn:hover {{
            background: #667eea;
            color: white;
        }}

        .feedback {{
            margin-top: 15px;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
            display: none;
        }}

        .feedback.show {{
            display: block;
        }}

        .feedback.success {{
            background: #d1fae5;
            color: #065f46;
        }}

        .feedback.error {{
            background: #fee2e2;
            color: #991b1b;
        }}

        @media (max-width: 768px) {{
            .container {{
                border-radius: 0;
            }}
            
            header, .content, .navigation {{
                padding: 25px;
            }}
            
            h1 {{
                font-size: 1.5em;
            }}
            
            .input-controls {{
                flex-direction: column;
            }}
            
            .score-display {{
                position: static;
                margin-bottom: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="score-display">
        得分: <span class="score-number" id="score">0</span>/100
    </div>

    <div class="container">
        <header>
            <div class="breadcrumb">
                <a href="../index.html">首页</a> / <a href="index.html">第一课</a> / {section_name}
            </div>
            <h1>新起点 - 得救</h1>
            <div class="section-info">{section_info}</div>
        </header>

        <div class="content">
            {content_html}
        </div>

        <div class="input-section">
            <div class="input-controls">
                <input type="text" id="answer-input" placeholder="输入答案后点击填空处...">
                <button class="btn btn-check" onclick="checkAnswers()">检查答案</button>
                <button class="btn btn-reset" onclick="resetAll()">重新开始</button>
                <button class="btn btn-submit" onclick="submitAnswers()">提交</button>
            </div>
            <div class="feedback" id="feedback"></div>
        </div>

        <div class="navigation">
            <a href="{prev_link}" class="nav-btn">← 上一节</a>
            <a href="{next_link}" class="nav-btn">下一节 →</a>
        </div>
    </div>

    <script>
        let blanks = {blanks_data};
        let currentBlankIndex = null;
        let userAnswers = {{}};

        // 初始化
        document.addEventListener('DOMContentLoaded', function() {{
            // 为每个填空添加点击事件
            document.querySelectorAll('.blank').forEach(blank => {{
                blank.addEventListener('click', function() {{
                    currentBlankIndex = this.dataset.id;
                    document.getElementById('answer-input').focus();
                    this.style.background = '#fff3cd';
                }});
            }});

            // 输入框回车填入答案
            document.getElementById('answer-input').addEventListener('keypress', function(e) {{
                if (e.key === 'Enter' && currentBlankIndex !== null) {{
                    fillBlank();
                }}
            }});
        }});

        function fillBlank() {{
            if (currentBlankIndex === null) return;
            
            const input = document.getElementById('answer-input');
            const answer = input.value.trim();
            
            if (!answer) return;
            
            const blank = document.querySelector(`[data-id="${{currentBlankIndex}}"]`);
            blank.textContent = answer;
            blank.classList.add('filled');
            blank.style.background = '#e8ebff';
            
            userAnswers[currentBlankIndex] = answer;
            
            input.value = '';
            currentBlankIndex = null;
            
            updateScore();
        }}

        function checkAnswers() {{
            let correct = 0;
            let total = blanks.length;
            
            blanks.forEach(blank => {{
                const blankElem = document.querySelector(`[data-id="${{blank.id}}"]`);
                const userAnswer = userAnswers[blank.id] || '';
                
                if (userAnswer === blank.answer) {{
                    blankElem.classList.remove('wrong');
                    blankElem.classList.add('correct');
                    correct++;
                }} else if (userAnswer) {{
                    blankElem.classList.remove('correct');
                    blankElem.classList.add('wrong');
                }}
            }});
            
            const score = Math.round((correct / total) * 100);
            document.getElementById('score').textContent = score;
            
            const feedback = document.getElementById('feedback');
            feedback.className = 'feedback show ' + (score >= 60 ? 'success' : 'error');
            feedback.textContent = score >= 60 ? 
                `太棒了！您答对了 ${{correct}}/${{total}} 题，得分 ${{score}} 分！` :
                `继续加油！您答对了 ${{correct}}/${{total}} 题，得分 ${{score}} 分。`;
        }}

        function resetAll() {{
            document.querySelectorAll('.blank').forEach(blank => {{
                const id = blank.dataset.id;
                const originalAnswer = blanks.find(b => b.id === id).answer;
                blank.textContent = '____';
                blank.className = 'blank';
            }});
            
            userAnswers = {{}};
            document.getElementById('score').textContent = '0';
            document.getElementById('answer-input').value = '';
            document.getElementById('feedback').className = 'feedback';
            currentBlankIndex = null;
        }}

        function updateScore() {{
            let correct = 0;
            let total = blanks.length;
            
            blanks.forEach(blank => {{
                const userAnswer = userAnswers[blank.id] || '';
                if (userAnswer === blank.answer) {{
                    correct++;
                }}
            }});
            
            const score = Math.round((correct / total) * 100);
            document.getElementById('score').textContent = score;
        }}

        function submitAnswers() {{
            checkAnswers();
            
            setTimeout(() => {{
                const score = parseInt(document.getElementById('score').textContent);
                if (score >= 60) {{
                    if (confirm('恭喜你完成本节学习！是否继续下一节？')) {{
                        window.location.href = '{next_link}';
                    }}
                }} else {{
                    alert('建议您再复习一下，争取达到60分以上！');
                }}
            }}, 500);
        }}
    </script>
</body>
</html>
'''

def create_verse_with_blanks(verse_text):
    """为经文创建填空"""
    # 关键词列表
    keywords = ['神', '耶稣', '基督', '罪', '信', '永生', '死', '救', '恩典', '血', '义', '爱']
    
    blanks = []
    result = verse_text
    
    for keyword in keywords:
        if keyword in result and len(blanks) < 5:
            blank_id = len(blanks)
            result = result.replace(keyword, f'<span class="blank" data-id="{blank_id}">____</span>', 1)
            blanks.append({'id': blank_id, 'answer': keyword})
    
    return result, blanks

def generate_content_html(section_data):
    """生成内容HTML"""
    html_parts = []
    all_blanks = []
    
    if section_data.get('title') and section_data['title'] != '引言':
        html_parts.append(f'<h2 class="section-title">{section_data["title"]}</h2>')
    
    for item in section_data['content']:
        if item['type'] == 'text':
            html_parts.append(f'<p class="text-block">{item["text"]}</p>')
        elif item['type'] == 'subtitle':
            html_parts.append(f'<h3 class="subtitle">{item["text"]}</h3>')
        elif item['type'] == 'verse':
            verse_text = item['text']
            # 检查是否是经文出处
            if '）' in verse_text or '(' in verse_text or '书' in verse_text:
                html_parts.append(f'<div class="verse-reference">{verse_text}</div>')
            else:
                # 创建填空
                verse_with_blanks, blanks = create_verse_with_blanks(verse_text)
                
                # 更新blank的ID
                for blank in blanks:
                    blank['id'] = len(all_blanks)
                    all_blanks.append(blank)
                
                # 更新HTML中的ID
                for i, blank in enumerate(blanks):
                    old_id = i
                    new_id = blank['id']
                    verse_with_blanks = verse_with_blanks.replace(
                        f'data-id="{old_id}"',
                        f'data-id="{new_id}"'
                    )
                
                html_parts.append(f'''<div class="verse-container">
                    <div class="verse-text">{verse_with_blanks}</div>
                </div>''')
    
    return '\n'.join(html_parts), all_blanks

def generate_html_files():
    """生成所有HTML文件"""
    
    # 读取结构化数据
    with open('/Users/andyshengruilee/Documents/website/web2Lord/one2one/lesson1_structured.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sections = data['sections']
    distribution = data['distribution']
    
    # 生成6个HTML文件
    for section_key, section_indices in distribution.items():
        section_num = int(section_key[1])
        
        # 合并多个章节的内容
        combined_content = []
        section_titles = []
        
        for idx in section_indices:
            if idx < len(sections):
                combined_content.extend(sections[idx]['content'])
                section_titles.append(sections[idx]['title'])
        
        section_data = {
            'title': ' + '.join(section_titles) if len(section_titles) > 1 else section_titles[0],
            'content': combined_content
        }
        
        # 生成内容HTML和填空数据
        content_html, blanks = generate_content_html(section_data)
        
        # 导航链接
        prev_link = f'one2one_C1_S{section_num-1}.html' if section_num > 1 else 'index.html'
        next_link = f'one2one_C1_S{section_num+1}.html' if section_num < 6 else '../one2one_C2_S1.html'
        
        # 生成HTML
        html_content = HTML_TEMPLATE.format(
            title=f'新起点 - 得救 - 第{section_num}节',
            section_name=f'第{section_num}节',
            section_info=f'第 {section_num} / 6 节',
            content_html=content_html,
            blanks_data=json.dumps(blanks, ensure_ascii=False),
            prev_link=prev_link,
            next_link=next_link
        )
        
        # 保存文件
        output_path = f'/Users/andyshengruilee/Documents/website/web2Lord/one2one/courses/one2one_C1_S{section_num}.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f'✅ 生成: one2one_C1_S{section_num}.html ({len(blanks)} 个填空)')

def main():
    print("="*80)
    print("开始生成第一课HTML文件...")
    print("="*80)
    
    generate_html_files()
    
    print("\n" + "="*80)
    print("生成完成!")
    print("="*80)

if __name__ == "__main__":
    main()
