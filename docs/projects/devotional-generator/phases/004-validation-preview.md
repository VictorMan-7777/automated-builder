# Phase 004: Validation & Preview

## Phase Information

- **Phase**: 004
- **Name**: Validation & Preview
- **Status**: Not Started
- **Estimated Duration**: 1-2 hours
- **Dependencies**: Phase 003 complete

## Overview

Phase 004 implements comprehensive quality assurance through pre-generation validation, post-generation validation, and preview capabilities. This ensures generated devotionals meet quality standards before export or distribution.

## Objectives

1. Implement pre-generation validation (template + content)
2. Build post-generation validation (output quality)
3. Create preview system (view before export)
4. Develop validation reporting
5. Add quality metrics and checks
6. Create validation configuration

## Commit Points

### CP8: Pre-Generation Validation

**Goal**: Validate inputs before devotional generation

#### Tasks

1. Create `src/validators/generation_validator.py`:
   - `GenerationValidator` class
   - `validate_template()` - Ensure template is valid and loaded
   - `validate_content_availability()` - Check required content exists
   - `validate_variable_mapping()` - Verify all variables can be satisfied
   - `validate_content_compatibility()` - Check content matches template requirements
   - `generate_pre_generation_report()` - Detailed validation report

2. Create `src/validators/validation_rules.py`:
   - Define validation rule classes
   - `Rule` base class
   - Specific rules: `RequiredContentRule`, `VariableMappingRule`, `ContentTypeRule`
   - Rule engine to execute rules

3. Create `config/validation-rules.yaml`:
   - Configurable validation rules
   - Rule severity levels (error, warning, info)
   - Enable/disable specific rules
   - Custom rule parameters

4. Enhance `src/generators/template_engine.py`:
   - Integrate pre-generation validation
   - Option to skip validation (for testing)
   - Report validation results before generation

5. Create `tests/test_validators/test_generation_validator.py`:
   - Test template validation
   - Test content availability checking
   - Test variable mapping validation
   - Test with invalid combinations (negative tests)
   - Test validation configuration

6. Create `tests/test_validators/test_validation_rules.py`:
   - Test each validation rule
   - Test rule engine execution
   - Test rule severity handling

#### Pre-Generation Validation Checks

1. **Template Validation**:
   - Template loaded successfully
   - Template schema valid
   - Template sections defined
   - Variables declared

2. **Content Availability**:
   - All required content types available
   - Sufficient content for selection
   - Content IDs exist if specified

3. **Variable Mapping**:
   - All template variables have content source
   - Required variables have values (no defaults)
   - Content types match variable types

4. **Content Compatibility**:
   - Content themes match template themes
   - Scripture references valid
   - Content relationships intact

5. **Configuration Validation**:
   - Output paths writable
   - Export formats supported
   - Required settings present

#### Verification Steps

- [ ] GenerationValidator class implemented
- [ ] All pre-generation checks work correctly
- [ ] Validation rules configurable
- [ ] Validation report is detailed and actionable
- [ ] Invalid combinations detected and reported
- [ ] At least 15 tests passing

#### Acceptance Criteria

- Pre-generation validation catches input issues
- Validation rules are configurable
- Validation report clearly lists all issues
- Severity levels (error/warning/info) work correctly
- Template engine integrates validation
- At least 15 passing tests
- Configuration file allows customization
- Error messages guide users to fix issues

#### Rollback Procedure

**Risk Level**: Low

If issues occur:
1. Revert to CP7: `git checkout CP7`
2. Review validation requirements
3. Prioritize critical validations
4. Re-implement incrementally

**Recovery**:
- Validation too strict: Adjust severity levels in config
- Performance issues: Cache validation results, optimize checks
- False positives: Review rule logic, add test cases

---

### CP9: Post-Generation Validation and Preview

**Goal**: Validate output quality and enable preview before export

#### Tasks

1. Create `src/validators/output_validator.py`:
   - `OutputValidator` class
   - `validate_completeness()` - All sections populated
   - `validate_formatting()` - No broken placeholders or formatting issues
   - `validate_quality()` - Quality metrics (word count, readability)
   - `validate_references()` - Scripture references formatted correctly
   - `generate_post_generation_report()` - Output quality report

2. Create `src/generators/preview.py`:
   - `PreviewGenerator` class
   - `generate_preview()` - Create preview without saving
   - `format_for_display()` - Format output for terminal/console
   - `highlight_issues()` - Highlight validation issues in preview
   - Support for different preview formats (plain text, markdown, HTML)

