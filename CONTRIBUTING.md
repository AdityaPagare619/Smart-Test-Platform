# Contributing to CR-V4 Smart Exams Platform

## Git Workflow

### Branch Naming
- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/[name]` - New features (e.g., `feature/layer-3-burnout`)
- `fix/[name]` - Bug fixes (e.g., `fix/bayes-edge-case`)
- `phase-[n]` - Phase milestones (e.g., `phase-2-core-layers`)

### Commit Messages
Use conventional commits:
```
type(scope): description

[optional body]
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `test` - Tests
- `refactor` - Code refactoring
- `chore` - Maintenance

**Examples:**
```
feat(layer-1): add knowledge graph traversal
fix(bayes): handle edge case for 0.5 prior mastery
docs(readme): update installation instructions
test(bayes): add performance benchmarks
```

### Pull Request Process
1. Create feature branch from `develop`
2. Make changes and commit
3. Push branch and create PR
4. Wait for CI checks to pass
5. Request review
6. Merge after approval

## Development Setup

```bash
# Clone
git clone https://github.com/AdityaPagare619/Smart-Test-Platform.git
cd Smart-Test-Platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r cr-v4-backend/requirements.txt

# Run tests
cd cr-v4-backend
pytest tests/ -v
```

## Phase Milestones

- **Phase 1** ✅ Foundation (Database, Bayesian Algorithm)
- **Phase 2** 🔄 Core Layers (1-10)
- **Phase 3** ⏳ Simulation Testing
- **Phase 4** ⏳ Integration
- **Phase 5** ⏳ Launch Prep
