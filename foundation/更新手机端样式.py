#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import re

def update_mobile_styles():
    """为所有foundation HTML文件添加手机端填空视觉优化"""
    
    # 获取foundation目录下所有HTML文件
    html_files = glob.glob('foundation_*.html')
    
    updated_files = []
    
    # 要添加的手机端样式
    mobile_enhancement = """
            /* 优化手机端填空的视觉呈现 */
            .answers-area {
                margin-left: 10px; /* 从30px减少到10px */
            }
            
            .reference-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 8px;
            }
            
            .hint-buttons {
                width: 100%;
                justify-content: flex-start;
            }"""
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经包含优化样式
            if "优化手机端填空的视觉呈现" in content:
                print(f"- 样式已存在: {file_path}")
                continue
                
            # 保存原始内容
            original_content = content
            
            # 查找@media (max-width: 768px) 块的结束位置
            media_pattern = r'(@media \(max-width: 768px\) \{[^}]*?)(\s*})'
            
            def replace_media_block(match):
                media_block = match.group(1)
                closing_brace = match.group(2)
                
                # 如果媒体查询块还没有包含我们的优化，就添加
                if "优化手机端填空的视觉呈现" not in media_block:
                    return media_block + mobile_enhancement + closing_brace
                else:
                    return match.group(0)  # 返回原始内容
            
            # 替换媒体查询块
            content = re.sub(media_pattern, replace_media_block, content, flags=re.DOTALL)
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_files.append(file_path)
                print(f"✓ 已更新手机端样式: {file_path}")
            else:
                print(f"- 无需更新: {file_path}")
                
        except Exception as e:
            print(f"✗ 处理文件 {file_path} 时出错: {e}")
    
    print(f"\n手机端样式更新完成！共更新了 {len(updated_files)} 个文件。")
    if updated_files:
        print("更新的文件:")
        for file in updated_files:
            print(f"  - {file}")

if __name__ == "__main__":
    print("正在更新手机端填空样式...")
    update_mobile_styles()