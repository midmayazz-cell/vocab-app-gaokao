#!/bin/bash
# 智能背单词 - 一键启动服务脚本

PORT=8000
DIR="/home/zz/下载/新建文件夹/vocab-app"

echo "======================================"
echo "   智能背单词 - 服务端启动脚本"
echo "======================================"
echo ""

# 获取本机 IP
LOCAL_IP=$(hostname -I | awk '{print $1}')

echo "📱 词库目录：$DIR"
echo "🌐 本地访问：http://localhost:$PORT"
echo "📲 手机访问：http://$LOCAL_IP:$PORT"
echo ""
echo "⚠️  注意："
echo "   - HTTP 模式无法使用 PWA 离线功能"
echo "   - 手机和电脑必须在同一 WiFi"
echo "   - 按 Ctrl+C 停止服务"
echo ""
echo "正在启动服务..."
echo ""

cd "$DIR"

# 检查 Python
if command -v python3 &> /dev/null; then
    echo "✅ 使用 Python3 HTTP 服务器"
    python3 -m http.server $PORT --bind 0.0.0.0
elif command -v python &> /dev/null; then
    echo "✅ 使用 Python HTTP 服务器"
    python -m SimpleHTTPServer $PORT
else
    echo "❌ 错误：需要 Python 环境"
    exit 1
fi
