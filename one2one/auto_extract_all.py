#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一对一课程自动提取和生成脚本
功能：
1. 自动从一对一.txt中提取所有70个小节的内容
2. 提取每节的标题、正文、经文引用
3. 生成标准化的JSON答案文件
4. 生成完整的HTML页面
"""

import json
import os
import re
from pathlib import Path

# 课程结构定义
COURSE_STRUCTURE = {
    1: {"title": "新起点 得救", "sections": 14, "start_page": "得救"},
    2: {"title": "新主人 主权", "sections": 8, "start_page": "悔改"},  # 注意：文件中主权部分标记为"悔改"
    3: {"title": "新方向 悔改", "sections": 9, "start_page": "悔改"},
    4: {"title": "新生命 洗礼", "sections": 10, "start_page": "洗礼"},
    5: {"title": "新操练 灵修", "sections": 11, "start_page": "灵修"},
    6: {"title": "新关系 教会", "sections": 8, "start_page": "教会"},
    7: {"title": "新使命 带门徒", "sections": 9, "start_page": "带门徒"}
}

def read_source_file():
    """读取一对一.txt文件"""
    file_path = Path(__file__).parent / "一对一.txt"
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def extract_bible_reference(text):
    """
    提取经文引用
    支持格式：
    - 马太福音 5:21,22
    - 罗马书 3:23
    - 以弗所书 2:8,9
    - 希伯来书 9:26-28
    """
    # 圣经书卷列表
    bible_books = [
        '创世记', '出埃及记', '利未记', '民数记', '申命记', '约书亚记', '士师记', '路得记',
        '撒母耳记上', '撒母耳记下', '列王纪上', '列王纪下', '历代志上', '历代志下',
        '以斯拉记', '尼希米记', '以斯帖记', '约伯记', '诗篇', '箴言', '传道书', '雅歌',
        '以赛亚书', '耶利米书', '耶利米哀歌', '以西结书', '但以理书',
        '何西阿书', '约珥书', '阿摩司书', '俄巴底亚书', '约拿书', '弥迦书', '那鸿书',
        '哈巴谷书', '西番雅书', '哈该书', '撒迦利亚书', '玛拉基书',
        '马太福音', '马可福音', '路加福音', '约翰福音', '使徒行传',
        '罗马书', '哥林多前书', '哥林多后书', '加拉太书', '以弗所书', '腓立比书',
        '歌罗西书', '帖撒罗尼迦前书', '帖撒罗尼迦后书', '提摩太前书', '提摩太后书',
        '提多书', '腓利门书', '希伯来书', '雅各书', '彼得前书', '彼得后书',
        '约翰一书', '约翰二书', '约翰三书', '犹大书', '启示录'
    ]
    
    # 构建正则表达式
    books_pattern = '|'.join(bible_books)
    pattern = rf'({books_pattern})\s+(\d+:\d+(?:[,-]\d+)*)'
    
    matches = re.findall(pattern, text)
    if matches:
        return [(book, chapter) for book, chapter in matches]
    return []

def parse_content():
    """解析整个文件内容"""
    lines = read_source_file()
    
    sections = []
    current_section = None
    current_content = []
    section_counter = 0
    
    # 标记模式：得救 1, 得救 2, 悔改 15, 等等
    section_pattern = re.compile(r'^(得救|悔改|洗礼|灵修|教会|带门徒)\s+(\d+)\s*$')
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # 检测小节标记
        match = section_pattern.match(line)
        if match:
            # 保存前一个小节
            if current_section is not None:
                current_section['content'] = '\n'.join(current_content)
                sections.append(current_section)
            
            # 开始新小节
            section_counter += 1
            marker = match.group(1)
            number = int(match.group(2))
            
            current_section = {
                'section_num': section_counter,
                'marker': marker,
                'marker_num': number,
                'title': '',
                'content': '',
                'verses': []
            }
            current_content = []
            
        elif current_section is not None:
            # 收集内容
            current_content.append(line)
            
            # 提取经文引用
            refs = extract_bible_reference(line)
            if refs:
                for book, chapter in refs:
                    ref_str = f"{book} {chapter}"
                    if ref_str not in [v['ref'] for v in current_section['verses']]:
                        current_section['verses'].append({
                            'ref': ref_str,
                            'text': '',  # 需要手动填充或从数据库获取
                            'version': '和合本'
                        })
    
    # 保存最后一个小节
    if current_section is not None:
        current_section['content'] = '\n'.join(current_content)
        sections.append(current_section)
    
    return sections

def infer_section_title(content, marker):
    """从内容推断小节标题"""
    # 常见的标题关键词
    title_keywords = {
        '得救': ['问题', '解决方法', '结果', '回应', '个人应用', '祷告', '新的生命'],
        '悔改': ['尊主权', '顺服', '内心', '行事为人'],
        '洗礼': ['悔改', '认罪', '洗礼', '见证'],
        '灵修': ['祷告', '读经', '灵修', '默想'],
        '教会': ['团契', '敬拜', '服事', '奉献'],
        '带门徒': ['见证', '传福音', '门徒']
    }
    
    lines = content.split('\n')
    for line in lines[:10]:  # 检查前10行
        line = line.strip()
        if line and len(line) < 30 and not line.startswith('('):
            # 检查是否包含关键词
            for keyword in title_keywords.get(marker, []):
                if keyword in line:
                    return line
            # 如果是独立的短行，可能是标题
            if len(line) < 15 and line and not any(c in line for c in '，。！？'):
                return line
    
    return "待定"

def assign_courses(sections):
    """将小节分配到对应的课程"""
    result = []
    section_counter = 1
    
    for course_num in range(1, 8):
        course_info = COURSE_STRUCTURE[course_num]
        num_sections = course_info['sections']
        
        for i in range(num_sections):
            if section_counter - 1 < len(sections):
                section = sections[section_counter - 1].copy()
                section['course_num'] = course_num
                section['course_title'] = course_info['title']
                section['section_num'] = section_counter
                
                # 推断标题
                if not section['title']:
                    section['title'] = infer_section_title(section['content'], section['marker'])
                
                result.append(section)
                section_counter += 1
    
    return result

def generate_json_answer(section):
    """生成JSON答案文件"""
    answers = {}
    
    for i, verse in enumerate(section['verses'], 1):
        key = f"q{i}_{verse['ref'].replace(' ', '')}"
        answers[key] = {
            "reference": verse['ref'],
            "text": verse.get('text', '【待补充：请从圣经中复制和合本译文】'),
            "version": verse.get('version', '和合本'),
            "text_alt": verse.get('text_alt', ''),
            "version_alt": verse.get('version_alt', ''),
            "has_data": bool(verse.get('text'))
        }
    
    json_data = {
        "course_num": section['course_num'],
        "course_title": section['course_title'],
        "section_num": section['section_num'],
        "section_title": section['title'],
        "answers": answers
    }
    
    return json_data

def generate_html_page(section, prev_link, next_link):
    """生成HTML页面"""
    course_num = section['course_num']
    section_num = section['section_num']
    section_title = section['title']
    
    # 简化内容（去除经文引用行）
    content_lines = section['content'].split('\n')
    clean_lines = []
    for line in content_lines:
        line = line.strip()
        if line and not extract_bible_reference(line):
            clean_lines.append(line)
    
    content_text = ' '.join(clean_lines[:5])  # 取前5行作为介绍
    if len(content_text) > 500:
        content_text = content_text[:500] + '...'
    
    # 生成经文填空HTML
    verse_blanks_html = ""
    for i, verse in enumerate(section['verses'], 1):
        verse_blanks_html += f"""
            <!-- 经文填空 {i} -->
            <div class="blank-section">
                <div class="blank-header">
                    <span class="blank-reference">📖 {verse['ref']}</span>
                    <div class="hint-buttons">
                        <button class="btn-hint btn-hint-partial" onclick="showPartialHint({i}, '{verse['ref']}')">💡 渐进提示</button>
                        <button class="btn-hint btn-hint-full" onclick="showFullHint({i}, '{verse['ref']}')">📝 查看答案</button>
                    </div>
                </div>
                <textarea 
                    class="answer-input" 
                    data-question="{i}" 
                    data-reference="{verse['ref']}"
                    data-has-answer="true"
                    placeholder="请根据经文引用，写出完整的经文内容..."></textarea>
                <div class="answer-feedback"></div>
                <div class="standard-answer" data-ref="{verse['ref']}">
                    <strong>📖 标准答案（和合本）：</strong>
                    <p>【待补充】</p>
                </div>
            </div>
