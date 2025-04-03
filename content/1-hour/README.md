# Getting started with GitHub Copilot

| [← Pets workshop selection][walkthrough-previous] | [Next: Workshop setup →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

Built to be your AI pair programmer, [GitHub Copilot][copilot] helps you generate code and focus on what's important. Through the use of code completion you can create code from comments, and functions from just a signature. With Copilot chat you can ask questions about your codebase, create new files and update existing ones, and even perform operations which update files across your entire codebase.

As with any tool, there are a set of skills which need to be acquired, which is the purpose of this (roughly) one hour workshop. You'll explore the most common workloads available to you by exploring and updating an existing application to add functionality.

## Prerequisites

The application for the workshop uses is built primarily with Python (Flask and SQLAlchemy) and Astro (using Tailwind and Svelte). While experience with these frameworks and languages is helpful, you'll be using Copilot to help you understand the project and generate the code. As a result, as long as you are familiar with programming you'll be able to complete the exercises!

> [!NOTE]
> When in doubt, you can always highlight a block of code you're unfamiliar with and ask GitHub Copilot chat for an explanation!

## Required resources

To complete this workshop, you will need the following:

- A [GitHub account][github-account].
- Access to [GitHub Copilot][copilot] (which is available for free for individuals!)

## Required local installation

You will also need the following available and installed locally:

### Code editor

- [Visual Studio Code][vscode-link].
- [Copilot extension installed in your IDE][copilot-extension].

### Local services

- A recent [Node.js runtime][nodejs-link].
- A recent version of [Python][python-link].
  - For Windows, you can install [Python via the Windows store](https://apps.microsoft.com/detail/9pjpw5ldxlz5?hl=en-US&gl=US).
- The [git CLI][git-link].
- A shell capable of running BASH commands.

> [!NOTE]
> Linux and macOS are able to run BASH commands without additional configuration. For Windows, you will need either [Windows Subsystem for Linux (WS)][windows-subsystem-linux] or the BASH shell available via [git][git-link].

## Getting started

Ready to get started? Let's go! The workshop scenario imagines you as a developer volunteering your time for a pet adoption center. You've been asked to add a filter to the website to allow people to limit their search results by breed and adoption status. You'll work over the next 5 exercises to perform the tasks!

0. [Clone the repository and start the app][walkthrough-next] for the workshop.
1. [Add an endpoint to the server][stage-1] to list all breeds.
2. [Explore the project][stage-2] to get a better understanding of what needs to be done.
3. [Create custom instructions][stage-3] to ensure Copilot chat has additional context.
4. [Add the new feature][stage-4] to the website, and ensure it works!

## Check out these resources to dive in and learn more
Check out the resources in [**GitHub-Copilot-Resources.md**][GitHub-Copilot-Resources]. 

This resource list has been carefully curated to help you to learn more about GitHub Copilot, how to use it effectively, what is coming in the future and more. There are even YouTube playlists that include the latest videos from the GitHub Developer Relations team and others from GitHub. 

| [← Pets workshop selection][walkthrough-previous] | [Next: Workshop setup →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

[copilot]: https://github.com/features/copilot
[copilot-extension]: https://docs.github.com/en/copilot/managing-copilot/configure-personal-settings/installing-the-github-copilot-extension-in-your-environment
[git-link]: https://git-scm.com/
[github-account]: https://github.com/join
[nodejs-link]: https://nodejs.org/en
[python-link]: https://www.python.org/
[stage-1]: ./1-add-endpoint.md
[stage-2]: ./2-explore-project.md
[stage-3]: ./3-copilot-instructions.md
[stage-4]: ./4-add-feature.md
[walkthrough-previous]: ../README.md
[walkthrough-next]: ./0-setup.md
[windows-python-link]: https://apps.microsoft.com/detail/9pjpw5ldxlz5
[windows-subsystem-linux]: https://learn.microsoft.com/en-us/windows/wsl/about
[vscode-link]: https://code.visualstudio.com/
[GitHub-Copilot-Resources]: ../GitHub-Copilot-Resources.md
