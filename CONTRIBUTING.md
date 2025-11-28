# Contributing to TransiScope

Thank you for your interest in contributing to TransiScope! We welcome contributions from the community to help make this tool more useful for biological research.

## Ways to Contribute

There are many ways you can contribute to TransiScope:

- **Report bugs**: If you encounter any issues, please open an issue on our [GitHub Issues page](https://github.com/InnovationLine/TransiScope/issues)
- **Suggest features**: Have an idea for a new feature? We'd love to hear it! Open an issue with the "enhancement" label
- **Improve documentation**: Help us make the documentation clearer and more comprehensive
- **Submit code**: Fix bugs, implement new features, or improve existing code
- **Share datasets**: If you have example microscopy datasets that could be useful for testing and validation

## Getting Started

### Setting up the Development Environment

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/TransiScope.git
   cd TransiScope
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**:
   ```bash
   pip install -e .
   ```

4. **Install development dependencies** (if applicable):
   ```bash
   pip install pytest pytest-cov black flake8
   ```

### Running TransiScope from Source

To launch the GUI directly from source:
```bash
python -m TransiScope.gui_manager
```

## Code Contribution Guidelines

### Before You Start

1. **Check existing issues**: Look for existing issues or discussions related to your proposed change
2. **Open an issue first**: For significant changes, please open an issue to discuss your proposal before starting work
3. **One feature per PR**: Keep pull requests focused on a single feature or bug fix

### Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clear, documented code
   - Follow the existing code style (PEP 8 for Python)
   - Add docstrings to functions and classes
   - Update documentation as needed

3. **Test your changes**:
   - Ensure the GUI launches without errors
   - Test with sample data
   - If possible, add unit tests for new functions

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Brief description of your changes"
   ```
   
   Use clear, descriptive commit messages. Follow this format:
   - `feat: Add new ROI drawing mode`
   - `fix: Resolve crash when loading corrupted AVI files`
   - `docs: Update installation instructions`
   - `refactor: Improve event detection algorithm efficiency`

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**:
   - Go to the TransiScope repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Provide a clear description of your changes
   - Reference any related issues (e.g., "Fixes #123")

### Code Style

- Follow [PEP 8](https://pep8.org/) style guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and modular
- Maximum line length: 100 characters (flexible for readability)

### Documentation

- Add docstrings to all public functions and classes
- Update the README if you add new features
- Update the UserGuide.md if user-facing behavior changes
- Consider adding examples to the tutorial notebook

## Reporting Bugs

When reporting bugs, please include:

1. **Description**: A clear description of the bug
2. **Steps to reproduce**: Detailed steps to recreate the issue
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **System information**:
   - Operating system and version
   - Python version
   - TransiScope version
   - Relevant package versions (napari, numpy, etc.)
6. **Sample data**: If possible, provide a minimal example data file that reproduces the issue
7. **Error messages**: Full error messages and tracebacks

## Suggesting Features

When suggesting new features:

1. **Use case**: Describe the biological problem or workflow you're trying to solve
2. **Proposed solution**: How you envision the feature working
3. **Alternatives**: Any alternative approaches you've considered
4. **Additional context**: Screenshots, mockups, or examples from other tools

## Questions and Discussions

- **Usage questions**: Open an issue with the "question" label
- **General discussions**: Use GitHub Discussions (if enabled) or open an issue with the "discussion" label
- **Scientific collaborations**: Contact the maintainers directly via email

## Code of Conduct

### Our Standards

We are committed to providing a welcoming and inclusive environment. We expect all contributors to:

- Be respectful and considerate of others
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members
- Accept constructive criticism gracefully

### Unacceptable Behavior

- Harassment, discrimination, or intimidation of any kind
- Trolling, insulting comments, or personal attacks
- Publishing others' private information without permission
- Other conduct that could reasonably be considered inappropriate

## Attribution

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/) code of conduct.

## License

By contributing to TransiScope, you agree that your contributions will be licensed under the MIT License, the same license as the project.

## Recognition

Contributors will be acknowledged in:
- The project's README (for significant contributions)
- Release notes
- The CITATION.cff file (for major contributors)

## Getting Help

If you need help with contributing:

- Check the [README](README.md) and [User Guide](UserGuide.md)
- Look at existing code for examples
- Open an issue with your question
- Contact the maintainers: 
  - Rinki Dasgupta: rinkidsgpt@gmail.com
  - Kaushik Das: kaushik.k.das@gmail.com

Thank you for contributing to TransiScope! Your efforts help make biological image analysis more accessible to researchers worldwide.

