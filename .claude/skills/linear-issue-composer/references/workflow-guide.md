# Linear Workflow Guide

Comprehensive workflow guidance for creating and managing Linear issues with MCP integration.

## Priority Determination

### Priority Matrix

| Priority | Linear Value | Severity | Examples |
|----------|--------------|----------|----------|
| Urgent | 1 | Critical production issues | App crashes, data loss, security breaches |
| High | 2 | Major functionality broken | Key features unavailable, blocking bugs |
| Medium | 3 | Standard work | Normal features, improvements, non-critical bugs |
| Low | 4 | Nice-to-have | Cosmetic issues, minor improvements |

### Decision Tree

```
Is production down or users unable to use the app?
├─ YES → Priority 1 (Urgent)
└─ NO → Is a major feature completely broken?
    ├─ YES → Priority 2 (High)
    └─ NO → Is this blocking other work?
        ├─ YES → Priority 2 (High)
        └─ NO → Is this a standard feature/improvement?
            ├─ YES → Priority 3 (Medium)
            └─ NO → Priority 4 (Low)
```

### Context-Based Priority Guidelines

**Bug Priority:**
- Critical severity → Priority 1
- High severity → Priority 2
- Medium severity → Priority 3
- Low severity → Priority 4

**Feature Priority:**
- Urgent business need → Priority 2
- Important enhancement → Priority 3
- Nice-to-have → Priority 4

**Task Priority:**
- Blocking other work → Priority 2
- Time-sensitive → Priority 2
- Regular maintenance → Priority 3
- When time allows → Priority 4

**Improvement Priority:**
- Security vulnerability → Priority 1
- Performance degradation → Priority 2
- Code quality → Priority 3
- Technical debt → Priority 3-4

## Label Selection

### Label Categories

#### Area Labels
Indicate which part of the codebase is affected:
- `frontend` - UI, components, client-side code
- `backend` - Server, API, database
- `docs` - Documentation changes
- `infra` - Infrastructure, deployment, DevOps
- `api` - API endpoints, integrations

#### Component Labels
Specify the feature or module:
- `chat` - Chat functionality
- `auth` - Authentication and authorization
- `settings` - User/system settings
- `admin` - Admin panel features
- `rag` - RAG (Retrieval-Augmented Generation)
- `models` - AI model integration
- `tools` - Tool functionality
- `ui` - General UI/UX

#### Size Labels
Estimate work effort:
- `size-small` - <1 day of work
- `size-medium` - 1-3 days of work
- `size-large` - >3 days of work

#### Type Labels (if available)
- `type-bug` - Bug fixes
- `type-feature` - New features
- `type-improvement` - Enhancements
- `type-task` - Maintenance work

### Label Selection Guidelines

**Minimum Labels:**
- Always add at least one area label
- Add component label when applicable
- Include size estimate for planning

**Maximum Labels:**
- Keep to 3-5 labels for clarity
- Avoid redundant or conflicting labels

**Label Priority:**
1. Area (required)
2. Component (recommended)
3. Size (recommended for features/improvements)
4. Additional context labels (optional)

### Retrieving Available Labels

Use Linear MCP to get current labels:

```javascript
// Get teams with labels
const teams = await linear_get_teams();

// Teams response includes:
teams.forEach(team => {
  console.log(`Team: ${team.name}`);
  console.log('Labels:', team.labels.nodes.map(l => ({
    id: l.id,
    name: l.name,
    description: l.description
  })));
});
```

## Issue Relationship Management

### Relationship Types

**Blocked By (선행 작업)**
- This issue cannot start until the blocking issue is completed
- Use when there's a hard dependency
- Example: "Feature implementation" blocked by "API design"

**Blocks (후행 작업)**
- The current issue must be completed before the blocked issue can start
- Inverse of "Blocked By"
- Example: "Database schema" blocks "API implementation"

**Related To (관련 이슈)**
- Issues that share context but no hard dependency
- Use for related features, similar bugs, or contextual links
- Example: Related bug reports in the same area

**Duplicate Of (중복)**
- The current issue is a duplicate of another issue
- Close the duplicate and keep the original
- Link to provide context and search history

### When to Link Issues

**Always link when:**
- Issues have dependencies (blocked by/blocks)
- Multiple bugs have the same root cause (related to)
- Similar features are being developed (related to)
- Issue is a duplicate (duplicate of)

**Consider linking when:**
- Issues affect the same code area
- Issues are part of the same feature set
- Issues share the same assignee/timeline

### Linking Best Practices

1. **Use specific relationships** - Don't use "related to" for dependencies
2. **Document the relationship** - Add a comment explaining why they're linked
3. **Keep links current** - Remove links when dependencies change
4. **Avoid circular dependencies** - Check for dependency loops

## Linear MCP Integration Patterns

### Basic Issue Creation Flow

```javascript
// Step 1: Get teams and metadata
const teams = await linear_get_teams();
const targetTeam = teams.find(t => t.name === "Engineering");

// Step 2: Prepare issue data
const issueData = {
  title: "bug: Login fails after session timeout",
  description: markdownContent,
  teamId: targetTeam.id,
  priority: 2, // High priority
  labelIds: [
    labelFrontend.id,
    labelAuth.id,
    labelSizeMedium.id
  ]
};

// Step 3: Create issue
const result = await linear_create_issue(issueData);

// Step 4: Confirm creation
console.log(`Created issue: ${result.issue.identifier}`);
```

