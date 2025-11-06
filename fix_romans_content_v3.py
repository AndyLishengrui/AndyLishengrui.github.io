#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
罗马书内容修复脚本 V3
修复问题:
1. 恢复被错误取消的段落换行
2. 简化inline-scripture标记,只标记引用不标记内容
3. 保留整段经文的scripture样式
4. 分离前言/引言为独立章节
"""

import re
import os
import shutil

class RomansContentFixerV3:
    def __init__(self):
        self.chapters_dir = "BooksofRoman/chapters_correct"
        self.output_dir = "BooksofRoman/chapters_fixed"
        
    def fix_paragraphs(self, text):
        """恢复正确的段落换行"""
        lines = text.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # 保留空行
            if not stripped:
                fixed_lines.append('')
                continue
            
            # 保留主题标题(数字开头)
            if re.match(r'^\d+\.\s+', stripped):
                # 主题标题前加空行(如果前一行不是空行)
                if fixed_lines and fixed_lines[-1].strip():
                    fixed_lines.append('')
                fixed_lines.append(line)
                continue
            
            # 保留标记行
            if '{{' in stripped:
                fixed_lines.append(line)
                continue
            
            # 判断是否需要换行
            # 换行条件: 以句号、问号、感叹号等结束
            needs_break = bool(re.search(r'[。！？]$', stripped))
            
            # 或者: 下一行是新段落的开始
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # 下一行是标题、空行、或者首字母缩进
                if (not next_line or 
                    re.match(r'^\d+\.\s+', next_line) or
                    next_line.startswith('{{') or
                    (len(stripped) < 60 and len(next_line) > 20)):  # 当前行较短,下一行是新段落
                    needs_break = True
            
            fixed_lines.append(line)
            if needs_break and i + 1 < len(lines) and lines[i + 1].strip():
                # 段落之间加空行
                fixed_lines.append('')
        
        return '\n'.join(fixed_lines)
    
    def fix_scripture_marks(self, text):
        """
        修复经文标记:
        1. 只标记引用文本,不标记经文内容
        2. 保留整段经文的{{scripture}}标记
        """
        lines = text.split('\n')
        fixed_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # 情况1: 整段经文({{scripture}}...{{/scripture}})
            if '{{scripture}}' in stripped:
                # 保持原样,这种标记很好
                fixed_lines.append(line)
                continue
            
            # 情况2: 段落中的经文引用
            # 移除所有 inline-scripture 标记
            line = re.sub(r'\{\{inline-scripture\}\}', '', line)
            line = re.sub(r'\{\{/inline-scripture\}\}', '', line)
            
            # 只标记引用部分: (书卷名 章:节)
            # 匹配模式: (书名 数字:数字)
            def mark_reference(match):
                return f'{{{{scripture-ref}}}}{match.group(0)}{{{{/scripture-ref}}}}'
            
            # 匹配经文引用
            scripture_ref_pattern = r'\((?:罗马书|创世[记纪]|出埃及记|利未记|民数记|申命记|约书亚记|士师记|路得记|撒母耳记[上下]|列王[记纪][上下]|历代志[上下]|以斯拉记|尼希米记|以斯帖记|约伯记|诗篇|箴言|传道书|雅歌|以赛亚书|耶利米书|耶利米哀歌|以西结书|但以理书|何西阿书|约珥书|阿摩司书|俄巴底亚书|约拿书|弥迦书|那鸿书|哈巴谷书|西番雅书|哈该书|撒迦利亚书|玛拉基书|马太福音|马可福音|路加福音|约翰福音|使徒行传|哥林多前书|哥林多后书|加拉太书|以弗所书|腓立比书|歌罗西书|帖撒罗尼迦前书|帖撒罗尼迦后书|提摩太前书|提摩太后书|提多书|腓利门书|希伯来书|雅各书|彼得前书|彼得后书|约翰一书|约翰二书|约翰三书|犹大书|启示录)\s*\d+[:：]\d+(?:[-—–]\d+)?(?:[,，]\s*\d+[:：]\d+(?:[-—–]\d+)?)*\)'
            
            line = re.sub(scripture_ref_pattern, mark_reference, line)
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def extract_preface(self, chapter1_content):
        """
        从第1章中提取前言/引言部分
        返回: (前言内容, 剩余的第1章内容)
        """
        lines = chapter1_content.split('\n')
        
        # 找到第一个罗马书主题(通常从"1. "开始)
        # 前言通常在文件开头,在第一个编号主题之前
        first_topic_idx = -1
        
        for i, line in enumerate(lines):
            # 找到第一个数字开头的主题(如 "1. 主题")
            if re.match(r'^1\.\s+', line.strip()):
                first_topic_idx = i
                break
        
        if first_topic_idx > 10:  # 如果前面有足够内容,说明有前言
            preface = '\n'.join(lines[:first_topic_idx])
            remaining = '\n'.join(lines[first_topic_idx:])
            
            # 给前言添加一个标题
            preface = "0. 前言与引言\n\n" + preface
            
            return preface, remaining
        else:
            # 没有明显的前言,返回空
            return None, chapter1_content
    
    def process_chapter(self, chapter_num):
        """处理单个章节"""
        input_file = os.path.join(self.chapters_dir, f'chapter_{chapter_num:02d}.txt')
        
        if not os.path.exists(input_file):
            return None
        
        # 读取内容
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 应用修复
        # 1. 修复段落
        content = self.fix_paragraphs(content)
        
        # 2. 修复经文标记
        content = self.fix_scripture_marks(content)
        
        return content
    
    def process_all_chapters(self):
        """处理所有章节"""
        print("=" * 60)
        print("罗马书内容修复 V3")
        print("=" * 60)
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 处理第1章,提取前言
        print("\n处理第1章并提取前言...")
        chapter1_content = self.process_chapter(1)
        
        if chapter1_content:
            preface, chapter1_content = self.extract_preface(chapter1_content)
            
            # 保存前言为 chapter_00.txt
            if preface:
                preface_file = os.path.join(self.output_dir, 'chapter_00.txt')
                with open(preface_file, 'w', encoding='utf-8') as f:
                    f.write(preface)
                print(f"✓ 提取前言保存到: chapter_00.txt")
            
            # 保存修复后的第1章
            output_file = os.path.join(self.output_dir, 'chapter_01.txt')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(chapter1_content)
            print(f"✓ 处理第1章: chapter_01.txt")
        
        # 处理第2-16章
        for i in range(2, 17):
            print(f"处理第{i}章...", end=' ')
            content = self.process_chapter(i)
            
            if content:
                output_file = os.path.join(self.output_dir, f'chapter_{i:02d}.txt')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓")
            else:
                print(f"✗ 文件不存在")
        
        print("\n" + "=" * 60)
        print("✓ 修复完成!")
        print(f"✓ 输出目录: {self.output_dir}")
        print("=" * 60)

if __name__ == '__main__':
    fixer = RomansContentFixerV3()
    fixer.process_all_chapters()
