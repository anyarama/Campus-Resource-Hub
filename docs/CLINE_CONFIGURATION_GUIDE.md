# Cline AI Configuration & Best Practices Guide
## Campus Resource Hub Project

---

## 📋 Table of Contents
1. [What We've Set Up](#what-weve-set-up)
2. [How Cline Will Use .clinerules](#how-cline-will-use-clinerules)
3. [Recommended Cursor Settings](#recommended-cursor-settings)
4. [Effective Prompting Strategies](#effective-prompting-strategies)
5. [AI-First Development Workflow](#ai-first-development-workflow)
6. [Context Management Tips](#context-management-tips)
7. [Common Prompting Patterns](#common-prompting-patterns)
8. [Troubleshooting & Tips](#troubleshooting--tips)

---

## 🎯 What We've Set Up

### 1. Project-Specific .clinerules File
I've created a comprehensive `.clinerules` file in your project root that includes:

- **Project Context**: Timeline, goals, grading criteria
- **Architecture Constraints**: MVC pattern, Data Access Layer requirements
- **Technology Stack**: Flask 3.x, SQLAlchemy, pytest, etc.
- **Security Requirements**: CSRF, XSS, password hashing, file upload security
- **Code Quality Standards**: Naming conventions, file organization, testing requirements
- **AI-First Development Requirements**: Folder structure, logging practices
- **Enterprise UI/UX Standards**: Design goals, components, accessibility
- **Prompt Engineering Examples**: Ready-to-use prompts for different tasks
- **Workflow Best Practices**: Git strategy, daily checklist, common mistakes

### 2. What This Means for You

Every time you interact with Cline, it will:
✅ Understand your project's architecture requirements
✅ Follow security best practices automatically
✅ Use proper naming conventions
✅ Implement correct file structure
✅ Apply enterprise-grade patterns
✅ Remember to log AI interactions

---

## 🔧 How Cline Will Use .clinerules

### Automatic Enforcement
Cline will use the `.clinerules` file to:

1. **Architectural Decisions**
   - Always use Flask App Factory pattern
   - Separate controllers, services, DAL, and models
   - Never put business logic in route handlers

2. **Security by Default**
   - Always include CSRF tokens in forms
   - Use bcrypt for password hashing
   - Sanitize file uploads
   - Use parameterized queries

3. **Code Quality**
   - Add type hints to all functions
   - Include docstrings
   - Follow naming conventions (snake_case, PascalCase, UPPER_SNAKE_CASE)

4. **Testing**
   - Write tests alongside code
   - Minimum 70% coverage
   - Include security tests

### How It Works
```
Your Prompt → Cline reads .clinerules → Applies constraints → Generates code
                                    ↓
                            Validates against rules
                                    ↓
                            Suggests best practices
```

---

## ⚙️ Recommended Cursor Settings

### 1. Enable Cline Terminal Integration
You mentioned you've already done this - great! This allows Cline to:
- Run commands directly
- Execute tests
- Run linters and formatters
- Interact with Git

### 2. Cursor Settings for This Project

**Settings → Extensions → Cline**:
```json
{
  "cline.autoExecuteApprovedCommands": false,  // Keep manual approval for safety
  "cline.maxFileSize": 5000000,  // 5MB limit for reading files
  "cline.alwaysInclude": [
    ".clinerules",
    "docs/context/**",
    ".prompt/dev_notes.md"
  ]
}
```

### 3. Enable Cursor Composer for Complex Tasks
- Use Composer mode (Ctrl/Cmd + I) for multi-file changes
- Cline can work with Composer for larger refactoring

### 4. Set Up .cursorrules (Optional Enhancement)
While `.clinerules` is for Cline, `.cursorrules` helps Cursor's inline suggestions:

```markdown
# .cursorrules (create in project root)
This is a Flask web app following MVC pattern.
- Use type hints
- Follow PEP 8
- Security-first approach
- Test-driven development
```

---

## 💬 Effective Prompting Strategies

### 1. Context-Rich Prompts (MOST IMPORTANT)

**❌ Bad Prompt**:
```
"Create a booking function"
```

**✅ Good Prompt**:
```
"Create a booking conflict detection function in src/services/booking_service.py.
It should:
1. Accept resource_id, start_datetime, end_datetime as parameters
2. Query existing approved bookings via BookingRepository from data_access layer
3. Check for overlaps using datetime comparison
4. Return True if conflict exists, False otherwise
5. Include type hints and docstring
6. Handle edge cases: same start/end time, midnight boundary crossings

Follow the Data Access Layer pattern specified in .clinerules."
```

**Why it's better**:
- Specifies exact file location
- Lists clear requirements
- References architecture (DAL)
- Mentions edge cases
- Points to .clinerules for context

### 2. Multi-Step Prompts for Complex Features

**Example: Implementing Authentication System**

```
Step 1: "Create the User model in src/models/user.py following the database 
        schema in .clinerules. Include user_id, name, email, password_hash, 
        role, and timestamps."

Step 2: "Create UserRepository in src/data_access/user_repository.py with 
        methods: create_user, get_user_by_email, update_user, delete_user.
        Use SQLAlchemy queries with error handling."

Step 3: "Create authentication routes in src/controllers/auth.py for:
        - POST /auth/register (with bcrypt password hashing)
        - POST /auth/login (with Flask-Login session)
        - POST /auth/logout
        Include CSRF protection and proper validation."

Step 4: "Write pytest unit tests in tests/test_auth.py covering:
        - Successful registration
        - Duplicate email rejection
        - Correct password verification
        - Failed login attempts"
```

### 3. Reference Existing Code

**Template**:
```
"Following the pattern I used in [existing file], create [new component].
The existing [X] does [Y], and the new one should do [Z] similarly."
```

**Example**:
```
"Following the pattern used in src/data_access/user_repository.py, create 
src/data_access/resource_repository.py with CRUD methods for Resource model.
Use the same error handling and session management approach."
```

---

## 🔄 AI-First Development Workflow

### Daily Routine with Cline

#### Morning/Start of Session:
```
1. Review: "Show me the current state of [feature I'm working on]"
2. Plan: "Based on .clinerules, what's the best approach for [today's task]?"
3. Execute: Work through implementation step-by-step
```

#### During Development:
```
1. Implement: "Create [component] following [architecture pattern]"
2. Review: Read generated code, understand logic
3. Test: "Write tests for [component] covering [scenarios]"
4. Refactor: "Improve [function] by [specific improvement]"
5. Document: "Update README with [new feature] instructions"
```

#### End of Session:
```
1. Commit: "Help me write a commit message for these changes"
2. Log: "Add entry to .prompt/dev_notes.md documenting today's work"
3. Plan ahead: "What should I tackle next based on the todo list?"
```

### Complete Example: Building Resource Search

**Prompt 1**: Planning
```
"I want to implement the resource search feature. Based on the requirements in 
.clinerules and the project brief, help me break this down into sub-tasks with 
the correct file locations and architecture layers."
```

**Prompt 2**: Data Layer
```
"Implement search_resources method in src/data_access/resource_repository.py.
It should accept filters: keyword, category, location, date_range, capacity.
Build dynamic SQLAlchemy query with joins if needed. Return paginated results.
Include type hints and error handling."
```

**Prompt 3**: Service Layer
```
"Create SearchService in src/services/search_service.py that:
1. Validates search parameters
2. Calls ResourceRepository.search_resources
3. Formats results for display (including availability preview)
4. Handles empty results gracefully
Follow the service layer pattern from .clinerules."
```

**Prompt 4**: Controller
```
"Create search route in src/controllers/resources.py:
- GET /resources/search
- Accept query parameters: q, category, location, date, capacity
- Call SearchService
- Render search results template
- Include CSRF protection
- Handle pagination"
```

**Prompt 5**: Frontend
```
"Create search results page template in templates/resources/search_results.html:
- Search form with filters (reusable component)
- Results grid with resource cards
- Pagination controls
- Empty state message when no results
- Loading spinner
Follow Bootstrap 5 + custom CSS from static/css/custom.css"
```

**Prompt 6**: Testing
```
"Write pytest tests in tests/test_search.py:
- Test search by keyword
- Test multiple filters combined
- Test pagination
- Test empty results
- Test SQL injection prevention (should be safe)
Use fixtures for sample data."
```

**Prompt 7**: Documentation
```
"Update docs/API.md with the search endpoint:
- Path and method
- Query parameters
- Response format
- Example requests
- Error codes"
```

---

## 📚 Context Management Tips

### 1. Always Reference .clinerules
When starting any new feature:
```
"Per .clinerules, I need to implement [feature]. Let's follow the [specific section] 
guidelines."
```

### 2. Use the AI-First Folder Structure

Create these folders early:
```bash
.prompt/
├── dev_notes.md
└── golden_prompts.md

docs/
└── context/
    ├── APA/
    ├── DT/
    ├── PM/
    └── shared/
```

### 3. Log Everything Important

After each significant Cline interaction:
```
"Add an entry to .prompt/dev_notes.md documenting:
- What feature we just built
- The prompts that worked well
- Any issues encountered and how we solved them
- Code review notes"
```

### 4. Build a Golden Prompts Library

When a prompt works exceptionally well:
```
"Add this prompt to .prompt/golden_prompts.md under the category [Feature Type]"
```

Example golden_prompts.md structure:
```markdown
# Golden Prompts - Campus Resource Hub

## Database & Models
**Prompt**: "Create [model] in src/models/[name].py following SQLAlchemy ORM..."
**Result**: Perfect model with all relationships and constraints

## Testing
**Prompt**: "Write comprehensive pytest tests for [feature] covering..."
**Result**: 95% coverage with edge cases

## UI Components
**Prompt**: "Create enterprise-grade [component] with..."
**Result**: Professional, accessible, responsive component
```

---

## 🎨 Common Prompting Patterns

### Pattern 1: Feature Implementation
```
"Implement [feature name] with the following requirements:

Architecture:
- Model: src/models/[name].py
- Repository: src/data_access/[name]_repository.py
- Service: src/services/[name]_service.py
- Controller: src/controllers/[name].py
- Templates: templates/[name]/

Requirements:
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

Security:
- [Security consideration 1]
- [Security consideration 2]

Follow the architecture in .clinerules. Start with the model layer."
```

### Pattern 2: Bug Fix
```
"There's an issue with [feature] in [file]:

Current behavior: [what's happening]
Expected behavior: [what should happen]
Error message: [paste error]

Please:
1. Identify the root cause
2. Propose a fix following our architecture
3. Ensure it doesn't break existing functionality
4. Add a test to prevent regression"
```

### Pattern 3: Refactoring
```
"The [file/function] violates .clinerules by [specific violation].

Current code location: [file:line]

Please refactor to:
1. Follow [specific pattern from .clinerules]
2. Maintain existing functionality
3. Improve [specific aspect]
4. Update related tests
5. Document the changes"
```

### Pattern 4: Testing
```
"Write comprehensive pytest tests for [feature] in tests/test_[name].py:

Test cases:
1. Happy path: [expected behavior]
2. Edge case: [scenario]
3. Error case: [scenario]
4. Security: [security test]

Use pytest fixtures for:
- [fixture 1]
- [fixture 2]

Aim for 80%+ coverage. Include docstrings explaining what each test validates."
```

### Pattern 5: Documentation
```
"Update documentation for [feature]:

Files to update:
- README.md: [what to add]
- docs/API.md: [endpoint documentation]
- .prompt/dev_notes.md: [development log]

Include:
- Code examples
- API request/response samples
- Setup instructions if needed
- Screenshots if UI change"
```

---

## 🚀 Advanced Techniques

### 1. Chain of Thought Prompting
```
"Let's implement the booking conflict detection step by step:

Step 1: First, explain the algorithm logic in pseudocode
Step 2: Then, identify edge cases we need to handle
Step 3: Now, implement in src/services/booking_service.py
Step 4: Finally, write tests covering all cases"
```

### 2. Constraint-Based Prompting
```
"Create admin dashboard with these constraints:
- MUST use Flask blueprints
- MUST implement RBAC (@require_role('admin'))
- MUST follow responsive design (320px to 1920px)
- MUST include loading states
- MUST pass accessibility checks (WCAG 2.1 AA)
- MUST NOT put queries in controller (use service layer)"
```

### 3. Example-Driven Prompting
```
"Create a review submission form similar to Airbnb's:
- Star rating selector (1-5)
- Text area for comments
- Character count (max 500)
- Submit/cancel buttons
- Validation messages
- Disable form after submission
Use Bootstrap 5 + our custom.css variables"
```

### 4. Comparison Prompting
```
"Compare these two approaches for [problem]:

Approach A: [description]
Pros: ...
Cons: ...

Approach B: [description]
Pros: ...
Cons: ...

Recommend the best approach for our project considering .clinerules constraints
and implement it."
```

---

## 🔍 Troubleshooting & Tips

### Common Issues & Solutions

#### Issue 1: Cline Not Following Architecture
**Problem**: Cline puts business logic in controllers

**Solution**:
```
"STOP. This violates .clinerules section 'Architecture Constraints'.
Business logic must be in services layer, not controllers.

Please refactor to:
1. Move logic to src/services/[name]_service.py
2. Have controller only handle HTTP and call service
3. Update imports"
```

#### Issue 2: Generated Code Lacks Security
**Problem**: No CSRF tokens or password hashing

**Solution**:
```
"Review .clinerules 'Security Requirements' section. This code is missing:
- CSRF protection on forms
- bcrypt password hashing
- Input validation

Update the code to include all required security measures."
```

#### Issue 3: Tests Not Comprehensive
**Problem**: Only happy path tested

**Solution**:
```
"These tests only cover the happy path. Per .clinerules testing requirements,
add tests for:
- Edge cases: [list specific ones]
- Error cases: [list specific ones]
- Security cases: SQL injection attempt, XSS attempt

Use pytest parametrize for multiple scenarios."
```

#### Issue 4: UI Looks Generic
**Problem**: Stock Bootstrap without customization

**Solution**:
```
"This UI uses default Bootstrap without customization. Per .clinerules 
'Enterprise UI/UX Standards', we need:

1. Custom CSS variables in static/css/custom.css
2. Unique color palette
3. Custom component styling
4. Professional animations/transitions

Make this look enterprise-grade, not generic."
```

### Pro Tips

1. **Be Specific About File Locations**
   - ✅ "in src/services/booking_service.py"
   - ❌ "in the services folder"

2. **Reference .clinerules Sections**
   - ✅ "following .clinerules Architecture Constraints"
   - ❌ "using best practices"

3. **Request Incremental Changes**
   - Build layer by layer (Model → DAL → Service → Controller → Template → Test)
   - Don't ask for entire features at once

4. **Always Ask for Tests**
   - Include testing in the same prompt as implementation
   - Specify coverage requirements

5. **Review Every Generated Code**
   - Read and understand before accepting
   - Check security measures
   - Verify architecture compliance

6. **Use Git Branching**
   - One feature per branch
   - Ask Cline to help with branch naming and commit messages

7. **Document As You Go**
   - Don't wait until the end
   - Update .prompt/dev_notes.md after each session

---

## 📝 Sample .prompt/dev_notes.md Entry

```markdown
# Development Notes - Campus Resource Hub

## 2025-11-03 - Booking Conflict Detection

### Objective
Implement booking conflict detection to prevent double-booking resources.

### Prompt Used
"Implement booking conflict detection algorithm in src/services/booking_service.py.
It should check if a new booking overlaps with existing approved bookings for the 
same resource_id. Use BookingRepository from data_access layer. Include docstrings 
and type hints. Consider edge cases: same start/end time, midnight boundaries."

### AI Contribution
Cline generated:
- Initial conflict detection logic in booking_service.py
- Algorithm using datetime comparison with timezone awareness
- Proper error handling for invalid date ranges
- Comprehensive docstring

### Human Review & Modifications
✅ Accepted: Core algorithm logic was sound
✅ Accepted: Edge case handling for same start/end time
❌ Modified: Added check for booking_status to only check 'approved' bookings
❌ Modified: Improved error messages for user feedback

### Outcome
✅ Feature implemented successfully
✅ All tests passing
✅ Security review: No SQL injection risk (using ORM)
✅ Performance: Indexed queries, no N+1 issues

### Reflection
The prompt worked well because it:
- Specified exact file location
- Referenced architecture (DAL)
- Mentioned edge cases
- Requested type hints and docstrings

**Added to golden_prompts.md** ⭐

### Next Steps
- Add integration test for full booking flow
- Implement email notification on booking approval
- Add admin override for conflict resolution
```

---

## 🎯 Your Next Steps

### Immediate Actions:
1. ✅ **Done**: .clinerules file created
2. **Now**: Review this guide thoroughly
3. **Next**: Create AI-First folder structure:
   ```bash
   mkdir -p .prompt docs/context/{APA,DT,PM,shared}
   ```
4. **Then**: Initialize dev_notes.md:
   ```
   "Create .prompt/dev_notes.md with a template for logging AI interactions"
   ```
5. **Finally**: Start with planning documents (PRD, ERD, wireframes)

### Setting Up Your Development Flow:
```
Session 1 (Day 1): Planning & Setup
- Create PRD with Cline's help
- Design ERD
- Sketch wireframes
- Log in dev_notes.md

Session 2 (Days 2-3): Database & Auth
- Implement models
- Create User authentication
- Write tests
- Log golden prompts

[Continue this pattern...]
```

---

## 🏆 Success Indicators

You'll know Cline is working well when:
- ✅ Generated code follows MVC + DAL pattern automatically
- ✅ Security measures are included by default
- ✅ Tests are written alongside code
- ✅ Documentation is maintained
- ✅ Code quality is consistent
- ✅ You're building progressively without major refactoring

---

## 📞 Getting Help

If something isn't working:
1. First, check if .clinerules is in project root
2. Try explicitly referencing .clinerules in your prompt
3. Break down complex requests into smaller steps
4. Use the patterns in this guide
5. Review and modify AI-generated code carefully

---

## Summary

You now have:
- ✅ Project-specific .clinerules file
- ✅ Complete configuration guide
- ✅ Effective prompting strategies
- ✅ AI-first development workflow
- ✅ Real-world examples and patterns
- ✅ Troubleshooting guidance

**Remember**: Cline is a powerful tool, but **you** are the engineer. Review everything, understand the code, and maintain ownership of technical decisions.

**Next**: Toggle to ACT MODE and let's start building! 🚀
