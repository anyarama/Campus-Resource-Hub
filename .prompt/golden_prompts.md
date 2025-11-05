# Golden Prompts - Campus Resource Hub
## Best Prompts for AI-Assisted Development

This file documents the most effective prompts used during development of the Campus Resource Hub project. When a prompt produces excellent results, it's captured here for reuse and adaptation.

---

## 📋 How to Use This File

**Purpose**: Save time by reusing proven prompts that generate high-quality code

**When to Add**:
- A prompt produces exceptional code that requires minimal modification
- A prompt saves significant development time
- A prompt handles a complex scenario elegantly
- A prompt demonstrates good architecture/security practices

**Template**:
```markdown
### [Category] - [Specific Task]

**Context**: [When this is useful]

**Prompt**:
```
[Exact prompt text]
```

**Result**: [What was generated and why it excelled]

**Reusability**: [How to adapt for similar tasks]

**Tags**: #category #feature #pattern
```

---

## 📚 Golden Prompts Collection

---

### Project Setup - Initial Configuration

**Context**: Setting up Cline AI configuration at project start

**Prompt**:
```
"Create a comprehensive .clinerules file for the Campus Resource Hub capstone project.
Include: architecture constraints (Flask App Factory + MVC + DAL), security requirements 
(CSRF, bcrypt, XSS), code quality standards (type hints, docstrings, tests), enterprise 
UI/UX standards, and prompt engineering examples. Reference the project brief requirements 
for an 18-day timeline with grading on functionality (30%), code quality (15%), UX (15%), 
testing (15%), documentation (10%), and presentation (15%)."
```

**Result**: 
- Comprehensive 2,500+ line configuration file
- Clear architecture patterns enforced
- Security requirements documented
- Prompt examples for common tasks
- Minimal need for revisions

**Reusability**: 
Adapt for any Flask project by changing:
- Project name and timeline
- Specific tech stack versions
- Domain-specific security requirements
- Custom business logic patterns

**Tags**: #setup #configuration #architecture #security

---

### Database Models - SQLAlchemy ORM

**Context**: Creating database models with proper relationships

**Prompt Template**:
```
"Create the [ModelName] model in src/models/[name].py following the database schema 
in .clinerules. Include:
- All fields specified in schema: [list fields]
- Proper SQLAlchemy column types and constraints
- Relationships to [related models]
- Indexes for [frequently queried fields]
- __repr__ method for debugging
- Type hints for all attributes
- Comprehensive docstring

Follow the ORM patterns in .clinerules."
```

**Example**:
```
"Create the User model in src/models/user.py following the database schema in .clinerules.
Include: user_id (primary key), name, email (unique), password_hash, role (student/staff/admin),
profile_image, department, created_at. Add relationship to Resource (one-to-many). Include 
proper indexes on email and role. Add type hints and docstring."
```

**Result**: 
- Clean SQLAlchemy model with proper types
- Relationships correctly defined
- Indexes for performance
- Ready for migrations

**Reusability**: Replace [ModelName], fields, and relationships for any model

**Tags**: #database #models #sqlalchemy #orm

---

### Data Access Layer - Repository Pattern

**Context**: Creating DAL layer with CRUD operations

**Prompt Template**:
```
"Create [ModelName]Repository in src/data_access/[name]_repository.py with CRUD methods:
- create_[model](data: dict) -> [Model]
- get_[model]_by_id(id: int) -> Optional[[Model]]
- get_all_[models](page: int, per_page: int) -> List[[Model]]
- update_[model](id: int, data: dict) -> [Model]
- delete_[model](id: int) -> bool

Include:
- Type hints for all methods
- Docstrings with parameter descriptions
- Error handling (try/except with logging)
- Session management with context managers
- Query optimization (eager loading where needed)

Follow the Data Access Layer pattern in .clinerules."
```

**Result**: 
- Proper separation of concerns (no SQL in controllers)
- Reusable CRUD methods
- Error handling and logging
- Type-safe interfaces

**Reusability**: Adapt for any model by replacing [ModelName] and customizing queries

