# 智能背单词 — 项目文档

> 基于艾宾浩斯记忆曲线（SM-2 算法）的高考词汇学习 PWA 应用  
> 单文件架构，无需后端，部署到 GitHub Pages，手机即开即用

---

## 1. 版本信息

| 项 | 值 |
|---|---|
| 版本号 | v1.0 |
| 最后更新 | 2026-07-19 |
| 核心文件 | `index.html`（单文件应用） |
| 词库 | 2666 个高考 3500 词汇 |
| 架构类型 | PWA（Progressive Web App） |
| 离线支持 | Service Worker |

---

## 2. GitHub 部署信息

### 2.1 仓库

| 项 | 值 |
|---|---|
| GitHub 用户名（实际） | `midmayazz-cell` |
| GitHub 邮箱 | `midmayazz@gmail.com` |
| 仓库名 | `vocab-app-gaokao` |
| 远程 URL（HTTPS） | `https://github.com/midmayazz-cell/vocab-app-gaokao.git` |
| 远程 URL（SSH） | `git@github.com:midmayazz-cell/vocab-app-gaokao.git` |
| 上线地址 | `https://midmayazz-cell.github.io/vocab-app-gaokao/` |
| 默认分支 | `main` |

### 2.2 推送方式（SSH，推荐）

本机已配置 SSH 密钥，推送时不需要任何密码或 token。

```bash
cd /home/zz/下载/新建文件夹/vocab-app

# 查看状态
git status

# 添加文件
git add index.html

# 提交
git commit -m "描述修改内容"

# 推送（SSH 无密码）
git push origin main
```

SSH 公钥已添加到 GitHub 账号（Key 名称：`G1-Sniper-B6`）。

### 2.3 初次 clone / 重新配置 remote

```bash
# SSH 方式
git clone git@github.com:midmayazz-cell/vocab-app-gaokao.git

# 如果 remote 不对，手动改
git remote set-url origin git@github.com:midmayazz-cell/vocab-app-gaokao.git
```

### 2.4 启用 GitHub Pages

```bash
curl -s -X POST \
  -H "Authorization: Bearer 你的TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/midmayazz-cell/vocab-app-gaokao/pages \
  -d '{"source":{"branch":"main","path":"/"}}'
```

---

## 3. 项目文件结构

```
vocab-app/
├── index.html              ← 主应用（单文件，约 350KB）
├── manifest.json           ← PWA 清单
├── sw.js                   ← Service Worker（离线缓存）
├── word-data.json          ← 词库原始数据（541KB）
├── assets/
│   └── sounds/             ← 击杀音效 mp3 目录
├── .gitignore              ← git 忽略规则
├── icon-192.png            ← PWA 图标 192x192
├── icon-512.png            ← PWA 图标 512x512
├── README.md               ← 使用指南
├── PROJECT.md               ← 项目文档（本文件）
├── TASKS.md                ← 修复任务清单
├── start-server.sh         ← 本地 HTTP 启动脚本
├── .claude/                ← Claude 配置目录
├── *测试截图.png           ← 自动化测试截图
├── vocab_app_tester.py     ← 自动化测试脚本
├── vocab_deep_test.py      ← 深度测试脚本
├── browser_automation.py   ← 浏览器自动化
└── fix_task04.py / task*.py ← 辅助修复脚本
```

---

## 4. 现有功能

### 4.1 核心功能

| 功能 | 描述 | 状态 |
|------|------|------|
| **学习模式** | 卡片式学习，隐藏释义，点击显示 | ✅ |
| **默写模式** | 看中文拼写英文，30 秒限时 | ✅ |
| **词库浏览** | 分页浏览 2666 个单词，分类筛选 | ✅ |
| **设置** | 发音开关、每日目标数、复习上限 | ✅ |
| **首页统计** | 学习进度、已掌握数、今日待复习、难点词数、连续天数 | ✅ |
| **发音** | 点击单词自动朗读（Web Speech API） | ✅ |

### 4.2 SRS 记忆算法（SM-2）

| 参数 | 值 | 说明 |
|------|----|------|
| `EBBINGHAUS_EASE_FACTOR` | 2.5 | 初始记忆难度系数 |
| `EBBINGHAUS_MIN_EASE` | 1.3 | 最小难度系数 |
| `EBBINGHAUS_QUALITY_THRESHOLD` | 3 | 记忆质量阈值（≥3 算记住） |
| `EBBINGHAUS_MAX_INTERVAL` | 1 年 | 最大复习间隔 |

**算法逻辑：**
- **评分 ≥ 3**（记住）：增加重复次数，按 ease factor 计算下次间隔
- **评分 < 3**（没记住）：重置重复次数为 0，明天必须复习
- **动态调整**：每次正确回答微调 ease factor

