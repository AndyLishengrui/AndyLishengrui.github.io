#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全重新生成第一课第一节 - 参考foundation格式
"""

import json
import os

# 第一课第一节的完整内容
section_content = """你相信天地间有神吗？你相信这个世界有一位救世主吗？如果有，他是谁呢？圣经启示我们，天地万物并不是自然就有的，有一位上帝，他是这一切的创造主。可是，如果有神，那为什么我看不见他，也感觉不到他呢？"""

# 标准答案数据
answer_data = {
    "course_num": 1,
    "course_title": "新起点 得救",
    "section_num": 1,
    "section_title": "问题：罪使我们与神隔绝",
    "answers": {
        "q1_以赛亚书 59:1,2": {
            "reference": "以赛亚书 59:1,2",
            "text": "看哪！耶和华的手不是缩短了，以致不能拯救；他的耳朵不是不灵，不能听见；而是你们的罪孽使你们与你们的神隔绝；你们的罪恶使他掩面不顾你们，不听你们的祷告。",
            "version": "新译本",
            "has_data": True
        }
    }
}

# 保存JSON文件
json_file = 'data/answers/one2one_C1_S1.json'
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(answer_data, f, ensure_ascii=False, indent=2)

print(f"✅ 已更新: {json_file}")

# 生成HTML（参考foundation格式）
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

        .question-block {
            margin-bottom: 35px;
            padding: 0;
            background: transparent;
            border: none;
        }

        .question-header {
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
        }

        .question-number {
            flex-shrink: 0;
            margin-right: 10px;
            color: #333;
            font-size: 1em;
        }

        .question-text {
            font-size: 1em;
            color: #333;
            font-weight: normal;
            line-height: 1.6;
        }

        .answers-area {
            margin-left: 30px;
        }

        .reference-with-blank {
            margin-bottom: 25px;
            position: relative;
        }

        .reference-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }

        .reference-text {
            color: #667eea;
            font-size: 0.95em;
            font-weight: 500;
        }

        .hint-buttons {
            display: flex;
            gap: 8px;
        }

        .btn-hint-partial, .btn-hint-full {
            padding: 4px 12px;
            border: none;
            border-radius: 5px;
            font-size: 0.85em;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-hint-partial {
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            color: white;
        }

        .btn-hint-partial:hover {
            transform: translateY(-1px);
            box-shadow: 0 3px 10px rgba(243, 156, 18, 0.3);
        }

        .btn-hint-full {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
        }

        .btn-hint-full:hover {
            transform: translateY(-1px);
            box-shadow: 0 3px 10px rgba(52, 152, 219, 0.3);
        }

        .answer-input {
            width: 100%;
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 12px;
            font-size: 1em;
            font-family: inherit;
            resize: vertical;
            outline: none;
            transition: all 0.3s;
            line-height: 1.6;
            min-height: 100px;
        }

        .answer-input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .answer-input.correct {
            border-color: #27ae60;
            background: rgba(39, 174, 96, 0.05);
        }

        .answer-input.incorrect {
            border-color: #e74c3c;
            background: rgba(231, 76, 60, 0.05);
        }

        .answer-input.partial {
            border-color: #f39c12;
            background: rgba(243, 156, 18, 0.05);
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

        .answer-feedback.partial {
            background: #fff3cd;
            color: #856404;
            border-left: 4px solid #f39c12;
        }

        .standard-answer {
            display: none;
            margin-top: 10px;
            padding: 15px;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 0 5px 5px 0;
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
            font-size: 0.95em;
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
            text-decoration: none;
            display: inline-block;
            font-weight: 500;
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

        .btn-secondary {
            background: #f5f5f5;
            color: #333;
        }

        .btn-secondary:hover {
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

        @media (max-width: 768px) {
            body {
                padding: 10px;
            }

            .content {
                padding: 20px;
            }

            .answers-area {
                margin-left: 10px;
            }

            .action-bar, .navigation {
                padding: 15px 20px;
            }

            .hint-buttons {
                flex-direction: column;
                width: 100%;
            }

            .btn-hint-partial, .btn-hint-full {
                width: 100%;
            }
        }

        .toast {
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
        }

        .toast.show {
            display: block;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
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
                <span class="section-label">第1节</span>
                <span class="section-name">问题：罪使我们与神隔绝</span>
            </div>
        </header>

        <div class="content">
            <div class="question-block" data-question-id="1">
                <div class="question-header">
                    <span class="question-number">1.</span>
                    <span class="question-text">''' + section_content + '''</span>
                </div>
                <div class="answers-area">
                    <div class="reference-with-blank">
                        <div class="reference-header">
                            <span class="reference-text">以赛亚书 59:1,2</span>
                            <div class="hint-buttons">
                                <button class="btn-hint-partial" onclick="showPartialHint('1', '以赛亚书 59:1,2')" title="渐进提示">💡 提示</button>
                                <button class="btn-hint-full" onclick="showFullHint('1', '以赛亚书 59:1,2')" title="显示完整答案">👁️ 答案</button>
                            </div>
                        </div>
                        <textarea class="answer-input" data-question="1" data-reference="以赛亚书 59:1,2" data-has-answer="true"
                               data-hint-progress="0"
                               placeholder="请填写经文内容..."></textarea>
                        <div class="answer-feedback" data-ref="以赛亚书 59:1,2"></div>
                        <div class="standard-answer" data-ref="以赛亚书 59:1,2"></div>
                    </div>
                </div>
            </div>
        </div>

        <div class="action-bar">
            <div class="score-display">
                成绩: <span class="score-number" id="scoreDisplay">0/0</span>
            </div>
            <div>
                <button class="btn btn-check" onclick="checkAnswers()">✓ 批改</button>
                <button class="btn btn-submit" onclick="submitAnswers()">📊 提交</button>
                <button class="btn btn-secondary" onclick="clearAnswers()">🔄 清空</button>
            </div>
        </div>

        <div class="navigation">
            <a href="../index.html" class="btn btn-secondary">返回目录</a>
            <a href="one2one_C1_S2.html" class="btn btn-check">下一节 →</a>
        </div>
    </div>

    <div class="toast" id="toast"></div>

    <script>
        // 存储标准答案
        let standardAnswers = {};
        
        // 页面加载时初始化
        window.addEventListener('load', () => {
            loadStandardAnswers();
            loadProgress();
            updateProgress();
        });

        // 自动保存
        document.querySelectorAll('.answer-input').forEach(input => {
            input.addEventListener('input', () => {
                saveProgress();
                updateProgress();
            });
        });

        // 加载标准答案
        async function loadStandardAnswers() {
            try {
                const response = await fetch('../data/answers/one2one_C1_S1.json');
                const data = await response.json();
                standardAnswers = data.answers || {};
                console.log('答案数据加载成功:', standardAnswers);
            } catch (error) {
                console.error('加载答案数据失败:', error);
            }
        }

        // 显示完整提示（标准答案）
        function showFullHint(questionId, ref) {
            const answerKey = `q${questionId}_${ref}`;
            const answerInfo = standardAnswers[answerKey];
            
            if (!answerInfo || !answerInfo.has_data) {
                showToast('暂无标准答案数据');
                return;
            }

            const answerDiv = document.querySelector(`.standard-answer[data-ref="${ref}"]`);
            
            if (answerDiv.classList.contains('show')) {
                answerDiv.classList.remove('show');
            } else {
                const version = answerInfo.version || '和合本';
                const text = answerInfo.text || '';
                answerDiv.innerHTML = `<strong>📖 标准答案（${version}）：</strong><p>${text}</p>`;
                answerDiv.classList.add('show');
            }
        }

        // 渐进提示（逐步填充答案）
        function showPartialHint(questionId, ref) {
            const input = document.querySelector(`.answer-input[data-question="${questionId}"][data-reference="${ref}"]`);
            const answerKey = `q${questionId}_${ref}`;
            const answerInfo = standardAnswers[answerKey];
            
            if (!answerInfo || !answerInfo.has_data) {
                showToast('暂无提示数据');
                return;
            }

            const standardAnswer = answerInfo.text || '';
            let currentProgress = parseInt(input.dataset.hintProgress) || 0;
            
            currentProgress += 10;
            
            if (currentProgress >= standardAnswer.length) {
                currentProgress = standardAnswer.length;
                showToast('已显示完整答案');
            } else {
                showToast(`已显示前 ${currentProgress} 个字`);
            }
            
            input.value = standardAnswer.substring(0, currentProgress);
            input.dataset.hintProgress = currentProgress;
            
            saveProgress();
            updateProgress();
        }

        // 清空所有答案
        function clearAnswers() {
            if (!confirm('确定要清空所有答案吗？')) {
                return;
            }

            document.querySelectorAll('.answer-input').forEach(input => {
                input.value = '';
                input.dataset.hintProgress = '0';
                input.classList.remove('correct', 'incorrect', 'partial');
            });

            document.querySelectorAll('.answer-feedback').forEach(div => {
                div.classList.remove('show');
            });

            document.querySelectorAll('.standard-answer').forEach(div => {
                div.classList.remove('show');
            });

            localStorage.removeItem('one2one_C1_S1_progress');
            updateProgress();
            showToast('✓ 答案已清空');
        }

        // 检查答案
        async function checkAnswers() {
            await loadStandardAnswers();
            
            let totalAnswerableQuestions = 0;
            let correctCount = 0;
            let incorrectInputs = [];
            
            document.querySelectorAll('.answer-input').forEach(input => {
                const ref = input.dataset.reference;
                const hasAnswer = input.dataset.hasAnswer === 'true';
                
                if (!ref || !hasAnswer) {
                    return;
                }
                
                const questionId = input.dataset.question;
                const answerKey = `q${questionId}_${ref}`;
                const answerInfo = standardAnswers[answerKey];
                
                if (!answerInfo || !answerInfo.has_data) {
                    return;
                }
                
                totalAnswerableQuestions++;
                
                const userAnswer = input.value.trim();
                const standardAnswer = answerInfo.text || '';
                
                // 清除之前的标记
                input.classList.remove('correct', 'incorrect', 'partial');
                
                const feedbackDiv = input.parentElement.querySelector('.answer-feedback');
                
                if (userAnswer === '') {
                    // 空答案 - 标记为错误
                    input.classList.add('incorrect');
                    feedbackDiv.textContent = '✗ 请填写答案';
                    feedbackDiv.className = 'answer-feedback incorrect show';
                    incorrectInputs.push(input);
                } else {
                    // 相似度检查
                    const similarity = calculateSimilarity(userAnswer, standardAnswer);
                    
                    if (similarity >= 0.85) {
                        input.classList.add('correct');
                        feedbackDiv.textContent = '✓ 正确！';
                        feedbackDiv.className = 'answer-feedback correct show';
                        correctCount++;
                    } else if (similarity >= 0.6) {
                        input.classList.add('partial');
                        feedbackDiv.textContent = '△ 部分正确，请对照标准答案修改';
                        feedbackDiv.className = 'answer-feedback partial show';
                        incorrectInputs.push(input);
                    } else {
                        input.classList.add('incorrect');
                        feedbackDiv.textContent = '✗ 不正确，请对照标准答案修改';
                        feedbackDiv.className = 'answer-feedback incorrect show';
                        incorrectInputs.push(input);
                    }
                }
            });
            
            // 如果有错误的答案，定位到第一个错误位置
            if (incorrectInputs.length > 0) {
                const firstIncorrect = incorrectInputs[0];
                firstIncorrect.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'center' 
                });
                setTimeout(() => {
                    firstIncorrect.focus();
                }, 500);
                
                showToast(`❌ 发现 ${incorrectInputs.length} 个错误，已定位到第一个错误`);
            } else if (correctCount === totalAnswerableQuestions && totalAnswerableQuestions > 0) {
                showToast('🎉 所有答案都正确！');
            } else if (totalAnswerableQuestions === 0) {
                showToast('ℹ️ 本节没有可检查的题目');
            } else {
                showToast(`✓ 检查完成 - ${correctCount}/${totalAnswerableQuestions} 正确`);
            }
            
            updateProgress();
        }

        // 提交成绩
        async function submitAnswers() {
            await checkAnswers();
            showToast('✓ 答案已提交并保存');
        }

        // 计算文本相似度（LCS算法）
        function calculateSimilarity(text1, text2) {
            text1 = text1.replace(/\\s+/g, '');
            text2 = text2.replace(/\\s+/g, '');
            
            const len1 = text1.length;
            const len2 = text2.length;
            const dp = Array(len1 + 1).fill(0).map(() => Array(len2 + 1).fill(0));
            
            for (let i = 1; i <= len1; i++) {
                for (let j = 1; j <= len2; j++) {
                    if (text1[i - 1] === text2[j - 1]) {
                        dp[i][j] = dp[i - 1][j - 1] + 1;
                    } else {
                        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                    }
                }
            }
            
            const lcs = dp[len1][len2];
            return lcs / Math.max(len1, len2);
        }

        function loadProgress() {
            const saved = localStorage.getItem('one2one_C1_S1_progress');
            if (saved) {
                const data = JSON.parse(saved);
                Object.keys(data).forEach(key => {
                    const [question, ref] = key.split('_', 2);
                    const input = document.querySelector(`.answer-input[data-question="${question}"][data-reference="${ref}"]`);
                    if (input && data[key]) {
                        input.value = data[key];
                    }
                });
            }
        }

        function saveProgress() {
            const progress = {};
            document.querySelectorAll('.answer-input').forEach(input => {
                const question = input.dataset.question;
                const ref = input.dataset.reference;
                const key = `${question}_${ref}`;
                progress[key] = input.value;
            });
            localStorage.setItem('one2one_C1_S1_progress', JSON.stringify(progress));
        }

        function updateProgress() {
            let answered = 0;
            let total = 0;
            
            document.querySelectorAll('.answer-input[data-has-answer="true"]').forEach(input => {
                total++;
                if (input.value.trim()) {
                    answered++;
                }
            });
            
            document.getElementById('scoreDisplay').textContent = `${answered}/${total}`;
        }

        function showToast(message) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }
    </script>
</body>
</html>'''

# 保存HTML文件
html_file = 'courses/one2one_C1_S1.html'
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ 已生成: {html_file}")
print("\n✨ 完成！页面已完全按照foundation格式重新生成")
