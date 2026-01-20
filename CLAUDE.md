# CLAUDE.md - AI Assistant Guide for Study-Research Repository

> Last Updated: 2026-01-20
> Repository: Study-Research
> Purpose: Research materials, study notes, and knowledge management

## Overview

This repository serves as a structured knowledge base for research, study materials, and learning resources. It's designed to support both human learning and AI-assisted research workflows.

## Repository Structure

This repository follows a modular organization pattern:

```
Study-Research/
├── research/           # Research papers, literature reviews, and analysis
│   ├── papers/        # Collected research papers and references
│   ├── notes/         # Research notes and summaries
│   └── reviews/       # Literature reviews and critical analysis
├── studies/           # Active study materials and learning resources
│   ├── topics/        # Subject-specific study materials
│   ├── exercises/     # Practice problems and solutions
│   └── projects/      # Hands-on learning projects
├── notes/             # General notes and observations
│   ├── daily/         # Daily notes and logs
│   ├── meetings/      # Meeting notes and discussions
│   └── ideas/         # Ideas and brainstorming
├── resources/         # Reference materials and external resources
│   ├── links/         # Curated links and bookmarks
│   ├── datasets/      # Data files and datasets
│   └── tools/         # Scripts and utilities
├── docs/              # Documentation and guides
│   └── guides/        # How-to guides and tutorials
└── archive/           # Completed or deprecated materials
```

## Development Workflows

### Research Workflow

1. **Literature Collection**
   - Add papers to `research/papers/` with standardized naming: `YYYY-MM-Author-Title.pdf`
   - Create corresponding notes in `research/notes/` with same base name
   - Tag papers with relevant topics and keywords

2. **Note-Taking**
   - Use markdown format for all notes
   - Include metadata headers (date, author, tags, related topics)
   - Cross-reference related materials using relative links
   - Use consistent heading hierarchy (H1 for title, H2 for sections, etc.)

3. **Review Process**
   - Synthesize findings in `research/reviews/`
   - Include citations and references
   - Update index files to maintain discoverability

### Study Workflow

1. **Topic Organization**
   - Create dedicated folders in `studies/topics/` for each subject
   - Include README.md with learning objectives and resources
   - Track progress and completions

2. **Exercise Management**
   - Document problems clearly with context
   - Provide solutions with explanations
   - Include references to source materials

3. **Project Development**
   - Use descriptive project names
   - Include project README with goals, setup, and learnings
   - Document challenges and solutions

## File Naming Conventions

### General Rules
- Use kebab-case for files: `my-research-notes.md`
- Use YYYY-MM-DD prefix for dated content: `2026-01-20-study-session.md`
- Use descriptive, searchable names
- Avoid spaces and special characters except hyphens and underscores

### Specific Formats
- Research papers: `YYYY-MM-Author-ShortTitle.pdf`
- Meeting notes: `YYYY-MM-DD-meeting-topic.md`
- Study notes: `topic-subtopic-notes.md`
- Scripts/tools: `snake_case.py` or `kebab-case.sh`

## Markdown Conventions

### Document Structure
```markdown
# Title

> Metadata: Date, Author, Tags, Status

## Overview
Brief summary of the document

## Main Content
Organized in logical sections

## References
Links and citations

## Related
Cross-references to related materials
```

### Metadata Format
```markdown
---
Date: 2026-01-20
Author: [Name or "AI-Assisted"]
Tags: [tag1, tag2, tag3]
Status: [Draft|In Progress|Complete|Archived]
Related: [links to related documents]
---
```

### Linking Conventions
- Use relative paths: `[Related Note](../notes/related-topic.md)`
- Link to specific sections: `[Section](#section-name)`
- External links: Include access date in footnote

## AI Assistant Guidelines

### When Adding Content

1. **Always preserve existing structure**
   - Don't reorganize without explicit request
   - Follow established naming conventions
   - Maintain consistent formatting

2. **Enhance discoverability**
   - Update or create index files when adding new content
   - Add appropriate metadata and tags
   - Create cross-references where relevant

3. **Document decisions**
   - Explain significant additions or changes
   - Note sources and reasoning
   - Flag areas needing human review

### Research Assistance

1. **Literature Analysis**
   - Provide accurate summaries and citations
   - Identify key contributions and limitations
   - Suggest related work and research directions

2. **Note Synthesis**
   - Consolidate information from multiple sources
   - Highlight connections and contradictions
   - Maintain academic integrity and proper attribution

3. **Knowledge Organization**
   - Suggest taxonomies and categorization schemes
   - Identify gaps and areas for deeper exploration
   - Create visual maps and relationship diagrams when helpful

### Study Support

1. **Content Creation**
   - Generate clear, accurate explanations
   - Provide multiple examples and perspectives
   - Include practice problems with solutions

2. **Progress Tracking**
   - Help maintain learning logs
   - Suggest review schedules and milestones
   - Identify areas needing reinforcement

3. **Resource Curation**
   - Recommend high-quality learning materials
   - Verify and validate external resources
   - Organize resources by difficulty and topic

## Quality Standards

