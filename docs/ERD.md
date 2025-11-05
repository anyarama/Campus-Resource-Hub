# Entity-Relationship Diagram (ERD)
## Campus Resource Hub Database Schema

**Project**: Campus Resource Hub - AiDD 2025 Capstone Project  
**Version**: 1.0  
**Date**: November 2, 2025  
**Database**: SQLite (Development), PostgreSQL (Production)  

---

## Overview

This document defines the complete database schema for Campus Resource Hub, including all tables, fields, relationships, constraints, and indexes. The schema supports user authentication, resource management, booking workflows, messaging, reviews, and admin oversight.

**Total Tables**: 6 (5 required + 1 optional admin logging)

---

## Visual ERD (Text Representation)

```
┌─────────────────┐
│     USERS       │
├─────────────────┤
│ user_id (PK)    │◄──────┐
│ name            │        │
│ email (UNIQUE)  │        │ Owner
│ password_hash   │        │
│ role            │        │
│ profile_image   │        │
│ department      │        │
│ created_at      │        │
└─────────────────┘        │
        │                  │
        │ Requester        │
        │                  │
        ▼                  │
┌─────────────────┐        │
│    BOOKINGS     │        │
├─────────────────┤        │
│ booking_id (PK) │        │
│ resource_id (FK)│───┐    │
│ requester_id(FK)│   │    │
│ start_datetime  │   │    │
│ end_datetime    │   │    │
│ status          │   │    │
│ created_at      │   │    │
│ updated_at      │   │    │
└─────────────────┘   │    │
        │             │    │
        │ Booking     │    │
        │             │    │
        ▼             ▼    │
┌─────────────────┐        │
│    REVIEWS      │        │
├─────────────────┤        │
│ review_id (PK)  │        │
│ resource_id (FK)│◄───────┼────┐
│ reviewer_id (FK)│───┐    │    │
│ rating (1-5)    │   │    │    │
│ comment         │   │    │    │
│ timestamp       │   │    │    │
└─────────────────┘   │    │    │
                      │    │    │
        ┌─────────────┘    │    │
        │                  │    │
        ▼                  ▼    │
┌─────────────────┐  ┌─────────────────┐
│    MESSAGES     │  │    RESOURCES    │
├─────────────────┤  ├─────────────────┤
│ message_id (PK) │  │ resource_id (PK)│
│ thread_id       │  │ owner_id (FK)   │───┘
│ sender_id (FK)  │──┤ title           │
│ receiver_id(FK) │──┤ description     │
│ content         │  │ category        │
│ timestamp       │  │ location        │
└─────────────────┘  │ capacity        │
                     │ images          │
                     │ availability    │
                     │ status          │
                     │ created_at      │
                     └─────────────────┘

┌─────────────────┐
│   ADMIN_LOGS    │  (Optional)
├─────────────────┤
│ log_id (PK)     │
│ admin_id (FK)   │───┐
│ action          │   │
│ target_table    │   │
│ details         │   │
│ timestamp       │   │
└─────────────────┘   │
                      │
                      └──► References USERS
```

---

## Table Definitions

### 1. USERS
**Purpose**: Store all user accounts with authentication and profile information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| user_id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique user identifier |
| name | VARCHAR(100) | NOT NULL | User's full name |
| email | VARCHAR(120) | NOT NULL, UNIQUE | Email address (login credential) |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt hashed password |
| role | VARCHAR(20) | NOT NULL, DEFAULT 'student' | User role: 'student', 'staff', 'admin' |
| profile_image | VARCHAR(255) | NULL | Path to profile image |
| department | VARCHAR(100) | NULL | Department/organization affiliation |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |

**Indexes**:
- `idx_users_email` on `email` (for login queries)
- `idx_users_role` on `role` (for role-based queries)

**Constraints**:
- Email must be unique and valid format
- Password must be bcrypt hash (never plaintext)
- Role must be one of: 'student', 'staff', 'admin'

**Relationships**:
- ONE user → MANY resources (as owner)
- ONE user → MANY bookings (as requester)
- ONE user → MANY reviews (as reviewer)
- ONE user → MANY messages (as sender or receiver)
- ONE user → MANY admin_logs (as admin performing action)

---

