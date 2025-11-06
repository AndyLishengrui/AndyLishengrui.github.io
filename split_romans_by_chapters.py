#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据罗马书圣经章节将内容分割成16个文件
基于详细的文件分析,确定每个章节的准确边界
"""

import os

def split_romans_by_chapters():
    """将罗马书内容按照圣经章节(罗马书1-16章)分割成16个文件"""
    
    # 输入文件路径
    input_file = 'BooksofRoman/romans_content.txt'
    
    # 输出目录
    output_dir = 'BooksofRoman/chapters_by_scripture'
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 定义每个章节的行号范围 (根据详细文件分析确定)
    # 每个元组格式: (起始行, 结束行)
    chapter_boundaries = {
        1: (1, 742),          # 罗马书第1章: 文件开头到第742行
        2: (743, 994),        # 罗马书第2章: "5 外邦人的罪" 开始
        3: (995, 1267),       # 罗马书第3章: "7 犹太人的罪" 开始
        4: (1268, 1388),      # 罗马书第4章: 亚伯拉罕的信心主题
        5: (1389, 1608),      # 罗马书第5章: 称义带来的结果
        6: (1609, 1893),      # 罗马书第6章: 向罪死、向神活
        7: (1894, 2241),      # 罗马书第7章: 基督徒与律法
        8: (2242, 2935),      # 罗马书第8章: 圣灵中的生命(结束于2935行)
        9: (2936, 3124),      # 罗马书第9章: "14人的不信与神的恩典罗马书9-11章概述"
        10: (3125, 3159),     # 罗马书第10章: 以色列的不信(9-11章段落的一部分)
        11: (3160, 3221),     # 罗马书第11章: 以色列的未来(9-11章段落结束)
        12: (3222, 3245),     # 罗马书第12章: "11. 彼此接纳使上帝得荣耀"(15章内容)
        13: (3246, 3256),     # 罗马书第13章: "13. 保罗的旅行计划"(15章23-33节)
        14: (3257, 3268),     # 罗马书第14章: "14. 保罗的同工"(16章开始)
        15: (3269, 3281),     # 罗马书第15章: "15. 失传的手术刀"(16章17-20节)
        16: (3282, 3427)      # 罗马书第16章: 16章后半部分到文件结束
    }
    
    print(f"正在读取文件: {input_file}")
    
    # 读取整个文件
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
        
        total_lines = len(all_lines)
        print(f"文件总行数: {total_lines}")
        
        # 为每个章节创建文件
        for chapter_num in range(1, 17):
            start_line, end_line = chapter_boundaries[chapter_num]
            
            # 调整为0-based索引
            start_idx = start_line - 1
            end_idx = end_line
            
            # 提取该章节的内容
            chapter_content = all_lines[start_idx:end_idx]
            
            # 创建输出文件名
            output_file = os.path.join(output_dir, f'chapter_{chapter_num:02d}.txt')
            
            # 写入文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.writelines(chapter_content)
            
            print(f"第{chapter_num:2d}章: 行 {start_line:4d}-{end_line:4d} ({len(chapter_content):4d}行) -> {output_file}")
        
        print(f"\n✅ 成功! 已创建16个章节文件在目录: {output_dir}")
        
        # 验证所有行都被包含
        total_extracted = sum(boundaries[1] - boundaries[0] + 1 
                            for boundaries in chapter_boundaries.values())
        print(f"\n验证: 提取的总行数 = {total_extracted}, 原文件行数 = {total_lines}")
        
        if total_extracted == total_lines:
            print("✅ 验证通过: 所有行都已正确分配")
        else:
            print(f"⚠️  警告: 行数不匹配! 差异 = {abs(total_extracted - total_lines)}行")
            
    except FileNotFoundError:
        print(f"❌ 错误: 找不到文件 {input_file}")
        return False
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    print("="*60)
    print("罗马书章节分割工具")
    print("将内容按照罗马书圣经章节(1-16章)分割")
    print("="*60)
    print()
    
    success = split_romans_by_chapters()
    
    if success:
        print("\n" + "="*60)
        print("处理完成!")
        print("="*60)
    else:
        print("\n处理失败,请检查错误信息")