### Content Quality
- **Accuracy**: Verify facts and cite sources
- **Clarity**: Write in clear, accessible language
- **Completeness**: Provide sufficient context and detail
- **Currency**: Note date sensitivity and update frequency

### Code Quality (if applicable)
- Document all scripts with purpose, usage, and dependencies
- Include error handling and input validation
- Use version control best practices
- Add tests for critical functionality

### Documentation Quality
- Keep documentation up-to-date with changes
- Use examples liberally
- Provide both quick-start and detailed guides
- Include troubleshooting sections

## Git Workflow

### Branching Strategy
- `main`: Stable, reviewed content
- `claude/*`: AI-assisted development branches
- `draft/*`: Work-in-progress content
- `archive/*`: Historical preservation branches

### Commit Messages
Format: `<type>: <description>`

Types:
- `add`: New content or files
- `update`: Modifications to existing content
- `fix`: Corrections and error fixes
- `refactor`: Reorganization without content changes
- `docs`: Documentation updates
- `archive`: Moving content to archive

Examples:
- `add: research notes on machine learning fundamentals`
- `update: expand literature review with recent papers`
- `fix: correct citation in quantum computing notes`

### Commit Practices
- Make atomic commits (one logical change per commit)
- Write descriptive commit messages
- Reference related issues or topics when relevant
- Don't commit large binary files without purpose

## Search and Discovery

### Tagging System
Use consistent tags across documents:
- **Subject areas**: `#mathematics`, `#computer-science`, `#physics`
- **Content types**: `#tutorial`, `#reference`, `#exercise`, `#review`
- **Status**: `#draft`, `#complete`, `#needs-review`
- **Difficulty**: `#beginner`, `#intermediate`, `#advanced`

### Index Files
Maintain index files in major directories:
- `INDEX.md`: List of contents with brief descriptions
- Update indexes when adding/removing content
- Include last-updated date
- Use tables for structured listings

## Security and Privacy

### Sensitive Information
- Never commit credentials, API keys, or passwords
- Use `.gitignore` for sensitive local files
- Anonymize personal data in shared materials
- Mark confidential content clearly

### Citation and Attribution
- Always attribute sources properly
- Respect copyright and licensing
- Use proper academic citation formats
- Note when content is AI-generated or AI-assisted

## Maintenance

### Regular Tasks
- Review and update outdated content monthly
- Archive completed or superseded materials
- Verify external links quarterly
- Consolidate and organize growing directories

### Quality Checks
- Spell-check and grammar review
- Verify code examples and commands
- Test links and references
- Ensure consistent formatting

## Special Conventions

### Version Tracking
For evolving research or study materials:
```markdown
## Version History
- v1.0 (2026-01-20): Initial draft
- v1.1 (2026-01-25): Added examples and clarifications
- v2.0 (2026-02-01): Major revision based on new findings
```

### TODO Tracking
Use consistent TODO format:
```markdown
## TODO
- [ ] Complete literature review section
- [ ] Add code examples for algorithm
- [ ] Verify statistical calculations
- [x] Create initial outline
```

### Review Markers
Mark sections needing attention:
- `[VERIFY]`: Needs fact-checking
- `[EXPAND]`: Needs more detail
- `[REVIEW]`: Needs human review
- `[CITATION NEEDED]`: Missing reference

## AI Interaction Patterns

### When Asked to Research
1. Search existing repository first for relevant materials
2. Synthesize findings from multiple sources
3. Create new notes following conventions
4. Update indexes and cross-references
5. Provide summary with next steps

### When Asked to Study
1. Assess current understanding from existing notes
2. Identify knowledge gaps
3. Create or suggest study materials
4. Generate practice problems
5. Track progress and suggest review

### When Asked to Organize
1. Analyze current structure
2. Propose reorganization plan
3. Get confirmation before major changes
4. Execute changes systematically
5. Update all references and indexes

## Getting Started

### For New Topics
1. Create directory structure in appropriate area
2. Add README.md with overview and objectives
3. Create initial notes or materials
4. Update parent index
5. Add to tags/search system

### For New Research
1. Add source materials to `research/papers/`
2. Create notes template in `research/notes/`
3. Extract key points and insights
4. Link related materials
5. Update research index

### For New Study Materials
1. Determine topic and create folder
2. Add learning objectives
3. Collect or create resources
4. Design exercises or projects
5. Set up progress tracking

## Tools and Automation

### Recommended Scripts
- `create-note.sh`: Template-based note creation
- `update-index.py`: Automatic index generation
- `check-links.sh`: Verify internal and external links
- `tag-stats.py`: Analyze tag usage and coverage

### Integration Suggestions
- Use Obsidian, Notion, or similar for visualization
- Set up automated backups
- Consider CI/CD for link checking and validation
- Use pre-commit hooks for formatting

## Questions and Improvements

This guide evolves with the repository. When uncertain:
1. Check existing patterns in the repository
2. Ask for clarification before major decisions
3. Document new patterns as they emerge
4. Suggest improvements to this guide

---

**Note**: This CLAUDE.md file itself should be updated as the repository evolves and new conventions are established. Always keep it synchronized with actual repository practices.
