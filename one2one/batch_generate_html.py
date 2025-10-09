#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成所有一对一课程的HTML页面
基于one2one_C1_S1.html的成功模板
"""

import json
import os
from pathlib import Path

# 课程信息
COURSES = {
    1: {"title": "新起点 得救", "sections": 14},
    2: {"title": "新主人 主权", "sections": 8},   # 实际只有8节
    3: {"title": "新方向 悔改", "sections": 9},   # 实际只有9节
    4: {"title": "新生命 洗礼", "sections": 9},
    5: {"title": "新操练 灵修", "sections": 9},
    6: {"title": "新关系 教会", "sections": 5},
    7: {"title": "新使命 带门徒", "sections": 2}
}

def load_json_data(course_num, section_num):
    """加载JSON答案数据"""
    json_file = f"data/answers/one2one_C{course_num}_S{section_num}.json"
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  JSON文件不存在: {json_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {json_file} - {e}")
        return None

def generate_verse_html(question_id, ref, has_answer=True):
    """生成单个经文填空的HTML"""
    return f'''                    <div class="reference-with-blank">
                        <div class="reference-header">
                            <span class="reference-text">{ref}</span>
                            <div class="hint-buttons">
                                <button class="btn-hint-partial" onclick="showPartialHint('{question_id}', '{ref}')" title="渐进提示">💡 提示</button>
                                <button class="btn-hint-full" onclick="showFullHint('{question_id}', '{ref}')" title="显示完整答案">👁️ 答案</button>
                            </div>
                        </div>
                        <textarea class="answer-input" data-question="{question_id}" data-reference="{ref}" data-has-answer="{'true' if has_answer else 'false'}"
                               data-hint-progress="0"
                               placeholder="请填写经文内容（和合本）..."></textarea>
                        <div class="answer-feedback" data-ref="{ref}"></div>
                        <div class="standard-answer" data-ref="{ref}"></div>
                    </div>'''

def generate_question_block(question_id, question_text, verses):
    """生成问题块HTML"""
    verses_html = "\n".join([
        generate_verse_html(question_id, v['reference'], v.get('has_data', True))
        for v in verses
    ])
    
    return f'''            <div class="question-block" data-question-id="{question_id}">
                <div class="question-header">
                    <span class="question-number">{question_id}.</span>
                    <span class="question-text">{question_text}</span>
                </div>
                <div class="answers-area">
{verses_html}
                </div>
            </div>'''

def get_navigation_links(course_num, section_num):
    """生成导航链接"""
    prev_link = ""
    next_link = ""
    
    # 上一节
    if section_num > 1:
        prev_link = f'<a href="one2one_C{course_num}_S{section_num-1}.html" class="btn btn-secondary">← 上一节</a>'
    else:
        prev_link = '<a href="../index.html" class="btn btn-secondary">返回目录</a>'
    
    # 下一节
    course_info = COURSES.get(course_num, {})
    total_sections = course_info.get('sections', 0)
    
    if section_num < total_sections:
        next_link = f'<a href="one2one_C{course_num}_S{section_num+1}.html" class="btn btn-check">下一节 →</a>'
    elif course_num < 7:
        # 跳到下一课第一节
        next_link = f'<a href="one2one_C{course_num+1}_S1.html" class="btn btn-check">下一课 →</a>'
    else:
        next_link = '<a href="../index.html" class="btn btn-check">完成课程 🎉</a>'
    
    return prev_link, next_link

def generate_html_page(course_num, section_num, json_data):
    """生成完整的HTML页面"""
    
    course_title = json_data.get('course_title', COURSES[course_num]['title'])
    section_title = json_data.get('section_title', f'第{section_num}节')
    answers = json_data.get('answers', {})
    
    # 提取问题和经文
    questions = {}
    for key, value in answers.items():
        # key格式: q{num}_{ref}
        parts = key.split('_', 1)
        if len(parts) == 2 and parts[0].startswith('q'):
            q_num = parts[0][1:]  # 去掉'q'
            if q_num not in questions:
                questions[q_num] = []
            questions[q_num].append({
                'reference': value.get('reference', parts[1]),
                'has_data': value.get('has_data', True)
            })
    
    # 生成问题块（假设只有一个问题）
    if questions:
        # 从一对一.txt提取的问题文本应该存储在某处
        # 这里先使用占位符
        question_text = "请阅读以下经文并填写："
        q_num = list(questions.keys())[0]
        verses = questions[q_num]
        questions_html = generate_question_block(q_num, question_text, verses)
    else:
        questions_html = '<p>本节暂无填空题目</p>'
    
    # 生成导航链接
    prev_link, next_link = get_navigation_links(course_num, section_num)
    
    # 计算总答案数
    total_answers = len([v for v in answers.values() if v.get('has_data', True)])
    
    # 生成完整HTML
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>第{course_num}课 第{section_num}节 - {section_title} | 一对一门徒训练</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            font-size: 16px;
            line-height: 1.8;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}

        header {{
            background: white;
            border-radius: 15px 15px 0 0;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .breadcrumb {{
            color: #888;
            font-size: 0.95em;
            margin-bottom: 12px;
        }}

        .breadcrumb a {{
            color: #667eea;
            text-decoration: none;
        }}

        .breadcrumb a:hover {{
            text-decoration: underline;
        }}

        h1 {{
            color: #333;
            margin-bottom: 15px;
            font-size: 2em;
            line-height: 1.4;
        }}

        .section-title-box {{
            display: inline-flex;
            align-items: center;
            gap: 15px;
            margin-top: 15px;
        }}

        .section-label {{
            display: inline-block;
            border: 2px solid #333;
            padding: 8px 20px;
            font-size: 1.1em;
            font-weight: 500;
            color: #333;
            line-height: 1.4;
        }}

        .section-name {{
            font-size: 1.3em;
            color: #333;
            font-weight: 500;
            line-height: 1.4;
        }}

        .content {{
            background: white;
            padding: 40px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .question-block {{
            margin-bottom: 35px;
            padding: 0;
            background: transparent;
            border: none;
        }}

        .question-header {{
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
        }}

        .question-number {{
            flex-shrink: 0;
            margin-right: 10px;
            color: #333;
            font-size: 1.1em;
            font-weight: 500;
            line-height: 1.8;
            min-width: 30px;
        }}

        .question-text {{
            font-size: 1.1em;
            color: #333;
            font-weight: normal;
            line-height: 1.8;
        }}

        .answers-area {{
            margin-left: 30px;
        }}

        .reference-with-blank {{
            margin-bottom: 25px;
            position: relative;
        }}

        .reference-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}

        .reference-text {{
            color: #667eea;
            font-size: 1em;
            font-weight: 500;
        }}

        .hint-buttons {{
            display: flex;
            gap: 8px;
        }}

        .btn-hint-partial, .btn-hint-full {{
            padding: 4px 12px;
            border: none;
            border-radius: 5px;
            font-size: 0.85em;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .btn-hint-partial {{
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            color: white;
        }}

        .btn-hint-partial:hover {{
            transform: translateY(-1px);
            box-shadow: 0 3px 10px rgba(243, 156, 18, 0.3);
        }}

        .btn-hint-full {{
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
        }}

        .btn-hint-full:hover {{
            transform: translateY(-1px);
            box-shadow: 0 3px 10px rgba(52, 152, 219, 0.3);
        }}

        .answer-input {{
            width: 100%;
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 12px;
            font-size: 1.05em;
            font-family: inherit;
            resize: vertical;
            outline: none;
            transition: all 0.3s;
            line-height: 1.8;
            min-height: 120px;
        }}

        .answer-input:focus {{
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}

        .answer-input.correct {{
            border-color: #27ae60;
            background: rgba(39, 174, 96, 0.05);
        }}

        .answer-input.incorrect {{
            border-color: #e74c3c;
            background: rgba(231, 76, 60, 0.05);
        }}

        .answer-input.partial {{
            border-color: #f39c12;
            background: rgba(243, 156, 18, 0.05);
        }}

        .answer-feedback {{
            margin-top: 8px;
            padding: 8px 12px;
            border-radius: 5px;
            font-size: 0.95em;
            display: none;
        }}

        .answer-feedback.show {{
            display: block;
        }}

        .answer-feedback.correct {{
            background: #d4edda;
            color: #155724;
            border-left: 4px solid #27ae60;
        }}

        .answer-feedback.incorrect {{
            background: #f8d7da;
            color: #721c24;
            border-left: 4px solid #e74c3c;
        }}

        .answer-feedback.partial {{
            background: #fff3cd;
            color: #856404;
            border-left: 4px solid #f39c12;
        }}

        .standard-answer {{
            display: none;
            margin-top: 12px;
            padding: 15px;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 0 5px 5px 0;
            font-size: 1em;
            color: #555;
            line-height: 1.8;
        }}

        .standard-answer.show {{
            display: block;
        }}

        .standard-answer strong {{
            color: #667eea;
            display: block;
            margin-bottom: 8px;
            font-size: 1em;
        }}

        .standard-answer .version-section {{
            margin-bottom: 15px;
        }}

        .standard-answer .version-section:last-child {{
            margin-bottom: 0;
        }}

        .standard-answer .version-label {{
            color: #667eea;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .standard-answer .verse-text {{
            color: #333;
            line-height: 1.8;
        }}

        .action-bar {{
            background: white;
            padding: 25px 40px;
            border-radius: 0 0 15px 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }}

        .score-display {{
            font-size: 1.15em;
            color: #333;
            font-weight: 500;
        }}

        .score-number {{
            color: #667eea;
            font-size: 1.4em;
            font-weight: bold;
        }}

        .btn {{
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
            font-weight: 500;
        }}

        .btn-check {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        .btn-check:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}

        .btn-submit {{
            background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
            color: white;
        }}

        .btn-submit:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(39, 174, 96, 0.4);
        }}

        .btn-secondary {{
            background: #f5f5f5;
            color: #333;
        }}

        .btn-secondary:hover {{
            background: #e0e0e0;
        }}

        .navigation {{
            background: white;
            padding: 20px 40px;
            margin-top: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            gap: 15px;
        }}

        .toast {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 15px 25px;
            border-radius: 8px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            display: none;
            z-index: 1000;
            max-width: 300px;
            font-size: 0.95em;
        }}

        .toast.show {{
            display: block;
            animation: slideIn 0.3s ease;
        }}

        @keyframes slideIn {{
            from {{
                transform: translateX(100%);
                opacity: 0;
            }}
            to {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}

        .score-modal {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.7);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 2000;
        }}

        .score-modal.show {{
            display: flex;
        }}

        .score-modal-content {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            max-width: 450px;
            animation: scaleIn 0.3s ease;
        }}

        @keyframes scaleIn {{
            from {{
                transform: scale(0.7);
                opacity: 0;
            }}
            to {{
                transform: scale(1);
                opacity: 1;
            }}
        }}

        .score-modal-content h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}

        .final-score {{
            font-size: 4em;
            color: #667eea;
            font-weight: bold;
            margin: 20px 0;
        }}

        .score-message {{
            font-size: 1.2em;
            color: #666;
            margin-bottom: 30px;
        }}

        .score-details {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: left;
        }}

        .score-details p {{
            margin: 8px 0;
            color: #555;
            font-size: 0.95em;
        }}

        .btn-close-modal {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            font-weight: 500;
        }}

        .btn-close-modal:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 10px;
                font-size: 15px;
            }}

            .content {{
                padding: 20px;
            }}

            .answers-area {{
                margin-left: 10px;
            }}

            .action-bar, .navigation {{
                padding: 15px 20px;
            }}

            .hint-buttons {{
                flex-direction: column;
                width: 100%;
            }}

            .btn-hint-partial, .btn-hint-full {{
                width: 100%;
            }}

            .score-modal-content {{
                max-width: 90%;
                padding: 30px 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="breadcrumb">
                <a href="../index.html">一对一首页</a> &gt; <a href="../index.html">第{course_num}课：{course_title}</a> &gt; 第{section_num}节
            </div>
            <h1>第{course_num}课：{course_title}</h1>
            <div class="section-title-box">
                <span class="section-label">第{section_num}节</span>
                <span class="section-name">{section_title}</span>
            </div>
        </header>

        <div class="content">
{questions_html}
        </div>

        <div class="action-bar">
            <div class="score-display">
                已完成: <span class="score-number" id="scoreDisplay">0/{total_answers}</span>
            </div>
            <div>
                <button class="btn btn-check" onclick="checkAnswers()">✓ 批改</button>
                <button class="btn btn-submit" onclick="submitAnswers()">📝 提交成绩</button>
                <button class="btn btn-secondary" onclick="clearAnswers()">🔄 清空</button>
            </div>
        </div>

        <div class="navigation">
            {prev_link}
            {next_link}
        </div>
    </div>

    <div class="toast" id="toast"></div>

    <div class="score-modal" id="scoreModal">
        <div class="score-modal-content">
            <h2>🎉 成绩报告</h2>
            <div class="final-score" id="finalScore">-</div>
            <div class="score-message" id="scoreMessage"></div>
            <div class="score-details" id="scoreDetails"></div>
            <button class="btn-close-modal" onclick="closeScoreModal()">确定</button>
        </div>
    </div>

    <script src="../js/one2one_common.js"></script>
    <script>
        // 页面特定配置
        const PAGE_CONFIG = {{
            courseNum: {course_num},
            sectionNum: {section_num},
            jsonFile: '../data/answers/one2one_C{course_num}_S{section_num}.json',
            storageKey: 'one2one_C{course_num}_S{section_num}_progress'
        }};
    </script>
</body>
</html>'''
    
    return html_content

def batch_generate_html(course_nums=None):
    """批量生成HTML页面"""
    
    if course_nums is None:
        course_nums = list(COURSES.keys())
    
    generated = 0
    failed = 0
    
    print("🚀 开始批量生成HTML页面...\n")
    
    for course_num in course_nums:
        if course_num not in COURSES:
            continue
        
        course_info = COURSES[course_num]
        course_title = course_info['title']
        total_sections = course_info['sections']
        
        print(f"📖 第{course_num}课：{course_title} ({total_sections}节)")
        
        for section_num in range(1, total_sections + 1):
            # 加载JSON数据
            json_data = load_json_data(course_num, section_num)
            
            if not json_data:
                print(f"  ⚠️  第{section_num}节 - JSON数据缺失")
                failed += 1
                continue
            
            # 生成HTML
            try:
                html_content = generate_html_page(course_num, section_num, json_data)
                
                # 保存HTML文件
                html_file = f"courses/one2one_C{course_num}_S{section_num}.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"  ✅ 第{section_num}节 - {html_file}")
                generated += 1
                
            except Exception as e:
                print(f"  ❌ 第{section_num}节 - 生成失败: {e}")
                failed += 1
        
        print()
    
    print(f"{'='*60}")
    print(f"🎉 完成！")
    print(f"  ✅ 成功生成: {generated} 个页面")
    print(f"  ❌ 失败: {failed} 个页面")
    print(f"{'='*60}")
    
    return generated, failed

if __name__ == '__main__':
    import sys
    
    # 确保目录存在
    Path('courses').mkdir(exist_ok=True)
    
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == '--all':
        print("🚀 批量生成所有课程（1-7课）")
        print("="*60)
        generated, failed = batch_generate_html(course_nums=list(range(1, 8)))
        print("\n🎊 完成！所有课程页面已生成！")
    else:
        # 测试模式：只生成第1课
        print("🧪 测试模式：只生成第1课")
        print("="*60)
        generated, failed = batch_generate_html(course_nums=[1])
        
        if failed == 0:
            print("\n✨ 测试成功！现在可以生成所有课程")
            print("💡 运行以下命令生成所有课程：")
            print("   python3 batch_generate_html.py --all")
