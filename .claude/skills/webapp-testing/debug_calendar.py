#!/usr/bin/env python3
"""
Debug calendar date selection and styling issue
"""
from playwright.sync_api import sync_playwright
import time

def debug_calendar():
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=False)  # Non-headless to see what's happening
        page = browser.new_page(viewport={'width': 1280, 'height': 800})

        print("Navigating to http://localhost:8081...")
        page.goto('http://localhost:8081')

        # Wait for page to load
        print("Waiting for page to load...")
        page.wait_for_load_state('networkidle')
        time.sleep(2)  # Extra wait for React Native Web

        # Take initial screenshot
        print("Taking initial screenshot...")
        page.screenshot(path='/tmp/calendar_debug_01_home.png', full_page=True)

        # Find and click the "여행 계획 만들기" button
        print("Looking for travel planning button...")
        try:
            planning_button = page.get_by_text('여행 계획 만들기')
            planning_button.click()
            print("Clicked planning button")

            # Wait for form to load
            page.wait_for_load_state('networkidle')
            time.sleep(2)

            # Take screenshot of form
            print("Taking form screenshot...")
            page.screenshot(path='/tmp/calendar_debug_02_form.png', full_page=True)

            # Find calendar
            print("Looking for calendar...")
            calendar = page.locator('.react-native-calendars')
            if calendar.count() == 0:
                print("Calendar component not found, trying alternative selector...")
                calendar = page.locator('[data-testid*="calendar"], .calendar, [class*="Calendar"]')

            print(f"Found {calendar.count()} calendar elements")

            # Get all date cells
            print("Looking for date cells...")
            date_cells = page.locator('text=/^[0-9]{1,2}$/').all()
            print(f"Found {len(date_cells)} date cells")

            if len(date_cells) > 0:
                # Click first available date (not disabled)
                print("Clicking first date...")
                date_cells[10].click()  # Skip first few days (might be from previous month)
                time.sleep(1)

                # Take screenshot after first click
                page.screenshot(path='/tmp/calendar_debug_03_first_date.png', full_page=True)

                # Click second date
                print("Clicking second date...")
                date_cells[15].click()
                time.sleep(1)

                # Take screenshot after second click
                page.screenshot(path='/tmp/calendar_debug_04_second_date.png', full_page=True)

                # Get computed styles of selected dates
                print("\nInspecting calendar styling...")

                # Get the calendar HTML
                calendar_html = page.locator('.react-native-calendars, [class*="calendar"]').first.inner_html()
                with open('/tmp/calendar_debug_html.html', 'w') as f:
                    f.write(calendar_html)
                print("Saved calendar HTML to /tmp/calendar_debug_html.html")

                # Check for period marking classes
                marked_dates = page.locator('[class*="period"], [class*="marked"], [style*="background"]').all()
                print(f"\nFound {len(marked_dates)} elements with marking styles")

                for i, elem in enumerate(marked_dates[:5]):  # First 5 only
                    try:
                        style = elem.get_attribute('style')
                        class_name = elem.get_attribute('class')
                        print(f"\nElement {i}:")
                        print(f"  Class: {class_name}")
                        print(f"  Style: {style}")
                    except:
                        pass

            else:
                print("No date cells found!")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path='/tmp/calendar_debug_error.png', full_page=True)

        print("\nScreenshots saved to /tmp/calendar_debug_*.png")
        print("HTML saved to /tmp/calendar_debug_html.html")

        # Keep browser open for manual inspection
        print("\nBrowser will close in 10 seconds...")
        time.sleep(10)

        browser.close()

if __name__ == '__main__':
    debug_calendar()
