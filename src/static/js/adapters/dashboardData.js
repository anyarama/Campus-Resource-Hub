/**
 * Dashboard Data Adapter
 * Fetches dashboard metrics with mock fallback
 * 
 * AI Contribution: Initial data adapter pattern and mock data structure
 * Reviewed and customized by developer on 2025-11-09
 */

/**
 * Mock dashboard data for development/fallback
 */
const MOCK_DASHBOARD_DATA = {
  kpis: {
    myResources: {
      value: 8,
      change: +2,
      changeLabel: 'from last month',
    },
    activeBookings: {
      value: 12,
      change: +3,
      changeLabel: 'from last week',
    },
    unreadMessages: {
      value: 5,
      change: -2,
      changeLabel: 'from yesterday',
    },
    avgRating: {
      value: 4.7,
      change: +0.3,
      changeLabel: 'from last month',
      outOf: 5,
    },
  },
  
  // Bookings over time (line chart data)
  bookingsTimeline: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Bookings',
        data: [12, 19, 15, 25, 22, 30],
      },
    ],
  },
  
  // Resource category breakdown (doughnut chart data)
  categoryMix: {
    labels: ['Study Rooms', 'Equipment', 'Meeting Spaces', 'Lab Resources', 'Other'],
    data: [45, 25, 15, 10, 5],
  },
  
  // Upcoming bookings
  upcomingBookings: [
    {
      id: 101,
      resource: 'Conference Room A',
      startTime: '2025-11-10T14:00:00',
      endTime: '2025-11-10T16:00:00',
      status: 'approved',
      requester: 'John Doe',
    },
    {
      id: 102,
      resource: 'MacBook Pro 16"',
      startTime: '2025-11-11T09:00:00',
      endTime: '2025-11-11T17:00:00',
      status: 'pending',
      requester: 'Jane Smith',
    },
    {
      id: 103,
      resource: 'Study Room B',
      startTime: '2025-11-12T10:00:00',
      endTime: '2025-11-12T12:00:00',
      status: 'approved',
      requester: 'Bob Johnson',
    },
  ],
  
  // Recent activity feed
  recentActivity: [
    {
      id: 1,
      type: 'booking_approved',
      message: 'Your booking for Conference Room A was approved',
      timestamp: '2025-11-09T13:30:00',
      icon: 'check-circle',
    },
    {
      id: 2,
      type: 'new_message',
      message: 'New message from Jane Smith about Lab Equipment',
      timestamp: '2025-11-09T12:15:00',
      icon: 'message-circle',
    },
    {
      id: 3,
      type: 'booking_requested',
      message: 'New booking request for MacBook Pro',
      timestamp: '2025-11-09T11:45:00',
      icon: 'calendar',
    },
    {
      id: 4,
      type: 'review_received',
      message: 'You received a 5-star review for Study Room A',
      timestamp: '2025-11-09T09:20:00',
      icon: 'star',
    },
  ],
};

/**
 * Fetch dashboard data from API with fallback to mock
 * @param {boolean} useMock - Force use of mock data (default: false)
 * @returns {Promise<Object>} Dashboard data
 */
