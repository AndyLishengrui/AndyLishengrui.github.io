#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查哪些答案文件需要补充数据
"""

import json
import os
from pathlib import Path

def check_answer_completeness(json_file):
    """检查答案文件的完成度"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        answers = data.get('answers', {})
        total = len(answers)
        completed = sum(1 for answer in answers.values() if answer.get('has_data', False))
        
        return total, completed, total - completed
    except Exception as e:
        return 0, 0, 0

def main():
    """主函数"""
    answers_dir = Path(__file__).parent / 'data' / 'answers'
    
    # 获取所有答案JSON文件
    json_files = list(answers_dir.glob('foundation_L*.json'))
    json_files.sort()
    
    print("检查答案完成度...")
    print("=" * 60)
    print(f"{'文件名':<25} {'总题数':<8} {'已完成':<8} {'未完成':<8} {'完成率':<8}")
    print("=" * 60)
    
    total_questions = 0
    total_completed = 0
    total_missing = 0
    
    for json_file in json_files:
        total, completed, missing = check_answer_completeness(json_file)
        completion_rate = f"{completed/total*100:.1f}%" if total > 0 else "0%"
        
        print(f"{json_file.name:<25} {total:<8} {completed:<8} {missing:<8} {completion_rate:<8}")
        
        total_questions += total
        total_completed += completed
        total_missing += missing
    
    print("=" * 60)
    overall_rate = f"{total_completed/total_questions*100:.1f}%" if total_questions > 0 else "0%"
    print(f"{'总计':<25} {total_questions:<8} {total_completed:<8} {total_missing:<8} {overall_rate:<8}")
    print("\n需要补充答案的课程:")
    
    # 显示需要补充的课程
    for json_file in json_files:
        total, completed, missing = check_answer_completeness(json_file)
        if missing > 0:
            lesson_name = json_file.name.replace('foundation_', '').replace('.json', '')
            print(f"  - {lesson_name}: {missing}个答案缺失")

if __name__ == '__main__':
    main()