# Product Requirements Document (PRD)
## Campus Resource Hub

**Project**: Campus Resource Hub - AiDD 2025 Capstone Project  
**Version**: 1.0  
**Date**: November 2, 2025  
**Author**: Aneesh Yaramati  
**Timeline**: 18 days (November 2-20, 2025)  

---

## 1. Executive Summary

### Problem Statement
University students, faculty, and staff currently lack a centralized platform to discover, book, and manage campus resources such as study rooms, equipment, lab instruments, event spaces, and tutoring services. This leads to:
- Underutilization of valuable campus resources
- Double bookings and scheduling conflicts
- Poor visibility into resource availability
- Manual, time-consuming booking processes
- Lack of accountability and feedback mechanisms

### Solution
Campus Resource Hub is a full-stack web application that enables departments, organizations, and individuals to **list, share, and reserve** campus resources through an intuitive, secure platform. The system features intelligent search, automated conflict detection, role-based access control, peer reviews, and AI-powered assistance.

---

## 2. Objectives & Success Metrics

### Primary Objectives
1. **Streamline Resource Management**: Enable efficient listing, discovery, and booking of campus resources
2. **Prevent Conflicts**: Implement robust conflict detection and approval workflows
3. **Enhance Transparency**: Provide visibility into resource availability and booking history
4. **Build Trust**: Foster accountability through ratings, reviews, and admin oversight
5. **Demonstrate Technical Excellence**: Showcase production-quality software engineering skills

### Success Metrics
- **Functionality**: All core features working correctly (30% of grade)
- **Code Quality**: Clean architecture, security, documentation (15% of grade)
- **User Experience**: Professional UI/UX, accessibility (15% of grade)
- **Testing**: 70%+ coverage, security validation (15% of grade)
- **Documentation**: Complete technical docs, AI logs (10% of grade)
- **Presentation**: Professional demo and reflection (15% of grade)

---

## 3. Stakeholders

### Primary Users
1. **Students**: Book study rooms, equipment; request resources; leave reviews
2. **Staff/Faculty**: List department resources; manage approvals; access advanced features
3. **Administrators**: Oversee all resources; moderate content; generate reports; manage users

### Secondary Stakeholders
- **Kelley MSIS Faculty**: Professor Jay Newquist (grading, evaluation)
- **Development Team**: Solo developer (Aneesh Yaramati)
- **Future Users**: Potential campus community members if deployed

---

## 4. Core Features (Required)

### 4.1 User Management & Authentication
**Priority**: P0 (Critical)

- User registration with email + password (bcrypt hashing)
- Secure login/logout with Flask-Login sessions
- Three role levels:
  - **Student**: Basic booking and listing
  - **Staff**: Resource approval capabilities
  - **Admin**: Full system management
- Profile management with department, profile image

**Acceptance Criteria**:
- Users can register with valid email and strong password
- Passwords stored as bcrypt hashes (never plaintext)
- CSRF protection on all forms
- Role-based access control enforced on all protected routes
- Session timeout after 1 hour of inactivity

### 4.2 Resource Listings
**Priority**: P0 (Critical)

- CRUD operations for resources with:
  - Title, description, category, location
  - Capacity, equipment lists
  - Image uploads (max 2MB, .jpg/.png/.gif only)
  - Availability rules (JSON format)
  - Owner information
- Resource lifecycle: draft → published → archived
- Rich text descriptions with proper sanitization

**Acceptance Criteria**:
- Resource owners can create, edit, delete their listings
- Images validated for type and size (per .clinerules security)
- Admins can moderate/archive any resource
- Published resources visible in search
- Draft resources only visible to owner

### 4.3 Search & Discovery
**Priority**: P0 (Critical)

- Search by:
  - Keyword (title, description)
  - Category (study rooms, equipment, spaces, tutoring)
  - Location (building, floor)
  - Availability (date/time range)
  - Capacity (minimum required)
- Sort options:
  - Most recent
  - Most booked
  - Highest rated
