---
name: rn-webapp-e2e-test
description: Automate E2E testing for React Native-based WebApps using Playwright with mobile viewport simulation. Use this skill when the user provides a local development URL (e.g., http://localhost:19006, http://localhost:8081) and requests testing of specific features, user flows, or UI interactions on a mobile web application. Ideal for RN projects running in web mode (Expo web, React Native Web).
---

# RN WebApp E2E Test

## Overview

Automate end-to-end testing for React Native WebApps using Playwright with mobile browser emulation. Test user flows, interactions, and features on mobile viewport configurations with automatic screenshot capture, console log monitoring, and detailed test reporting.

## When to Use This Skill

Activate this skill when:
- User provides a local development URL for a React Native WebApp
- User requests E2E testing of specific features or flows
- Keywords: "test", "e2e", "playwright", "mobile", "webapp", "flow"
- Testing login flows, form submissions, navigation, button interactions
- Validating responsive mobile UI behavior

**Not for**: Native React Native app testing (requires Appium/Detox), API-only testing, unit tests

## Quick Start

### Basic Test Request
```
"Test the home page at http://localhost:19006"
"Test login flow at http://localhost:8081"
"Test form submission on /contact"
```

### Workflow
1. **Setup**: Configure mobile viewport (375x667 iPhone SE default)
2. **Navigate**: Connect to provided local URL
3. **Interact**: Execute requested user actions
4. **Validate**: Verify expected outcomes
5. **Report**: Generate results with screenshots and logs

## Core Testing Capabilities

### 1. Navigation Testing

**Purpose**: Verify page loads and renders correctly on mobile viewport

**Steps**:
1. Resize browser to mobile viewport using `mcp__playwright__browser_resize`
2. Navigate to URL with `mcp__playwright__browser_navigate`
3. Wait for page load with `mcp__playwright__browser_wait_for`
4. Capture page snapshot with `mcp__playwright__browser_snapshot`
5. Take screenshot with `mcp__playwright__browser_take_screenshot`
6. Verify key elements present in snapshot
7. Report results with evidence

**Example Request**: "Test the home page at http://localhost:19006"

### 2. Login Flow Testing

**Purpose**: Validate authentication flow on mobile

**Steps**:
1. Setup mobile viewport (375x667)
2. Navigate to login page
3. Capture initial state snapshot
4. Type email using `mcp__playwright__browser_type` with email input selector
5. Type password using `mcp__playwright__browser_type` with password input selector
6. Click login button using `mcp__playwright__browser_click`
7. Wait for navigation/response
8. Capture logged-in state snapshot
9. Verify authentication success (check for user profile, dashboard, etc.)
10. Get console logs with `mcp__playwright__browser_console_messages`
11. Report with screenshots at each key step

**Example Request**: "Test login flow at http://localhost:8081"

### 3. Form Submission Testing

**Purpose**: Test form handling, validation, and submission

**Steps**:
1. Mobile viewport setup
2. Navigate to form page
3. Capture initial form state
4. Fill all form fields using `mcp__playwright__browser_fill_form` or individual `browser_type` calls
5. Capture filled form state
6. Submit form (click submit button)
7. Wait for submission response
8. Verify success/error message
9. Check console for errors
10. Review network requests with `mcp__playwright__browser_network_requests`
11. Report with screenshots and evidence

**Example Request**: "Test the contact form submission"

### 4. Button Interaction Testing

**Purpose**: Test button clicks and resulting UI changes

**Steps**:
1. Setup mobile viewport
2. Navigate to page
3. Capture initial state
4. Click target button using `mcp__playwright__browser_click`
5. Wait for action completion
6. Capture new state snapshot
7. Verify UI changes (modals, alerts, navigation)
8. Check console logs for errors
9. Report results with before/after screenshots

**Example Request**: "Test the 'Add to Cart' button functionality"

### 5. Scroll and Content Loading

**Purpose**: Test scroll behavior and lazy loading

**Steps**:
1. Mobile viewport setup
2. Navigate to page
3. Scroll to bottom using `mcp__playwright__browser_evaluate` with scroll script
4. Wait for lazy-loaded content
5. Verify new content appears
6. Check network requests for data fetching
7. Report results

**Example Request**: "Test infinite scroll on the feed page"

### 6. Multi-Step Flow Testing

**Purpose**: Test complex user journeys with multiple steps

**Steps**:
1. Setup mobile viewport
2. Navigate to starting point
3. Execute step 1, capture state, verify
4. Execute step 2, capture state, verify
5. Continue through all flow steps
6. Verify final state
7. Collect evidence at each step (screenshots, logs)
8. Generate comprehensive flow report

**Example Request**: "Test the complete checkout flow from cart to payment"

## Mobile Configuration

### Default Viewport
```
Width: 375px (iPhone SE)
Height: 667px
isMobile: true
hasTouch: true
deviceScaleFactor: 2
```

### User Agent
```
iOS Safari (default):
Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)
AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0
Mobile/15E148 Safari/604.1
```

### Alternative Viewports
Use `scripts/common_tests.py` for other device configurations:
- iPhone 12: 390x844
- iPhone 14 Pro: 393x852
- Pixel 5: 393x851
- Samsung S21: 360x800

## Element Selection Strategy

### Selector Priority (Most to Least Reliable)

1. **Text Content** (Most reliable)
   ```
   text="Login"
   text="Submit Form"
   text="Add to Cart"
   ```

2. **ARIA Labels** (Semantic)
   ```
   [aria-label="menu"]
   [aria-labelledby="header"]
   ```

3. **Data Test IDs** (Test-specific)
   ```
   [data-testid="login-button"]
   [data-test="submit-form"]
   ```

4. **Roles** (Semantic HTML)
   ```
   role="button"
   role="navigation"
   ```

5. **CSS Selectors** (Last resort)
   ```
   button[type="submit"]
   .submit-button
   ```

Refer to `references/playwright_mobile_guide.md` for comprehensive selector examples.

## Wait Strategies

### When to Wait

1. **After Navigation**: Use `browser_wait_for` with navigation/response conditions
2. **Before Interaction**: Ensure elements are visible before clicking/typing
3. **After Form Submit**: Wait for network idle or success message
4. **For Animations**: Add brief wait (1000ms) for CSS transitions
5. **For Lazy Load**: Wait for specific elements or network requests

### Default Timeouts
```
Page load: 30000ms
Element visible: 10000ms
Network idle: 5000ms
Animation: 1000ms
```

## Evidence Collection

### Always Capture

1. **Screenshots**
   - Initial page state
   - Before critical actions
   - After interactions
   - Error states
   - Success states
   - Final test state

2. **Console Logs**
   - Errors (critical issues)
   - Warnings (potential problems)
   - Network errors (failed requests)
   - React errors (component issues)

3. **Network Requests**
   - API calls (status codes, timing)
   - Failed requests (4xx, 5xx)
   - Slow requests (>1s)

## Test Report Format

Generate structured test reports using this format:

```markdown
## Test Results: [Feature Name]

**URL**: [local-url]
**Device**: iPhone SE (375x667)
**Status**: ✅ PASS | ❌ FAIL

### Test Steps
1. [Step description] - ✅
2. [Step description] - ✅
3. [Step description] - ❌

### Evidence
- Screenshots: [list paths]
- Console logs: [errors/warnings found]
- Network requests: [relevant API calls]

### Issues Found
- [Issue 1 with description]
- [Issue 2 with description]

### Recommendations
- [Actionable suggestion 1]
- [Actionable suggestion 2]
```

## Error Handling

### Common Issues

**Connection Failed**
- **Symptoms**: Cannot connect to URL
- **Solutions**: Verify server running with `curl -I [url]`, check port, verify URL

**Element Not Found**
- **Symptoms**: Selector doesn't match any elements
- **Solutions**: Use `browser_snapshot` to see available elements, try alternative selectors, add wait time

**Timeout Exceeded**
- **Symptoms**: Operation takes too long
- **Solutions**: Increase wait time, check network tab, verify page isn't stuck loading

**Console Errors**
- **Symptoms**: JavaScript errors in console
- **Solutions**: Review error stack, check React component issues, verify dependencies loaded

## Debugging Workflow

When tests fail:

1. **Capture current state** with `browser_snapshot`
2. **Get console logs** with `browser_console_messages(onlyErrors=true)`
3. **Review network** with `browser_network_requests`
4. **Take screenshot** for visual debugging
5. **Adjust selectors** if elements not found
6. **Increase waits** if timing issues
7. **Report findings** with evidence

## Pre-Test Checklist

Before running tests:

- ✅ Verify dev server is running (curl/browser check)
- ✅ Confirm correct URL and port
- ✅ Install Playwright browser if needed: `mcp__playwright__browser_install`
- ✅ Identify key elements to test
- ✅ Define success criteria

## Resources

### scripts/common_tests.py
Contains reusable utilities:
- Mobile viewport configurations for different devices
- Common user agents (iOS Safari, Android Chrome)
- Element selector patterns for typical RN components
- Wait time recommendations
- Test result template

**Usage**: Reference this file when setting up tests for different devices or when needing standard selector patterns.

### references/playwright_mobile_guide.md
Comprehensive reference covering:
- Detailed test patterns with step-by-step workflows
- Element selection strategies with examples
- Wait strategies and timing best practices
- Console log monitoring guidelines
- Screenshot capture best practices
- Network request analysis
- Mobile-specific considerations (touch, performance, accessibility)
- Debugging failed tests workflow

**Usage**: Load this file when encountering complex testing scenarios, debugging issues, or needing detailed Playwright mobile testing guidance.

## Integration with RN Development

### Common RN WebApp Ports
```
Expo Web: http://localhost:19006
Metro Bundler: http://localhost:8081
Custom Dev Server: varies
```

### Testing After Changes
1. Make code changes
2. Verify hot reload completes
3. Run E2E test to validate
4. Review console for new errors
5. Iterate as needed

### Continuous Testing
- Run tests after feature implementation
- Validate critical flows before commits
- Test on different viewports for responsive design
- Monitor performance with network analysis

## Limitations

### Current Scope
- ✅ WebApp testing (browser-based RN web builds)
- ✅ Mobile viewport simulation with touch emulation
- ✅ User flow and interaction testing
- ✅ Screenshot and console log capture

### Not Supported
- ❌ Native RN app testing (requires Appium/Detox)
- ❌ Device-specific native features (camera, sensors, biometrics)
- ❌ Native module functionality testing
- ❌ iOS/Android platform-specific APIs

### Workarounds
For native app testing, consider:
- Expo Go for manual device testing
- Detox for native E2E automation
- Appium for cross-platform native testing

## Tips for Effective Testing

### Server Verification
Always verify the dev server before testing:
```bash
# Check server status
curl -I http://localhost:19006

# Verify response
# Should see HTTP/1.1 200 OK
```

### Selector Best Practices
- Prefer text content for buttons/links
- Use data-testid for dynamic elements
- Avoid fragile CSS class selectors
- Test selectors in browser DevTools first

### Performance Monitoring
- Check page load times (<3s on WiFi)
- Monitor bundle size impact
- Verify smooth scrolling (60fps)
- Test on simulated 3G network

### Accessibility Validation
- Verify tap target sizes (44x44px minimum)
- Check color contrast ratios
- Test keyboard navigation
- Validate ARIA labels

## Examples

### Example 1: Home Page Navigation
```
User: "Test the home page at http://localhost:19006"

Execution:
1. Resize to 375x667 mobile viewport
2. Navigate to http://localhost:19006
3. Wait for page load (network idle)
4. Snapshot page structure
5. Verify header, navigation, key content
6. Screenshot current state
7. Check console for errors
8. Report: PASS with screenshot evidence
```

### Example 2: Login Flow
```
User: "Test login with email test@example.com"

Execution:
1. Mobile viewport setup
2. Navigate to /login
3. Screenshot initial state
4. Type "test@example.com" in email field
5. Type password in password field
6. Screenshot filled form
7. Click "Login" button
8. Wait for navigation
9. Verify dashboard/profile loaded
10. Screenshot success state
11. Check console logs
12. Report: PASS/FAIL with evidence
```

### Example 3: Form Validation
```
User: "Test the contact form with empty fields"

Execution:
1. Mobile viewport setup
2. Navigate to /contact
3. Screenshot empty form
4. Click submit without filling
5. Wait for validation messages
6. Screenshot error state
7. Verify error messages visible
8. Check console for validation logs
9. Report: PASS with error message evidence
```
