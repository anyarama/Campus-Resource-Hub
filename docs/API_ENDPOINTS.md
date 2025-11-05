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

## Resource Endpoints

### GET /resources
**Description**: List/search resources  
**Auth Required**: No  
**Query Parameters**:
- `q`: Search keyword
- `category`: Filter by category
- `location`: Filter by location
- `capacity`: Minimum capacity
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)

**Response 200**:
```json
{
  "resources": [{
    "resource_id": 1,
    "title": "Library Room 204",
    "category": "study_room",
    "location": "Main Library",
    "capacity": 8,
    "rating": 4.8,
    "status": "published"
  }],
  "total": 45,
  "page": 1,
  "pages": 3
}
```

### GET /resources/:id
**Description**: Get resource details  
**Auth Required**: No  
**Response 200**:
```json
{
  "resource_id": 1,
  "title": "Library Room 204",
  "description": "Spacious study room...",
  "owner": {"id": 5, "name": "Library Staff"},
  "rating": 4.8,
  "reviews_count": 42
}
```

### POST /resources
**Description**: Create new resource  
**Auth Required**: Yes  
**Request Body**:
```json
{
  "title": "Study Room A",
  "description": "Quiet study space",
  "category": "study_room",
  "location": "Library 2F",
  "capacity": 6
}
```
**Response 201**: Created resource object

### PUT /resources/:id
**Description**: Update resource  
**Auth Required**: Yes (Owner or Admin)  
**Response 200**: Updated resource

### DELETE /resources/:id
**Description**: Delete resource  
**Auth Required**: Yes (Owner or Admin)  
**Response 204**: No content

---

## Booking Endpoints

### POST /bookings
**Description**: Create booking request  
**Auth Required**: Yes  
**Request Body**:
```json
{
  "resource_id": 1,
  "start_datetime": "2025-11-05T14:00:00",
  "end_datetime": "2025-11-05T16:00:00"
}
```
**Response 201**: Booking created
**Response 409**: Conflict (overlapping booking)

### GET /bookings
**Description**: Get user's bookings  
**Auth Required**: Yes  
**Query Parameters**: `status` (pending/approved/past)  
**Response 200**: Array of booking objects

### GET /bookings/:id
**Description**: Get booking details  
**Auth Required**: Yes  
**Response 200**: Booking object with resource details

### PUT /bookings/:id/approve
**Description**: Approve booking  
**Auth Required**: Yes (Resource owner or Admin)  
**Response 200**: `{"status": "approved"}`

### PUT /bookings/:id/reject
**Description**: Reject booking  
**Auth Required**: Yes (Resource owner or Admin)  
**Response 200**: `{"status": "rejected"}`

### DELETE /bookings/:id
**Description**: Cancel booking  
**Auth Required**: Yes (Requester only)  
**Response 204**: No content

---

## Review Endpoints

### POST /reviews
**Description**: Submit review  
**Auth Required**: Yes  
**Request Body**:
```json
{
  "resource_id": 1,
  "rating": 5,
  "comment": "Excellent space!"
}
```
**Response 201**: Review created
**Response 403**: No completed booking found

### GET /reviews
**Description**: Get reviews for resource  
**Query Parameters**: `resource_id` (required)  
**Response 200**: Array of review objects

---

## Message Endpoints

### POST /messages
**Description**: Send message  
**Auth Required**: Yes  
**Request Body**:
```json
{
  "receiver_id": 5,
  "content": "Is the room available?"
}
```
**Response 201**: Message sent

### GET /messages
**Description**: Get user's messages  
**Auth Required**: Yes  
**Query Parameters**: `type` (inbox/sent)  
**Response 200**: Array of message objects

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
