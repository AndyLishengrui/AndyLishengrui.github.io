#!/usr/bin/env python3
"""
更新成绩统计显示脚本
同时显示问题数和答案框数，成绩按答案框正确数计算
"""

import os
import glob
import re

def update_score_display(html_file):
    """更新单个HTML文件中的成绩统计显示"""
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changes_made = 0
        
        # 1. 更新问题级别统计变量名
        old_pattern1 = r'let correctCount = 0;\s*let partialCount = 0;\s*let incorrectCount = 0;'
        new_pattern1 = '''let questionCorrectCount = 0;
            let questionPartialCount = 0;
            let questionIncorrectCount = 0;'''
        
        if re.search(old_pattern1, content):
            content = re.sub(old_pattern1, new_pattern1, content)
            changes_made += 1
        
        # 2. 更新问题统计逻辑
        old_pattern2 = r'if \(accuracy >= 0\.8\) \{\s*correctCount\+\+;\s*\} else if \(accuracy >= 0\.4\) \{\s*partialCount\+\+;\s*\} else \{\s*incorrectCount\+\+;'
        new_pattern2 = '''if (accuracy >= 0.8) {
                    questionCorrectCount++;
                } else if (accuracy >= 0.4) {
                    questionPartialCount++;
                } else {
                    questionIncorrectCount++;'''
        
        if re.search(old_pattern2, content):
            content = re.sub(old_pattern2, new_pattern2, content)
            changes_made += 1
        
        # 3. 更新分数计算基准
        old_pattern3 = r'const score = totalQuestions > 0[^?]*\? Math\.round\(\(\(correctCount \+ partialCount \* 0\.6\) / totalQuestions\) \* 100\)'
        new_pattern3 = '''const score = totalInputs > 0 
                ? Math.round(((correctInputs + partialInputs * 0.6) / totalInputs) * 100)'''
        
        if re.search(old_pattern3, content):
            content = re.sub(old_pattern3, new_pattern3, content)
            changes_made += 1
        
        # 4. 更新消息判断条件
        old_pattern4 = r'if \(totalQuestions === 0\) \{'
        new_pattern4 = 'if (totalInputs === 0) {'
        
        if re.search(old_pattern4, content):
            content = re.sub(old_pattern4, new_pattern4, content)
            changes_made += 1
        
        # 5. 更新详细统计显示
        old_pattern5 = r'scoreDetailsEl\.innerHTML = `[^`]*`;'
        new_pattern5 = '''scoreDetailsEl.innerHTML = `
                <p>📊 总题数: ${totalQuestions} 题 | 总答案框: ${totalInputs} 个</p>
                <p>📋 问题统计: ✅${questionCorrectCount} ⚠️${questionPartialCount} ❌${questionIncorrectCount}</p>
                <p>📝 答案框统计: ✅${correctInputs} ⚠️${partialInputs} ❌${incorrectInputs}</p>
                <p>🎯 成绩计算: 基于答案框正确率 (${Math.round((correctInputs/totalInputs)*100)}% 完全正确)</p>
            `;'''
        
        if re.search(old_pattern5, content):
            content = re.sub(old_pattern5, new_pattern5, content)
            changes_made += 1
        
        if changes_made > 0:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ 修复文件: {os.path.basename(html_file)} (修改项数: {changes_made})")
            return True
        else:
            print(f"  ⚪ 跳过文件: {os.path.basename(html_file)} (无需修改)")
            return False
            
    except Exception as e:
        print(f"  ❌ 处理文件时出错: {e}")
        return False

def main():
    """主函数"""
    print("🔧 开始更新成绩统计显示...")
    print("=" * 60)
    
    foundation_dir = "/Users/andyshengruilee/Documents/website/integrated-site/foundation"
    
    # 获取所有HTML文件
    html_files = glob.glob(os.path.join(foundation_dir, "foundation_L*_S*.html"))
    html_files.sort()
    
    total_files = len(html_files)
    updated_files = 0
    
    for html_file in html_files:
        filename = os.path.basename(html_file)
        print(f"\n📄 处理文件: {filename}")
        
        if update_score_display(html_file):
            updated_files += 1
    
    print("\n" + "=" * 60)
    print(f"🎉 更新完成!")
    print(f"📊 统计信息:")
    print(f"   - 处理文件数: {total_files}")
    print(f"   - 更新文件数: {updated_files}")
    print(f"   - 跳过文件数: {total_files - updated_files}")
    
    if updated_files > 0:
        print("\n✨ 更新内容:")
        print("   - ✅ 同时显示问题数和答案框数")
        print("   - ✅ 分别统计问题正确率和答案框正确率") 
        print("   - ✅ 成绩按答案框正确数计算")
        print("   - ✅ 提供详细的统计信息展示")
        print("   - ✅ 清晰区分题目统计和填空统计")

if __name__ == "__main__":
    main()