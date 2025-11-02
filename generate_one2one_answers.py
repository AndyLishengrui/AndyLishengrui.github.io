#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 one2one 每课的答案占位 JSON
扫描 done2one/ 下的 HTML 页面，为每个页面在
done2one/data/answers/{section}.json 生成占位文件，避免页面 fetch 404。

用法: python3 generate_one2one_answers.py
"""
import os
import re
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
DONE_DIR = os.path.join(ROOT, 'done2one')
ANS_DIR = os.path.join(DONE_DIR, 'data', 'answers')

os.makedirs(ANS_DIR, exist_ok=True)

html_files = [f for f in os.listdir(DONE_DIR) if f.endswith('.html')]

ref_pattern = re.compile(r'([\u4e00-\u9fff]{1,10}\s*\d+[:：]\d+(?:-\d+)?)')

created = []
for fname in html_files:
    section = os.path.splitext(fname)[0]
    path = os.path.join(DONE_DIR, fname)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"跳过 {fname}：读取失败：{e}")
        continue

    # 尝试抽取可能的经文引用（简单匹配：书名 + 空格 + 章:节）
    refs = re.findall(ref_pattern, text)
    # 去重并保持顺序
    seen = set()
    refs_unique = []
    for r in refs:
        if r not in seen:
            seen.add(r)
            refs_unique.append(r)

    answer_obj = {
        'section': section,
        'has_data': False,
        'refs': refs_unique,
        'answers': {}
    }

    out_file = os.path.join(ANS_DIR, f"{section}.json")
    try:
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(answer_obj, f, ensure_ascii=False, indent=2)
        created.append(out_file)
        print(f"✓ 生成: {out_file} (refs: {len(refs_unique)})")
    except Exception as e:
        print(f"✗ 写入失败: {out_file} -> {e}")

print('\n完成。总共生成/更新 %d 个答案占位文件。' % len(created))