"""
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>第{course_num}课 第{section_num}节 - {section_title} | 一对一门徒训练</title>
    <link rel="stylesheet" href="css/one2one_style.css">
</head>
<body>
    <div class="container">
        <header>
            <div class="breadcrumb">
                <a href="index.html">一对一首页</a> &gt; <a href="index.html">第{course_num}课：{section['course_title']}</a> &gt; 第{section_num}节
            </div>
            <h1>第{course_num}课：{section['course_title']}</h1>
            <div class="section-title-box">
                <span class="section-label">第 {section_num} 节</span>
                <span class="section-name">{section_title}</span>
            </div>
        </header>

        <div class="content">
            <div class="question-block">
                <p class="content-paragraph">
                    {content_text}
                </p>
            </div>

            {verse_blanks_html}
        </div>

        <!-- 操作栏 -->
        <div class="action-bar">
            <div class="score-display">
                完成进度: <span class="score-number" id="progressDisplay">0%</span>
            </div>
            <div>
                <button class="btn-check" onclick="checkAnswers()">✓ 检查答案</button>
                <button class="btn-submit" onclick="submitAnswers()">📊 提交成绩</button>
                <button class="btn-clear" onclick="clearAnswers()">🔄 清空答案</button>
            </div>
        </div>

        <div class="navigation">
            <a href="{prev_link}" class="btn btn-secondary">← 上一节</a>
            <a href="index.html" class="btn btn-secondary">返回目录</a>
            <a href="{next_link}" class="btn btn-primary">下一节 →</a>
        </div>
    </div>

    <!-- Toast提示 -->
    <div class="toast" id="toast"></div>

    <script src="js/one2one_common.js"></script>
    <script>
        // 设置当前页面的JSON文件路径
        const ANSWER_JSON_FILE = 'data/answers/one2one_C{course_num}_S{section_num}.json';
        const STORAGE_KEY = 'one2one_C{course_num}_S{section_num}';
    </script>
</body>
</html>'''
    
    return html_content

def main():
    """主函数"""
    print("=" * 60)
    print("一对一课程自动提取和生成工具")
    print("=" * 60)
    print()
    
    # 1. 解析内容
    print("步骤 1/4: 解析一对一.txt文件...")
    sections = parse_content()
    print(f"✓ 找到 {len(sections)} 个小节标记")
    
    # 2. 分配课程
    print("\n步骤 2/4: 分配到各课程...")
    sections_with_courses = assign_courses(sections)
    print(f"✓ 已分配 {len(sections_with_courses)} 个小节到7个课程")
    
    # 打印课程统计
    for course_num in range(1, 8):
        course_sections = [s for s in sections_with_courses if s['course_num'] == course_num]
        print(f"  第{course_num}课: {course_sections[0]['course_title']} - {len(course_sections)}节")
    
    # 3. 生成JSON文件
    print("\n步骤 3/4: 生成JSON答案文件...")
    data_dir = Path(__file__).parent / "data" / "answers"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    for section in sections_with_courses:
        json_data = generate_json_answer(section)
        json_file = data_dir / f"one2one_C{section['course_num']}_S{section['section_num']}.json"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ {json_file.name}")
    
    # 4. 生成HTML文件
    print("\n步骤 4/4: 生成HTML页面...")
    
    for i, section in enumerate(sections_with_courses):
        section_num = section['section_num']
        
        # 确定导航链接
        if i == 0:
            prev_link = "index.html"
        else:
            prev_link = f"one2one_C{sections_with_courses[i-1]['course_num']}_S{sections_with_courses[i-1]['section_num']}.html"
        
        if i == len(sections_with_courses) - 1:
            next_link = "index.html"
        else:
            next_link = f"one2one_C{sections_with_courses[i+1]['course_num']}_S{sections_with_courses[i+1]['section_num']}.html"
        
        html_content = generate_html_page(section, prev_link, next_link)
        html_file = Path(__file__).parent / f"one2one_C{section['course_num']}_S{section_num}.html"
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"  ✓ {html_file.name}")
    
    print("\n" + "=" * 60)
    print("✅ 所有文件生成完成！")
    print("=" * 60)
    print("\n📋 生成摘要:")
    print(f"  - JSON文件: {len(sections_with_courses)} 个")
    print(f"  - HTML文件: {len(sections_with_courses)} 个")
    print(f"  - 总课程数: 7 课")
    print(f"  - 总小节数: {len(sections_with_courses)} 节")
    print("\n⚠️  重要提示:")
    print("  1. JSON文件中的经文内容标记为【待补充】")
    print("  2. 请运行 'fill_bible_verses.py' 自动填充经文")
    print("  3. 或手动编辑JSON文件，添加完整经文")
    print("\n🚀 下一步:")
    print("  python3 fill_bible_verses.py")
    print()

if __name__ == '__main__':
    main()
