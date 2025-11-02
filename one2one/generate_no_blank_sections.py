#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为第9节和第12节（无填空题的页面）生成特殊HTML
"""

import json
import os

def generate_no_blank_section(section_num):
    """生成没有填空题的节页面"""
    
    # 读取JSON获取description
    json_file = f"data/answers/one2one_C1_S{section_num}.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    description = data.get('description', '')
    
    section_titles = {
        9: "回应：凭信心领受神的恩典",
        11: "个人应用",
        12: "得救的祷告"
    }
    section_title = section_titles.get(section_num, f"第{section_num}节")
    
    # 确定导航
    prev_link = f"one2one_C1_S{section_num-1}.html"
    next_link = f"one2one_C1_S{section_num+1}.html" if section_num < 14 else "../index.html"
    next_text = "下一节 →" if section_num < 14 else "返回目录"
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>第1课 第{section_num}节 - {section_title} | 一对一门徒训练</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
            line-height: 1.8;
            color: #2c3e50;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .breadcrumb {{
            font-size: 0.9em;
            margin-bottom: 15px;
            opacity: 0.9;
        }}

        .breadcrumb a {{
            color: white;
            text-decoration: none;
        }}

        .breadcrumb a:hover {{
            text-decoration: underline;
        }}

        h1 {{
            font-size: 2em;
            margin-bottom: 15px;
            font-weight: 600;
        }}

        .section-title-box {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 10px 25px;
            border-radius: 25px;
            backdrop-filter: blur(10px);
        }}

        .section-label {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-right: 10px;
        }}

        .section-name {{
            font-size: 1.1em;
            font-weight: 500;
        }}

        .content {{
            padding: 40px;
        }}

        .description-text {{
            font-size: 1.1em;
            line-height: 2;
            color: #34495e;
            white-space: pre-wrap;
            margin-bottom: 30px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}

        .navigation {{
            display: flex;
            justify-content: space-between;
            padding: 20px 40px;
            background: #f8f9fa;
            border-top: 1px solid #e9ecef;
        }}

        .btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s;
            font-weight: 500;
        }}

        .btn-secondary {{
            background: #6c757d;
            color: white;
        }}

        .btn-secondary:hover {{
            background: #5a6268;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}

        .btn-check {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        .btn-check:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}

            .container {{
                border-radius: 10px;
            }}

            header {{
                padding: 20px;
            }}

            h1 {{
                font-size: 1.5em;
            }}

            .content {{
                padding: 20px;
            }}

            .description-text {{
                font-size: 1em;
                padding: 15px;
            }}

            .navigation {{
                flex-direction: column;
                gap: 10px;
                padding: 15px 20px;
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
                <a href="index.html">一对一首页</a> &gt; 
                <a href="index.html">第1课：新起点 得救</a> &gt; 
                第{section_num}节
            </div>
            <h1>第1课：新起点 得救</h1>
            <div class="section-title-box">
                <span class="section-label">第{section_num}节</span>
                <span class="section-name">{section_title}</span>
            </div>
        </header>

        <div class="content">
            <div class="description-text">{description}</div>
        </div>

        <div class="navigation">
            <a href="{prev_link}" class="btn btn-secondary">← 上一节</a>
            <a href="../index.html" class="btn btn-secondary">返回目录</a>
            <a href="{next_link}" class="btn btn-check">{next_text}</a>
        </div>
    </div>
</body>
</html>'''
    
    # 保存HTML
    output_file = f"courses/one2one_C1_S{section_num}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 第{section_num}节: 已生成纯讲解页面")

def main():
    print("=" * 60)
    print("生成第9节和第12节的纯讲解页面...")
    print("=" * 60)
    
    # 生成第9节和第12节
    for section_num in [9, 12]:
        generate_no_blank_section(section_num)
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
