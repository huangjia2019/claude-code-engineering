# API Documentation Pipeline

This project uses a 3-stage pipeline to generate and validate API documentation.

## Pipeline Stages

When the user asks to run the documentation pipeline, execute these stages **in order**:

### Stage 1: Route Scanning
Use the `route-scanner` agent to scan the source directory.
Pass the source directory path as the task.
Collect the route manifest (JSON) from its output.

### Stage 2: Documentation Generation
Use the `doc-writer` agent to generate documentation.
Pass the route manifest from Stage 1 as input context.
Collect the documentation manifest from its output.

### Stage 3: Quality Validation
Use the `quality-checker` agent to validate the generated docs.
Pass the documentation manifest from Stage 2 as input context.
Report the quality verdict to the user.

## Important

- Each stage must complete before the next begins
- Pass the output of each stage as input to the next
- If Stage 3 reports NEEDS_REVISION, show the issues to the user
