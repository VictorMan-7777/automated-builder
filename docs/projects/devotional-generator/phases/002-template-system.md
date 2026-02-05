# Phase 002: Template System

## Phase Information

- **Phase**: 002
- **Name**: Template System
- **Status**: Not Started
- **Estimated Duration**: 2-3 hours
- **Dependencies**: Phase 001 complete

## Overview

Phase 002 builds the core template engine for the Devotional Generator. This includes defining the JSON template schema, implementing template parsing and validation, creating variable substitution logic, and developing sample templates.

## Objectives

1. Define JSON template schema
2. Implement template parser
3. Build template validation system
4. Create variable substitution engine
5. Develop sample templates
6. Write comprehensive tests

## Commit Points

### CP3: Template Schema and Basic Parser

**Goal**: Define template structure and implement basic parsing

#### Tasks

1. Create `src/templates/schema.json`:
   - Define template structure (metadata, sections, variables)
   - Specify required fields
   - Define section types (scripture, reflection, prayer, action)
   - Define variable placeholder format

2. Create `src/templates/template.py`:
   - `Template` class to represent a template
   - `load_template()` function to read JSON file
   - `parse_template()` function to convert JSON to Template object
   - Basic error handling

3. Create example template `examples/basic-template.json`:
   - Simple template with all section types
   - Include sample variables
   - Include metadata (name, version, description)

4. Create `tests/test_templates/test_parser.py`:
   - Test template loading
   - Test JSON parsing
   - Test error handling for malformed JSON

