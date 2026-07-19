#!/usr/bin/env python3
"""Task-06: 实现词库分页加载"""

with open('/home/zz/下载/新建文件夹/vocab-app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 添加分页全局变量
old_let = "let currentCategory = 'all';"
new_let = """let currentCategory = 'all';
let currentPage = 0;
const pageSize = 50;
let filteredWords = [];"""

if old_let in content:
    content = content.replace(old_let, new_let, 1)
    print("✓ 添加分页全局变量")

# 2. 修改 renderWordList 函数
old_render = """const container = document.getElementById('word-list-container');
  if (words.length === 0) {
    container.innerHTML = '<div class="empty-state"><h3>暂无单词</h3><p>请先学习一些单词</p></div>';
    return;
  }"""

new_render = """const container = document.getElementById('word-list-container');
  filteredWords = words;

  if (filteredWords.length === 0) {
    container.innerHTML = '<div class="empty-state"><h3>暂无单词</h3><p>请先学习一些单词</p></div>';
    document.getElementById('pagination-controls').style.display = 'none';
    return;
  }

  document.getElementById('pagination-controls').style.display = 'block';
  const start = currentPage * pageSize;
  const end = start + pageSize;
  const pageWords = filteredWords.slice(start, end);
  const totalPages = Math.ceil(filteredWords.length / pageSize);
  document.getElementById('page-info').textContent = `第 ${currentPage + 1} / ${totalPages} 页 (共 ${filteredWords.length} 个单词)`;"""

if old_render in content:
    content = content.replace(old_render, new_render, 1)
    print("✓ 修改 renderWordList 添加分页逻辑")

# 3. 将 words 改为 pageWords
content = content.replace(
    "words.forEach((word, index) => {",
    "pageWords.forEach((word, index) => {"
)
print("✓ 修改渲染循环")

# 4. 添加分页控制 HTML
old_container = "</div>\n\n<!-- Settings Page -->"
new_container = """</div>

  <div id="pagination-controls" style="display:none;text-align:center;margin-top:20px;padding-bottom:80px;">
    <button class="btn btn-outline" onclick="prevPage()" style="width:48%;display:inline-block;padding:12px;">← 上一页</button>
    <span id="page-info" style="margin:0 10px;font-size:14px;color:var(--subtext);"></span>
    <button class="btn btn-outline" onclick="nextPage()" style="width:48%;display:inline-block;padding:12px;">下一页 →</button>
  </div>
</div>

<!-- Settings Page -->"""

if old_container in content:
    content = content.replace(old_container, new_container, 1)
    print("✓ 添加分页控件 HTML")

# 5. 添加分页函数
old_switchpage = "function switchPage(pageName) {"
new_functions = """function prevPage() {
  if (currentPage > 0) { currentPage--; renderWordList(); }
}

function nextPage() {
  const totalPages = Math.ceil(filteredWords.length / pageSize);
  if (currentPage < totalPages - 1) { currentPage++; renderWordList(); }
}

function switchPage(pageName) {"

if old_switchpage in content:
    content = content.replace(old_switchpage, new_functions, 1)
    print("✓ 添加分页控制函数")

with open('/home/zz/下载/新建文件夹/vocab-app/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Task-06 完成！")