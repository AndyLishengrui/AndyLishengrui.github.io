#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复被损坏的checkAnswers函数
"""

import os
import re
from pathlib import Path

def restore_check_answers_function(html_file):
    """恢复并修复HTML文件中的checkAnswers函数"""
    
    # 读取HTML文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 正确的checkAnswers函数
    correct_function = '''        // 检查答案
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
        }

        // 提交成绩'''
    
    # 更精确的匹配模式 - 找到损坏的函数并用正确的替换
    # 匹配从 "// 检查答案" 开始到下一个函数声明
    pattern = r'(\s+)// 检查答案[^}]*async function checkAnswers\(\)[^}]*\}[^}]*\}[^}]*\}[^/]*(?=\s*//\s*提交成绩)'
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        indent = match.group(1)
        new_content = content[:match.start()] + correct_function + content[match.end():]
    else:
        # 如果找不到，尝试更宽松的模式
        pattern2 = r'(\s+)async function checkAnswers\(\)[^}]*\}[^}]*\}[^}]*\}.*?(?=\s*async function submitAnswers|//\s*提交成绩)'
        match = re.search(pattern2, content, re.DOTALL)
        if match:
            # 保留缩进，替换函数
            lines = correct_function.split('\n')
            indented_function = '\n'.join([match.group(1) + line.lstrip() if line.strip() else line for line in lines])
            new_content = content[:match.start()] + indented_function + content[match.end():]
        else:
            print(f"  ⚠️  无法找到checkAnswers函数模式")
            return False
    
    # 写回文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    """主函数"""
    foundation_dir = Path(__file__).parent
    
    # 处理已更新的文件
    problem_files = [
        'foundation_L1_S1.html',
        'foundation_L1_S2.html', 
        'foundation_L1_S3.html',
        'foundation_L1_S4.html',
        'foundation_L1_S5.html',
        'foundation_L2_S1.html',
        'foundation_L2_S2.html',
        'foundation_L2_S3.html',
        'foundation_L2_S4.html',
        'foundation_L3_S1.html',
        'foundation_L3_S2.html',
        'foundation_L3_S3.html',
        'foundation_L3_S4.html'
    ]
    
    print("开始修复被损坏的checkAnswers函数...")
    print(f"需要修复 {len(problem_files)} 个文件\n")
    
    fixed_count = 0
    for filename in problem_files:
        html_file = foundation_dir / filename
        if html_file.exists():
            print(f"修复: {filename}")
            if restore_check_answers_function(html_file):
                print(f"  ✅ 已修复")
                fixed_count += 1
            else:
                print(f"  ❌ 修复失败")
            print()
        else:
            print(f"跳过: {filename} (文件不存在)")
    
    print(f"\n完成！共修复了 {fixed_count} 个HTML文件")

if __name__ == '__main__':
    main()