#### Template Schema Structure

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["metadata", "sections"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["name", "version"],
      "properties": {
        "name": {"type": "string"},
        "version": {"type": "string"},
        "description": {"type": "string"},
        "author": {"type": "string"},
        "created": {"type": "string", "format": "date"}
      }
    },
    "sections": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["type", "content"],
        "properties": {
          "type": {"enum": ["scripture", "reflection", "prayer", "action"]},
          "title": {"type": "string"},
          "content": {"type": "string"},
          "variables": {
            "type": "array",
            "items": {"type": "string"}
          }
        }
      }
    },
    "variables": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "type": {"enum": ["string", "scripture", "theme", "prayer"]},
          "required": {"type": "boolean"},
          "default": {"type": "string"},
          "description": {"type": "string"}
        }
      }
    }
  }
}
```

#### Verification Steps

- [ ] Template schema file exists and is valid JSON Schema
- [ ] Template class correctly represents template structure
- [ ] Template loading function reads JSON files
- [ ] Example template validates against schema
- [ ] Parser tests run and pass
- [ ] Error handling works for invalid JSON

#### Acceptance Criteria

- Template schema defines all required fields
- Template class has properties for metadata and sections
- Loading function returns Template object
- Example template is complete and valid
- At least 5 parser tests passing
- Error messages are clear and actionable

#### Rollback Procedure

**Risk Level**: Low

If issues occur:
1. Revert to CP2: `git checkout CP2`
2. Review schema design
3. Simplify if too complex
4. Re-implement with lessons learned

**Recovery**:
- Schema issues: Review JSON Schema specification, use validator
- Parser issues: Test with simple JSON first, add complexity gradually

---

### CP4: Template Validation System

**Goal**: Implement comprehensive template validation

#### Tasks

1. Create `src/validators/template_validator.py`:
   - `TemplateValidator` class
   - `validate_schema()` - JSON Schema validation
   - `validate_sections()` - Section structure validation
   - `validate_variables()` - Variable consistency checking
   - `validate_references()` - Ensure all variable references exist
   - `generate_validation_report()` - Detailed error reporting

2. Enhance `src/templates/template.py`:
   - Add `validate()` method to Template class
   - Integrate with TemplateValidator
   - Store validation results

3. Create `tests/test_validators/test_template_validator.py`:
   - Test schema validation
   - Test section validation
   - Test variable validation
   - Test validation reporting
   - Test invalid templates (negative tests)

4. Create invalid example templates for testing:
   - `examples/invalid-missing-required.json`
   - `examples/invalid-bad-section-type.json`
   - `examples/invalid-undefined-variable.json`

#### Validation Rules

1. **Schema Validation**:
   - Template conforms to schema.json
   - All required fields present
   - Field types correct

2. **Section Validation**:
   - At least one section present
   - Section types are valid
   - Content is non-empty

3. **Variable Validation**:
   - All referenced variables defined
   - Variable names are unique
   - Required variables have no default
   - Variable types are valid

4. **Reference Validation**:
   - All `{{variable}}` references in content have definitions
   - No circular references
   - Variables used in correct section types

#### Verification Steps

- [ ] TemplateValidator class implemented
- [ ] All validation methods work correctly
- [ ] Validation report is detailed and clear
- [ ] Valid templates pass validation
- [ ] Invalid templates fail with specific errors
- [ ] At least 10 validation tests passing

#### Acceptance Criteria

- Schema validation catches JSON Schema violations
- Section validation identifies structural issues
- Variable validation finds undefined references
- Validation report lists all errors with line numbers
- At least 10 passing tests including negative cases
- Error messages guide users to fix issues

#### Rollback Procedure

**Risk Level**: Low

If issues occur:
1. Revert to CP3: `git checkout CP3`
2. Review validation requirements
3. Prioritize critical validations
4. Implement in stages if complex

**Recovery**:
- Validation too strict: Add configuration for validation levels
- Performance issues: Optimize validation order, cache results

---

### CP5: Variable Substitution and Sample Templates

**Goal**: Implement variable substitution and create production-ready templates

#### Tasks

1. Create `src/generators/substitution.py`:
   - `VariableSubstitution` class
   - `substitute()` - Replace `{{variable}}` with values
   - `validate_required()` - Check required variables provided
   - `apply_defaults()` - Use default values when appropriate
   - Support for nested variables (optional)

2. Create `src/generators/template_engine.py`:
   - `TemplateEngine` class
   - `load_template()` - Load and validate template
   - `render()` - Generate output with substitution
   - `preview()` - Generate without saving

3. Create sample templates:
   - `src/templates/daily-devotional.json` - Standard daily format
   - `src/templates/themed-reflection.json` - Theme-focused format
   - `src/templates/prayer-guide.json` - Prayer-focused format

4. Create `tests/test_generators/test_substitution.py`:
   - Test basic substitution
   - Test required variable checking
   - Test default value application
   - Test error handling for missing variables

5. Create `tests/test_generators/test_template_engine.py`:
   - Test full template rendering
   - Test with all sample templates
   - Test preview mode
   - Test error propagation

6. Create `examples/sample-render.py`:
   - Demonstration script
   - Load template
   - Provide sample variables
   - Render and display output

#### Variable Substitution Format

- **Simple**: `{{variable_name}}`
- **With default**: `{{variable_name|default_value}}`
- **Conditional**: `{{?variable_name}}content{{/variable_name}}` (optional)

#### Verification Steps

- [ ] Variable substitution works correctly
- [ ] Required variables enforced
- [ ] Default values applied appropriately
- [ ] Template engine renders templates
- [ ] All sample templates valid
- [ ] Preview mode works without saving
- [ ] Sample render script executes successfully
- [ ] At least 15 tests passing

#### Acceptance Criteria

- Variable substitution replaces all placeholders
- Required variables throw error if missing
- Default values work when variable not provided
- Template engine generates complete output
- At least 3 sample templates provided
- Sample render script demonstrates full workflow
- At least 15 passing tests
- Documentation explains substitution syntax

#### Rollback Procedure

**Risk Level**: Medium

If issues occur:
1. Revert to CP4: `git checkout CP4`
2. Review substitution approach
3. Consider simpler substitution syntax
4. Re-implement incrementally

**Recovery**:
- Substitution errors: Test with simple cases first, add features gradually
- Template complexity: Start with one template type, expand after validation
- Performance issues: Profile and optimize hot paths

---

## Phase Acceptance Criteria

All of the following must be true to consider Phase 002 complete:

### Schema and Structure
- [x] Template schema defined and valid
- [x] Schema covers all template requirements
- [x] Example templates validate against schema

### Parsing
- [x] Template parser loads JSON files
- [x] Parser creates Template objects correctly
- [x] Error handling for malformed templates

### Validation
- [x] Template validator checks schema compliance
- [x] Validator checks section structure
- [x] Validator checks variable consistency
- [x] Validation reports are detailed and actionable

### Substitution
- [x] Variable substitution works correctly
- [x] Required variables enforced
- [x] Default values applied
- [x] Template engine renders complete output

### Templates
- [x] At least 3 sample templates provided
- [x] All sample templates valid
- [x] Templates cover different use cases

### Testing
- [x] At least 30 tests passing (15 per commit point average)
- [x] Tests cover positive and negative cases
- [x] Test fixtures for common scenarios

### Documentation
- [x] Template schema documented
- [x] Substitution syntax documented
- [x] Sample render script demonstrates usage

## Gatekeeper Checklist

### Human Review Required

- [ ] Template schema meets flexibility requirements
- [ ] Sample templates are realistic and useful
- [ ] Substitution syntax is intuitive
- [ ] Documentation is clear for template authors

### AI Review Recommended

- [ ] Template validation logic is comprehensive
- [ ] Variable substitution handles edge cases
- [ ] Error messages are helpful and specific
- [ ] Test coverage is adequate

### Review Questions

1. Can template authors easily create new templates?
2. Does the schema support anticipated future needs?
3. Are validation errors helpful for debugging?
4. Is the substitution syntax simple enough?
5. Do sample templates demonstrate best practices?

## Common Issues and Solutions

### Issue 1: Template Schema Too Restrictive

**Symptom**: Valid use cases rejected by schema

**Solution**:
- Review schema requirements vs. optional fields
- Add flexibility with `additionalProperties`
- Consider schema versioning for future changes

### Issue 2: Variable Substitution Errors

**Symptom**: Variables not replaced or incorrectly replaced

**Solution**:
1. Verify variable name format (case-sensitive)
2. Check for typos in template vs. variable definitions
3. Use regex to find all `{{...}}` patterns
4. Test with simple examples first

### Issue 3: Validation Too Slow

**Symptom**: Template validation takes too long

**Solution**:
1. Cache validation results
2. Validate only changed sections
3. Move complex validation to async process
4. Profile to identify bottlenecks

### Issue 4: Template Complexity

**Symptom**: Templates becoming too complex to manage

**Solution**:
- Consider template inheritance/composition
- Break complex templates into reusable parts
- Add template helpers or macros
- Simplify schema if over-engineered

## Testing Strategy

### Unit Tests (Phase 002)

- Template parsing
- Schema validation
- Section validation
- Variable validation
- Variable substitution
- Default value application

### Integration Tests (Phase 002)

- End-to-end template loading and rendering
- Multiple templates with same engine
- Error propagation through layers

### Manual Tests (Phase 002)

- [ ] Load each sample template
- [ ] Render with sample variables
- [ ] Intentionally provide invalid input
- [ ] Verify error messages are helpful
- [ ] Test with edge cases (empty values, special characters)

## Success Metrics

- [ ] Template loading time: < 100ms
- [ ] Validation time: < 500ms
- [ ] Substitution time: < 100ms
- [ ] 100% of valid templates pass validation
- [ ] 100% of invalid test templates fail validation
- [ ] At least 30 passing tests

## Dependencies and Prerequisites

### Phase Dependencies
- Phase 001 complete (CP2)
- Configuration system working
- Test framework operational

### Technical Dependencies
- jsonschema library for validation
- Python regex for variable substitution
- JSON parsing capabilities

### Knowledge Requirements
- JSON Schema specification
- Template engine concepts
- Regular expressions

## Next Steps

After Phase 002 completion:

1. Commit all changes: `git commit -m "Complete Phase 002: Template System"`
2. Tag the commit: `git tag CP5`
3. Update iteration log with Phase 002 results
4. Begin Phase 003: Content Library

## Notes and Observations

### Design Decisions

**Decision**: JSON Schema for validation
- **Rationale**: Standard, well-supported, declarative
- **Alternative**: Custom validation logic
- **Trade-off**: Dependency but better maintainability

**Decision**: Simple `{{variable}}` syntax
- **Rationale**: Familiar, easy to parse, minimal escaping issues
- **Alternative**: Jinja2 templates (more powerful but complex)
- **Trade-off**: Simplicity vs. advanced features

**Decision**: Three sample templates
- **Rationale**: Cover different use cases, demonstrate flexibility
- **Alternative**: Single "canonical" template
- **Trade-off**: More to maintain but better examples

### Potential Improvements

- Template inheritance/composition system
- Template preview with live variable editing
- Template library/repository
- Visual template editor (future)

### Related Documentation

- [Project Index](../index.md)
- [PRD](../prd.md)
- [Roadmap](../roadmap.md)
- [Iteration Log](../iteration-log.md)
- [Phase 001](./001-project-scaffold.md)

---

**Phase Status**: Not Started
**Previous Phase**: [001-project-scaffold.md](./001-project-scaffold.md)
**Next Phase**: [003-content-library.md](./003-content-library.md)
