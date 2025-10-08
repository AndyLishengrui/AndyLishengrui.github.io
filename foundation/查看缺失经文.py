#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查看所有缺失答案的经文引用，用于扩充经文数据库
"""

import json
import os
from pathlib import Path
from collections import Counter

def collect_missing_references():
    """收集所有缺失的经文引用"""
    answers_dir = Path(__file__).parent / 'data' / 'answers'
    json_files = list(answers_dir.glob('foundation_L*.json'))
    
    missing_refs = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for key, answer in data.get('answers', {}).items():
                if not answer.get('has_data', False):
                    ref = answer.get('reference', '').strip()
                    if ref:
                        missing_refs.append((ref, json_file.name))
        except Exception as e:
            print(f"读取失败 {json_file}: {e}")
    
    return missing_refs

def main():
    """主函数"""
    missing_refs = collect_missing_references()
    
    # 统计经文引用
    ref_counter = Counter([ref for ref, _ in missing_refs])
    
    print("缺失的经文引用统计:")
    print("=" * 80)
    print(f"{'经文引用':<25} {'出现次数':<8} {'文件示例':<30}")
    print("=" * 80)
    
    # 按出现频率排序
    for ref, count in ref_counter.most_common():
        files = [filename for r, filename in missing_refs if r == ref]
        example_file = files[0] if files else ""
        print(f"{ref:<25} {count:<8} {example_file:<30}")
    
    print("=" * 80)
    print(f"总计: {len(ref_counter)} 个不同的经文引用，{len(missing_refs)} 个缺失答案")
    
    print("\n按圣经书卷分组:")
    print("=" * 50)
    
    # 按书卷分组
    books = {}
    for ref, _ in missing_refs:
        # 提取书卷名
        book = ref.split()[0] if ref else "未知"
        if book not in books:
            books[book] = []
        books[book].append(ref)
    
    for book, refs in sorted(books.items()):
        unique_refs = list(set(refs))
        print(f"{book}: {len(unique_refs)} 个经文")
        for ref in sorted(unique_refs):
            print(f"  - {ref}")

if __name__ == '__main__':
    main()