# 智能背单词 - 手机端使用指南

## 📱 方案一：本地 HTTPS 服务（推荐）

### 使用 Node.js `serve`（最简单）

```bash
# 1. 安装 serve（首次需要）
npm install -g serve

# 2. 进入项目目录
cd /home/zz/下载/新建文件夹/vocab-app

# 3. 启动 HTTPS 服务
serve --ssl-cert <(openssl req -newkey rsa:2048 -nodes -keyout /tmp/key.pem -x509 -days 365 -out /tmp/cert.pem -subj "/CN=localhost") --ssl-key /tmp/key.pem -l 3000

# 或者不使用 HTTPS（仅限同一 WiFi）
serve -l 3000
```

### 使用 Python HTTPS 服务

```bash
# 1. 生成自签名证书
openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem -subj "/CN=localhost"

# 2. 启动 HTTPS 服务
python3 -m http.server --bind 0.0.0.0 8000 --certfile cert.pem --keyfile key.pem
```

### 使用 mkcert（最佳体验）

```bash
# 1. 安装 mkcert
wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64
chmod +x mkcert-v1.4.4-linux-amd64
sudo mv mkcert-v1.4.4-linux-amd64 /usr/local/bin/mkcert

# 2. 安装根证书
mkcert -install

# 3. 为本地 IP 生成证书
mkcert $(hostname -I | awk '{print $1}') localhost 127.0.0.1

# 4. 使用 Caddy 或 nginx 启动 HTTPS 服务
```

---

## 📱 方案二：部署到 GitHub Pages（免费，推荐生产用）

### 步骤：

1. **创建 GitHub 仓库**
   ```bash
   cd /home/zz/下载/新建文件夹/vocab-app
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **推送到 GitHub**
   ```bash
   git remote add origin https://github.com/你的用户名/vocab-app.git
   git branch -M main
   git push -u origin main
   ```

3. **启用 GitHub Pages**
   - 进入仓库 Settings → Pages
   - Source 选择 `main` 分支
   - 保存后获得 `https://你的用户名.github.io/vocab-app`

4. **手机访问**
   - 用手机浏览器打开上面的 URL
   - 点击浏览器菜单"添加到主屏幕"
   - 即可像 App 一样使用

---

## 📱 方案三：Vercel / Netlify 部署（最简单）

### Vercel 部署：

1. 访问 [vercel.com](https://vercel.com)
2. 用 GitHub 账号登录
3. Import 你的仓库
4. 自动获得 `https://xxx.vercel.app` 域名

### Netlify 部署：

1. 访问 [netlify.com](https://netlify.com)
2. Drag & Drop `vocab-app` 文件夹
3. 自动获得 `https://xxx.netlify.app` 域名

---

## 📱 方案四：局域网 HTTP 访问（临时测试）

```bash
# 1. 查看本机 IP
ip addr show | grep "inet " | grep -v 127.0.0.1
# 假设输出：inet 192.168.1.100

# 2. 启动 HTTP 服务
python3 -m http.server 8000 --bind 0.0.0.0

# 3. 手机访问
# 手机浏览器打开：http://192.168.1.100:8000
```

**注意：**
- 电脑和手机必须在**同一 WiFi**
- HTTP 无法使用 PWA 功能（离线、推送等）
- 仅用于临时测试

---

## 📱 iOS Safari 添加到主屏幕

1. Safari 打开网站
2. 点击底部分享按钮（方框 + 向上箭头）
3. 滚动找到"添加到主屏幕"
4. 点击右上角"添加"

## 📱 Android Chrome 添加到主屏幕

1. Chrome 打开网站
2. 点击右上角三个点
3. 点击"添加到主屏幕"
4. 确认添加

---

## 🔧 常见问题

### Q: 手机访问显示空白？
A: 检查：
1. 电脑防火墙是否开放端口
2. 服务是否绑定 `0.0.0.0` 而非 `127.0.0.1`
3. 手机和电脑是否在同一网络

### Q: PWA 功能不可用？
A: PWA 需要 HTTPS（localhost 除外），请使用方案一、二、三。

### Q: 数据会丢失吗？
A: 数据存储在浏览器 LocalStorage，清除缓存会丢失。建议定期导出备份。

---

## 🚀 快速开始（最快方式）

```bash
# 如果你有 npm
npx serve /home/zz/下载/新建文件夹/vocab-app -l 3000

# 然后用手机访问 http://你的电脑IP:3000
```