### 2. RESOURCES
**Purpose**: Store campus resources available for booking

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| resource_id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique resource identifier |
| owner_id | INTEGER | NOT NULL, FOREIGN KEY → users(user_id) | User who created/owns the resource |
| title | VARCHAR(200) | NOT NULL | Resource name/title |
| description | TEXT | NULL | Detailed description |
| category | VARCHAR(50) | NOT NULL | Category: 'study_room', 'equipment', 'lab', 'space', 'tutoring' |
| location | VARCHAR(200) | NULL | Physical location (building, room number) |
| capacity | INTEGER | NULL | Maximum number of users/seats |
| images | TEXT | NULL | JSON array of image paths |
| availability_rules | TEXT | NULL | JSON object defining when resource is available |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'draft' | Status: 'draft', 'published', 'archived' |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Creation timestamp |

**Indexes**:
- `idx_resources_owner` on `owner_id` (for "My Resources" queries)
- `idx_resources_status` on `status` (for published resources queries)
- `idx_resources_category` on `category` (for category filtering)
- `idx_resources_created` on `created_at` (for sorting by recency)

**Constraints**:
- Status must be one of: 'draft', 'published', 'archived'
- Category must be one of predefined categories
- Images must be valid JSON array
- Availability_rules must be valid JSON object

**Relationships**:
- ONE resource → MANY bookings
- ONE resource → MANY reviews
- MANY resources ← ONE user (owner)

---

### 3. BOOKINGS
**Purpose**: Store booking requests and approvals for resources

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| booking_id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique booking identifier |
| resource_id | INTEGER | NOT NULL, FOREIGN KEY → resources(resource_id) | Resource being booked |
| requester_id | INTEGER | NOT NULL, FOREIGN KEY → users(user_id) | User making the booking |
| start_datetime | DATETIME | NOT NULL | Booking start time |
| end_datetime | DATETIME | NOT NULL | Booking end time |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | Status: 'pending', 'approved', 'rejected', 'cancelled', 'completed' |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Request creation timestamp |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last status update timestamp |

**Indexes**:
- `idx_bookings_resource` on `resource_id` (for conflict detection)
- `idx_bookings_requester` on `requester_id` (for "My Bookings")
- `idx_bookings_status` on `status` (for approval queues)
- `idx_bookings_datetime` on `start_datetime, end_datetime` (for conflict checks)
- Composite index: `idx_bookings_resource_datetime` on `(resource_id, start_datetime, end_datetime)`

**Constraints**:
- `end_datetime` must be after `start_datetime`
- Status must be one of: 'pending', 'approved', 'rejected', 'cancelled', 'completed'
- No overlapping approved bookings for same resource (enforced by service layer)

**Relationships**:
- MANY bookings ← ONE resource
- MANY bookings ← ONE user (requester)
- ONE booking → OPTIONAL ONE review

---

### 4. MESSAGES
**Purpose**: Enable communication between users (requester ↔ resource owner)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| message_id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique message identifier |
| thread_id | INTEGER | NULL | Groups messages in conversation |
| sender_id | INTEGER | NOT NULL, FOREIGN KEY → users(user_id) | User sending the message |
| receiver_id | INTEGER | NOT NULL, FOREIGN KEY → users(user_id) | User receiving the message |
| content | TEXT | NOT NULL | Message body |
| timestamp | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Message send time |

**Indexes**:
- `idx_messages_sender` on `sender_id` (for sent messages)
- `idx_messages_receiver` on `receiver_id` (for inbox)
- `idx_messages_thread` on `thread_id` (for conversation threading)

**Constraints**:
- Content must not be empty
- Sender and receiver must be different users
- Content sanitized (XSS protection via Jinja auto-escaping)

**Relationships**:
- MANY messages ← ONE user (sender)
- MANY messages ← ONE user (receiver)

---

### 5. REVIEWS
**Purpose**: Store ratings and feedback for resources after booking completion

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| review_id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique review identifier |
| resource_id | INTEGER | NOT NULL, FOREIGN KEY → resources(resource_id) | Resource being reviewed |
| reviewer_id | INTEGER | NOT NULL, FOREIGN KEY → users(user_id) | User writing the review |
| rating | INTEGER | NOT NULL, CHECK (rating BETWEEN 1 AND 5) | Star rating 1-5 |
| comment | TEXT | NULL | Written review/feedback |
| timestamp | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Review submission time |

