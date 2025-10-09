import json
import re

def extract_romans_data():
    """从罗马书HTML文件提取经文数据"""
    
    with open('romans_study.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取romansData数组
    romans_pattern = r'const romansData = \[(.*?)\];'
    romans_match = re.search(romans_pattern, content, re.DOTALL)
    
    # 提取keyVerses数组
    key_verses_pattern = r'const keyVerses = \[(.*?)\];'
    key_verses_match = re.search(key_verses_pattern, content, re.DOTALL)
    
    if not romans_match or not key_verses_match:
        print("Could not find data arrays in HTML file")
        return None
    
    # 解析经文数据
    verses = []
    verse_pattern = r'\{ chapter: (\d+), verse: (\d+), zh: "(.*?)", en: "(.*?)"(?:, background: "(.*?)")? \}'
    
    for match in re.finditer(verse_pattern, romans_match.group(1)):
        chapter, verse, zh, en = match.groups()[:4]
        background = match.groups()[4] if match.groups()[4] else ""
        
        # 清理HTML标签
        if background:
            background = re.sub(r'<[^>]+>', '', background)
        
        verse_data = {
            'chapter': int(chapter),
            'verse': int(verse),
            'zh': zh,
            'en': en
        }
        
        # 只有当background不为空时才添加该字段
        if background:
            verse_data['background'] = background
        
        verses.append(verse_data)
    
    # 解析金句数据
    key_verses = []
    key_verse_pattern = r'\{ chapter: (\d+), verse: (\d+) \}'
    
    for match in re.finditer(key_verse_pattern, key_verses_match.group(1)):
        chapter, verse = match.groups()
        key_verses.append({
            'chapter': int(chapter),
            'verse': int(verse)
        })
    
    return {
        'verses': verses,
        'keyVerses': key_verses
    }

def extract_ephesians_data():
    """从以弗所书HTML文件提取经文数据"""
    
    with open('ephesians_study.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取ephesiansData数组
    ephesians_pattern = r'const ephesiansData = \[(.*?)\];'
    ephesians_match = re.search(ephesians_pattern, content, re.DOTALL)
    
    # 提取keyVerses数组
    key_verses_pattern = r'const keyVerses = \[(.*?)\];'
    key_verses_match = re.search(key_verses_pattern, content, re.DOTALL)
    
    if not ephesians_match or not key_verses_match:
        print("Could not find data arrays in HTML file")
        return None
    
        # 解析经文数据
        verses = []
        verse_pattern = r'\{ chapter: (\d+), verse: (\d+), zh: "(.*?)", en: "(.*?)"(?:, background: "(.*?)")? \}'
        
        for match in re.finditer(verse_pattern, ephesians_match.group(1)):
            chapter, verse, zh, en = match.groups()[:4]
            background = match.groups()[4] if match.groups()[4] else ""
            
            # 清理HTML标签
            if background:
                background = re.sub(r'<[^>]+>', '', background)
            
            verse_data = {
                'chapter': int(chapter),
                'verse': int(verse),
                'zh': zh,
                'en': en
            }
            
            # 只有当background不为空时才添加该字段
            if background:
                verse_data['background'] = background
            
            verses.append(verse_data)    # 解析金句数据
    key_verses = []
    key_verse_pattern = r'\{ chapter: (\d+), verse: (\d+) \}'
    
    for match in re.finditer(key_verse_pattern, key_verses_match.group(1)):
        chapter, verse = match.groups()
        key_verses.append({
            'chapter': int(chapter),
            'verse': int(verse)
        })
    
    return {
        'verses': verses,
        'keyVerses': key_verses
    }

if __name__ == "__main__":
    # 提取罗马书数据
    print("Extracting Romans data...")
    romans_data = extract_romans_data()
    if romans_data:
        romans_book_data = {
            "book": "romans",
            "name": "罗马书",
            "englishName": "Romans",
            "testament": "new",
            "category": "pauline_epistles", 
            "chapters": 16,
            "color": "#e74c3c",
            "description": "保罗向罗马教会阐述因信称义的伟大真理",
            "keyThemes": ["因信称义", "神的义", "罪与救恩", "基督徒生活", "神的主权"],
            **romans_data
        }
        
        with open('data/romans.json', 'w', encoding='utf-8') as f:
            json.dump(romans_book_data, f, ensure_ascii=False, indent=2)
        print(f"Romans data saved: {len(romans_data['verses'])} verses, {len(romans_data['keyVerses'])} key verses")
    
    # 提取以弗所书数据
    print("Extracting Ephesians data...")
    ephesians_data = extract_ephesians_data()
    if ephesians_data:
        ephesians_book_data = {
            "book": "ephesians",
            "name": "以弗所书", 
            "englishName": "Ephesians",
            "testament": "new",
            "category": "pauline_epistles",
            "chapters": 6,
            "color": "#3498db",
            "description": "保罗向以弗所教会论述神在基督里的丰盛恩典",
            "keyThemes": ["神的拣选", "教会合一", "属灵争战", "夫妻关系", "基督的爱"],
            **ephesians_data
        }
        
        with open('data/ephesians.json', 'w', encoding='utf-8') as f:
            json.dump(ephesians_book_data, f, ensure_ascii=False, indent=2)
        print(f"Ephesians data saved: {len(ephesians_data['verses'])} verses, {len(ephesians_data['keyVerses'])} key verses")
    
    print("Data extraction completed!")