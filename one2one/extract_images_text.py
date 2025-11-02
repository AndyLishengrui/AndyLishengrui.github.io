#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从一对一手册图片中提取文字内容
"""

from PIL import Image
import pytesseract
import os
import json

def extract_text_from_images(folder_path):
    """从文件夹中的所有图片提取文字"""
    
    # 获取所有图片文件
    image_files = sorted([f for f in os.listdir(folder_path) if f.endswith(('.jpeg', '.jpg', '.png'))])
    
    extracted_data = {}
    
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        print(f"\n处理图片: {image_file}")
        
        try:
            # 打开图片
            img = Image.open(image_path)
            
            # 使用pytesseract进行OCR识别（中文）
            text = pytesseract.image_to_string(img, lang='chi_sim+eng')
            
            # 保存结果
            extracted_data[image_file] = {
                'text': text,
                'cleaned_text': text.strip()
            }
            
            print(f"成功提取文字，长度: {len(text)} 字符")
            print(f"前100字符预览: {text[:100]}")
            
        except Exception as e:
            print(f"处理 {image_file} 时出错: {e}")
            extracted_data[image_file] = {
                'text': '',
                'error': str(e)
            }
    
    return extracted_data

def main():
    folder_path = "/Users/andyshengruilee/Documents/website/web2Lord/one2one/得救20251011"
    
    print("=" * 60)
    print("开始提取图片文字内容...")
    print("=" * 60)
    
    # 提取文字
    extracted_data = extract_text_from_images(folder_path)
    
    # 保存为JSON文件
    output_file = "/Users/andyshengruilee/Documents/website/web2Lord/one2one/extracted_text_得救.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"提取完成！结果已保存到: {output_file}")
    print("=" * 60)
    
    # 打印所有提取的文字
    print("\n完整提取内容：")
    print("=" * 60)
    for image_file, data in sorted(extracted_data.items()):
        print(f"\n【{image_file}】")
        print("-" * 60)
        if 'text' in data:
            print(data['cleaned_text'])
        if 'error' in data:
            print(f"错误: {data['error']}")

if __name__ == "__main__":
    main()
