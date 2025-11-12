# Authentication System Design Components

## Overview
This document outlines the authentication component library for the Campus Resource Hub, aligned with the Indiana University Admin Panel design system.

---

## 📁 Component Structure

### Forms
- **cmp/form/login-card** - `LoginCard.tsx`
- **cmp/form/signup-card** - `SignUpCard.tsx`

### Inputs
- **cmp/input/email** - `EmailInput.tsx`
- **cmp/input/password** - `PasswordInput.tsx`
- **cmp/input/confirm-password** - `ConfirmPasswordInput.tsx`

### Buttons
- **cmp/button/auth-primary** - `AuthPrimaryButton.tsx`

### Links
- **cmp/link/inline** - `InlineLink.tsx`

### Alerts
- **cmp/alert/form-feedback** - `FormFeedbackAlert.tsx`

### Dropdowns
- **cmp/dropdown/role-select** - `RoleSelect.tsx`

---

## 🎨 Design Tokens

### Colors
```
Brand Crimson: #990000
Brand Cream: #FBFAF9
Neutral Border: #E9E4DD
Error Red: #B71C1C
Error Background: #FFF8F8
Success Green: #1B5E20
Success Background: #E8F5E9
Info Amber: #F57C00
Info Background: #FFF3E0
Primary Text: #1E1E1E
Secondary Text: #6E6E6E
```

### Spacing (8pt Grid)
```
Gap Small: 6px
Gap Medium: 8px
Gap Large: 12px
Card Padding: 32px
Input Height: 40-44px
Button Height: 44px
```

### Border Radius
```
Cards: 16px
Form Inputs: 12px
Buttons: 12px
Alerts: 8px
```

### Elevation
```
Card Shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1)
Button Shadow: 0 1px 2px rgba(0,0,0,0.06)
```

### Focus States
```
Normal Focus: 0 0 0 2px rgba(153, 0, 0, 0.18)
Error Focus: 0 0 0 2px rgba(183, 28, 28, 0.18)
Transition: 200ms ease-in-out
```

---

## 📝 Component Usage Guidelines

### cmp/form/login-card
**Use case:** Use login-card for all secure entry points.

**Specifications:**
- Size: 480×520px
- Contains: Email input, password input, remember me checkbox, primary button
- Supports: Error states, loading states, success states
- Navigation: Links to forgot password and sign up

**Example:**
```tsx
<LoginCard 
  onNavigateToSignUp={() => navigate('/signup')}
  onSuccess={(data) => handleLogin(data)}
/>
```

---

### cmp/form/signup-card
**Use case:** Use signup-card for all new user registration flows.

**Specifications:**
- Size: 520×auto (responsive height)
- Contains: Name, email, password, confirm password, role select, terms checkbox
- Supports: Multiple validation states, info banners, success feedback
- Navigation: Link to login

**Example:**
```tsx
<SignUpCard 
  onNavigateToLogin={() => navigate('/login')}
  onSuccess={(data) => handleSignup(data)}
/>
```

---

### cmp/input/email
**Use case:** Use for all email entry fields requiring @iu.edu validation.

**Features:**
- Auto-validation for IU email format
- Error state with helper text
- Focus ring animation
- Disabled state support

**Props:**
- `value`: string
- `onChange`: (value: string) => void
- `error?`: boolean
- `disabled?`: boolean

---

### cmp/input/password
**Use case:** Use for password entry with show/hide functionality.

**Features:**
- Toggle visibility (eye icon)
- Secure input masking
- Focus ring animation
- Icon hover states

**Props:**
- `value`: string
- `onChange`: (value: string) => void
- `disabled?`: boolean
- `label?`: string

---

### cmp/input/confirm-password
**Use case:** Use for password confirmation during account creation.

**Features:**
- Mismatch validation
- Error state with helper text
- Toggle visibility
- Focus ring animation

**Props:**
- `value`: string
- `onChange`: (value: string) => void
- `error?`: boolean
- `disabled?`: boolean

---

### cmp/button/auth-primary
**Use case:** Use for primary authentication actions (Login, Sign Up, Submit).

