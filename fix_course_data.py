#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复建立根基课程数据 - 手动校正版本
基于对txt文件的分析，手动标记每一课的起始位置
"""

import json

def fix_foundation_course():
    """手动修复课程数据"""
    
    # 读取可读txt文件
    with open('建立根基_readable.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 手动标记12课的准确位置（通过查看文件确定）
    # 格式: (课程ID, 标题, 大约起始行号)
    lesson_markers = [
        (1, "罪与得救", 117),           # "罪与得救" 出现在此
        (2, "主权与顺服", 446),         # "主权与顺服 13" 
        (3, "悔改与洗礼", 647),         # "悔改与受洗" (注意是"受洗"不是"洗礼")
        (4, "圣灵与属灵恩赐", 895),     # 需要查找
        (5, "渴慕与神的话语", 1073),    # 已知
        (6, "门徒与带领", 1191),        # 需要查找
        (7, "属灵家庭与教会生活", 1409), # 需要查找  
        (8, "祷告与敬拜", 1612),        # 需要查找
        (9, "信心与盼望", 1810),        # 需要查找
        (10, "富足与慷慨", 2008),       # 需要查找
        (11, "传福音与世界宣教", 2198), # 需要查找
        (12, "复活与审判", 2482),       # 需要查找
    ]
    
    print("开始修复课程数据...")
    print("首先让我找到每课的准确起始行...")
    
    # 搜索每一课的标题
    for i, (lid, title, approx_line) in enumerate(lesson_markers):
        # 在大约位置附近搜索
        found = False
        for line_num in range(max(0, approx_line - 50), min(len(lines), approx_line + 50)):
            line = lines[line_num].strip()
            # 匹配课程标题（可能有页码粘在后面）
            if title in line or (title == "悔改与洗礼" and "悔改与受洗" in line):
                # 确认这不是目录行
                if "·" not in line and line_num > 100:
                    print(f"第{lid}课 '{title}' 找到于第{line_num + 1}行: {line[:60]}")
                    lesson_markers[i] = (lid, title, line_num)
                    found = True
                    break
        
        if not found:
            print(f"⚠️  第{lid}课 '{title}' 未找到，使用估计位置 {approx_line}")
    
    print("\n建议：请手动检查原始txt文件，确认每课起始位置")
    print("然后更新 extract_foundation_v4.py 以使用正确的课程标记")

if __name__ == "__main__":
    fix_foundation_course()
