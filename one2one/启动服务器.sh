#!/bin/bash
# 一对一课程 - 启动本地服务器并打开浏览器

echo "🚀 启动本地HTTP服务器..."
cd "$(dirname "$0")"

# 检查8765端口是否已被占用
if lsof -Pi :8765 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ 服务器已在运行 (端口 8765)"
else
    echo "🔧 启动新服务器..."
    python3 -m http.server 8765 > /dev/null 2>&1 &
    echo "✅ 服务器已启动 (端口 8765)"
    sleep 1
fi

echo ""
echo "📖 课程访问地址："
echo "   第1课第1节: http://localhost:8765/one2one_C1_S1.html"
echo "   前言: http://localhost:8765/preface.html"
echo "   五步骤: http://localhost:8765/steps.html"
echo ""
echo "🌐 正在打开浏览器..."
open "http://localhost:8765/one2one_C1_S1.html"

echo ""
echo "⚠️  重要提示："
echo "   - 不要直接双击HTML文件打开"
echo "   - 必须通过 http://localhost:8765 访问"
echo "   - 按 Ctrl+C 停止服务器"
echo ""
