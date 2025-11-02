#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成第一课的6个HTML页面
基于course_1_structure.json中的真实章节结构
"""

import json
import os

def create_verse_blanks(verse_text, reference):
    """创建经文填空"""
    # 选择关键词作为填空
    keywords = {
        '约翰福音 3:16': ['神', '独生子', '信', '永生'],
        '以赛亚书 59:1,2': ['罪孽', '隔绝', '掩面'],
        '马太福音 5:21,22': ['杀人', '发怒', '审判'],
        '马太福音 5:27,28': ['通奸', '淫念', '心里'],
        '罗马书 3:23': ['犯了罪', '亏缺', '荣耀'],
        '罗马书 6:23': ['罪', '死亡', '永生'],
        '罗马书 5:8': ['罪人', '基督', '替我们死'],
        '希伯来书 9:26-28': ['献上', '除去', '承担', '救恩'],
        '哥林多后书 5:21': ['没有罪', '替我们', '神的义'],
        '加拉太书 3:13': ['诅咒', '救赎', '木头'],
        '以弗所书 1:7': ['血', '救赎', '赦免', '恩典'],
        '以弗所书 2:13': ['血', '重归神', '亲近'],
        '罗马书 10:9,10': ['宣认', '耶稣为主', '复活', '得救'],
        '以弗所书 2:8,9': ['得救', '恩', '信', '行为'],
        '哥林多后书 5:17': ['基督', '新造的人', '旧事', '新的']
    }
    
    blanks = keywords.get(reference, [])
    result = verse_text
    
    for keyword in blanks:
        if keyword in result:
            result = result.replace(keyword, f'<span class="blank" data-answer="{keyword}">____</span>', 1)
    
    return result

def generate_section_html(section, course_num, total_sections):
    """生成单个章节的HTML"""
    section_num = section['section_number']
    title = section['title']
    description = section.get('description', '')
    
    # 导航链接 - 修正文件名格式
    prev_link = f'one2one_C{course_num}_S{section_num-1}.html' if section_num > 1 else 'index.html'
    next_link = f'one2one_C{course_num}_S{section_num+1}.html' if section_num < total_sections else 'index.html'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 第{section_num}节</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
            line-height: 1.8;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .course-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 14px;
            margin-bottom: 15px;
        }}
        
        h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .section-info {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .description {{
            background: #f8f9ff;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
            line-height: 2;
            white-space: pre-wrap;
        }}
        
        .verse-section {{
            margin-bottom: 35px;
            padding: 25px;
            background: #fff;
            border-radius: 12px;
            border: 2px solid #e8e8e8;
            transition: all 0.3s;
        }}
        
        .verse-section:hover {{
            border-color: #667eea;
            box-shadow: 0 5px 20px rgba(102,126,234,0.1);
        }}
        
        .verse-text {{
            font-size: 18px;
            line-height: 2;
            color: #333;
            margin-bottom: 15px;
        }}
        
        .blank {{
            display: inline-block;
            min-width: 80px;
            height: 32px;
            border-bottom: 2px solid #667eea;
            margin: 0 5px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            position: relative;
        }}
        
        .blank:hover {{
            background: #f0f4ff;
        }}
        
        .blank.filled {{
            border-bottom-color: #10b981;
            color: #10b981;
        }}
        
        .blank.wrong {{
            border-bottom-color: #ef4444;
            color: #ef4444;
        }}
        
        .verse-reference {{
            text-align: right;
            color: #667eea;
            font-weight: 600;
            font-size: 15px;
        }}
        
        .input-section {{
            margin-top: 30px;
            padding: 25px;
            background: #f8f9ff;
            border-radius: 12px;
        }}
        
        input[type="text"] {{
            width: 100%;
            padding: 12px 20px;
            border: 2px solid #e8e8e8;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s;
        }}
        
        input[type="text"]:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
        }}
        
        .button-group {{
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }}
        
        button {{
            flex: 1;
            padding: 14px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 600;
        }}
        
        .btn-check {{
            background: #667eea;
            color: white;
        }}
        
        .btn-check:hover {{
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102,126,234,0.3);
        }}
        
        .btn-reset {{
            background: #94a3b8;
            color: white;
        }}
        
        .btn-reset:hover {{
            background: #64748b;
        }}
        
        .navigation {{
            display: flex;
            justify-content: space-between;
            padding: 30px 40px;
            background: #f8f9ff;
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
            transform: translateY(-2px);
        }}
        
        .feedback {{
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
            display: none;
        }}
        
        .feedback.success {{
            background: #d1fae5;
            color: #065f46;
            display: block;
        }}
        
        .feedback.error {{
            background: #fee2e2;
            color: #991b1b;
            display: block;
        }}
        
        .progress {{
            position: fixed;
            top: 0;
            left: 0;
            height: 4px;
            background: #10b981;
            transition: width 0.3s;
            z-index: 1000;
        }}

        .application-section {{
            background: #fef3c7;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            border-left: 4px solid #f59e0b;
        }}

        .application-section h3 {{
            color: #92400e;
            margin-bottom: 20px;
            font-size: 20px;
        }}

        .application-section ul {{
            list-style: none;
            padding-left: 0;
        }}

        .application-section li {{
            padding: 12px 0;
            padding-left: 30px;
            position: relative;
            color: #78350f;
            font-size: 16px;
        }}

        .application-section li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: #f59e0b;
            font-weight: bold;
            font-size: 20px;
        }}

        .prayer-section {{
            background: #dbeafe;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            border-left: 4px solid #3b82f6;
        }}

        .prayer-section h3 {{
            color: #1e40af;
            margin-bottom: 20px;
            font-size: 20px;
        }}

        .prayer-text {{
            color: #1e3a8a;
            line-height: 2;
            font-size: 16px;
            white-space: pre-wrap;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                border-radius: 0;
            }}
            
            .header, .content, .navigation {{
                padding: 25px;
            }}
            
            h1 {{
                font-size: 24px;
            }}
            
            .button-group {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="progress" id="progress"></div>
    
    <div class="container">
        <div class="header">
            <div class="course-badge">第一课：新起点 - 得救</div>
            <h1>{title}</h1>
            <div class="section-info">第 {section_num} / {total_sections} 节</div>
        </div>
        
        <div class="content">
            <div class="description">{description}</div>
'''
    
    # 添加经文部分
    if 'verses' in section:
        for idx, verse in enumerate(section['verses'], 1):
            verse_with_blanks = create_verse_blanks(verse['content'], verse['reference'])
            html += f'''
            <div class="verse-section" data-verse-id="{idx}">
                <div class="verse-text">{verse_with_blanks}</div>
                <div class="verse-reference">{verse['reference']} ({verse['version']})</div>
            </div>
'''
    elif 'content' in section:  # 第一节的单个经文
        verse_with_blanks = create_verse_blanks(section['content'], section['verse_reference'])
        html += f'''
            <div class="verse-section" data-verse-id="1">
                <div class="verse-text">{verse_with_blanks}</div>
                <div class="verse-reference">{section['verse_reference']} ({section['verse_version']})</div>
            </div>
'''
    
    # 添加个人应用部分
    if 'application_questions' in section:
        html += '''
            <div class="application-section">
                <h3>💭 个人应用</h3>
                <ul>
'''
        for question in section['application_questions']:
            html += f'                    <li>{question}</li>\n'
        html += '''                </ul>
            </div>
'''
    
    # 添加祷告部分
    if 'prayer' in section:
        html += f'''
            <div class="prayer-section">
                <h3>🙏 得救的祷告</h3>
                <div class="prayer-text">{section['prayer']}</div>
            </div>
'''
    
    # 添加最后的经文（如果有）
    if 'verse' in section:
        verse = section['verse']
        verse_with_blanks = create_verse_blanks(verse['content'], verse['reference'])
        html += f'''
            <div class="verse-section" data-verse-id="final">
                <div class="verse-text">{verse_with_blanks}</div>
                <div class="verse-reference">{verse['reference']} ({verse['version']})</div>
            </div>
'''
    
    # 添加填空输入和按钮（只有在有填空时才显示）
    html += '''
            <div class="input-section">
                <input type="text" id="answer-input" placeholder="请输入答案，然后点击填空处填入...">
                <div class="button-group">
                    <button class="btn-check" onclick="checkAnswers()">检查答案</button>
                    <button class="btn-reset" onclick="resetAll()">重新开始</button>
                </div>
                <div class="feedback" id="feedback"></div>
            </div>
        </div>
        
        <div class="navigation">
'''
    
    # 导航按钮
    html += f'            <a href="{prev_link}" class="nav-btn">← 上一节</a>\n'
    html += f'            <a href="{next_link}" class="nav-btn">下一节 →</a>\n'
    
    html += '''        </div>
    </div>
    
    <script>
        let currentBlank = null;
        
        // 更新进度条
        function updateProgress() {
            const blanks = document.querySelectorAll('.blank');
            const filled = document.querySelectorAll('.blank.filled').length;
            const progress = blanks.length > 0 ? (filled / blanks.length) * 100 : 0;
            document.getElementById('progress').style.width = progress + '%';
        }
        
        // 点击填空处
        document.querySelectorAll('.blank').forEach(blank => {
            blank.addEventListener('click', function() {
                // 移除其他填空的选中状态
                document.querySelectorAll('.blank').forEach(b => b.style.background = '');
                
                // 选中当前填空
                currentBlank = this;
                this.style.background = '#f0f4ff';
                
                // 聚焦输入框
                document.getElementById('answer-input').focus();
            });
        });
        
        // 输入框回车事件
        document.getElementById('answer-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && currentBlank) {
                const answer = this.value.trim();
                if (answer) {
                    currentBlank.textContent = answer;
                    currentBlank.classList.remove('wrong');
                    currentBlank.classList.add('filled');
                    currentBlank.style.background = '';
                    this.value = '';
                    currentBlank = null;
                    updateProgress();
                }
            }
        });
        
        // 检查答案
        function checkAnswers() {
            const blanks = document.querySelectorAll('.blank');
            let correct = 0;
            let total = 0;
            
            blanks.forEach(blank => {
                total++;
                const userAnswer = blank.textContent.trim();
                const correctAnswer = blank.dataset.answer;
                
                if (userAnswer === correctAnswer) {
                    blank.classList.remove('wrong');
                    blank.classList.add('filled');
                    correct++;
                } else if (userAnswer && userAnswer !== '____') {
                    blank.classList.remove('filled');
                    blank.classList.add('wrong');
                }
            });
            
            const feedback = document.getElementById('feedback');
            if (correct === total) {
                feedback.className = 'feedback success';
                feedback.textContent = '🎉 太棒了！全部正确！';
            } else {
                feedback.className = 'feedback error';
                feedback.textContent = `答对了 ${correct}/${total} 个，继续努力！`;
            }
            
            updateProgress();
        }
        
        // 重新开始
        function resetAll() {
            document.querySelectorAll('.blank').forEach(blank => {
                blank.textContent = '____';
                blank.classList.remove('filled', 'wrong');
                blank.style.background = '';
            });
            
            document.getElementById('answer-input').value = '';
            document.getElementById('feedback').className = 'feedback';
            currentBlank = null;
            updateProgress();
        }
        
        // 初始化进度
        updateProgress();
    </script>
</body>
</html>'''
    
    return html

def main():
    # 读取结构文件
    with open('course_1_structure.json', 'r', encoding='utf-8') as f:
        course_data = json.load(f)
    
    sections = course_data['sections']
    total_sections = len(sections)
    
    # 生成每个章节的HTML
    for section in sections:
        section_num = section['section_number']
        html = generate_section_html(section, 1, total_sections)
        
        # 保存文件到courses目录
        output_dir = 'courses'
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f'{output_dir}/one2one_C1_S{section_num}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f'✅ 已生成: {filename}')
    
    print(f'\n🎉 完成！共生成 {total_sections} 个HTML文件')

if __name__ == '__main__':
    main()
