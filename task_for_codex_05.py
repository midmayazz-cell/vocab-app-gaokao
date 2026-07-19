#!/usr/bin/env python3
"""
Task-05: 修复释义点击显示功能

问题：学习模式下，点击模糊的释义后无法显示
原因：revealMeaning() 函数使用了错误的类操作

修复：将 classList.remove('word-hidden') 改为 classList.add('revealed')
"""

with open('/home/zz/下载/新建文件夹/vocab-app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_code = """document.getElementById('learn-meaning').classList.remove('word-hidden');
  document.getElementById('learn-example').classList.remove('word-hidden');"""

new_code = """document.getElementById('learn-meaning').classList.add('revealed');
  document.getElementById('learn-example').classList.add('revealed');"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('/home/zz/下载/新建文件夹/vocab-app/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Task-05 完成！")
else:
    print("✗ 未找到需要修复的代码，可能已被修复")

# 验证
with open('/home/zz/下载/新建文件夹/vocab-app/index.html', 'r', encoding='utf-8') as f:
    check = f.read()
if "classList.add('revealed')" in check:
    print("✓ 验证通过")
else:
    print("✗ 验证失败")