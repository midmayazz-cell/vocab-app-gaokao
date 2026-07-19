#!/usr/bin/env python3
"""
Task-07: 补充缺失释义

问题：部分单词释义不完整或只有一个字"的"
"""

with open('/home/zz/下载/新建文件夹/vocab-app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('material', '"的"', '"材料；物质的"', 'adj.'),
    ('materials', '"的"', '"材料（复数）"', 'n.'),
    ('physical', '"的"', '"身体的；物理的"', 'adj.'),
    ('typical', '"的"', '"典型的"', 'adj.'),
    ('critical', '"的"', '"关键的；批判的"', 'adj.'),
]

count = 0
for word, old_meaning, new_meaning, new_pos in replacements:
    old = f'{{word:"{word}",phonetic:"",meaning:{old_meaning},pos:'
    new = f'{{word:"{word}",phonetic:"",meaning:{new_meaning},pos:'
    if old in content:
        content = content.replace(old, new)
        count += 1
        print(f"✓ Fixed: {word}")

with open('/home/zz/下载/新建文件夹/vocab-app/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nTask-07 完成！共修正 {count} 个单词")

# 验证
remaining = content.count('meaning:"的"')
print(f"剩余'{remaining}'处不完整释义")