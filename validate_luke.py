#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
路加福音经文验证脚本
检查常见的经文错误和不一致性
"""

import json
import re

def load_luke_data():
    """加载路加福音数据"""
    with open('data/luke.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['verses']

def check_quotation_marks(verses):
    """检查引号一致性"""
    issues = []
    for verse in verses:
        zh_text = verse.get('zh', '')
        
        # 检查不一致的引号
        single_quotes = zh_text.count("'")
        double_quotes = zh_text.count('"')
        chinese_quotes_start = zh_text.count('"')
        chinese_quotes_end = zh_text.count('"')
        
        if single_quotes > 0 and (double_quotes > 0 or chinese_quotes_start > 0):
            issues.append({
                'type': '引号不一致',
                'chapter': verse.get('chapter'),
                'verse': verse.get('verse'),
                'text': zh_text[:100] + '...' if len(zh_text) > 100 else zh_text
            })
    
    return issues

def check_punctuation_issues(verses):
    """检查标点符号问题"""
    issues = []
    for verse in verses:
        zh_text = verse.get('zh', '')
        
        # 检查句子末尾没有标点
        common_endings = ['。', '！', '？', '：', '，', '"', '"', "'", "。'", "！'", "？'"]
        if zh_text and not any(zh_text.strip().endswith(ending) for ending in common_endings):
            issues.append({
                'type': '缺少结尾标点',
                'chapter': verse.get('chapter'),
                'verse': verse.get('verse'),
                'text': zh_text
            })
    
    return issues

def check_common_errors(verses):
    """检查常见的经文错误"""
    issues = []
    
    # 已知的问题模式
    error_patterns = [
        # 检查是否还有马太福音的主祷文版本
        {
            'pattern': r'我们在天上的父',
            'description': '可能是马太福音版本的主祷文，路加福音应为"父啊"',
            'chapters': [11]
        }
    ]
    
    for verse in verses:
        zh_text = verse.get('zh', '')
        chapter = verse.get('chapter')
        verse_num = verse.get('verse')
        
        for error in error_patterns:
            if chapter in error.get('chapters', []):
                if re.search(error['pattern'], zh_text):
                    issues.append({
                        'type': error['description'],
                        'chapter': chapter,
                        'verse': verse_num,
                        'text': zh_text
                    })
    
    return issues

def validate_verse_numbering(verses):
    """验证经文编号连续性"""
    issues = []
    chapter_verses = {}
    
    # 组织按章节
    for verse in verses:
        chapter = verse.get('chapter')
        verse_num = verse.get('verse')
        
        if chapter not in chapter_verses:
            chapter_verses[chapter] = []
        chapter_verses[chapter].append(verse_num)
    
    # 检查每章的连续性
    for chapter, verse_nums in chapter_verses.items():
        verse_nums.sort()
        for i, verse_num in enumerate(verse_nums):
            expected = i + 1
            if verse_num != expected:
                issues.append({
                    'type': '经文编号不连续',
                    'chapter': chapter,
                    'verse': verse_num,
                    'expected': expected
                })
    
    return issues

def main():
    """主验证流程"""
    print("🔍 开始路加福音经文验证...")
    
    verses = load_luke_data()
    all_issues = []
    
    # 运行各种检查
    print("📝 检查引号一致性...")
    all_issues.extend(check_quotation_marks(verses))
    
    print("🔤 检查标点符号问题...")
    all_issues.extend(check_punctuation_issues(verses))
    
    print("⚠️  检查常见错误...")
    all_issues.extend(check_common_errors(verses))
    
    print("🔢 验证经文编号...")
    all_issues.extend(validate_verse_numbering(verses))
    
    # 报告结果
    if all_issues:
        print(f"\n❌ 发现 {len(all_issues)} 个问题:")
        for issue in all_issues[:20]:  # 只显示前20个问题
            print(f"  📍 {issue['type']} - {issue['chapter']}:{issue['verse']}")
            print(f"     {issue['text'][:80]}...")
            print()
        
        if len(all_issues) > 20:
            print(f"... 还有 {len(all_issues) - 20} 个问题未显示")
    else:
        print("✅ 未发现明显问题")
    
    print(f"\n📊 验证完成，总共检查 {len(verses)} 节经文")

if __name__ == "__main__":
    main()