- Pagination (20 items per page)

**Acceptance Criteria**:
- Search returns accurate results within 2 seconds
- Multiple filters can be combined
- Empty states provide helpful guidance
- SQL injection attempts prevented (ORM-based queries)

### 4.4 Booking & Scheduling
**Priority**: P0 (Critical)

- Calendar-based booking interface
- Conflict detection algorithm:
  - Check overlapping start/end times
  - Handle edge cases (midnight boundaries, same-time requests)
  - Prevent double-booking
- Booking workflow:
  - Student requests → Pending status
  - Auto-approve for open resources
  - Staff/admin approval for restricted resources
  - Email/notification on status change
- Booking statuses: pending, approved, rejected, cancelled, completed

**Acceptance Criteria**:
- No overlapping bookings for same resource
- Conflict detection works across date boundaries
- Approval workflow enforced based on resource settings
- Users notified of booking status changes
- Cancelled bookings free up the time slot

### 4.5 Messaging & Notifications
**Priority**: P1 (High)

- Message threads between requester and resource owner
- Inbox/sent views
- Notification badges for unread messages
- Basic threading support

**Acceptance Criteria**:
- Messages delivered between users
- Thread history preserved
- Unread count displayed accurately
- XSS protection on message content (Jinja auto-escaping)

### 4.6 Reviews & Ratings
**Priority**: P1 (High)

- Post-booking reviews (1-5 stars + comment)
- Authorization: Only after completed booking
- Aggregate rating calculation
- Display on resource detail page
- Optional: "Verified Booking" badge

**Acceptance Criteria**:
- Users can only review after completed booking
- One review per booking
- Aggregate ratings update in real-time
- Admin can moderate/remove abusive reviews

### 4.7 Admin Dashboard
**Priority**: P1 (High)

- User management (view, suspend, delete)
- Resource moderation
- Booking approval queue
- Usage analytics:
  - Most booked resources
  - Active users
  - Department usage reports
- Action logging (audit trail)

**Acceptance Criteria**:
- Admin can access all management features
- Analytics load within 3 seconds
- All admin actions logged for audit
- Non-admins cannot access admin routes

---

## 5. AI-Powered Feature (Required)

### Selected: **Resource Concierge** (AI-Assisted Search)
**Priority**: P1 (High)

Natural language query interface that helps users find resources:
- Example queries:
  - "Find a study room for 4 people tomorrow afternoon"
  - "I need a projector for my presentation next Tuesday"
  - "Show me available lab equipment this weekend"
- AI parses query → extracts parameters → searches database
- Returns results with helpful suggestions
- Grounded in real data (no fabrications)

**Implementation**:
- OpenAI API or local LLM (Ollama)
- Model Context Protocol (MCP) for safe database access
- Logged in `.prompt/dev_notes.md`

**Acceptance Criteria**:
- AI correctly interprets common queries (80%+ accuracy)
- Only returns resources that actually exist in database
- Graceful fallback if AI service unavailable
- All AI decisions logged for transparency

---

## 6. Non-Functional Requirements

### 6.1 Security (Per .clinerules)
- **CSRF Protection**: Enabled on ALL forms (Flask-WTF)
- **Password Security**: bcrypt hashing with salt
- **SQL Injection Prevention**: ORM-based queries only
- **XSS Protection**: Jinja auto-escaping, input sanitization
- **File Upload Security**: Whitelist extensions, random filenames, size limits
- **Authorization**: Role-based decorators (@require_role)

### 6.2 Performance
- Page load time < 2 seconds
- Search results < 2 seconds
- No N+1 database queries (use eager loading)
- Database indexes on frequently queried fields

### 6.3 Usability
- Responsive design (320px to 1920px)
- Accessibility (WCAG 2.1 AA):
  - Proper ARIA labels
  - Keyboard navigation
  - Color contrast 4.5:1 minimum
  - Screen reader compatible
- Professional UI (NOT generic Bootstrap)
- Loading states, empty states, error messages

