# Acceptance Criteria
## Campus Resource Hub - AiDD 2025 Capstone Project

**Project**: Campus Resource Hub  
**Version**: 1.0  
**Date**: November 4, 2025  
**Purpose**: Define testable acceptance criteria for all core features

---

## Overview

This document provides detailed, testable acceptance criteria for all 7 core features of the Campus Resource Hub application, plus the AI-powered Resource Concierge feature. Each criterion is written in Given-When-Then format that can be validated through manual testing or automated test scripts.

**Total Acceptance Criteria**: 50+ testable criteria across 8 feature areas

---

## Feature 1: User Management & Authentication

### AC-AUTH-001: User Registration
**Priority**: P0 (Critical)

**Given** a user visits the registration page  
**When** they submit valid registration data with name, unique email, strong password (8+ chars)  
**Then** account is created with bcrypt-hashed password, user redirected to login, email uniqueness enforced

### AC-AUTH-002: User Login  
**Priority**: P0 (Critical)

**Given** registered user with correct credentials  
**When** they submit login form  
**Then** Flask-Login session created, redirected to dashboard, session cookie set with HttpOnly flag

### AC-AUTH-003: Role-Based Access Control (RBAC)
**Priority**: P0 (Critical)

**Given** user with specific role (student/staff/admin)  
**When** attempting to access protected routes  
**Then** authorization enforced per role permissions, unauthorized access returns 403

---

## Feature 2: Resource Listings

### AC-RESOURCE-001: Create Resource
**Priority**: P0 (Critical)

**Given** authenticated user on create resource page  
**When** submitting valid resource form (title, category, description, images)  
**Then** resource created in database with owner_id, images uploaded securely with random filenames, user redirected to resource detail

### AC-RESOURCE-002: Image Upload Security
**Priority**: P0 (Critical)

**Given** user uploading resource images  
**When** selecting files  
**Then** only .jpg/.jpeg/.png/.gif accepted, 2MB max per image, 5 images max, filenames randomized (UUID), secure_filename() applied

### AC-RESOURCE-003: Resource Lifecycle
**Priority**: P1 (High)

**Given** resource with status (draft/published/archived)  
**When** status changes  
**Then** draft=owner-only visible, published=searchable+bookable, archived=admin-only visible

---

## Feature 3: Search & Discovery

### AC-SEARCH-001: Keyword Search
**Priority**: P0 (Critical)

**Given** user on search page  
**When** entering search keyword  
**Then** results returned <2 seconds, searches title+description case-insensitive, only published resources shown

### AC-SEARCH-002: Multi-Filter Search
**Priority**: P0 (Critical)

**Given** search page with filters  
**When** applying category, location, capacity, availability filters  
**Then** results match all active filters (AND), filters persist during pagination, filter count badge shown

### AC-SEARCH-003: Availability Filter
**Priority**: P0 (Critical)

**Given** user filtering by date/time range  
**When** availability filter applied  
**Then** conflict detection runs, only truly available resources shown, booking overlaps excluded

---

## Feature 4: Booking & Scheduling

### AC-BOOKING-001: Request Booking
**Priority**: P0 (Critical)

**Given** user viewing available resource  
**When** selecting date/time and submitting booking request  
**Then** booking created with requester_id, conflict detection runs, status set to pending, notification sent to owner

### AC-BOOKING-002: Conflict Detection Algorithm
**Priority**: P0 (Critical - Core Logic)

**Given** new booking request for resource  
**When** conflict check runs  
**Then** algorithm checks `(new.start < existing.end) AND (new.end > existing.start)`, only approved bookings count, conflicts rejected with error

### AC-BOOKING-003: Booking Approval Workflow
**Priority**: P0 (Critical)

**Given** resource requiring approval  
**When** owner/staff views approval queue and approves/rejects  
**Then** status updated (approved/rejected), notifications sent, approved bookings block time slot

### AC-BOOKING-004: Cancel Booking
**Priority**: P0 (Critical)

**Given** approved booking  
**When** requester/admin cancels  
**Then** confirmation prompt shown, status changed to cancelled, time slot freed, notifications sent

---

## Feature 5: Messaging & Notifications

### AC-MESSAGE-001: Send Message
**Priority**: P1 (High)

**Given** user wants to contact resource owner  
**When** composing and sending message  
**Then** message created with sender_id, receiver_id, thread_id, XSS protection applied, 2000 char limit enforced

### AC-MESSAGE-002: View Inbox
**Priority**: P1 (High)

**Given** user opening inbox  
**When** inbox loads  
**Then** messages where user=receiver displayed, unread count shown, most recent first, sender name+timestamp visible

