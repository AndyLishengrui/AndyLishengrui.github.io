#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成第一课第一节
"""

import os

# 从一对一.txt读取原始内容
with open('一对一.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到"得救 1"开始的位置
start_idx = None
for i, line in enumerate(lines):
    if '得救 1' in line:
        start_idx = i
        break

# 提取得救1的内容（到得救2之前）
content_lines = []
if start_idx:
    for i in range(start_idx, len(lines)):
        if '得救 2' in lines[i]:
            break
        content_lines.append(lines[i])

# 获取内容文本
content_text = ''.join(content_lines).strip()
print("提取的内容：")
print("=" * 60)
print(content_text[:500])
print("=" * 60)

# 生成HTML
html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>第1课 第1节 - 问题：罪使我们与神隔绝 | 一对一门徒训练</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
        }

        header {
            background: white;
            border-radius: 15px 15px 0 0;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }

        .breadcrumb {
            color: #888;
            font-size: 0.9em;
            margin-bottom: 10px;
        }

        .breadcrumb a {
            color: #667eea;
            text-decoration: none;
        }

        .breadcrumb a:hover {
            text-decoration: underline;
        }

        h1 {
            color: #333;
            margin-bottom: 15px;
            font-size: 2em;
        }

        .section-title-box {
            display: inline-flex;
            align-items: center;
            gap: 15px;
            margin-top: 15px;
        }

        .section-label {
            display: inline-block;
            border: 2px solid #333;
            padding: 8px 20px;
            font-size: 1.1em;
            font-weight: 500;
            color: #333;
        }

        .section-name {
            font-size: 1.3em;
            color: #333;
            font-weight: 500;
        }

        .content {
            background: white;
            padding: 40px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }

        .content-paragraph {
            line-height: 1.8;
            color: #333;
            margin-bottom: 25px;
            font-size: 1.05em;
            text-align: justify;
        }

        .blank-section {
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }

        .blank-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .blank-reference {
            font-weight: 600;
            color: #667eea;
            font-size: 1.1em;
        }

        .hint-buttons {
            display: flex;
            gap: 10px;
        }

        .btn-hint {
            padding: 6px 12px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.3s;
        }

        .btn-hint:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }

        .answer-input {
            width: 100%;
            min-height: 100px;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 1em;
            font-family: inherit;
            resize: vertical;
            line-height: 1.6;
        }

        .answer-input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .answer-feedback {
            margin-top: 8px;
            padding: 8px 12px;
            border-radius: 5px;
            font-size: 0.9em;
            display: none;
        }

        .answer-feedback.show {
            display: block;
        }

        .answer-feedback.correct {
            background: #d4edda;
            color: #155724;
            border-left: 4px solid #27ae60;
        }

        .answer-feedback.incorrect {
            background: #f8d7da;
            color: #721c24;
            border-left: 4px solid #e74c3c;
        }

        .standard-answer {
            display: none;
            margin-top: 10px;
            padding: 15px;
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 0.95em;
            color: #555;
            line-height: 1.6;
        }

        .standard-answer.show {
            display: block;
        }

        .standard-answer strong {
            color: #667eea;
            display: block;
            margin-bottom: 8px;
        }

        .action-bar {
            background: white;
            padding: 25px 40px;
            border-radius: 0 0 15px 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }

        .score-display {
            font-size: 1.1em;
            color: #333;
            font-weight: 500;
        }

        .score-number {
            color: #667eea;
            font-size: 1.4em;
            font-weight: bold;
        }

        .btn {
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 500;
            margin: 0 5px;
        }

        .btn-check {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-check:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-submit {
            background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
            color: white;
        }

        .btn-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(39, 174, 96, 0.4);
        }

        .btn-clear {
            background: #f5f5f5;
            color: #333;
        }

        .btn-clear:hover {
            background: #e0e0e0;
        }

        .navigation {
            background: white;
            padding: 20px 40px;
            margin-top: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            gap: 15px;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-secondary {
            background: #f5f5f5;
            color: #333;
        }

        .btn-secondary:hover {
            background: #e0e0e0;
        }

        @media (max-width: 768px) {
            body {
                padding: 10px;
            }

            .content {
                padding: 20px;
            }

            .action-bar, .navigation {
                padding: 15px 20px;
            }

            .hint-buttons {
                flex-direction: column;
                width: 100%;
            }

            .btn-hint {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="breadcrumb">
                <a href="../index.html">一对一首页</a> &gt; <a href="../index.html">第1课：新起点 得救</a> &gt; 第1节
            </div>
            <h1>第1课：新起点 得救</h1>
            <div class="section-title-box">
                <span class="section-label">第 1 节</span>
                <span class="section-name">问题：罪使我们与神隔绝</span>
            </div>
        </header>

        <div class="content">
            <div class="content-paragraph">
'''

# 添加内容文本
html_content += content_text.replace('\n', '<br>\n                ')

html_content += '''
            </div>

            <!-- 经文填空：以赛亚书 59:1,2 -->
            <div class="blank-section">
                <div class="blank-header">
                    <span class="blank-reference">📖 以赛亚书 59:1,2</span>
                    <div class="hint-buttons">
                        <button class="btn-hint" onclick="showPartialHint(1, '以赛亚书 59:1,2')">💡 渐进提示</button>
                        <button class="btn-hint" onclick="showFullHint(1, '以赛亚书 59:1,2')">📝 查看答案</button>
                    </div>
                </div>
                <textarea 
                    class="answer-input" 
                    data-question="1" 
                    data-reference="以赛亚书 59:1,2"
                    data-has-answer="true"
                    placeholder="请根据经文引用，写出完整的经文内容..."></textarea>
                <div class="answer-feedback"></div>
                <div class="standard-answer" data-ref="以赛亚书 59:1,2">
                    <strong>📖 标准答案（和合本）：</strong>
                    <p>耶和华的膀臂并非缩短，不能拯救，耳朵并非发沉，不能听见，但你们的罪孽使你们与　神隔绝；你们的罪恶使他掩面不听你们。</p>
                </div>
            </div>
        </div>

        <!-- 操作栏 -->
        <div class="action-bar">
            <div class="score-display">
                完成进度: <span class="score-number" id="progressDisplay">0%</span>
            </div>
            <div>
                <button class="btn btn-check" onclick="checkAnswers()">✓ 批改</button>
                <button class="btn btn-submit" onclick="submitAnswers()">📊 提交</button>
                <button class="btn btn-clear" onclick="clearAnswers()">🔄 清空</button>
            </div>
        </div>

        <div class="navigation">
            <a href="../index.html" class="btn btn-secondary">← 返回目录</a>
            <a href="one2one_C1_S2.html" class="btn btn-primary">下一节 →</a>
        </div>
    </div>

    <script>
        // 设置当前页面的JSON文件路径
        const ANSWER_JSON_FILE = '../data/answers/one2one_C1_S1.json';
        const STORAGE_KEY = 'one2one_C1_S1';

        let hintsUsed = {};
        let answersData = {};

        // 加载答案数据
        async function loadAnswers() {
            try {
                const response = await fetch(ANSWER_JSON_FILE);
                answersData = await response.json();
                console.log('答案数据加载成功:', answersData);
            } catch (error) {
                console.error('加载答案数据失败:', error);
            }
        }

        // 渐进提示
        function showPartialHint(questionNum, reference) {
            const answerKey = `q${questionNum}_${reference}`;
            if (!answersData[answerKey]) {
                alert('暂无提示数据');
                return;
            }

            const answer = answersData[answerKey].version;
            if (!hintsUsed[answerKey]) {
                hintsUsed[answerKey] = 0;
            }

            hintsUsed[answerKey]++;
            const charsToShow = Math.min(hintsUsed[answerKey] * 10, answer.length);
            const hint = answer.substring(0, charsToShow) + '...';

            alert(`提示 ${hintsUsed[answerKey]}：\n${hint}`);
        }

        // 查看完整答案
        function showFullHint(questionNum, reference) {
            const answerDiv = document.querySelector(`.standard-answer[data-ref="${reference}"]`);
            if (answerDiv) {
                answerDiv.classList.toggle('show');
            }
        }

        // 检查答案
        function checkAnswers() {
            const inputs = document.querySelectorAll('.answer-input[data-has-answer="true"]');
            let correct = 0;
            let total = 0;

            inputs.forEach((input, index) => {
                const question = input.dataset.question;
                const reference = input.dataset.reference;
                const userAnswer = input.value.trim();
                const answerKey = `q${question}_${reference}`;

                if (userAnswer && answersData[answerKey]) {
                    total++;
                    const standardAnswer = answersData[answerKey].version;
                    const altAnswer = answersData[answerKey].version_alt;

                    // 简单的相似度判断
                    const similarity = calculateSimilarity(userAnswer, standardAnswer);
                    const feedbackDiv = input.nextElementSibling;

                    if (similarity > 0.8) {
                        correct++;
                        feedbackDiv.className = 'answer-feedback correct show';
                        feedbackDiv.textContent = '✓ 回答正确！';
                    } else if (similarity > 0.5) {
                        feedbackDiv.className = 'answer-feedback partial show';
                        feedbackDiv.textContent = '⚠ 部分正确，请查看标准答案';
                    } else {
                        feedbackDiv.className = 'answer-feedback incorrect show';
                        feedbackDiv.textContent = '✗ 答案不正确，请重新作答';
                    }
                }
            });

            if (total > 0) {
                const percentage = Math.round((correct / total) * 100);
                document.getElementById('progressDisplay').textContent = `${percentage}%`;
                alert(`批改完成！\n正确：${correct}/${total}\n得分：${percentage}%`);
            } else {
                alert('请先填写答案');
            }
        }

        // 计算相似度（简化版）
        function calculateSimilarity(str1, str2) {
            str1 = str1.replace(/\s+/g, '');
            str2 = str2.replace(/\s+/g, '');
            
            let matches = 0;
            const len = Math.min(str1.length, str2.length);
            
            for (let i = 0; i < len; i++) {
                if (str1[i] === str2[i]) matches++;
            }
            
            return matches / Math.max(str1.length, str2.length);
        }

        // 提交答案
        function submitAnswers() {
            const inputs = document.querySelectorAll('.answer-input');
            const answers = {};
            
            inputs.forEach(input => {
                const key = `${input.dataset.question}_${input.dataset.reference}`;
                answers[key] = input.value;
            });
            
            localStorage.setItem(STORAGE_KEY, JSON.stringify(answers));
            alert('答案已保存！');
        }

        // 清空答案
        function clearAnswers() {
            if (confirm('确定要清空所有答案吗？')) {
                document.querySelectorAll('.answer-input').forEach(input => {
                    input.value = '';
                });
                document.querySelectorAll('.answer-feedback').forEach(div => {
                    div.className = 'answer-feedback';
                });
                document.querySelectorAll('.standard-answer').forEach(div => {
                    div.classList.remove('show');
                });
                document.getElementById('progressDisplay').textContent = '0%';
                localStorage.removeItem(STORAGE_KEY);
                hintsUsed = {};
                alert('已清空所有答案');
            }
        }

        // 页面加载时
        window.addEventListener('DOMContentLoaded', () => {
            loadAnswers();
            
            // 恢复之前保存的答案
            const saved = localStorage.getItem(STORAGE_KEY);
            if (saved) {
                const answers = JSON.parse(saved);
                Object.keys(answers).forEach(key => {
                    const [question, ...refParts] = key.split('_');
                    const reference = refParts.join('_');
                    const input = document.querySelector(`.answer-input[data-question="${question}"][data-reference="${reference}"]`);
                    if (input) {
                        input.value = answers[key];
                    }
                });
            }
        });
    </script>
</body>
</html>'''

# 保存文件
output_file = 'courses/one2one_C1_S1.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\n✅ 成功生成: {output_file}")
