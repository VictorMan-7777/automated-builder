# Phase 003: Content Library

## Phase Information

- **Phase**: 003
- **Name**: Content Library
- **Status**: Not Started
- **Estimated Duration**: 2-3 hours
- **Dependencies**: Phase 002 complete

## Overview

Phase 003 creates the structured content library that feeds the template system. This includes defining content schemas, organizing content by type (scriptures, themes, prayers, reflections), implementing content validation and retrieval, and populating with sample data.

## Objectives

1. Define content schemas for each content type
2. Create content directory structure
3. Implement content loading and retrieval
4. Build content validation system
5. Populate library with sample content
6. Create content indexing/search capability

## Commit Points

### CP6: Content Structure and Sample Data

**Goal**: Define content organization and create initial content library

#### Tasks

1. Create content schemas:
   - `src/content/schemas/scripture-schema.json`
   - `src/content/schemas/theme-schema.json`
   - `src/content/schemas/prayer-schema.json`
   - `src/content/schemas/reflection-schema.json`

2. Create `src/content/content_item.py`:
   - Base `ContentItem` class
   - Subclasses: `Scripture`, `Theme`, `Prayer`, `Reflection`
   - Common properties: id, title, content, metadata, tags
   - Type-specific properties

3. Populate sample content:
   - **Scriptures** (10 examples):
     - `src/content/scriptures/001-psalm-23.json`
     - `src/content/scriptures/002-john-3-16.json`
     - `src/content/scriptures/003-philippians-4-13.json`
     - etc.
   - **Themes** (10 examples):
     - `src/content/themes/001-faith.json`
     - `src/content/themes/002-hope.json`
     - `src/content/themes/003-love.json`
     - etc.
   - **Prayers** (10 examples):
     - `src/content/prayers/001-morning-prayer.json`
     - `src/content/prayers/002-thanksgiving.json`
     - `src/content/prayers/003-guidance.json`
     - etc.
   - **Reflections** (10 examples):
     - `src/content/reflections/001-trusting-god.json`
     - `src/content/reflections/002-overcoming-fear.json`
     - `src/content/reflections/003-finding-peace.json`
     - etc.

4. Create `src/content/content_loader.py`:
   - `ContentLoader` class
   - `load_content()` - Load single content item by path
   - `load_directory()` - Load all content from directory
   - Parse JSON and create ContentItem objects

5. Create `tests/test_content/test_content_item.py`:
   - Test ContentItem base class
   - Test each subclass
   - Test property access
   - Test serialization/deserialization

6. Create `tests/test_content/test_content_loader.py`:
   - Test loading single item
   - Test loading directory
   - Test error handling for missing files
   - Test error handling for malformed JSON

#### Content Schema Structures

**Scripture Schema**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "reference", "text", "version"],
  "properties": {
    "id": {"type": "string"},
    "reference": {"type": "string"},
    "text": {"type": "string"},
    "version": {"type": "string"},
    "book": {"type": "string"},
    "chapter": {"type": "integer"},
    "verses": {"type": "string"},
    "tags": {"type": "array", "items": {"type": "string"}},
    "themes": {"type": "array", "items": {"type": "string"}}
  }
}
```

**Theme Schema**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "name", "description"],
  "properties": {
    "id": {"type": "string"},
    "name": {"type": "string"},
    "description": {"type": "string"},
    "related_themes": {"type": "array", "items": {"type": "string"}},
    "scripture_references": {"type": "array", "items": {"type": "string"}},
    "tags": {"type": "array", "items": {"type": "string"}}
  }
}
```

**Prayer Schema**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "title", "content"],
  "properties": {
    "id": {"type": "string"},
    "title": {"type": "string"},
    "content": {"type": "string"},
    "type": {"enum": ["praise", "thanksgiving", "petition", "intercession", "confession"]},
    "themes": {"type": "array", "items": {"type": "string"}},
    "tags": {"type": "array", "items": {"type": "string"}}
  }
}
```

**Reflection Schema**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "title", "content"],
  "properties": {
    "id": {"type": "string"},
    "title": {"type": "string"},
    "content": {"type": "string"},
    "questions": {"type": "array", "items": {"type": "string"}},
    "action_points": {"type": "array", "items": {"type": "string"}},
    "themes": {"type": "array", "items": {"type": "string"}},
    "tags": {"type": "array", "items": {"type": "string"}}
  }
}
```

#### Verification Steps

- [ ] All content schemas defined and valid
- [ ] ContentItem classes implemented
- [ ] At least 40 sample content items created (10 per type)
- [ ] ContentLoader loads items successfully
- [ ] All sample content validates against schemas
- [ ] At least 10 tests passing

#### Acceptance Criteria

- Four content schemas defined and valid
- ContentItem base class and subclasses implemented
- At least 10 examples per content type
- All sample content is valid JSON
- ContentLoader successfully loads all content
- At least 10 passing tests
- Content is well-organized and easy to find