**间隔计算：**
- 第 1 次记住 → 1 天后复习
- 第 2 次记住 → 6 天后复习
- 第 3+ 次记住 → `repetitions * easeFactor` 天后复习
- 答错 → 明天复习

### 4.3 学习选词策略

```
每天学习目标（设为 N）
├── 80% ← [难点词 + 高频词]
│   • wrongCount ≥ 3 或 ⭐ 星标的词
│   • 词库前 2000 个高考核心词汇
└── 20% ← [普通词]
```

### 4.4 难记词系统

| 特性 | 说明 |
|------|------|
| 自动标记 | wrongCount ≥ 3 自动标记为 🔥 难点词 |
| 手动星标 | 学习卡片上点击 ⭐ 按钮手动标记 |
| 首页统计 | 首页显示难点词数量 |
| 词库标识 | 词库列表中🔥和⭐标识 |
| 复习入口 | 首页"复习难点词"按钮 |
| 复习队列 | 复习时从默写模式和学习模式优先出现 |

### 4.5 王者击杀音效系统

**mp3 文件映射规则：**

| 连对数 | 文件名 | 击杀文本 | 说明 |
|--------|--------|---------|------|
| 1 | `first_blood.mp3` | First Blood | 初始首杀 |
| 2 | `double_kill.mp3` | Double Kill | 双杀 |
| 3 | `triple_kill.mp3` | Triple Kill | 三杀 |
| 4 | `quadra_kill.mp3` | Quadra Kill | 四杀 |
| 5 | `penta_kill.mp3` | Penta Kill | 五杀 |
| 6-10 | `godlike.mp3` | Godlike | 同上 |
| 11+ | `legendary.mp3` | Legendary | 同上 |
| **全对** | **`ace.mp3`** | Ace | 默写总结页延迟 1.2s 播放 |

**音效放置路径：** `assets/sounds/`  
**降级策略：** 找不到 mp3 时自动降级为 TTS 英语语音播报

### 4.6 默写模式

| 功能 | 说明 |
|------|------|
| 队列来源 | 今天学的 + 难点词 + 遗忘曲线待复习 |
| 限时 | 每题 30 秒倒计时 |
| 空输入处理 | 视为错误，显示正确答案，1.5s 后自动下一题 |
| 释义显示 | 只显示 `\|` 之前的中文部分，隐藏英文词组 |
| 正确反馈 | 激励文案 + 击杀音效 + 震动（移动端） |

### 4.7 默写总结

| 项目 | 说明 |
|------|------|
| 连对排序 | 倔强青铜(3) → 秩序白银(5) → 华丽黄金(7) → 至尊星耀(10) → 永恒钻石(15) → 最强王者(20) |
| 统计 | 正确数、错误数、最佳连对纪录 |
| 错误列表 | 显示需要复习的单词 |
| 全对彩蛋 | 全对时播放 ace.mp3 |

---

## 5. 踩坑记录

### B001 — 释义数据错误
- **问题**：多个基础词汇释义完全错误（use→"美国"、gold→"去" 等）
- **原因**：词库数据源处理有误
- **修复**：已逐条修正
- **状态**：✅ 已修复

### B002 — 默写模式数据显示为空
- **问题**：默写模式下中文释义、音标、词性标注全部为空
- **修复**：修正 `initDictation()` 函数，确保数据正确传递
- **状态**：✅ 已修复

### B003 — 源文件信息泄露
- **问题**：释义包含"（来自英语学习资料_edited2.docx）"等来源信息
- **修复**：全文替换清理
- **状态**：✅ 已修复

### B004 — "高考常见词"占位符
- **问题**：约 30+ 个单词显示 "v.高考常见词" 而非实际释义
- **修复**：补充完整释义
- **状态**：✅ 已修复

### B005 — 释义点击显示功能失效
- **问题**：点击模糊释义后 CSS 类 `revealed` 未被正确添加
- **删除**：已修复 `revealMeaning()` 函数
- **状态**：✅ 已修复

### B006 — 词库分页加载
- **问题**：一次性加载 2666 个单词导致性能问题
- **修复**：实现分页，每页 50 个
- **状态**：✅ 已修复

### B007 — 导航栏 active 状态
- **问题**：切换页面后导航项 active 状态未正确更新
- **修复**：修正 `switchPage()` 函数
- **状态**：✅ 已修复

### B008 — 默写空输入死锁
- **问题**：不输入单词点确认，计时器停止且无法继续
- **原因**：`handleDictationSubmit()` 中 `stopDictationTimer()` 后 `return`，没有重启计时器
- **修复**：空输入视为错误，显示答案后自动进入下一题
- **状态**：✅ 已修复

### B009 — 艾宾浩斯算法过于简单
- **问题**：旧算法固定 7 个间隔段，简单加减等级，没有 ease factor
- **修复**：实现完整 SM-2 算法（ease factor + 动态间隔）
- **状态**：✅ 已修复

