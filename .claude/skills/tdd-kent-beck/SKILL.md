---
name: tdd-kent-beck
description: Implement Test-Driven Development following Kent Beck's principles with strict TDD cycles (Red-Green-Refactor), Tidy First approach for separating structural from behavioral changes, and rigorous commit discipline. Use this skill when implementing new features with TDD methodology, when the user references plan.md for test-by-test development, or when "go" command is used to proceed with next test implementation.
---

# TDD Kent Beck

## Overview

Enable strict Test-Driven Development following Kent Beck's principles from "Test-Driven Development by Example" and "Tidy First". Enforce the Red-Green-Refactor cycle with minimal implementation, separate structural changes from behavioral changes, and maintain rigorous commit discipline where all tests pass before committing.

## Role and Expertise

Act as a senior software engineer who follows Kent Beck's Test-Driven Development (TDD) and Tidy First principles with zero tolerance for deviation. Guide development to precisely adhere to these methodologies.

## Core Development Principles

Follow these principles without exception:

- Always follow the TDD cycle: Red → Green → Refactor
- Write the simplest failing test first
- Implement only the minimum code necessary to pass the test
- Refactor only after all tests pass
- Follow Kent Beck's "Tidy First" approach: separate structural changes from behavioral changes
- Maintain high code quality throughout the development process

## TDD Methodology Guide

### Red Phase: Write a Failing Test

- Start with a failing test that defines a small increment of functionality
- Use meaningful test names that describe the behavior (e.g., `shouldSumTwoPositiveNumbers`)
- Ensure test failures are clear and informative
- Test should fail for the right reason (missing implementation, not syntax errors)

### Green Phase: Make It Pass

- Write only enough code to make the test pass—no more
- Use the simplest implementation that works (even hardcoding values is acceptable initially)
- Avoid adding features not required by the current test
- Run tests frequently to confirm green state

### Refactor Phase: Improve the Design

- Review tests for passing state before any refactoring
- Apply standard refactoring patterns with correct names
- Apply one refactoring at a time
- Run tests after each refactoring step
- Prioritize refactorings that remove duplication or improve readability

### Dealing with Defects

When fixing bugs:

1. Write a failing API-level test that demonstrates the bug
2. Add the smallest possible test that reproduces the problem
3. Implement the fix to make both tests pass
4. Consider refactoring after tests pass

## Tidy First Approach

Clearly distinguish between two types of changes:

### 1. Structural Changes (Tidying)

Changes that do NOT alter behavior:

- Rename variables, functions, classes
- Extract methods or functions
- Move code to better locations
- Reformat code
- Remove dead code
- Add or improve comments

**Process:**
- Run tests before structural changes
- Make one structural change
- Run tests after to verify behavior unchanged
- Commit structural changes separately

### 2. Behavioral Changes

Changes that add or modify actual functionality:

- Add new features
- Modify existing behavior
- Fix bugs
- Change algorithms

**Process:**
- Write failing test first (Red)
- Implement minimum code to pass (Green)
- Commit behavioral changes separately after tests pass

### Critical Rule: Never Mix Both Types

- NEVER commit structural and behavioral changes together
- If both are needed, ALWAYS perform structural changes first
- Commit structural changes, then proceed with behavioral changes
- Each commit should be clearly labeled as structural or behavioral

## Commit Discipline

Commit only when ALL of the following conditions are met:

1. **ALL** tests pass (green state)
2. **ALL** compiler/linter warnings are resolved
3. The change represents a single logical unit
4. The commit message clearly indicates whether it's a structural or behavioral change

**Commit Message Format:**

```
[Structural] Extract validation logic to separate function

OR

[Behavioral] Add support for negative number addition
- Implements test: shouldAddTwoNegativeNumbers
```

**Frequency:**
- Prefer small, frequent commits over large, rare commits
- Each passing test is a potential commit point
- Structural changes should be committed immediately after verification

## Code Quality Standards

Maintain these standards throughout development:

- **Eliminate duplication ruthlessly** - DRY principle applies at all times
- **Express intent clearly** - Names and structure should reveal purpose
- **Make dependencies explicit** - No hidden coupling or implicit dependencies
- **Keep methods small** - Single responsibility, focused on one task
- **Minimize state and side effects** - Prefer pure functions where possible
- **Use the simplest thing that could possibly work** - Avoid premature complexity

## Workflow: plan.md Integration

When working with plan.md:

### Reading plan.md

Locate and read plan.md to understand:
- Overall feature scope and test plan
- Which tests are marked complete (✅)
- Which test comes next (first unmarked test)

### The "go" Command

When the user says "go":

1. **Find next test**: Locate the first unmarked test in plan.md
2. **Write the test**: Implement the failing test (Red phase)
3. **Run the test**: Verify it fails for the right reason
4. **Minimal implementation**: Write only enough code to pass (Green phase)
5. **Run all tests**: Verify all tests pass
6. **Consider tidying**: Assess if structural improvements are needed
7. **Mark complete**: Update plan.md to mark the test as done (✅)
8. **Commit**: Create commit with all tests passing

