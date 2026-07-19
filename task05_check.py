#!/usr/bin/env python3
"""
Task-05: 修复释义点击显示功能

问题：学习模式下，点击模糊的释义后，CSS 类 'revealed' 未被正确添加
文件：index.html
位置：revealMeaning() 函数

修复内容：
1. 检查 revealMeaning() 函数是否正确添加 revealed 类
2. 确保点击事件绑定正确
"""

import re

with open('/home/zz/下载/新建文件夹/vocab-app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找 revealMeaning 函数
if 'function revealMeaning()' in content:
    print("✓ 找到 revealMeaning() 函数")

    # 检查函数实现
    pattern = r'function revealMeaning\(\)\s*\{([^}]+)\}'
    match = re.search(pattern, content)
    if match:
        func_body = match.group(1)
        print(f"当前实现:\n{func_body}")

        # 检查是否有添加 revealed 类的代码
        if 'revealed' in func_body or 'classList' in func_body:
            print("✓ 函数中已有 revealed 相关代码")
        else:
            print("✗ 函数缺少 revealed 类添加逻辑")
    else:
        print("✗ 无法解析 revealMeaning 函数")
else:
    print("✗ 未找到 revealMeaning() 函数")

# 检查 HTML 中的 onclick 绑定
onclick_count = content.count('onclick="revealMeaning()"')
print(f"\nonclick 绑定数量：{onclick_count}")

print("\n=== 需要人工检查 ===")
print("1. revealMeaning() 函数是否正确实现？")
print("2. 点击事件是否正确绑定？")
print("3. CSS 类切换是否生效？")
