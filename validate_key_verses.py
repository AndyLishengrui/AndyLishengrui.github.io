#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
路加福音关键经文验证
验证路加福音中最重要经文的准确性
"""

import json

# 关键经文的标准和合本文本（用于对比验证）
KEY_VERSES = {
    (1, 35): '天使回答说："圣灵要临到你身上，至高者的能力要荫庇你，因此所要生的圣者必称为神的儿子。',
    (2, 11): '因今天在大卫的城里，为你们生了救主，就是主基督。',
    (4, 18): '主的灵在我身上，因为他用膏膏我，叫我传福音给贫穷的人；差遣我报告：被掳的得释放，瞎眼的得看见，叫那受压制的得自由，',
    (9, 23): '耶稣又对众人说："若有人要跟从我，就当舍己，天天背起他的十字架来跟从我。',
    (15, 7): '我告诉你们，一个罪人悔改，在天上也要这样为他欢喜，较比为九十九个不用悔改的义人欢喜更大。"',
    (19, 10): '人子来，为要寻找、拯救失丧的人。"',
    (22, 19): '又拿起饼来，祝谢了，就掰开，递给他们，说："这是我的身体，为你们舍的，你们也应当如此行，为的是记念我。"',
    (23, 34): '当下耶稣说："父啊！赦免他们；因为他们所做的，他们不晓得。"兵丁就拈阄分他的衣服。',
    (24, 6): '他不在这里，已经复活了。当记念他还在加利利的时候怎样告诉你们，'
}

def load_luke_data():
    """加载路加福音数据"""
    with open('data/luke.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['verses']

def find_verse(verses, chapter, verse_num):
    """查找指定经文"""
    for verse in verses:
        if verse.get('chapter') == chapter and verse.get('verse') == verse_num:
            return verse
    return None

def compare_with_standard(verses):
    """与标准和合本文本对比"""
    issues = []
    
    for (chapter, verse_num), standard_text in KEY_VERSES.items():
        verse_data = find_verse(verses, chapter, verse_num)
        
        if not verse_data:
            issues.append({
                'type': '经文缺失',
                'chapter': chapter,
                'verse': verse_num,
                'issue': f'找不到经文 {chapter}:{verse_num}'
            })
            continue
        
        current_text = verse_data.get('zh', '').strip()
        
        # 简单的文本对比（忽略标点符号差异）
        def normalize_text(text):
            return text.replace('"', '"').replace('"', '"').replace("'", "'").replace("'", "'").strip()
        
        current_normalized = normalize_text(current_text)
        standard_normalized = normalize_text(standard_text)
        
        # 检查主要内容是否匹配（允许一些标点差异）
        if not current_normalized.startswith(standard_normalized[:30]):  # 检查前30个字符
            issues.append({
                'type': '经文内容可能有误',
                'chapter': chapter,
                'verse': verse_num,
                'current': current_text,
                'standard': standard_text
            })
    
    return issues

def check_verse_completeness(verses):
    """检查经文完整性"""
    issues = []
    
    # 检查是否有明显不完整的经文
    for verse in verses:
        zh_text = verse.get('zh', '').strip()
        chapter = verse.get('chapter')
        verse_num = verse.get('verse')
        
        # 检查过短的经文（可能不完整）
        if len(zh_text) < 5 and chapter not in [3]:  # 第3章有很多短的家谱经文
            issues.append({
                'type': '经文过短，可能不完整',
                'chapter': chapter,
                'verse': verse_num,
                'text': zh_text
            })
        
        # 检查明显的截断
        if zh_text.endswith('...') or zh_text.endswith('…'):
            issues.append({
                'type': '经文可能被截断',
                'chapter': chapter,
                'verse': verse_num,
                'text': zh_text
            })
    
    return issues

def main():
    """主验证流程"""
    print("🔍 路加福音关键经文验证...")
    
    verses = load_luke_data()
    all_issues = []
    
    print("📖 验证关键经文准确性...")
    all_issues.extend(compare_with_standard(verses))
    
    print("🔍 检查经文完整性...")
    all_issues.extend(check_verse_completeness(verses))
    
    # 报告结果
    if all_issues:
        print(f"\n❌ 发现 {len(all_issues)} 个问题:")
        for issue in all_issues:
            print(f"  📍 {issue['type']} - {issue['chapter']}:{issue['verse']}")
            if 'current' in issue:
                print(f"     当前: {issue['current'][:80]}...")
                print(f"     标准: {issue['standard'][:80]}...")
            else:
                print(f"     {issue.get('text', issue.get('issue', ''))}...")
            print()
    else:
        print("✅ 关键经文验证通过")
    
    print(f"\n📊 验证完成，总共检查 {len(verses)} 节经文")

if __name__ == "__main__":
    main()