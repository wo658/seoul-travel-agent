# Issue Execution Guide

Issue 유형별 실행 패턴, 요구사항 분석 및 구현 전략

**작성 원칙:**
- 기술 용어는 영어 유지 (component, session, workflow, test, authentication 등)
- 설명과 가이드는 한글 사용
- Commit message 예시에는 한글/영어 모두 제공

## Issue Type Patterns

### Bug Fix Execution

**Workflow:**
1. 버그 이해하기 (Understand the bug)
2. 이슈 재현하기 (Reproduce the issue)
3. Root cause 파악 (Identify root cause)
4. 수정 구현 (Implement fix)
5. 수정사항 테스트 (Test fix)
6. Regression 없는지 검증 (Verify no regression)

**Step 1: 버그 이해하기**

Issue description에서 파싱할 정보:
- 현재 동작 (Current behavior - 무엇이 고장났는지)
- 예상 동작 (Expected behavior - 어떻게 동작해야 하는지)
- 재현 단계 (Reproduction steps)
- 환경 정보 (Environment details)
- Error message/log

**Issue 분석 예시:**
```markdown
## Issue: ECM-105 - bug: 세션 타임아웃 후 로그인 실패

현재 동작:
- 사용자가 login page로 redirect됨
- Credential 입력 후 login 실패
- Error: "Invalid session"

예상 동작:
- Session timeout 후 login이 성공해야 함
- 새로운 session이 생성되어야 함

재현 단계:
1. 성공적으로 login
2. 30분 대기 (session timeout)
3. Navigate 시도
4. 다시 login -> 실패

환경:
- Browser: Chrome 120
- OS: Windows 11
- Version: 0.1.0
```

**핵심 정보 추출:**
- Component: Authentication
- 영향받을 가능성 있는 파일: auth.py, session.py
- 필요한 테스트: Session timeout handling

**Step 2: Reproduce the Issue**

```bash
# Create test case to reproduce
# File: tests/test_session_timeout.py

def test_login_after_session_timeout():
    # Login
    response = login(username, password)
    assert response.status == 200

    # Simulate timeout
    time.sleep(31 * 60)  # 31 minutes

    # Try to access protected resource
    response = get_protected_resource()
    assert response.status == 401

    # Login again
    response = login(username, password)
    assert response.status == 200  # Should succeed
```

**Step 3: Identify Root Cause**

Use debugging and code inspection:
```bash
# Check session handling code
grep -r "session" backend/auth/

# Check logs
tail -f logs/app.log

# Add debug logging if needed
```

**Potential causes:**
- Session not properly cleared on timeout
- Cookie not updated after re-login
- Token validation failing

**Step 4: Implement Fix**

```python
# File: backend/auth/session.py

def login(username, password):
    # Validate credentials
    user = authenticate(username, password)

    if not user:
        return {"error": "Invalid credentials"}, 401

    # Clear any existing session
    clear_session(username)  # FIX: Added this line

    # Create new session
    session = create_session(user)

    return {"session_id": session.id}, 200
```

**Commit:**
```bash
git add backend/auth/session.py
git commit -m "fix: clear existing session on re-login (ECM-105)"
```

**Step 5: Test Fix**

```bash
# Run specific test
pytest tests/test_session_timeout.py

# Run all auth tests
pytest tests/auth/

# Manual testing
# Follow reproduction steps and verify fix
```

**Step 6: Verify No Regression**

```bash
# Run full test suite
pytest

# Check related functionality
# - Normal login still works
# - Logout works
# - Session expiry works correctly
```

**Final Commit:**
```bash
git add tests/test_session_timeout.py
git commit -m "test: add session timeout regression test (ECM-105)"
```

### Feature Implementation

**Workflow:**
1. Understand requirements
2. Design solution
3. Break down into tasks
4. Implement incrementally
5. Test functionality
6. Update documentation

**Step 1: Understand Requirements**

Parse issue for:
- Problem being solved
- User requirements
- Acceptance criteria
- UI/UX specifications
- API requirements