export async function fetchDashboardData(useMock = false) {
  // If mock is forced, return immediately
  if (useMock) {
    console.log('[Dashboard] Using mock data (forced)');
    return Promise.resolve(MOCK_DASHBOARD_DATA);
  }
  
  try {
    // Attempt to fetch from API endpoint
    const response = await fetch('/api/dashboard', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
      credentials: 'same-origin',
    });
    
    if (!response.ok) {
      throw new Error(`API returned ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    console.log('[Dashboard] Loaded data from API');
    return data;
    
  } catch (error) {
    // Fallback to mock data on error
    console.warn('[Dashboard] API fetch failed, using mock data:', error.message);
    return MOCK_DASHBOARD_DATA;
  }
}

/**
 * Fetch KPI metrics only
 * @returns {Promise<Object>} KPI data
 */
export async function fetchKPIs() {
  try {
    const response = await fetch('/api/dashboard/kpis', {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
      credentials: 'same-origin',
    });
    
    if (!response.ok) throw new Error(`API error: ${response.status}`);
    return await response.json();
    
  } catch (error) {
    console.warn('[Dashboard] KPI fetch failed, using mock:', error.message);
    return MOCK_DASHBOARD_DATA.kpis;
  }
}

/**
 * Fetch bookings timeline for chart
 * @param {string} period - Time period ('week', 'month', 'year')
 * @returns {Promise<Object>} Timeline data
 */
export async function fetchBookingsTimeline(period = 'month') {
  try {
    const response = await fetch(`/api/dashboard/bookings-timeline?period=${period}`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
      credentials: 'same-origin',
    });
    
    if (!response.ok) throw new Error(`API error: ${response.status}`);
    return await response.json();
    
  } catch (error) {
    console.warn('[Dashboard] Timeline fetch failed, using mock:', error.message);
    return MOCK_DASHBOARD_DATA.bookingsTimeline;
  }
}

/**
 * Fetch category mix for chart
 * @returns {Promise<Object>} Category data
 */
export async function fetchCategoryMix() {
  try {
    const response = await fetch('/api/dashboard/category-mix', {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
      credentials: 'same-origin',
    });
    
    if (!response.ok) throw new Error(`API error: ${response.status}`);
    return await response.json();
    
  } catch (error) {
    console.warn('[Dashboard] Category mix fetch failed, using mock:', error.message);
    return MOCK_DASHBOARD_DATA.categoryMix;
  }
}

/**
 * Fetch upcoming bookings
 * @param {number} limit - Number of bookings to fetch (default: 5)
 * @returns {Promise<Array>} Bookings array
 */
export async function fetchUpcomingBookings(limit = 5) {
  try {
    const response = await fetch(`/api/dashboard/upcoming-bookings?limit=${limit}`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
      credentials: 'same-origin',
    });
    
    if (!response.ok) throw new Error(`API error: ${response.status}`);
    return await response.json();
    
  } catch (error) {
    console.warn('[Dashboard] Upcoming bookings fetch failed, using mock:', error.message);
    return MOCK_DASHBOARD_DATA.upcomingBookings.slice(0, limit);
  }
}

/**
 * Fetch recent activity feed
 * @param {number} limit - Number of activities to fetch (default: 10)
 * @returns {Promise<Array>} Activity array
 */
export async function fetchRecentActivity(limit = 10) {
  try {
    const response = await fetch(`/api/dashboard/recent-activity?limit=${limit}`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
      credentials: 'same-origin',
    });
    
    if (!response.ok) throw new Error(`API error: ${response.status}`);
    return await response.json();
    
  } catch (error) {
    console.warn('[Dashboard] Activity feed fetch failed, using mock:', error.message);
    return MOCK_DASHBOARD_DATA.recentActivity.slice(0, limit);
  }
}

/**
 * Format date for display
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
export function formatDateTime(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now - date;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);
  
  // Relative time for recent items
  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  
  // Absolute date for older items
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined,
  });
}

/**
 * Format time range for display
 * @param {string} startTime - ISO start time
 * @param {string} endTime - ISO end time
 * @returns {string} Formatted time range
 */
export function formatTimeRange(startTime, endTime) {
  const start = new Date(startTime);
  const end = new Date(endTime);
  
  const formatTime = (date) => {
    return date.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true,
    });
  };
  
  const formatDate = (date) => {
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
    });
  };
  
  // Same day
  if (start.toDateString() === end.toDateString()) {
    return `${formatDate(start)}, ${formatTime(start)} - ${formatTime(end)}`;
  }
  
  // Different days
  return `${formatDate(start)} ${formatTime(start)} - ${formatDate(end)} ${formatTime(end)}`;
}

/**
 * Get status badge color
 * @param {string} status - Status string
 * @returns {string} CSS class suffix
 */
export function getStatusColor(status) {
  const statusMap = {
    approved: 'success',
    pending: 'warning',
    rejected: 'danger',
    cancelled: 'secondary',
    completed: 'info',
  };
  
  return statusMap[status] || 'secondary';
}

/**
 * Get activity icon class
 * @param {string} type - Activity type
 * @returns {string} Lucide icon name
 */
export function getActivityIcon(type) {
  const iconMap = {
    booking_approved: 'check-circle',
    booking_rejected: 'x-circle',
    booking_requested: 'calendar',
    new_message: 'message-circle',
    review_received: 'star',
    resource_created: 'plus-circle',
    resource_updated: 'edit',
  };
  
  return iconMap[type] || 'bell';
}

export { MOCK_DASHBOARD_DATA };
