#!/usr/bin/env python3
"""
vocab_deep_test.py — 智能背单词深度测试

针对已发现的问题进行深入验证，并从初中生视角检查用户体验
"""
import time
from playwright.sync_api import sync_playwright

def run_test():
    p = sync_playwright().start()
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
    )
    context = browser.new_context(viewport={"width": 375, "height": 812})
    page = context.new_page()

    issues = []

    def add_issue(severity, category, desc):
        issue = {"severity": severity, "category": category, "description": desc}
        issues.append(issue)
        print(f"[{severity}] {category}: {desc}")

    try:
        # 导航到应用
        page.goto("file:///home/zz/下载/新建文件夹/vocab-app/index.html")
        time.sleep(1)
        page.screenshot(path="deep_test_01_home.png")

        print("\n=== 1. 首页检查 ===")

        # 检查统计数据
        total = page.locator("#total-words").text_content()
        learned = page.locator("#learned-words").text_content()
        mastered = page.locator("#mastered-words").text_content()
        due = page.locator("#due-today").text_content()

        print(f"词汇统计: 总{total}, 已学{learned}, 已掌握{mastered}, 今日待复习{due}")

        if int(total) > 2000:
            add_issue("MINOR", "CONTENT", f"词库数量({total})对于初中生可能过多")

        # 检查连续学习天数
        streak = page.locator("#streak-count").text_content()
        print(f"连续学习天数: {streak}")

        print("\n=== 2. 学习模式检查 ===")

        # 进入学习模式
        page.locator("#page-home button:has-text('开始学习')").click()
        time.sleep(1)
        page.screenshot(path="deep_test_02_learn.png")

        # 获取当前单词信息
        word = page.locator("#learn-word").text_content()
        phonetic = page.locator("#learn-phonetic").text_content()
        meaning = page.locator("#learn-meaning").text_content()
        example = page.locator("#learn-example").text_content()

        print(f"当前单词: {word}")
        print(f"音标: '{phonetic}'")
        print(f"释义: {meaning}")
        print(f"例句: '{example}'")

        # 检查音标是否为空
        if not phonetic.strip():
            add_issue("MAJOR", "CONTENT", f"单词 '{word}' 缺少音标标注")

        # 检查例句是否为空
        if not example.strip():
            add_issue("MINOR", "CONTENT", f"单词 '{word}' 缺少例句")

        # 检查释义质量
        if "高考常见词" in meaning:
            add_issue("CRITICAL", "CONTENT", f"单词 '{word}' 释义不完整，显示'高考常见词'")

        if "（来自" in meaning:
            add_issue("CRITICAL", "CONTENT", f"单词 '{word}' 释义包含源文件信息")

        # 测试点击显示释义
        meaning_elem = page.locator("#learn-meaning")
        initial_class = meaning_elem.get_attribute("class")
        meaning_elem.click()
        time.sleep(0.5)
        after_click_class = meaning_elem.get_attribute("class")

        if "revealed" not in after_click_class:
            add_issue("MAJOR", "FUNCTIONAL", "点击释义后未正确显示（缺少revealed类）")

        # 检查评分按钮
        buttons_found = []
        for text in ["完全忘记", "模糊", "记得", "熟练"]:
            btn = page.locator(f"button:has-text('{text}')")
            if btn.is_visible():
                buttons_found.append(text)
            else:
                add_issue("MAJOR", "FUNCTIONAL", f"评分按钮'{text}'不可见")

        print(f"找到的评分按钮: {buttons_found}")

        # 测试评分功能
        page.locator("button:has-text('熟练')").click()
        time.sleep(1)

        new_word = page.locator("#learn-word").text_content()
        if new_word == word:
            add_issue("MAJOR", "FUNCTIONAL", "点击评分后未切换到下一个单词")
        else:
            print(f"成功切换到新单词: {new_word}")

        print("\n=== 3. 默写模式检查 ===")

        # 导航到默写页面
        page.locator(".nav-item:nth-child(3)").click()
        time.sleep(1)
        page.screenshot(path="deep_test_03_dictation.png")

        # 检查默写界面元素
        dict_meaning = page.locator("#dict-meaning").text_content()
        dict_phonetic = page.locator("#dict-phonetic").text_content()
        dict_pos = page.locator("#dict-pos").text_content()

        print(f"默写释义: '{dict_meaning}'")
        print(f"默写音标: '{dict_phonetic}'")
        print(f"词性标注: '{dict_pos}'")

        if not dict_meaning.strip():
            add_issue("CRITICAL", "FUNCTIONAL", "默写模式下中文释义未显示")
        else:
            # 测试输入功能
            input_box = page.locator("#dict-input")
            input_box.fill("test")
            time.sleep(0.5)

            # 点击确认
            page.locator("button:has-text('确认')").click()
            time.sleep(0.5)

            feedback = page.locator("#dict-feedback").text_content()
            print(f"反馈信息: '{feedback}'")

            if not feedback:
                add_issue("MAJOR", "FUNCTIONAL", "提交答案后无反馈信息")

        print("\n=== 4. 词库管理检查 ===")

        # 导航到词库页面
        page.locator(".nav-item:nth-child(4)").click()
        time.sleep(1)
        page.screenshot(path="deep_test_04_wordlist.png")

        # 检查搜索功能
        search_box = page.locator("#search-input")
        search_box.fill("the")
        time.sleep(1)

        results = page.locator(".word-list-item").count()
        print(f"搜索'the'结果数: {results}")

        if results == 0:
            add_issue("MAJOR", "FUNCTIONAL", "搜索常见单词'the'无结果")

        # 清空搜索
        search_box.fill("")
        time.sleep(0.5)

        # 检查列表项结构
        first_item = page.locator(".word-list-item:first-child")
        if first_item.is_visible():
            item_word = first_item.locator("h3").text_content()
            item_meaning = first_item.locator("p").text_content()
            print(f"第一个单词: {item_word} - {item_meaning}")

        print("\n=== 5. 设置页面检查 ===")

        # 导航到设置页面
        page.locator(".nav-item:nth-child(5)").click()
        time.sleep(1)
        page.screenshot(path="deep_test_05_settings.png")

        # 检查滑块功能
        slider = page.locator("#daily-new-slider")
        slider_value = page.locator("#daily-new-value").text_content()
        print(f"每日新词设置值: {slider_value}")

        # 测试滑块变化
        slider.fill("25")
        time.sleep(0.5)
        new_value = page.locator("#daily-new-value").text_content()
        print(f"修改后值: {new_value}")

        if slider_value == new_value:
            add_issue("MAJOR", "FUNCTIONAL", "调整每日新词滑块后显示值未更新")

        print("\n=== 6. 导航栏检查 ===")

        # 检查导航项
        nav_items = page.locator(".nav-item")
        for i in range(nav_items.count()):
            item = nav_items.nth(i)
            text = item.locator("span").text_content()
            is_active = "active" in item.get_attribute("class")
            print(f"导航项 {i+1}: '{text}' (活跃: {is_active})")

        print("\n=== 7. 内容质量抽查 ===")

        # 返回首页并进入学习模式
        page.locator(".nav-item:first-child").click()
        time.sleep(0.5)
        page.locator("#page-home button:has-text('开始学习')").click()
        time.sleep(1)

        # 检查多个单词
        checked_words = set()
        for _ in range(10):
            current_word = page.locator("#learn-word").text_content()
            current_meaning = page.locator("#learn-meaning").text_content()

            if current_word in checked_words:
                continue
            checked_words.add(current_word)

            # 检查内容质量问题
            problems = []
            if "高考常见词" in current_meaning:
                problems.append("释义不完整")
            if "（来自" in current_meaning:
                problems.append("包含源文件信息")
            if not current_meaning.strip():
                problems.append("缺少释义")

            if problems:
                add_issue("MAJOR", "CONTENT", f"单词 '{current_word}': {', '.join(problems)} - 实际释义: '{current_meaning[:50]}...'")

            # 点击熟练切换到下一个
            page.locator("button:has-text('熟练')").click()
            time.sleep(0.3)

        print(f"\n共检查了 {len(checked_words)} 个不同单词")

    finally:
        # 生成报告
        print("\n" + "="*50)
        print("📊 测试报告")
        print("="*50)

        severity_counts = {}
        for issue in issues:
            sev = issue["severity"]
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        print(f"\n共发现 {len(issues)} 个问题:")
        for sev, count in sorted(severity_counts.items()):
            print(f"  - {sev}: {count} 个")

        print("\n详细问题列表:")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. [{issue['severity']}] {issue['category']}")
            print(f"   {issue['description']}")

        browser.close()
        p.stop()

if __name__ == "__main__":
    run_test()