**Example Issue Analysis:**
```markdown
## Issue: ECM-108 - feat: Add user search functionality

Problem:
- Users cannot search for other users
- Need to find users by name or email

Requirements:
- Search API endpoint
- Search UI in user management
- Real-time search (as you type)
- Results limited to 50 users

Acceptance Criteria:
- [ ] API endpoint /api/users/search?q=query
- [ ] Returns max 50 results
- [ ] Search by name or email
- [ ] Case-insensitive search
- [ ] UI with search input and results list
- [ ] Debounced search (300ms)
```

**Step 2: Design Solution**

**Backend:**
- Endpoint: GET /api/users/search?q={query}
- Database query with LIKE operator
- Index on name and email columns for performance
- Pagination (limit 50)

**Frontend:**
- Search input component
- Debounced API calls
- Results display component
- Loading states

**Step 3: Break Down into Tasks**

Use TodoWrite to track:
```markdown
- [ ] Create database index on users.name and users.email
- [ ] Implement search API endpoint
- [ ] Add search endpoint tests
- [ ] Create search input component
- [ ] Implement debounced search
- [ ] Create results display component
- [ ] Add frontend tests
- [ ] Update API documentation
```

**Step 4: Implement Incrementally**

**Task 1: Database Index**
```sql
-- migrations/add_user_search_index.sql
CREATE INDEX idx_users_name ON users(name);
CREATE INDEX idx_users_email ON users(email);
```

```bash
git add migrations/add_user_search_index.sql
git commit -m "feat: add database indexes for user search (ECM-108)"
```

**Task 2: API Endpoint**
```python
# backend/api/users.py

@app.route('/api/users/search')
def search_users():
    query = request.args.get('q', '')

    if len(query) < 2:
        return {'users': []}, 200

    users = User.query.filter(
        or_(
            User.name.ilike(f'%{query}%'),
            User.email.ilike(f'%{query}%')
        )
    ).limit(50).all()

    return {
        'users': [user.to_dict() for user in users]
    }, 200
```

```bash
git add backend/api/users.py
git commit -m "feat: add user search API endpoint (ECM-108)"
```

**Task 3: API Tests**
```python
# tests/api/test_user_search.py

def test_search_users_by_name():
    response = client.get('/api/users/search?q=john')
    assert response.status_code == 200
    assert len(response.json['users']) <= 50

def test_search_users_by_email():
    response = client.get('/api/users/search?q=john@example.com')
    assert response.status_code == 200
    assert any(u['email'] == 'john@example.com'
               for u in response.json['users'])

def test_search_case_insensitive():
    response = client.get('/api/users/search?q=JOHN')
    assert response.status_code == 200
    assert len(response.json['users']) > 0
```

```bash
git add tests/api/test_user_search.py
git commit -m "test: add user search API tests (ECM-108)"
```

**Task 4: Frontend Component**
```javascript
// src/components/UserSearch.svelte

<script>
  import { debounce } from '$lib/utils';

  let query = '';
  let results = [];
  let loading = false;

  const searchUsers = debounce(async (q) => {
    if (q.length < 2) {
      results = [];
      return;
    }

    loading = true;
    try {
      const response = await fetch(`/api/users/search?q=${q}`);
      const data = await response.json();
      results = data.users;
    } finally {
      loading = false;
    }
  }, 300);

  $: searchUsers(query);
</script>

<div class="user-search">
  <input
    type="text"
    bind:value={query}
    placeholder="Search users..."
  />

  {#if loading}
    <div class="loading">Searching...</div>
  {:else if results.length > 0}
    <ul class="results">
      {#each results as user}
        <li>{user.name} ({user.email})</li>
      {/each}
    </ul>
  {:else if query.length >= 2}
    <div class="no-results">No users found</div>
  {/if}
</div>
```

```bash
git add src/components/UserSearch.svelte
git commit -m "feat: add user search UI component (ECM-108)"
```

**Step 5: Test Functionality**

```bash
# Backend tests
pytest tests/api/test_user_search.py

# Frontend tests (if applicable)
npm run test

# Manual testing
# - Search by name
# - Search by email
# - Verify debouncing
# - Check results limit
```

**Step 6: Update Documentation**

```markdown
# docs/api/users.md

## Search Users

GET /api/users/search?q={query}

Search for users by name or email.

### Parameters
- `q` (string, required): Search query (minimum 2 characters)

### Response
Returns up to 50 matching users.

### Example
GET /api/users/search?q=john

Response:
{
  "users": [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Johnny Smith", "email": "johnny@example.com"}
  ]
}
```

