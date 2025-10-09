#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复不完整的题目内容
"""

import os
import re
from pathlib import Path

# 不完整题目的修复映射
INCOMPLETE_QUESTIONS = {
    # L1_S1
    "你相信万物都是藉着神的话造成的吗？你是否有因着犯": "你相信万物都是藉着神的话造成的吗？你是否有因着犯罪而远离了神？请分享你如何重新与神建立关系。",
    
    # L1_S3  
    "罪可以透过善行来抵消吗？你如何看待神对罪的终极解": "罪可以透过善行来抵消吗？你如何看待神对罪的终极解决方案？请分享你对福音的理解。",
    
    # L5_S1
    "花一些时间默想，神的话在你的生命中是否有影响力。": "花一些时间默想，神的话在你的生命中是否有影响力？你如何在日常生活中应用神的话语？",
    
    # L8_S3
    "你在本节学习到了什么？要如何应用到生活中？你是否": "你在本节学习到了什么？要如何应用到生活中？你是否愿意更加信靠神的供应？",
    
    # L9_S3
    "你对神的信心带出了你的忠心吗？你在本节学习到了什": "你对神的信心带出了你的忠心吗？你在本节学习到了什么？要如何应用到生活中？",
    
    # L10_S1
    "你认为钱财是有危险的吗？你是否很想发财？本课的教": "你认为钱财是有危险的吗？你是否很想发财？本课的教导对你有什么提醒？",
    
    # L11_S1
    "你在本节学习到了什么？要如何应用到生活中？神有没": "你在本节学习到了什么？要如何应用到生活中？神有没有呼召你去做特别的事工？"
}

def fix_incomplete_questions(html_file):
    """修复HTML文件中的不完整题目"""
    
    # 读取HTML文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 修复每个不完整的题目
    for incomplete, complete in INCOMPLETE_QUESTIONS.items():
        if incomplete in content:
            content = content.replace(incomplete, complete)
            print(f"    修复: {incomplete[:30]}... → {complete[:30]}...")
    
    # 如果内容有变化，写回文件
    if content != original_content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    """主函数"""
    foundation_dir = Path(__file__).parent
    
    # 查找所有foundation HTML文件
    html_files = list(foundation_dir.glob('foundation_L*.html'))
    html_files.sort()
    
    print("开始修复不完整的题目...")
    print(f"找到 {len(html_files)} 个HTML文件需要检查\n")
    
    updated_count = 0
    for html_file in html_files:
        print(f"检查: {html_file.name}")
        if fix_incomplete_questions(html_file):
            print(f"  ✅ 已修复不完整题目")
            updated_count += 1
        else:
            print(f"  ➡️  无需修复")
        print()
    
    print(f"\n完成！共修复了 {updated_count} 个HTML文件")

if __name__ == '__main__':
    main()