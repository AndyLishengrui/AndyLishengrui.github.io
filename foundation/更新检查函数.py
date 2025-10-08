#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新HTML文件中的checkAnswers函数
"""

import os
import re
from pathlib import Path

def update_check_answers_function(html_file):
    """更新HTML文件中的checkAnswers函数"""
    
    # 读取HTML文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 新的checkAnswers函数
    new_function = '''        // 检查答案
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
                // 平滑滚动到第一个错误位置
                firstIncorrect.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'center' 
                });
                // 短暂聚焦到第一个错误输入框
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
        }'''
    
    # 查找现有的checkAnswers函数
    pattern = r'(\s+)// 检查答案\s*\n\s*async function checkAnswers\(\) \{[^}]+\}(?:\s*\{[^}]*\})*[^}]*\}'
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        # 替换现有函数
        new_content = content[:match.start()] + new_function + content[match.end():]
        
        # 写回文件
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    
    return False

def main():
    """主函数"""
    foundation_dir = Path(__file__).parent
    
    # 处理第1-3课，排除已经更新的L1_S3
    html_files = []
    for i in range(1, 4):
        files = list(foundation_dir.glob(f'foundation_L{i}_S*.html'))
        html_files.extend([f for f in files if f.name != 'foundation_L1_S3.html'])
    
    html_files.sort()
    
    print("开始更新第1-3课的checkAnswers函数...")
    print(f"找到 {len(html_files)} 个HTML文件需要处理\n")
    
    updated_count = 0
    for html_file in html_files:
        print(f"处理: {html_file.name}")
        if update_check_answers_function(html_file):
            print(f"  ✅ 已更新checkAnswers函数")
            updated_count += 1
        else:
            print(f"  ❌ 未找到checkAnswers函数")
        print()
    
    print(f"\n完成！共更新了 {updated_count} 个HTML文件")

if __name__ == '__main__':
    main()