# AI Documentation Assistant

An AI-powered assistant that analyzes GitHub repository changes and
helps developers understand what documentation should be created or
updated based on recent commits and changed files.

## Overview

This project automates documentation review by analyzing GitHub
repositories and generating recommendations using Gemini AI.

The system: 1. Validates repository information. 2. Retrieves GitHub
data. 3. Analyzes README, commits, and changed files. 4. Sends context
to Gemini AI. 5. Generates documentation recommendations.

## Features

### GitHub Repository Analysis

-   Repository information
-   README content
-   Recent commits
-   Changed files
-   File status (Added, Modified, Deleted)

### AI Documentation Review

Generates: - Documentation update recommendations - Missing README
sections - Setup instructions - Configuration suggestions - Explanations
of code changes

### Interactive AI Chat & Input Parsing

Supports: - GitHub URL detection - Repository analysis requests -
Documentation questions - Follow-up explanations

## System Architecture

``` text
Android Application (Kotlin + Jetpack Compose)
                 |
        Firebase Cloud Function
                 |
        -----------------
        |               |
    GitHub API      Gemini API
```

## Project Structure

``` text
AI-Documentation-Assistant
|
├── frontend/
|   └── Android Kotlin Jetpack Compose app
|
├── backend/
|   └── Firebase Cloud Functions (Python)
|       ├── services/
|       ├── tests/
|       └── main.py
|
└── README.md
```

## Backend Setup

### Prerequisites

-   Python 3.11+
-   Firebase CLI

### Environment Variables

Create:

``` bash
cp backend/functions/.env.example backend/functions/.env
```

Configure:

``` env
GEMINI_API_KEY=your_gemini_api_key
GITHUB_TOKEN=your_github_token
```

### Install Dependencies

``` bash
cd backend/functions
pip install -r requirements.txt
```

### Run Firebase Emulator

``` bash
firebase emulators:start
```

## Frontend Setup (Android)

### Prerequisites

-   Android Studio Hedgehog or newer
-   JDK 17+
-   Android SDK API 34+

### Running

1.  Open Android Studio.
2.  Open the frontend directory.
3.  Sync Gradle.
4.  Run on emulator or Android device.

## Running Backend Tests

``` bash
cd backend/functions
pytest
```

## Current Status

Completed: - Firebase backend setup - GitHub API integration - Gemini
API integration - Repository analysis workflow - AI documentation review
prototype - Android frontend prototype

# Screenshots

## Mobile Application

### Home Screen
<img src="docs/screenshots/home_screen.png" width="300"/>

### Repository Analysis
<img src="docs/screenshots/analysis_screen.png" width="300"/>

### AI Documentation Result
<img src="docs/screenshots/result_screen.png" width="300"/>

## Note

README improvements can be generated automatically by the AI
Documentation Assistant based on repository changes and implementation
details.
