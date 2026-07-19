#!/usr/bin/env python3
"""
Task-04: 替换"高考常见词"占位符为实际释义

需要修正的单词列表：
exercise, risk, effect, consider, economy, foreign, comfort, custom,
customs, issue, pressure, brilliant, burden, candidate, career, capable,
colleague, combine, describe, degree, boundary, force, narrow, customers,
encourage, physical, physically, countries, customers, effect, effects,
economy, economic, encourage, foreign, foreigners, force, function, functions,
issue, issues, matter, matters, narrow, narrowly, patient, patients, play, plays,
pressure, pressures, regular, regularly, risk, risks, work, works, working
"""

import re

# 正确的释义映射
CORRECT_MEANINGS = {
    "exercise": "运动，锻炼；练习",
    "risk": "风险，危险",
    "effect": "效果，影响",
    "consider": "考虑，认为",
    "economy": "经济",
    "foreign": "外国的",
    "comfort": "舒适；安慰",
    "custom": "习俗，习惯",
    "customs": "海关；风俗",
    "issue": "问题；发行",
    "pressure": "压力",
    "brilliant": "杰出的；灿烂的",
    "burden": "负担，重担",
    "candidate": "候选人",
    "career": "职业，事业",
    "capable": "有能力的",
    "colleague": "同事",
    "combine": "结合，组合",
    "describe": "描述，形容",
    "degree": "程度；学位",
    "boundary": "边界，界限",
    "force": "力量；强迫",
    "narrow": "狭窄的",
    "customers": "顾客",
    "encourage": "鼓励",
    "physical": "身体的；物理的",
    "physically": "身体上",
    "countries": "国家（复数）",
    "effects": "效果（复数）",
    "economic": "经济的",
    "foreigners": "外国人",
    "functions": "功能（复数）",
    "issues": "问题（复数）",
    "matters": "事情（复数）",
    "narrowly": "勉强地；狭窄地",
    "patients": "病人",
    "play": "玩耍；播放",
    "plays": "播放（第三人称）",
    "pressures": "压力（复数）",
    "regular": "规律的；定期的",
    "regularly": "定期地",
    "risks": "风险（复数）",
    "work": "工作",
    "works": "作品；工作",
    "working": "工作的",
}

with open('/home/zz/下载/新建文件夹/vocab-app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

fixed_count = 0
for word, meaning in CORRECT_MEANINGS.items():
    # 匹配 pattern: {word:"xxx",phonetic:"",meaning:"v.高考常见词",...}
    pattern = rf'(\{{word:"{word}",phonetic:"",meaning:")v\.? 高考常见词(.*\}})'

    def replacer(match):
        nonlocal fixed_count
        fixed_count += 1
        return f'{match.group(1)}{meaning}{match.group(2)}'

    content = re.sub(pattern, replacer, content)

with open('/home/zz/下载/新建文件夹/vocab-app/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Task-04 完成！共修正 {fixed_count} 个单词")

# 验证
remaining = content.count('高考常见词')
print(f"剩余'{remaining}'处'高考常见词'")
