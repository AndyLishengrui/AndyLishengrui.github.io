#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
罗马书天书八部 - PDF生成器
将16个章节生成为精美的PDF文档
"""

import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Table, TableStyle, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import re

class RomansPDFGenerator:
    def __init__(self):
        self.chapters_dir = "BooksofRoman/chapters"
        self.output_file = "罗马书天书八部_16章完整版.pdf"
        
        # 16个章节标题
        self.chapter_titles = [
            "1. 序言",
            "2. 保罗与福音", 
            "3. 保罗与罗马人",
            "4. 保罗与宣教",
            "5. 外邦人的罪",
            "6. 道德主义者的罪",
            "7. 犹太人的罪",
            "8. 全人类的属灵处境",
            "9. 人如何称义?",
            "10. 称义的结果",
            "11. 圣洁与成圣",
            "12. 成圣与律法",
            "13. 与基督一同受苦得荣耀",
            "14. 永恒的荣耀",
            "15. 圣经中的末世观",
            "16. 基督徒的盼望"
        ]
        
        # 注册中文字体(使用系统字体)
        self.setup_fonts()
        
        # 创建样式
        self.styles = self.create_styles()
    
    def setup_fonts(self):
        """注册中文字体"""
        try:
            # macOS系统字体
            pdfmetrics.registerFont(TTFont('SimSun', '/System/Library/Fonts/STHeiti Light.ttc', subfontIndex=0))
            pdfmetrics.registerFont(TTFont('SimSun-Bold', '/System/Library/Fonts/STHeiti Medium.ttc', subfontIndex=0))
            self.font_name = 'SimSun'
            self.font_name_bold = 'SimSun-Bold'
            print("✓ 使用系统字体: STHeiti")
        except:
            try:
                # 尝试其他常见字体
                pdfmetrics.registerFont(TTFont('SimSun', '/System/Library/Fonts/PingFang.ttc', subfontIndex=0))
                self.font_name = 'SimSun'
                self.font_name_bold = 'SimSun'
                print("✓ 使用系统字体: PingFang")
            except:
                # 使用Helvetica作为后备
                self.font_name = 'Helvetica'
                self.font_name_bold = 'Helvetica-Bold'
                print("⚠️  使用默认字体: Helvetica (中文可能显示异常)")
    
    def create_styles(self):
        """创建文档样式"""
        styles = getSampleStyleSheet()
        
        # 标题样式
        styles.add(ParagraphStyle(
            name='ChineseTitle',
            parent=styles['Title'],
            fontName=self.font_name_bold,
            fontSize=24,
            textColor=HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # 章节标题样式
        styles.add(ParagraphStyle(
            name='ChapterTitle',
            parent=styles['Heading1'],
            fontName=self.font_name_bold,
            fontSize=20,
            textColor=HexColor('#667eea'),
            spaceAfter=20,
            spaceBefore=20,
            alignment=TA_LEFT
        ))
        
        # 主题标题样式
        styles.add(ParagraphStyle(
            name='TopicTitle',
            parent=styles['Heading2'],
            fontName=self.font_name_bold,
            fontSize=16,
            textColor=HexColor('#34495e'),
            spaceAfter=15,
            spaceBefore=15,
            alignment=TA_LEFT
        ))
        
        # 正文样式
        styles.add(ParagraphStyle(
            name='ChineseBody',
            parent=styles['BodyText'],
            fontName=self.font_name,
            fontSize=11,
            textColor=HexColor('#333333'),
            leading=20,
            spaceAfter=10,
            alignment=TA_JUSTIFY,
            firstLineIndent=22  # 首行缩进2个字符
        ))
        
        # 经文块样式
        styles.add(ParagraphStyle(
            name='ScriptureBlock',
            parent=styles['BodyText'],
            fontName=self.font_name,
            fontSize=10,
            textColor=HexColor('#1565c0'),
            leading=18,
            leftIndent=20,
            rightIndent=20,
            spaceAfter=15,
            spaceBefore=10,
            alignment=TA_JUSTIFY,
            backColor=HexColor('#e3f2fd')
        ))
        
        # 内联经文样式
        styles.add(ParagraphStyle(
            name='InlineScripture',
            parent=styles['BodyText'],
            fontName=self.font_name,
            fontSize=11,
            textColor=HexColor('#7b1fa2'),
            backColor=HexColor('#f3e5f5')
        ))
        
        return styles
    
    def extract_topics_from_chapter(self, chapter_content):
        """从章节内容中提取主题"""
        topics = []
        lines = chapter_content.strip().split('\n')
        current_topic = None
        current_content = []
        
        # 主题编号模式
        topic_pattern = re.compile(r'^(\d+)\.\s+(.+)$')
        
        for line in lines:
            match = topic_pattern.match(line.strip())
            
            if match:
                # 保存上一个主题
                if current_topic:
                    topics.append({
                        'number': current_topic['number'],
                        'title': current_topic['title'],
                        'content': '\n'.join(current_content).strip()
                    })
                
                # 开始新主题
                topic_num = match.group(1)
                topic_title = match.group(2).strip()
                current_topic = {
                    'number': topic_num,
                    'title': topic_title
                }
                current_content = []
            else:
                # 累积内容
                if line.strip():
                    current_content.append(line)
        
        # 保存最后一个主题
        if current_topic:
            topics.append({
                'number': current_topic['number'],
                'title': current_topic['title'],
                'content': '\n'.join(current_content).strip()
            })
        
        return topics
    
    def clean_text(self, text):
        """清理文本,移除标记"""
        # 移除经文标记
        text = re.sub(r'\{\{scripture\}\}', '', text)
        text = re.sub(r'\{\{/scripture\}\}', '', text)
        text = re.sub(r'\{\{inline-scripture\}\}', '<font color="#7b1fa2" backColor="#f3e5f5">', text)
        text = re.sub(r'\{\{/inline-scripture\}\}', '</font>', text)
        return text
    
    def is_scripture_line(self, line):
        """判断是否为经文行"""
        patterns = [
            r'^\{\{scripture\}\}',
            r'《.+?》\d+[:：]\d+',
            r'\(.+?书\s*\d+[:：]\d+.*?\)',
            r'^"[^"]{30,}"\s*$'
        ]
        for pattern in patterns:
            if re.search(pattern, line):
                return True
        return False
    
    def process_content(self, content):
        """处理内容,转换为PDF段落"""
        content = self.clean_text(content)
        lines = content.split('\n')
        paragraphs = []
        scripture_buffer = []
        in_scripture = False
        
        for line in lines:
            stripped = line.strip()
            
            if not stripped:
                if in_scripture and scripture_buffer:
                    # 输出经文块
                    scripture_text = ' '.join(scripture_buffer)
                    p = Paragraph(scripture_text, self.styles['ScriptureBlock'])
                    paragraphs.append(p)
                    paragraphs.append(Spacer(1, 0.3*cm))
                    scripture_buffer = []
                    in_scripture = False
                continue
            
            # 检测经文
            if self.is_scripture_line(stripped):
                if not in_scripture:
                    in_scripture = True
                scripture_buffer.append(stripped)
            else:
                # 先输出缓存的经文
                if in_scripture and scripture_buffer:
                    scripture_text = ' '.join(scripture_buffer)
                    p = Paragraph(scripture_text, self.styles['ScriptureBlock'])
                    paragraphs.append(p)
                    paragraphs.append(Spacer(1, 0.3*cm))
                    scripture_buffer = []
                    in_scripture = False
                
                # 输出普通段落
                p = Paragraph(stripped, self.styles['ChineseBody'])
                paragraphs.append(p)
                paragraphs.append(Spacer(1, 0.2*cm))
        
        # 处理最后的经文块
        if scripture_buffer:
            scripture_text = ' '.join(scripture_buffer)
            p = Paragraph(scripture_text, self.styles['ScriptureBlock'])
            paragraphs.append(p)
        
        return paragraphs
    
    def create_cover_page(self):
        """创建封面页"""
        story = []
        
        # 添加大标题
        story.append(Spacer(1, 5*cm))
        title = Paragraph("罗马书天书八部", self.styles['ChineseTitle'])
        story.append(title)
        
        # 副标题
        subtitle_style = ParagraphStyle(
            name='Subtitle',
            parent=self.styles['ChineseBody'],
            fontSize=16,
            textColor=HexColor('#7f8c8d'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        subtitle = Paragraph("16章完整版 · 系统性圣经研读", subtitle_style)
        story.append(subtitle)
        
        story.append(Spacer(1, 2*cm))
        
        # 统计信息
        info_style = ParagraphStyle(
            name='Info',
            parent=self.styles['ChineseBody'],
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=10
        )
        
        story.append(Paragraph("16个章节", info_style))
        story.append(Paragraph("深度解析 · 灵修材料", info_style))
        
        story.append(Spacer(1, 3*cm))
        
        # 生成日期
        date_text = f"生成日期: {datetime.now().strftime('%Y年%m月%d日')}"
        date_para = Paragraph(date_text, info_style)
        story.append(date_para)
        
        # 换页
        story.append(PageBreak())
        
        return story
    
    def create_table_of_contents(self, chapter_data):
        """创建目录页"""
        story = []
        
        # 目录标题
        toc_title = Paragraph("目录", self.styles['ChapterTitle'])
        story.append(toc_title)
        story.append(Spacer(1, 0.5*cm))
        
        # 目录内容
        toc_style = ParagraphStyle(
            name='TOC',
            parent=self.styles['ChineseBody'],
            fontSize=12,
            spaceAfter=8,
            leftIndent=10
        )
        
        for i, title in enumerate(self.chapter_titles, 1):
            topic_count = len(chapter_data.get(i, {}).get('topics', []))
            toc_line = f"{title} ({topic_count}个主题)"
            p = Paragraph(toc_line, toc_style)
            story.append(p)
        
        story.append(PageBreak())
        
        return story
    
    def generate_pdf(self):
        """生成PDF文档"""
        print("=" * 60)
        print("开始生成PDF文档")
        print("=" * 60)
        print()
        
        # 创建PDF文档
        doc = SimpleDocTemplate(
            self.output_file,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        story = []
        chapter_data = {}
        
        # 首先收集所有章节数据
        print("📖 读取章节内容...")
        for chapter_num in range(1, 17):
            chapter_file = os.path.join(self.chapters_dir, f"chapter_{chapter_num:02d}.txt")
            
            if not os.path.exists(chapter_file):
                print(f"⚠️  跳过: {chapter_file} (不存在)")
                continue
            
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            topics = self.extract_topics_from_chapter(content)
            chapter_data[chapter_num] = {
                'title': self.chapter_titles[chapter_num - 1],
                'topics': topics,
                'content': content
            }
            
            print(f"  ✓ 章节 {chapter_num}: {self.chapter_titles[chapter_num - 1]} ({len(topics)}个主题)")
        
        print()
        print("📝 生成PDF页面...")
        
        # 创建封面
        print("  ✓ 封面页")
        story.extend(self.create_cover_page())
        
        # 创建目录
        print("  ✓ 目录页")
        story.extend(self.create_table_of_contents(chapter_data))
        
        # 处理每个章节
        for chapter_num in range(1, 17):
            if chapter_num not in chapter_data:
                continue
            
            data = chapter_data[chapter_num]
            chapter_title = data['title']
            topics = data['topics']
            
            print(f"  ✓ 章节 {chapter_num}: {chapter_title}")
            
            # 章节标题
            ch_title = Paragraph(f"第{chapter_num}章: {chapter_title}", self.styles['ChapterTitle'])
            story.append(ch_title)
            story.append(Spacer(1, 0.5*cm))
            
            # 处理每个主题
            for topic in topics:
                # 主题标题
                topic_title = Paragraph(f"{topic['number']}. {topic['title']}", self.styles['TopicTitle'])
                story.append(topic_title)
                story.append(Spacer(1, 0.3*cm))
                
                # 主题内容
                content_paras = self.process_content(topic['content'])
                story.extend(content_paras)
                
                story.append(Spacer(1, 0.5*cm))
            
            # 章节结束,换页
            story.append(PageBreak())
        
        print()
        print("💾 正在生成PDF文件...")
        
        # 构建PDF
        doc.build(story)
        
        # 获取文件大小
        file_size = os.path.getsize(self.output_file) / (1024 * 1024)
        
        print()
        print("=" * 60)
        print("✅ PDF生成完成!")
        print("=" * 60)
        print(f"📄 文件名: {self.output_file}")
        print(f"📊 文件大小: {file_size:.2f} MB")
        print(f"📖 章节数: 16")
        print(f"📝 主题总数: {sum(len(d['topics']) for d in chapter_data.values())}")
        print(f"📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

if __name__ == "__main__":
    generator = RomansPDFGenerator()
    generator.generate_pdf()
