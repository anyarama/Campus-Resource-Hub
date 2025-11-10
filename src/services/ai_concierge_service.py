"""
Campus Resource Hub - AI Concierge Service
AiDD 2025 Capstone Project - Phase 9

Natural language query parsing and resource search service.
Uses regex-based pattern matching for reliable parameter extraction.

AI Contribution: Cline generated initial service structure and regex patterns
Reviewed and extended by developer on 2025-11-06
"""

import re
from typing import Dict, List, Optional, Any
from src.repositories.resource_repo import ResourceRepository


class QueryParser:
    """
    Parse natural language queries to extract search parameters.

    Uses regex patterns to identify:
    - Intent (search, book, help)
    - Category (study room, lab, equipment, etc.)
    - Capacity (number of people)
    - Date/Time (tomorrow, next week, afternoon, etc.)
    - Location (building names, floors)
    """

    # Category pattern mapping
    CATEGORY_PATTERNS = {
        "Study Room": r"\b(study\s*room|study\s*space|study\s*area|quiet\s*room)\b",
        "Lab": r"\b(lab|laboratory|computer\s*lab)\b",
        "Equipment": r"\b(equipment|projector|laptop|av\s*equipment|camera|device)\b",
        "Conference Room": r"\b(conference\s*room|meeting\s*room|meeting\s*space)\b",
        "Office": r"\b(office|workspace)\b",
    }

    # Intent patterns
    INTENT_PATTERNS = {
        "search": r"\b(find|show|need|looking\s*for|available|search|get|give\s*me)\b",
        "book": r"\b(book|reserve|schedule)\b",
        "help": r"\b(how|what|help|explain|tell\s*me)\b",
    }

    # Capacity patterns
    CAPACITY_PATTERN = r"\b(?:for|seats?|capacity|room\s*for|accommodate|hold)\s*(\d+)(?:\s*people|persons|students)?\b"

    # Date patterns
    DATE_PATTERNS = {
        "today": r"\b(today|now)\b",
        "tomorrow": r"\b(tomorrow|tmrw|tommorow)\b",  # Handle typos
        "weekend": r"\b(this\s*weekend|weekend)\b",
        "next_week": r"\b(next\s*week)\b",
        "monday": r"\b(next\s*)?monday\b",
        "tuesday": r"\b(next\s*)?tuesday\b",
        "wednesday": r"\b(next\s*)?wednesday\b",
        "thursday": r"\b(next\s*)?thursday\b",
        "friday": r"\b(next\s*)?friday\b",
        "saturday": r"\b(next\s*)?saturday\b",
        "sunday": r"\b(next\s*)?sunday\b",
    }

    # Time period patterns
    TIME_PATTERNS = {
        "morning": r"\b(morning|am)\b",
        "afternoon": r"\b(afternoon|pm)\b",
        "evening": r"\b(evening|night)\b",
    }

    # Location patterns
    LOCATION_PATTERN = (
        r"\b(?:in|at|near|on)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+Hall|\s+Building)?)\b"
    )

    @classmethod
    def parse_query(cls, query: str) -> Dict[str, Any]:
        """
        Parse a natural language query and extract parameters.

        Args:
            query: User's natural language query (e.g., "Find a study room for 4 people")

        Returns:
            Dictionary with extracted parameters:
            {
                'intent': 'search'|'book'|'help',
                'category': str or None,
                'capacity': int or None,
                'date': str or None,
                'time': str or None,
                'location': str or None,
                'keywords': List[str],
                'original_query': str
            }
        """
        query_lower = query.lower()

        params = {
            "intent": cls._extract_intent(query_lower),
            "category": cls._extract_category(query_lower),
            "capacity": cls._extract_capacity(query_lower),
            "date": cls._extract_date(query_lower),
            "time": cls._extract_time(query_lower),
            "location": cls._extract_location(query),
            "keywords": cls._extract_keywords(query_lower),
            "original_query": query,
        }

        return params

    @classmethod
    def _extract_intent(cls, query: str) -> str:
        """Extract user intent from query."""
        for intent, pattern in cls.INTENT_PATTERNS.items():
            if re.search(pattern, query, re.IGNORECASE):
                return intent
        return "search"  # Default intent

    @classmethod
    def _extract_category(cls, query: str) -> Optional[str]:
        """Extract resource category from query."""
        for category, pattern in cls.CATEGORY_PATTERNS.items():
            if re.search(pattern, query, re.IGNORECASE):
                return category
        return None

    @classmethod
    def _extract_capacity(cls, query: str) -> Optional[int]:
        """Extract capacity requirement from query."""
        match = re.search(cls.CAPACITY_PATTERN, query, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, IndexError):
                return None
        return None

    @classmethod
    def _extract_date(cls, query: str) -> Optional[str]:
        """Extract date reference from query."""
        for date_key, pattern in cls.DATE_PATTERNS.items():
            if re.search(pattern, query, re.IGNORECASE):
                return date_key
        return None

    @classmethod
    def _extract_time(cls, query: str) -> Optional[str]:
        """Extract time period from query."""
        for time_key, pattern in cls.TIME_PATTERNS.items():
            if re.search(pattern, query, re.IGNORECASE):
                return time_key
        return None

    @classmethod
    def _extract_location(cls, query: str) -> Optional[str]:
        """Extract location (building name) from query."""
        match = re.search(cls.LOCATION_PATTERN, query)
        if match:
            return match.group(1)
        return None

    @classmethod
    def _extract_keywords(cls, query: str) -> List[str]:
        """Extract potential search keywords from query."""
        # Remove common words
        stop_words = {
            "find",
            "show",
            "me",
            "need",
            "looking",
            "for",
            "a",
            "an",
            "the",
            "in",
            "at",
            "on",
            "is",
            "are",
            "with",
            "and",
            "or",
        }

        words = re.findall(r"\b\w+\b", query.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 2]

        return keywords[:5]  # Limit to 5 keywords


