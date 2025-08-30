# GPAF Development Guide

This guide provides information for developers working on GPAF.

## Development Setup

### Prerequisites

- Python 3.12+
- Docker
- Git
- IDE of choice

### Environment Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/frdel/gpaf.git
   cd gpaf
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Set required variables
   - Configure API keys

## Development Workflow

### Code Structure

- `/python` - Core Python code
- `/webui` - Frontend code
- `/docs` - Documentation
- `/tests` - Test files

### Testing

1. **Unit Tests**
   ```bash
   python -m pytest tests/
   ```

2. **Integration Tests**
   ```bash
   python -m pytest tests/integration/
   ```

3. **Code Quality**
   ```bash
   flake8 python/
   black python/
   ```

### Documentation

- Update relevant docs
- Add code comments
- Write docstrings
- Update README

## Contributing

### Pull Requests

1. **Create Branch**
   - Use feature branch
   - Follow naming convention
   - Keep focused

2. **Submit PR**
   - Add description
   - Include tests
   - Update docs
   - Request review

### Code Review

- Follow style guide
- Add tests
- Update docs
- Address feedback

## Resources

- [Documentation](https://github.com/frdel/gpaf/docs)
- [Discord Community](https://discord.gg/Z2tun2N3)
- [Skool](https://www.skool.com/gpaf)
- [Issue Tracker](https://github.com/frdel/gpaf/issues)

For development questions, join our community. 