#!/usr/bin/env python3
"""
Task-09: 优化导航栏状态管理

问题：切换页面后导航项 active 状态未正确更新
"""

with open('/home/zz/下载/新建文件夹/vocab-app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查 switchPage 函数中的导航状态更新
if "classList.add('active')" in content and "classList.remove('active')" in content:
    print("✓ switchPage 函数中有导航状态管理代码")

    # 查找具体实现
    import re
    pattern = r"document\.querySelectorAll\('\.nav-item'\)\[.*?\]\?\.classList\.add\('active'\)"
    matches = re.findall(pattern, content)
    print(f"找到 {len(matches)} 处导航激活代码")
else:
    print("✗ 导航状态管理代码缺失")

print("\n当前 switchPage 实现:")
idx = content.find("function switchPage")
if idx >= 0:
    print(content[idx:idx+500])