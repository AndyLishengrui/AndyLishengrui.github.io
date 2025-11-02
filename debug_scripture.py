import re

def format_scripture_block_simple(verse_text, reference):
    """格式化简单的圣经经文块"""
    html = '<div class="scripture">'
    html += f'<div class="scripture-text">{verse_text}</div>'
    html += f'<div class="scripture-ref">({reference})</div>'
    html += '</div>'
    return html

def format_inline_text(text):
    """格式化行内文本"""
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    return text

def convert_content_to_html(text):
    """将markdown内容转换为HTML"""
    lines = text.split('\n')
    html_parts = []
    i = 0
    
    while i < len(lines):
        line_stripped = lines[i].strip()
        
        # 跳过空行
        if not line_stripped:
            i += 1
            continue
        
        # 处理圣经经文块
        if line_stripped.startswith('*'):
            print(f"\n[DEBUG] Line {i} starts with *, processing scripture block")
            print(f"[DEBUG] Line content: [{repr(line_stripped[:50])}...]")
            
            verse_lines = []
            reference = None
            j = i
            in_verse = True
            
            # 收集经文内容
            while j < len(lines) and in_verse:
                current_stripped = lines[j].strip()
                
                if not current_stripped:
                    print(f"[DEBUG] Line {j} is empty, breaking")
                    j += 1
                    break
                
                # 如果是引用行: *(xxx)* 或 (xxx)
                if current_stripped.startswith('*(') and current_stripped.endswith(')*'):
                    reference = current_stripped.strip('*').strip('()')
                    print(f"[DEBUG] Line {j} is reference: {reference}")
                    j += 1
                    break
                elif current_stripped.startswith('(') and current_stripped.endswith(')'):
                    reference = current_stripped.strip('()')
                    print(f"[DEBUG] Line {j} is reference (alt format): {reference}")
                    j += 1
                    break
                
                # 检查是否是经文内容
                if j == i:
                    # 第一行必须以*开头
                    if current_stripped.startswith('*'):
                        verse_text = current_stripped.lstrip('*').rstrip('*').strip()
                        verse_lines.append(verse_text)
                        print(f"[DEBUG] Line {j} is first verse line: [{verse_text[:30]}...]")
                        if current_stripped.endswith('*') and len(current_stripped) > 1:
                            # 单行经文
                            print(f"[DEBUG] Single line scripture")
                            in_verse = False
                        j += 1
                    else:
                        print(f"[DEBUG] Line {j} doesn't start with *, breaking")
                        break
                else:
                    # 后续行
                    if current_stripped.endswith('*'):
                        # 最后一行
                        verse_text = current_stripped.rstrip('*').strip()
                        if verse_text:
                            verse_lines.append(verse_text)
                        print(f"[DEBUG] Line {j} is last verse line: [{verse_text[:30]}...]")
                        in_verse = False
                        j += 1
                    elif current_stripped.startswith('*'):
                        # 又一个新的经文块开始了
                        print(f"[DEBUG] Line {j} starts new scripture block, breaking")
                        break
                    else:
                        # 中间行
                        verse_lines.append(current_stripped)
                        print(f"[DEBUG] Line {j} is middle verse line: [{current_stripped[:30]}...]")
                        j += 1
            
            # 如果找到经文和引用,格式化为经文块
            if verse_lines and reference:
                combined_verse = '<br>'.join(verse_lines)
                print(f"[DEBUG] Found complete scripture: {len(verse_lines)} lines, ref={reference}")
                html_parts.append(format_scripture_block_simple(combined_verse, reference))
                i = j
                continue
            else:
                print(f"[DEBUG] Scripture incomplete: verse_lines={len(verse_lines)}, reference={reference}")
        
        # 其他处理...
        print(f"[DEBUG] Line {i}: treating as paragraph: [{line_stripped[:30]}...]")
        html_parts.append(f'<p>{line_stripped}</p>')
        i += 1
    
    return '\n'.join(html_parts)

# 读取markdown
with open('one2one/一对一20251029.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 使用和generate_one2one_v3.py完全相同的逻辑提取第一章
i = 1
title_pattern = f'## {i} (新.*?)\\s*\n'
title_match = re.search(title_pattern, content)
if title_match:
    chapter_title = title_match.group(1).strip()
    content_pattern = f'## {i} {re.escape(chapter_title)}\\s*\n(.*?)(?=## {i+1} 新)'
    content_match = re.search(content_pattern, content, re.DOTALL)
    if content_match:
        chapter1_content = content_match.group(1).strip()
        print(f"第一章标题: {chapter_title}")
        print(f"开始转换HTML...")
        print("=" * 80)
        
        result_html = convert_content_to_html(chapter1_content)
        
        print("=" * 80)
        print(f"\n转换完成!")
        print(f"检查'scripture'是否在输出中: {'scripture' in result_html}")
        print(f"检查'膀臂'是否在输出中: {'膀臂' in result_html}")



