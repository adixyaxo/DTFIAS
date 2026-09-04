# Antarctic Digital Twin - Architecture Analysis

This document outlines the architectural decisions and structural layout for the Antarctic Digital Twin (DTFIAS) project.

## Core Philosophy

The project follows a **Domain-Driven Design (DDD)** inspired layered architecture with a clear separation between the presentation layer (FastAPI), the core business logic (Engine), and the external concerns (Infrastructure).

### 1. Presentation Layer (`app/`)
The `app/` directory contains the FastAPI application. Its sole responsibility is HTTP lifecycle management, routing, request validation (via Pydantic), and rendering HTMX-driven HTML templates using Jinja2.

- **`main.py`**: The single FastAPI instance.
- **`routers/`**: Organized by portal (`maitri`, `bharati`, `hq`). Each portal has its own dependencies (e.g., RBAC).
- **`templates/`**: Jinja2 templates, structured to match the routers, utilizing HTMX for dynamic frontend interactions without a heavy SPA framework.

### 2. Core Engine Layer (`engine/`)
The `engine/` directory represents the heart of the application. It contains pure Python code, free from web framework dependencies (no FastAPI here).

- **`domain/`**: Pydantic models representing the core entities (Station, Energy, Environment, Users).
- **`services/`**: Application services. This is where business use-cases are orchestrated. It is split into `core/` (shared logic) and `portals/` (specific logic for each frontend portal).
- **`interfaces/`**: Abstract base classes (protocols) for repositories and other external dependencies, ensuring the engine depends on abstractions, not implementations.

### 3. Infrastructure Layer (`infrastructure/`)
The `infrastructure/` directory contains all implementations for interacting with the outside world.

- **`database/`**: MySQL specific implementations of the repository interfaces defined in the engine.
- **`security/`**: Concrete implementations for authentication, authorization (RBAC), and auditing.

## Key Benefits
- **Testability**: The engine can be tested entirely in isolation without a database or HTTP server.
- **Portability**: If the web framework (FastAPI) needs to be replaced, the engine remains untouched.
- **Security**: Portal-specific routing and services ensure strict isolation (e.g., Maitri operators cannot access HQ commands).
