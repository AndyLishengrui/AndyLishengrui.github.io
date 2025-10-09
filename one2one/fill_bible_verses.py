#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from pathlib import Path

def read_source():
    f = Path(__file__).parent / "一对一.txt"
    with open(f, 'r', encoding='utf-8') as fp:
        return fp.read().split('\n')

def extract_verses():
    lines = read_source()
    verses = {}
    
    books = ['以赛亚书', '马太福音', '马可福音', '路加福音', '约翰福音', '使徒行传',
             '罗马书', '哥林多前书', '哥林多后书', '加拉太书', '以弗所书', '腓立比书',
             '歌罗西书', '帖撒罗尼迦前书', '帖撒罗尼迦后书', '提摩太前书', '提摩太后书',
             '提多书', '腓利门书', '希伯来书', '雅各书', '彼得前书', '彼得后书',
             '约翰一书', '约翰二书', '约翰三书', '犹大书', '启示录', '歌罗西书',
             '约书亚记', '撒母耳记上', '撒母耳记下', '诗篇', '箴言', '耶利米书']
    
    pattern = r'^(%s)\s+(\d+:\d+(?:[,-]\d+)*)\s*[(（]([^)）]+)[)）]?\s*$' % '|'.join(re.escape(b) for b in books)
    ref_re = re.compile(pattern)
    
    for i, line in enumerate(lines):
        line = line.strip()
        m = ref_re.match(line)
        if m:
            book, chapter, version = m.group(1), m.group(2), m.group(3)
            ref_key = f"{book} {chapter}"
            
            text_lines = []
            j = i - 1
            while j >= 0 and len(text_lines) < 10:
                prev = lines[j].strip()
                if not prev or any(prev.startswith(x) for x in ['得救', '悔改', '洗礼', '灵修', '教会', '带门徒']):
                    break
                if prev and not ref_re.match(prev):
                    text_lines.insert(0, prev)
                j -= 1
            
            if text_lines:
                if ref_key not in verses:
                    verses[ref_key] = {}
                verses[ref_key][version] = ' '.join(text_lines)
    
    return verses

def fill_json():
    print("提取经文...")
    vdb = extract_verses()
    print(f"提取到 {len(vdb)} 个经文")
    
    data_dir = Path(__file__).parent / "data" / "answers"
    updated = 0
    
    for jf in sorted(data_dir.glob("one2one_C*.json")):
        with open(jf, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        changed = False
        for key, ans in data['answers'].items():
            ref = ans['reference']
            if ref in vdb:
                versions = list(vdb[ref].keys())
                main_v = None
                for v in ['和合本', '和修版', '新译本', '标准译本', '当代译本']:
                    if v in versions:
                        main_v = v
                        break
                if not main_v:
                    main_v = versions[0]
                
                ans['text'] = vdb[ref][main_v]
                ans['version'] = main_v
                ans['has_data'] = True
                
                if len(versions) > 1:
                    for alt in versions:
                        if alt != main_v:
                            ans['text_alt'] = vdb[ref][alt]
                            ans['version_alt'] = alt
                            break
                changed = True
        
        if changed:
            with open(jf, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✓ {jf.name}")
            updated += 1
    
    print(f"\n完成！更新了 {updated} 个文件")

if __name__ == '__main__':
    fill_json()
