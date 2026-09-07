# AI Documentation Assistant

An AI-powered assistant that analyzes GitHub repository changes and
helps developers understand what documentation should be created or
updated based on recent commits and changed files

## Overview

Developers often update their code but forget to update the related
documentation. This project aims to automate part of the documentation
workflow by analyzing recent GitHub changes and generating documentation
recommendations using Gemini AI.

The user provides a GitHub repository URL, and the system:

1.  Retrieves the latest commits.
2.  Analyzes changed files and code changes (diffs).
3.  Sends relevant information to Gemini AI.
4.  Generates documentation recommendations.
5.  Returns the result to the user.

------------------------------------------------------------------------

# Features

## Authentication

-   User registration and login.
-   Authentication handled by Firebase Authentication.
-   Backend functions validate authenticated users before processing
    requests.

## GitHub Repository Analysis

-   Accept GitHub repository URL.
-   Retrieve recent commits using GitHub REST API.
-   Analyze:
    -   Commit messages.
    -   Changed files.
    -   File status (added, modified, deleted).
    -   Code changes/diffs.

## AI Documentation Generation

Using Gemini API, the system generates:

-   Documentation updates required.
-   Missing README sections.
-   Suggested documentation improvements.
-   Explanations of recent changes.

## AI Conversation

-   Users can ask follow-up questions about the generated analysis.
-   The current analysis session can be continued during the active
    session.

------------------------------------------------------------------------

# System Architecture

``` text
Android Application (Kotlin)
            |
            |
   Firebase Authentication
            |
            |
 Firebase Cloud Function
       (JavaScript)
            |
     -----------------
     |               |
 GitHub API      Gemini API
            |
            |
       Firestore
```

------------------------------------------------------------------------

# Development Plan

## Phase 1 - Setup

-   Create Android project.
-   Configure Firebase.
-   Implement authentication.
-   Setup Firestore.

## Phase 2 - Backend Integration

-   Create Firebase Cloud Functions.
-   Connect GitHub API.
-   Connect Gemini API.
-   Implement authentication validation.

## Phase 3 - Repository Analysis

-   Fetch latest commits.
-   Retrieve changed files.
-   Process code differences.
-   Prepare AI prompts.

## Phase 4 - AI Processing

-   Generate documentation suggestions.
-   Display results.
-   Support follow-up questions.


------------------------------------------------------------------------

# Status

🚧 Currently under development.