3. Create `src/validators/quality_metrics.py`:
   - `QualityMetrics` class
   - Calculate word count per section
   - Calculate readability score (Flesch-Kincaid or similar)
   - Check for common issues (repeated words, poor formatting)
   - Generate quality report

4. Enhance `src/generators/template_engine.py`:
   - Add `preview()` method
   - Integrate post-generation validation
   - Option to validate before saving
   - Return validation results with output

5. Create `tests/test_validators/test_output_validator.py`:
   - Test completeness checking
   - Test formatting validation
   - Test quality metrics
   - Test with low-quality output (negative tests)

6. Create `tests/test_generators/test_preview.py`:
   - Test preview generation
   - Test preview formatting
   - Test issue highlighting
   - Test different preview formats

7. Create `tests/test_validators/test_quality_metrics.py`:
   - Test word count calculation
   - Test readability scoring
   - Test quality thresholds

8. Create `examples/preview-devotional.py`:
   - Demonstration script
   - Load template and content
   - Generate preview
   - Display validation results
   - Show formatted output

#### Post-Generation Validation Checks

1. **Completeness**:
   - All sections have content
   - No empty sections
   - All variables replaced
   - No placeholder remnants ({{...}})

2. **Formatting**:
   - Proper paragraph breaks
   - Correct heading levels
   - No formatting errors
   - Links and references formatted correctly

3. **Quality Metrics**:
   - Word count per section (min/max)
   - Overall word count (target range)
   - Readability score (target level)
   - No repeated content

4. **Content Integrity**:
   - Scripture references match source
   - No truncated content
   - Proper punctuation and grammar (basic checks)
   - Consistent formatting throughout

5. **Metadata**:
   - Date/time stamp present
   - Theme/tags included
   - Attribution present
   - Version information included

#### Quality Metrics

```yaml
quality_thresholds:
  word_count:
    min: 300
    max: 1500
    target: 800
  section_word_count:
    scripture: {min: 20, max: 200}
    reflection: {min: 100, max: 500}
    prayer: {min: 50, max: 300}
    action: {min: 20, max: 100}
  readability:
    min_grade_level: 6
    max_grade_level: 12
    target_grade_level: 8
```

#### Preview Formats

1. **Plain Text**: Console-friendly, no formatting
2. **Markdown**: Show markdown syntax
3. **Formatted**: ANSI colors for terminal display
4. **HTML**: Browser-friendly preview

#### Verification Steps

- [ ] OutputValidator validates generated devotionals
- [ ] Quality metrics calculate correctly
- [ ] Preview generates without saving
- [ ] Preview highlights validation issues
- [ ] Multiple preview formats supported
- [ ] Post-generation validation catches quality issues
- [ ] At least 20 tests passing
- [ ] Preview example runs successfully

#### Acceptance Criteria

- Post-generation validation checks output quality
- Quality metrics provide actionable feedback
- Preview displays formatted output
- Preview highlights issues clearly
- Multiple preview formats available
- Validation integrates with template engine
- At least 20 passing tests
- Preview example demonstrates full workflow
- Documentation explains quality thresholds

#### Rollback Procedure

**Risk Level**: Low

If issues occur:
1. Revert to CP8: `git checkout CP8`
2. Review validation and preview requirements
3. Simplify quality metrics if too complex
4. Re-implement incrementally

**Recovery**:
- Quality metrics issues: Use simpler calculations, defer advanced metrics
- Preview formatting issues: Start with plain text, add formatting gradually
- Performance issues: Cache calculations, lazy load preview

---

## Phase Acceptance Criteria

All of the following must be true to consider Phase 004 complete:

### Pre-Generation Validation
- [x] Template validation works
- [x] Content availability checking works
- [x] Variable mapping validation works
- [x] Validation rules configurable

### Post-Generation Validation
- [x] Completeness checking works
- [x] Formatting validation works
- [x] Quality metrics calculate correctly
- [x] Validation catches quality issues

### Preview System
- [x] Preview generates without saving
- [x] Preview displays formatted output
- [x] Preview highlights issues
- [x] Multiple preview formats supported

### Validation Reporting
- [x] Pre-generation report is detailed
- [x] Post-generation report is detailed
- [x] Quality metrics report is actionable
- [x] Reports use severity levels appropriately

### Integration
- [x] Validation integrates with template engine
- [x] Preview integrates with generation workflow
- [x] Validation can be configured/customized

### Testing
- [x] At least 35 tests passing (total)
- [x] Tests cover positive and negative cases
- [x] Tests cover all validation checks

### Documentation
- [x] Validation rules documented
- [x] Quality metrics explained
- [x] Preview usage documented
- [x] Configuration options explained

