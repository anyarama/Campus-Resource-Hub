# Wireframes - Campus Resource Hub
## UI/UX Design Specifications

**Project**: Campus Resource Hub - AiDD 2025 Capstone Project  
**Version**: 1.0  
**Date**: November 3, 2025  
**Design Goal**: Enterprise-grade UI (like Airbnb/Notion/Linear, NOT generic Bootstrap)

---

## Design System

### Color Palette
- Primary: #2563EB (Blue)
- Secondary: #10B981 (Green) 
- Accent: #F59E0B (Amber)
- Error: #EF4444 (Red)
- Background: #F9FAFB
- Surface: #FFFFFF
- Text: #111827 / #6B7280

### Typography
- Font: Inter, system-ui
- H1: 2.5rem Bold
- H2: 2rem Semibold
- Body: 1rem Regular

---

## Screen 1: Homepage

**Layout**: Hero + Search + Featured Resources

**Components**:
- Navigation bar with logo, search, user menu
- Large search box with AI query placeholder
- Category filter buttons
- Resource cards grid (4 cols desktop, responsive)
- Each card: Image, Title, Rating, Capacity, Availability badge

**Interactions**:
- Search: Natural language queries
- Cards: Hover overlay with "Book Now" / "View Details"

---

## Screen 2: Search Results

**Layout**: Sidebar filters + Results grid

**Filters** (Collapsible sidebar):
- Category checkboxes
- Location dropdown
- Capacity radio buttons
- Availability toggle

**Results**:
- List cards with image, title, details, CTA buttons
- Sort dropdown (Recent, Popular, Rating)
- Pagination

---

## Screen 3: Resource Detail

**Layout**: Image gallery + Info + Booking CTA

**Sections**:
1. Image carousel with thumbnails
2. Title, rating, location, capacity, amenities
3. Availability calendar (month view, color-coded)
4. Reviews list with verified badges
5. Prominent "Book This Resource" button

---

## Screen 4: Booking Flow (Modal/Page)

**Steps**:
1. Select date/time (calendar + time slots)
2. Add details (purpose, notes)
3. Review & confirm

**Features**:
- Visual time slot selector
- Conflict detection warnings
- Approval requirement notice

---

## Screen 5: User Dashboard

**Tabs**: Upcoming | Pending | Past | Cancelled

**Each booking card**:
- Resource thumbnail
- Date/time
- Status badge
- Actions: Cancel, Message Owner, Leave Review

---

## Screen 6: My Resources (Staff/Admin)

**Layout**: Resource list + Create button

**Table columns**:
- Title, Category, Status, Bookings, Rating, Actions

**Actions**: Edit, Archive, View Bookings

---

## Screen 7: Messages/Inbox

**Layout**: Thread list + Message pane (split view)

**Left**: Conversation list with unread badges
**Right**: Message thread with reply box

---

## Screen 8: Admin Dashboard

**Layout**: Stats cards + Management sections

**Stat Cards**:
- Total Users
- Active Resources
- Pending Approvals
- Recent Activity

**Sections**:
- User Management table
- Resource Moderation queue
- Booking Approvals
- Analytics charts

---

## Screen 9: Review Submission

**Layout**: Modal/Form

**Fields**:
- Star rating (1-5, interactive)
- Comment textarea
- Submit/Cancel buttons

**Validation**: Only after completed booking

---

## Screen 10: Profile Settings

**Sections**:
- Profile info (name, email, department)
- Profile image upload
- Password change
- Notification preferences

---

## Responsive Breakpoints

- Mobile: < 640px (single column, hamburger menu)
- Tablet: 640-1024px (2 columns, collapsible sidebar)
- Desktop: > 1024px (full layout, persistent sidebar)

---

## Accessibility (WCAG 2.1 AA)

- Semantic HTML (nav, main, article, aside)
- Proper heading hierarchy (h1 → h2 → h3)
- ARIA labels on all interactive elements
- Keyboard navigation support (tab order, focus visible)
- Color contrast minimum 4.5:1
- Alt text on all images
- Form labels and error messages

---

## Key UI Components

1. **Resource Card**: Reusable component with image, info, status
2. **Calendar Picker**: Interactive date/time selector
3. **Status Badge**: Color-coded (Available=green, Busy=yellow, Full=red)
4. **Rating Display**: Star icons + count
5. **Modal**: Overlay for booking, reviews, confirmations
6. **Toast Notifications**: Success/error feedback
7. **Loading Skeleton**: Placeholder while data loads
8. **Empty State**: Helpful message when no results

---

**Status**: Wireframes complete - ready for implementation  
**Next**: API endpoint specifications