**Tags**: #dal #repository #crud #database

---

### Authentication - Flask-Login Integration

**Context**: Implementing secure authentication with bcrypt

**Prompt**:
```
"Create authentication system in src/controllers/auth.py with:
- POST /auth/register: validates email, hashes password with bcrypt, creates user via UserRepository
- POST /auth/login: verifies credentials, creates Flask-Login session
- POST /auth/logout: clears session
- Include CSRF protection (Flask-WTF)
- Add server-side validation (email format, password strength min 8 chars)
- Use UserRepository from data_access layer (no direct DB calls)
- Return proper HTTP status codes and JSON responses
- Include type hints and docstrings

Follow the controller pattern in .clinerules (no business logic here, delegate to service if needed)."
```

**Result**: 
- Secure authentication with bcrypt
- CSRF protection enabled
- Clean separation (controller → repository)
- Proper status codes

**Reusability**: Standard pattern for any Flask-Login auth system

**Tags**: #authentication #security #flask-login #bcrypt #csrf

---

### Business Logic - Service Layer

**Context**: Implementing business logic with proper separation

**Prompt Template**:
```
"Create [ServiceName] in src/services/[name]_service.py with method:
[method_name]([parameters]) -> [return_type]

Business Logic:
1. [Step 1 description]
2. [Step 2 description]
3. [Step 3 description]

Requirements:
- Use [Repository] from data_access layer for all DB operations
- Include edge case handling: [list edge cases]
- Add comprehensive error handling
- Include type hints and detailed docstring
- Log important decisions/events
- Return Result object or raise custom exceptions

Follow the service layer pattern in .clinerules. This is where business logic belongs, 
not in controllers."
```

**Example - Booking Conflict Detection**:
```
"Create BookingService in src/services/booking_service.py with method:
check_booking_conflict(resource_id: int, start_datetime: datetime, end_datetime: datetime) -> bool

Business Logic:
1. Query all approved bookings for resource_id via BookingRepository
2. Check if new booking time overlaps with any existing booking
3. Handle edge cases: same start/end time, midnight boundaries, timezone awareness

Requirements:
- Use BookingRepository from data_access layer
- Return True if conflict exists, False otherwise
- Include type hints and comprehensive docstring
- Handle timezone-aware datetime objects

Follow the service layer pattern in .clinerules."
```

**Result**: 
- Business logic properly isolated
- No database calls in service (uses repository)
- Testable pure functions
- Clear responsibilities

**Reusability**: Use for any service layer logic by describing the business rules

**Tags**: #service #business-logic #architecture

---

### Testing - Pytest Unit Tests

**Context**: Writing comprehensive tests with good coverage

**Prompt Template**:
```
"Write pytest unit tests for [component] in tests/test_[name].py.

Test Coverage:
1. Happy path: [expected behavior]
2. Edge cases: [list specific scenarios]
3. Error cases: [what should fail and how]
4. Security: [security-related tests]

Requirements:
- Use pytest fixtures for [setup needs]
- Use parametrize for multiple test inputs
- Mock external dependencies (database, APIs)
- Include descriptive docstrings for each test
- Aim for 80%+ coverage
- Follow AAA pattern (Arrange, Act, Assert)

Test names should be: test_[feature]_[scenario]_[expected_result]
Example: test_booking_conflict_detection_prevents_overlap()"
```

**Example - Booking Conflict Tests**:
```
"Write pytest unit tests for BookingService.check_booking_conflict in tests/test_booking_service.py.

Test Coverage:
1. Happy path: No conflict when times don't overlap
2. Edge cases: Exact same start/end time, back-to-back bookings OK, midnight boundary
3. Error cases: Invalid datetime range (end before start)
4. Multiple bookings: Check against all existing bookings

Use pytest fixtures for:
- Sample resource_id
- Sample existing bookings
- Datetime ranges

Use parametrize for different overlap scenarios."
```

**Result**: 
- Comprehensive test coverage
- Clear test names and structure
- Proper use of fixtures and parametrize
- Security tests included

