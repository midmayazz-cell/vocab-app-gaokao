#!/usr/bin/env python3
"""
Task-10: 添加空状态提示

问题：今日已学等页面无数据时缺少友好提示
"""

with open('/home/zz/下载/新建文件夹/vocab-app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查 showTodaysWords 函数是否有空状态处理
if "showTodaysWords" in content:
    print("✓ 找到 showTodaysWords 函数")

    # 查找当前实现
    import re
    pattern = r'function showTodaysWords\(\)\s*\{([^}]+(?:\{[^}]+\}[^}]*)*)\}'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        func_body = match.group(1)
        if "还没有学习" in func_body or "暂无" in func_body:
            print("✓ 已有空状态提示")
        else:
            print("✗ 缺少空状态提示，需要添加")
else:
    print("✗ 未找到 showTodaysWords 函数")

print("\n=== Task-10 检查完成 ===")