#### Rollback Procedure

**Risk Level**: Low

If issues occur:
1. Revert to CP5: `git checkout CP5`
2. Review content schema design
3. Simplify if too complex
4. Re-create sample content with corrected schema

**Recovery**:
- Schema issues: Validate with JSON Schema validator
- Sample content errors: Use validation to identify and fix
- Loading errors: Test with minimal example first

---

### CP7: Content Validation and Retrieval

**Goal**: Implement content validation, search, and retrieval capabilities

#### Tasks

1. Create `src/validators/content_validator.py`:
   - `ContentValidator` class
   - `validate_schema()` - Schema validation
   - `validate_references()` - Check cross-references (themes, scriptures)
   - `validate_completeness()` - Ensure required fields populated
   - Generate validation reports

2. Create `src/content/content_library.py`:
   - `ContentLibrary` class
   - `load_all()` - Load all content from all directories
   - `get_by_id()` - Retrieve content by ID
   - `get_by_type()` - Retrieve all content of specific type
   - `search()` - Search by tags, themes, keywords
   - `filter()` - Filter content by criteria
   - `get_random()` - Get random content item(s)

3. Enhance content items with relationships:
   - Link themes to related scriptures
   - Link reflections to themes
   - Link prayers to themes
   - Create content relationship graph

4. Create `src/content/content_index.py`:
   - `ContentIndex` class
   - Index by ID (fast lookup)
   - Index by tags (search)
   - Index by themes (filtering)
   - Index by type (retrieval)

5. Create `tests/test_validators/test_content_validator.py`:
   - Test schema validation
   - Test reference validation
   - Test completeness validation
   - Test with invalid content (negative tests)

6. Create `tests/test_content/test_content_library.py`:
   - Test loading all content
   - Test retrieval by ID
   - Test search functionality
   - Test filtering
   - Test random selection

7. Create `tests/test_content/test_content_index.py`:
   - Test index creation
   - Test index lookups
   - Test index updates

8. Create `examples/content-browser.py`:
   - Demonstration script
   - Load content library
   - Search and filter examples
   - Display content

#### Content Relationships

```
Theme
  ├── related_themes → [Theme IDs]
  ├── scripture_references → [Scripture IDs]
  └── used_in → [Reflection IDs, Prayer IDs]

Scripture
  ├── themes → [Theme IDs]
  └── used_in → [Reflection IDs]

Reflection
  ├── themes → [Theme IDs]
  ├── scriptures → [Scripture IDs]
  └── related_prayers → [Prayer IDs]

Prayer
  ├── themes → [Theme IDs]
  └── related_reflections → [Reflection IDs]
```

#### Search and Filter Capabilities

1. **Search by tag**: Find all content with specific tag
2. **Search by theme**: Find all content related to theme
3. **Search by keyword**: Find content containing keyword in title/content
4. **Filter by type**: Get all scriptures, prayers, etc.
5. **Combined search**: Multiple criteria (AND/OR logic)
6. **Random selection**: Get random item(s) optionally filtered by criteria

#### Verification Steps

- [ ] Content validator validates all sample content
- [ ] ContentLibrary loads all content successfully
- [ ] All retrieval methods work correctly
- [ ] Search returns expected results
- [ ] Filtering works with multiple criteria
- [ ] Random selection provides diverse results
- [ ] Content index improves lookup performance
- [ ] At least 20 tests passing
- [ ] Content browser example runs successfully

#### Acceptance Criteria

- Content validator checks schema and references
- ContentLibrary manages all content types
- Retrieval by ID is fast (< 10ms)
- Search and filter work correctly
- Random selection provides diverse results
- Content relationships are maintained
- At least 20 passing tests
- Content browser demonstrates all capabilities
- Documentation explains search/filter syntax

#### Rollback Procedure

**Risk Level**: Low

If issues occur:
1. Revert to CP6: `git checkout CP6`
2. Review retrieval and search requirements
3. Simplify search logic if too complex
4. Re-implement incrementally

**Recovery**:
- Validation errors: Fix content or relax validation rules
- Performance issues: Add caching or lazy loading
- Search complexity: Start with simple tag search, expand gradually

---

## Phase Acceptance Criteria

All of the following must be true to consider Phase 003 complete:

### Content Schemas
- [x] All four content schemas defined and valid
- [x] Schemas cover all requirements
- [x] Schemas support future extensibility

### Content Organization
- [x] Content directories properly structured
- [x] At least 40 sample content items (10 per type)
- [x] All sample content validates against schemas
- [x] Content uses consistent ID format

### Content Loading
- [x] ContentLoader reads JSON files
- [x] ContentItem objects created correctly
- [x] Error handling for missing/malformed files

### Content Validation
- [x] Schema validation works
- [x] Reference validation works
- [x] Validation reports are detailed

### Content Retrieval
- [x] Load all content efficiently
- [x] Retrieve by ID works
- [x] Filter by type works
- [x] Search by tags/themes works
- [x] Random selection works

