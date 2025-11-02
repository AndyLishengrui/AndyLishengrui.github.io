#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按照设计文档标准生成第一课的HTML页面
使用textarea、提示按钮、批改功能等完整功能
"""

import json
import os

def generate_section_html(section, course_num, total_sections):
    """生成单个章节的HTML - 完全按照设计文档标准"""
    section_num = section['section_number']
    title = section['title']
    description = section.get('description', '')
    
    # 导航链接
    prev_link = f'one2one_C{course_num}_S{section_num-1}.html' if section_num > 1 else '../index.html'
    next_link = f'one2one_C{course_num}_S{section_num+1}.html' if section_num < total_sections else '../index.html'
    
    # 文件标识符
    file_id = f'C{course_num}_S{section_num}'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 第{section_num}节 | 一对一门徒训练</title>
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
            font-size: 16px;
            line-height: 1.8;
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
            font-size: 0.95em;
            margin-bottom: 12px;
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
            line-height: 1.4;
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
            line-height: 1.4;
        }}

        .section-name {{
            font-size: 1.3em;
            color: #333;
            font-weight: 500;
            line-height: 1.4;
        }}

        .content {{
            background: white;
            padding: 40px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .description-block {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 35px;
            border-left: 4px solid #667eea;
            line-height: 2;
            white-space: pre-wrap;
            color: #333;
            font-size: 1.05em;
        }}

        .question-block {{
            margin-bottom: 35px;
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
            min-width: 30px;
            font-weight: 500;
            color: #667eea;
            font-size: 1.1em;
            line-height: 1.8;
        }}

        .question-text {{
            flex: 1;
            color: #333;
            font-size: 1.1em;
            line-height: 1.8;
        }}

        .answers-area {{
            margin-left: 30px;
        }}

        .reference-with-blank {{
            margin-bottom: 25px;
        }}

        .reference-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .reference-text {{
            font-weight: 500;
            color: #667eea;
            font-size: 1.05em;
        }}

        .hint-buttons {{
            display: flex;
            gap: 8px;
        }}

        .btn-hint-partial, .btn-hint-full {{
            padding: 6px 12px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 5px;
            font-size: 0.9em;
            cursor: pointer;
            transition: all 0.3s;
        }}

        .btn-hint-partial:hover {{
            background: #fff3cd;
            border-color: #f39c12;
        }}

        .btn-hint-full:hover {{
            background: #d4edda;
            border-color: #27ae60;
        }}

        .answer-input {{
            width: 100%;
            min-height: 120px;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1.05em;
            line-height: 1.8;
            font-family: inherit;
            resize: vertical;
            transition: all 0.3s;
        }}

        .answer-input:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}

        .answer-input.correct {{
            border-color: #27ae60;
            background: rgba(39, 174, 96, 0.05);
        }}

        .answer-input.incorrect {{
            border-color: #e74c3c;
            background: rgba(231, 76, 60, 0.05);
        }}

        .answer-input.partial {{
            border-color: #f39c12;
            background: rgba(243, 156, 18, 0.05);
        }}

        .answer-feedback {{
            margin-top: 8px;
            padding: 8px 12px;
            border-radius: 5px;
            font-size: 0.95em;
            display: none;
        }}

        .answer-feedback.show {{
            display: block;
        }}

        .answer-feedback.correct {{
            background: #d4edda;
            color: #155724;
            border-left: 4px solid #27ae60;
        }}

        .answer-feedback.incorrect {{
            background: #f8d7da;
            color: #721c24;
            border-left: 4px solid #e74c3c;
        }}

        .answer-feedback.partial {{
            background: #fff3cd;
            color: #856404;
            border-left: 4px solid #f39c12;
        }}

        .standard-answer {{
            display: none;
            margin-top: 12px;
            padding: 15px;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 0 5px 5px 0;
            font-size: 1em;
            color: #555;
            line-height: 1.8;
        }}

        .standard-answer.show {{
            display: block;
        }}

        .standard-answer .version-section {{
            margin-bottom: 15px;
        }}

        .standard-answer .version-section:last-child {{
            margin-bottom: 0;
        }}

        .standard-answer .version-label {{
            color: #667eea;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .standard-answer .verse-text {{
            color: #333;
            line-height: 1.8;
        }}

        .application-section {{
            background: #fff3cd;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 4px solid #f39c12;
        }}

        .application-section h3 {{
            color: #856404;
            margin-bottom: 15px;
            font-size: 1.2em;
        }}

        .application-section ul {{
            list-style: none;
            padding-left: 0;
        }}

        .application-section li {{
            padding: 10px 0;
            padding-left: 25px;
            position: relative;
            color: #333;
        }}

        .application-section li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: #f39c12;
            font-weight: bold;
        }}

        .prayer-section {{
            background: #d4edda;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 4px solid #27ae60;
        }}

        .prayer-section h3 {{
            color: #155724;
            margin-bottom: 15px;
            font-size: 1.2em;
        }}

        .prayer-text {{
            color: #333;
            line-height: 2;
            white-space: pre-wrap;
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
            font-size: 1.15em;
            color: #333;
            font-weight: 500;
        }}

        .score-number {{
            color: #667eea;
            font-size: 1.4em;
            font-weight: bold;
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

        .btn-check {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        .btn-check:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}

        .btn-submit {{
            background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
            color: white;
        }}

        .btn-submit:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(39, 174, 96, 0.4);
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
                transform: translateX(100%);
                opacity: 0;
            }}
            to {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}

        .score-modal {{
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

        .score-modal.show {{
            display: flex;
        }}

        .score-modal-content {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            max-width: 500px;
            width: 90%;
            text-align: center;
        }}

        .score-title {{
            font-size: 2em;
            color: #667eea;
            font-weight: bold;
            margin: 20px 0;
        }}

        .score-message {{
            font-size: 1.2em;
            color: #666;
            margin-bottom: 30px;
        }}

        .score-details {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: left;
        }}

        .score-details p {{
            margin: 8px 0;
            color: #555;
        }}

        .btn-close-modal {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            font-weight: 500;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 10px;
                font-size: 15px;
            }}

            .content {{
                padding: 20px;
            }}

            .answers-area {{
                margin-left: 10px;
            }}

            .action-bar {{
                flex-direction: column;
                width: 100%;
            }}

            .btn-hint-partial, .btn-hint-full {{
                width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="breadcrumb">
                <a href="../index.html">一对一首页</a> &gt; <a href="../index.html">第1课：新起点 得救</a> &gt; 第{section_num}节
            </div>
            <h1>第1课：新起点 得救</h1>
            <div class="section-title-box">
                <span class="section-label">第{section_num}节</span>
                <span class="section-name">{title}</span>
            </div>
        </header>

        <div class="content">
'''
    
    # 添加说明文字
    if description:
        html += f'''            <div class="description-block">{description}</div>
'''
    
    # 添加经文填空部分
    if 'verses' in section and section['verses']:
        html += '''            <div class="question-block" data-question-id="1">
                <div class="question-header">
                    <span class="question-number">1.</span>
                    <span class="question-text">请阅读以下经文并填写：</span>
                </div>
                <div class="answers-area">
'''
        for idx, verse in enumerate(section['verses'], 1):
            verse_key = f"q1_{verse['reference']}"
            html += f'''                    <div class="reference-with-blank">
                        <div class="reference-header">
                            <span class="reference-text">{verse['reference']}</span>
                            <div class="hint-buttons">
                                <button class="btn-hint-partial" onclick="showPartialHint('1', '{verse['reference']}')" title="渐进提示">💡 提示</button>
                                <button class="btn-hint-full" onclick="showFullHint('1', '{verse['reference']}')" title="显示完整答案">👁️ 答案</button>
                            </div>
                        </div>
                        <textarea class="answer-input" data-question="1" data-reference="{verse['reference']}" data-has-answer="true"
                               data-hint-progress="0"
                               placeholder="请填写经文内容（和合本）..."></textarea>
                        <div class="answer-feedback" data-ref="{verse['reference']}"></div>
                        <div class="standard-answer" data-ref="{verse['reference']}"></div>
                    </div>
'''
        html += '''                </div>
            </div>
'''
    elif 'content' in section:
        # 单个经文
        verse_key = f"q1_{section['verse_reference']}"
        html += f'''            <div class="question-block" data-question-id="1">
                <div class="question-header">
                    <span class="question-number">1.</span>
                    <span class="question-text">请阅读以下经文并填写：</span>
                </div>
                <div class="answers-area">
                    <div class="reference-with-blank">
                        <div class="reference-header">
                            <span class="reference-text">{section['verse_reference']}</span>
                            <div class="hint-buttons">
                                <button class="btn-hint-partial" onclick="showPartialHint('1', '{section['verse_reference']}')" title="渐进提示">💡 提示</button>
                                <button class="btn-hint-full" onclick="showFullHint('1', '{section['verse_reference']}')" title="显示完整答案">👁️ 答案</button>
                            </div>
                        </div>
                        <textarea class="answer-input" data-question="1" data-reference="{section['verse_reference']}" data-has-answer="true"
                               data-hint-progress="0"
                               placeholder="请填写经文内容（和合本）..."></textarea>
                        <div class="answer-feedback" data-ref="{section['verse_reference']}"></div>
                        <div class="standard-answer" data-ref="{section['verse_reference']}"></div>
                    </div>
                </div>
            </div>
'''
    
    # 添加个人应用
    if 'application_questions' in section:
        html += '''            <div class="application-section">
                <h3>💭 个人应用</h3>
                <ul>
'''
        for question in section['application_questions']:
            html += f'                    <li>{question}</li>\n'
        html += '''                </ul>
            </div>
'''
    
    # 添加祷告
    if 'prayer' in section:
        html += f'''            <div class="prayer-section">
                <h3>🙏 得救的祷告</h3>
                <div class="prayer-text">{section['prayer']}</div>
            </div>
'''
    
    # 添加最后的经文（如果有）
    if 'verse' in section:
        verse = section['verse']
        html += f'''            <div class="reference-with-blank">
                <div class="reference-header">
                    <span class="reference-text">{verse['reference']}</span>
                </div>
                <textarea class="answer-input" data-question="2" data-reference="{verse['reference']}" data-has-answer="true"
                       data-hint-progress="0"
                       placeholder="请填写经文内容（{verse['version']}）..."></textarea>
                <div class="answer-feedback" data-ref="{verse['reference']}"></div>
                <div class="standard-answer" data-ref="{verse['reference']}"></div>
            </div>
'''
    
    html += '''        </div>

        <div class="action-bar">
            <div class="score-display">
                已完成: <span class="score-number" id="scoreDisplay">0/0</span>
            </div>
            <div>
                <button class="btn btn-check" onclick="checkAnswers()">✓ 批改</button>
                <button class="btn btn-submit" onclick="submitAnswers()">📝 提交</button>
                <button class="btn btn-secondary" onclick="clearAnswers()">🔄 清空</button>
            </div>
        </div>

        <div class="navigation">
'''
    html += f'            <a href="{prev_link}" class="btn btn-secondary">← 上一节</a>\n'
    html += f'            <a href="{next_link}" class="btn btn-check">下一节 →</a>\n'
    html += f'''        </div>
    </div>

    <div class="toast" id="toast"></div>

    <div class="score-modal" id="scoreModal">
        <div class="score-modal-content">
            <h2>📊 学习成绩</h2>
            <div class="score-title" id="scoreTitle">0分</div>
            <div class="score-message" id="scoreMessage">继续努力！</div>
            <div class="score-details" id="scoreDetails"></div>
            <button class="btn-close-modal" onclick="closeScoreModal()">关闭</button>
        </div>
    </div>

    <script>
        let standardAnswers = {{}};

        // 页面加载时初始化
        window.addEventListener('load', () => {{
            loadStandardAnswers();
            loadProgress();
            updateProgress();
        }});

        // 加载标准答案
        async function loadStandardAnswers() {{
            try {{
                // 加载课程级别的JSON文件（一课一个文件，包含所有节）
                const response = await fetch('../data/answers/one2one_C{course_num}.json');
                const data = await response.json();
                // 从课程数据中获取当前节的答案
                const sectionData = data.sections['{section_num}'];
                standardAnswers = sectionData ? sectionData.answers : {{}};
                console.log('答案数据加载成功:', Object.keys(standardAnswers).length, '个答案');
            }} catch (error) {{
                console.error('加载答案数据失败:', error);
                showToast('答案数据加载失败，部分功能可能无法使用');
            }}
        }}

        // 自动保存
        document.querySelectorAll('.answer-input').forEach(input => {{
            input.addEventListener('input', () => {{
                saveProgress();
                updateProgress();
            }});
        }});

        // 保存进度
        function saveProgress() {{
            const progress = {{}};
            document.querySelectorAll('.answer-input').forEach(input => {{
                const question = input.dataset.question;
                const ref = input.dataset.reference;
                const key = `${{question}}_${{ref}}`;
                progress[key] = input.value;
            }});
            localStorage.setItem('one2one_{file_id}_progress', JSON.stringify(progress));
        }}

        // 加载进度
        function loadProgress() {{
            const saved = localStorage.getItem('one2one_{file_id}_progress');
            if (saved) {{
                const data = JSON.parse(saved);
                Object.keys(data).forEach(key => {{
                    const [question, ...refParts] = key.split('_');
                    const ref = refParts.join('_');
                    const input = document.querySelector(
                        `.answer-input[data-question="${{question}}"][data-reference="${{ref}}"]`
                    );
                    if (input && data[key]) {{
                        input.value = data[key];
                    }}
                }});
            }}
        }}

        // 更新进度显示
        function updateProgress() {{
            const inputs = document.querySelectorAll('.answer-input');
            const filled = Array.from(inputs).filter(input => input.value.trim()).length;
            document.getElementById('scoreDisplay').textContent = `${{filled}}/${{inputs.length}}`;
        }}

        // 渐进提示
        function showPartialHint(questionId, ref) {{
            const input = document.querySelector(`.answer-input[data-question="${{questionId}}"][data-reference="${{ref}}"]`);
            const answerKey = `q${{questionId}}_${{ref}}`;
            const answerInfo = standardAnswers[answerKey];
            
            if (!answerInfo || !answerInfo.has_data) {{
                showToast('暂无答案数据');
                return;
            }}
            
            const standardAnswer = answerInfo.text;
            let currentProgress = parseInt(input.dataset.hintProgress) || 0;
            currentProgress += 10;
            
            if (currentProgress >= standardAnswer.length) {{
                input.value = standardAnswer;
                input.dataset.hintProgress = standardAnswer.length;
                showToast('已显示完整答案');
            }} else {{
                input.value = standardAnswer.substring(0, currentProgress);
                input.dataset.hintProgress = currentProgress;
                showToast(`显示了前 ${{currentProgress}} 个字`);
            }}
            
            saveProgress();
            updateProgress();
        }}

        // 显示完整答案
        function showFullHint(questionId, ref) {{
            const answerKey = `q${{questionId}}_${{ref}}`;
            const answerInfo = standardAnswers[answerKey];
            const answerDiv = document.querySelector(`.standard-answer[data-ref="${{ref}}"]`);
            
            if (!answerInfo || !answerInfo.has_data) {{
                showToast('暂无答案数据');
                return;
            }}
            
            // 始终显示和合本作为标准答案
            let html = `<div class="version-section">
                <div class="version-label">📖 标准答案（和合本）：</div>
                <div class="verse-text">${{answerInfo.text}}</div>
            </div>`;
            
            // 如果有其他版本，显示为参考答案
            if (answerInfo.version_alt && answerInfo.text_alt) {{
                html += `<div class="version-section">
                    <div class="version-label">📖 其他经文（${{answerInfo.version_alt}}）：</div>
                    <div class="verse-text">${{answerInfo.text_alt}}</div>
                </div>`;
            }}
            
            answerDiv.innerHTML = html;
            answerDiv.classList.toggle('show');
        }}

        // LCS相似度算法
        function calculateSimilarity(text1, text2) {{
            text1 = text1.replace(/\\s+/g, '');
            text2 = text2.replace(/\\s+/g, '');
            
            const len1 = text1.length;
            const len2 = text2.length;
            const dp = Array(len1 + 1).fill(0).map(() => Array(len2 + 1).fill(0));
            
            for (let i = 1; i <= len1; i++) {{
                for (let j = 1; j <= len2; j++) {{
                    if (text1[i - 1] === text2[j - 1]) {{
                        dp[i][j] = dp[i - 1][j - 1] + 1;
                    }} else {{
                        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                    }}
                }}
            }}
            
            const lcs = dp[len1][len2];
            return lcs / Math.max(len1, len2);
        }}

        // 批改答案
        function checkAnswers() {{
            const inputs = document.querySelectorAll('.answer-input');
            let hasError = false;
            let firstError = null;
            let correctInputs = 0;
            let partialInputs = 0;
            let totalInputs = 0;
            
            inputs.forEach(input => {{
                const question = input.dataset.question;
                const ref = input.dataset.reference;
                const answerKey = `q${{question}}_${{ref}}`;
                const answerInfo = standardAnswers[answerKey];
                const feedbackDiv = input.nextElementSibling;
                
                if (!answerInfo || !answerInfo.has_data) {{
                    return;
                }}
                
                totalInputs++;
                const userAnswer = input.value.trim();
                const standardAnswer = answerInfo.text;
                
                if (!userAnswer) {{
                    input.className = 'answer-input';
                    feedbackDiv.className = 'answer-feedback';
                    return;
                }}
                
                const similarity = calculateSimilarity(userAnswer, standardAnswer);
                
                if (similarity >= 0.85) {{
                    input.className = 'answer-input correct';
                    feedbackDiv.className = 'answer-feedback correct show';
                    feedbackDiv.textContent = '✅ 正确！';
                    correctInputs++;
                }} else if (similarity >= 0.60) {{
                    input.className = 'answer-input partial';
                    feedbackDiv.className = 'answer-feedback partial show';
                    feedbackDiv.textContent = `⚠️ 部分正确（相似度：${{Math.round(similarity * 100)}}%）`;
                    partialInputs++;
                    if (!firstError) firstError = input;
                    hasError = true;
                }} else {{
                    input.className = 'answer-input incorrect';
                    feedbackDiv.className = 'answer-feedback incorrect show';
                    feedbackDiv.textContent = `❌ 需要修改（相似度：${{Math.round(similarity * 100)}}%）`;
                    if (!firstError) firstError = input;
                    hasError = true;
                }}
            }});
            
            if (firstError) {{
                firstError.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                firstError.focus();
            }}
            
            if (!hasError && totalInputs > 0) {{
                showToast('🎉 全部正确！');
            }} else {{
                showToast(`批改完成：${{correctInputs}}/${{totalInputs}} 完全正确`);
            }}
        }}

        // 提交成绩
        function submitAnswers() {{
            const inputs = document.querySelectorAll('.answer-input');
            let correctInputs = 0;
            let partialInputs = 0;
            let totalInputs = 0;
            
            inputs.forEach(input => {{
                const question = input.dataset.question;
                const ref = input.dataset.reference;
                const answerKey = `q${{question}}_${{ref}}`;
                const answerInfo = standardAnswers[answerKey];
                
                if (!answerInfo || !answerInfo.has_data) return;
                
                totalInputs++;
                const userAnswer = input.value.trim();
                if (!userAnswer) return;
                
                const similarity = calculateSimilarity(userAnswer, answerInfo.text);
                
                if (similarity >= 0.85) {{
                    correctInputs++;
                }} else if (similarity >= 0.60) {{
                    partialInputs++;
                }}
            }});
            
            const score = totalInputs > 0 
                ? Math.round(((correctInputs + partialInputs * 0.6) / totalInputs) * 100) 
                : 0;
            
            let message = '';
            if (score >= 90) {{
                message = '优秀！你掌握得非常好！';
            }} else if (score >= 75) {{
                message = '良好！继续加油！';
            }} else if (score >= 60) {{
                message = '及格！建议再复习一下';
            }} else {{
                message = '继续努力！多读几遍经文吧';
            }}
            
            document.getElementById('scoreTitle').textContent = `${{score}}分`;
            document.getElementById('scoreMessage').textContent = message;
            document.getElementById('scoreDetails').innerHTML = `
                <p>📊 总答案框：${{totalInputs}}</p>
                <p>✅ 完全正确：${{correctInputs}}</p>
                <p>⚠️ 部分正确：${{partialInputs}}</p>
                <p>❌ 需要修改：${{totalInputs - correctInputs - partialInputs}}</p>
            `;
            
            document.getElementById('scoreModal').classList.add('show');
        }}

        // 关闭评分模态框
        function closeScoreModal() {{
            document.getElementById('scoreModal').classList.remove('show');
        }}

        // 清空答案
        function clearAnswers() {{
            if (!confirm('确定要清空所有答案吗？')) return;
            
            document.querySelectorAll('.answer-input').forEach(input => {{
                input.value = '';
                input.className = 'answer-input';
                input.dataset.hintProgress = '0';
            }});
            
            document.querySelectorAll('.answer-feedback').forEach(div => {{
                div.className = 'answer-feedback';
                div.textContent = '';
            }});
            
            document.querySelectorAll('.standard-answer').forEach(div => {{
                div.classList.remove('show');
            }});
            
            localStorage.removeItem('one2one_{file_id}_progress');
            updateProgress();
            showToast('已清空所有答案');
        }}

        // 显示Toast消息
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
    
    print(f'\n🎉 完成！共生成 {total_sections} 个HTML文件（按设计文档标准）')

if __name__ == '__main__':
    main()
