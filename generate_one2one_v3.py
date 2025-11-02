#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一对一课程页面生成器 V3
完全重构版本 - 确保格式与markdown源文件完全一致
"""

import os
import re
from pathlib import Path

def parse_markdown_file():
    """解析markdown文件,提取所有章节"""
    with open('one2one/一对一20251029.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = []
    
    # 1. 提取前言
    preface_pattern = r'### 前言（慕容）\s*\n(.*?)(?=### 开始作门徒)'
    match = re.search(preface_pattern, content, re.DOTALL)
    if match:
        sections.append({
            'id': 'preface',
            'title': '前言',
            'subtitle': '',
            'content': match.group(1).strip()
        })
    
    # 2. 提取开始作门徒
    intro_pattern = r'### 开始作门徒（三关系）\s*\n(.*?)(?=## 1 新起点)'
    match = re.search(intro_pattern, content, re.DOTALL)
    if match:
        sections.append({
            'id': 'intro',
            'title': '开始作门徒',
            'subtitle': '三关系',
            'content': match.group(1).strip()
        })
    
    # 3. 提取7个主要章节
    for i in range(1, 8):
        # 提取章节标题
        title_pattern = f'## {i} (新.*?)\\s*\n'
        title_match = re.search(title_pattern, content)
        if not title_match:
            continue
        
        chapter_title = title_match.group(1).strip()
        
        # 提取章节内容
        if i < 7:
            content_pattern = f'## {i} {re.escape(chapter_title)}\\s*\n(.*?)(?=## {i+1} 新)'
        else:
            content_pattern = f'## {i} {re.escape(chapter_title)}\\s*\n(.*?)(?=---|$)'
        
        content_match = re.search(content_pattern, content, re.DOTALL)
        if content_match:
            sections.append({
                'id': f'chapter_{i}',
                'title': chapter_title,
                'subtitle': f'第{i}课',
                'content': content_match.group(1).strip()
            })
    
    return sections


def format_scripture_block_simple(verse_text, reference):
    """格式化简单的圣经经文块"""
    html = '<div class="scripture">'
    html += f'<div class="scripture-text">{verse_text}</div>'
    html += f'<div class="scripture-ref">({reference})</div>'
    html += '</div>'
    return html


def format_inline_text(text):
    """格式化行内文本: 粗体、斜体等"""
    # 处理粗体 **text**
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    return text


def convert_content_to_html(text):
    """
    将markdown内容转换为HTML
    核心规则:
    1. 圣经经文格式: *经文文本* (经文引用) 或 *经文文本* *(经文引用)*
    2. 标题: ### 为h3, #### 为h4
    3. 段落: 空行分隔的文本块
    4. 列表: - 或数字开头
    5. 粗体: **文本**
    """
    lines = text.split('\n')
    html_parts = []
    i = 0
    
    while i < len(lines):
        line_stripped = lines[i].strip()
        
        # 跳过空行
        if not line_stripped:
            i += 1
            continue
        
        # 处理标题
        if line_stripped.startswith('####'):
            title = line_stripped.replace('####', '').strip()
            html_parts.append(f'<h4>{title}</h4>')
            i += 1
            continue
        
        if line_stripped.startswith('###'):
            title = line_stripped.replace('###', '').strip()
            html_parts.append(f'<h3>{title}</h3>')
            i += 1
            continue
        
        # 处理圣经经文块
        # 格式1: *经文文本（引用）* - 经文和引用在同一行
        # 格式2: *经文文本* 后面跟着 *(引用)* 或 (引用) - 分两行
        # 格式3: *经文开始... (可能多行) ...经文结束* 后面跟着 *(引用)* - 多行经文
        if line_stripped.startswith('*'):
            # 先检测是否是"经文和引用在同一行"的格式
            if line_stripped.endswith('*'):
                single_line = line_stripped.lstrip('*').rstrip('*').strip()
                # 检查是否包含括号作为引用（中文或英文括号）
                if '（' in single_line or '(' in single_line:
                    # 使用正则提取经文和引用
                    match = re.match(r'^(.*?)([（(][^（）()]+[）)])$', single_line)
                    if match:
                        verse_text = match.group(1).strip()
                        reference = match.group(2).strip('（）()')
                        # 只有当经文部分不为空时才作为单行经文处理
                        if verse_text:
                            html_parts.append(format_scripture_block_simple(verse_text, reference))
                            i += 1
                            continue
            
            # 原有的多行/分行经文逻辑
            verse_lines = []
            reference = None
            j = i
            
            # 第一阶段: 收集经文内容
            while j < len(lines):
                current_stripped = lines[j].strip()
                
                if not current_stripped:
                    j += 1
                    break
                
                # 检查是否是经文内容的第一行
                if j == i:
                    if current_stripped.startswith('*'):
                        verse_text = current_stripped.lstrip('*').rstrip('*').strip()
                        verse_lines.append(verse_text)
                        # 判断是单行还是多行经文
                        if current_stripped.endswith('*') and len(current_stripped.strip('*')) > 0:
                            # 单行经文 *text*
                            j += 1
                            break  # 经文收集完成,去检查引用
                        else:
                            # 多行经文的第一行 *text
                            j += 1
                    else:
                        # 不是经文开始,跳过这个块
                        break
                else:
                    # 后续行
                    if current_stripped.endswith('*') and not current_stripped.startswith('*'):
                        # 多行经文的最后一行 text*
                        verse_text = current_stripped.rstrip('*').strip()
                        if verse_text:
                            verse_lines.append(verse_text)
                        j += 1
                        break  # 经文收集完成,去检查引用
                    elif current_stripped.startswith('*'):
                        # 又一个新的特殊行(可能是引用或新经文),停止收集
                        break
                    else:
                        # 中间行
                        verse_lines.append(current_stripped)
                        j += 1
            
            # 第二阶段: 如果收集到了经文,检查下一行是否是引用（跳过空行）
            if verse_lines and j < len(lines):
                # 跳过空行
                while j < len(lines) and not lines[j].strip():
                    j += 1
                
                # 检查引用行
                if j < len(lines):
                    next_line_stripped = lines[j].strip()
                    # 引用格式: *(xxx)* 或 (xxx)
                    if next_line_stripped.startswith('*(') and next_line_stripped.endswith(')*'):
                        reference = next_line_stripped.strip('*').strip('()')
                        j += 1
                    elif next_line_stripped.startswith('(') and next_line_stripped.endswith(')'):
                        reference = next_line_stripped.strip('()')
                        j += 1
            
            # 如果找到完整的经文和引用,格式化为经文块
            if verse_lines and reference:
                combined_verse = '<br>'.join(verse_lines)
                html_parts.append(format_scripture_block_simple(combined_verse, reference))
                i = j
                continue
        
        # 处理列表
        if line_stripped.startswith('- ') or (len(line_stripped) > 2 and line_stripped[0].isdigit() and line_stripped[1] in '.)'):
            list_items = []
            j = i
            is_ordered = line_stripped[0].isdigit()
            
            while j < len(lines):
                list_line = lines[j].strip()
                if not list_line:
                    j += 1
                    if j < len(lines) and (lines[j].strip().startswith('- ') or 
                       (len(lines[j].strip()) > 2 and lines[j].strip()[0].isdigit())):
                        continue
                    break
                
                if list_line.startswith('- '):
                    item_text = list_line[2:].strip()
                    list_items.append(format_inline_text(item_text))
                    j += 1
                elif len(list_line) > 2 and list_line[0].isdigit() and list_line[1] in '.)':
                    item_text = re.sub(r'^\d+[.)]?\s*', '', list_line)
                    list_items.append(format_inline_text(item_text))
                    j += 1
                else:
                    break
            
            if list_items:
                tag = 'ol' if is_ordered else 'ul'
                html_parts.append(f'<{tag}>')
                for item in list_items:
                    html_parts.append(f'<li>{item}</li>')
                html_parts.append(f'</{tag}>')
                i = j
                continue
        
        # 处理水平线
        if line_stripped.startswith('---'):
            html_parts.append('<hr>')
            i += 1
            continue
        
        # 处理普通段落
        para_lines = [line_stripped]
        j = i + 1
        
        # 收集连续的非空行组成段落
        while j < len(lines):
            next_line = lines[j].strip()
            if not next_line:
                break
            # 如果遇到特殊标记,停止
            if (next_line.startswith('#') or 
                next_line.startswith('- ') or 
                next_line.startswith('*') or
                next_line.startswith('---') or
                (len(next_line) > 2 and next_line[0].isdigit() and next_line[1] in '.)')):
                break
            para_lines.append(next_line)
            j += 1
        
        para_text = ' '.join(para_lines)
        html_parts.append(f'<p>{format_inline_text(para_text)}</p>')
        i = j
    
    return '\n'.join(html_parts)


def format_scripture_block(verse_lines):
    """格式化圣经经文块"""
    full_text = '\n'.join(verse_lines)
    
    # 提取经文内容和引用
    # 经文在 * * 之间
    verse_pattern = r'\*(.*?)\*'
    ref_pattern = r'\((.*?)\)'
    
    verses = re.findall(verse_pattern, full_text)
    refs = re.findall(ref_pattern, full_text)
    
    if not verses:
        return ''
    
    # 组装HTML
    html = '<div class="scripture">'
    
    # 经文文本
    for verse in verses:
        verse = verse.strip()
        if verse and '和合本' not in verse and '和修版' not in verse:
            html += f'<div class="scripture-text">{verse}</div>'
    
    # 经文引用
    if refs:
        ref_text = refs[-1].strip()  # 通常最后一个括号是引用
        html += f'<div class="scripture-ref">({ref_text})</div>'
    
    html += '</div>'
    return html


def generate_html_page(section):
    """生成完整的HTML页面"""
    
    # 转换内容
    content_html = convert_content_to_html(section['content'])
    
    # 导航链接
    nav_links = {
        'preface': {'prev': '', 'next': 'intro.html'},
        'intro': {'prev': 'preface.html', 'next': 'chapter_1.html'},
        'chapter_1': {'prev': 'intro.html', 'next': 'chapter_2.html'},
        'chapter_2': {'prev': 'chapter_1.html', 'next': 'chapter_3.html'},
        'chapter_3': {'prev': 'chapter_2.html', 'next': 'chapter_4.html'},
        'chapter_4': {'prev': 'chapter_3.html', 'next': 'chapter_5.html'},
        'chapter_5': {'prev': 'chapter_4.html', 'next': 'chapter_6.html'},
        'chapter_6': {'prev': 'chapter_5.html', 'next': 'chapter_7.html'},
        'chapter_7': {'prev': 'chapter_6.html', 'next': ''},
    }
    
    nav = nav_links.get(section['id'], {'prev': '', 'next': ''})
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{section['title']} | 一对一门徒训练</title>
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
            line-height: 1.8;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            overflow: hidden;
        }}

        header {{
            background: white;
            padding: 30px;
            border-bottom: 3px solid #667eea;
        }}

        .breadcrumb {{
            color: #888;
            font-size: 0.9em;
            margin-bottom: 15px;
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
            font-size: 2em;
            margin-bottom: 10px;
        }}

        .subtitle {{
            color: #667eea;
            font-size: 1.1em;
            font-weight: 500;
        }}

        .content {{
            padding: 40px;
        }}

        .content h3 {{
            color: #333;
            margin: 35px 0 20px 0;
            font-size: 1.4em;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}

        .content h4 {{
            color: #555;
            margin: 25px 0 15px 0;
            font-size: 1.2em;
        }}

        .content p {{
            color: #444;
            margin-bottom: 20px;
            text-align: justify;
        }}

        .content strong {{
            color: #333;
            font-weight: 600;
        }}

        .content ul, .content ol {{
            margin: 20px 0;
            padding-left: 30px;
        }}

        .content li {{
            margin-bottom: 12px;
            color: #444;
        }}

        .content hr {{
            border: none;
            border-top: 2px solid #e0e0e0;
            margin: 40px 0;
        }}

        /* 圣经经文样式 */
        .scripture {{
            background: linear-gradient(135deg, #f0fff4 0%, #e6f7ed 100%);
            border-left: 5px solid #27ae60;
            padding: 25px;
            margin: 30px 0;
            border-radius: 0 10px 10px 0;
            box-shadow: 0 3px 10px rgba(39, 174, 96, 0.1);
        }}

        .scripture-text {{
            color: #2c3e50;
            font-size: 1.05em;
            line-height: 1.9;
            font-style: italic;
            margin-bottom: 12px;
        }}

        .scripture-ref {{
            color: #27ae60;
            font-weight: 600;
            font-size: 0.95em;
            text-align: right;
        }}

        /* 导航 */
        .navigation {{
            background: #f8f9fa;
            padding: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid #e0e0e0;
        }}

        .nav-btn {{
            padding: 12px 28px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s;
            display: inline-block;
        }}

        .nav-btn:hover {{
            background: #667eea;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}

        .nav-btn.home {{
            background: #667eea;
            color: white;
        }}

        .nav-btn.home:hover {{
            background: #5a67d8;
        }}

        .nav-btn:disabled,
        .nav-btn.disabled {{
            opacity: 0.3;
            cursor: not-allowed;
            pointer-events: none;
        }}

        /* 响应式 */
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}

            header {{
                padding: 20px;
            }}

            .content {{
                padding: 25px;
            }}

            h1 {{
                font-size: 1.6em;
            }}

            .content h3 {{
                font-size: 1.2em;
            }}

            .scripture {{
                padding: 20px;
            }}

            .navigation {{
                flex-direction: column;
                gap: 15px;
            }}

            .nav-btn {{
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
                <a href="index.html">一对一</a> &gt; {section['title']}
            </div>
            <h1>{section['title']}</h1>
            {f'<div class="subtitle">{section["subtitle"]}</div>' if section['subtitle'] else ''}
        </header>

        <div class="content">
            {content_html}
        </div>

        <div class="navigation">
            <div>
                {f'<a href="{nav["prev"]}" class="nav-btn">← 上一课</a>' if nav['prev'] else '<span class="nav-btn disabled">← 上一课</span>'}
            </div>
            <div>
                <a href="index.html" class="nav-btn home">📚 目录</a>
            </div>
            <div>
                {f'<a href="{nav["next"]}" class="nav-btn">下一课 →</a>' if nav['next'] else '<span class="nav-btn disabled">下一课 →</span>'}
            </div>
        </div>
    </div>
</body>
</html>'''
    
    return html


def generate_index_page(sections):
    """生成目录页"""
    
    items_html = []
    for section in sections:
        filename = f"{section['id']}.html"
        subtitle = f" - {section['subtitle']}" if section['subtitle'] else ''
        items_html.append(f'''
            <a href="{filename}" class="chapter-item">
                <div class="chapter-title">{section['title']}</div>
                {f'<div class="chapter-subtitle">{section["subtitle"]}</div>' if section['subtitle'] else ''}
            </a>
        ''')
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>一对一门徒训练课程</title>
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
            max-width: 800px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            color: white;
            padding: 40px 20px;
        }}

        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .chapters {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        }}

        .chapter-item {{
            display: block;
            padding: 20px;
            margin-bottom: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            text-decoration: none;
            transition: all 0.3s;
            border-left: 5px solid #667eea;
        }}

        .chapter-item:hover {{
            background: #667eea;
            transform: translateX(10px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}

        .chapter-title {{
            color: #333;
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 5px;
        }}

        .chapter-item:hover .chapter-title {{
            color: white;
        }}

        .chapter-subtitle {{
            color: #667eea;
            font-size: 0.95em;
        }}

        .chapter-item:hover .chapter-subtitle {{
            color: rgba(255,255,255,0.9);
        }}

        footer {{
            text-align: center;
            color: white;
            padding: 30px 20px;
            font-size: 0.9em;
            opacity: 0.8;
        }}

        @media (max-width: 768px) {{
            h1 {{
                font-size: 2em;
            }}

            .chapters {{
                padding: 20px;
            }}

            .chapter-item {{
                padding: 15px;
            }}

            .chapter-title {{
                font-size: 1.1em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📖 一对一</h1>
            <div class="subtitle">个人跟进及带门徒</div>
        </header>

        <div class="chapters">
            {''.join(items_html)}
        </div>

        <footer>
            <p>耶稣对他们说:"来跟从我,我要叫你们得人如得鱼一样。"</p>
            <p>(马可福音 1:17)</p>
        </footer>
    </div>
</body>
</html>'''
    
    return html


def main():
    """主函数"""
    print("=" * 50)
    print("一对一课程页面生成器 V3")
    print("=" * 50)
    
    # 创建输出目录
    output_dir = Path('done2one')
    output_dir.mkdir(exist_ok=True)
    
    # 解析markdown
    print("\n📖 解析markdown文件...")
    sections = parse_markdown_file()
    print(f"✓ 找到 {len(sections)} 个章节")
    
    # 生成各章节页面
    print("\n🔨 生成章节页面...")
    for section in sections:
        filename = f"{section['id']}.html"
        filepath = output_dir / filename
        
        html = generate_html_page(section)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  ✓ {filename} - {section['title']}")
    
    # 生成目录页
    print("\n🏠 生成目录页...")
    index_html = generate_index_page(sections)
    with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("  ✓ index.html")
    
    print("\n" + "=" * 50)
    print("✅ 全部完成!")
    print(f"📁 输出目录: {output_dir.absolute()}")
    print("🌐 启动服务器: python3 bible_server.py")
    print("=" * 50)


if __name__ == '__main__':
    main()