**States:**
- **Default:** Crimson background, white text
- **Hover:** Darker crimson (#8A0000)
- **Loading:** Spinner + "Authenticating..."
- **Success:** Checkmark + "Success!" with animation
- **Active:** Scale down (0.98) for tactile feedback

**Props:**
- `isLoading?`: boolean
- `isSuccess?`: boolean
- `loadingText?`: string
- `successText?`: string

---

### cmp/link/inline
**Use case:** Use for secondary navigation within forms (forgot password, sign up, etc.).

**Variants:**
- **primary:** Crimson text (#990000) - for CTAs
- **secondary:** Muted text (#6E6E6E) - for less important links

**Features:**
- Animated underline on hover (100ms)
- Caption sizing (13px)
- Keyboard accessible

---

### cmp/alert/form-feedback
**Use case:** Use for inline form feedback (errors, success, info messages).

**Variants:**
- **error:** Red border + crimson icon + light red background
- **success:** Green border + green icon/text + light green background
- **info:** Amber border + amber icon/text + light amber background

**Example:**
```tsx
<FormFeedbackAlert variant="error">
  Invalid credentials. Please check your email and password.
</FormFeedbackAlert>
```

---

### cmp/dropdown/role-select
**Use case:** Role-select dropdown restricted to staff/admin contexts. Use during signup to determine user access level.

**Options:**
- **Student:** Standard access for IU students
- **Staff:** Enhanced access for IU staff members
- **Administrator:** Full system access for admin users

**Features:**
- Custom focus ring (crimson)
- Disabled state support
- Consistent height with form inputs (40px)

---

## 🔒 Implementation Notes

### Admin Panel Alignment
All components maintain strict alignment with the existing Admin Panel design system:

1. **No detached components:** All components extend base ShadCN UI components
2. **Consistent tokens:** Border colors, radii, shadows match admin panel
3. **Typography:** Maintains Inter font stack with proper weights
4. **Grid system:** All spacing follows 8pt grid
5. **Accessibility:** WCAG AA compliant focus states and contrast ratios

### Responsive Considerations
- Login card: Fixed 480×520px (fits 1024px viewport)
- Signup card: Responsive height (optimized for vertical space)
- All inputs: Full width within container
- Focus states: Minimum 2px visible ring

### Animation Timings
- Link underline: 100ms ease-in-out
- Input focus: 200ms ease-in-out
- Button success: 300ms scale + fade
- Checkbox tick: 120ms ease-in
- Page transition: 300ms ease-out

---

## 📦 Import Guide

```tsx
// Import all components from the auth module
import {
  LoginCard,
  SignUpCard,
  EmailInput,
  PasswordInput,
  ConfirmPasswordInput,
  AuthPrimaryButton,
  InlineLink,
  FormFeedbackAlert,
  RoleSelect
} from './components/auth';

// Or import individually
import { LoginCard } from './components/auth/LoginCard';
import { EmailInput } from './components/auth/inputs/EmailInput';
```

---

## 🎯 Design System Checklist

- ✅ All components use IU brand colors
- ✅ 8pt grid system maintained
- ✅ Border radius consistent (8px, 12px, 16px)
- ✅ Focus rings use crimson brand color
- ✅ Error states use consistent red (#B71C1C)
- ✅ Typography follows Admin Panel standards
- ✅ Elevation/shadows match admin components
- ✅ All components documented with usage guidelines
- ✅ Props interfaces exported for TypeScript support
- ✅ Accessibility features included (ARIA, focus management)

---

## 📋 Figma Integration

When creating these components in Figma:

1. Create a new page titled "📁 Authentication System"
2. Add each component with its designated name (cmp/form/login-card, etc.)
3. Include usage captions below each component
4. Ensure all design tokens match this specification
5. Create variants for different states (default, hover, focus, error, disabled)
6. Link components to existing Admin Panel tokens
7. Document any deviations from this spec in Figma comments

---

**Version:** 1.0.0  
**Last Updated:** November 2025  
**Maintained By:** Campus Resource Hub Design Team
