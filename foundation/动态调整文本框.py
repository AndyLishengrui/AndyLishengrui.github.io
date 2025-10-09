#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import re

def calculate_rows_for_text(text):
    """根据文本内容计算合适的行数"""
    if not text:
        return 3  # 默认3行
    
    # 计算文本行数（按照换行符分割）
    lines = text.split('\n')
    line_count = len(lines)
    
    # 计算字符长度，估算折行
    max_chars_per_line = 50  # 估算每行最多字符数（考虑中文和标点）
    
    total_estimated_lines = 0
    for line in lines:
        # 计算每行实际需要的显示行数
        estimated_lines = max(1, (len(line) + max_chars_per_line - 1) // max_chars_per_line)
        total_estimated_lines += estimated_lines
    
    # 设置行数范围：最少2行，最多8行
    calculated_rows = max(2, min(8, total_estimated_lines))
    
    return calculated_rows

def process_html_file(html_file, answers_data):
    """处理单个HTML文件，调整其中的textarea行数"""
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changes_made = 0
        
        # 查找所有textarea元素（多行匹配）
        textarea_pattern = r'<textarea class="answer-input"[^>]*?rows="(\d+)"[^>]*?data-question="(\d+)"[^>]*?>'
        
        def replace_textarea(match):
            nonlocal changes_made
            full_match = match.group(0)
            current_rows = int(match.group(1))
            question_num = match.group(2)
            
            # 查找对应的答案数据
            answer_text = ""
            # 从HTML中提取data-ref属性来找到对应的经文引用
            ref_match = re.search(r'data-ref="([^"]*)"', full_match)
            if not ref_match:
                # 如果没有data-ref，尝试从下面的div中查找
                remaining_content = content[match.end():]
                next_div_match = re.search(r'<div class="answer-feedback" data-ref="([^"]*)">', remaining_content[:200])
                if next_div_match:
                    reference = next_div_match.group(1)
                else:
                    return full_match
            else:
                reference = ref_match.group(1)
            
            # 在答案数据中查找
            for q_key, answer_data in answers_data.get('answers', {}).items():
                if answer_data.get('reference') == reference:
                    answer_text = answer_data.get('text', '')
                    break
            
            # 计算新的行数
            new_rows = calculate_rows_for_text(answer_text)
            
            if new_rows != current_rows:
                changes_made += 1
                updated_textarea = full_match.replace(f'rows="{current_rows}"', f'rows="{new_rows}"')
                print(f"    📏 调整 {reference}: {current_rows}行 → {new_rows}行 ({''.join(answer_text.split())[:30]}...)")
                return updated_textarea
            
            return full_match
        
        # 执行替换
        new_content = re.sub(textarea_pattern, replace_textarea, content)
        
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
        print("\n💡 建议:")
        print("   - 请在浏览器中刷新页面查看效果")
        print("   - 短答案的文本框现在更紧凑")
        print("   - 长答案的文本框有足够的显示空间")
        print("   - 提升了整体的页面布局体验")

if __name__ == "__main__":
    main()