class AIConciergeService:
    """
    AI-powered Resource Concierge service.

    Handles natural language queries, searches database,
    and formats conversational responses.
    """

    @classmethod
    def process_query(cls, query: str, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Process a natural language query and return search results.

        Args:
            query: User's natural language query
            user_id: Optional user ID for logging

        Returns:
            Dictionary with:
            {
                'success': bool,
                'message': str (conversational response),
                'results': List[Resource],
                'params': Dict (extracted parameters),
                'suggestions': List[str] (if no results)
            }
        """
        # Input validation
        if not query or len(query.strip()) == 0:
            return cls._error_response("Please enter a search query.")

        if len(query) > 500:
            return cls._error_response("Query too long. Please keep it under 500 characters.")

        # Parse query
        params = QueryParser.parse_query(query)

        # Handle different intents
        if params["intent"] == "help":
            return cls._help_response(params)

        if params["intent"] == "book":
            return cls._booking_intent_response(params)

        # Search intent (default)
        return cls._search_resources(params)

    @classmethod
    def _search_resources(cls, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search for resources based on extracted parameters.

        Args:
            params: Extracted query parameters

        Returns:
            Response dictionary with results and conversational message
        """
        # Build search filters
        filters = {}

        if params["category"]:
            filters["category"] = params["category"]

        if params["capacity"]:
            filters["min_capacity"] = params["capacity"]

        if params["location"]:
            filters["location"] = params["location"]

        # Search database (only published resources)
        try:
            all_resources = ResourceRepository.search(
                query_str=None,
                category=filters.get("category"),
                location=filters.get("location"),
                status="published",
            )

            # Filter by capacity if specified
            if "min_capacity" in filters:
                all_resources = [
                    r for r in all_resources if r.capacity and r.capacity >= filters["min_capacity"]
                ]

            # Format response
            if len(all_resources) == 0:
                return cls._no_results_response(params, filters)

            elif len(all_resources) == 1:
                return cls._single_result_response(all_resources[0], params)

            else:
                return cls._multiple_results_response(all_resources, params, filters)

        except Exception as e:
            return cls._error_response(f"Search error: {str(e)}")

    @classmethod
    def _multiple_results_response(
        cls, resources: List, params: Dict, filters: Dict
    ) -> Dict[str, Any]:
        """Format response for multiple results."""
        count = len(resources)
        category = params.get("category", "resources")

        # Build message
        msg_parts = []

        # Greeting with context
        if params.get("time") and params.get("date"):
            msg_parts.append(
                f"I found {count} {category} available {params['date']} {params['time']}:"
            )
        elif params.get("capacity"):
            msg_parts.append(
                f"I found {count} {category} that can accommodate {params['capacity']} people:"
            )
        else:
            msg_parts.append(f"I found {count} {category} matching your search:")

        message = "\n\n".join(msg_parts)

        return {
            "success": True,
            "message": message,
            "results": resources[:10],  # Limit to top 10
            "total_count": count,
            "params": params,
            "filters": filters,
            "suggestions": [],
        }

    @classmethod
    def _single_result_response(cls, resource, params: Dict) -> Dict[str, Any]:
        """Format response for single result."""
        msg = "I found exactly what you're looking for!\n\n"
        msg += f"**{resource.title}**"

        if resource.capacity:
            msg += f"\n• Capacity: {resource.capacity} people"
        if resource.location:
            msg += f"\n• Location: {resource.location}"

        msg += "\n\nWould you like to book this resource?"

        return {
            "success": True,
            "message": msg,
            "results": [resource],
            "total_count": 1,
            "params": params,
            "suggestions": [],
        }

    @classmethod
    def _no_results_response(cls, params: Dict, filters: Dict) -> Dict[str, Any]:
        """Format response when no results found."""
        category = params.get("category", "resources")

        msg = f"I couldn't find any {category}"

        if params.get("capacity"):
            msg += f" that can accommodate {params['capacity']} people"

        if params.get("date") or params.get("time"):
            time_desc = " ".join(filter(None, [params.get("date"), params.get("time")]))
            msg += f" available {time_desc}"

        msg += ".\n\n**Here's what you can try:**\n"
        msg += "• Search for a different time or date\n"
        msg += "• Reduce capacity requirements\n"
        msg += "• Try a different resource category\n"
        msg += "• Browse all available resources"

        suggestions = [
            "Try different dates or times",
            "Browse all resources",
            "Adjust search criteria",
        ]

        return {
            "success": False,
            "message": msg,
            "results": [],
            "total_count": 0,
            "params": params,
            "filters": filters,
            "suggestions": suggestions,
        }

    @classmethod
    def _help_response(cls, params: Dict) -> Dict[str, Any]:
        """Format help/information response."""
        msg = "**🤖 Resource Concierge Help**\n\n"
        msg += "I can help you find campus resources using natural language!\n\n"
        msg += "**Try queries like:**\n"
        msg += "• 'Find a study room for 4 people'\n"
        msg += "• 'I need a projector for tomorrow'\n"
        msg += "• 'Show me available labs this weekend'\n"
        msg += "• 'Conference room for 20 people next Tuesday'\n\n"
        msg += "**Available Resources:**\n"
        msg += "• Study Rooms\n"
        msg += "• Labs & Equipment\n"
        msg += "• Conference Rooms\n"
        msg += "• Office Spaces"

        return {
            "success": True,
            "message": msg,
            "results": [],
            "total_count": 0,
            "params": params,
            "is_help": True,
        }

    @classmethod
    def _booking_intent_response(cls, params: Dict) -> Dict[str, Any]:
        """Format response when user wants to book (redirect to search then booking)."""
        msg = "Ready to book a resource? Let me show you what's available...\n\n"
        msg += "I'll search for options and you can click 'Book Now' on any resource you like."

        # Perform the search
        search_result = cls._search_resources(params)
        search_result["message"] = msg + "\n\n" + search_result["message"]
        search_result["is_booking_intent"] = True

        return search_result

    @classmethod
    def _error_response(cls, error_message: str) -> Dict[str, Any]:
        """Format error response."""
        return {
            "success": False,
            "message": f"❌ {error_message}",
            "results": [],
            "total_count": 0,
            "params": {},
            "error": True,
        }

    @classmethod
    def get_example_queries(cls) -> List[str]:
        """
        Get list of example queries for UI prompts.

        Returns:
            List of example query strings
        """
        return [
            "Find a study room for 4 people",
            "I need a projector for tomorrow",
            "Show me available labs this weekend",
            "Conference room for 20 people",
            "Study space for tomorrow afternoon",
            "Equipment available next week",
        ]


# Custom exception for AI service errors
class AIConciergeError(Exception):
    """Exception raised for errors in the AI Concierge service."""

    pass
