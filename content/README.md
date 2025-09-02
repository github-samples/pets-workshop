# Modern DevOps with GitHub

| [Next: Workshop setup →][next] |
|:-----------------------------------:|

[DevOps][devops] is a [portmanteau][portmanteau] of **development** and **operations**. At its core is a desire to bring development practices more inline with operations, and operations practices more inline with development. This fosters better communication and collaboration between teams, breaks down barriers, and gives everyone an investment in ensuring customers are delighted by the software we ship.

This workshop is built to help guide you through some of the most common DevOps tasks on GitHub. You will:

- manage a project with [GitHub Issues][github-issues].
- create a development environment with [GitHub Codespaces][github-codespaces].
- use [GitHub Copilot][github-copilot] as your AI pair programmer.
- secure the development pipeline with [GitHub Advanced Security][github-security].
- automate tasks and CI/CD with [GitHub Actions][github-actions].

## Prerequisites

The application for the workshop uses is built primarily with Python (Flask and SQLAlchemy) and Astro (using Tailwind and Svelte). Experience with these frameworks and languages is not required for the course, as the primary focus will be around GitHub features.

## Required resources

To complete this workshop, you will need the following:

- A [GitHub account][github-signup]
- Access to [GitHub Copilot][github-copilot]

> [!IMPORTANT]
> This workshop is designed to utilize the free version of GitHub Copilot, the [free compute for Codespaces][codespaces-free], and the functionality provided by GHAS and Actions to public repos.

## Getting started

Ready to get started? Let's go! The workshop scenario imagines you as a developer volunteering your time for a pet adoption center. You will work through the process of creating a development environment, creating code, enabling security, and automating processes.

0. [Setup your environment][next] for the workshop
1. [Enable Code Scanning][code-scanning] to ensure new code is secure
2. [Create an issue][issues] to document a feature request
3. [Create a codespace][codespaces] to start writing code
4. [Implement continuous integration][testing] to supplement development
5. [Add features to your app][code] with GitHub Copilot
6. [Use the GitHub flow][github-flow] to incorporate changes into your codebase
7. [Deploy your application][deployment] to Azure to make your application available to users

| [Next: Workshop setup →][next] |
|:------------------------------------------:|

[next]: ./0-setup.md
[code]: ./5-code.md
[code-scanning]: ./1-code-scanning.md
[codespaces]: ./3-codespaces.md
[deployment]: ./7-deployment.md
[github-flow]: ./6-github-flow.md
[issues]: ./2-issues.md
[testing]: ./4-continuous-integration.md

[codespaces-free]: https://docs.github.com/en/billing/concepts/product-billing/github-codespaces#free-and-billed-use-by-personal-accounts
[devops]: https://en.wikipedia.org/wiki/DevOps
[github-actions]: https://github.com/features/actions
[github-codespaces]: https://github.com/features/codespaces
[github-copilot]: https://github.com/features/copilot
[github-issues]: https://github.com/features/issues
[github-security]: https://github.com/features/security
[github-signup]: https://github.com/join
[portmanteau]: https://www.merriam-webster.com/dictionary/portmanteau
