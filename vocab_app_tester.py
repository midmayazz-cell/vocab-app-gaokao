#!/usr/bin/env python3
"""
vocab_app_tester.py — 智能背单词应用全面测试脚本

测试视角：初中生用户
测试目标：发现所有功能bug和操作不便之处
"""
import time
import random
from playwright.sync_api import sync_playwright

class VocabAppTester:
    def __init__(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        self.context = self.browser.new_context(
            viewport={"width": 375, "height": 812},  # iPhone X 尺寸
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
        )
        self.page = self.context.new_page()

        # 测试结果存储
        self.issues_found = []
        self.screenshots = []

    def take_screenshot(self, name):
        """截图并记录"""
        path = f"test_{name}.png"
        self.page.screenshot(path=path)
        self.screenshots.append(path)
        return path

    def add_issue(self, severity, category, description, steps_to_reproduce=None):
        """记录发现的问题"""
        issue = {
            "severity": severity,  # CRITICAL, MAJOR, MINOR, COSMETIC
            "category": category,  # FUNCTIONAL, UX, PERFORMANCE, CONTENT
            "description": description,
            "steps": steps_to_reproduce or []
        }
        self.issues_found.append(issue)
        print(f"[{severity}] {category}: {description}")

    def navigate_to_file(self):
        """导航到本地文件"""
        self.page.goto("file:///home/zz/下载/新建文件夹/vocab-app/index.html")
        time.sleep(1)
        self.take_screenshot("initial_load")

    def test_home_page(self):
        """测试首页功能"""
        print("\n=== 测试首页 ===")

        # 检查页面标题
        title = self.page.title()
        if not title or "单词" not in title:
            self.add_issue("MINOR", "CONTENT", f"页面标题不明确: '{title}'")

        # 检查统计数据是否正确初始化
        total_words = self.page.locator("#total-words").text_content()
        learned = self.page.locator("#learned-words").text_content()
        mastered = self.page.locator("#mastered-words").text_content()
        due_today = self.page.locator("#due-today").text_content()

        print(f"初始数据: 总词汇={total_words}, 已学习={learned}, 已掌握={mastered}, 今日待复习={due_today}")

        # 检查进度条
        progress_text = self.page.locator("#progress-percent").text_content()
        if progress_text != "0%":
            self.add_issue("MAJOR", "FUNCTIONAL", f"新用户的进度应该显示0%，实际显示: {progress_text}")

        # 测试"开始学习"按钮
        start_btn = self.page.locator("button:has-text('开始学习')")
        if not start_btn.is_visible():
            self.add_issue("CRITICAL", "FUNCTIONAL", "首页缺少'开始学习'按钮")
        else:
            self.take_screenshot("home_before_click")
            start_btn.click()
            time.sleep(1)
            self.take_screenshot("after_click_start")

            # 检查是否进入学习模式
            current_page = self.page.locator(".page.active").get_attribute("id")
            if "learn" not in current_page:
                self.add_issue("CRITICAL", "FUNCTIONAL", f"点击'开始学习'后未进入学习页面，当前页面: {current_page}")

        # 返回首页测试其他按钮
        home_btn = self.page.locator("#page-learn button:has-text('返回首页')")
        if home_btn.count() > 0:
            home_btn.first.click()
        else:
            self.page.locator(".nav-item:first-child").click()  # 点击首页导航
        time.sleep(0.5)

        # 测试"今日已学"按钮
        today_btn = self.page.locator("button:has-text('今日已学')")
        if today_btn.is_visible():
            today_btn.click()
            time.sleep(0.5)
            # 检查是否有适当的空状态提示
            empty_state = self.page.locator(".empty-state")
            if not empty_state.is_visible():
                self.add_issue("MINOR", "UX", "点击'今日已学'后应显示空状态提示")

    def test_learning_mode(self):
        """测试学习模式"""
        print("\n=== 测试学习模式 ===")

        # 进入学习模式
        self.page.locator("button:has-text('开始学习')").click()
        time.sleep(1)

        # 检查单词卡片是否显示
        word_card = self.page.locator("#word-card")
        if not word_card.is_visible():
            self.add_issue("CRITICAL", "FUNCTIONAL", "学习模式下单词卡片未显示")
            return

        # 检查单词内容
        english_word = self.page.locator("#learn-word").text_content()
        phonetic = self.page.locator("#learn-phonetic").text_content()
        meaning = self.page.locator("#learn-meaning").text_content()
        example = self.page.locator("#learn-example").text_content()

        print(f"当前单词: {english_word}, 音标: {phonetic}, 释义: {meaning}")

        # 检查单词是否为空
        if not english_word.strip():
            self.add_issue("CRITICAL", "FUNCTIONAL", "单词卡片中英语单词为空")

        # 检查释义是否被正确隐藏
        meaning_element = self.page.locator("#learn-meaning")
        if "word-hidden" not in meaning_element.get_attribute("class"):
            self.add_issue("MINOR", "UX", "释义应该在首次加载时被隐藏")

        # 测试点击显示释义
        meaning_element.click()
        time.sleep(0.5)
        if "revealed" not in meaning_element.get_attribute("class"):
            self.add_issue("MAJOR", "FUNCTIONAL", "点击释义后未正确显示")

        # 测试评分按钮
        buttons = ["完全忘记", "模糊", "记得", "熟练"]
        for btn_text in buttons:
            btn = self.page.locator(f"button:has-text('{btn_text}')")
            if not btn.is_visible():
                self.add_issue("MAJOR", "FUNCTIONAL", f"评分按钮'{btn_text}'未显示")
            else:
                btn.click()
                time.sleep(0.5)
                # 检查是否切换到下一个单词或完成提示
                new_word = self.page.locator("#learn-word").text_content()
                if new_word == english_word:  # 单词没变，说明没有前进
                    self.add_issue("MAJOR", "FUNCTIONAL", f"点击'{btn_text}'后未切换到下一个单词")
                break  # 只测试一个按钮避免过多操作

        # 检查学习计数器
        counter = self.page.locator("#learn-counter").text_content()
        if not counter or "/" not in counter:
            self.add_issue("MINOR", "UX", f"学习计数器格式不正确: {counter}")

    def test_dictation_mode(self):
        """测试默写模式"""
        print("\n=== 测试默写模式 ===")

        # 进入默写模式
        self.page.locator("nav .nav-item:nth-child(3)").click()  # 点击默写标签
        time.sleep(1)

        # 检查默写界面元素
        meaning_display = self.page.locator("#dict-meaning").text_content()
        if not meaning_display.strip():
            self.add_issue("CRITICAL", "FUNCTIONAL", "默写模式下中文释义未显示")

        # 检查输入框
        input_box = self.page.locator("#dict-input")
        if not input_box.is_visible():
            self.add_issue("CRITICAL", "FUNCTIONAL", "默写输入框未显示")
        else:
            # 测试输入功能
            test_word = "test"
            input_box.fill(test_word)
            time.sleep(0.5)

            # 检查确认按钮
            confirm_btn = self.page.locator("button:has-text('确认')")
            if confirm_btn.is_visible():
                confirm_btn.click()
                time.sleep(0.5)

                # 检查反馈信息
                feedback = self.page.locator("#dict-feedback").text_content()
                if not feedback:
                    self.add_issue("MAJOR", "FUNCTIONAL", "提交答案后无反馈信息")

            # 清空输入框
            input_box.fill("")

        # 测试提示功能
        hint_btn = self.page.locator("button:has-text('提示')")
        if hint_btn.is_visible():
            hint_btn.click()
            time.sleep(0.5)
            # 检查是否有提示信息出现
            if not self.page.locator("#dict-feedback").text_content():
                self.add_issue("MINOR", "FUNCTIONAL", "点击提示后无提示信息")

    def test_word_list(self):
        """测试词库管理"""
        print("\n=== 测试词库管理 ===")

        # 进入词库页面
        self.page.locator("nav .nav-item:nth-child(4)").click()  # 点击词库标签
        time.sleep(1)

        # 检查搜索框
        search_box = self.page.locator("#search-input")
        if not search_box.is_visible():
            self.add_issue("CRITICAL", "FUNCTIONAL", "词库搜索框未显示")
        else:
            # 测试搜索功能
            search_box.fill("apple")
            time.sleep(1)

            # 检查结果数量
            items = self.page.locator(".word-list-item").count()
            print(f"搜索'apple'结果数: {items}")

            # 清空搜索
            search_box.fill("")
            time.sleep(0.5)

        # 检查分类标签
        tags = self.page.locator(".category-tag").count()
        print(f"分类标签数量: {tags}")

        # 检查单词列表项
        list_items = self.page.locator(".word-list-item").count()
        print(f"单词列表项数量: {list_items}")

        if list_items == 0:
            self.add_issue("CRITICAL", "FUNCTIONAL", "词库列表为空，应显示单词")
        elif list_items > 100:
            self.add_issue("MINOR", "PERFORMANCE", f"一次性加载过多单词({list_items}个)，建议分页")

    def test_settings(self):
        """测试设置页面"""
        print("\n=== 测试设置页面 ===")

        # 进入设置页面
        self.page.locator("nav .nav-item:nth-child(5)").click()  # 点击设置标签
        time.sleep(1)

        # 检查每日新词滑块
        slider = self.page.locator("#daily-new-slider")
        if slider.is_visible():
            current_value = slider.input_value()
            display_value = self.page.locator("#daily-new-value").text_content()
            if current_value != display_value:
                self.add_issue("MAJOR", "FUNCTIONAL", f"滑块值({current_value})与显示值({display_value})不一致")

        # 检查开关控件
        toggles = self.page.locator(".toggle").count()
        print(f"设置开关数量: {toggles}")

        # 测试导出数据功能
        export_btn = self.page.locator(".setting-item:has-text('导出数据')")
        if export_btn.count() > 0:
            try:
                export_btn.click()
                time.sleep(1)
                # 检查是否有下载或提示
                toast = self.page.locator(".toast")
                if not toast.text_content():
                    self.add_issue("MINOR", "FUNCTIONAL", "导出数据后无用户反馈")
            except Exception as e:
                self.add_issue("MAJOR", "FUNCTIONAL", f"导出数据功能异常: {str(e)}")

    def test_navigation(self):
        """测试导航功能"""
        print("\n=== 测试导航功能 ===")

        # 检查底部导航栏
        nav_items = self.page.locator(".nav-item").count()
        expected_items = 5  # 首页、学习、默写、词库、设置

        if nav_items != expected_items:
            self.add_issue("MAJOR", "FUNCTIONAL", f"导航栏项目数量错误: 期望{expected_items}, 实际{nav_items}")

        # 测试每个导航项
        nav_names = ["首页", "学习", "默写", "词库", "设置"]
        for i, name in enumerate(nav_names):
            nav_item = self.page.locator(f".nav-item:nth-child({i+1})")
            if nav_item.is_visible():
                nav_item.click()
                time.sleep(0.5)

                # 检查是否高亮当前页面
                if "active" not in nav_item.get_attribute("class"):
                    self.add_issue("MINOR", "UX", f"点击'{name}'后导航项未高亮")

                # 截图记录
                self.take_screenshot(f"nav_{name}")

    def test_content_quality(self):
        """测试内容质量"""
        print("\n=== 测试内容质量 ===")

        # 进入学习模式查看单词
        self.page.locator("button:has-text('开始学习')").click()
        time.sleep(1)

        # 检查多个单词的内容质量
        for _ in range(min(5, 10)):  # 最多检查5个单词
            word = self.page.locator("#learn-word").text_content()
            meaning = self.page.locator("#learn-meaning").text_content()

            # 检查是否有明显错误
            if "高考常见词" in meaning:
                self.add_issue("MAJOR", "CONTENT", f"单词 '{word}' 释义不完整，显示'高考常见词'")

            if "（来自" in meaning:
                self.add_issue("MAJOR", "CONTENT", f"单词 '{word}' 释义包含源文件信息: {meaning[:30]}...")

            if not meaning.strip():
                self.add_issue("CRITICAL", "CONTENT", f"单词 '{word}' 缺少中文释义")

            # 点击"熟练"切换到下一个单词
            self.page.locator("button:has-text('熟练')").click()
            time.sleep(0.5)

    def test_responsiveness(self):
        """测试响应式设计"""
        print("\n=== 测试响应式设计 ===")

        # 在不同视口大小下测试
        viewports = [
            (375, 812),   # iPhone X
            (414, 896),   # iPhone 11 Pro Max
            (768, 1024),  # iPad
            (1024, 768),  # Laptop
        ]

        for width, height in viewports:
            self.page.set_viewport_size({"width": width, "height": height})
            time.sleep(0.5)

            # 检查基本元素是否可见
            nav_visible = self.page.locator(".nav").is_visible()
            page_visible = self.page.locator(".page.active").is_visible()

            if not nav_visible or not page_visible:
                self.add_issue("MAJOR", "UX", f"在视口 {width}x{height} 下导航或页面不可见")

            self.take_screenshot(f"responsive_{width}x{height}")

        # 恢复原始视口
        self.page.set_viewport_size({"width": 375, "height": 812})

    def test_accessibility(self):
        """测试无障碍功能"""
        print("\n=== 测试无障碍功能 ===")

        # 检查ARIA标签
        buttons = self.page.locator("button")
        for i in range(buttons.count()):
            btn = buttons.nth(i)
            text = btn.text_content()
            aria_label = btn.get_attribute("aria-label")

            if not text and not aria_label:
                self.add_issue("MINOR", "ACCESSIBILITY", f"按钮缺少文本或aria-label: {btn.get_attribute('class')}")

    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始智能背单词应用全面测试")
        print("=" * 50)

        try:
            # 导航到应用
            self.navigate_to_file()

            # 运行各模块测试
            self.test_home_page()
            self.test_learning_mode()
            self.test_dictation_mode()
            self.test_word_list()
            self.test_settings()
            self.test_navigation()
            self.test_content_quality()
            self.test_responsiveness()
            self.test_accessibility()

            # 生成测试报告
            self.generate_report()

        except Exception as e:
            print(f"❌ 测试过程中发生错误: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.browser.close()
            self.p.stop()

    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 50)
        print("📊 测试报告")
        print("=" * 50)

        # 统计问题数量
        severity_counts = {}
        category_counts = {}

        for issue in self.issues_found:
            sev = issue["severity"]
            cat = issue["category"]
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
            category_counts[cat] = category_counts.get(cat, 0) + 1

        print(f"\n🔍 共发现 {len(self.issues_found)} 个问题:")
        print("\n按严重程度分类:")
        for sev, count in sorted(severity_counts.items()):
            print(f"  - {sev}: {count} 个")

        print("\n按类别分类:")
        for cat, count in sorted(category_counts.items()):
            print(f"  - {cat}: {count} 个")

        print(f"\n📸 生成截图: {len(self.screenshots)} 张")
        for path in self.screenshots:
            print(f"  - {path}")

        # 详细问题列表
        print("\n📋 详细问题列表:")
        for i, issue in enumerate(self.issues_found, 1):
            print(f"\n{i}. [{issue['severity']}] {issue['category']}")
            print(f"   描述: {issue['description']}")
            if issue['steps']:
                print(f"   复现步骤: {' → '.join(issue['steps'])}")

if __name__ == "__main__":
    tester = VocabAppTester()
    tester.run_all_tests()