```bash
git add docs/api/users.md
git commit -m "docs: add user search API documentation (ECM-108)"
```

### Task Execution

**Workflow:**
1. Review task checklist
2. Complete each item
3. Verify completion
4. Update documentation

**Example:**
```markdown
## Issue: ECM-112 - task: Migrate to Python 3.12

Checklist:
- [ ] Update requirements.txt
- [ ] Update Dockerfile base image
- [ ] Update CI/CD Python version
- [ ] Test compatibility
- [ ] Update documentation
```

**Execute sequentially:**
```bash
# Item 1: Update requirements.txt
# ... make changes ...
git commit -m "task: update requirements for Python 3.12 (ECM-112)"

# Item 2: Update Dockerfile
# ... make changes ...
git commit -m "task: update Docker base image to Python 3.12 (ECM-112)"

# Item 3: Update CI/CD
# ... make changes ...
git commit -m "task: update CI/CD to Python 3.12 (ECM-112)"

# Item 4: Test compatibility
pytest
git commit -m "task: verify Python 3.12 compatibility (ECM-112)"

# Item 5: Update docs
# ... make changes ...
git commit -m "docs: update Python version in documentation (ECM-112)"
```

### Improvement Implementation

**Workflow:**
1. Measure baseline
2. Implement improvement
3. Measure improvement
4. Document results

**Example:**
```markdown
## Issue: ECM-115 - improve: Optimize database query performance

Current Performance:
- Query time: 2.5s
- Database hits: 50 queries (N+1 problem)

Goal:
- Query time: <500ms
- Database hits: <5 queries

Solution:
- Use eager loading
- Add database indexes
- Implement caching
```

**Step 1: Measure Baseline**
```python
# Add profiling
import time

start = time.time()
results = get_users_with_posts()
duration = time.time() - start

print(f"Query time: {duration}s")
print(f"Query count: {db.query_count}")
```

**Step 2: Implement Improvement**
```python
# Before (N+1 problem)
users = User.query.all()
for user in users:
    posts = user.posts  # Separate query for each user

# After (eager loading)
users = User.query.options(
    joinedload(User.posts)
).all()
for user in users:
    posts = user.posts  # No additional query
```

```bash
git commit -m "improve: use eager loading for user posts (ECM-115)"
```

**Step 3: Measure Improvement**
```python
# Profile again
start = time.time()
results = get_users_with_posts()
duration = time.time() - start

print(f"Query time: {duration}s")  # 0.3s (83% improvement)
print(f"Query count: {db.query_count}")  # 2 queries
```

**Step 4: Document Results**
```markdown
## Performance Results

Before:
- Query time: 2.5s
- Database queries: 50

After:
- Query time: 0.3s (83% improvement)
- Database queries: 2 (96% reduction)

Changes:
- Implemented eager loading with joinedload
- Added composite index on (user_id, created_at)
- Reduced N+1 queries

Testing:
- Benchmarked with 100 users, 10 posts each
- Verified same results returned
- No regression in other queries
```

## Requirement Parsing

### Acceptance Criteria

Extract clear, measurable completion conditions:

**Example:**
```markdown
Acceptance Criteria:
- [ ] Users can search by name
- [ ] Users can search by email
- [ ] Search is case-insensitive
- [ ] Results limited to 50 users
- [ ] Search updates as user types
- [ ] Tests added and passing
```

**Map to Implementation:**
- Criteria 1-4 → Backend API
- Criteria 5 → Frontend debouncing
- Criteria 6 → Test coverage

### Dependency Identification

Look for:
- Blocked by other issues
- Required infrastructure/tools
- External service dependencies
- Team coordination needs

**Example:**
```markdown
Dependencies:
- Blocked by ECM-105 (auth refactor must complete first)
- Requires ElasticSearch setup
- Needs design approval from UX team
```

### File and Component Identification

Parse issue for mentioned:
- File paths
- Component names
- API endpoints
- Database tables

**Create search strategy:**
```bash
# Find relevant files
grep -r "user search" src/
grep -r "SearchComponent" frontend/

# Check existing similar functionality
grep -r "search" src/api/
```

## Implementation Strategies

### Incremental Development

