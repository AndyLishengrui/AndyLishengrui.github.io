#!/usr/bin/env python3
"""
修复成绩统计逻辑脚本
解决总题数统计错误的问题，确保按问题数量而不是答案框数量统计
"""

import os
import glob
import re

def fix_score_statistics(html_file):
    """修复单个HTML文件中的成绩统计逻辑"""
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找并替换统计逻辑
        old_pattern = r'// 提交成绩(?:// 提交成绩)?\s*async function submitAnswers\(\) \{\s*await loadStandardAnswers\(\);\s*let totalQuestions = 0;\s*let correctCount = 0;\s*let partialCount = 0;\s*let incorrectCount = 0;\s*document\.querySelectorAll\(\'\.answer-input\'\)\.forEach\(input => \{\s*const ref = input\.dataset\.reference;\s*const hasAnswer = input\.dataset\.hasAnswer === \'true\';\s*if \(\!ref \|\| \!hasAnswer\) \{\s*return;\s*\}\s*const questionId = input\.dataset\.question;\s*const answerKey = `q\$\{questionId\}_\$\{ref\}`;\s*const answerInfo = standardAnswers\[answerKey\];\s*if \(\!answerInfo \|\| \!answerInfo\.has_data\) \{\s*return;\s*\}\s*totalQuestions\+\+;\s*const userAnswer = input\.value\.trim\(\);\s*const standardAnswer = answerInfo\.text \|\| \'\';\s*const similarity = calculateSimilarity\(userAnswer, standardAnswer\);\s*if \(similarity >= 0\.85\) \{\s*correctCount\+\+;\s*\} else if \(similarity >= 0\.6\) \{\s*partialCount\+\+;\s*\} else \{'
        
        # 检查是否包含旧的统计逻辑
        if 'totalQuestions++' in content and 'questionStats' not in content:
            print(f"  🔧 修复文件: {os.path.basename(html_file)}")
            
            # 替换整个submitAnswers函数
            submit_function_pattern = r'(// 提交成绩(?:// 提交成绩)?\s*async function submitAnswers\(\) \{[\s\S]*?)(\s+// 保存进度)'
            
            new_submit_function = '''// 提交成绩
        async function submitAnswers() {
            await loadStandardAnswers();
            
            // 按问题ID统计，避免重复计数
            const questionStats = {};
            let totalInputs = 0;
            let correctInputs = 0;
            let partialInputs = 0;
            let incorrectInputs = 0;
            
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
                
                totalInputs++;
                
                // 初始化问题统计
                if (!questionStats[questionId]) {
                    questionStats[questionId] = {
                        total: 0,
                        correct: 0,
                        partial: 0,
                        incorrect: 0
                    };
                }
                questionStats[questionId].total++;
                
                const userAnswer = input.value.trim();
                const standardAnswer = answerInfo.text || '';
                
                const similarity = calculateSimilarity(userAnswer, standardAnswer);
                
                if (similarity >= 0.85) {
                    correctInputs++;
                    questionStats[questionId].correct++;
                } else if (similarity >= 0.6) {
                    partialInputs++;
                    questionStats[questionId].partial++;
                } else {
                    incorrectInputs++;
                    questionStats[questionId].incorrect++;
                }
            });
            
            // 计算问题级别的统计
            let totalQuestions = Object.keys(questionStats).length;
            let correctCount = 0;
            let partialCount = 0;
            let incorrectCount = 0;
            
            Object.values(questionStats).forEach(stats => {
                const accuracy = stats.total > 0 ? stats.correct / stats.total : 0;
                if (accuracy >= 0.8) {
                    correctCount++;
                } else if (accuracy >= 0.4) {
                    partialCount++;
                } else {
                    incorrectCount++;
                }
            });
            
            // 计算得分
            const score = totalQuestions > 0 
                ? Math.round(((correctCount + partialCount * 0.6) / totalQuestions) * 100) 
                : 0;
            
            // 显示成绩模态框
            const finalScoreEl = document.getElementById('finalScore');
            const scoreMessageEl = document.getElementById('scoreMessage');
            const scoreDetailsEl = document.getElementById('scoreDetails');
            
            finalScoreEl.textContent = score + '分';
            
            // 根据分数显示不同的消息
            if (totalQuestions === 0) {
                scoreMessageEl.textContent = '本节暂无可评分的题目';
            } else if (score >= 90) {
                scoreMessageEl.textContent = '优秀！你掌握得非常好！';
            } else if (score >= 75) {
                scoreMessageEl.textContent = '良好！继续加油！';
            } else if (score >= 60) {
                scoreMessageEl.textContent = '及格！建议再复习一下';
            } else {
                scoreMessageEl.textContent = '继续努力！多读几遍经文吧';
            }
            
            scoreDetailsEl.innerHTML = `
                <p>📊 总题数: ${totalQuestions} (共 ${totalInputs} 个填空)</p>
                <p>✅ 完全正确: ${correctCount}</p>
                <p>⚠️ 部分正确: ${partialCount}</p>
                <p>❌ 需要改进: ${incorrectCount}</p>
            `;
            
            document.getElementById('scoreModal').classList.add('show');
            '''
            
            def replace_function(match):
                return new_submit_function + match.group(2)
            
            new_content = re.sub(submit_function_pattern, replace_function, content, flags=re.DOTALL)
            
            if new_content != content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True
            else:
                print(f"    ⚠️  未能成功替换函数内容")
                return False
        else:
            print(f"  ✅ 跳过 (已修复或无需修复): {os.path.basename(html_file)}")
            return False
            
    except Exception as e:
        print(f"  ❌ 处理文件时出错: {e}")
        return False

def main():
    """主函数"""
    print("🔧 开始修复成绩统计逻辑...")
    print("=" * 60)
    
    foundation_dir = "/Users/andyshengruilee/Documents/website/integrated-site/foundation"
    
    # 获取所有HTML文件
    html_files = glob.glob(os.path.join(foundation_dir, "foundation_L*_S*.html"))
    html_files.sort()
    
    total_files = len(html_files)
    fixed_files = 0
    
    for html_file in html_files:
        filename = os.path.basename(html_file)
        print(f"\n📄 处理文件: {filename}")
        
        if fix_score_statistics(html_file):
            fixed_files += 1
    
    print("\n" + "=" * 60)
    print(f"🎉 修复完成!")
    print(f"📊 统计信息:")
    print(f"   - 处理文件数: {total_files}")
    print(f"   - 修复文件数: {fixed_files}")
    print(f"   - 跳过文件数: {total_files - fixed_files}")
    
    if fixed_files > 0:
        print("\n✨ 修复内容:")
        print("   - ✅ 按问题数量统计，而不是答案框数量")
        print("   - ✅ 显示问题数和填空数的区别")
        print("   - ✅ 改进问题级别的正确率计算")
        print("   - ✅ 提供更准确的成绩报告")

if __name__ == "__main__":
    main()