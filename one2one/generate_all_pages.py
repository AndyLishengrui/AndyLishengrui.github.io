#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一对一课程批量生成器
自动从一对一.txt文件中提取内容，生成HTML页面和JSON答案文件
"""

import json
import os
import re
from pathlib import Path

# 课程结构定义
COURSE_STRUCTURE = {
    1: {"title": "新起点 得救", "sections": 14, "start_num": 1},
    2: {"title": "新主人 主权", "sections": 8, "start_num": 15},
    3: {"title": "新方向 悔改", "sections": 9, "start_num": 23},
    4: {"title": "新生命 洗礼", "sections": 10, "start_num": 32},
    5: {"title": "新操练 灵修", "sections": 11, "start_num": 42},
    6: {"title": "新关系 教会", "sections": 8, "start_num": 53},
    7: {"title": "新使命 带门徒", "sections": 9, "start_num": 61}
}

def create_html_page(course_num, section_num, section_title, content_text, verses, prev_link, next_link):
    """创建HTML页面"""
    
    course_info = COURSE_STRUCTURE[course_num]
    
    # 生成经文填空HTML
    verse_blanks_html = ""
    for i, verse in enumerate(verses, 1):
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
                    <p>{verse.get('text', '待补充')}</p>
                    {f'''<div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #ddd; color: #666; font-size: 0.95em;">
                        <strong>其他译本（{verse.get('version_alt', '新译本')}）：</strong><br>
                        {verse.get('text_alt', '')}
                    </div>''' if verse.get('text_alt') else ''}
                </div>
            </div>
"""
    
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
            font-size: 0.9em;
            margin-bottom: 10px;
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
        }}

        .section-name {{
            font-size: 1.3em;
            color: #333;
            font-weight: 500;
        }}

        .content {{
            background: white;
            padding: 40px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .question-block {{
            margin: 30px 0;
            padding: 30px;
            background: #fafbfc;
            border-radius: 10px;
            border: 1px solid #e8e8e8;
        }}

        .content-paragraph {{
            font-size: 1.05em;
            line-height: 1.9;
            margin-bottom: 20px;
            color: #333;
            text-align: justify;
        }}

        /* 经文填空样式 */
        .blank-section {{
            margin: 30px 0;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 10px;
            border: 2px dashed #ddd;
        }}

        .blank-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}

        .blank-reference {{
            color: #667eea;
            font-weight: 600;
            font-size: 1.05em;
        }}

        .hint-buttons {{
            display: flex;
            gap: 8px;
        }}

        .btn-hint {{
            padding: 6px 15px;
            border: none;
            border-radius: 6px;
            font-size: 0.9em;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 500;
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
            min-height: 120px;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1.05em;
            font-family: inherit;
            line-height: 1.8;
            resize: vertical;
            transition: all 0.3s;
        }}

        .answer-input:focus {{
            outline: none;
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
            margin-top: 10px;
            padding: 10px 15px;
            border-radius: 6px;
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
            margin-top: 15px;
            padding: 20px;
            background: white;
            border: 2px solid #667eea;
            border-radius: 8px;
            font-size: 1em;
            color: #333;
            line-height: 1.8;
        }}

        .standard-answer.show {{
            display: block;
        }}

        .standard-answer strong {{
            color: #667eea;
            display: block;
            margin-bottom: 10px;
        }}

        .action-bar {{
            background: white;
            padding: 25px 40px;
            margin-top: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }}

        .score-display {{
            font-size: 1.1em;
            color: #333;
            font-weight: 500;
        }}

        .score-number {{
            color: #667eea;
            font-size: 1.4em;
            font-weight: bold;
        }}

        .btn-check, .btn-submit, .btn-clear {{
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s;
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

        .btn-clear {{
            background: #f5f5f5;
            color: #333;
        }}

        .btn-clear:hover {{
            background: #e0e0e0;
        }}

        .navigation {{
            background: white;
            border-radius: 0 0 15px 15px;
            padding: 25px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
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

        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}

        .btn-secondary {{
            background: #f0f0f0;
            color: #333;
        }}

        .btn-secondary:hover {{
            background: #e0e0e0;
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
            animation: slideIn 0.3s ease;
        }}

        .toast.show {{
            display: block;
        }}

        @keyframes slideIn {{
            from {{
                transform: translateX(400px);
            }}
            to {{
                transform: translateX(0);
            }}
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}

            header, .content, .navigation, .action-bar {{
                padding: 20px;
            }}

            h1 {{
                font-size: 1.6em;
            }}

            .question-block, .blank-section {{
                padding: 20px;
            }}

            .blank-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}

            .hint-buttons {{
                width: 100%;
            }}

            .action-bar {{
                flex-direction: column;
            }}

            .navigation {{
                flex-direction: column;
                gap: 10px;
            }}

            .btn {{
                width: 100%;
                text-align: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="breadcrumb">
                <a href="index.html">一对一首页</a> &gt; <a href="index.html">第{course_num}课：{course_info['title']}</a> &gt; 第{section_num}节
            </div>
            <h1>第{course_num}课：{course_info['title']}</h1>
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

# 先只生成第1课作为示例
print("开始生成第1课的所有页面...")
print("第1课：新起点 得救（14节）")
print("\n注意：这是一个框架脚本，实际使用需要从一对一.txt文件中提取详细内容")
print("建议手动完成内容提取，确保准确性\n")
