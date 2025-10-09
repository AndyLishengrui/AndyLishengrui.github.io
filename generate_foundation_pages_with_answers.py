#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成建立根基课程的学习页面（带预填标准答案）
为每一节生成一个独立的HTML页面，并预填标准答案
"""

import json
import os

def count_lines_needed(text):
    """计算需要的行数"""
    if not text:
        return 1
    # 每50个字符需要一行，最少2行，最多10行
    lines = max(2, min(10, len(text) // 50 + 1))
    return lines

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
            unique_lessons[lesson_id]['sections'].extend(lesson['sections'])
    
    lessons = sorted(unique_lessons.values(), key=lambda x: x['id'])
    
    print(f"开始生成课程页面（预填答案版本）...")
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
            
            # 清理节标题
            if '_' in section_title and len(section_title) > 20:
                section_title = f"第{section_id}节"
            
            # 加载答案数据
            answer_file = f"data/answers/foundation_L{lesson_id}_S{section_idx + 1}.json"
            answer_data = {}
            if os.path.exists(answer_file):
                with open(answer_file, 'r', encoding='utf-8') as f:
                    answers_json = json.load(f)
                    answer_data = answers_json.get('answers', {})
            
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
                next_section,
                answer_data
            )
            
            total_pages += 1
            answers_count = sum(1 for a in answer_data.values() if a.get('has_data'))
            print(f"    ✓ 第{section_idx + 1}节: {section_title[:30]} ({answers_count}个答案已预填)")
    
    print(f"\n✓ 共生成 {total_pages} 个页面")


def generate_section_html(filename, lesson_id, lesson_title, section_num, section, prev_section, next_section, answer_data):
    """生成单个节的HTML页面（带预填答案）"""
    
    section_title = section['title']
    if '_' in section_title and len(section_title) > 20:
        section_title = f"第{section_num}节"
    
    questions_html = ""
    for q in section['questions']:
        question_id = q['id']
        question_text = q['question']
        references = q.get('references', [])
        
        # 生成经文引用和填空区域
        refs_and_blanks_html = ""
        if references:
            for ref in references:
                # 获取标准答案
                answer_key = f"q{question_id}_{ref}"
                answer_info = answer_data.get(answer_key, {})
                standard_text = answer_info.get('text', '')
                has_data = answer_info.get('has_data', False)
                
                # 计算需要的行数
                rows = count_lines_needed(standard_text) if standard_text else 3
                
                # 预填答案
                prefilled_value = standard_text if has_data else ''
                
                refs_and_blanks_html += f'''
                <div class="reference-with-blank">
                    <span class="reference-text">{ref}</span>
                    <textarea class="answer-input" 
                           rows="{rows}"
                           data-question="{question_id}" 
                           data-reference="{ref}"
                           data-has-answer="{str(has_data).lower()}"
                           placeholder="{'请填写经文内容...' if has_data else '暂无标准答案（仅支持新约）'}">{prefilled_value}</textarea>
                    <span class="answer-feedback" data-ref="{ref}"></span>
                </div>
                '''
        else:
            # 没有经文引用时，显示一个填空行
            refs_and_blanks_html = f'''
                <div class="reference-with-blank">
                    <textarea class="answer-input full-width" 
                           rows="3"
                           data-question="{question_id}" 
                           placeholder="请写下你的答案..."></textarea>
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
            margin-bottom: 20px;
            position: relative;
        }}

        .reference-text {{
            display: block;
            color: #667eea;
            font-size: 0.95em;
            font-weight: 500;
            margin-bottom: 8px;
        }}

        .answer-input {{
            width: 100%;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            font-size: 1em;
            font-family: inherit;
            resize: vertical;
            outline: none;
            transition: all 0.3s;
            line-height: 1.6;
        }}

        .answer-input:focus {{
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}

        .answer-input.correct {{
            border-color: #27ae60;
            background: linear-gradient(to right, rgba(39, 174, 96, 0.05) 0%, transparent 100%);
        }}

        .answer-input.incorrect {{
            border-color: #e74c3c;
            background: linear-gradient(to right, rgba(231, 76, 60, 0.05) 0%, transparent 100%);
        }}

        .answer-input.partial {{
            border-color: #f39c12;
            background: linear-gradient(to right, rgba(243, 156, 18, 0.05) 0%, transparent 100%);
        }}

        .answer-feedback {{
            position: absolute;
            top: 0;
            right: 0;
            font-size: 1.2em;
            font-weight: bold;
        }}

        .answer-feedback.correct {{
            color: #27ae60;
        }}

        .answer-feedback.incorrect {{
            color: #e74c3c;
        }}

        .answer-feedback.partial {{
            color: #f39c12;
        }}

        .standard-answer {{
            display: none;
            margin-top: 10px;
            padding: 12px;
            background: #f8f9fa;
            border-left: 3px solid #667eea;
            font-size: 0.95em;
            color: #555;
            line-height: 1.6;
            border-radius: 0 5px 5px 0;
        }}

        .standard-answer.show {{
            display: block;
        }}

        .standard-answer strong {{
            color: #667eea;
            display: block;
            margin-bottom: 5px;
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

        .btn-success {{
            background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
            color: white;
        }}

        .btn-success:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(39, 174, 96, 0.4);
        }}

        .btn-warning {{
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            color: white;
        }}

        .btn-warning:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(243, 156, 18, 0.4);
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
            max-width: 300px;
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

        .loading-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.7);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 2000;
        }}

        .loading-overlay.show {{
            display: flex;
        }}

        .loading-spinner {{
            background: white;
            padding: 30px 40px;
            border-radius: 10px;
            text-align: center;
        }}

        .spinner {{
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }}

        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
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
                得分: <span class="score-number" id="scoreDisplay">-</span> | 
                完成度: <span class="score-number" id="progressDisplay">100%</span>
            </div>
            <div>
                <button class="btn btn-warning" onclick="clearAnswers()">🗑️ 清空答案</button>
                <button class="btn btn-secondary" onclick="saveProgress()">💾 保存进度</button>
                <button class="btn btn-success" onclick="checkAnswers()" id="checkBtn">✓ 检查答案</button>
                <button class="btn btn-primary" onclick="submitAnswers()">📝 提交</button>
            </div>
        </div>

        <div class="navigation">
            {nav_buttons}
        </div>
    </div>

    <div class="toast" id="toast"></div>
    
    <div class="loading-overlay" id="loadingOverlay">
        <div class="loading-spinner">
            <div class="spinner"></div>
            <div>正在检查答案...</div>
        </div>
    </div>

    <script>
        // 存储标准答案
        let standardAnswers = {{}};
        
        // 加载保存的进度
        window.addEventListener('load', () => {{
            // 不自动加载进度，因为答案已预填
            updateProgress();
            loadStandardAnswers();
        }});

        // 自动保存
        document.querySelectorAll('.answer-input, .application-input').forEach(input => {{
            input.addEventListener('change', () => {{
                updateProgress();
            }});
        }});

        // 加载标准答案
        async function loadStandardAnswers() {{
            try {{
                const response = await fetch('data/answers/foundation_L{lesson_id}_S{section_num}.json');
                if (!response.ok) {{
                    console.warn('未找到答案数据文件');
                    return;
                }}
                
                const answerData = await response.json();
                standardAnswers = answerData.answers || {{}};
                console.log('标准答案已加载:', Object.keys(standardAnswers).length, '个');
            }} catch (e) {{
                console.error('加载标准答案失败:', e);
            }}
        }}

        // 清空所有答案
        function clearAnswers() {{
            if (!confirm('确定要清空所有答案吗？此操作不可恢复。')) {{
                return;
            }}
            
            document.querySelectorAll('.answer-input').forEach(input => {{
                input.value = '';
                input.classList.remove('correct', 'incorrect', 'partial');
            }});
            
            document.querySelector('.application-input').value = '';
            
            document.querySelectorAll('.answer-feedback').forEach(feedback => {{
                feedback.textContent = '';
                feedback.className = 'answer-feedback';
            }});
            
            document.querySelectorAll('.standard-answer').forEach(div => {{
                div.classList.remove('show');
            }});
            
            document.getElementById('scoreDisplay').textContent = '-';
            updateProgress();
            showToast('✓ 答案已清空');
        }}

        // 检查答案
        async function checkAnswers() {{
            const loadingOverlay = document.getElementById('loadingOverlay');
            loadingOverlay.classList.add('show');
            
            // 确保标准答案已加载
            await loadStandardAnswers();
            
            setTimeout(() => {{
                let totalQuestions = 0;
                let correctCount = 0;
                
                document.querySelectorAll('.answer-input').forEach(input => {{
                    const ref = input.dataset.reference;
                    const hasAnswer = input.dataset.hasAnswer === 'true';
                    
                    if (!ref || !hasAnswer) {{
                        // 没有标准答案的题目不计分
                        return;
                    }}
                    
                    const questionId = input.dataset.question;
                    const answerKey = `q${{questionId}}_${{ref}}`;
                    const answerInfo = standardAnswers[answerKey];
                    
                    if (!answerInfo || !answerInfo.has_data) {{
                        return;
                    }}
                    
                    totalQuestions++;
                    
                    const userAnswer = input.value.trim();
                    const standardAnswer = answerInfo.text || '';
                    
                    // 清除之前的标记
                    input.classList.remove('correct', 'incorrect', 'partial');
                    
                    const feedbackSpan = input.parentElement.querySelector('.answer-feedback');
                    let standardAnswerDiv = input.parentElement.querySelector('.standard-answer');
                    
                    // 如果标准答案div不存在，创建它
                    if (!standardAnswerDiv) {{
                        standardAnswerDiv = document.createElement('div');
                        standardAnswerDiv.className = 'standard-answer';
                        input.parentElement.appendChild(standardAnswerDiv);
                    }}
                    
                    // 相似度检查
                    const similarity = calculateSimilarity(userAnswer, standardAnswer);
                    
                    if (similarity >= 0.85) {{
                        // 85%以上相似度认为正确
                        input.classList.add('correct');
                        feedbackSpan.textContent = '✓';
                        feedbackSpan.className = 'answer-feedback correct';
                        correctCount++;
                        standardAnswerDiv.classList.remove('show');
                    }} else if (similarity >= 0.6) {{
                        // 60-85%相似度认为部分正确
                        input.classList.add('partial');
                        feedbackSpan.textContent = '△';
                        feedbackSpan.className = 'answer-feedback partial';
                        correctCount += 0.6;
                        standardAnswerDiv.innerHTML = `<strong>标准答案:</strong> ${{standardAnswer}}`;
                        standardAnswerDiv.classList.add('show');
                    }} else {{
                        // 低于60%认为错误
                        input.classList.add('incorrect');
                        feedbackSpan.textContent = '✗';
                        feedbackSpan.className = 'answer-feedback incorrect';
                        standardAnswerDiv.innerHTML = `<strong>标准答案:</strong> ${{standardAnswer}}`;
                        standardAnswerDiv.classList.add('show');
                    }}
                }});
                
                // 计算得分
                const score = totalQuestions > 0 ? Math.round((correctCount / totalQuestions) * 100) : 0;
                document.getElementById('scoreDisplay').textContent = score + '分';
                
                // 显示反馈
                let message = '';
                if (totalQuestions === 0) {{
                    message = 'ℹ️ 本节暂无可检查的题目（仅支持新约经文）';
                }} else if (score >= 90) {{
                    message = '🎉 优秀！你掌握得非常好！';
                }} else if (score >= 75) {{
                    message = '👍 良好！继续加油！';
                }} else if (score >= 60) {{
                    message = '📚 及格！建议再复习一下';
                }} else {{
                    message = '💪 继续努力！多读几遍经文吧';
                }}
                
                showToast(message);
                loadingOverlay.classList.remove('show');
            }}, 300);
        }}

        // 计算文本相似度
        function calculateSimilarity(text1, text2) {{
            // 移除标点符号和空格
            const clean1 = text1.replace(/[\\s\\.,;:!?，。；：！？、""''（）【】《》]/g, '');
            const clean2 = text2.replace(/[\\s\\.,;:!?，。；：！？、""''（）【】《》]/g, '');
            
            if (!clean1 || !clean2) return 0;
            
            // 计算共同字符数
            let matches = 0;
            const shorter = clean1.length < clean2.length ? clean1 : clean2;
            const longer = clean1.length < clean2.length ? clean2 : clean1;
            
            // 使用动态规划计算最长公共子序列
            const dp = Array(shorter.length + 1).fill(null).map(() => 
                Array(longer.length + 1).fill(0)
            );
            
            for (let i = 1; i <= shorter.length; i++) {{
                for (let j = 1; j <= longer.length; j++) {{
                    if (shorter[i-1] === longer[j-1]) {{
                        dp[i][j] = dp[i-1][j-1] + 1;
                    }} else {{
                        dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);
                    }}
                }}
            }}
            
            matches = dp[shorter.length][longer.length];
            
            // 相似度 = 公共字符数 / 较长文本的长度
            return matches / longer.length;
        }}

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
                    // 恢复得分
                    if (data.score !== undefined) {{
                        document.getElementById('scoreDisplay').textContent = data.score + '分';
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
                score: document.getElementById('scoreDisplay').textContent.replace('分', '').replace('-', ''),
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
            updateProgress();
            showToast('✓ 答案已提交！继续下一节吧');
        }}

        function updateProgress() {{
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
            document.getElementById('progressDisplay').textContent = percentage + '%';
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
    print("\n✓ 所有页面生成完成（带预填答案）！")
