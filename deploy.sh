#!/bin/bash
# 智能背单词 - 推送并启用 GitHub Pages
# Token 从 .github_token 读取（已加入 .gitignore）

set -e

GITHUB_USER="midmayazz"
REPO_NAME="vocab-app"
PROJECT_DIR="/home/zz/下载/新建文件夹/vocab-app"

cd "$PROJECT_DIR"

# 从文件读取 Token（不暴露在命令行）
if [ ! -f ".github_token" ]; then
  echo "❌ 错误：缺少 .github_token 文件"
  exit 1
fi
TOKEN=$(cat .github_token | tr -d '\n')

echo "======================================"
echo "   智能背单词 - 推送并启用 Pages"
echo "======================================"

# 1. 推送代码
echo "🚀 推送代码到 GitHub..."
git push "https://oauth2:${TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git" main --force 2>&1 | grep -v "http.version" | grep -v "warning:"

echo ""
echo "✅ 代码推送成功！"

# 2. 启用 GitHub Pages
echo ""
echo "🌐 启用 GitHub Pages..."
curl -s -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/${GITHUB_USER}/${REPO_NAME}/pages" \
  -d '{"source":{"branch":"main","path":"/"}}' | jq -r '.html_url // .message'

echo ""
echo "======================================"
echo "   ✅ 全部完成！"
echo "======================================"
echo ""
echo "🌐 等待 1-2 分钟后访问："
echo "   https://${GITHUB_USER}.github.io/${REPO_NAME}/"
echo ""
echo "📲 手机添加到主屏幕："
echo "   Safari/Chrome → 分享 → 添加到主屏幕"
