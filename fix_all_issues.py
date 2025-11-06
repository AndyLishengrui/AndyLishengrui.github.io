#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
罗马书内容综合修复脚本
1. 移除多余空格
2. 修复错误换行
3. 统一经文标记格式
4. 修复嵌套错误
"""

import re
import os

class RomansContentFixer:
    def __init__(self):
        self.chapters_dir = "BooksofRoman/chapters"
        self.backup_dir = "BooksofRoman/chapters_backup"
        self.fix_count = {
            'extra_spaces': 0,
            'line_breaks': 0,
            'scripture_marks': 0,
            'nested_errors': 0
        }
    
    def backup_files(self):
        """备份原始文件"""
        import shutil
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            for i in range(1, 17):
                src = os.path.join(self.chapters_dir, f"chapter_{i:02d}.txt")
                dst = os.path.join(self.backup_dir, f"chapter_{i:02d}.txt")
                if os.path.exists(src):
                    shutil.copy2(src, dst)
            print("✓ 已备份所有章节文件到", self.backup_dir)
    
    def fix_extra_spaces(self, text):
        """修复多余空格"""
        original = text
        
        # 1. 移除中文字符间的多余空格(保留句子间的空格)
        # 匹配: 中文字符 + 空格 + 中文字符
        text = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', text)
        
        # 2. 移除中文标点后多余空格
        text = re.sub(r'([，。！？；：、])\s+', r'\1', text)
        
        # 3. 移除行尾空格
        text = re.sub(r'\s+$', '', text, flags=re.MULTILINE)
        
        # 4. 移除行首空格(除了缩进)
        lines = text.split('\n')
        fixed_lines = []
        for line in lines:
            # 保留有意义的缩进,移除无意义的空格
            if line.strip():
                fixed_lines.append(line.rstrip())
            else:
                fixed_lines.append('')
        text = '\n'.join(fixed_lines)
        
        # 5. 多个连续空格变为单个空格
        text = re.sub(r'  +', ' ', text)
        
        if text != original:
            self.fix_count['extra_spaces'] += text.count('\n')
        
        return text
    
    def fix_line_breaks(self, text):
        """修复错误换行"""
        original = text
        lines = text.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # 跳过空行
            if not line:
                fixed_lines.append('')
                i += 1
                continue
            
            # 跳过标题行(数字开头)
            if re.match(r'^\d+\.?\s+', line):
                fixed_lines.append(lines[i])
                i += 1
                continue
            
            # 跳过经文标记行
            if '{{scripture}}' in line or '{{/scripture}}' in line:
                fixed_lines.append(lines[i])
                i += 1
                continue
            
            # 检查是否是被错误截断的行
            # 如果行尾没有标点符号,且下一行不是标题/空行,则合并
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                
                # 如果当前行没有结束标点,且下一行不是新段落
                if (not re.search(r'[。！？；：]$', line) and 
                    next_line and 
                    not re.match(r'^\d+\.?\s+', next_line) and
                    not next_line.startswith('{{') and
                    len(line) > 20):  # 只合并较长的行
                    
                    # 合并行
                    merged = line + next_line
                    fixed_lines.append(merged)
                    i += 2
                    self.fix_count['line_breaks'] += 1
                    continue
            
            fixed_lines.append(lines[i])
            i += 1
        
        return '\n'.join(fixed_lines)
    
    def fix_scripture_marks(self, text):
        """统一经文标记格式"""
        original = text
        
        # 1. 修复 {{inline-scripture}} 标记
        # 标准格式: "经文内容" {{inline-scripture}}(引用){{/inline-scripture}}
        
        # 先移除所有 inline-scripture 标记,重新识别
        text = re.sub(r'\{\{inline-scripture\}\}', '', text)
        text = re.sub(r'\{\{/inline-scripture\}\}', '', text)
        
        # 2. 识别经文引用模式并添加标记
        # 模式1: (书卷名 章:节)
        scripture_pattern = r'\(([^)]*?书|[^)]*?音|约翰一书|约翰二书|约翰三书|犹大书)\s*\d+[:：]\d+[^)]*?\)'
        
        def mark_scripture(match):
            ref = match.group(0)
            return f'{{{{scripture-ref}}}}{ref}{{{{/scripture-ref}}}}'
        
        text = re.sub(scripture_pattern, mark_scripture, text)
        self.fix_count['scripture_marks'] += len(re.findall(scripture_pattern, original))
        
        # 3. 识别完整经文块
        # 模式: 引号开始的长句 + 经文引用
        lines = text.split('\n')
        in_scripture_block = False
        scripture_buffer = []
        fixed_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # 检测经文块开始
            if (stripped.startswith('"') or stripped.startswith('"')) and '{{scripture-ref}}' in line:
                # 这是一个完整的经文块
                # 格式: {{scripture}}"经文内容" (引用){{/scripture}}
                # 提取引号中的内容和引用
                quote_match = re.search(r'["""](.+?)["""](.+)', stripped)
                if quote_match:
                    verse_text = quote_match.group(1)
                    reference = quote_match.group(2)
                    fixed_line = f'{{{{scripture}}}}"{verse_text}" {reference}{{{{/scripture}}}}'
                    fixed_lines.append(fixed_line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def fix_nested_errors(self, text):
        """修复嵌套错误"""
        original = text
        
        # 1. 移除错误的嵌套标记
        # 检测: {{scripture}}...{{scripture}}...{{/scripture}}{{/scripture}}
        
        # 简单的修复策略: 移除内层重复的标记
        text = re.sub(r'\{\{scripture\}\}(\s*)\{\{scripture\}\}', r'{{\1scripture}}', text)
        text = re.sub(r'\{\{/scripture\}\}(\s*)\{\{/scripture\}\}', r'{{\1/scripture}}', text)
        
        # 2. 修复未闭合的标记
        # 统计开始和结束标记数量
        open_count = text.count('{{scripture}}')
        close_count = text.count('{{/scripture}}')
        
        if open_count != close_count:
            print(f"  ⚠️  警告: scripture标记不匹配 (开始:{open_count}, 结束:{close_count})")
            self.fix_count['nested_errors'] += abs(open_count - close_count)
        
        # 3. 修复 scripture-ref 嵌套
        open_ref_count = text.count('{{scripture-ref}}')
        close_ref_count = text.count('{{/scripture-ref}}')
        
        if open_ref_count != close_ref_count:
            print(f"  ⚠️  警告: scripture-ref标记不匹配 (开始:{open_ref_count}, 结束:{close_ref_count})")
        
        # 4. 移除直接写在文本中的标记文本
        # 有时候标记本身被当作文本输出了
        text = re.sub(r'(?<!\{)\{\{scripture\}\}(?!\{)', '', text)
        text = re.sub(r'(?<!\})\{\{/scripture\}\}(?!\})', '', text)
        
        return text
    
    def process_chapter(self, chapter_num):
        """处理单个章节"""
        chapter_file = os.path.join(self.chapters_dir, f"chapter_{chapter_num:02d}.txt")
        
        if not os.path.exists(chapter_file):
            return
        
        print(f"\n处理章节 {chapter_num}: {chapter_file}")
        
        # 读取文件
        with open(chapter_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 应用所有修复
        print("  → 修复多余空格...")
        content = self.fix_extra_spaces(content)
        
        print("  → 修复错误换行...")
        content = self.fix_line_breaks(content)
        
        print("  → 统一经文标记...")
        content = self.fix_scripture_marks(content)
        
        print("  → 修复嵌套错误...")
        content = self.fix_nested_errors(content)
        
        # 保存修复后的文件
        if content != original_content:
            with open(chapter_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("  ✓ 已保存修复")
        else:
            print("  ✓ 无需修复")
    
    def fix_all_chapters(self):
        """修复所有章节"""
        print("=" * 60)
        print("开始修复罗马书16章内容")
        print("=" * 60)
        
        # 备份
        self.backup_files()
        print()
        
        # 处理每章
        for i in range(1, 17):
            self.process_chapter(i)
        
        print()
        print("=" * 60)
        print("✓ 修复完成!")
        print("=" * 60)
        print(f"📊 统计:")
        print(f"  - 修复多余空格: ~{self.fix_count['extra_spaces']} 处")
        print(f"  - 修复错误换行: {self.fix_count['line_breaks']} 处")
        print(f"  - 添加经文标记: {self.fix_count['scripture_marks']} 处")
        print(f"  - 修复嵌套错误: {self.fix_count['nested_errors']} 处")
        print()
        print(f"💾 备份位置: {self.backup_dir}/")
        print()

if __name__ == "__main__":
    fixer = RomansContentFixer()
    fixer.fix_all_chapters()