## Gatekeeper Checklist

### Human Review Required

- [ ] Validation rules are appropriate and not too strict
- [ ] Quality metrics align with content goals
- [ ] Preview format is useful and readable
- [ ] Error messages are helpful

### AI Review Recommended

- [ ] Validation logic is comprehensive
- [ ] Quality metrics calculations are correct
- [ ] Preview handles edge cases
- [ ] Performance is acceptable

### Review Questions

1. Does validation catch real quality issues?
2. Are quality metrics meaningful and actionable?
3. Is the preview helpful for reviewing content?
4. Can users easily fix validation issues?
5. Are validation rules customizable enough?

## Common Issues and Solutions

### Issue 1: Validation Too Strict

**Symptom**: Valid devotionals fail validation

**Solution**:
1. Review validation rules and thresholds
2. Adjust severity levels (error → warning)
3. Make rules configurable
4. Add override capability for specific cases

### Issue 2: Quality Metrics Misleading

**Symptom**: Metrics don't reflect actual quality

**Solution**:
1. Review metric calculations
2. Adjust thresholds based on real content
3. Consider multiple metrics together
4. Add context-specific metrics

### Issue 3: Preview Formatting Issues

**Symptom**: Preview is hard to read or displays incorrectly

**Solution**:
1. Test with various terminal types
2. Use safe formatting (ASCII fallback)
3. Provide multiple preview formats
4. Allow format selection

### Issue 4: Validation Performance

**Symptom**: Validation takes too long

**Solution**:
1. Cache validation results
2. Validate only changed content
3. Parallelize independent checks
4. Profile and optimize bottlenecks

## Testing Strategy

### Unit Tests (Phase 004)

- Pre-generation validation rules
- Post-generation validation rules
- Quality metrics calculations
- Preview formatting
- Validation configuration

### Integration Tests (Phase 004)

- End-to-end validation workflow
- Preview with validation results
- Template engine with validation
- Multiple validation scenarios

### Manual Tests (Phase 004)

- [ ] Generate devotional with validation
- [ ] Intentionally create invalid inputs
- [ ] Preview in different formats
- [ ] Verify quality metrics are accurate
- [ ] Test with edge cases (very short, very long)

## Success Metrics

- [ ] Pre-generation validation time: < 500ms
- [ ] Post-generation validation time: < 1 second
- [ ] Preview generation time: < 500ms
- [ ] 100% of quality issues detected
- [ ] Zero false positives for valid content
- [ ] At least 35 passing tests

## Dependencies and Prerequisites

### Phase Dependencies
- Phase 003 complete (CP7)
- Content library operational
- Template engine functional

### Technical Dependencies
- Text analysis libraries (for readability)
- Terminal formatting (ANSI colors)
- Quality metric algorithms

### Knowledge Requirements
- Quality assurance principles
- Text analysis techniques
- Validation patterns

## Next Steps

After Phase 004 completion:

1. Commit all changes: `git commit -m "Complete Phase 004: Validation & Preview"`
2. Tag the commit: `git tag CP9`
3. Update iteration log with Phase 004 results
4. Begin Phase 005: Export & Distribution

## Notes and Observations

### Design Decisions

**Decision**: Separate pre and post-generation validation
- **Rationale**: Catch issues early, but also verify output quality
- **Alternative**: Single validation step after generation
- **Trade-off**: More validation steps but better error prevention

**Decision**: Configurable validation rules
- **Rationale**: Different use cases have different requirements
- **Alternative**: Hard-coded validation
- **Trade-off**: Complexity vs. flexibility

**Decision**: Multiple preview formats
- **Rationale**: Users have different preferences and contexts
- **Alternative**: Single preview format
- **Trade-off**: More code but better user experience

**Decision**: Quality metrics with thresholds
- **Rationale**: Objective quality assessment
- **Alternative**: Manual review only
- **Trade-off**: Risk of false positives but consistent standards

### Potential Improvements

- Visual preview (web-based)
- Interactive preview with editing
- A/B testing for quality metrics
- Machine learning for quality prediction
- Spell checking and grammar checking
- Plagiarism detection
- Accessibility checking (readability for different audiences)

### Related Documentation

- [Project Index](../index.md)
- [PRD](../prd.md)
- [Roadmap](../roadmap.md)
- [Iteration Log](../iteration-log.md)
- [Phase 003](./003-content-library.md)

---

**Phase Status**: Not Started
**Previous Phase**: [003-content-library.md](./003-content-library.md)
**Next Phase**: [005-export-distribution.md](./005-export-distribution.md)
