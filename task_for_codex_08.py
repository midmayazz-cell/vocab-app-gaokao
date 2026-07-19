#!/usr/bin/env python3
"""
Task-08: 合并重复词汇

问题：book/books, make/makes/made 等被当作独立词条
策略：标记重复词，保留基础形式
"""

with open('/home/zz/下载/新建文件夹/vocab-app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找出常见的重复模式
duplicates = {
    # (变体，基础形式)
    ("books", "book"),
    ("makes", "make"),
    ("made", "make"),
    ("making", "make"),
    ("wants", "want"),
    ("wanted", "want"),
    ("using", "use"),
    ("uses", "use"),
    ("used", "use"),
    ("jobs", "job"),
    ("friends", "friend"),
    ("teachers", "teacher"),
    ("days", "day"),
    ("times", "time"),
    ("ways", "way"),
    ("words", "word"),
    ("workers", "worker"),
    ("played", "play"),
    ("players", "play"),
}

print("=== 重复词汇分析 ===\n")

found_duplicates = []
for variant, base in duplicates:
    # 检查变体是否存在
    pattern_variant = f'{{word:"{variant}"'
    pattern_base = f'{{word:"{base}"'

    has_variant = pattern_variant in content
    has_base = pattern_base in content

    if has_variant and has_base:
        found_duplicates.append((variant, base))
        print(f"发现重复：{variant} ← {base}")

print(f"\n共发现 {len(found_duplicates)} 组重复词汇")
print("\n建议处理方式:")
print("1. 在变体单词的 meaning 字段添加'参见：[基础词]'提示")
print("2. 或在词库列表中折叠显示变体")
print("3. 或直接删除变体，只保留基础形式")

if found_duplicates:
    print("\n⚠️  Task-08 需要人工决策如何处理重复词汇")
else:
    print("\n✓ 未发现明显重复词汇")