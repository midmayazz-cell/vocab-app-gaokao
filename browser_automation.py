#!/usr/bin/env python3
"""browser_automation.py — 通用浏览器自动化工具

功能：模拟鼠标点击、键盘输入、滚轮滚动、翻页
用法：python browser_automation.py --url https://example.com
"""
import argparse
import time
import random
from playwright.sync_api import sync_playwright


class BrowserBot:
    """浏览器自动化机器人"""

    def __init__(self, headless=False, slow_mo=300):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(
            headless=headless,
            slow_mo=slow_mo,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ]
        )
        self.context = self.browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        self.page = self.context.new_page()

    # ── 导航 ──────────────────────────────────────
    def goto(self, url):
        print(f"[NAV] → {url}")
        self.page.goto(url, wait_until="networkidle")
        time.sleep(0.5)

    # ── 鼠标点击 ──────────────────────────────────
    def click_at(self, x, y, button="left", clicks=1):
        """在指定坐标点击"""
        action = {
            1: "单击",
            2: "双击",
            3: "三击",
        }.get(clicks, f"{clicks}次点击")
        print(f"[MOUSE] {action} ({x}, {y}) [{button}]")
        self.page.mouse.click(x, y, button=button, click_count=clicks)

    def click_element(self, selector):
        """点击指定元素"""
        print(f"[MOUSE] 点击元素 {selector}")
        self.page.click(selector)

    def drag(self, x1, y1, x2, y2):
        """拖拽操作"""
        print(f"[MOUSE] 拖拽 ({x1},{y1}) → ({x2},{y2})")
        self.page.mouse.move(x1, y1)
        self.page.mouse.down()
        self.page.mouse.move(x2, y2)
        self.page.mouse.up()

    # ── 键盘输入 ──────────────────────────────────
    def type_text(self, text, delay=50):
        """模拟逐字输入"""
        print(f"[KEY] 输入: {text[:40]}{'...' if len(text)>40 else ''}")
        self.page.keyboard.type(text, delay=delay)

    def press_key(self, key):
        """按单个键"""
        print(f"[KEY] 按键: {key}")
        self.page.keyboard.press(key)

    def hotkey(self, keys):
        """快捷键组合，如 Ctrl+A"""
        print(f"[KEY] 快捷键: {keys}")
        self.page.keyboard.press(keys)

    # ── 滚动 ──────────────────────────────────────
    def scroll_down(self, amount=300):
        """向下滚动"""
        print(f"[SCROLL] ↓ {amount}px")
        self.page.mouse.wheel(0, amount)
        time.sleep(0.3)

    def scroll_up(self, amount=300):
        """向上滚动"""
        print(f"[SCROLL] ↑ {amount}px")
        self.page.mouse.wheel(0, -amount)
        time.sleep(0.3)

    def scroll_to_bottom(self):
        """滚到底部"""
        print("[SCROLL] 滚到底部")
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.5)

    def scroll_to_top(self):
        """滚到顶部"""
        print("[SCROLL] 滚到顶部")
        self.page.evaluate("window.scrollTo(0, 0)")
        time.sleep(0.5)

    def page_down(self):
        """Page Down"""
        print("[SCROLL] PageDown")
        self.page.keyboard.press("PageDown")
        time.sleep(0.3)

    def page_up(self):
        """Page Up"""
        print("[SCROLL] PageUp")
        self.page.keyboard.press("PageUp")
        time.sleep(0.3)

    # ── 工具 ──────────────────────────────────────
    def screenshot(self, path="screenshot.png"):
        """截图"""
        self.page.screenshot(path=path)
        print(f"[SNAP] 截图 → {path}")

    def random_click(self):
        """随机位置点击（模拟人类行为）"""
        x = random.randint(50, 1230)
        y = random.randint(50, 670)
        self.click_at(x, y)

    def random_scroll(self):
        """随机方向滚动"""
        direction = random.choice([-1, 1])
        amount = random.randint(100, 500)
        self.page.mouse.wheel(0, direction * amount)
        time.sleep(random.uniform(0.2, 0.8))

    def close(self):
        """关闭浏览器"""
        self.browser.close()
        self.p.stop()
        print("[DONE] 浏览器已关闭")


# ── 预设场景 ────────────────────────────────────────

def demo_basic(url, headless=False):
    """基础演示：导航 + 点击 + 输入 + 滚动"""
    bot = BrowserBot(headless=headless)
    try:
        bot.goto(url)
        bot.screenshot("demo_01_start.png")

        # 向下滚动几次
        for _ in range(3):
            bot.scroll_down(400)
            time.sleep(0.5)

        bot.screenshot("demo_02_scrolled.png")

        # 滚到顶部
        bot.scroll_to_top()

        # 随机点击
        bot.random_click()
        time.sleep(1)

        bot.screenshot("demo_03_end.png")

    finally:
        bot.close()


def demo_typing(url, headless=False):
    """打字演示：在搜索框中输入"""
    bot = BrowserBot(headless=headless)
    try:
        bot.goto(url)
        time.sleep(1)

        # 尝试找搜索框
        selectors = ["input[type='search']", "input[name='q']", "#search-input", "textarea"]
        found = False
        for sel in selectors:
            if bot.page.locator(sel).first.is_visible():
                bot.page.locator(sel).first.click()
                bot.type_text("Hello World from Playwright!", delay=80)
                bot.press_key("Enter")
                found = True
                break

        if not found:
            # 直接键盘输入
            bot.hotkey("Ctrl+A")
            bot.type_text("test input text")

        time.sleep(1)
        bot.screenshot("demo_typing.png")

    finally:
        bot.close()


def demo_human_like(url, headless=False):
    """模拟人类行为：随机操作序列"""
    bot = BrowserBot(headless=headless, slow_mo=500)
    try:
        bot.goto(url)
        time.sleep(1)

        actions = 0
        max_actions = 15

        while actions < max_actions:
            action = random.choice([
                "scroll_down", "scroll_up", "page_down",
                "page_up", "random_click", "random_scroll"
            ])

            if action == "scroll_down":
                bot.scroll_down(random.randint(100, 600))
            elif action == "scroll_up":
                bot.scroll_up(random.randint(100, 600))
            elif action == "page_down":
                bot.page_down()
            elif action == "page_up":
                bot.page_up()
            elif action == "random_click":
                bot.random_click()
            elif action == "random_scroll":
                bot.random_scroll()

            actions += 1
            time.sleep(random.uniform(0.5, 2.0))

        bot.screenshot("demo_human_like.png")

    finally:
        bot.close()


# ── 主入口 ──────────────────────────────────────────

SCENES = {
    "basic": ("基础演示（导航+点击+滚动）", demo_basic),
    "typing": ("打字演示（搜索框输入）", demo_typing),
    "human": ("人类模拟（随机操作序列）", demo_human_like),
}


def main():
    parser = argparse.ArgumentParser(description="浏览器自动化工具")
    parser.add_argument("--url", default="https://example.com", help="目标网址")
    parser.add_argument(
        "--scene", choices=list(SCENES.keys()), default="basic",
        help="选择演示场景"
    )
    parser.add_argument("--headless", action="store_true", help="无头模式（不显示窗口）")
    args = parser.parse_args()

    name, desc = SCENES[args.scene]
    print(f"\n{'='*50}")
    print(f"  浏览器自动化 — {desc}")
    print(f"  URL: {args.url}")
    print(f"{'='*50}\n")

    scene_func = SCENES[args.scene][1]
    scene_func(args.url, args.headless)


if __name__ == "__main__":
    main()
