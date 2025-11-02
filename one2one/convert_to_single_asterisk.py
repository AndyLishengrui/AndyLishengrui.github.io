#!/usr/bin/env python3
import re

# 读取文件
with open('一对一20251029.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 将所有 **内容** 格式转换为 *内容* 格式
# 使用非贪婪匹配，避免跨行问题
pattern = r'\*\*([^*]+?)\*\*'
replacement = r'*\1*'

# 多次替换，确保所有双星号都被转换
new_content = content
while re.search(pattern, new_content):
    new_content = re.sub(pattern, replacement, new_content)

# 写回文件
with open('一对一20251029.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("所有圣经经文和引文已成功转换为 *   * 格式")
