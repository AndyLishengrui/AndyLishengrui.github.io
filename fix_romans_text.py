#!/usr/bin/env python3#!/usr/bin/env python3

# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-

""""""

修复罗马书源文件的三个问题:修复罗马书源文件的三个问题:

1. 移除中文之间不合适的空格(如 "的 时候" -> "的时候")1. 移除中文之间不合适的空格(如 "的 时候" -> "的时候")

2. 修正错误换行(将被错误断开的句子连接起来)2. 修正错误换行(将被错误断开的句子连接起来)

3. 为段内经文引用添加标记,以便在HTML生成时应用内联样式3. 为段内经文引用添加标记,以便在HTML生成时应用内联样式

""""""



import reimport re



def fix_inappropriate_spaces(text):def fix_inappropriate_spaces(text):

    """    """

    移除中文字符之间不合适的空格    移除中文字符之间不合适的空格

    """    保留:

    # 移除中文字符之间的单个空格    - 中英文之间的空格

    text = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', text)    - 数字和中文之间的空格

        - 标点符号后的正常空格

    # 多次运行以处理连续的情况    """

    for _ in range(5):    # 移除中文字符之间的单个空格

        text = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', text)    # 匹配: 中文字符 + 空格 + 中文字符

        text = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', text)

    return text    

    # 多次运行以处理连续的情况

