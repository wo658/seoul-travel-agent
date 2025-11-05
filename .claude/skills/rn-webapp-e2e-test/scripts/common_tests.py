#!/usr/bin/env python3
"""
Common E2E test patterns for RN WebApp testing with Playwright.
Provides reusable test utilities for typical mobile web app scenarios.
"""

# Common mobile viewport configurations
MOBILE_VIEWPORTS = {
    "iphone_se": {"width": 375, "height": 667},
    "iphone_12": {"width": 390, "height": 844},
    "iphone_14_pro": {"width": 393, "height": 852},
    "pixel_5": {"width": 393, "height": 851},
    "samsung_s21": {"width": 360, "height": 800},
}

# Common user agents
USER_AGENTS = {
    "ios_safari": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "android_chrome": "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36",
}

# Test patterns documentation
TEST_PATTERNS = """
Common E2E Test Patterns for RN WebApp:

1. NAVIGATION TEST
   - Navigate to URL
   - Wait for page load
   - Verify key elements
   - Capture screenshot

2. FORM SUBMISSION TEST
   - Fill form fields
   - Submit form
   - Wait for response
   - Verify success state

3. LOGIN FLOW TEST
   - Navigate to login
   - Enter credentials
   - Submit login
   - Verify authenticated state

4. BUTTON INTERACTION TEST
   - Click button
   - Wait for action
   - Verify UI change
   - Check console logs

5. SCROLL TEST
   - Scroll to element
   - Verify element visibility
   - Check lazy loading

6. MULTI-STEP FLOW TEST
   - Navigate through steps
   - Validate each step
   - Complete flow
   - Verify final state
"""

# Common element selectors
COMMON_SELECTORS = {
    "login_button": ['text="Login"', 'text="Sign In"', '[data-testid="login-button"]', 'button[type="submit"]'],
    "submit_button": ['text="Submit"', '[data-testid="submit-button"]', 'button[type="submit"]'],
    "email_input": ['[type="email"]', '[placeholder*="email"]', '[name="email"]', '[data-testid="email-input"]'],
    "password_input": ['[type="password"]', '[placeholder*="password"]', '[name="password"]', '[data-testid="password-input"]'],
}

# Default wait times (in milliseconds)
WAIT_TIMES = {
    "page_load": 30000,
    "element_visible": 10000,
    "network_idle": 5000,
    "animation": 1000,
}

def get_mobile_config(device="iphone_se", platform="ios"):
    """
    Get mobile viewport and user agent configuration.

    Args:
        device: Device type (iphone_se, iphone_12, pixel_5, etc.)
        platform: Platform type (ios, android)

    Returns:
        dict: Configuration with viewport and userAgent
    """
    viewport = MOBILE_VIEWPORTS.get(device, MOBILE_VIEWPORTS["iphone_se"])
    user_agent = USER_AGENTS.get(f"{platform}_safari" if platform == "ios" else f"{platform}_chrome")

    return {
        "viewport": viewport,
        "userAgent": user_agent,
        "isMobile": True,
        "hasTouch": True,
        "deviceScaleFactor": 2,
    }

# Test result template
TEST_RESULT_TEMPLATE = """
## Test Results: {test_name}

**URL**: {url}
**Device**: {device}
**Status**: {status}

### Test Steps
{steps}

### Evidence
- Screenshots: {screenshots}
- Console logs: {console_logs}
- Network requests: {network_requests}

### Issues Found
{issues}

### Recommendations
{recommendations}
"""
