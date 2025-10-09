#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于PDF的完整准确解析 - 54节完整版
"""

import json
import re

def parse_complete_course():
    """基于PDF完整解析54节课程"""
    
    # 读取PDF提取的文本
    with open('建立根基_from_pdf.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 完整的54节结构（基于PDF grep结果）
    # 格式: (课程ID, 课程标题, [(节ID, 节标题, 起始行), ...])
    complete_structure = [
        (1, "罪与得救", [
            (1, "最初的故事", 160),
            (2, "罪的后果", 214),
            (3, "神对罪的解决方案：耶稣的死与复活", 264),
            (4, "接受神的礼物：一颗新心", 358),
            (5, "本乎恩也因着信", 390),
        ]),
        (2, "主权与顺服", [
            (1, "耶稣是主", 456),
            (2, "窄门", 489),
            (3, "主权与人际关系", 564),
            (4, "你能通过考验吗？", 618),
        ]),
        (3, "悔改与洗礼", [
            (1, "我们应当怎样行？", 679),
            (2, "悔改：转离罪", 727),
            (3, "悔改：转向神", 795),
            (4, "洗礼：水洗礼", 831),
        ]),
        (4, "圣灵与属灵恩赐", [
            (1, "认识圣灵", 942),
            (2, "圣灵的果子", 969),
            (3, "属灵恩赐", 1021),
            (4, "圣灵的洗", 1075),
        ]),
        (5, "渴慕与神的话语", [
            (1, "神的话语的权柄和能力", 1123),
            (2, "神的话语的益处", 1179),
            (3, "属灵的渴慕", 1215),
            (4, "顺服神的话语", 1252),
        ]),
        (6, "门徒与带领", [
            (1, "大使命：带门徒", 1307),
            (2, "代价：绝对降服", 1369),
            (3, "作门徒与十字架", 1422),
            (4, "基督徒的品格", 1464),
            (5, "作门徒与带门徒", 1519),
        ]),
        (7, "属灵家庭与教会生活", [
            (1, "得胜的教会", 1617),
            (2, "基督的身体", 1655),
            (3, "教会的带领", 1710),
            (4, "教会纪律", 1765),
            (5, "圣餐", 1818),
        ]),
        (8, "祷告与敬拜", [
            (1, "个人的祷告", 1885),
            (2, "祷告的大能", 1931),
            (3, "一起祷告", 1980),
            (4, "圣经中的祷告", 2022),
            (5, "敬拜", 2069),
        ]),
        (9, "信心与盼望", [
            (1, "什么是信心", 2119),
            (2, "得救的信心", 2162),
            (3, "信心与顺服", 2209),
            (4, "移山的信心", 2263),
            (5, "信心与盼望", 2312),
        ]),
        (10, "富足与慷慨", [
            (1, "财富的危险", 2364),
            (2, "圣经中关于富足的法则", 2422),
            (3, "神居首位", 2472),
            (4, "牺牲的慷慨", 2506),
        ]),
        (11, "传福音与世界宣教", [
            (1, "每个门徒都是传道人", 2559),
            (2, "刚强壮胆", 2618),
            (3, "属灵争战与传福音", 2649),
            (4, "神迹奇事", 2680),
            (5, "直到世界的末了", 2732),
        ]),
        (12, "复活与审判", [
            (1, "死亡与复活", 2795),
            (2, "神的公义与人的邪恶", 2882),
            (3, "对罪人的审判", 2942),
            (4, "对圣徒的审判", 3001),
        ]),
    ]
    
    course_data = {
        "title": "建立根基",
        "description": "12课系统性门徒培训课程",
        "lessons": []
    }
    
    print("开始解析完整课程...")
    print("="*70)
    
    # 逐课逐节解析
    for lesson_id, lesson_title, sections in complete_structure:
        print(f"\n第{lesson_id}课: {lesson_title} ({len(sections)}节)")
        
        lesson_data = {
            "id": lesson_id,
            "title": lesson_title,
            "sections": []
        }
        
        for i, (section_id, section_title, start_line) in enumerate(sections):
            # 确定结束行
            if i < len(sections) - 1:
                end_line = sections[i + 1][2]
            elif lesson_id < len(complete_structure):
                # 下一课的第一节
                end_line = complete_structure[lesson_id][2][0][2] if lesson_id < len(complete_structure) else len(lines)
            else:
                end_line = len(lines)
            
            section_data = {
                "id": section_id,
                "title": section_title,
                "content": [],
                "questions": [],
                "application": ""
            }
            
            current_question = None
            
            # 解析这一节的内容
            for line_num in range(start_line, end_line):
                if line_num >= len(lines):
                    break
                    
                line = lines[line_num].strip()
                
                if not line or line.startswith('==='):
                    continue
                
                # 跳过节标题行
                if f"第{['一','二','三','四','五','六','七','八'][section_id-1]}节" in line:
                    continue
                
                # 检测问题
                question_match = re.match(r'^(\d+)\.\s+(.+)', line)
                if question_match:
                    question_num = int(question_match.group(1))
                    question_text = question_match.group(2).strip()
                    
                    # 保存上一个问题
                    if current_question:
                        section_data["questions"].append(current_question)
                    
                    current_question = {
                        "id": question_num,
                        "question": question_text,
                        "references": [],
                        "answer": "",
                        "blanks": 0
                    }
                    continue
                
                # 检测经文引用
                reference_match = re.match(r'^([a-zA-Z\u4e00-\u9fa5]+)\s*(\d+:\d+[\-,\d]*)\s*_*\s*$', line)
                if reference_match and current_question:
                    book = reference_match.group(1)
                    verses = reference_match.group(2)
                    current_question["references"].append(f"{book} {verses}")
                    continue
                
                # 检测填空线
                if line.count('_') > 10 and current_question:
                    current_question["blanks"] += 1
                    continue
                
                # 检测个人应用
                if '个人应用' in line and section_data:
                    section_data["application"] = line
                    continue
            
            # 保存最后一个问题
            if current_question:
                section_data["questions"].append(current_question)
            
            lesson_data["sections"].append(section_data)
            
            print(f"  ✓ 第{section_id}节: {section_title[:40]} ({len(section_data['questions'])}题)")
        
        course_data["lessons"].append(lesson_data)
        
        total_q = sum(len(s["questions"]) for s in lesson_data["sections"])
        print(f"  小计: {len(lesson_data['sections'])}节, {total_q}个问题")
    
    # 总统计
    print("\n" + "="*70)
    print("课程结构总览：")
    print("="*70)
    for lesson in course_data["lessons"]:
        total_q = sum(len(s["questions"]) for s in lesson["sections"])
        print(f"第{lesson['id']:2d}课: {lesson['title']:20s} - {len(lesson['sections'])}节, {total_q:3d}个问题")
    
    total_sections = sum(len(l["sections"]) for l in course_data["lessons"])
    total_questions = sum(
        sum(len(s["questions"]) for s in l["sections"])
        for l in course_data["lessons"]
    )
    print("="*70)
    print(f"总计：{len(course_data['lessons'])}课, {total_sections}节, {total_questions}个问题")
    
    # 保存
    output_file = "data/foundation_course.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(course_data, f, ensure_ascii=False, indent=2)
    print(f"\n✓ 完整数据已保存到: {output_file}")
    
    return course_data


if __name__ == "__main__":
    parse_complete_course()
