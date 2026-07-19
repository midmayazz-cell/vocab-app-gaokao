#!/bin/bash
# 智能背单词 - 完全自动化部署到 GitHub Pages
# 使用方法：复制整个脚本，在终端运行

REPO_NAME="vocab-app"
GITHUB_USER="midmayazz"
PROJECT_DIR="/home/zz/下载/新建文件夹/vocab-app"

echo "======================================"
echo "   智能背单词 - 自动化部署"
echo "======================================"
echo ""

cd "$PROJECT_DIR"

# 1. 初始化 Git
if [ ! -d ".git" ]; then
    echo "🔧 初始化 Git..."
    git init
fi

# 2. 配置 git 用户
git config user.name "midmayazz"
git config user.email "midmayazz@gmail.com"

# 3. 添加所有文件
echo "📦 添加文件..."
git add .

# 4. 提交
echo "💾 提交..."
git commit -m "Initial deploy - $(date '+%Y-%m-%d %H:%M:%S')"

# 5. 创建 main 分支
git branch -M main

# 6. 设置远程仓库（使用 HTTPS）
echo "🔗 设置远程仓库..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/${GITHUB_USER}/${REPO_NAME}.git

echo ""
echo "======================================"
echo "   ⚠️  需要手动操作"
echo "======================================"
echo ""
echo "请在 GitHub 创建仓库："
echo "   1. 访问：https://github.com/new"
echo "   2. Repository name: ${REPO_NAME}"
echo "   3. 不要勾选 README"
echo "   4. 点击 Create repository"
echo ""
read -p "✅ 完成后按回车继续..."

# 7. 推送
echo "🚀 推送到 GitHub..."
git push -u origin main --force

echo ""
echo "======================================"
echo "   ✅ 部署完成！"
echo "======================================"
echo ""
echo "📱 启用 GitHub Pages："
echo "   访问：https://github.com/${GITHUB_USER}/${REPO_NAME}/settings/pages"
echo "   - Source: Deploy from a branch"
echo "   - Branch: main, Folder: /"
echo "   - 点击 Save"
echo ""
echo "🌐 等待 1-2 分钟后访问："
echo "   https://${GITHUB_USER}.github.io/${REPO_NAME}/"
echo ""
echo "📲 手机添加到主屏幕："
echo "   Safari/Chrome → 分享 → 添加到主屏幕"
echo ""
