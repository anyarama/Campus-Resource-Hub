# Phase 11.5: Manual Testing Guide

**Tester**: _________________  
**Date**: November 6, 2025  
**Browser**: Chrome (Primary)  
**Screen Resolution**: _________________

---

## 🚀 Pre-Testing Setup

### 1. Ensure Flask Server is Running
```bash
# Check if server is running on port 5002
lsof -i:5002

# If not running, start it:
cd /Users/aneeshyaramati/Documents/GitHub/Campus-Resource-Hub
FLASK_APP=src/app.py flask run --port=5002
```

### 2. Open Website
- URL: `http://localhost:5002`
- Clear browser cache (Cmd+Shift+R on Mac)
- Open DevTools (F12 or Cmd+Option+I)

### 3. Test User Credentials
```
Email: admin@example.com
Password: admin123
```

---

## ✅ Test Checklist

## 1. VISUAL INSPECTION - Kelley Red Branding

### Desktop View (1920x1080)
- [ ] **Login page loads** correctly
- [ ] Login button is **Kelley Red (#990000)** - NOT blue
- [ ] Hover over login button - turns darker red
- [ ] After login, sidebar logo has red gradient
- [ ] Sidebar nav items turn red when active
- [ ] All primary buttons are red (not blue)
- [ ] Links use red color for hover/active states
- [ ] Overall appearance is professional

**Issues Found:**
```
[Write any visual issues here]




```

---

## 2. NAVIGATION TEST - All 20 Pages

### Check each page loads without errors:

#### Resources (6 pages)
- [ ] 1. Dashboard (`/dashboard`) - Shows stats or welcome message
- [ ] 2. Resources List (`/resources`) - Shows available resources
- [ ] 3. Resource Detail (`/resources/<id>`) - Pick any resource
- [ ] 4. Create Resource (`/resources/create`) - Form displays (staff/admin only)
- [ ] 5. Edit Resource (`/resources/<id>/edit`) - Form displays
- [ ] 6. My Resources (`/resources/my-resources`) - Shows your resources

#### Bookings (4 pages)
- [ ] 7. My Bookings (`/bookings/my-bookings`) - Lists your bookings
- [ ] 8. New Booking (`/bookings/new?resource_id=X`) - Booking form
- [ ] 9.Booking Detail (`/bookings/<id>`) - Shows booking details
- [ ] 10. (Approval flow works if admin)

#### Messages (3 pages)
- [ ] 11. Inbox (`/messages/inbox`) - Lists conversations
- [ ] 12. Conversation (`/messages/conversation/<id>`) - Shows thread
- [ ] 13. Compose (`/messages/compose`) - New message form

#### Admin (4 pages) - Admin Only
- [ ] 14. Admin Dashboard (`/admin/dashboard`) - Admin stats
- [ ] 15. Users List (`/admin/users`) - All users
- [ ] 16. User Detail (`/admin/users/<id>`) - User profile
- [ ] 17. Analytics (`/admin/analytics`) - Charts/graphs

#### Other (3 pages)
- [ ] 18. Profile (`/auth/profile`) - User profile page
- [ ] 19. AI Concierge (`/concierge`) - Chatbot interface
- [ ] 20. Concierge Help (`/concierge/help`) - Help docs

**Pages with Errors:**
```
[List any pages that don't load or show errors]




```

---

## 3. KEYBOARD NAVIGATION TEST

### Instructions:
1. Start on Dashboard
2. Press **Tab** key repeatedly
3. Observe focus indicator (should be visible red outline)

### Test Each Area:
- [ ] **Sidebar Navigation** - Tab highlights each nav item
- [ ] **Topbar Search** - Can focus and type
- [ ] **Topbar Buttons** - Theme toggle, messages, logout are focusable
- [ ] **Main Content** - Cards, buttons, links are focusable
- [ ] **Forms** - All inputs can be reached via Tab
- [ ] **Skip to Main Content** - Press Tab on page load, should show skip link

### Test Form Navigation:
- [ ] Go to Resources → Create Resource
- [ ] Tab through all form fields
- [ ] Can submit form with Enter key
- [ ] Can navigate back with Shift+Tab

**Keyboard Issues:**
```
[Note any areas where Tab doesn't work or focus is invisible]




```

---

## 4. MOBILE RESPONSIVE TEST

### Instructions:
1. Open Chrome DevTools (F12)
2. Click "Toggle Device Toolbar" (Cmd+Shift+M)
3. Test different screen sizes

### Screen Size Tests:

#### iPhone SE (375px x 667px)
- [ ] Sidebar hidden by default
- [ ] Hamburger menu (☰) visible in top-left
- [ ] Click hamburger → sidebar slides in from left
- [ ] Click backdrop → sidebar closes
- [ ] Content is readable (no horizontal scroll)
- [ ] Buttons are thumb-sized (44px minimum)
- [ ] Forms stack vertically nicely

#### iPad (768px x 1024px)
- [ ] Sidebar still hidden initially
- [ ] Layout looks good in portrait
- [ ] Layout looks good in landscape (rotate device)
- [ ] Touch targets are adequate

#### iPhone X (375px x 812px)
- [ ] All content fits without horizontal scroll
- [ ] Text is readable (not too small)
- [ ] Images scale properly

**Responsive Issues:**
```
[Document any layout breaks, overflow, or usability issues on mobile]




```

---

## 5. FUNCTIONALITY TEST - Core Features

### Authentication
- [ ] **Logout** works (redirects to login)
- [ ] **Login again** works
- [ ] Session persists across page refreshes

### Resources
- [ ] Can view resource details
- [ ] Can search resources (topbar search)
- [ ] Can filter resources (if filters exist)
- [ ] Images load correctly

### Bookings
- [ ] Can create a new booking
- [ ] Can view booking details
- [ ] Can cancel a booking (if allowed)
- [ ] Status badges show correctly (pending/approved/etc.)

### Messages
- [ ] Can send a new message
- [ ] Can view conversation
- [ ] Can reply to messages

### Admin (if admin user)
- [ ] Can view all users
- [ ] Can view analytics
- [ ] Admin dashboard shows stats

**Functional Issues:**
```
[Note any broken features, errors, or unexpected behavior]




```

---

## 6. ACCESSIBILITY CHECK

### Screen Reader Simulation:
- [ ] Navigate to Dashboard
- [ ] Look at the page source (View → Developer → View Source)
- [ ] Verify `<main>`, `<nav>`, `<aside>` tags are present
- [ ] Verify images have `alt="..."` attributes
- [ ] Verify buttons have `aria-label` or descriptive text

### Check ARIA Landmarks:
- [ ] Sidebar has `role="navigation"`
- [ ] Main content has `<main>` tag
- [ ] Skip link exists (Tab on first page load)

### Color Contrast:
- [ ] Text on white background is dark enough to read easily
- [ ] Red buttons have sufficient contrast with white text
- [ ] Gray text (secondary info) is readable

**Accessibility Issues:**
```
[Note any missing labels, poor contrast, or accessibility concerns]




```

---

## 7. BROWSER CONSOLE CHECK

### Look for Errors:
1. Open DevTools → Console tab
2. Reload the page (Cmd+R)
3. Navigate to different pages
4. Check for red error messages

### Expected: Zero Errors
- [ ] No JavaScript errors
- [ ] No 404 errors (missing files)
- [ ] No CORS errors
- [ ] No CSS errors

**Console Errors Found:**
```
[Copy/paste any error messages from console]




```

---

## 8. PERFORMANCE CHECK

### Page Load Speed:
- [ ] Dashboard loads in < 2 seconds
- [ ] Resource list loads in < 2 seconds
- [ ] No noticeable lag when clicking links
- [ ] Images load progressively (not all at once blocking page)

### Interactions Feel Snappy:
- [ ] Button hover effects are instant
- [ ] Form inputs respond immediately
- [ ] Sidebar slide animation is smooth (not janky)

**Performance Issues:**
```
[Note any slow pages or laggy interactions]




```

---

## 9. EMPTY STATES & EDGE CASES

### Test Empty States:
- [ ] New user with no bookings - shows helpful empty state?
- [ ] No messages - shows empty state with CTA?
- [ ] No resources found (search "xyz123") - shows empty state?

### Test Error Handling:
- [ ] Try to access non-existent resource (`/resources/99999`)
- [ ] Try to book with invalid dates
- [ ] Try to submit form with missing required fields

**Edge Case Issues:**
```
[Document how app handles empty states and errors]




```

---

## 10. THEME TOGGLE TEST

### Dark Mode Toggle:
- [ ] Click moon/sun icon in topbar
- [ ] Page theme changes (if dark mode implemented)
- [ ] Theme persists on page reload
- [ ] Theme toggle icon updates correctly

**Theme Issues:**
```
[If dark mode doesn't work or has issues, note them]




```

---

## 📊 OVERALL ASSESSMENT

### Rating (1-10)
- **Visual Design**: _____ / 10
- **Functionality**: _____ / 10
- **Responsiveness**: _____ / 10
- **Accessibility**: _____ / 10
- **Performance**: _____ / 10

### **Overall**: _____ / 10

### Top 3 Issues to Fix:
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### What Works Great:
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

---

## 🎯 NEXT STEPS

After completing this test:

1. **Report Issues**: Share this completed checklist
2. **Screenshot Capture**: If everything works, capture screenshots of all 20 pages
3. **Fix Critical Bugs**: Address any major issues found
4. **Re-test**: Verify fixes work

---

## 📸 SCREENSHOT CHECKLIST (If Testing Passes)

Capture high-quality screenshots (1920x1080) of:

### Desktop Screenshots (13 required):
- [ ] 01_login_page.png
- [ ] 02_dashboard.png
- [ ] 03_resources_list.png
- [ ] 04_resource_detail.png
- [ ] 05_create_resource.png
- [ ] 06_my_bookings.png
- [ ] 07_booking_detail.png
- [ ] 08_messages_inbox.png
- [ ] 09_conversation.png
- [ ] 10_ai_concierge.png
- [ ] 11_admin_dashboard.png
- [ ] 12_user_profile.png
- [ ] 13_analytics.png

### Mobile Screenshots (3 required):
- [ ] mobile_01_dashboard_375px.png
- [ ] mobile_02_sidebar_open_375px.png
- [ ] mobile_03_resource_list_375px.png

**Save screenshots to**: `docs/screens/`

---

**Testing Complete!** ✅  
Date Completed: _________________  
Total Time: _________________  
Ready for Next Phase: [ ] Yes  [ ] No (needs fixes)