**Reusability**: Adapt by listing specific test scenarios for any component

**Tags**: #testing #pytest #unit-tests #tdd

---

### UI Components - Enterprise-Grade Templates

**Context**: Creating professional, accessible UI components

**Prompt Template**:
```
"Create [component name] template in templates/[path]/[name].html.

Design Requirements:
- Professional look (inspired by [Airbnb/Notion/Linear])
- Responsive (mobile-first, 320px to 1920px)
- Accessible (WCAG 2.1 AA):
  * Proper ARIA labels
  * Keyboard navigation
  * Color contrast 4.5:1 minimum
  * Focus indicators

Components:
- [Component 1 description]
- [Component 2 description]

Style:
- Use Bootstrap 5 base + custom CSS from static/css/custom.css
- CSS variables from :root (--primary-color, --shadow-sm, etc.)
- Smooth transitions and hover effects
- Loading states and empty states

Include:
- CSRF tokens on all forms ({{ csrf_token }})
- Client-side validation (HTML5 + custom JS)
- Error message displays
- Success feedback (toast notifications)

Follow the UI/UX standards in .clinerules."
```

**Result**: 
- Modern, professional UI (not generic Bootstrap)
- Fully accessible
- Responsive across devices
- Includes all security measures

**Reusability**: Describe the specific component needs and reference design inspiration

**Tags**: #ui #frontend #templates #accessibility #responsive

---

### API Documentation - Endpoint Specs

**Context**: Documenting API endpoints clearly

