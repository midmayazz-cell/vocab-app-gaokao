#!/bin/bash
# 智能背单词 - 一键部署到 GitHub Pages

REPO_NAME="vocab-app"
GITHUB_USER="midmayazz"
PROJECT_DIR="/home/zz/下载/新建文件夹/vocab-app"

echo "======================================"
echo "   智能背单词 - 部署到 GitHub Pages"
echo "======================================"
echo ""
echo "📱 仓库：https://github.com/${GITHUB_USER}/${REPO_NAME}"
echo "🌐 上线地址：https://${GITHUB_USER}.github.io/${REPO_NAME}/"
echo ""

cd "$PROJECT_DIR"

# 检查是否已经是 git 仓库
if [ ! -d ".git" ]; then
    echo "🔧 初始化 Git 仓库..."
    git init
fi

# 添加所有文件
echo "📦 添加文件..."
git add .

# 提交
echo "💾 提交更改..."
git commit -m "Deploy to GitHub Pages - $(date '+%Y-%m-%d %H:%M:%S')"

# 检查远程仓库是否存在
if ! git remote | grep -q "origin"; then
    echo "🔗 添加远程仓库..."
    git remote add origin git@github.com:${GITHUB_USER}/${REPO_NAME}.git
fi

# 创建/切换到 main 分支
echo "🔄 切换到 main 分支..."
git branch -M main

# 推送
echo "🚀 推送到 GitHub..."
git push -u origin main --force

echo ""
echo "======================================"
echo "   ✅ 部署完成！"
echo "======================================"
echo ""
echo "📱 下一步操作："
echo "   1. 访问 https://github.com/${GITHUB_USER}/${REPO_NAME}/settings/pages"
echo "   2. Source 选择 'Deploy from a branch'"
echo "   3. Branch 选择 'main'，文件夹 '/'"
echo "   4. 点击 Save"
echo ""
echo "   等待 1-2 分钟后访问："
echo "   🌐 https://${GITHUB_USER}.github.io/${REPO_NAME}/"
echo ""
echo "📲 手机使用："
echo "   1. 用手机浏览器打开上面的链接"
echo "   2. 点击浏览器菜单 '添加到主屏幕'"
echo "   3. 即可像 App 一样使用！"
echo ""
