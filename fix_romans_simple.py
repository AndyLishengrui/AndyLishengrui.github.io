#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
罗马书内容简单修复 - 只修复经文标注,不改变段落结构
"""

import os
import re

def fix_scripture_marks(content):
    """
    修复经文标注:
    1. 保留 {{scripture}}...{{/scripture}} (整段经文)
    2. 移除 {{inline-scripture}}...{{/inline-scripture}}
    3. 只标注经文引用: (书名 章:节)
    """
    # 66卷圣经书名列表
    bible_books = [
        '创世记', '出埃及记', '利未记', '民数记', '申命记',
        '约书亚记', '士师记', '路得记', '撒母耳记上', '撒母耳记下',
        '列王纪上', '列王纪下', '历代志上', '历代志下', '以斯拉记',
        '尼希米记', '以斯帖记', '约伯记', '诗篇', '箴言',
        '传道书', '雅歌', '以赛亚书', '耶利米书', '耶利米哀歌',
        '以西结书', '但以理书', '何西阿书', '约珥书', '阿摩司书',
        '俄巴底亚书', '约拿书', '弥迦书', '那鸿书', '哈巴谷书',
        '西番雅书', '哈该书', '撒迦利亚书', '玛拉基书',
        '马太福音', '马可福音', '路加福音', '约翰福音', '使徒行传',
        '罗马书', '哥林多前书', '哥林多后书', '加拉太书', '以弗所书',
        '腓立比书', '歌罗西书', '帖撒罗尼迦前书', '帖撒罗尼迦后书',
        '提摩太前书', '提摩太后书', '提多书', '腓利门书', '希伯来书',
        '雅各书', '彼得前书', '彼得后书', '约翰一书', '约翰二书',
        '约翰三书', '犹大书', '启示录'
    ]
    
    # 1. 移除 {{inline-scripture}} 标签
    content = re.sub(r'\{\{inline-scripture\}\}', '', content)
    content = re.sub(r'\{\{/inline-scripture\}\}', '', content)
    
    # 2. 标注经文引用 (书名 章:节)
    books_pattern = '|'.join(bible_books)
    # 匹配模式: (书名 章:节) 或 (书名 章:节-节)
    reference_pattern = rf'\(({books_pattern})\s+(\d+):(\d+)(?:-(\d+))?\)'
    
    def mark_reference(match):
        full_match = match.group(0)
        # 检查是否已经被标注
        if '{{scripture-ref}}' in content[max(0, match.start()-20):match.start()]:
            return full_match
        return f'{{{{scripture-ref}}}}{full_match}{{{{/scripture-ref}}}}'
    
    content = re.sub(reference_pattern, mark_reference, content)
    
    # 修复可能重复标注的问题
    content = re.sub(r'\{\{scripture-ref\}\}\s*\{\{scripture-ref\}\}', '{{scripture-ref}}', content)
    content = re.sub(r'\{\{/scripture-ref\}\}\s*\{\{/scripture-ref\}\}', '{{/scripture-ref}}', content)
    
    return content


def process_chapter(input_file, output_file):
    """处理单个章节文件"""
    print(f"处理: {os.path.basename(input_file)}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 只修复经文标注,保持原有段落结构
    content = fix_scripture_marks(content)
    
    # 保存
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ 已保存: {os.path.basename(output_file)}")


def main():
    """主函数"""
    print("=" * 60)
    print("罗马书内容简单修复 - 只修复经文标注")
    print("=" * 60)
    print()
    
    input_dir = "BooksofRoman/chapters_correct"
    output_dir = "BooksofRoman/chapters_final"
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 处理16个章节
    for i in range(1, 17):
        chapter_num = f"{i:02d}"
        input_file = f"{input_dir}/chapter_{chapter_num}.txt"
        output_file = f"{output_dir}/chapter_{chapter_num}.txt"
        
        if os.path.exists(input_file):
            process_chapter(input_file, output_file)
        else:
            print(f"⚠ 警告: 找不到文件 {input_file}")
    
    print()
    print("=" * 60)
    print("✓ 修复完成!")
    print(f"✓ 输出目录: {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