**Indexes**:
- `idx_reviews_resource` on `resource_id` (for aggregate rating calc)
- `idx_reviews_reviewer` on `reviewer_id` (for user's review history)
- Composite index: `idx_reviews_resource_reviewer` on `(resource_id, reviewer_id)` (UNIQUE)

**Constraints**:
- Rating must be between 1 and 5 (inclusive)
- One review per (resource, reviewer) combination
- Reviewer must have completed booking for resource (enforced by service layer)

**Relationships**:
- MANY reviews ← ONE resource
- MANY reviews ← ONE user (reviewer)

---

### 6. ADMIN_LOGS (Optional)
**Purpose**: Audit trail for administrative actions

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| log_id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique log entry identifier |
| admin_id | INTEGER | NOT NULL, FOREIGN KEY → users(user_id) | Admin performing action |
| action | VARCHAR(100) | NOT NULL | Action type: 'user_suspend', 'resource_archive', etc. |
| target_table | VARCHAR(50) | NOT NULL | Table affected: 'users', 'resources', 'bookings', etc. |
| details | TEXT | NULL | JSON object with action details |
| timestamp | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | When action occurred |

**Indexes**:
- `idx_admin_logs_admin` on `admin_id` (for admin action history)
- `idx_admin_logs_timestamp` on `timestamp` (for time-based queries)
- `idx_admin_logs_target` on `target_table` (for table-specific logs)

**Constraints**:
- Admin must have 'admin' role (enforced by service layer)
- Details must be valid JSON

**Relationships**:
- MANY admin_logs ← ONE user (admin)

---

## Relationship Summary

### One-to-Many Relationships

1. **User → Resources**
   - One user can own many resources
   - Foreign Key: `resources.owner_id` → `users.user_id`
   - On Delete: CASCADE (delete resources when user deleted)

2. **User → Bookings (as Requester)**
   - One user can make many booking requests
   - Foreign Key: `bookings.requester_id` → `users.user_id`
   - On Delete: SET NULL (preserve booking history)

3. **Resource → Bookings**
   - One resource can have many bookings
   - Foreign Key: `bookings.resource_id` → `resources.resource_id`
   - On Delete: CASCADE (delete bookings when resource deleted)

4. **Resource → Reviews**
   - One resource can have many reviews
   - Foreign Key: `reviews.resource_id` → `resources.resource_id`
   - On Delete: CASCADE (delete reviews when resource deleted)

5. **User → Reviews (as Reviewer)**
   - One user can write many reviews
   - Foreign Key: `reviews.reviewer_id` → `users.user_id`
   - On Delete: CASCADE (delete reviews when user deleted)

6. **User → Messages (as Sender)**
   - One user can send many messages
   - Foreign Key: `messages.sender_id` → `users.user_id`
   - On Delete: CASCADE (delete sent messages)

7. **User → Messages (as Receiver)**
   - One user can receive many messages
   - Foreign Key: `messages.receiver_id` → `users.user_id`
   - On Delete: CASCADE (delete received messages)

8. **User → Admin_Logs**
   - One admin can perform many actions
   - Foreign Key: `admin_logs.admin_id` → `users.user_id`
   - On Delete: SET NULL (preserve audit trail)

---

## Business Rules & Validations

### User Authentication
- ✅ Passwords must be at least 8 characters
- ✅ Passwords stored as bcrypt hashes (rounds=12)
- ✅ Email must be unique and valid format
- ✅ Default role is 'student'

### Resource Lifecycle
- ✅ Only 'published' resources appear in search
- ✅ Only owner or admin can edit/delete resource
- ✅ Images limited to 2MB, extensions: .jpg, .jpeg, .png, .gif
- ✅ Archived resources retain bookings but cannot accept new bookings

### Booking Conflicts
- ✅ No overlapping approved bookings for same resource
- ✅ Conflict check: `(new.start < existing.end) AND (new.end > existing.start)`
- ✅ Cancelling a booking frees the time slot
- ✅ Only approved bookings count for conflict detection

### Review Authorization
- ✅ User can only review a resource after completed booking
- ✅ One review per user per resource
- ✅ Rating must be 1-5 stars
- ✅ Admin can moderate/remove inappropriate reviews

### Messaging Rules
- ✅ Users cannot message themselves
- ✅ Thread_id links related messages
- ✅ XSS protection via Jinja auto-escaping
- ✅ No HTML in message content (plain text only)

### Admin Actions
- ✅ Only users with role='admin' can access admin routes
- ✅ All admin actions logged in admin_logs
- ✅ User suspension prevents login (not deletion)
- ✅ Admin can approve/reject any booking

---

## Database Initialization SQL

```sql
-- Users Table
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'student',
    profile_image VARCHAR(255),
    department VARCHAR(100),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (role IN ('student', 'staff', 'admin'))
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Resources Table
CREATE TABLE resources (
    resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    location VARCHAR(200),
    capacity INTEGER,
    images TEXT,
    availability_rules TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CHECK (status IN ('draft', 'published', 'archived'))
);

CREATE INDEX idx_resources_owner ON resources(owner_id);
CREATE INDEX idx_resources_status ON resources(status);
CREATE INDEX idx_resources_category ON resources(category);
CREATE INDEX idx_resources_created ON resources(created_at);

-- Bookings Table
CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_id INTEGER NOT NULL,
    requester_id INTEGER NOT NULL,
    start_datetime DATETIME NOT NULL,
    end_datetime DATETIME NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resource_id) REFERENCES resources(resource_id) ON DELETE CASCADE,
    FOREIGN KEY (requester_id) REFERENCES users(user_id) ON DELETE SET NULL,
    CHECK (status IN ('pending', 'approved', 'rejected', 'cancelled', 'completed')),
    CHECK (end_datetime > start_datetime)
);

CREATE INDEX idx_bookings_resource ON bookings(resource_id);
CREATE INDEX idx_bookings_requester ON bookings(requester_id);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_bookings_resource_datetime ON bookings(resource_id, start_datetime, end_datetime);

-- Messages Table
CREATE TABLE messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_id INTEGER,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CHECK (sender_id != receiver_id)
);

CREATE INDEX idx_messages_sender ON messages(sender_id);
CREATE INDEX idx_messages_receiver ON messages(receiver_id);
CREATE INDEX idx_messages_thread ON messages(thread_id);

-- Reviews Table
CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_id INTEGER NOT NULL,
    reviewer_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    comment TEXT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resource_id) REFERENCES resources(resource_id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CHECK (rating BETWEEN 1 AND 5),
    UNIQUE (resource_id, reviewer_id)
);

CREATE INDEX idx_reviews_resource ON reviews(resource_id);
CREATE INDEX idx_reviews_reviewer ON reviews(reviewer_id);

-- Admin Logs Table (Optional)
CREATE TABLE admin_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER NOT NULL,
    action VARCHAR(100) NOT NULL,
    target_table VARCHAR(50) NOT NULL,
    details TEXT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE INDEX idx_admin_logs_admin ON admin_logs(admin_id);
CREATE INDEX idx_admin_logs_timestamp ON admin_logs(timestamp);
CREATE INDEX idx_admin_logs_target ON admin_logs(target_table);
```

---

## Migration Notes

### From Development (SQLite) to Production (PostgreSQL)

**Type Differences**:
- `AUTOINCREMENT` → `SERIAL`
- `DATETIME` → `TIMESTAMP`
- `TEXT` → `TEXT` (same)
- `VARCHAR(n)` → `VARCHAR(n)` (same)

**Index Strategy**:
- SQLite: B-tree indexes only
- PostgreSQL: Consider GIN indexes for JSON fields (availability_rules)

**JSON Fields**:
- SQLite: Store as TEXT, parse in application
- PostgreSQL: Use native JSONB type for better performance

---

## Performance Considerations

### Query Optimization
1. **Conflict Detection**: Composite index on `(resource_id, start_datetime, end_datetime)`
2. **Search**: Full-text index on `resources.title` and `resources.description` (Phase 4)
3. **Aggregate Ratings**: Computed column or cached value in resources table
4. **Pagination**: Use cursor-based pagination for large result sets

### N+1 Prevention
- Use SQLAlchemy `joinedload()` for relationships
- Eager load user data when fetching resources
- Batch load reviews when displaying resource lists

---

## Next Steps

1. **Implement SQLAlchemy Models** (Phase 3)
   - Create model classes in `src/models/`
   - Define relationships with `relationship()` and `backref`
   - Add validation methods

2. **Create Migration Scripts**
   - Use Flask-Migrate for schema versioning
   - Generate initial migration from models

3. **Seed Development Data** (Phase 11)
   - Create sample users (student, staff, admin)
   - Add diverse resources
   - Generate bookings and reviews

---

**Document Status**: ✅ Complete  
**Last Updated**: November 2, 2025  
**Next**: Create wireframes for UI design
