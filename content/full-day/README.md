# Modern DevOps with GitHub

| [← Pets workshop selection][walkthrough-previous] | [Next: Workshop setup →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

[DevOps][devops] is a [portmanteau][portmanteau] of **development** and **operations**. At its core is a desire to bring development practices more inline with operations, and operations practices more inline with development. This fosters better communication and collaboration between teams, breaks down barriers, and gives everyone an investment in ensuring customers are delighted by the software we ship.

This workshop is built to help guide you through some of the most common DevOps tasks on GitHub. You'll explore:

- Managing projects with [GitHub Issues][github-issues]
- Creating a development environment with [GitHub Codespaces][github-codespaces]
- Using [GitHub Copilot][github-copilot] as your AI pair programmer
- Securing the development pipeline with [GitHub Advanced Security][github-security]
- Automating tasks and CI/CD with [GitHub Actions][github-actions]

## Prerequisites

The application for the workshop uses is built primarily with Python (Flask and SQLAlchemy) and Astro (using Tailwind and Svelte). While experience with these frameworks and languages is helpful, you'll be using Copilot to help you understand the project and generate the code. As a result, as long as you are familiar with programming you'll be able to complete the exercises!

## Required resources

To complete this workshop, you will need the following:

- A [GitHub account][github-signup]
- Access to [GitHub Copilot][github-copilot]

## Getting started

Ready to get started? Let's go! The workshop scenario imagines you as a developer volunteering your time for a pet adoption center. You will work through the process of creating a development environment, creating code, enabling security, and automating processes.

0. [Setup your environment][walkthrough-next] for the workshop
1. [Enable Code Scanning][code-scanning] to ensure new code is secure
2. [Create an issue][issues] to document a feature request
3. [Create a codespace][codespaces] to start writing code
4. [Implement testing][testing] to supplement continuous integration
5. [Provide Copilot context][context] to generate quality code suggestions
6. [Add features to your app][code] with GitHub Copilot
7. [Use the GitHub flow][github-flow] to incorporate changes into your codebase
8. [Deploy your application][deployment] to Azure to make your application available to users

## Check out these resources to dive in and learn more
Check out the resources in [**GitHub-Copilot-Resources.md**][GitHub-Copilot-Resources]. 

This resource list has been carefully curated to help you to learn more about GitHub Copilot, how to use it effectively, what is coming in the future and more. There are even YouTube playlists that include the latest videos from the GitHub Developer Relations team and others from GitHub. 

| [← Pets workshop selection][walkthrough-previous] | [Next: Workshop setup →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

[code]: ./6-code.md
[code-scanning]: ./1-code-scanning.md
[codespaces]: ./3-codespaces.md
[context]: ./5-context.md
[deployment]: ./8-deployment.md
[devops]: https://en.wikipedia.org/wiki/DevOps
[github-actions]: https://github.com/features/actions
[github-codespaces]: https://github.com/features/codespaces
[github-copilot]: https://github.com/features/copilot
[github-flow]: ./7-github-flow.md
[github-issues]: https://github.com/features/issues
[github-security]: https://github.com/features/security
[github-signup]: https://github.com/join
[issues]: ./2-issues.md
[portmanteau]: https://www.merriam-webster.com/dictionary/portmanteau
[testing]: ./4-testing.md
[walkthrough-next]: ./0-setup.md
[walkthrough-previous]: ../README.md
[GitHub-Copilot-Resources]: ../GitHub-Copilot-Resources.md