def fix_wrong_line_breaks(text):    for _ in range(5):

    """        text = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', text)

    修正错误的换行    

    """    return text

    lines = text.split('\n')

    fixed_lines = []def fix_wrong_line_breaks(text):

    i = 0    """

        修正错误的换行

    # 句子结束标记    - 如果一行以中文句号、问号、感叹号、引号等结束,则保留换行

    sentence_endings = ('。', '！', '？', '"', ''', '）', '>', ':', '：')    - 否则,与下一行连接(移除换行)

        """

    # 标题模式    lines = text.split('\n')

    heading_patterns = [    fixed_lines = []

        r'^\d+\s+.+$',    i = 0

        r'^\d+[\.、]\s*.+$',    

        r'^[一二三四五六七八九十]+、',    # 句子结束标记

    ]    sentence_endings = ('。', '！', '？', '"', ''', '）', '>', ':', '：')

        

    while i < len(lines):    # 特殊标记:章节标题、主题标题等应该独立成行

        line = lines[i].rstrip()    heading_patterns = [

                r'^\d+\s+.+$',  # 章节标题: "1 序言"

        if not line:        r'^\d+[\.、]\s*.+$',  # 主题标题: "1. 保罗是谁？"

            fixed_lines.append('')        r'^[一二三四五六七八九十]+、',  # 中文序号

            i += 1    ]

            continue    

            while i < len(lines):

        is_heading = any(re.match(pattern, line) for pattern in heading_patterns)        line = lines[i].rstrip()

        if is_heading:        

            fixed_lines.append(line)        # 空行保留

            i += 1        if not line:

            continue            fixed_lines.append('')

                    i += 1

        ends_with_sentence_end = line.endswith(sentence_endings)            continue

                

        if ends_with_sentence_end or i == len(lines) - 1:        # 检查是否是标题

            fixed_lines.append(line)        is_heading = any(re.match(pattern, line) for pattern in heading_patterns)

            i += 1        if is_heading:

        else:            fixed_lines.append(line)

            if i + 1 < len(lines):            i += 1

                next_line = lines[i + 1].strip()            continue

                if not next_line or any(re.match(pattern, next_line) for pattern in heading_patterns):        

                    fixed_lines.append(line)        # 检查当前行是否以句子结束符结尾

                    i += 1        ends_with_sentence_end = line.endswith(sentence_endings)

                else:        

                    combined = line + next_line        if ends_with_sentence_end or i == len(lines) - 1:

                    fixed_lines.append(combined)            # 句子结束或最后一行,保留

                    i += 2            fixed_lines.append(line)

            else:            i += 1

                fixed_lines.append(line)        else:

                i += 1            # 检查下一行

                if i + 1 < len(lines):

    return '\n'.join(fixed_lines)                next_line = lines[i + 1].strip()

                # 如果下一行是空行或标题,当前行独立

def mark_inline_scriptures(text):                if not next_line or any(re.match(pattern, next_line) for pattern in heading_patterns):

    """                    fixed_lines.append(line)

    标记段内经文引用                    i += 1

    """                else:

    lines = text.split('\n')                    # 连接到下一行

    processed_lines = []                    combined = line + next_line

                        fixed_lines.append(combined)

    scripture_pattern = r'\(([^)]*?)(\d+):(\d+[-\d,:]*)\)'                    i += 2

                else:

    for line in lines:                fixed_lines.append(line)

        stripped = line.strip()                i += 1

        if re.match(r'^\([^)]+\d+:\d+[-\d,:]*\)$', stripped):    

            processed_lines.append(line)    return '\n'.join(fixed_lines)

            continue

        def mark_inline_scriptures(text):

        if re.search(scripture_pattern, line):    """

            def replace_inline(match):    标记段内经文引用,以便后续HTML生成时应用内联样式

                return f'{{{{inline-scripture}}}}{match.group(0)}{{{{/inline-scripture}}}}'    匹配模式: (书名 章:节)

            line = re.sub(scripture_pattern, replace_inline, line)    

            不处理:

        processed_lines.append(line)    - 已经独立成段的经文(单独一行的经文引用)

        - 在经文块(<scripture>)内的引用

    return '\n'.join(processed_lines)    """

    lines = text.split('\n')

def main():    processed_lines = []

    input_file = 'BooksofRoman/romans_content.txt'    

    output_file = 'BooksofRoman/romans_content_fixed.txt'    # 经文引用模式: (书名 章:节) 或 (书名章:节)

        scripture_pattern = r'\(([^)]*?)(\d+):(\d+[-\d,:]*)\)'

    print(f"正在读取文件: {input_file}")    

    with open(input_file, 'r', encoding='utf-8') as f:    for line in lines:

        content = f.read()        # 检查是否是独立的经文行(整行只有一个经文引用)

            stripped = line.strip()

    original_length = len(content)        if re.match(r'^\([^)]+\d+:\d+[-\d,:]*\)$', stripped):

    print(f"原文件长度: {original_length} 字符")            # 独立经文引用,不需要标记为inline

                processed_lines.append(line)

    print("\n步骤 1/3: 移除中文之间不合适的空格...")            continue

    content = fix_inappropriate_spaces(content)        

    after_space_fix = len(content)        # 检查行中是否包含经文引用

    print(f"  - 移除了 {original_length - after_space_fix} 个空格")        if re.search(scripture_pattern, line):

                # 有经文引用,但不是独立的

    print("\n步骤 2/3: 修正错误的换行...")            # 用特殊标记包裹: {{inline-scripture}}(书名 章:节){{/inline-scripture}}

    content = fix_wrong_line_breaks(content)            def replace_inline(match):

    print(f"  - 处理完成")                return f'{{{{inline-scripture}}}}{match.group(0)}{{{{/inline-scripture}}}}'

                

    print("\n步骤 3/3: 标记段内经文引用...")            line = re.sub(scripture_pattern, replace_inline, line)

    content = mark_inline_scriptures(content)        

    inline_count = content.count('{{inline-scripture}}')        processed_lines.append(line)

    print(f"  - 标记了 {inline_count} 处段内经文引用")    

        return '\n'.join(processed_lines)

    print(f"\n正在保存到: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:def main():

        f.write(content)    input_file = 'BooksofRoman/romans_content.txt'

        output_file = 'BooksofRoman/romans_content_fixed.txt'

    final_length = len(content)    

    print(f"修复后文件长度: {final_length} 字符")    print(f"正在读取文件: {input_file}")

    print(f"\n✅ 完成! 修复后的文件已保存。")    with open(input_file, 'r', encoding='utf-8') as f:

    print(f"\n请检查 {output_file} 并确认修复效果。")        content = f.read()

    print("如果确认无误,请:")    

    print(f"  1. 备份原文件: cp {input_file} {input_file}.backup")    original_length = len(content)

    print(f"  2. 替换原文件: mv {output_file} {input_file}")    print(f"原文件长度: {original_length} 字符")

    print(f"  3. 重新生成网站: python3 generate_romans_website_v2.py")    

    # 步骤1: 移除不合适的空格

if __name__ == '__main__':    print("\n步骤 1/3: 移除中文之间不合适的空格...")

    main()    content = fix_inappropriate_spaces(content)

    after_space_fix = len(content)
    print(f"  - 移除了 {original_length - after_space_fix} 个空格")
    
    # 步骤2: 修正错误的换行
    print("\n步骤 2/3: 修正错误的换行...")
    content = fix_wrong_line_breaks(content)
    after_linebreak_fix = len(content)
    print(f"  - 处理完成")
    
    # 步骤3: 标记段内经文引用
    print("\n步骤 3/3: 标记段内经文引用...")
    content = mark_inline_scriptures(content)
    inline_count = content.count('{{inline-scripture}}')
    print(f"  - 标记了 {inline_count} 处段内经文引用")
    
    # 保存修复后的文件
    print(f"\n正在保存到: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    final_length = len(content)
    print(f"修复后文件长度: {final_length} 字符")
    print(f"\n✅ 完成! 修复后的文件已保存。")
    print(f"\n请检查 {output_file} 并确认修复效果。")
    print("如果确认无误,请:")
    print(f"  1. 备份原文件: cp {input_file} {input_file}.backup")
    print(f"  2. 替换原文件: mv {output_file} {input_file}")
    print(f"  3. 重新生成网站: python3 generate_romans_website_v2.py")

if __name__ == '__main__':
    main()