### 6.4 Scalability
- Support 100+ concurrent users
- Handle 1000+ resources
- Efficient pagination and caching

---

## 7. Technical Architecture

### Stack
- **Backend**: Flask 3.x, SQLAlchemy, Flask-Login, Flask-WTF
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Frontend**: Jinja2 + Bootstrap 5 (heavily customized)
- **Testing**: pytest (70%+ coverage required)
- **Code Quality**: ruff, black, mypy

### Architecture Pattern
- **App Factory**: Flask application factory pattern
- **MVC + DAL**: Model-View-Controller with Data Access Layer
- **Blueprints**: auth, resources, bookings, messages, reviews, admin
- **Security-First**: All .clinerules requirements enforced

### Database Schema (5 Tables Minimum)
1. **users**: user_id, name, email, password_hash, role, profile_image, department, created_at
2. **resources**: resource_id, owner_id, title, description, category, location, capacity, images, availability_rules, status, created_at
3. **bookings**: booking_id, resource_id, requester_id, start_datetime, end_datetime, status, created_at, updated_at
4. **messages**: message_id, thread_id, sender_id, receiver_id, content, timestamp
5. **reviews**: review_id, resource_id, reviewer_id, rating, comment, timestamp
6. **admin_logs** (optional): log_id, admin_id, action, target_table, details, timestamp

---

## 8. Out of Scope (Non-Goals)

- Native mobile apps (web-only)
- Real-time chat (basic messaging only)
- Payment processing
- External calendar sync (Google Calendar integration optional)
- Multi-language support
- Social media integration
- Push notifications (email/in-app only)

---

## 9. Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Timeline too aggressive (18 days) | High | Medium | Prioritize P0 features; cut P2 if needed |
| Solo developer (no team) | High | High | Use AI tools effectively; plan thoroughly |
| AI feature complexity | Medium | Medium | Start simple; use proven APIs; test early |
| Security vulnerabilities | High | Low | Follow .clinerules strictly; security tests |
| Poor UI/UX | High | Medium | Reference Airbnb/Notion designs; iterate |
| Low test coverage | High | Low | Write tests alongside code (TDD approach) |

---

## 10. Deliverables Checklist

### Phase 1: Planning (Days 1-3) ✅
- [x] PRD (this document)
- [ ] ERD diagram
- [ ] Wireframes (8+ screens)
- [ ] API endpoint specifications
- [ ] Acceptance criteria

### Phase 2: Development (Days 4-14)
- [ ] All core features implemented
- [ ] AI feature integrated
- [ ] Enterprise-grade UI
- [ ] 70%+ test coverage

### Phase 3: Documentation (Days 15-16)
- [ ] README
- [ ] API documentation
- [ ] .prompt/dev_notes.md
- [ ] .prompt/golden_prompts.md

### Phase 4: Demo (Days 17-18)
- [ ] Deployed application (optional)
- [ ] Demo slide deck (7 slides max)
- [ ] Demo script
- [ ] Q&A preparation

---

## 11. Approval & Sign-Off

**Developer**: Aneesh Yaramati  
**Date**: November 2, 2025  
**Status**: ✅ Approved - Ready for Implementation

**Next Steps**:
1. Design ERD with all table relationships
2. Create wireframes for key user flows
3. Define API endpoint contracts
4. Begin Phase 3 (Backend Development)

---

## Appendix: Reference Documents

- **Project Brief**: `/Users/aneeshyaramati/Downloads/2025_AiDD_Core_Final_Project.docx`
- **.clinerules**: `/Users/aneeshyaramati/Documents/GitHub/Campus-Resource-Hub/.clinerules`
- **AI Development Guide**: `/Users/aneeshyaramati/Documents/GitHub/Campus-Resource-Hub/docs/CLINE_CONFIGURATION_GUIDE.md`

---

*This PRD serves as the guiding document for the Campus Resource Hub project. All implementation decisions should align with the objectives and requirements defined here.*