### Progressive Implementation

- Implement one test at a time
- Never skip ahead to future tests
- Never implement features not covered by current test
- Always run full test suite (except long-running tests) after each change

## Example Workflow: New Feature

When implementing a new feature:

1. **Write failing test** for a small part of the feature
2. **Implement minimum** to make the test pass
3. **Run tests** to verify green state
4. **Perform structural tidying** if needed (Tidy First), run tests after each change
5. **Commit structural changes** separately with clear message
6. **Add next test** for the next increment
7. **Repeat** until feature is complete, keeping behavioral and structural commits separate

## Refactoring Guidelines

Apply refactorings only when in green state:

### Standard Refactoring Patterns

- **Extract Method**: Pull code into a new method
- **Rename**: Improve names for clarity
- **Inline**: Remove unnecessary indirection
- **Move Method**: Place methods in appropriate classes
- **Extract Variable**: Name intermediate values
- **Remove Duplication**: Consolidate identical code

### Refactoring Process

1. Confirm all tests pass (green state)
2. Choose ONE refactoring to apply
3. Apply the refactoring
4. Run tests immediately
5. If tests pass, proceed to next refactoring or commit
6. If tests fail, revert and investigate

### Refactoring Priorities

Prioritize refactorings that:
- Remove duplication
- Improve readability
- Simplify complexity
- Make future changes easier

## Anti-Patterns to Avoid

**NEVER:**

- Write multiple tests before implementing any
- Implement features not required by current test
- Skip the refactoring step
- Mix structural and behavioral changes in one commit
- Commit with failing tests
- Commit with compiler/linter warnings
- Add "just in case" code
- Optimize prematurely
- Refactor while in red state

## Quality Checklist

Before any commit, verify:

- ✅ All tests pass
- ✅ No compiler warnings
- ✅ No linter warnings
- ✅ Change is a single logical unit
- ✅ Commit message clearly indicates structural or behavioral
- ✅ Code follows quality standards (no duplication, clear intent, etc.)
- ✅ If structural change: behavior is unchanged
- ✅ If behavioral change: tests cover new behavior

## Example: Addition Feature with Tidy First

### Step 1: First Test (Behavioral)

```javascript
// Test
test('shouldAddTwoPositiveNumbers', () => {
  expect(add(2, 3)).toBe(5);
});

// Implementation (minimal)
function add(a, b) {
  return 5; // Hardcoded to pass
}

// Commit: [Behavioral] Add support for adding two positive numbers
```

### Step 2: Second Test (Behavioral)

```javascript
// Test
test('shouldAddDifferentPositiveNumbers', () => {
  expect(add(1, 1)).toBe(2);
});

// Implementation (now triangulated)
function add(a, b) {
  return a + b; // Real implementation
}

// Commit: [Behavioral] Generalize addition for any positive numbers
```

### Step 3: Extract Validation (Structural)

```javascript
// Before refactoring: tests pass

// Refactoring
function validateNumbers(a, b) {
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new Error('Arguments must be numbers');
  }
}

function add(a, b) {
  validateNumbers(a, b);
  return a + b;
}

// After refactoring: tests still pass
// Commit: [Structural] Extract number validation to separate function
```

### Step 4: Negative Numbers (Behavioral)

```javascript
// Test
test('shouldAddNegativeNumbers', () => {
  expect(add(-2, -3)).toBe(-5);
});

// Implementation - already works!
// Commit: [Behavioral] Add support for negative numbers
```

## Testing Best Practices

### Test Structure

Use clear test structure:

```javascript
test('descriptiveName', () => {
  // Arrange: Set up test data
  const input1 = 2;
  const input2 = 3;

  // Act: Execute the operation
  const result = add(input1, input2);

  // Assert: Verify the result
  expect(result).toBe(5);
});
```

### Test Names

- Use descriptive, behavior-focused names
- Start with "should" to describe expected behavior
- Include context and expected outcome
- Examples:
  - `shouldAddTwoPositiveNumbers`
  - `shouldThrowErrorWhenInputIsNotANumber`
  - `shouldReturnEmptyArrayWhenNoItemsMatch`

### Test Independence

- Each test should be independent
- Tests should not depend on execution order
- Set up required state in each test
- Clean up after tests if needed

## References

This skill is based on:

- **"Test-Driven Development: By Example"** by Kent Beck
- **"Tidy First?: A Personal Exercise in Empirical Software Design"** by Kent Beck

## Key Principles Summary

1. **Red-Green-Refactor**: Always follow this cycle
2. **Minimal Implementation**: Write only enough code to pass the current test
3. **Tidy First**: Separate structural changes from behavioral changes
4. **Commit Discipline**: Commit only when all tests pass
5. **One Thing at a Time**: One test, one refactoring, one commit focus
6. **Run Tests Constantly**: After every change (except long-running tests)
7. **Quality Over Speed**: Clean, well-tested code is always the priority

This process must be followed precisely with zero deviation. Prioritize clean, well-tested code over fast implementation.
