# API Endpoint Specifications
## Campus Resource Hub REST API

**Project**: Campus Resource Hub  
**Version**: 1.0  
**Base URL**: `http://localhost:5000` (development)  
**Authentication**: Flask-Login sessions with CSRF tokens  

---

## Authentication Endpoints

### POST /auth/register
**Description**: Create new user account  
**Auth Required**: No  
**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "department": "Computer Science"
}
```
**Response 201**:
```json
{
  "status": "success",
  "user_id": 1,
  "message": "Account created successfully"
}
```
**Response 400**: Email already exists or validation failed

### POST /auth/login
**Description**: User login  
**Auth Required**: No  
**Request Body**:
```json
{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```
**Response 200**:
```json
{
  "status": "success",
  "user": {"id": 1, "name": "John Doe", "role": "student"}
}
```

### POST /auth/logout
**Description**: User logout  
**Auth Required**: Yes  
**Response 200**: `{"status": "success"}`

---

## Resource Endpoints (Phase 5 - Implemented)

### GET /resources
**Description**: List all published resources with search and filtering  
**Auth Required**: No (public route)  
**Query Parameters**:
- `q`: Search keyword (searches title and description)
- `category`: Filter by category (Study Space, Equipment, Lab, Event Space, Technology, etc.)
- `location`: Filter by location (partial match)
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20, max: 100)

**Response 200** (HTML): Renders `resources/list.html` with filtered resources  
**Query Examples**:
- `/resources` - All published resources
- `/resources?q=macbook` - Search for "macbook"
- `/resources?category=Study Space` - Filter by category
- `/resources?category=Technology&location=IT` - Combined filters

---

### GET /resources/<int:resource_id>
**Description**: Get resource detail page with images, availability, and reviews  
**Auth Required**: No (public for published resources)  
**Path Parameters**: `resource_id` - Resource ID  
**Response 200** (HTML): Renders `resources/detail.html`  
**Response 302**: Redirects to `/resources` if not found  

**Displays**:
- Image carousel (if images exist)
- Full description and metadata
- Owner information
- Availability rules (if set)
- Action buttons (edit/delete for owner, book for others)

---

### GET /resources/create
### POST /resources/create
**Description**: Create new resource with optional image uploads  
**Auth Required**: Yes (any authenticated user)  
**Method**: GET displays form, POST processes submission  

**Form Fields** (multipart/form-data):
```
title (required): Resource title (min 3 chars)
description (required): Description (min 10 chars)
category (required): One of [Study Space, Equipment, Lab, Event Space, Technology, Tutoring, Sports, Other]
location (required): Resource location
capacity (optional): Integer capacity
images (optional): Multiple image files (max 5, 2MB each, jpg/jpeg/png/gif only)
status (required): "draft" or "published"
```

**Response 302** (POST): Redirects to `/resources/<id>` on success  
**Response 200** (POST): Re-renders form with error message on failure  
**Security**: CSRF protected, file validation (type/size), owner authorization  

---

### GET /resources/<int:resource_id>/edit
### POST /resources/<int:resource_id>/edit
**Description**: Edit existing resource (owner-only)  
**Auth Required**: Yes (owner only)  
**Method**: GET displays edit form, POST processes updates  

**Form Fields** (same as create, pre-populated):
- All fields from create endpoint
- Existing images displayed with option to replace

**Response 302** (POST): Redirects to `/resources/<id>` on success  
**Response 403**: If non-owner attempts to edit  
**Note**: Uploading new images replaces all existing images  

---

### POST /resources/<int:resource_id>/delete
**Description**: Delete resource and associated images (owner-only)  
**Auth Required**: Yes (owner only)  
**Method**: POST only (CSRF protection)  

**Response 302**: Redirects to `/my-resources` on success  
**Response 403**: If non-owner attempts to delete  
**Side Effects**: 
- Removes database record
- Deletes associated image files from filesystem
- Cascading deletion of related bookings/reviews (future)

---

### POST /resources/<int:resource_id>/publish
**Description**: Publish a draft resource (owner-only)  
**Auth Required**: Yes (owner only)  
**Method**: POST only  
**Transitions**: draft → published  

**Response 302**: Redirects to `/resources/<id>` with success message  
**Response 400**: If resource already published  

---

### POST /resources/<int:resource_id>/archive
**Description**: Archive a published resource (owner-only)  
**Auth Required**: Yes (owner only)  
**Method**: POST only  
**Transitions**: published → archived  

**Response 302**: Redirects to `/resources/<id>` with info message  
**Response 400**: If resource already archived  
**Note**: Archived resources don't appear in public listings  

---

### GET /my-resources
**Description**: User's resource management dashboard  
**Auth Required**: Yes  
**Response 200** (HTML): Renders `resources/my_resources.html`  

**Displays**:
- Statistics (total, published, drafts, archived)
- Tabbed filtering (All, Published, Drafts, Archived)
- Quick actions per resource (view, edit, publish/archive)
- Empty state for new users

---

## Resource Data Model

```json
{
  "resource_id": 1,
  "owner_id": 5,
  "title": "Main Library Study Room A",
  "description": "Quiet study room perfect for group work...",
  "category": "Study Space",
  "location": "Main Library, 2nd Floor, Room 201",
  "capacity": 6,
  "images": ["uploads/resources/abc123.jpg", "uploads/resources/def456.jpg"],
  "availability_rules": {"description": "24/7 access"},
  "status": "published",
  "created_at": "2025-11-05T10:00:00Z"
}
```

## Image Upload Specifications

**Allowed Extensions**: jpg, jpeg, png, gif  
**Max File Size**: 2MB per image  
**Max Files**: 5 images per resource  
**Storage**: `src/static/uploads/resources/`  
**Naming**: UUID-based random filenames (e.g., `a1b2c3d4e5f6.jpg`)  
**Security**: 
- werkzeug.secure_filename() sanitization
- File type validation (extension + MIME type check recommended)
- Size validation before save
- Files stored with random names (prevents path traversal)

## Status Lifecycle

```
draft → published → archived
  ↓         ↓
(can edit) (public listing)
```

- **draft**: Visible only to owner, can be edited freely
- **published**: Visible in public `/resources` listing, bookable
- **archived**: Hidden from public, not bookable, preserved in database

---

## Booking Endpoints (Phase 6 - Implemented)

### GET /bookings/new
**Description**: Display booking form for a specific resource  
**Auth Required**: Yes  
**Query Parameters**: 
- `resource_id` (required): ID of resource to book  

**Response 200** (HTML): Renders `bookings/new.html` with booking form  
**Response 302**: Redirects if resource not found or not published  

**Form Features**:
- Date/time pickers (HTML5 inputs with validation)
- Auto-sets minimum date to today
- Client-side validation
- Resource information display
- Conflict detection on submission

---

### POST /bookings
**Description**: Create new booking request with conflict detection  
**Auth Required**: Yes  
**Method**: POST (CSRF protected)  

**Form Data** (application/x-www-form-urlencoded):
```
resource_id (required): Integer resource ID
start_date (required): YYYY-MM-DD format
start_time (required): HH:MM format (24-hour)
end_date (required): YYYY-MM-DD format
end_time (required): HH:MM format (24-hour)
notes (optional): Text notes for booking request
```

**Validation Rules**:
- Start datetime must be in the future
- End datetime must be after start datetime
- No overlapping approved bookings for same resource
- Resource must be published

**Response 302**: Redirects to booking detail page on success  
**Response 302**: Redirects back to form with error on conflict  
**Conflict Detection**: Checks for overlapping approved bookings using `BookingService.check_booking_conflicts()`  

**Status on Creation**: `pending` (requires owner/staff approval)

---

### GET /bookings/<int:booking_id>
**Description**: View detailed booking information  
**Auth Required**: Yes (requester, resource owner, or staff/admin)  
**Path Parameters**: `booking_id` - Booking ID  

**Response 200** (HTML): Renders `bookings/detail.html`  
**Response 403**: If user not authorized to view  
**Response 404**: Booking not found  

**Displays**:
- Booking status with color-coded badge
- Resource information (title, location, category)
- Start/end date and time
- Duration calculation
- Requester information
- Notes (if provided)
- Rejection reason (if rejected)
- Action buttons based on role and status
- Timestamps (created, updated)

**Available Actions** (based on role and status):
- **Pending + Staff/Admin/Owner**: Approve or Reject
- **Pending/Approved + Requester**: Cancel
- **Approved + Admin**: Mark as Complete
- **Completed + Requester**: Leave Review link

---

### POST /bookings/<int:booking_id>/approve
**Description**: Approve pending booking  
**Auth Required**: Yes (staff, admin, or resource owner only)  
**Method**: POST (CSRF protected)  
**Decorator**: `@require_staff` (includes admin)  

**Status Transition**: pending → approved  
**Response 302**: Redirects to booking detail with success message  
**Response 403**: If unauthorized  
**Response 400**: If booking not in pending status  

**Side Effects**:
- Updates booking status to 'approved'
- Sets updated_at timestamp
- Flash success message

---

### POST /bookings/<int:booking_id>/reject
**Description**: Reject pending booking with reason  
**Auth Required**: Yes (staff, admin, or resource owner only)  
**Method**: POST (CSRF protected)  

**Form Data**:
```
rejection_reason (required): Text reason for rejection (min 10 chars)
```

**Status Transition**: pending → rejected  
**Response 302**: Redirects to booking detail  
**Response 400**: If rejection_reason missing or too short  

**Displays Rejection Modal**: Bootstrap modal with textarea for reason

---

### POST /bookings/<int:booking_id>/cancel
**Description**: Cancel booking (requester-initiated)  
**Auth Required**: Yes (requester only)  
**Method**: POST (CSRF protected)  

**Valid Statuses**: Can cancel pending or approved bookings only  
**Status Transition**: pending/approved → cancelled  
**Response 302**: Redirects to My Bookings page  
**Response 403**: If not requester  

**Confirmation**: JavaScript confirm dialog before submission

---

### POST /bookings/<int:booking_id>/complete
**Description**: Mark booking as completed (admin workflow)  
**Auth Required**: Yes (admin only)  
**Method**: POST (CSRF protected)  
**Decorator**: `@require_admin`  

**Status Transition**: approved → completed  
**Response 302**: Redirects to booking detail  
**Purpose**: Allows requester to leave reviews after completion  

**Confirmation**: JavaScript confirm dialog

---

### GET /my-bookings
**Description**: User's booking dashboard with categorized tabs  
**Auth Required**: Yes  
**Response 200** (HTML): Renders `bookings/my_bookings.html`  

**Features**:
- **Tabbed Interface**: Upcoming, Pending, Past, Cancelled/Rejected
- **Booking Counts**: Badge showing count for each tab
- **Status Filtering**: Client-side tab switching with URL hash
- **Booking Cards**: Reusable card component with quick actions
- **Empty States**: Helpful messages when no bookings exist
- **Quick Actions**: Context-sensitive buttons per booking
- **Help Section**: Status badge legend

**Tab Definitions**:
- **Upcoming**: Approved bookings (status='approved')
- **Pending**: Awaiting approval (status='pending')
- **Past**: Completed bookings (status='completed')
- **Cancelled**: Cancelled or rejected (status in ['cancelled', 'rejected'])

**Quick Actions Per Card**:
- View Details button (always shown)
- Approve button (staff/admin, pending only)
- Cancel button (requester, pending/approved only)
- Complete button (admin, approved only)
- Leave Review button (requester, completed only)

---

## Booking Data Model

```json
{
  "booking_id": 1,
  "resource_id": 5,
  "requester_id": 3,
  "start_datetime": "2025-11-06T14:00:00Z",
  "end_datetime": "2025-11-06T16:00:00Z",
  "status": "approved",
  "notes": "Need projector setup before meeting",
  "rejection_reason": null,
  "created_at": "2025-11-05T10:30:00Z",
  "updated_at": "2025-11-05T11:00:00Z"
}
```

**Status Values**:
- `pending`: Awaiting approval
- `approved`: Confirmed, upcoming
- `rejected`: Denied by owner/staff
- `cancelled`: User-cancelled
- `completed`: Finished (can review)

**Status Lifecycle**:
```
pending → approved → completed
    ↓         ↓
 rejected  cancelled
```

---

## Review Endpoints (Phase 6 - Implemented)

### POST /resources/<int:resource_id>/reviews
**Description**: Submit review for resource after completed booking  
**Auth Required**: Yes  
**Method**: POST (CSRF protected)  
**Path Parameters**: `resource_id` - Resource ID  

**Form Data**:
```
rating (required): Integer 1-5 (star rating)
comment (required): Text review (min 10 chars, max 1000 chars)
```

**Authorization Rules**:
- User must have at least one completed booking for this resource
- One review per user per resource (enforced in database)
- Cannot review own resources

**Validation**:
- Rating: Must be integer between 1 and 5
- Comment: Minimum 10 characters, maximum 1000 characters
- Server-side + client-side validation

**Response 302**: Redirects to resource detail page with success  
**Response 403**: If no completed booking or authorization failed  
**Response 400**: If validation fails or duplicate review  

**Side Effects**:
- Creates review record
- Updates resource aggregate rating
- Timestamps automatically set

---

### PUT /reviews/<int:review_id>
**Description**: Update own review  
**Auth Required**: Yes (review author only)  
**Method**: POST with `_method=PUT` hidden field  

**Form Data** (same as create):
```
rating (required): Integer 1-5
comment (required): Text (10-1000 chars)
```

**Response 302**: Redirects to resource detail page  
**Response 403**: If not review author  
**Response 404**: Review not found  

**Updates**: 
- Rating and comment can be changed
- Timestamps updated_at automatically set
- Cannot change resource_id or reviewer_id

---

### POST /reviews/<int:review_id>/delete
**Description**: Delete own review  
**Auth Required**: Yes (review author only)  
**Method**: POST (CSRF protected)  

**Response 302**: Redirects to resource detail page  
**Response 403**: If not review author  

**Confirmation**: JavaScript confirm dialog before deletion  
**Side Effects**: Soft delete or hard delete (configurable), recalculates resource aggregate rating

---

### POST /reviews/<int:review_id>/hide
**Description**: Hide inappropriate review (admin moderation)  
**Auth Required**: Yes (admin only)  
**Method**: POST (CSRF protected)  
**Decorator**: `@require_admin`  

**Response 302**: Redirects back with success message  
**Response 403**: If not admin  

**Effect**: Sets `is_hidden=True` flag  
**Display**: Hidden reviews shown only to admins with warning badge  

**Confirmation**: JavaScript confirm dialog

---

### POST /reviews/<int:review_id>/unhide
**Description**: Unhide previously hidden review  
**Auth Required**: Yes (admin only)  
**Method**: POST (CSRF protected)  
**Decorator**: `@require_admin`  

**Response 302**: Redirects back with success message  
**Effect**: Sets `is_hidden=False`, review becomes public again

---

### GET /resources/<int:resource_id>/reviews
**Description**: Get all reviews for a resource (JSON API endpoint)  
**Auth Required**: No  
**Path Parameters**: `resource_id` - Resource ID  

**Response 200** (JSON):
```json
[
  {
    "review_id": 1,
    "resource_id": 5,
    "reviewer": {
      "user_id": 3,
      "name": "John Doe",
      "profile_image": "uploads/profile_123.jpg"
    },
    "rating": 5,
    "comment": "Excellent projector! Very clear image.",
    "is_hidden": false,
    "timestamp": "2025-11-03T14:30:00Z",
    "updated_at": "2025-11-03T14:30:00Z"
  }
]
```

**Filters**: Excludes hidden reviews for non-admin users  
**Ordering**: Newest first (by timestamp DESC)

---

### GET /resources/<int:resource_id>/rating
**Description**: Get aggregate rating for resource (JSON API endpoint)  
**Auth Required**: No  
**Path Parameters**: `resource_id` - Resource ID  

**Response 200** (JSON):
```json
{
  "resource_id": 5,
  "average_rating": 4.3,
  "review_count": 12,
  "rating_distribution": {
    "5": 6,
    "4": 4,
    "3": 1,
    "2": 1,
    "1": 0
  }
}
```

**Calculation**: Average of all non-hidden reviews, rounded to 1 decimal

---

## Review Data Model

```json
{
  "review_id": 1,
  "resource_id": 5,
  "reviewer_id": 3,
  "rating": 5,
  "comment": "Excellent projector! Very clear image and easy to use. Would definitely book again.",
  "is_hidden": false,
  "timestamp": "2025-11-03T14:30:00Z",
  "updated_at": "2025-11-03T14:30:00Z"
}
```

**Field Constraints**:
- `rating`: INTEGER, CHECK (rating >= 1 AND rating <= 5)
- `comment`: TEXT, length 10-1000 characters
- `is_hidden`: BOOLEAN, default FALSE
- Unique constraint: (resource_id, reviewer_id)

**UI Components**:
- **Star Rating Input**: Interactive 5-star selection with hover effects
- **Character Counter**: Real-time feedback (green/yellow/red)
- **Review Cards**: Avatar, rating stars, comment, timestamp, actions
- **Moderation**: Admin-only hide/unhide buttons
- **Edit Mode**: Pre-fills form with existing review data

---

## Message Endpoints (Phase 7 - Implemented)

### GET /messages
**Description**: View message inbox with conversation list and statistics  
**Auth Required**: Yes  
**Response 200** (HTML): Renders `messages/inbox.html`  

**Features**:
- **Statistics Dashboard**: Total conversations, messages received, sent, unread count
- **Conversation List**: Groups messages by conversation partner
- **Unread Badges**: Shows unread count per conversation
- **Last Message Preview**: Displays most recent message in conversation
- **Timestamps**: Shows when last message was sent
- **Empty State**: Helpful message when no conversations exist
- **Quick Actions**: View conversation, start new message

**Conversation Grouping**:
- Groups messages by unique sender/receiver pair
- Most recent conversation first
- Shows partner's name and avatar
- Calculates unread count per conversation

---

### GET /messages/conversation/<int:user_id>
**Description**: View full message thread with specific user  
**Auth Required**: Yes  
**Path Parameters**: `user_id` - ID of conversation partner  

**Response 200** (HTML): Renders `messages/conversation.html`  
**Response 404**: If user not found  

**Features**:
- **Thread View**: All messages between current user and partner
- **Message Bubbles**: Different styling for sent (right, blue) vs received (left, gray)
- **Auto-scroll**: JavaScript auto-scrolls to bottom on page load
- **Reply Form**: Inline form to send new message
- **Character Counter**: Real-time character count (0/1000)
- **Delete Own Messages**: Delete button for sender's messages
- **Partner Info**: Shows partner's name and department at top
- **Timestamps**: Full timestamp for each message
- **Auto-read Marking**: Marks all messages as read when viewing

**Message Display**:
- Sent messages: Right-aligned, primary color
- Received messages: Left-aligned, light gray
- Delete button shown only on own messages
- Timestamps below each message

---

### GET /messages/compose/<int:user_id>
### POST /messages/compose/<int:user_id>
**Description**: Compose and send message to specific user  
**Auth Required**: Yes  
**Path Parameters**: `user_id` - Recipient user ID  
**Method**: GET displays form, POST sends message  

**Form Data**:
```
content (required): Message text (min 1 char, max 1000 chars)
```

**Response 302** (POST): Redirects to conversation view on success  
**Response 200** (POST): Re-renders form with error on failure  
**Response 403**: If trying to message self  
**Response 404**: If recipient not found  

**Compose Page Features**:
- **Recipient Card**: Shows who you're messaging
- **Message Textarea**: Large input with character counter
- **Guidelines**: Messaging etiquette reminders
- **Cancel Button**: Returns to inbox
- **Validation**: Client-side + server-side validation

---

### POST /messages/send
**Description**: Send message (alternative endpoint for AJAX/form submission)  
**Auth Required**: Yes  
**Method**: POST (CSRF protected)  

**Form Data**:
```
receiver_id (required): Integer recipient user ID
content (required): Message text (min 1 char, max 1000 chars)
```

**Validation**:
- Content length: 1-1000 characters
- Cannot send to self
- Recipient must exist
- Both users must be authenticated

**Response 302**: Redirects to conversation view on success  
**Response 400**: Validation errors (missing fields, invalid format)  
**Response 403**: Authorization errors (self-message, etc.)  
**Response 404**: Recipient not found  

**Side Effects**:
- Creates message record with timestamp
- Sets receiver's message as unread (`is_read=False`)
- Flash success message

---

### POST /messages/<int:message_id>/delete
**Description**: Delete own message (sender-only)  
**Auth Required**: Yes (message sender only)  
**Method**: POST (CSRF protected)  
**Path Parameters**: `message_id` - Message ID  

**Response 302**: Redirects back to conversation  
**Response 403**: If not message sender  
**Response 404**: Message not found  

**Confirmation**: JavaScript confirm dialog before deletion  
**Note**: Only sender can delete their own messages

---

### POST /messages/mark-read/<int:user_id>
**Description**: Mark all messages from specific user as read  
**Auth Required**: Yes  
**Method**: POST (CSRF protected)  
**Path Parameters**: `user_id` - Sender user ID  

**Response 302**: Redirects back to previous page  
**Effect**: Sets `is_read=True` for all messages from user_id to current user  
**Usage**: Automatically called when viewing conversation

---

### GET /messages/unread-count
**Description**: Get unread message count (AJAX endpoint for badge)  
**Auth Required**: Yes  
**Response 200** (JSON):
```json
{
  "unread_count": 5
}
```

**Usage**: Called by JavaScript to update navigation badge  
**Updates**: Can be polled periodically for real-time updates  
**Security**: Only returns count for current authenticated user

---

### GET /messages/stats
**Description**: Get messaging statistics for current user  
**Auth Required**: Yes  
**Response 200** (JSON):
```json
{
  "total_conversations": 8,
  "messages_received": 45,
  "messages_sent": 38,
  "unread_count": 3
}
```

**Calculations**:
- `total_conversations`: Unique users messaged/received from
- `messages_received`: Total messages received
- `messages_sent`: Total messages sent
- `unread_count`: Unread messages count

**Usage**: Used in inbox statistics dashboard

---

### GET /messages/about-resource/<int:resource_id>
**Description**: Send message to resource owner (convenience redirect)  
**Auth Required**: Yes  
**Path Parameters**: `resource_id` - Resource ID  

**Response 302**: Redirects to `/messages/compose/<owner_id>`  
**Response 403**: If trying to message own resource  
**Response 404**: If resource not found  

**Purpose**: Quick action from resource detail page  
**Integration**: "Message Owner" button on resource detail page  
**Usage Example**: `/messages/about-resource/15` → redirects to compose message to owner of resource 15

---

### GET /messages/about-booking/<int:booking_id>
**Description**: Send message related to specific booking  
**Auth Required**: Yes (requester or resource owner)  
**Path Parameters**: `booking_id` - Booking ID  

**Response 302**: Redirects to compose message with pre-filled context  
**Response 403**: If not authorized (not requester or owner)  
**Response 404**: If booking not found  

**Purpose**: Communicate about booking details  
**Integration**: Can be called from booking detail page  
**Pre-fills**: Message textarea with booking reference (optional enhancement)

---

## Message Data Model

```json
{
  "message_id": 1,
  "thread_id": null,
  "sender_id": 3,
  "receiver_id": 5,
  "content": "Hi! Is the projector still available for tomorrow afternoon?",
  "is_read": false,
  "timestamp": "2025-11-06T10:30:00Z"
}
```

**Field Constraints**:
- `content`: TEXT, length 1-1000 characters
- `is_read`: BOOLEAN, default FALSE
- `timestamp`: DATETIME, auto-generated
- `thread_id`: INTEGER (optional, for threading conversations)

**Relationships**:
- `sender`: FK to users.user_id
- `receiver`: FK to users.user_id

**Conversation Threading**:
- Messages grouped by sender/receiver pair
- Bidirectional: (user_a ↔ user_b) forms one conversation
- Ordered by timestamp DESC (newest first in list, oldest first in thread)

**Unread Logic**:
- Set `is_read=False` on message creation
- Set `is_read=True` when viewing conversation
- Badge shows total unread count across all conversations

---

## Navigation Integration

**Messages Link**:
- Located in main navigation bar
- Shows envelope icon
- Displays unread badge (red pill) when unread messages exist
- Badge updates via AJAX call to `/messages/unread-count`
- Badge hides when count is 0

**Resource Detail Integration**:
- "Message Owner" button in non-owner actions section
- Clicking redirects to `/messages/about-resource/<resource_id>`
- Helps users ask questions before booking
- Button only shown to authenticated, non-owner users

---

## UI Components

### Inbox Page
- **Stats Cards**: Four metric cards at top
- **Conversation List**: Card-based layout with avatars
- **Unread Badges**: Red pill badges showing count
- **Last Message**: Truncated preview of recent message
- **Timestamps**: Human-readable relative time
- **Empty State**: Encourages starting conversations

### Conversation Thread
- **Message Bubbles**: Chat-style interface
- **Sender Info**: Shows "You" for own messages
- **Auto-scroll**: Scrolls to bottom on load
- **Reply Form**: Fixed at bottom with character counter
- **Delete Buttons**: Only on own messages

### Compose Form
- **Recipient Card**: Shows who you're messaging
- **Large Textarea**: For composing message
- **Character Counter**: Real-time (0/1000)
- **Guidelines Card**: Messaging best practices
- **Action Buttons**: Send or Cancel

---

## Security & Authorization

**Message Access Rules**:
- Users can only view their own messages (sender or receiver)
- Cannot send messages to self
- Cannot delete others' messages
- Conversation view checks: must be sender or receiver
- CSRF protection on all POST endpoints

**Input Validation**:
- Content length: 1-1000 characters
- HTML escaping (Jinja auto-escape enabled)
- No XSS vulnerabilities
- SQL injection prevention (ORM parameterized queries)

**Privacy**:
- Messages visible only to sender and receiver
- No public message listing
- Admin can view messages (optional, not currently implemented)

---

## Future Enhancements (Optional)

- **Real-time Updates**: WebSocket for instant messaging
- **Threading**: Group messages by conversation thread_id
- **Attachments**: File upload in messages
- **Message Search**: Search within message history
- **Archive Conversations**: Hide old conversations
- **Block Users**: Prevent messages from specific users
- **Read Receipts**: Show when message was read
- **Typing Indicators**: Show when other user is typing
- **Push Notifications**: Browser notifications for new messages

---

## Admin Endpoints

### GET /admin/users
**Description**: List all users  
**Auth Required**: Yes (Admin only)  
**Response 200**: Array of user objects

### PUT /admin/users/:id/suspend
**Description**: Suspend user  
**Auth Required**: Yes (Admin only)  
**Response 200**: User suspended

### GET /admin/stats
**Description**: Get platform statistics  
**Auth Required**: Yes (Admin only)  
**Response 200**:
```json
{
  "total_users": 245,
  "total_resources": 89,
  "pending_approvals": 5,
  "total_bookings": 1240
}
```

---

## Error Responses

**400 Bad Request**: Invalid input
**401 Unauthorized**: Not authenticated
**403 Forbidden**: Insufficient permissions
**404 Not Found**: Resource not found
**409 Conflict**: Booking conflict
**500 Internal Server Error**: Server error

**Error Format**:
```json
{
  "status": "error",
  "message": "Description of error",
  "code": "ERROR_CODE"
}
```

---

**Status**: API specifications complete  
**Next**: Acceptance criteria documentation