### Content Relationships
- [x] Themes link to scriptures
- [x] Reflections link to themes
- [x] Relationships are bidirectional where appropriate

### Testing
- [x] At least 30 tests passing (15 per commit point)
- [x] Tests cover all content types
- [x] Tests cover positive and negative cases

### Documentation
- [x] Content schemas documented
- [x] Content organization explained
- [x] Search/filter syntax documented
- [x] Content browser example demonstrates usage

## Gatekeeper Checklist

### Human Review Required

- [ ] Sample content is appropriate and high-quality
- [ ] Content organization is intuitive
- [ ] Search capabilities meet user needs
- [ ] Content relationships make sense

### AI Review Recommended

- [ ] Content validation is comprehensive
- [ ] Search/filter logic handles edge cases
- [ ] Performance is acceptable for expected library size
- [ ] Content relationships are maintained correctly

### Review Questions

1. Is sample content representative of real usage?
2. Can content authors easily add new content?
3. Is the search capability intuitive?
4. Do content relationships enhance usability?
5. Is the content library scalable?

## Common Issues and Solutions

### Issue 1: Content Reference Errors

**Symptom**: Referenced IDs not found

**Solution**:
1. Validate all IDs exist before saving relationships
2. Implement reference checking in validation
3. Provide tools to find broken references
4. Consider referential integrity constraints

### Issue 2: Search Performance Slow

**Symptom**: Search takes too long with large library

**Solution**:
1. Implement content indexing
2. Cache search results
3. Use lazy loading for large result sets
4. Optimize search algorithms

### Issue 3: Content Inconsistency

**Symptom**: Content quality varies, missing fields

**Solution**:
1. Enforce required fields in schema
2. Provide content templates
3. Create content validation checklist
4. Review all content before adding to library

### Issue 4: Complex Content Relationships

**Symptom**: Difficult to maintain bidirectional relationships

**Solution**:
1. Consider uni-directional relationships only
2. Auto-generate reverse relationships
3. Use relationship management tools
4. Document relationship conventions clearly

## Testing Strategy

### Unit Tests (Phase 003)

- Content schema validation
- ContentItem creation and properties
- Content loading from files
- Content search and filter logic
- Content index operations

### Integration Tests (Phase 003)

- Load entire content library
- Search across all content types
- Validate all relationships
- Random selection with filters

### Manual Tests (Phase 003)

- [ ] Load all sample content
- [ ] Search for specific themes
- [ ] Filter by tags
- [ ] Verify relationships are correct
- [ ] Test random selection diversity
- [ ] Run content browser example

## Success Metrics

- [ ] Content loading time: < 1 second for 40 items
- [ ] Search time: < 100ms
- [ ] Retrieval by ID: < 10ms
- [ ] 100% of sample content validates
- [ ] Search finds expected items (100% recall for tag search)
- [ ] At least 30 passing tests

## Dependencies and Prerequisites

### Phase Dependencies
- Phase 002 complete (CP5)
- Template system operational
- Validation framework available

### Technical Dependencies
- JSON Schema validation
- File system access
- Search/indexing capabilities

### Knowledge Requirements
- JSON data modeling
- Search algorithms
- Content organization best practices

## Next Steps

After Phase 003 completion:

1. Commit all changes: `git commit -m "Complete Phase 003: Content Library"`
2. Tag the commit: `git tag CP7`
3. Update iteration log with Phase 003 results
4. Begin Phase 004: Validation & Preview

## Notes and Observations

### Design Decisions

**Decision**: JSON files for content storage
- **Rationale**: Human-readable, easily version-controlled, no database needed
- **Alternative**: Database (SQLite, PostgreSQL)
- **Trade-off**: Simplicity vs. advanced query capabilities

**Decision**: Tag-based search
- **Rationale**: Simple, flexible, extensible
- **Alternative**: Full-text search engine
- **Trade-off**: Performance vs. complexity

**Decision**: 10 examples per content type
- **Rationale**: Sufficient for testing, demonstrates variety
- **Alternative**: More examples (50+)
- **Trade-off**: Time to create vs. comprehensiveness

**Decision**: Bidirectional relationships
- **Rationale**: Easier navigation between related content
- **Alternative**: Uni-directional only
- **Trade-off**: Maintenance complexity vs. usability

### Potential Improvements

- Full-text search with ranking
- Content versioning and history
- Content approval workflow
- Bulk content import tools
- Content statistics and analytics
- Related content suggestions (ML-based)

### Related Documentation

- [Project Index](../index.md)
- [PRD](../prd.md)
- [Roadmap](../roadmap.md)
- [Iteration Log](../iteration-log.md)
- [Phase 002](./002-template-system.md)

---

**Phase Status**: Not Started
**Previous Phase**: [002-template-system.md](./002-template-system.md)
**Next Phase**: [004-validation-preview.md](./004-validation-preview.md)
