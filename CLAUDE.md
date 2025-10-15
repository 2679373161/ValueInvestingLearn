# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **ValueInvestingLearn** repository - a structured development environment for building value investing learning tools and applications. The repository is currently in its initial setup phase with a focus on organized AI-assisted development workflows.

## Development Workflow

This repository uses a structured AI development framework for feature implementation:

### AI Development Framework

The `/ai-dev-tasks/` directory contains templates for managing feature development:

- **[create-prd.md](ai-dev-tasks/create-prd.md)**: Guidelines for creating Product Requirements Documents
- **[generate-tasks.md](ai-dev-tasks/generate-tasks.md)**: Process for generating task lists from PRDs
- **[process-task-list.md](ai-dev-tasks/process-task-list.md)**: Protocol for implementing tasks systematically

### Feature Development Process

1. **Create PRD**: Use `/ai-dev-tasks/create-prd.md` to generate detailed product requirements
2. **Generate Tasks**: Use `/ai-dev-tasks/generate-tasks.md` to create implementation task lists
3. **Implement Tasks**: Follow the structured workflow in `/ai-dev-tasks/process-task-list.md`

### Task Implementation Protocol

- Work on **one sub-task at a time**
- Get user approval before starting each sub-task
- Mark sub-tasks as completed immediately after finishing
- Run tests before marking parent tasks as completed
- Commit changes with descriptive messages following conventional commit format

## Project Structure

- **`/ai-dev-tasks/`**: AI development workflow templates
- **`/tasks/`**: Future location for PRDs and task lists (to be created)
- **`.gitignore`**: Python-focused ignore patterns
- **`LICENSE`**: Apache 2.0 open source license

## Technology Stack

Based on the `.gitignore` file, this project will likely use:
- **Python** (primary language)
- **Jupyter Notebooks** for analysis
- **Pytest** for testing
- **Ruff** for linting
- **Poetry/PDM/UV** for dependency management (patterns included in .gitignore)

## Development Guidelines

### When Starting New Features

1. Always begin with the AI development framework in `/ai-dev-tasks/`
2. Create PRDs before implementation
3. Generate detailed task lists
4. Follow the systematic implementation protocol

### Code Organization

- Keep the `/tasks/` directory organized with sequentially numbered PRDs
- Follow Python best practices and naming conventions
- Include comprehensive testing for all new features

### Git Workflow

- Use conventional commit messages
- Follow the task completion protocol for commits
- Maintain clean commit history with descriptive messages

## Current State

This repository is in its initial setup phase. The AI development framework is established, but no application code has been implemented yet. Future development should follow the structured workflow outlined in the `/ai-dev-tasks/` directory.