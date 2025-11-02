#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成一对一课程的学习页面
为每一章节生成一个独立的HTML页面
参考foundation的设计方式
"""

import os
import re
from pathlib import Path

def parse_one2one_content():
    """解析一对一markdown文件内容"""

    with open('one2one/一对一20251029.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # 按章节分割内容
    sections = []

    # 提取前言
    preface_match = re.search(r'### 前言（慕容）\s*\n(.*?)(?=### 开始作门徒)', content, re.DOTALL)
    if preface_match:
        sections.append({
            'id': 'preface',
            'title': '前言',
            'content': preface_match.group(1).strip()
        })

    # 提取开始作门徒
    intro_match = re.search(r'### 开始作门徒（三关系）\s*\n(.*?)(?=## 1 新起点)', content, re.DOTALL)
    if intro_match:
        sections.append({
            'id': 'intro',
            'title': '开始作门徒',
            'content': intro_match.group(1).strip()
        })

    # 提取主要章节（1-7）
    for i in range(1, 8):
        pattern = f'## {i} 新.*?\\n(.*?)(?=(## \\d+|---|$))'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            # 提取章节标题
            title_match = re.search(f'## {i} (新.*?)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else f'第{i}章'

            sections.append({
                'id': f'chapter_{i}',
                'title': title,
                'content': match.group(1).strip()
            })

    return sections

def generate_section_html(section_id, section_title, section_content, prev_section, next_section):
    """生成单个章节的HTML页面"""

    # 处理内容，将markdown转换为HTML（传入章节 id 以便生成答题/提示回调）
    html_content = process_markdown_content(section_content, section_id)

    # 生成导航HTML
    nav_html = generate_navigation_html(prev_section, next_section)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{section_title} | 一对一</title>
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
            line-height: 1.8;
        }}

        .content h2 {{
            color: #333;
            margin: 30px 0 20px 0;
            font-size: 1.5em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}

        .content h3 {{
            color: #555;
            margin: 25px 0 15px 0;
            font-size: 1.2em;
        }}

        .content p {{
            margin-bottom: 20px;
            color: #444;
        }}

        .content blockquote {{
            border-left: 4px solid #667eea;
            padding-left: 20px;
            margin: 20px 0;
            font-style: italic;
            color: #666;
            background: #f8f9fa;
            padding: 15px 20px;
            border-radius: 0 5px 5px 0;
        }}

        .content ul, .content ol {{
            margin: 20px 0;
            padding-left: 30px;
        }}

        .content li {{
            margin-bottom: 10px;
            color: #444;
        }}

        .scripture {{
            background: #f8f9fa;
            border-left: 4px solid #27ae60;
            padding: 20px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
        }}

        .scripture-ref {{
            color: #27ae60;
            font-weight: bold;
            margin-bottom: 10px;
            display: block;
        }}

        .scripture-text {{
            font-style: italic;
            color: #333;
            line-height: 1.6;
        }}

        /* 去除答案输入/提示相关样式（已移除功能） */

        .personal-application {{
            background: #fff3cd;
            border: 1px solid #f0c674;
            border-radius: 8px;
            padding: 25px;
            margin: 30px 0;
        }}

        .personal-application h3 {{
            color: #856404;
            margin-bottom: 15px;
        }}

        .personal-application ul {{
            margin: 0;
            padding-left: 20px;
        }}

        .personal-application li {{
            margin-bottom: 8px;
            color: #856404;
        }}

        .navigation {{
            background: white;
            border-radius: 0 0 15px 15px;
            padding: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            display: flex;
            justify-content: center;
            gap: 20px;
        }}

        .nav-btn {{
            padding: 12px 25px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s;
        }}

        .nav-btn:hover {{
            background: #667eea;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}

        .home-btn {{
            background: #667eea;
            color: white;
        }}

        .home-btn:hover {{
            background: #5a67d8;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}

            .container {{
                max-width: 100%;
            }}

            header {{
                padding: 20px;
            }}

            .content {{
                padding: 20px;
            }}

            .navigation {{
                padding: 15px;
                gap: 10px;
            }}

            .nav-btn {{
                padding: 10px 15px;
                font-size: 0.9em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="breadcrumb">
                <a href="index.html">一对一</a> > {section_title}
            </div>
            <h1>{section_title}</h1>
            <div class="section-title-box">
                <div class="section-label">一对一</div>
                <div class="section-name">{section_title}</div>
            </div>
        </header>

        <div class="content">
            {html_content}
        </div>

        {nav_html}
    </div>

    <div id="toast" style="position:fixed;left:50%;transform:translateX(-50%);bottom:20px;background:rgba(0,0,0,0.75);color:white;padding:8px 14px;border-radius:6px;display:none;z-index:9999;"></div>

    <script>
        // 已移除提示/答案功能，保留简单的 toast 用于短消息显示
        function showToast(msg) {{
            const t = document.getElementById('toast');
            t.textContent = msg;
            t.style.display = 'block';
            setTimeout(() => t.style.display = 'none', 2500);
        }}
    </script>
</body>
</html>'''

    return html

def process_markdown_content(content, section_id=None):
    """将markdown内容转换为HTML

    增强对圣经引用的识别，并为每个经文块加入提示/答案按钮与标准答案容器。
    如果 future 有答案 JSON，会尝试通过 showFullHint 去加载并展示答案。
    """

    # 处理标题
    content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)

    # 优先处理常见的两行/两行内格式：
    # 形如：
    # *经文内容*
    # (申命记 6:4,5)
    # 或者：
    # *经文内容*  (申命记 6:4,5)
    # 为避免匹配跨段落或吞掉后续内容，使用行边界匹配并确保替换后保留段落分隔。

    def bible_replace(match):
        text = match.group('text').strip()
        ref = match.group('ref').strip()
        # 返回时保证后面有一个空行，避免紧跟文字被误认为在同一容器内
        return (f'<div class="scripture">\n'
                f'  <span class="scripture-ref">{ref}</span>\n'
                f'  <p class="scripture-text">{text}</p>\n'
                f'</div>\n\n')

    # 更稳健的经文匹配：按行匹配文本行（可能被 * 包裹）后紧跟一个引用行（可能在括号内）
    bible_pattern = re.compile(r'(?m)^[ \t]*\*?(?P<text>[^\n\*].*?\S)\*?[ \t]*\n[ \t]*\(?\s*(?P<ref>[^\)\n]+?)\s*\)?[ \t]*$', flags=re.MULTILINE)

    # 只在匹配的原始文本中不包含HTML标签时才替换为经文块，避免对已生成的HTML二次替换
    def safe_bible_sub(match):
        raw = match.group(0)
        if '<' in raw or '>' in raw:
            return raw
        return bible_replace(match)

    content = bible_pattern.sub(safe_bible_sub, content)

    # 处理单行内的 *经文* (参考) 形式（经文和引用在同一行或引用在行尾）
    inline_bible = re.compile(r'(?m)\*(?P<text>[^*]+)\*\s*\(?\s*(?P<ref>[^)\n]+)\s*\)?')

    def safe_inline_sub(match):
        raw = match.group(0)
        if '<' in raw or '>' in raw:
            return raw
        return bible_replace(match)

    content = inline_bible.sub(safe_inline_sub, content)

    # 处理普通引用（单独的引用段），使用行边界，避免吞掉其他 HTML
    content = re.sub(r'(?m)^[ \t]*\*([^*]+)\*\s*\n\s*\(([^*\)]+)\)[ \t]*$', r'<blockquote>\1<br><cite>\2</cite></blockquote>', content)

    # 确保经文块（scripture）在独立的段落中：在 <div class="scripture"> 前后保证有空行
    # 这样可以避免经文块被包裹进前面的 <p> 中，导致样式混用的问题。
    content = re.sub(r'\s*<div class="scripture">', r'\n\n<div class="scripture">', content)
    content = re.sub(r'</div>\s*', r'</div>\n\n', content)

    # 处理粗体
    content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)

    # 处理列表
    content = re.sub(r'^- (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
    content = re.sub(r'^(\d+)\. (.+)$', r'<li>\1. \2</li>', content, flags=re.MULTILINE)

    # 包装列表
    lines = content.split('\n')
    in_list = False
    processed_lines = []

    for line in lines:
        if line.strip().startswith('<li>'):
            if not in_list:
                processed_lines.append('<ul>')
                in_list = True
        elif in_list and line.strip():
            processed_lines.append('</ul>')
            in_list = False

        processed_lines.append(line)

    if in_list:
        processed_lines.append('</ul>')

    content = '\n'.join(processed_lines)

    # 删除仅含单个星号的孤立行（这些会显示为单独的 '*'，常来自原始 markdown 中的格式或替换残留）
    content = re.sub(r'(?m)^[ \t]*\*[ \t]*$', '', content)

    # 处理个人应用部分：替换已经转换为 <h3> 的标题片段并把下面内容包裹为个人应用卡片
    content = re.sub(r'(?s)(<h3>\s*个人应用.*?<\/h3>)(.*?)(?=(?:<h3>|<h4>|<div class="scripture">|\Z))', lambda m: f'<div class="personal-application">{m.group(1)}{m.group(2)}</div>', content)

    # 确保块级 HTML 结束标签后有段落分隔（避免紧跟文字被当成同一行，导致样式混用）
    content = re.sub(r'(?i)(</div>|</h3>|</h4>|</blockquote>)(?=[^\n])', r'\1\n\n', content)

    # 处理段落
    paragraphs = []
    for para in content.split('\n\n'):
        para = para.strip()
        if para and not para.startswith('<'):
            para = f'<p>{para}</p>'
        paragraphs.append(para)

    content = '\n\n'.join(paragraphs)

    # 移除孤立的星号行（例如 markdown 中单独的 "*" 被误保留下来）
    # 这会删除只包含星号的行（允许前后空白）
    content = re.sub(r'(?m)^[ \t]*\*[ \t]*$', '', content)

    # 进一步清理：删除位于 HTML 标签附近的孤立星号（例如 '</div>*' 或 '</div>*</p>' 等残留）
    # 把标签后面的 "*" 删除
    content = re.sub(r'>\s*\*\s*', '>', content)
    # 把标签前面的 "*" 删除
    content = re.sub(r'\*\s*(?=<)', '', content)
    # 删除紧邻闭合段落标签的星号
    content = re.sub(r'\*<\/p>', '</p>', content)
    # 删除行尾或换行前的星号
    content = re.sub(r'\*\s*(?=\n|$)', '', content)
    # 删除被空白包围的孤立星号
    content = re.sub(r'\s+\*\s+', ' ', content)

    # 删除空的列表项或空的列表（可能来自原始 markdown 中的换行或我们对经文块的插入）
    # 例如：<ul>\n<li></li>\n</ul> 这样的结构没有意义，移除它
    content = re.sub(r'(?s)<ul>\s*(?:<li>\s*</li>\s*)+</ul>', '', content)
    # 删除孤立的空 <li>
    content = re.sub(r'(?m)<li>\s*</li>', '', content)

    # 压缩过多的空行（最多保留两个换行），避免页面出现巨大的垂直间距
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content

def generate_navigation_html(prev_section, next_section):
    """生成导航HTML"""

    nav_parts = []

    if prev_section:
        nav_parts.append(f'<a href="{prev_section["file"]}" class="nav-btn">← {prev_section["title"]}</a>')
    else:
        nav_parts.append('<span class="nav-btn" style="opacity: 0.5; cursor: not-allowed;">← 上一章</span>')

    nav_parts.append('<a href="index.html" class="nav-btn home-btn">📚 目录</a>')

    if next_section:
        nav_parts.append(f'<a href="{next_section["file"]}" class="nav-btn">{next_section["title"]} →</a>')
    else:
        nav_parts.append('<span class="nav-btn" style="opacity: 0.5; cursor: not-allowed;">下一章 →</span>')

    return f'''
        <div class="navigation">
            {nav_parts[0]}
            {nav_parts[1]}
            {nav_parts[2]}
        </div>
    '''

def generate_index_page(sections):
    """生成目录页面"""

    section_links = []
    for section in sections:
        file_name = f"{section['id']}.html"
        section_links.append(f'<li><a href="{file_name}">{section["title"]}</a></li>')

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>一对一 - 个人跟进及带门徒</title>
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
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}

        h1 {{
            color: #333;
            margin-bottom: 15px;
            font-size: 2.5em;
        }}

        .subtitle {{
            color: #666;
            font-size: 1.2em;
            margin-bottom: 20px;
        }}

        .description {{
            color: #555;
            line-height: 1.6;
            max-width: 600px;
            margin: 0 auto;
        }}

        .content {{
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .toc {{
            margin: 30px 0;
        }}

        .toc h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}

        .toc ul {{
            list-style: none;
            padding: 0;
        }}

        .toc li {{
            margin-bottom: 10px;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }}

        .toc li:last-child {{
            border-bottom: none;
        }}

        .toc a {{
            display: block;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            text-decoration: none;
            color: #333;
            font-weight: 500;
            transition: all 0.3s;
        }}

        .toc a:hover {{
            background: #667eea;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}

            header {{
                padding: 20px;
            }}

            .content {{
                padding: 20px;
            }}

            h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>一对一</h1>
            <div class="subtitle">个人跟进及带门徒</div>
            <div class="description">
                《一对一》是一本帮助你进行个人跟进和带门徒的向导。它本身带不了门徒，但它能帮你带领门徒。
            </div>
        </header>

        <div class="content">
            <div class="toc">
                <h2>目录</h2>
                <ul>
                    {"\n                    ".join(section_links)}
                </ul>
            </div>
        </div>
    </div>
</body>
</html>'''

    return html

    return html

def main():
    """主函数"""

    print("开始解析一对一课程内容...")

    # 解析内容
    sections = parse_one2one_content()
    print(f"共解析出 {len(sections)} 个章节")

    # 创建done2one目录
    os.makedirs('done2one', exist_ok=True)

    # 生成章节页面
    prev_section = None
    for i, section in enumerate(sections):
        section_id = section['id']
        section_title = section['title']

        # 确定下一章节
        next_section = None
        if i < len(sections) - 1:
            next_section = {
                'file': f'{sections[i+1]["id"]}.html',
                'title': sections[i+1]['title']
            }

        # 生成HTML页面
        filename = f'done2one/{section_id}.html'
        html_content = generate_section_html(
            section_id,
            section_title,
            section['content'],
            prev_section,
            next_section
        )

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✓ 生成: {filename} - {section_title}")

        # 设置为下一章节的prev
        prev_section = {
            'file': f'{section_id}.html',
            'title': section_title
        }

    # 生成目录页面
    index_html = generate_index_page(sections)
    with open('done2one/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)

    print("✓ 生成目录页面: done2one/index.html")
    print(f"\n🎉 一对一课程网站生成完成！共 {len(sections)} 个页面")
    print("📁 文件保存在 done2one/ 目录中")
    print("🌐 启动服务器: python3 bible_server.py (然后访问 http://localhost:8001/done2one/)")

if __name__ == '__main__':
    main()