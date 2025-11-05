# Playwright Mobile Testing Guide for RN WebApps

## Overview

Comprehensive reference for testing React Native WebApps using Playwright with mobile viewport emulation.

## Mobile Configuration

### Viewport Sizes
```javascript
// Common mobile viewports
iPhone SE:      375 x 667
iPhone 12:      390 x 844
iPhone 14 Pro:  393 x 852
Pixel 5:        393 x 851
Samsung S21:    360 x 800
```

### User Agents
```
iOS Safari:
Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1

Android Chrome:
Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36
```

## Common Test Patterns

### 1. Basic Navigation Test
```markdown
Purpose: Verify page loads and key elements render

Steps:
1. Set mobile viewport (375x667)
2. Navigate to URL
3. Wait for page load (wait for network idle)
4. Capture snapshot
5. Verify key elements present
6. Take screenshot
7. Report results
```

### 2. Login Flow Test
```markdown
Purpose: Test authentication flow

Steps:
1. Setup mobile viewport
2. Navigate to login page
3. Capture initial state
4. Type email into email field
5. Type password into password field
6. Click login button
7. Wait for navigation/response
8. Verify logged-in state
9. Capture success state
10. Report with evidence
```

### 3. Form Submission Test
```markdown
Purpose: Test form handling and validation

Steps:
1. Mobile viewport setup
2. Navigate to form page
3. Capture initial form state
4. Fill all required fields
5. Capture filled state
6. Submit form
7. Wait for response
8. Verify success/error state
9. Check console for errors
10. Report with screenshots
```

### 4. Button Interaction Test
```markdown
Purpose: Test button click and resulting actions

Steps:
1. Setup mobile viewport
2. Navigate to page
3. Capture initial state
4. Click target button
5. Wait for action completion
6. Verify UI changes
7. Check console logs
8. Report results
```

### 5. Scroll and Lazy Load Test
```markdown
Purpose: Test scroll behavior and lazy loading

Steps:
1. Mobile viewport setup
2. Navigate to page
3. Scroll to bottom
4. Wait for lazy load
5. Verify new content loaded
6. Check network requests
7. Report results
```

### 6. Multi-Step Flow Test
```markdown
Purpose: Test complex user journeys

Steps:
1. Setup mobile viewport
2. Navigate to start page
3. Complete step 1, verify
4. Navigate to step 2
5. Complete step 2, verify
6. Continue through all steps
7. Verify final state
8. Capture evidence at each step
9. Report complete flow
```

## Element Selection Strategies

### Priority Order
1. **Text content**: Most reliable for user-facing elements
   - `text="Login"`
   - `text="Submit Form"`

2. **ARIA labels**: Semantic and accessible
   - `[aria-label="menu"]`
   - `[aria-labelledby="header"]`

3. **Data attributes**: Test-specific selectors
   - `[data-testid="login-button"]`
   - `[data-test="submit-form"]`

4. **Roles**: Semantic HTML roles
   - `role="button"`
   - `role="navigation"`

5. **CSS selectors**: Last resort
   - `button[type="submit"]`
   - `.submit-button`

### Common Selectors
```javascript
// Login elements
Email input:    [type="email"], [placeholder*="email"], [name="email"]
Password input: [type="password"], [placeholder*="password"], [name="password"]
Login button:   text="Login", text="Sign In", [data-testid="login-button"]

// Form elements
Submit button:  text="Submit", [data-testid="submit-button"], button[type="submit"]
Text input:     [type="text"], input[name="..."]
Checkbox:       [type="checkbox"], input[role="checkbox"]

// Navigation
Menu button:    [aria-label="menu"], text="Menu", [data-testid="menu"]
Back button:    text="Back", [aria-label="back"], button[data-action="back"]
```

## Wait Strategies

### Wait Times (milliseconds)
```javascript
Page load:        30000  // Wait for full page load
Element visible:  10000  // Wait for element to appear
Network idle:     5000   // Wait for network requests to settle
Animation:        1000   // Wait for CSS animations
```