### B010 — GitHub 推送认证失败
- **问题**：2021 年后 GitHub 禁用密码认证
- **解决**：使用 Personal Access Token 替代密码
- **TLS 警告**：`unknown value given to http.version: 'TLSv1.2'` — 不影响功能，可忽略
- **状态**：⚠️ 需使用 Token 推送

### B011 — GitHub Pages 部署
- **问题**：`midmayazz` 用户名不存在，实际是 `midmayazz-cell`
- **解决**：仓库地址改为 `https://github.com/midmayazz-cell/vocab-app-gaokao.git`
- **状态**：✅ 已解决

### B012 — 音效播放冲突
- **问题**：TTS 语音和背景和弦同时播放，导致电子音覆盖语音
- **解决**：去掉背景和弦，纯 TTS 语音；或者放 mp3 文件覆盖
- **状态**：✅ 已解决

### B013 — SSH 推送被全局配置拦截
- **问题**：`git remote` 设为 SSH 后仍然走 HTTPS，提示 `could not read Username`
- **原因**：全局 git 配置有 `url.https://github.com/.insteadof=git@github.com:`，把 SSH URL 自动转回 HTTPS
- **修复**：`git config --global --unset url.https://github.com/.insteadof`
- **状态**：✅ 已修复

---

## 6. Git 提交历史

```
d987fef  2026-07-19  添加王者击杀音效mp3 7个
b9a0a8d  2026-07-19  击杀音效：6-10连对godlike, 11+legendary, 全对ace
7d36bf8  2026-07-19  击杀音效支持mp3文件，自动降级TTS
95f6853  2026-07-19  王者击杀真人语音播报 + SM-2算法 + 难记词追踪
7a0323f  2026-07-19  Add deploy script and gitignore
df2c7a9  2026-07-19  Initial deploy
```

### Git 配置

```bash
git config user.name  = "midmayazz"
git config user.email = "midmayazz@gmail.com"
```

---

## 7. 开发维护指南

### 7.1 修改后提交流程

```bash
cd /home/zz/下载/新建文件夹/vocab-app

# 1. 查看修改
git status
git diff

# 2. 添加文件
git add <file1> <file2>

# 3. 提交
git commit -m "描述修改内容"

# 4. 推送到 GitHub（SSH 无密码）
git push origin main
```

### 7.2 本地启动测试

```bash
cd /home/zz/下载/新建文件夹/vocab-app
python3 -m http.server 8000 --bind 0.0.0.0
# 手机访问：http://电脑IP:8000
```

### 7.3 添加击杀音效

下载 mp3 文件放入 `assets/sounds/` 目录：

```
assets/sounds/
├── first_blood.mp3
├── double_kill.mp3
├── triple_kill.mp3
├── quadra_kill.mp3
├── penta_kill.mp3
├── godlike.mp3      ← 6-10 连对
├── legendary.mp3    ← 11+ 连对
└── ace.mp3           ← 全对
```

### 7.4 修改词库

词库数据在 `index.html` 的 `WORD_DATABASE` 数组中，格式：
```javascript
{word:"单词", phonetic:"音标", meaning:"释义", pos:"词性", example:"例句", category:"分类"}
```

### 7.5 重要安全提醒

- **Token 不能提交到公开仓库** — `.gitignore` 已排除 `.github_token`
- **推送后立即清除 remote URL 中的 Token**
- 修改 `sw.js` 后需要更新 `CACHE_NAME` 版本号，否则用户浏览器不更新缓存

---

## 8. 关键技术参数

### 8.1 学习参数

| 参数 | 默认值 | 配置位置 |
|------|--------|---------|
| 每日新词目标 | 15 | 设置页 / `appState.dailyGoal` |
| 每日复习上限 | 50 | 设置页 / `appState.dailyReviewLimit` |
| 墨写限时 | 30 秒 | `DICTATION_TIME_LIMIT` |
| 默写队列上限 | 20 | `startDictation()` 中的 `.slice(0, 20)` |
| 难点词阈值 | wrongCount ≥ 3 | `DIFFICULT_THRESHOLD` |
| 高频词范围 | 词库前 2000 个 | `startLearning()` 中的 `WORD_DATABASE.indexOf(w) < 2000` |

### 8.2 PWA 配置

| 项 | 值 |
|---|---|
| App 名称 | 智能背单词 |
| 主题色 | `#007AFF` |
| 背景色 | `#F2F2F7` |
| 图标 | `icon-192.png`, `icon-512.png` |
| Service Worker | `sw.js`（缓存 `/`, `/index.html`, `/manifest.json`） |

---

*文档生成于 2026-07-19，由 Claude Code 自动维护*
