#!/usr/bin/env python3
"""
Calendar Date Click and Highlighting Test

Tests whether the calendar component properly highlights dates
when clicked according to Tailwind CSS theme.

Usage:
    # Make sure webapp is running first
    make webapp

    # Then run this test
    uv run python .claude/skills/webapp-testing/test_calendar_highlighting.py
"""

from playwright.sync_api import sync_playwright
import time
import sys


def test_calendar_highlighting():
    """Test calendar date click events and theme highlighting"""

    print("🚀 Starting calendar highlighting test...")

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()

        try:
            # Navigate to the app
            print("\n📍 Navigating to http://localhost:8081...")
            page.goto('http://localhost:8081', wait_until='networkidle', timeout=30000)

            # Take initial screenshot
            page.screenshot(path='/tmp/calendar_home.png', full_page=True)
            print("📸 Home screenshot saved: /tmp/calendar_home.png")

            # Wait a bit for React Native to fully render
            time.sleep(2)

            # Click "여행 계획 만들기" button to navigate to calendar
            print("\n🔍 Looking for '여행 계획 만들기' button...")
            try:
                plan_button = page.locator('text=여행 계획 만들기')
                if plan_button.count() > 0:
                    print("✅ Found '여행 계획 만들기' button, clicking...")
                    plan_button.click()
                    time.sleep(2)
                    page.screenshot(path='/tmp/calendar_plan_screen.png', full_page=True)
                    print("📸 Plan screen screenshot saved: /tmp/calendar_plan_screen.png")
                else:
                    print("⚠️  '여행 계획 만들기' button not found, trying alternative selectors...")
            except Exception as e:
                print(f"⚠️  Could not click plan button: {e}")

            # Look for calendar-related elements
            print("\n🔍 Searching for calendar elements...")

            # Try to find calendar container or date buttons
            calendar_selectors = [
                '[data-testid*="calendar"]',
                '[class*="calendar"]',
                'button[data-date]',
                'div[role="button"]',
                '.react-calendar',
                '[aria-label*="날짜"]',
                '[aria-label*="date"]',
            ]

            calendar_found = False
            for selector in calendar_selectors:
                elements = page.locator(selector).all()
                if elements:
                    print(f"✅ Found {len(elements)} elements with selector: {selector}")
                    calendar_found = True
                    break

            if not calendar_found:
                print("⚠️  No specific calendar selectors found, checking all buttons...")

            # Get all buttons on the page that are NOT disabled
            all_buttons = page.locator('button:not([disabled])').all()
            print(f"\n📊 Total enabled buttons found: {len(all_buttons)}")

            # Find date-like buttons (buttons with numbers or date patterns)
            date_buttons = []
            for i, button in enumerate(all_buttons):
                try:
                    text = button.inner_text()
                    # Check if button text looks like a date (number between 1-31)
                    if text.strip().isdigit():
                        num = int(text.strip())
                        if 1 <= num <= 31:  # Valid date numbers
                            date_buttons.append((i, button, text))
                            print(f"  📅 Button {i}: '{text}' (enabled)")
                except Exception as e:
                    continue

            if not date_buttons:
                print("\n❌ No clickable date buttons found!")
                print("\n🔍 Dumping page content for inspection...")
                content = page.content()
                with open('/tmp/calendar_page.html', 'w', encoding='utf-8') as f:
                    f.write(content)
                print("📄 Page HTML saved: /tmp/calendar_page.html")
                return False

            print(f"\n✅ Found {len(date_buttons)} clickable date buttons")

            # Test clicking on date buttons and check for highlighting
            print("\n🎯 Testing date button clicks and highlighting...")

            test_results = []

            for idx, (btn_idx, button, text) in enumerate(date_buttons[:5]):  # Test first 5 dates
                try:
                    print(f"\n--- Test {idx + 1}: Clicking button '{text}' ---")

                    # Get initial styles before click
                    initial_class = button.get_attribute('class') or ''
                    initial_styles = page.evaluate('''
                        (btn) => {
                            const styles = window.getComputedStyle(btn);
                            return {
                                backgroundColor: styles.backgroundColor,
                                color: styles.color,
                                borderColor: styles.borderColor,
                                opacity: styles.opacity
                            };
                        }
                    ''', button.element_handle())

                    print(f"  📋 Initial class: {initial_class}")
                    print(f"  🎨 Initial styles: {initial_styles}")

                    # Click the button
                    button.click()
                    time.sleep(0.5)  # Wait for state update

                    # Get styles after click
                    after_class = button.get_attribute('class') or ''
                    after_styles = page.evaluate('''
                        (btn) => {
                            const styles = window.getComputedStyle(btn);
                            return {
                                backgroundColor: styles.backgroundColor,
                                color: styles.color,
                                borderColor: styles.borderColor,
                                opacity: styles.opacity
                            };
                        }
                    ''', button.element_handle())

                    # Check parent and siblings for changes
                    parent_info = page.evaluate('''
                        (btn) => {
                            const parent = btn.parentElement;
                            if (!parent) return null;
                            const parentStyles = window.getComputedStyle(parent);
                            return {
                                class: parent.className,
                                backgroundColor: parentStyles.backgroundColor,
                                borderColor: parentStyles.borderColor
                            };
                        }
                    ''', button.element_handle())

                    print(f"  📋 After class: {after_class}")
                    print(f"  🎨 After styles: {after_styles}")
                    print(f"  👪 Parent info: {parent_info}")

                    # Check if styles changed
                    style_changed = (
                        initial_styles['backgroundColor'] != after_styles['backgroundColor'] or
                        initial_styles['color'] != after_styles['color'] or
                        initial_styles['borderColor'] != after_styles['borderColor'] or
                        initial_class != after_class
                    )

                    # Take screenshot after click
                    screenshot_path = f'/tmp/calendar_click_{idx + 1}.png'
                    page.screenshot(path=screenshot_path, full_page=True)
                    print(f"  📸 Screenshot saved: {screenshot_path}")

                    if style_changed:
                        print(f"  ✅ PASS: Styling changed after click!")
                        test_results.append({
                            'button': text,
                            'passed': True,
                            'message': 'Style changed successfully'
                        })
                    else:
                        print(f"  ⚠️  WARNING: No visible style change detected")
                        test_results.append({
                            'button': text,
                            'passed': False,
                            'message': 'No style change detected'
                        })

                except Exception as e:
                    print(f"  ❌ ERROR: {str(e)}")
                    test_results.append({
                        'button': text,
                        'passed': False,
                        'message': f'Error: {str(e)}'
                    })

            # Print summary
            print("\n" + "="*60)
            print("📊 TEST SUMMARY")
            print("="*60)

            passed = sum(1 for r in test_results if r['passed'])
            total = len(test_results)

            for i, result in enumerate(test_results, 1):
                status = "✅ PASS" if result['passed'] else "❌ FAIL"
                print(f"{i}. Button '{result['button']}': {status} - {result['message']}")

            print(f"\nResults: {passed}/{total} tests passed")
            print("="*60)

            # Keep browser open for manual inspection
            print("\n⏸️  Browser will stay open for 10 seconds for manual inspection...")
            time.sleep(10)

            return passed == total

        except Exception as e:
            print(f"\n❌ Test failed with error: {str(e)}")
            page.screenshot(path='/tmp/calendar_error.png', full_page=True)
            print("📸 Error screenshot saved: /tmp/calendar_error.png")
            return False

        finally:
            browser.close()
            print("\n✅ Browser closed")


if __name__ == '__main__':
    print("="*60)
    print("  Calendar Date Click & Highlighting Test")
    print("="*60)
    print("\n⚠️  Make sure the webapp is running:")
    print("    make webapp")
    print("\nStarting test in 3 seconds...")
    time.sleep(3)

    success = test_calendar_highlighting()

    sys.exit(0 if success else 1)
