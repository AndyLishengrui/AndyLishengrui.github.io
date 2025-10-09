#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bible Study Server with Verse Editing API
圣经学习服务器 - 支持经文编辑功能
"""

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.parse

class BibleServerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        """处理POST请求 - 用于保存经文编辑"""
        if self.path == '/api/save-verse':
            self.handle_save_verse()
        else:
            self.send_error(404, "Not Found")
    
    def handle_save_verse(self):
        """处理经文保存请求"""
        try:
            # 读取请求数据
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            book = data['book']
            chapter = int(data['chapter'])
            verse = int(data['verse'])
            new_text = data['text']
            
            print(f"保存经文: {book} {chapter}:{verse} -> {new_text[:50]}...")
            
            # 读取对应的JSON文件
            json_file = f"data/{book}.json"
            if not os.path.exists(json_file):
                self.send_error(404, f"Book file not found: {json_file}")
                return
            
            with open(json_file, 'r', encoding='utf-8') as f:
                book_data = json.load(f)
            
            # 查找并更新对应的经文
            updated = False
            for verse_data in book_data.get('verses', []):
                if verse_data['chapter'] == chapter and verse_data['verse'] == verse:
                    verse_data['text'] = new_text
                    verse_data['zh'] = new_text  # 同时更新zh字段
                    updated = True
                    break
            
            if not updated:
                # 如果没找到，添加新的经文
                book_data.setdefault('verses', []).append({
                    'chapter': chapter,
                    'verse': verse,
                    'text': new_text,
                    'zh': new_text
                })
            
            # 保存回文件
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(book_data, f, ensure_ascii=False, indent=2)
            
            # 创建备份
            backup_file = f"backup_original/data/{book}_{chapter}_{verse}_edited.json"
            os.makedirs(os.path.dirname(backup_file), exist_ok=True)
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'book': book,
                    'chapter': chapter,
                    'verse': verse,
                    'old_text': data.get('old_text', ''),
                    'new_text': new_text,
                    'timestamp': __import__('datetime').datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            
            # 返回成功响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': True,
                'message': f'经文 {book} {chapter}:{verse} 保存成功'
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
            print(f"✅ 经文保存成功: {book} {chapter}:{verse}")
            
        except Exception as e:
            print(f"❌ 保存经文失败: {str(e)}")
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def do_OPTIONS(self):
        """处理预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def end_headers(self):
        """添加CORS头"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def run_server(port=8001):
    """运行服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, BibleServerHandler)
    
    print(f"🌟 圣经学习服务器启动成功！")
    print(f"📖 访问地址: http://localhost:{port}")
    print(f"✏️  支持经文在线编辑功能")
    print(f"🔧 使用 Ctrl+C 停止服务器")
    print("-" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n服务器已停止")
        httpd.shutdown()

if __name__ == '__main__':
    run_server()