#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
建立根基课程数据提取脚本
从Word导出的HTML中提取课程结构和内容
"""

from bs4 import BeautifulSoup
import json
import re

# 12课的准确标题
LESSON_TITLES = [
    "罪与得救",
    "主权与顺服",
    "悔改与洗礼",
    "圣灵与属灵恩赐",
    "渴慕与神的话语",
    "门徒与带领",
    "属灵家庭与教会生活",
    "祷告与敬拜",
    "信心与盼望",
    "富足与慷慨",
    "传福音与世界宣教",
    "复活与审判"
]

def extract_foundation_course():
    """提取建立根基课程的结构和内容"""
    
    print("📚 开始解析建立根基课程...")
    
    # 读取HTML文件
    with open('建立根基.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 获取所有文本段落
    paragraphs = soup.find_all('p')
    
    # 课程结构
    courses = []
    lesson_starts = {}  # 记录每课的开始位置
    
    print(f"找到 {len(paragraphs)} 个段落")
    print("\n📖 第一步：定位12课位置...")
    
    # 先找到每课的大标题位置
    for i, p in enumerate(paragraphs):
        text = p.get_text().strip()
        for lesson_num, title in enumerate(LESSON_TITLES, 1):
            # 查找大标题（font-size: 24.0pt 或更大的，且文本较短）
            if title in text:
                # 检查是否包含大字体样式
                html_str = str(p)
                if ('font-size:24.0pt' in html_str or 
                    'font-size:19.5pt' in html_str):
                    # 确保不是页眉页脚（通常是font-size:7.0pt或9.0pt）
                    if lesson_num not in lesson_starts:
                        lesson_starts[lesson_num] = i
                        print(f"  ✓ 第{lesson_num}课《{title}》- 位于段落 {i}")
                    break
    
    print(f"\n📄 第二步：提取每课的内容...")
    
    # 为每课提取内容
    for lesson_num in range(1, 13):
        if lesson_num not in lesson_starts:
            continue
        
        lesson_title = LESSON_TITLES[lesson_num - 1]
        start_idx = lesson_starts[lesson_num]
        end_idx = lesson_starts.get(lesson_num + 1, len(paragraphs))
        
        print(f"\n  第{lesson_num}课《{lesson_title}》")
        
        # 提取这一课的所有段落
        lesson_paragraphs = paragraphs[start_idx:end_idx]
        
        # 提取节和问题
        sections = extract_sections(lesson_paragraphs, lesson_title)
        
        courses.append({
            'lesson': lesson_num,
            'title': lesson_title,
            'sections': sections
        })
        
        print(f"    ✓ 找到 {len(sections)} 个节")
    
    print(f"\n✅ 解析完成！共找到 {len(courses)} 课")
    
    # 保存为JSON
    output_file = 'data/foundation_course.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({'courses': courses}, f, ensure_ascii=False, indent=2)
    
    print(f"💾 数据已保存到 {output_file}")
    
    return courses

def extract_sections(paragraphs, lesson_title):
    """从段落中提取节的内容"""
    sections = []
    current_section = None
    current_content = []
    current_question_num = 0
    
    section_pattern = re.compile(r'第([一二三四五])节')
    
    for p in paragraphs:
        text = p.get_text().strip()
        
        if not text or len(text) < 2:
            continue
        
        # 检测节标题
        section_match = section_pattern.search(text)
        if section_match:
            # 保存上一节
            if current_section:
                current_section['content'] = '\n'.join(current_content)
                sections.append(current_section)
            
            # 开始新节
            section_num = convert_chinese_number(section_match.group(1))
            current_section = {
                'section': section_num,
                'title': text.replace(lesson_title, '').strip(),
                'questions': []
            }
            current_content = []
            current_question_num = 0
            continue
        
        if current_section:
            # 检测问题（以数字开头）
            question_match = re.match(r'^(\d+)\.\s*(.+)', text)
            if question_match:
                current_question_num = int(question_match.group(1))
                question_text = question_match.group(2)
                
                # 下一行可能是经文引用
                current_question = {
                    'num': current_question_num,
                    'question': question_text,
                    'scripture_ref': None,
                    'answer_lines': 0,
                    'is_personal': '个人应用' in question_text or '应用题' in question_text
                }
                current_section['questions'].append(current_question)
            
            # 检测经文引用（短文本，包含数字和冒号）
            elif current_question_num > 0 and re.match(r'^[\u4e00-\u9fa5]{1,5}\s*\d+:\d+', text):
                if current_section['questions']:
                    current_section['questions'][-1]['scripture_ref'] = text
            
            # 计算答案行数（下划线）
            elif '_' * 20 in text:
                if current_section['questions']:
                    current_section['questions'][-1]['answer_lines'] += 1
            
            # 普通内容
            else:
                current_content.append(text)
    
    # 保存最后一节
    if current_section:
        current_section['content'] = '\n'.join(current_content)
        sections.append(current_section)
    
    return sections

def convert_chinese_number(chinese_num):
    """转换中文数字为阿拉伯数字"""
    chinese_to_arabic = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        '十一': 11, '十二': 12
    }
    
    if isinstance(chinese_num, str) and chinese_num.isdigit():
        return int(chinese_num)
    
    return chinese_to_arabic.get(chinese_num, 0)

def generate_course_summary(courses):
    """生成课程摘要"""
    print("\n" + "="*60)
    print("📚 建立根基课程结构总结")
    print("="*60)
    
    for course in courses:
        print(f"\n第{course['lesson']}课: {course['title']}")
        for section in course['sections']:
            questions = section.get('questions', [])
            personal_q = len([q for q in questions if q.get('is_personal', False)])
            scripture_q = len([q for q in questions if not q.get('is_personal', False)])
            print(f"  第{section['section']}节: {scripture_q} 经文题 + {personal_q} 应用题")
    
    total_sections = sum(len(c['sections']) for c in courses)
    total_questions = sum(
        sum(len(s['questions']) for s in c['sections'])
        for c in courses
    )
    
    print(f"\n📊 总计:")
    print(f"  课程数: {len(courses)}")
    print(f"  节数: {total_sections}")
    print(f"  问题数: {total_questions}")

if __name__ == "__main__":
    courses = extract_foundation_course()
    generate_course_summary(courses)