### AC-MESSAGE-003: Notification System
**Priority**: P1 (High)

**Given** key user actions (booking approved, message received, review posted)  
**When** event occurs  
**Then** in-app notification created, notification badge updated, email notification sent (simulated)

---

## Feature 6: Reviews & Ratings

### AC-REVIEW-001: Submit Review
**Priority**: P1 (High)

**Given** user with completed booking  
**When** submitting review with rating (1-5) and optional comment  
**Then** review saved with unique constraint (one per user per resource), only completed booking users can review

### AC-REVIEW-002: Authorization Check
**Priority**: P0 (Critical)

**Given** any review submission  
**When** authorization validated  
**Then** must have completed booking for this resource, cannot review own resources, validation enforced server-side

### AC-REVIEW-003: Aggregate Rating Calculation
**Priority**: P1 (High)

**Given** resource with multiple reviews  
**When** resource detail page loads  
**Then** average rating calculated (AVG rounded to 1 decimal), total count shown, star visualization rendered

---

## Feature 7: Admin Dashboard

### AC-ADMIN-001: Access Control
**Priority**: P0 (Critical)

**Given** any user attempting /admin routes  
**When** authorization check runs  
**Then** only role=admin can access, non-admins get 403 Forbidden, redirect to login if not authenticated

### AC-ADMIN-002: User Management
**Priority**: P1 (High)

**Given** admin on user management page  
**When** viewing user list  
**Then** all users displayed with ID/name/email/role, can suspend/delete users, search by name/email, filter by role

### AC-ADMIN-003: Analytics Dashboard
**Priority**: P1 (High)

**Given** admin viewing dashboard  
**When** analytics page loads  
**Then** usage metrics displayed (total bookings, active users, popular resources), loads <3 seconds, charts/graphs rendered

### AC-ADMIN-004: Audit Logging
**Priority**: P1 (High)

**Given** any admin action (suspend user, delete resource, moderate review)  
**When** action performed  
**Then** entry created in admin_logs table with admin_id, action, target_table, details (JSON), timestamp

---

## Feature 8: AI-Powered Resource Concierge

### AC-AI-001: Natural Language Query
**Priority**: P1 (High - AI Feature)

**Given** user on AI Concierge interface  
**When** entering natural language query (e.g., "Find study room for 4 people tomorrow 2-4pm")  
**Then** AI parses query, extracts parameters (capacity=4, date=tomorrow, time=14:00-16:00), searches database, returns matching results

### AC-AI-002: Context Grounding
**Priority**: P0 (Critical - AI Safety)

**Given** AI Concierge responding to query  
**When** generating response  
**Then** AI only references real database data, never fabricates resources/availability, graceful fallback if AI unavailable

### AC-AI-003: Query Parsing Accuracy
**Priority**: P1 (High)

**Given** common query patterns  
**When** AI processes query  
**Then** correctly extracts: date/time (relative and absolute), capacity, location, category, 80%+ accuracy on test queries

### AC-AI-004: Fallback Handling
**Priority**: P1 (High)

**Given** AI service unavailable or query unparseable  
**When** Concierge invoked  
**Then** system falls back to standard search, error message shown ("AI temporarily unavailable, showing standard search"), functionality not blocked

### AC-AI-005: AI Decision Logging
**Priority**: P1 (High - Transparency)

**Given** any AI Concierge interaction  
**When** query processed and response generated  
**Then** interaction logged in .prompt/dev_notes.md with: query text, parsed parameters, response, timestamp

---

## Security Acceptance Criteria

### AC-SEC-001: CSRF Protection
**Priority**: P0 (Critical)

**Given** any state-changing form (create, edit, delete)  
**When** form submitted  
**Then** CSRF token required and validated, forms without valid token rejected with 400 error

### AC-SEC-002: SQL Injection Prevention
**Priority**: P0 (Critical)

**Given** any database query with user input  
**When** query executed  
**Then** only ORM queries or parameterized SQL used, raw SQL concatenation never used, injection attempts fail safely

### AC-SEC-003: XSS Protection
**Priority**: P0 (Critical)

**Given** any user-generated content displayed (reviews, messages, resource descriptions)  
**When** content rendered  
**Then** Jinja auto-escaping enabled, HTML tags escaped, script injection attempts neutralized

### AC-SEC-004: File Upload Security
**Priority**: P0 (Critical)

**Given** file upload functionality  
**When** user uploads file  
**Then** extension whitelist enforced, file size limits checked, filenames randomized, path traversal prevented

---

## Performance Acceptance Criteria

