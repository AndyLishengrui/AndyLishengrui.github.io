#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成建立根基课程的学习页面
为每一节生成一个独立的HTML页面
"""

import json
import os

def generate_section_pages():
    """为每一节生成独立的学习页面"""
    
    # 读取课程数据
    with open('data/foundation_course.json', 'r', encoding='utf-8') as f:
        course_data = json.load(f)
    
    # 合并重复的课程
    unique_lessons = {}
    for lesson in course_data['lessons']:
        lesson_id = lesson['id']
        if lesson_id not in unique_lessons:
            unique_lessons[lesson_id] = lesson
        else:
            # 合并节
            unique_lessons[lesson_id]['sections'].extend(lesson['sections'])
    
    lessons = sorted(unique_lessons.values(), key=lambda x: x['id'])
    
    print(f"开始生成课程页面...")
    print(f"共 {len(lessons)} 课")
    
    total_pages = 0
    
    # 为每一课的每一节生成页面
    for lesson in lessons:
        lesson_id = lesson['id']
        lesson_title = lesson['title']
        
        print(f"\n第{lesson_id}课: {lesson_title}")
        print(f"  共 {len(lesson['sections'])} 节")
        
        for section_idx, section in enumerate(lesson['sections']):
            section_id = section['id']
            section_title = section['title']
            
            # 清理节标题（去掉下划线）
            if '_' in section_title and len(section_title) > 20:
                section_title = f"第{section_id}节"
            
            # 确定上一节和下一节
            prev_section = None
            next_section = None
            
            if section_idx > 0:
                prev_section = {
                    'lesson_id': lesson_id,
                    'section_num': section_idx,
                    'title': lesson['sections'][section_idx - 1]['title']
                }
            elif lesson_id > 1:
                # 上一课的最后一节
                prev_lesson = lessons[lesson_id - 2]
                if prev_lesson['sections']:
                    last_section_idx = len(prev_lesson['sections']) - 1
                    prev_section = {
                        'lesson_id': lesson_id - 1,
                        'section_num': last_section_idx + 1,
                        'title': prev_lesson['sections'][last_section_idx]['title']
                    }
            
            if section_idx < len(lesson['sections']) - 1:
                next_section = {
                    'lesson_id': lesson_id,
                    'section_num': section_idx + 2,
                    'title': lesson['sections'][section_idx + 1]['title']
                }
            elif lesson_id < len(lessons):
                # 下一课的第一节
                next_lesson = lessons[lesson_id]
                if next_lesson['sections']:
                    next_section = {
                        'lesson_id': lesson_id + 1,
                        'section_num': 1,
                        'title': next_lesson['sections'][0]['title']
                    }
            
            # 生成页面
            filename = f"foundation_L{lesson_id}_S{section_idx + 1}.html"
            generate_section_html(
                filename,
                lesson_id,
                lesson_title,
                section_idx + 1,
                section,
                prev_section,
                next_section
            )
            
            total_pages += 1
            print(f"    ✓ 第{section_idx + 1}节: {section_title[:30]}")
    
    print(f"\n✓ 共生成 {total_pages} 个页面")


def generate_section_html(filename, lesson_id, lesson_title, section_num, section, prev_section, next_section):
    """生成单个节的HTML页面"""
    
    section_title = section['title']
    if '_' in section_title and len(section_title) > 20:
        section_title = f"第{section_num}节"
    
    questions_html = ""
    for q in section['questions']:
        question_id = q['id']
        question_text = q['question']
        references = q.get('references', [])
        blanks = q.get('blanks', 1)
        
        # 生成经文引用和填空行（每个引用后跟一个填空行）
        refs_and_blanks_html = ""
        if references:
            for ref in references:
                refs_and_blanks_html += f'''
                <div class="reference-with-blank">
                    <span class="reference-text">{ref}</span>
                    <input type="text" 
                           class="answer-input" 
                           data-question="{question_id}" 
                           data-reference="{ref}"
                           placeholder="">
                </div>
                '''
        else:
            # 没有经文引用时，显示一个填空行
            refs_and_blanks_html = f'''
                <div class="reference-with-blank">
                    <input type="text" 
                           class="answer-input full-width" 
                           data-question="{question_id}" 
                           placeholder="">
                </div>
            '''
        
        questions_html += f'''
            <div class="question-block" data-question-id="{question_id}">
                <div class="question-header">
                    <span class="question-number">{question_id}.</span>
                    <span class="question-text">{question_text}</span>
                </div>
                <div class="answers-area">
                    {refs_and_blanks_html}
                </div>
            </div>
        '''
    
    # 个人应用部分
    application_text = section.get('application', '')
    if not application_text or len(application_text) < 20:
        application_text = "请根据本节内容，写下你的个人应用和具体行动计划。"
    
    application_html = f'''
        <div class="application-section">
            <h3>个人应用</h3>
            <p class="application-prompt">{application_text}</p>
            <textarea class="application-input" 
                      placeholder="写下你的思考、感受和具体的行动计划..."
                      rows="6"></textarea>
        </div>
    '''
    
    # 导航按钮
    nav_buttons = ""
    if prev_section:
        nav_buttons += f'''
            <a href="foundation_L{prev_section['lesson_id']}_S{prev_section['section_num']}.html" 
               class="nav-btn prev-btn">
                ← 上一节
            </a>
        '''
    
    nav_buttons += f'''
        <a href="foundation_course.html" class="nav-btn home-btn">
            返回目录
        </a>
    '''
    
    if next_section:
        nav_buttons += f'''
            <a href="foundation_L{next_section['lesson_id']}_S{next_section['section_num']}.html" 
               class="nav-btn next-btn">
                下一节 →
            </a>
        '''
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{lesson_title} - 第{section_num}节 | 建立根基</title>
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
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}

        header {{
            background: white;
            border-radius: 15px 15px 0 0;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .breadcrumb {{
            color: #888;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}

        .breadcrumb a {{
            color: #667eea;
            text-decoration: none;
        }}

        .breadcrumb a:hover {{
            text-decoration: underline;
        }}

        h1 {{
            color: #333;
            margin-bottom: 15px;
            font-size: 2em;
        }}

        .section-title-box {{
            display: inline-flex;
            align-items: center;
            gap: 15px;
            margin-top: 15px;
        }}

        .section-label {{
            display: inline-block;
            border: 2px solid #333;
            padding: 8px 20px;
            font-size: 1.1em;
            font-weight: 500;
            color: #333;
        }}

        .section-name {{
            font-size: 1.3em;
            color: #333;
            font-weight: 500;
        }}

        .content {{
            background: white;
            padding: 40px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .question-block {{
            margin-bottom: 30px;
            padding: 0;
            background: transparent;
            border: none;
        }}

        .question-header {{
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
        }}

        .question-number {{
            flex-shrink: 0;
            margin-right: 10px;
            color: #333;
            font-size: 1em;
        }}

        .question-text {{
            font-size: 1em;
            color: #333;
            font-weight: normal;
            line-height: 1.6;
        }}

        .answers-area {{
            margin-left: 30px;
        }}

        .reference-with-blank {{
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .reference-text {{
            color: #333;
            font-size: 0.95em;
            min-width: 100px;
            flex-shrink: 0;
        }}

        .answer-input {{
            flex: 1;
            border: none;
            border-bottom: 1px solid #333;
            padding: 5px 0;
            font-size: 1em;
            font-family: inherit;
            background: transparent;
            outline: none;
        }}

        .answer-input.full-width {{
            width: 100%;
        }}

        .answer-input:focus {{
            border-bottom: 2px solid #667eea;
        }}

        .application-section {{
            margin-top: 40px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 5px;
        }}

        .application-section h3 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 1.1em;
            font-weight: 600;
        }}

        .application-prompt {{
            color: #666;
            margin-bottom: 15px;
            line-height: 1.6;
            font-size: 0.95em;
        }}

        .application-input {{
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
            font-family: inherit;
            resize: vertical;
            min-height: 120px;
        }}

        .application-input:focus {{
            outline: none;
            border-color: #667eea;
        }}

        .action-bar {{
            background: white;
            padding: 25px 40px;
            border-radius: 0 0 15px 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }}

        .score-display {{
            font-size: 1.2em;
            color: #333;
            font-weight: bold;
        }}

        .score-number {{
            color: #667eea;
            font-size: 1.5em;
        }}

        .btn {{
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
            font-weight: 500;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}

        .btn-secondary {{
            background: #f5f5f5;
            color: #333;
        }}

        .btn-secondary:hover {{
            background: #e0e0e0;
        }}

        .navigation {{
            background: white;
            padding: 20px 40px;
            margin-top: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            gap: 15px;
        }}

        .nav-btn {{
            padding: 12px 25px;
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.3s;
            font-weight: 500;
        }}

        .prev-btn, .next-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        .prev-btn:hover, .next-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}

        .home-btn {{
            background: #f5f5f5;
            color: #333;
        }}

        .home-btn:hover {{
            background: #e0e0e0;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}

            header, .content, .action-bar {{
                padding: 20px;
            }}

            h1 {{
                font-size: 1.5em;
            }}

            h2 {{
                font-size: 1.2em;
            }}

            .navigation {{
                flex-direction: column;
                padding: 15px;
            }}

            .nav-btn {{
                width: 100%;
                text-align: center;
            }}

            .action-bar {{
                flex-direction: column;
                text-align: center;
            }}
        }}

        .toast {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 15px 25px;
            border-radius: 8px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            display: none;
            z-index: 1000;
        }}

        .toast.show {{
            display: block;
            animation: slideIn 0.3s ease;
        }}

        @keyframes slideIn {{
            from {{
                transform: translateX(400px);
            }}
            to {{
                transform: translateX(0);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="breadcrumb">
                <a href="foundation_course.html">建立根基</a> / 
                第{lesson_id}课: {lesson_title}
            </div>
            <h1>{lesson_title}</h1>
            <div class="section-title-box">
                <span class="section-label">第{section_num}节</span>
                <span class="section-name">{section_title}</span>
            </div>
        </header>

        <div class="content">
            {questions_html}
            {application_html}
        </div>

        <div class="action-bar">
            <div class="score-display">
                完成度: <span class="score-number" id="scoreDisplay">0%</span>
            </div>
            <div>
                <button class="btn btn-secondary" onclick="saveProgress()">💾 保存进度</button>
                <button class="btn btn-primary" onclick="submitAnswers()">✓ 提交答案</button>
            </div>
        </div>

        <div class="navigation">
            {nav_buttons}
        </div>
    </div>

    <div class="toast" id="toast"></div>

    <script>
        // 加载保存的进度
        window.addEventListener('load', () => {{
            loadProgress();
            updateScore();
        }});

        // 自动保存
        document.querySelectorAll('.answer-input, .application-input').forEach(input => {{
            input.addEventListener('change', () => {{
                updateScore();
            }});
        }});

        function loadProgress() {{
            const key = 'foundation_L{lesson_id}_S{section_num}';
            const saved = localStorage.getItem(key);
            if (saved) {{
                try {{
                    const data = JSON.parse(saved);
                    // 恢复答案
                    document.querySelectorAll('.answer-input').forEach(input => {{
                        const q = input.dataset.question;
                        const ref = input.dataset.reference || 'main';
                        const savedAnswer = data.answers?.[`q${{q}}_${{ref}}`];
                        if (savedAnswer) {{
                            input.value = savedAnswer;
                        }}
                    }});
                    // 恢复个人应用
                    const appInput = document.querySelector('.application-input');
                    if (appInput && data.application) {{
                        appInput.value = data.application;
                    }}
                }} catch (e) {{
                    console.error('加载进度失败:', e);
                }}
            }}
        }}

        function saveProgress() {{
            const key = 'foundation_L{lesson_id}_S{section_num}';
            const data = {{
                answers: {{}},
                application: '',
                timestamp: new Date().toISOString()
            }};
            
            // 保存所有答案
            document.querySelectorAll('.answer-input').forEach(input => {{
                const q = input.dataset.question;
                const ref = input.dataset.reference || 'main';
                data.answers[`q${{q}}_${{ref}}`] = input.value;
            }});
            
            // 保存个人应用
            const appInput = document.querySelector('.application-input');
            if (appInput) {{
                data.application = appInput.value;
            }}
            
            localStorage.setItem(key, JSON.stringify(data));
            showToast('✓ 进度已保存');
        }}

        function submitAnswers() {{
            saveProgress();
            updateScore();
            showToast('✓ 答案已提交！继续下一节吧');
        }}

        function updateScore() {{
            let totalFields = 0;
            let filledFields = 0;
            
            // 统计答案输入框
            document.querySelectorAll('.answer-input').forEach(input => {{
                totalFields++;
                if (input.value.trim()) {{
                    filledFields++;
                }}
            }});
            
            // 统计个人应用
            const appInput = document.querySelector('.application-input');
            if (appInput) {{
                totalFields++;
                if (appInput.value.trim()) {{
                    filledFields++;
                }}
            }}
            
            const percentage = totalFields > 0 ? Math.round((filledFields / totalFields) * 100) : 0;
            document.getElementById('scoreDisplay').textContent = percentage + '%';
        }}

        function showToast(message) {{
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => {{
                toast.classList.remove('show');
            }}, 3000);
        }}
    </script>
</body>
</html>
'''
    
    # 写入文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)


if __name__ == "__main__":
    generate_section_pages()
    print("\n✓ 所有页面生成完成！")
