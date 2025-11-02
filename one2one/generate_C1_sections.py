#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门为第一课生成2-14节的HTML页面
基于已经正确的C1_S1.html模板
"""

import json
import os
from pathlib import Path

def load_json_data(section_num):
    """加载JSON答案数据"""
    json_file = f"data/answers/one2one_C1_S{section_num}.json"
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"  ✅ 加载JSON: {json_file}")
            return data
    except FileNotFoundError:
        print(f"  ⚠️  JSON文件不存在: {json_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON解析错误 {json_file}: {e}")
        return None

def generate_verse_html(verse_data):
    """生成单个经文填空区的HTML"""
    reference = verse_data.get('reference', '')
    
    # 获取经文文本
    text = verse_data.get('text', '')
    text_alt = verse_data.get('text_alt', '')
    
    html = f'''
                        <div class="reference-with-blank">
                            <div class="reference-header">
                                <span class="reference-text">{reference}</span>
                                <div class="hint-buttons">
                                    <button class="btn-hint-partial" onclick="showPartialHint('1', '{reference}')" title="渐进提示">💡 提示</button>
                                    <button class="btn-hint-full" onclick="showFullHint('1', '{reference}')" title="显示完整答案">👁️ 答案</button>
                                </div>
                            </div>
                            <textarea class="answer-input" 
                                data-question="1" 
                                data-reference="{reference}" 
                                data-has-answer="true"
                                data-hint-progress="0"
                                placeholder="请填写经文内容（和合本）..."></textarea>
                            <div class="answer-feedback" data-ref="{reference}"></div>
                            <div class="standard-answer" data-ref="{reference}"></div>
                        </div>'''
    
    return html

def get_section_title(section_num):
    """获取章节标题"""
    titles = {
        1: "问题：罪使我们与神隔绝",
        2: "神的回应：耶稣基督",
        3: "我们当做的回应：悔改和相信",
        4: "称义——从神而来的礼物",
        5: "得救的确据（一）神的道",
        6: "得救的确据（二）内在的见证",
        7: "得救的确据（三）生命的改变",
        8: "生命的成长",
        9: "圣经",
        10: "祷告",
        11: "与神同行",
        12: "罪",
        13: "弟兄姐妹的关系",
        14: "基督徒的见证"
    }
    return titles.get(section_num, f"第{section_num}节")

def generate_html_for_section(section_num, json_data):
    """为指定章节生成完整的HTML页面"""
    
    # 获取说明文字
    description = json_data.get('description', '请阅读以下经文并填写：')
    
    # 检查数据格式：支持两种格式
    verses = []
    if 'verses' in json_data:
        verses = json_data['verses']
    elif 'answers' in json_data:
        # 转换answers格式为verses格式
        for key, answer in json_data['answers'].items():
            if answer.get('has_data'):
                verses.append(answer)
    
    if not verses:
        print(f"  ❌ 第{section_num}节: JSON数据无效或为空")
        return False
    
    section_title = get_section_title(section_num)
    
    # 生成所有经文填空区
    verses_html = ""
    for verse in verses:
        verses_html += generate_verse_html(verse)
    
    # 确定导航链接
    prev_link = f'one2one_C1_S{section_num-1}.html' if section_num > 1 else 'index.html'
    next_link = f'one2one_C1_S{section_num+1}.html' if section_num < 14 else 'one2one_C2_S1.html'
    
    prev_disabled = '' if section_num > 1 else 'disabled'
    next_text = '下一节 →' if section_num < 14 else '下一课 →'
    
    # 生成完整HTML
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>第1课 第{section_num}节 - {section_title} | 一对一门徒训练</title>
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

        @media (max-width: 768px) {{
            body {{
                padding: 10px;
                font-size: 15px;
            }}
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
            font-size: 2em;
            margin-bottom: 15px;
        }}

        .section-title-box {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 12px 20px;
            border-radius: 8px;
            color: white;
        }}

        .section-label {{
            font-size: 1.1em;
            font-weight: 600;
            border-right: 2px solid rgba(255,255,255,0.3);
            padding-right: 12px;
        }}

        .section-name {{
            font-size: 1em;
        }}

        .content {{
            background: white;
            padding: 35px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .question-block {{
            margin-bottom: 35px;
            padding-bottom: 30px;
            border-bottom: 2px solid #f0f0f0;
        }}

        .question-block:last-child {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}

        .question-header {{
            display: flex;
            align-items: flex-start;
            margin-bottom: 20px;
            gap: 8px;
        }}

        .question-number {{
            color: #667eea;
            font-weight: 600;
            font-size: 1.1em;
            flex-shrink: 0;
        }}

        .question-text {{
            color: #333;
            font-size: 1.05em;
            line-height: 1.6;
        }}

        .reference-with-blank {{
            margin-bottom: 25px;
            background: #f8f9ff;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}

        .reference-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .reference-text {{
            color: #667eea;
            font-weight: 600;
            font-size: 1.05em;
        }}

        .hint-buttons {{
            display: flex;
            gap: 8px;
        }}

        .btn-hint-partial,
        .btn-hint-full {{
            padding: 6px 12px;
            border: none;
            border-radius: 6px;
            font-size: 0.9em;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 500;
        }}

        .btn-hint-partial {{
            background: #ffc107;
            color: #333;
        }}

        .btn-hint-partial:hover {{
            background: #ffb300;
            transform: translateY(-2px);
        }}

        .btn-hint-full {{
            background: #4CAF50;
            color: white;
        }}

        .btn-hint-full:hover {{
            background: #45a049;
            transform: translateY(-2px);
        }}

        .answer-input {{
            width: 100%;
            min-height: 120px;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            font-family: inherit;
            line-height: 1.6;
            resize: vertical;
            transition: all 0.3s;
        }}

        .answer-input:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}

        .answer-input.correct {{
            border-color: #4CAF50;
            background: #f1f8f4;
        }}

        .answer-input.incorrect {{
            border-color: #f44336;
            background: #ffebee;
        }}

        .answer-feedback {{
            margin-top: 12px;
            padding: 12px;
            border-radius: 6px;
            font-size: 0.95em;
            display: none;
        }}

        .answer-feedback.show {{
            display: block;
        }}

        .answer-feedback.correct {{
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }}

        .answer-feedback.incorrect {{
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}

        .standard-answer {{
            margin-top: 12px;
            padding: 15px;
            background: #e3f2fd;
            border-left: 4px solid #2196F3;
            border-radius: 6px;
            display: none;
        }}

        .standard-answer.show {{
            display: block;
        }}

        .standard-answer strong {{
            color: #667eea;
            display: block;
            margin-bottom: 8px;
            font-size: 1em;
        }}

        .standard-answer .version-section {{
            margin-bottom: 15px;
        }}

        .standard-answer .version-section:last-child {{
            margin-bottom: 0;
        }}

        .standard-answer .version-label {{
            font-weight: 600;
            color: #555;
            margin-bottom: 5px;
        }}

        .standard-answer .version-text {{
            color: #333;
            line-height: 1.8;
        }}

        .action-bar {{
            background: white;
            padding: 25px 35px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            flex-wrap: wrap;
            gap: 15px;
        }}

        .score-display {{
            font-size: 1.1em;
            color: #555;
        }}

        .score-number {{
            font-weight: 600;
            color: #667eea;
            font-size: 1.2em;
        }}

        .btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 500;
            text-decoration: none;
            display: inline-block;
        }}

        .btn-check {{
            background: #667eea;
            color: white;
        }}

        .btn-check:hover {{
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }}

        .btn-submit {{
            background: #4CAF50;
            color: white;
        }}

        .btn-submit:hover {{
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
        }}

        .btn-secondary {{
            background: #757575;
            color: white;
        }}

        .btn-secondary:hover {{
            background: #616161;
            transform: translateY(-2px);
        }}

        .btn:disabled {{
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }}

        .navigation {{
            background: white;
            padding: 25px 35px;
            border-radius: 0 0 15px 15px;
            display: flex;
            justify-content: space-between;
            gap: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .toast {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #333;
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 1000;
            display: none;
            animation: slideIn 0.3s ease-out;
        }}

        @keyframes slideIn {{
            from {{
                transform: translateX(400px);
                opacity: 0;
            }}
            to {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}

        .toast.show {{
            display: block;
        }}

        .score-modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 2000;
            justify-content: center;
            align-items: center;
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
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }}

        .score-modal-content h2 {{
            color: #333;
            margin-bottom: 25px;
            font-size: 2em;
        }}

        .final-score {{
            font-size: 4em;
            font-weight: bold;
            color: #667eea;
            margin: 20px 0;
        }}

        .score-message {{
            font-size: 1.2em;
            color: #555;
            margin: 20px 0;
        }}

        .score-details {{
            margin: 25px 0;
            text-align: left;
            padding: 20px;
            background: #f8f9ff;
            border-radius: 10px;
        }}

        .score-details p {{
            margin: 8px 0;
            color: #555;
        }}

        .btn-close-modal {{
            padding: 12px 40px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            cursor: pointer;
            margin-top: 20px;
        }}

        .btn-close-modal:hover {{
            background: #5568d3;
        }}

        @media (max-width: 768px) {{
            header, .content, .action-bar, .navigation {{
                padding: 20px;
            }}

            h1 {{
                font-size: 1.5em;
            }}

            .section-title-box {{
                flex-direction: column;
                align-items: flex-start;
                gap: 5px;
            }}

            .section-label {{
                border-right: none;
                border-bottom: 2px solid rgba(255,255,255,0.3);
                padding-right: 0;
                padding-bottom: 5px;
            }}

            .action-bar, .navigation {{
                flex-direction: column;
            }}

            .action-bar > div {{
                width: 100%;
                display: flex;
                justify-content: center;
                gap: 10px;
            }}

            .navigation {{
                gap: 10px;
            }}

            .navigation .btn {{
                flex: 1;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="breadcrumb">
                <a href="index.html">一对一首页</a> &gt; 
                <a href="index.html">第1课：新起点 得救</a> &gt; 
                第{section_num}节
            </div>
            <h1>第1课：新起点 得救</h1>
            <div class="section-title-box">
                <span class="section-label">第{section_num}节</span>
                <span class="section-name">{section_title}</span>
            </div>
        </header>

        <div class="content">
            <div class="question-block" data-question-id="1">
                <div class="question-header">
                    <span class="question-number">1.</span>
                    <span class="question-text">{description}</span>
                </div>
                <div class="answers-area">
{verses_html}
                </div>
            </div>
        </div>

        <div class="action-bar">
            <div class="score-display">
                已完成: <span class="score-number" id="scoreDisplay">0/{len(verses)}</span>
            </div>
            <div>
                <button class="btn btn-check" onclick="checkAnswers()">✓ 批改</button>
                <button class="btn btn-submit" onclick="submitAnswers()">📝 提交成绩</button>
                <button class="btn btn-secondary" onclick="clearAnswers()">🔄 清空</button>
            </div>
        </div>

        <div class="navigation">
            <a href="{prev_link}" class="btn btn-secondary" {prev_disabled}>← 上一节</a>
            <a href="index.html" class="btn btn-secondary">返回目录</a>
            <a href="{next_link}" class="btn btn-check">{next_text}</a>
        </div>
    </div>

    <div class="toast" id="toast"></div>

    <div class="score-modal" id="scoreModal">
        <div class="score-modal-content">
            <h2>🎉 成绩报告</h2>
            <div class="final-score" id="finalScore">-</div>
            <div class="score-message" id="scoreMessage"></div>
            <div class="score-details" id="scoreDetails"></div>
            <button class="btn-close-modal" onclick="closeScoreModal()">确定</button>
        </div>
    </div>

    <script>
        // 页面配置
        const CONFIG = {{
            courseNum: 1,
            sectionNum: {section_num},
            storageKey: 'one2one_C1_S{section_num}_progress'
        }};

        // 答案数据
        let answersData = {json.dumps({'verses': verses}, ensure_ascii=False, indent=8)};

        // 当前提示级别 {{reference: level}}
        let hintLevels = {{}};

        // 页面加载时执行
        document.addEventListener('DOMContentLoaded', function() {{
            loadProgress();
            updateScore();
        }});

        // 加载进度
        function loadProgress() {{
            const saved = localStorage.getItem(CONFIG.storageKey);
            if (saved) {{
                try {{
                    const data = JSON.parse(saved);
                    Object.keys(data).forEach(ref => {{
                        const input = document.querySelector(`textarea[data-reference="${{ref}}"]`);
                        if (input) input.value = data[ref];
                    }});
                }} catch(e) {{
                    console.error('加载进度失败:', e);
                }}
            }}
        }}

        // 保存进度
        function saveProgress() {{
            const inputs = document.querySelectorAll('.answer-input');
            const data = {{}};
            inputs.forEach(input => {{
                const ref = input.dataset.reference;
                if (ref && input.value.trim()) {{
                    data[ref] = input.value;
                }}
            }});
            localStorage.setItem(CONFIG.storageKey, JSON.stringify(data));
        }}

        // 自动保存
        document.addEventListener('input', function(e) {{
            if (e.target.classList.contains('answer-input')) {{
                saveProgress();
                updateScore();
            }}
        }});

        // 更新成绩显示
        function updateScore() {{
            const inputs = document.querySelectorAll('.answer-input');
            const total = inputs.length;
            let filled = 0;
            
            inputs.forEach(input => {{
                if (input.value.trim()) filled++;
            }});
            
            document.getElementById('scoreDisplay').textContent = `${{filled}}/${{total}}`;
        }}

        // 批改答案
        function checkAnswers() {{
            const inputs = document.querySelectorAll('.answer-input');
            let correct = 0;
            let total = 0;
            
            inputs.forEach(input => {{
                const ref = input.dataset.reference;
                const userAnswer = input.value.trim();
                
                if (!userAnswer) return;
                
                total++;
                const verse = answersData.verses.find(v => v.reference === ref);
                if (!verse) return;
                
                const standardAnswer = verse.text || '';
                const similarity = calculateSimilarity(userAnswer, standardAnswer);
                
                const feedback = input.parentElement.querySelector('.answer-feedback');
                feedback.classList.remove('correct', 'incorrect');
                
                if (similarity >= 0.8) {{
                    input.classList.remove('incorrect');
                    input.classList.add('correct');
                    feedback.classList.add('correct');
                    feedback.textContent = '✓ 正确！';
                    correct++;
                }} else {{
                    input.classList.remove('correct');
                    input.classList.add('incorrect');
                    feedback.classList.add('incorrect');
                    feedback.textContent = `✗ 答案不够准确，相似度：${{Math.round(similarity * 100)}}%`;
                }}
                
                feedback.classList.add('show');
            }});
            
            if (total > 0) {{
                const score = Math.round((correct / total) * 100);
                showToast(`批改完成！正确率：${{score}}% (${{correct}}/${{total}})`);
            }} else {{
                showToast('请先填写答案！');
            }}
        }}

        // 计算相似度
        function calculateSimilarity(str1, str2) {{
            const s1 = str1.replace(/\\s+/g, '').toLowerCase();
            const s2 = str2.replace(/\\s+/g, '').toLowerCase();
            
            if (s1 === s2) return 1.0;
            
            let matches = 0;
            const len = Math.min(s1.length, s2.length);
            
            for (let i = 0; i < len; i++) {{
                if (s1[i] === s2[i]) matches++;
            }}
            
            const maxLen = Math.max(s1.length, s2.length);
            return matches / maxLen;
        }}

        // 显示部分提示
        function showPartialHint(questionId, reference) {{
            const verse = answersData.verses.find(v => v.reference === reference);
            if (!verse || !verse.text) {{
                showToast('暂无提示');
                return;
            }}
            
            const currentLevel = hintLevels[reference] || 0;
            const text = verse.text;
            const button = event.target;
            
            let hint = '';
            let newLevel = currentLevel;
            
            if (currentLevel === 0) {{
                hint = text.substring(0, 2) + '...';
                button.textContent = '💡 更多提示';
                newLevel = 1;
            }} else if (currentLevel === 1) {{
                hint = text.substring(0, 4) + '...';
                button.textContent = '💡 完整提示';
                newLevel = 2;
            }} else {{
                hint = text;
                button.textContent = '💡 提示';
                newLevel = 0;
            }}
            
            hintLevels[reference] = newLevel;
            showToast(`提示：${{hint}}`);
        }}

        // 显示完整答案
        function showFullHint(questionId, reference) {{
            const verse = answersData.verses.find(v => v.reference === reference);
            if (!verse) {{
                showToast('暂无答案');
                return;
            }}
            
            const answerDiv = document.querySelector(`.standard-answer[data-ref="${{reference}}"]`);
            if (!answerDiv) return;
            
            let html = '<strong>📖 标准答案：</strong>';
            
            if (verse.text) {{
                html += '<div class="version-section">';
                html += '<div class="version-label">和合本：</div>';
                html += `<div class="version-text">${{verse.text}}</div>`;
                html += '</div>';
            }}
            
            if (verse.text_alt) {{
                html += '<div class="version-section">';
                html += '<div class="version-label">新译本：</div>';
                html += `<div class="version-text">${{verse.text_alt}}</div>`;
                html += '</div>';
            }}
            
            answerDiv.innerHTML = html;
            answerDiv.classList.toggle('show');
        }}

        // 提交答案
        function submitAnswers() {{
            const inputs = document.querySelectorAll('.answer-input');
            let total = inputs.length;
            let filled = 0;
            let correct = 0;
            
            inputs.forEach(input => {{
                const userAnswer = input.value.trim();
                if (!userAnswer) return;
                
                filled++;
                const ref = input.dataset.reference;
                const verse = answersData.verses.find(v => v.reference === ref);
                if (!verse) return;
                
                const standardAnswer = verse.text || '';
                const similarity = calculateSimilarity(userAnswer, standardAnswer);
                if (similarity >= 0.8) correct++;
            }});
            
            if (filled === 0) {{
                showToast('请先填写答案！');
                return;
            }}
            
            const score = Math.round((correct / total) * 100);
            const percentage = filled === total ? 100 : Math.round((filled / total) * 100);
            
            document.getElementById('finalScore').textContent = score + '分';
            
            let message = '';
            if (score >= 90) message = '优秀！继续保持！';
            else if (score >= 80) message = '良好！还有进步空间';
            else if (score >= 60) message = '及格了，继续努力！';
            else message = '需要加强，建议复习';
            
            document.getElementById('scoreMessage').textContent = message;
            document.getElementById('scoreDetails').innerHTML = `
                <p>✓ 正确：${{correct}} 题</p>
                <p>✗ 错误：${{filled - correct}} 题</p>
                <p>○ 未填：${{total - filled}} 题</p>
                <p>📊 完成度：${{percentage}}%</p>
            `;
            
            document.getElementById('scoreModal').classList.add('show');
        }}

        // 关闭成绩弹窗
        function closeScoreModal() {{
            document.getElementById('scoreModal').classList.remove('show');
        }}

        // 清空答案
        function clearAnswers() {{
            if (!confirm('确定要清空所有答案吗？')) return;
            
            document.querySelectorAll('.answer-input').forEach(input => {{
                input.value = '';
                input.classList.remove('correct', 'incorrect');
            }});
            
            document.querySelectorAll('.answer-feedback').forEach(feedback => {{
                feedback.classList.remove('show');
            }});
            
            document.querySelectorAll('.standard-answer').forEach(answer => {{
                answer.classList.remove('show');
            }});
            
            localStorage.removeItem(CONFIG.storageKey);
            updateScore();
            showToast('已清空所有答案');
        }}

        // 显示提示消息
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
    
    # 写入文件
    output_file = f"courses/one2one_C1_S{section_num}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"  ✅ 生成成功: {output_file}")
    return True

def main():
    """主函数：生成第1课的2-14节"""
    print("=" * 60)
    print("🚀 开始生成第1课的第2-14节HTML页面")
    print("=" * 60)
    
    # 确保目录存在
    Path('courses').mkdir(exist_ok=True)
    
    success_count = 0
    fail_count = 0
    
    # 生成2-14节
    for section_num in range(2, 15):
        print(f"\n📖 处理第1课第{section_num}节...")
        
        # 加载JSON数据
        json_data = load_json_data(section_num)
        if not json_data:
            fail_count += 1
            continue
        
        # 生成HTML
        if generate_html_for_section(section_num, json_data):
            success_count += 1
        else:
            fail_count += 1
    
    print("\n" + "=" * 60)
    print("🎉 完成！")
    print(f"  ✅ 成功生成: {success_count} 个页面")
    print(f"  ❌ 失败: {fail_count} 个页面")
    print("=" * 60)

if __name__ == '__main__':
    main()
