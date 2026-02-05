# Devotional Generator - Project Index

## Overview

The Devotional Generator is an automated system for creating personalized daily devotional content. This project demonstrates a complete workflow from template design to content generation, validation, and distribution.

## Project Status

- **Current Phase**: Planning
- **Last Updated**: 2026-02-05
- **Status**: Not Started

## Navigation

### Core Documents

- **[Product Requirements (PRD)](./prd.md)** - Complete requirements specification
- **[Roadmap](./roadmap.md)** - Five-phase milestone plan with commit points
- **[Iteration Log](./iteration-log.md)** - Progress tracking and decision history

### Phase Documentation

1. **[Phase 001: Project Scaffold](./phases/001-project-scaffold.md)** - Initial setup and structure
2. **[Phase 002: Template System](./phases/002-template-system.md)** - Core template engine
3. **[Phase 003: Content Library](./phases/003-content-library.md)** - Structured content management
4. **[Phase 004: Validation & Preview](./phases/004-validation-preview.md)** - Quality assurance
5. **[Phase 005: Export & Distribution](./phases/005-export-distribution.md)** - Multi-format output

## Quick Links

### For Implementers

- Start with [PRD](./prd.md) to understand requirements
- Review [Phase 001](./phases/001-project-scaffold.md) for initial setup
- Check [Iteration Log](./iteration-log.md) for current status

### For Reviewers

- Review [Roadmap](./roadmap.md) for milestone overview
- Check commit point gates in each phase document
- Verify acceptance criteria completion

### For Stakeholders

- See [PRD](./prd.md) for business value and success metrics
- Review [Roadmap](./roadmap.md) for timeline and deliverables

## Key Principles

### Plan-First Methodology

All work follows the automated-builder plan-first approach:

1. **Plan** - Define scope and approach
2. **Review** - Validate before implementation
3. **Implement** - Execute incrementally
4. **Verify** - Confirm results

### Quality Gates

Each phase includes:

- **Commit Points** - Incremental checkpoints with rollback capability
- **Acceptance Criteria** - Clear pass/fail validation
- **Gatekeeper Checklist** - Human/AI review requirements

### Human Oversight

Human review required at:

- Phase transitions
- Before merging to main branch
- When scope changes occur
- Security or data integrity decisions

## Project Metrics

### Success Criteria

- Generate devotionals in under 2 minutes
- 95%+ template validation pass rate
- Support 3+ output formats (Markdown, HTML, PDF)
- Zero manual intervention for standard generation

### Technical Targets

- Modular, extensible architecture
- Comprehensive test coverage
- Clear documentation
- Rollback capability at all commit points

## Repository Structure

```
devotional-generator/
├── src/
│   ├── templates/           # Template definitions
│   ├── content/             # Content library
│   ├── generators/          # Generation engines
│   ├── validators/          # Quality checks
│   └── exporters/           # Output formatters
├── tests/                   # Test suite
├── config/                  # Configuration files
├── output/                  # Generated devotionals
└── docs/                    # Additional documentation
```

## Getting Started

1. Read the [PRD](./prd.md) for complete context
2. Review [Phase 001](./phases/001-project-scaffold.md) for setup instructions
3. Follow commit points sequentially
4. Verify acceptance criteria at each gate

## Support and Questions

For questions or clarifications:

1. Check the [Iteration Log](./iteration-log.md) for similar issues
2. Review phase-specific documentation
3. Consult the automated-builder CLAUDE.md for general guidelines

---

**Document Version**: 1.0
**Last Updated**: 2026-02-05
**Maintained By**: Automated Builder Project