### Wait Methods
```markdown
1. Wait for navigation: After clicking links/buttons that navigate
2. Wait for element: Before interacting with elements
3. Wait for text: When verifying text content appears
4. Wait for network: After form submissions or API calls
5. Custom timeout: For slow-loading content
```

## Console Log Handling

### Log Levels to Monitor
- **Error**: Critical issues, failed operations
- **Warning**: Potential problems, deprecations
- **Info**: General information, debug data

### Common Issues to Check
```javascript
// Network errors
Failed to fetch
404 Not Found
500 Internal Server Error

// JavaScript errors
Uncaught TypeError
ReferenceError
SyntaxError

// React errors
Warning: Failed prop type
Error: Maximum update depth exceeded
```

## Screenshot Best Practices

### When to Capture
1. Initial page state
2. Before critical actions
3. After interactions
4. Error states
5. Success states
6. Final test state

### Naming Convention
```
{test-name}-{step}-{timestamp}.png

Examples:
login-flow-initial-20240105-143022.png
form-submit-success-20240105-143045.png
button-click-error-20240105-143101.png
```

## Network Request Monitoring

### Requests to Monitor
1. API calls (POST, GET, PUT, DELETE)
2. Asset loading (images, fonts, scripts)
3. Failed requests (4xx, 5xx errors)
4. Slow requests (>3s response time)

### Request Analysis
```markdown
Status codes:
- 2xx: Success
- 3xx: Redirect
- 4xx: Client error
- 5xx: Server error

Performance:
- <200ms: Fast
- 200-500ms: Acceptable
- 500ms-1s: Slow
- >1s: Very slow
```

## Error Handling

### Common Errors

#### Connection Failed
```
Symptoms: Cannot connect to URL
Causes: Server not running, wrong port, firewall
Solutions: Verify server running, check URL, test with curl
```

#### Element Not Found
```
Symptoms: Element not visible/clickable
Causes: Wrong selector, timing issue, element hidden
Solutions: Verify selector, add wait, check element state
```

#### Timeout Exceeded
```
Symptoms: Operation takes too long
Causes: Slow network, heavy page, infinite loading
Solutions: Increase timeout, check network, verify page state
```

#### Console Errors
```
Symptoms: JavaScript errors in console
Causes: Code bugs, missing dependencies, runtime errors
Solutions: Review error stack, check code, verify dependencies
```

## Mobile-Specific Considerations

### Touch Events
- Use click for tap simulation
- Playwright automatically converts to touch events on mobile
- Consider long press for context menus

### Viewport Changes
- Test portrait and landscape orientations
- Verify responsive breakpoints
- Check viewport meta tag

### Performance
- Monitor page load time
- Check bundle size impact
- Verify smooth scrolling
- Test on slower network (3G)

### Accessibility
- Verify tap target size (minimum 44x44px)
- Check contrast ratios
- Test keyboard navigation
- Verify screen reader compatibility

## Debugging Failed Tests

### Step-by-Step Debugging
1. **Review console messages**
   - Check for JavaScript errors
   - Look for network failures
   - Verify API responses

2. **Examine screenshots**
   - Compare actual vs expected state
   - Check element positioning
   - Verify content rendering

3. **Analyze network requests**
   - Verify API calls made
   - Check request/response data
   - Look for failed requests

4. **Validate selectors**
   - Test selector in browser DevTools
   - Verify element exists
   - Check timing issues

5. **Adjust wait times**
   - Increase timeout for slow operations
   - Add explicit waits
   - Wait for specific conditions

## Best Practices

### Test Organization
1. One test per user flow
2. Clear test names describing scenario
3. Modular test steps
4. Reusable helper functions

### Assertions
1. Verify critical elements present
2. Check expected text content
3. Validate URLs/navigation
4. Confirm data persistence

### Evidence Collection
1. Screenshots at key steps
2. Console logs for debugging
3. Network request logs
4. Performance metrics

### Maintenance
1. Use stable selectors (data-testid)
2. Avoid brittle CSS selectors
3. Document test purpose
4. Update tests with UI changes