**Benefits:**
- Early feedback
- Easier debugging
- Progressive complexity
- Commit history clarity

**Approach:**
1. Start with simplest version
2. Add one feature at a time
3. Test after each addition
4. Commit working code

**Example:**
```bash
# Iteration 1: Basic search
git commit -m "feat: add basic user search (ECM-108)"

# Iteration 2: Add email search
git commit -m "feat: add email search to user search (ECM-108)"

# Iteration 3: Add pagination
git commit -m "feat: add pagination to search results (ECM-108)"

# Iteration 4: Optimize performance
git commit -m "improve: optimize search query performance (ECM-108)"
```

### Test-Driven Development

**Workflow:**
1. Write test (fails)
2. Implement feature (test passes)
3. Refactor (tests still pass)
4. Commit

**Example:**
```python
# Step 1: Write test
def test_user_search():
    result = search_users("john")
    assert len(result) > 0
# Test fails - function doesn't exist

# Step 2: Implement
def search_users(query):
    return User.query.filter(
        User.name.ilike(f'%{query}%')
    ).all()
# Test passes

# Step 3: Refactor
def search_users(query, limit=50):
    return User.query.filter(
        or_(
            User.name.ilike(f'%{query}%'),
            User.email.ilike(f'%{query}%')
        )
    ).limit(limit).all()
# Tests still pass

# Step 4: Commit
git commit -m "feat: implement user search with TDD (ECM-108)"
```

### Documentation-First Development

**For complex features:**
1. Write documentation first
2. Define API contracts
3. Implement to spec
4. Update docs with examples

**Example:**
```markdown
# Step 1: Document API
## User Search API

GET /api/users/search?q={query}&limit={limit}

Parameters:
- q: search query (required)
- limit: max results (optional, default 50)

Response:
{
  "users": [...],
  "total": 123,
  "limit": 50
}

# Step 2: Implement to match spec
# ... implementation ...

# Step 3: Add examples
curl '/api/users/search?q=john&limit=10'
```

## Testing Approaches

### Unit Testing

Test individual functions/methods:

```python
def test_search_query_builder():
    query = build_search_query("john")
    assert "ILIKE" in str(query)
    assert "%john%" in str(query)

def test_search_sanitization():
    result = sanitize_search_query("test'; DROP TABLE users--")
    assert "DROP" not in result
    assert ";" not in result
```

### Integration Testing

Test component interaction:

```python
def test_search_endpoint_integration():
    # Setup: Create test users
    create_user("John Doe", "john@example.com")
    create_user("Jane Smith", "jane@example.com")

    # Execute: Call API
    response = client.get('/api/users/search?q=john')

    # Verify: Check response
    assert response.status_code == 200
    assert len(response.json['users']) == 1
    assert response.json['users'][0]['name'] == "John Doe"
```

### End-to-End Testing

Test complete user workflows:

```python
def test_user_search_workflow():
    # User opens search page
    page.goto('/users/search')

    # User types search query
    page.fill('input[name="search"]', 'john')

    # Wait for results
    page.wait_for_selector('.search-results')

    # Verify results displayed
    results = page.query_selector_all('.user-result')
    assert len(results) > 0

    # User clicks on result
    results[0].click()

    # Verify user profile opens
    assert '/users/1' in page.url
```

### Manual Testing Checklist

After implementation:

- [ ] Happy path works
- [ ] Edge cases handled
- [ ] Error cases handled
- [ ] UI is responsive
- [ ] Loading states work
- [ ] No console errors
- [ ] Performance acceptable
- [ ] Works in different browsers (if frontend)
- [ ] Accessibility tested (if frontend)

## Common Patterns

### API Implementation Pattern
1. Define route and parameters
2. Validate input
3. Process request
4. Handle errors
5. Return response
6. Add tests

### UI Component Pattern
1. Create component structure
2. Add state management
3. Implement user interactions
4. Add loading/error states
5. Style component
6. Add accessibility
7. Test functionality

### Database Change Pattern
1. Create migration
2. Test migration (up and down)
3. Update models/schemas
4. Update queries
5. Add indexes if needed
6. Test with real data

### Bug Fix Pattern
1. Reproduce bug
2. Add failing test
3. Fix code
4. Verify test passes
5. Check for regression
6. Document fix
