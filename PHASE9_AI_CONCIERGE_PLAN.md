# Phase 9: AI-Powered Resource Concierge - Implementation Plan

## Overview
Implementing a **Resource Concierge** that uses AI to interpret natural language queries and help users find campus resources.

## Feature Specification

### User Stories
1. **As a student**, I want to ask "Find a study room for 4 people tomorrow afternoon" and get relevant results
2. **As a faculty member**, I want to type "I need a projector for my presentation next Tuesday" without using complex filters
3. **As any user**, I want natural language search that understands my intent

### Technical Requirements
- **AI Grounding**: Must reference real database data (no fabrications)
- **Fallback**: Graceful handling if AI service unavailable
- **Security**: Sanitize AI inputs and outputs
- **Logging**: Document all AI interactions in `.prompt/dev_notes.md`
- **Context**: Reference artifacts from `/docs/context/`

### Implementation Options
- **Option A**: Local LLM using Ollama (no API costs, privacy)
- **Option B**: OpenAI API (more powerful, requires API key)
- **Option C**: Rule-based NLP with regex patterns (simple, reliable fallback)

**Decision**: Start with Option C (rule-based) as a reliable foundation, with hooks for future LLM integration.

## Architecture

### Components to Build

1. **AI Service Layer** (`src/services/ai_concierge_service.py`)
   - Parse natural language queries
   - Extract intent and parameters (date, time, capacity, category, etc.)
   - Convert to database filters
   - Query ResourceRepository
   - Format results with conversational response

2. **Routes** (`src/routes/ai.py` or extend `resources.py`)
   - `GET /concierge` - Concierge search interface
   - `POST /concierge/query` - Process natural language query
   - `GET /concierge/suggestions` - Get example queries

3. **Templates**
   - `src/templates/concierge/index.html` - Main concierge interface
   - `src/templates/concierge/results.html` - Results with AI explanation
   - Enhanced search bar component for homepage

4. **Context Documentation** (`/docs/context/AI/`)
   - `concierge_spec.md` - AI behavior specification
   - `example_queries.md` - Training examples for future LLM
   - `query_patterns.md` - Pattern matching rules

5. **Tests**
   - `tests/unit/test_ai_concierge.py` - Unit tests for query parsing
   - `tests/integration/test_concierge_flow.py` - End-to-end user flow

## Implementation Steps

### Step 1: Context & Documentation Setup
- [ ] Create `/docs/context/AI/` folder
- [ ] Document concierge specification
- [ ] Create example query patterns
- [ ] Define response templates

### Step 2: AI Service Layer
- [ ] Create `AIConciergeService` class
- [ ] Implement query parser (regex-based patterns)
- [ ] Extract parameters: date, time, capacity, category, location
- [ ] Handle common patterns:
  - "find/show/need [resource] for [#] people [time]"
  - "available [category] [time]"
  - "book [resource] [time]"
- [ ] Convert to ResourceRepository filters
- [ ] Format conversational responses

### Step 3: Routes & Controllers
- [ ] Create blueprint `ai_bp` or extend `resources_bp`
- [ ] Implement concierge index route
- [ ] Implement query processing endpoint
- [ ] Add CSRF protection
- [ ] Handle errors gracefully

### Step 4: UI/UX
- [ ] Design concierge interface (chat-like or search-enhanced)
- [ ] Create conversational result cards
- [ ] Add example query chips/buttons
- [ ] Integrate with existing search page
- [ ] Add "Ask Concierge" button to navbar

### Step 5: Testing
- [ ] Test query parsing accuracy
- [ ] Test parameter extraction
- [ ] Test database grounding (no fabricated results)
- [ ] Test error handling
- [ ] Test UI flow end-to-end

### Step 6: Documentation
- [ ] Log implementation in `.prompt/dev_notes.md`
- [ ] Update README with AI feature description
- [ ] Document query patterns for users
- [ ] Add to API_ENDPOINTS.md

## Query Parsing Logic

### Pattern Examples

```python
PATTERNS = {
    'capacity': r'(?:for|room for|seats for|capacity)\s+(\d+)',
    'date': r'(?:tomorrow|today|on\s+\w+|next\s+\w+|\d{1,2}/\d{1,2})',
    'time': r'(?:morning|afternoon|evening|night|\d{1,2}(?::\d{2})?\s*(?:am|pm))',
    'category': r'(?:study room|lab|equipment|projector|conference room)',
    'duration': r'(?:for|about)\s+(\d+)\s+(?:hour|hr)',
}
```

### Examples

| Query | Extracted Parameters | SQL Filters |
|-------|---------------------|-------------|
| "Find a study room for 4 people tomorrow afternoon" | capacity=4, category='study room', date=tomorrow, time=afternoon | capacity >= 4, category='Study Room', available tomorrow 1-5pm |
| "I need a projector for next Tuesday" | category='projector', date=next_tuesday | category LIKE '%projector%', available on date |
| "Show me available labs this weekend" | category='lab', date=this_weekend | category='Lab', available Sat/Sun |

## Success Metrics

- **Accuracy**: 80%+ correct parameter extraction on test queries
- **Coverage**: Handle 10+ common query patterns
- **Performance**: < 1 second response time
- **Reliability**: Graceful fallback if pattern doesn't match
- **User Satisfaction**: Clear, helpful responses

## Future Enhancements (Post-MVP)

- Integrate Ollama for true NLU (natural language understanding)
- Learn from user query corrections
- Multi-turn conversations ("And what about Friday?")
- Personalized suggestions based on booking history
- Voice input support

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Complex queries fail | Provide example queries, fallback to standard search |
| User expects too much | Set clear expectations ("I can help you find resources...") |
| Performance issues | Cache common patterns, optimize regex |
| Security (prompt injection) | Sanitize inputs, whitelist parameters |

---

## Begin Implementation

Starting with Step 1: Context & Documentation Setup