**Prompt**:
```
"Document the [endpoint path] API endpoint in docs/API.md following this format:

### [Method] [Path]

**Description**: [What this endpoint does]

**Authentication**: [Required/Optional, role requirements]

**Request**:
- **Method**: [GET/POST/PUT/DELETE]
- **Headers**: [Content-Type, CSRF token, etc.]
- **Parameters**: [Path/query parameters]
- **Body** (if applicable):
```json
{
  "field1": "type and description",
  "field2": "type and description"
}
```

**Response**:
- **Success (200/201):**
```json
{
  "status": "success",
  "data": {...}
}
```

- **Error (400/401/404):**
```json
{
  "status": "error",
  "message": "Error description"
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/[path] \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'
```

**Related**: [Links to related endpoints]"
```

**Result**: 
- Clear, consistent API docs
- Easy for developers to understand
- Includes error cases
- Has working examples

**Reusability**: Standard format for any REST API endpoint

**Tags**: #documentation #api #endpoints

---

### Refactoring - Code Cleanup

**Context**: Refactoring code to follow architecture patterns

**Prompt**:
```
"The [file/function] violates .clinerules by [specific violation].

Current issues:
1. [Issue 1: e.g., business logic in controller]
2. [Issue 2: e.g., direct database queries]
3. [Issue 3: e.g., missing type hints]

Please refactor to:
1. Move business logic to services/[name]_service.py
2. Move database operations to data_access/[name]_repository.py
3. Keep controller thin (HTTP handling only)
4. Add type hints and docstrings
5. Maintain all existing functionality
6. Update related tests

Show me the refactored files and explain the changes."
```

**Result**: 
- Clean separation of concerns
- Architecture compliance
- Improved maintainability
- Tests still passing

**Reusability**: Identify violations and specify the correct pattern

**Tags**: #refactoring #architecture #code-quality

---

### Security Audit - Vulnerability Check

**Context**: Reviewing code for security issues

**Prompt**:
```
"Security audit [feature/file] against .clinerules security requirements:

Check for:
1. CSRF protection: All forms have {{ csrf_token }}?
2. SQL injection: Using parameterized queries or ORM (no string concatenation)?
3. XSS: Jinja auto-escaping enabled, user input sanitized?
4. Password security: Using bcrypt (no plaintext)?
5. File uploads: Whitelist extensions, random filenames, size limits?
6. Authorization: Proper role checks (@require_role decorators)?
7. Input validation: Server-side validation (never trust client)?
8. Error messages: No sensitive data exposed?

For any vulnerabilities found, provide:
- Description of risk
- OWASP category
- Fix recommendation with code
- Test to verify fix"
```

**Result**: 
- Comprehensive security review
- Specific vulnerabilities identified
- Actionable fixes provided
- Tests for verification

**Reusability**: Standard checklist for any feature security review

**Tags**: #security #audit #vulnerabilities #owasp

---

### Git Workflow - Commit Messages

**Context**: Writing clear, conventional commit messages

**Prompt**:
```
"Help me write a commit message for these changes:

Changes made:
- [List what was changed]
- [What was added]
- [What was fixed]

Follow conventional commits format:
<type>: <description>

[optional body]

[optional footer]

Types: feat, fix, docs, style, refactor, test, chore

Keep first line under 50 chars, body wrapped at 72 chars. Explain why not just what."
```

**Result**: 
- Professional commit messages
- Clear git history
- Easy to generate changelogs

**Reusability**: Standard for any commit

**Tags**: #git #workflow #commits

---

## 🏷️ Tag Index

Quick reference to find prompts by category:

- **#setup** - Project initialization
- **#configuration** - Config files and settings
- **#architecture** - Structural patterns
- **#database** - Models and migrations
- **#models** - SQLAlchemy models
- **#dal** - Data Access Layer
- **#repository** - Repository pattern
- **#service** - Service layer (business logic)
- **#authentication** - Auth and security
- **#security** - Security measures
- **#testing** - Test writing
- **#pytest** - Pytest specific
- **#ui** - Frontend/templates
- **#frontend** - Client-side code
- **#accessibility** - WCAG compliance
- **#responsive** - Mobile-first design
- **#api** - API endpoints
- **#documentation** - Docs and READMEs
- **#refactoring** - Code cleanup
- **#git** - Version control
- **#workflow** - Development process

---

## 📈 Effectiveness Tracking

As you use these prompts, rate their effectiveness:

| Prompt | Times Used | Success Rate | Notes |
|--------|------------|--------------|-------|
| Initial Configuration | 1 | 100% | Minimal revisions needed |
| Database Models | - | - | To be tracked |
| Repository Pattern | - | - | To be tracked |
| Authentication | - | - | To be tracked |
| Service Layer | - | - | To be tracked |
| Testing | - | - | To be tracked |
| UI Components | - | - | To be tracked |
| Security Audit | - | - | To be tracked |

---

## 🎓 Meta-Prompts

Prompts to help you create better prompts:

### Improve a Prompt
```
"This prompt: '[paste prompt]' didn't work well because [reason]. 

Please improve it to:
1. Be more specific about [aspect]
2. Include [missing information]
3. Reference .clinerules for [constraint]
4. Add example of expected output

Show me the improved version."
```

### Generate Prompt from Example
```
"I want to create similar code to [paste example code]. 
Write a prompt that would generate this type of code, including:
- Specific file paths
- Architecture patterns to follow
- Security requirements
- Testing requirements
- References to .clinerules

Make it reusable for similar scenarios."
```

---

## 📝 Continuous Improvement

**Guidelines for Adding New Golden Prompts**:

1. **Test First**: Use the prompt at least twice successfully
2. **Document Context**: Explain when and why to use it
3. **Show Results**: Include what made the output excellent
4. **Make Reusable**: Provide adaptation guidelines
5. **Tag Properly**: Add relevant tags for searchability

**Prompt Quality Criteria**:
- ✅ Specific and detailed
- ✅ References .clinerules or architecture
- ✅ Includes acceptance criteria
- ✅ Mentions security/testing requirements
- ✅ Specifies exact file locations
- ✅ Provides context for AI

**Avoid**:
- ❌ Vague requests ("create a function")
- ❌ Missing file paths
- ❌ No architecture reference
- ❌ Ignoring security
- ❌ No testing mention
- ❌ One-time-use prompts

---

**Last Updated**: November 2, 2025  
**Next Review**: After each major feature completion  
**Total Golden Prompts**: 13

---

> 💡 **Tip**: Before starting a new feature, check this file for relevant prompts. Adapt them to your specific needs rather than starting from scratch!
