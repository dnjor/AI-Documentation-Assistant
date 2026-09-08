# AI Documentation Assistant

An AI-powered assistant that analyzes GitHub repository changes and
helps developers understand what documentation should be created or
updated based on recent commits and changed files.

------------------------------------------------------------------------

# Overview

Developers often update their code but forget to update the related
documentation.

This project automates part of the documentation workflow by analyzing
GitHub repository changes and generating documentation recommendations
using Gemini AI.

The user provides a GitHub repository URL, and the system:

1.  Validates and extracts repository information.
2.  Retrieves repository data using GitHub REST API.
3.  Analyzes README content, recent commits, and changed files.
4.  Sends relevant repository information to Gemini AI.
5.  Generates documentation recommendations and README updates.
6.  Returns the analysis result to the user.

------------------------------------------------------------------------

# Features

## Authentication

-   User registration and login.
-   Authentication handled by Firebase Authentication.
-   Backend functions validate authenticated users before processing
    requests.

## GitHub Repository Analysis

The system analyzes GitHub repositories using GitHub REST API.

Supported analysis:

-   Repository information.
-   README content.
-   Recent commits.
-   Changed files.
-   File status:
    -   Added.
    -   Modified.
    -   Deleted.

The system analyzes recent changes to determine whether documentation
needs to be updated.

## AI Documentation Review

Using Gemini API, the system generates:

-   Documentation update recommendations.
-   Missing README sections.
-   Configuration documentation suggestions.
-   Environment variable documentation.
-   Setup instructions.
-   Explanations of recent code changes.

The AI compares:

-   Current README documentation.
-   Recent commits.
-   Changed files.

and identifies differences between the documented behavior and the
actual codebase.

------------------------------------------------------------------------

# System Architecture

``` text
Android Application (Kotlin)

            |

Firebase Authentication

            |

Firebase Cloud Function
        (Python)

            |

    -----------------

    |               |

GitHub API      Gemini API

            |

       Firestore
```

------------------------------------------------------------------------

# Backend Setup & Environment Configuration

## Prerequisites

-   Python 3.11+
-   Firebase CLI

## Environment Variables

Create an environment file:

``` bash
cp backend/functions/.env.example backend/functions/.env
```

Configure:

``` env
GEMINI_API_KEY=your_gemini_api_key
GITHUB_TOKEN=your_github_token
```

## Backend Installation

Navigate to:

``` bash
cd backend/functions
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Run Firebase emulator:

``` bash
firebase emulators:start
```

------------------------------------------------------------------------

# Current Status

🚧 Currently under development.

Completed:

✅ Firebase backend setup.\
✅ GitHub API integration.\
✅ Gemini API integration.\
✅ Repository analysis workflow.\
✅ AI documentation review prototype.

Next steps:

-   Improve AI recommendations.
-   Optimize repository context handling.
-   Improve user experience.

### Note

- The latest README updates were generated automatically by the AI documentation assistant review logic based on repository changes, commits, and implementation details.