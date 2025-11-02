import re

# 模拟处理逻辑
line1 = '*"你们为什么称呼我\'主啊，主啊\'却不遵我的话行呢？*'
line2 = '*(路加福音 6:46 和合本)*'

# 处理第一行
line_stripped = line1.strip()
print(f'Line 1: [{line_stripped}]')
print(f'  starts with *: {line_stripped.startswith("*")}')
print(f'  ends with *: {line_stripped.endswith("*")}')

single_line = line_stripped.lstrip('*').rstrip('*').strip()
print(f'  single_line: [{single_line}]')
print(f'  has 括号: {"（" in single_line or "(" in single_line}')

# 如果没有括号，进入分行逻辑
verse_text = line_stripped.lstrip('*').rstrip('*').strip()
print(f'  verse_text: [{verse_text}]')

# 检查下一行
next_line_stripped = line2.strip()
print(f'\nLine 2: [{next_line_stripped}]')
print(f'  starts with *(: {next_line_stripped.startswith("*(")}')
print(f'  ends with )*: {next_line_stripped.endswith(")*")}')

if next_line_stripped.startswith('*(') and next_line_stripped.endswith(')*'):
    reference = next_line_stripped.strip('*').strip('()')
    print(f'  reference: [{reference}]')
    print(f'\n✓ Should generate scripture block with:')
    print(f'  verse: {verse_text}')
    print(f'  ref: {reference}')
