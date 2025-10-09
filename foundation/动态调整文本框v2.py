#!/usr/bin/env python3
"""
动态调整文本框高度脚本 - 改进版
根据答案内容的实际长度来设置合适的文本框行数，优化页面布局
"""

import json
import os
import glob
import re

def calculate_rows_for_text(text):
    """根据文本内容计算合适的行数"""
    if not text:
        return 3  # 默认3行
    
    # 计算文本长度
    text_length = len(text.strip())
    
    if text_length <= 50:  # 短文本
        return 2
    elif text_length <= 120:  # 中等文本
        return 3
    elif text_length <= 200:  # 较长文本
        return 4
    elif text_length <= 300:  # 长文本
        return 5
    else:  # 很长文本
        return 6

def process_html_file(html_file, answers_data):
    """处理单个HTML文件，调整其中的textarea行数"""
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changes_made = 0
        new_content = content
        
        # 更精确的匹配模式：匹配textarea和紧接着的feedback div
        pattern = r'(<textarea class="answer-input"[^>]*?rows=")(\d+)("[^>]*?></textarea>\s*<div class="answer-feedback" data-ref="([^"]*)")'
        
        def replace_textarea_block(match):
            nonlocal changes_made
            before_rows = match.group(1)
            current_rows = int(match.group(2))
            after_rows_before_ref = match.group(3)
            reference = match.group(4)
            
            # 查找对应的答案数据
            answer_text = ""
            for q_key, answer_data in answers_data.get('answers', {}).items():
                if answer_data.get('reference') == reference:
                    answer_text = answer_data.get('text', '')
                    break
            
            # 计算新的行数
            new_rows = calculate_rows_for_text(answer_text)
            
            if new_rows != current_rows:
                changes_made += 1
                text_preview = ''.join(answer_text.split())[:40] + "..." if len(answer_text) > 40 else answer_text
                print(f"    📏 调整 {reference}: {current_rows}行 → {new_rows}行")
                print(f"       内容: {text_preview}")
                
                return before_rows + str(new_rows) + after_rows_before_ref
            
            return match.group(0)
        
        # 执行替换
        new_content = re.sub(pattern, replace_textarea_block, content, flags=re.DOTALL)
        
        if changes_made > 0:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✅ 完成调整，共修改 {changes_made} 个文本框")
            return changes_made
        else:
            print(f"  ✅ 无需调整")
            return 0
            
    except Exception as e:
        print(f"  ❌ 处理文件时出错: {e}")
        return 0

def main():
    """主函数"""
    print("🎯 开始动态调整文本框高度...")
    print("=" * 60)
    
    foundation_dir = "/Users/andyshengruilee/Documents/website/integrated-site/foundation"
    answers_dir = os.path.join(foundation_dir, "data", "answers")
    
    # 获取所有HTML文件
    html_files = glob.glob(os.path.join(foundation_dir, "foundation_L*_S*.html"))
    html_files.sort()
    
    total_files = 0
    total_changes = 0
    
    for html_file in html_files:
        filename = os.path.basename(html_file)
        print(f"\n📄 处理文件: {filename}")
        
        # 构造对应的JSON文件路径
        json_filename = filename.replace('.html', '.json')
        json_file = os.path.join(answers_dir, json_filename)
        
        if not os.path.exists(json_file):
            print(f"  ⚠️  未找到对应的答案文件: {json_filename}")
            continue
        
        # 加载答案数据
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                answers_data = json.load(f)
        except Exception as e:
            print(f"  ❌ 加载答案数据失败: {e}")
            continue
        
        # 处理HTML文件
        changes = process_html_file(html_file, answers_data)
        total_files += 1
        total_changes += changes
    
    print("\n" + "=" * 60)
    print(f"🎉 处理完成!")
    print(f"📊 统计信息:")
    print(f"   - 处理文件数: {total_files}")
    print(f"   - 调整文本框数: {total_changes}")
    
    if total_changes > 0:
        print("\n💡 调整规则:")
        print("   - 短答案(≤50字符): 2行")
        print("   - 中等答案(51-120字符): 3行") 
        print("   - 较长答案(121-200字符): 4行")
        print("   - 长答案(201-300字符): 5行")
        print("   - 很长答案(>300字符): 6行")
        print("\n🎯 效果:")
        print("   - 页面布局更加紧凑合理")
        print("   - 提升用户体验")
        print("   - 请在浏览器中刷新页面查看效果")

if __name__ == "__main__":
    main()