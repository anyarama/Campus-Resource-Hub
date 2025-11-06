"""
Campus Resource Hub - Admin Routes
AiDD 2025 Capstone Project

Admin dashboard and platform management routes.

AI Contribution: Cline generated admin routes structure
Reviewed and extended by developer on 2025-11-06
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from src.security.rbac import require_admin
from src.services.admin_service import AdminService, AdminServiceError
from src.repositories.user_repo import UserRepository

# Create admin blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required
@require_admin
def dashboard():
    """
    Admin dashboard with platform overview and statistics.
    
    GET /admin/dashboard
    
    Security: Admin only
    
    Returns:
        HTML: Dashboard with stats cards, charts, recent activity
    """
    try:
        # Get platform statistics
        raw_stats = AdminService.get_platform_stats()
        
        # Restructure stats for template (nested dictionaries)
        stats = {
            'total_users': raw_stats['total_users'],
            'total_resources': raw_stats['total_resources'],
            'published_resources': raw_stats['published_resources'],
            'total_bookings': raw_stats['total_bookings'],
            'pending_bookings': raw_stats['pending_bookings'],
            'total_messages': raw_stats['total_messages'],
            'total_reviews': raw_stats['total_reviews'],
            'role_distribution': {
                'admin': raw_stats['admins'],
                'staff': raw_stats['staff'],
                'student': raw_stats['students']
            },
            'booking_status': {
                'pending': raw_stats['pending_bookings'],
                'approved': raw_stats['approved_bookings'],
                'completed': raw_stats['completed_bookings'],
                'cancelled': raw_stats['cancelled_bookings']
            }
        }
        
        # Get recent activity
        activity = AdminService.get_recent_activity(limit=10)
        
        # Get popular resources
        popular_resources = AdminService.get_popular_resources(limit=5)
        
        # Get booking trends (last 30 days)
        raw_trends = AdminService.get_booking_trends(days=30)
        
        # Restructure trends for template
        trends = {
            'total_bookings': raw_trends['total_bookings'],
            'approved_bookings': raw_trends['by_status'].get('approved', 0),
            'pending_bookings': raw_trends['by_status'].get('pending', 0),
            'completed_bookings': raw_trends['by_status'].get('completed', 0),
            'cancelled_bookings': raw_trends['by_status'].get('cancelled', 0) + raw_trends['by_status'].get('rejected', 0),
            'rejected_bookings': raw_trends['by_status'].get('rejected', 0)
        }
        
        return render_template(
            'admin/dashboard.html',
            stats=stats,
            activity=activity,
            popular_resources=popular_resources,
            trends=trends
        )
        
    except AdminServiceError as e:
        flash(f"Error loading dashboard: {e}", "danger")
        # Return with default empty structures
        empty_stats = {
            'total_users': 0,
            'total_resources': 0,
            'published_resources': 0,
            'total_bookings': 0,
            'pending_bookings': 0,
            'total_messages': 0,
            'total_reviews': 0,
            'role_distribution': {'admin': 0, 'staff': 0, 'student': 0},
            'booking_status': {'pending': 0, 'approved': 0, 'completed': 0, 'cancelled': 0}
        }
        empty_trends = {
            'total_bookings': 0,
            'approved_bookings': 0,
            'pending_bookings': 0,
            'completed_bookings': 0,
            'cancelled_bookings': 0,
            'rejected_bookings': 0
        }
        return render_template(
            'admin/dashboard.html',
            stats=empty_stats,
            activity={'bookings': [], 'users': []},
            popular_resources=[],
            trends=empty_trends
        )


@admin_bp.route('/users')
@login_required
@require_admin
def users():
    """
    User management interface - list all users with search/filter.
    
    GET /admin/users?search=<term>&role=<role>&status=<status>&page=<num>
    
    Query Parameters:
        search: Search by name or email
        role: Filter by role (admin/staff/student)
        status: Filter by status (active/suspended)
        page: Page number (default 1)
    
    Security: Admin only
    
    Returns:
        HTML: User list with management actions
    """
    try:
        # Get query parameters
        search_term = request.args.get('search', '')
        role_filter = request.args.get('role', '')
        status_filter = request.args.get('status', '')
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        # Get all users (with pagination in future)
        users = UserRepository.get_all(role=role_filter if role_filter else None)
        
        # Apply search filter
        if search_term:
            search_lower = search_term.lower()
            users = [u for u in users if search_lower in u.name.lower() or search_lower in u.email.lower()]
        
        # Apply status filter
        if status_filter == 'active':
            users = [u for u in users if u.is_active]
        elif status_filter == 'suspended':
            users = [u for u in users if not u.is_active]
        
        # Get user stats
        total_users = len(users)
        active_count = sum(1 for u in users if u.is_active)
        suspended_count = total_users - active_count
        
        return render_template(
            'admin/users.html',
            users=users,
            search_term=search_term,
            role_filter=role_filter,
            status_filter=status_filter,
            total_users=total_users,
            active_count=active_count,
            suspended_count=suspended_count,
            page=page
        )
        
    except Exception as e:
        flash(f"Error loading users: {e}", "danger")
        return render_template('admin/users.html', users=[])


@admin_bp.route('/users/<int:user_id>')
@login_required
@require_admin
def user_detail(user_id):
    """
    View detailed user information and activity.
    
    GET /admin/users/<user_id>
    
    Security: Admin only
    
    Returns:
        HTML: User detail page with activity summary
    """
    try:
        # Get user details
        user = UserRepository.get_by_id(user_id)
        if not user:
            flash("User not found", "danger")
            return redirect(url_for('admin.users'))
        
        # Get user activity summary
        activity = AdminService.get_user_activity_summary(user_id)
        
        return render_template(
            'admin/user_detail.html',
            user=user,
            activity=activity
        )
        
    except AdminServiceError as e:
        flash(f"Error loading user details: {e}", "danger")
        return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/suspend', methods=['POST'])
@login_required
@require_admin
def suspend_user(user_id):
    """
    Suspend a user account.
    
    POST /admin/users/<user_id>/suspend
    
    Security: 
        - Admin only
        - Cannot suspend admins
        - Cannot suspend self
    
    Returns:
        Redirect: Back to user list with success/error message
    """
    try:
        AdminService.suspend_user(user_id, current_user.user_id)
        flash("User suspended successfully", "success")
        
    except AdminServiceError as e:
        flash(f"Error suspending user: {e}", "danger")
    
    # Redirect back to referring page or user list
    return redirect(request.referrer or url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/activate', methods=['POST'])
@login_required
@require_admin
def activate_user(user_id):
    """
    Activate a suspended user account.
    
    POST /admin/users/<user_id>/activate
    
    Security: Admin only
    
    Returns:
        Redirect: Back to user list with success/error message
    """
    try:
        AdminService.activate_user(user_id)
        flash("User activated successfully", "success")
        
    except AdminServiceError as e:
        flash(f"Error activating user: {e}", "danger")
    
    return redirect(request.referrer or url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@require_admin
def delete_user(user_id):
    """
    Permanently delete a user account.
    
    POST /admin/users/<user_id>/delete
    
    WARNING: Destructive operation - deletes all user data.
    
    Security:
        - Admin only
        - Cannot delete admins
        - Cannot delete self
        - Requires confirmation in UI
    
    Returns:
        Redirect: Back to user list with success/error message
    """
    try:
        AdminService.delete_user(user_id, current_user.user_id)
        flash("User deleted successfully", "success")
        return redirect(url_for('admin.users'))
        
    except AdminServiceError as e:
        flash(f"Error deleting user: {e}", "danger")
        return redirect(request.referrer or url_for('admin.users'))


@admin_bp.route('/analytics')
@login_required
@require_admin
def analytics():
    """
    Platform analytics and insights.
    
    GET /admin/analytics?period=<days>
    
    Query Parameters:
        period: Time period in days (7, 30, or 90, default 30)
    
    Security: Admin only
    
    Returns:
        HTML: Analytics dashboard with charts and trends
    """
    try:
        # Get period parameter (default 30 days)
        period = request.args.get('period', 30, type=int)
        if period not in [7, 30, 90]:
            period = 30
        
        # Get platform stats
        raw_stats = AdminService.get_platform_stats()
        
        # Restructure stats for template
        stats = {
            'total_users': raw_stats['total_users'],
            'total_resources': raw_stats['total_resources'],
            'published_resources': raw_stats['published_resources'],
            'total_bookings': raw_stats['total_bookings'],
            'pending_bookings': raw_stats['pending_bookings'],
            'total_messages': raw_stats['total_messages'],
            'total_reviews': raw_stats['total_reviews'],
            'role_distribution': {
                'admin': raw_stats['admins'],
                'staff': raw_stats['staff'],
                'student': raw_stats['students']
            }
        }
        
        # Get popular resources
        popular_resources = AdminService.get_popular_resources(limit=10)
        
        # Get booking trends for selected period
        raw_trends = AdminService.get_booking_trends(days=period)
        
        # Restructure trends for template
        trends = {
            'total_bookings': raw_trends['total_bookings'],
            'approved_bookings': raw_trends['by_status'].get('approved', 0),
            'pending_bookings': raw_trends['by_status'].get('pending', 0),
            'completed_bookings': raw_trends['by_status'].get('completed', 0),
            'cancelled_bookings': raw_trends['by_status'].get('cancelled', 0) + raw_trends['by_status'].get('rejected', 0),
            'rejected_bookings': raw_trends['by_status'].get('rejected', 0)
        }
        
        return render_template(
            'admin/analytics.html',
            stats=stats,
            popular_resources=popular_resources,
            trends=trends,
            period=period
        )
        
    except AdminServiceError as e:
        flash(f"Error loading analytics: {e}", "danger")
        return render_template('admin/analytics.html', stats={}, period=30)


@admin_bp.route('/stats')
@login_required
@require_admin
def stats():
    """
    Get platform statistics as JSON (for AJAX/API calls).
    
    GET /admin/stats
    
    Security: Admin only
    
    Returns:
        JSON: Platform statistics
    """
    try:
        stats = AdminService.get_platform_stats()
        return jsonify(stats), 200
        
    except AdminServiceError as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/ping')
@login_required
@require_admin
def ping():
    """
    Health check endpoint for admin dashboard.
    
    GET /admin/ping
    
    Security: Admin only
    
    Returns:
        JSON: Status and admin info
    """
    return jsonify({
        'status': 'ok',
        'admin_id': current_user.user_id,
        'admin_name': current_user.name,
        'role': current_user.role,
        'timestamp': str(datetime.utcnow())
    }), 200


# Import datetime for ping endpoint
from datetime import datetime