### Batch Issue Creation

For multiple related issues:

```javascript
const issues = [
  {
    title: "feat: User dashboard UI",
    description: dashboardDesc,
    teamId: teamId,
    priority: 3
  },
  {
    title: "feat: User dashboard API",
    description: apiDesc,
    teamId: teamId,
    priority: 3
  },
  {
    title: "task: Dashboard documentation",
    description: docsDesc,
    teamId: teamId,
    priority: 4
  }
];

const result = await linear_create_issues({ issues });
```

### Project with Issues

For feature work spanning multiple issues:

```javascript
const projectData = {
  project: {
    name: "User Dashboard Feature",
    description: "Complete user dashboard implementation",
    teamIds: [teamId] // Note: array of team IDs
  },
  issues: [
    {
      title: "feat: Dashboard UI",
      description: uiDesc,
      teamId: teamId
    },
    {
      title: "feat: Dashboard API",
      description: apiDesc,
      teamId: teamId
    }
  ]
};

const result = await linear_create_project_with_issues(projectData);
```

### Issue Updates and Edits

```javascript
// Get issue by identifier
const issue = await linear_get_issue({ identifier: "ENG-123" });

// Edit issue
await linear_edit_issue({
  issueId: issue.id, // UUID, not identifier
  priority: 1, // Escalate to Urgent
  stateId: inProgressState.id,
  assigneeId: userId
});
```

### Bulk Updates

```javascript
// Update multiple issues at once
await linear_bulk_update_issues({
  issueIds: [issue1.id, issue2.id, issue3.id],
  update: {
    priority: 2,
    stateId: targetState.id
  }
});
```

## Common Workflows

### Bug Triage Workflow

1. **Assess Severity**
   - Review bug description and impact
   - Determine priority (1-4)

2. **Add Context**
   - Add environment labels (frontend/backend)
   - Add component labels
   - Link related issues if applicable

3. **Route Issue**
   - Assign to appropriate team member if known
   - Add to current sprint if urgent/high priority

4. **Track Resolution**
   - Update status as work progresses
   - Link to PR when fixed
   - Close when deployed and verified

### Feature Planning Workflow

1. **Define Scope**
   - Write clear problem definition
   - Outline solution approach
   - Define acceptance criteria

2. **Break Down Work**
   - Create sub-tasks if feature is large
   - Use "blocked by" relationships for dependencies
   - Estimate size (small/medium/large)

3. **Organize**
   - Add to project or milestone
   - Set priority based on business needs
   - Add relevant labels

4. **Implementation**
   - Update status to "In Progress"
   - Link PR when ready
   - Request review

5. **Completion**
   - Verify acceptance criteria met
   - Update documentation
   - Close issue

### Improvement Planning Workflow

1. **Document Current State**
   - Measure current performance/quality
   - Identify specific problems
   - Show impact and scope

2. **Propose Solution**
   - Describe improvement approach
   - Estimate impact
   - Identify risks

3. **Get Buy-in**
   - Add to backlog with appropriate priority
   - Discuss in planning if high impact
   - Assign based on expertise

4. **Execute and Measure**
   - Implement changes
   - Measure improvements against baseline
   - Document results

5. **Follow-up**
   - Close issue with summary
   - Create follow-up issues if needed
   - Share learnings with team

## Error Handling

### Common Errors and Solutions

**Error: Team not found**
- Solution: Use `linear_get_teams()` to get valid team IDs
- Check team name spelling
- Verify team permissions

**Error: Invalid label ID**
- Solution: Get labels from team metadata
- Verify label exists in target team
- Check label ID format (UUID)

**Error: Invalid priority value**
- Solution: Use values 1-4 only
- 0 is also valid (no priority)
- Default is 3 if not specified

**Error: Issue not found**
- Solution: Use UUID (from `issue.id`), not identifier ("ENG-123")
- For searches, use `linear_get_issue()` with identifier
- Then use returned UUID for updates

**Error: Permission denied**
- Solution: Verify Linear access token is valid
- Check user has write permissions
- Confirm team membership

### Debugging Tips

1. **Always fetch fresh metadata** - Teams, labels, and states can change
2. **Log issue IDs** - Keep track of created issue UUIDs
3. **Test with simple issues first** - Verify connection before complex operations
4. **Validate input** - Check all required fields before API calls
5. **Handle partial failures** - In batch operations, some may succeed while others fail

## Best Practices Summary

### Issue Creation
1. Choose correct issue type based on work nature
2. Fill all required template sections
3. Use clear, concise titles (under 50 characters)
4. Set appropriate priority (1-4)
5. Add relevant labels (area, component, size)
6. Link related issues
7. Never use emojis

### Issue Management
1. Keep issues focused on single problems/features
2. Update status as work progresses
3. Add comments for significant updates
4. Link PRs when implementation starts
5. Close issues with resolution summary

### Team Collaboration
1. Use labels for categorization and filtering
2. Set priorities to guide team focus
3. Link dependencies to show relationships
4. Assign issues to appropriate team members
5. Use projects for organizing related work

### Quality Standards
1. Professional, technical tone
2. Specific, actionable descriptions
3. Complete template sections
4. Proper markdown formatting
5. No emojis or decorative elements