### AC-PERF-001: Page Load Time
**Priority**: P1 (High)

**Given** any application page  
**When** user navigates to page  
**Then** page loads in <2 seconds on standard connection, <3 seconds for search results, <5 seconds for admin analytics

### AC-PERF-002: Search Response Time
**Priority**: P1 (High)

**Given** search query with multiple filters  
**When** search executed  
**Then** results returned in <2 seconds, database queries optimized with indexes, no N+1 queries

### AC-PERF-003: Concurrent Users
**Priority**: P2 (Medium)

**Given** 100+ concurrent users  
**When** system under load  
**Then** application remains responsive, no deadlocks, session conflicts handled gracefully

---

## Accessibility Acceptance Criteria

### AC-A11Y-001: Keyboard Navigation
**Priority**: P1 (High)

**Given** user navigating with keyboard only  
**When** using Tab, Enter, Escape keys  
**Then** all interactive elements reachable, focus order logical, focus indicators visible, no keyboard traps

### AC-A11Y-002: Screen Reader Compatibility
**Priority**: P1 (High)

**Given** screen reader user (NVDA, JAWS, VoiceOver)  
**When** navigating application  
**Then** ARIA labels present, semantic HTML used, forms have proper labels, error messages announced

### AC-A11Y-003: Color Contrast
**Priority**: P1 (High - WCAG 2.1 AA)

**Given** any text content  
**When** rendered on page  
**Then** contrast ratio ≥ 4.5:1 for normal text, ≥ 3:1 for large text, color not sole indicator of information

---

## Testing Acceptance Criteria

### AC-TEST-001: Test Coverage
**Priority**: P0 (Critical)

**Given** full codebase  
**When** test suite runs  
**Then** coverage ≥ 70%, all critical paths tested (auth, booking conflict, RBAC), pytest passes with 0 failures

### AC-TEST-002: Unit Tests
**Priority**: P0 (Critical)

**Given** business logic in services layer  
**When** unit tests execute  
**Then** booking conflict detection tested, rating aggregation tested, DAL CRUD operations tested independently

### AC-TEST-003: Integration Tests
**Priority**: P0 (Critical)

**Given** complete user workflows  
**When** integration tests run  
**Then** auth flow tested (register→login→access), booking flow tested (browse→book→approve→complete), review flow tested

---

## Definition of Done (Each Feature)

**A feature is considered complete when**:
- [ ] All acceptance criteria pass (manual or automated tests)
- [ ] Security requirements verified (CSRF, XSS, SQL injection tests)
- [ ] Code quality checks pass (ruff, black, mypy)
- [ ] Documentation updated (docstrings, README, API docs)
- [ ] UI/UX polished and responsive (mobile + desktop tested)
- [ ] Accessibility verified (keyboard nav, screen reader, contrast)
- [ ] Peer review completed (self-review in solo project)
- [ ] Git commit with clear message

---

## Verification Matrix

| Feature | Total AC | P0 (Critical) | P1 (High) | P2 (Medium) | Automated Tests |
|---------|----------|---------------|-----------|-------------|-----------------|
| Authentication | 5 | 4 | 1 | 0 | Yes |
| Resource Listings | 5 | 3 | 2 | 0 | Yes |
| Search & Discovery | 7 | 3 | 4 | 0 | Partial |
| Booking & Scheduling | 7 | 5 | 2 | 0 | Yes |
| Messaging | 5 | 1 | 4 | 0 | Partial |
| Reviews & Ratings | 5 | 2 | 3 | 0 | Yes |
| Admin Dashboard | 4 | 1 | 3 | 0 | Partial |
| AI Concierge | 5 | 1 | 4 | 0 | Manual |
| Security | 4 | 4 | 0 | 0 | Yes |
| Performance | 3 | 0 | 2 | 1 | Manual |
| Accessibility | 3 | 0 | 3 | 0 | Manual |
| Testing | 3 | 3 | 0 | 0 | Automated |
| **TOTAL** | **56** | **27** | **28** | **1** | **~75% Coverage** |

---

## Next Steps

1. **Development Phase**: Implement features according to these criteria
2. **Test Development**: Write pytest tests for each AC (especially P0/P1)
3. **Manual Testing**: Create test scripts for manual verification
4. **Acceptance Review**: Validate each criterion before marking feature complete
5. **Documentation**: Update README with "How to Verify" section

---

**Document Status**: ✅ Complete  
**Last Updated**: November 4, 2025  
**Approved By**: Aneesh Yaramati (Developer)  
**Next**: Begin Phase 3 (Backend Development - Models & DAL)
