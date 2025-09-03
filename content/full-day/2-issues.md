# Project management with GitHub Issues

| [← Securing the development pipeline][walkthrough-previous] | [Next: Cloud-based development with GitHub Codespaces →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

"URL or it didn't happen" is a common mantra at GitHub, which is used to highlight the importance of documenting the development process. Feature requests should have a history; who made the request, what was the rationale, who was involved in the process, what decisions were made, why were they made, was the feature implemented, how was it implemented... All of this information helps provide context to both drive future decisions and avoid repeating old mistakes.

GitHub provides various features to enable collaboration and project management, including [GitHub Discussions][discussions], [wikis][wikis], [pull requests][about-prs] and [GitHub Issues][issues]. Each of these can help your organization drive the creation process. We're going to focus on GitHub Issues, which is the foundation of project management on GitHub. Issues can also be linked to [milestones](https://docs.github.com/issues/using-labels-and-milestones-to-track-work/about-milestones) and [Projects](https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects), helping organize them into a broad roadmap.

At their core, issues document some form of an action. They can be a request for a feature, a bug report, or another operation taken by the team. There's no prescribed methodology for using GitHub Issues, allowing your team to determine the best way to manage and drive your projects. A common flow teams will implement on issues is:

1. File an issue to request a new feature or file a bug report.
1. Discuss the issue, and determine the correct people and mechanism to resolve the request.
1. Create a pull request with a proposed implementation of the request.
1. Further discuss and review the pull request.
1. Once everyone is satisfied and has signed off, merge the pull request and close the issue.

Issues can sometimes seem too big, or often we experience 'scope-creep' in a task. Issues can be broken down into [sub-issues](https://docs.github.com/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues) that allow smaller issues to be linked together, especially when working on dependencies. For example, you might have a feature request that includes a list of subtasks that make the task a bit too large for your sprint or for the work required. Using sub-issues allows you to cleanly define all dependent tasks into more manageable items of work.

To further track work in an issue, the right-hand sidebar of any issue is where you can manage metadata and organizational details. You can assign the issue to yourself or various team members, apply labels for categorization (i.e "bug", "enhancement", "documentation"), allowing you to link your issue to a milestone, connect it to a GitHub Project board, or mark it as part of an epic/initiative. If there are linked discussions or pull requests you can track them from this panel. This side panel makes it easier to triage issues and keep them aligned with the project's workflow.

GitHub Issues also come with some very handy shortcuts and productivity hacks:

- Typing `#` in a comment or description lets you reference another issue or pull request by number.
- Use Markdown to format text, add checklists (- [ ]), code snippets, or images.
- Pressing `g` then `i` quickly takes you to the Issues tab from anywhere in a repository.
- Typing `@username` mentions someone, notifying them directly.
- Filter issues in the search bar with queries like `is:open label:bug assignee:@me` to quickly find relevant ones.

## Scenario

The shelter wants to begin pushing new features to the website. They want to start by displaying the hours for the current day on the landing page. There's also a need to make updates to help support development and DevOps for both current and future updates. You want to track these updates to document the work being done. You'll do this by creating issues in the repository.

## Creating issues to manage feature requests

Our project needs two main updates. We want to make the updates to support development for our project, and add a new component to the website to display the shelter's hours. Let's create the issues for each of these. In the next few exercises we'll begin making the appropriate updates to our project to resolve these requests.

1. Return to the repository you created at the beginning of this workshop.
1. Select the **Issues** tab.
1. Select **New issue**.
2. If prompted for type, select **Blank issue**.
3. Select **Create more** at the bottom of the page to streamline the creation process.
4. Create new issues by adding the information indicated in the table below, selecting **Submit new issue** after creating each one:

    | Title                   | Description                                                                    |
    | ----------------------- | ------------------------------------------------------------------------------ |
    | Define codespace        | Create the necessary definitions for the codespace to enable cloud development |
    | Implement testing       | Create a workflow to automate testing for continuous integration               |
    | Add filters to dog list | Add the code to allow users to filter for dogs by breed and availability       |

> [!TIP]
> You can also save an issue by pressing <kbd>Ctl</kbd> - <kbd>Enter</kbd> (or <kbd>Cmd</kbd> - <kbd>Return</kbd> on a Mac) in the title or description fields.

You've now defined all the issues for the workshop! You'll use these issues to help guide your progress through the workshop.

## Summary and next steps
GitHub Issues are the core to project management on GitHub. Their flexibility allows your organization to determine the best course of action to support your development lifecycle's methodology. With your issues created, it's time to turn your attention to the first big change to the project, [defining a codespace][walkthrough-next].

## Resources
- [GitHub Issues][issues-docs]
- [Communicate using markdown][skills-markdown]
- [GitHub Projects][projects-docs]

| [← Securing the development pipeline][walkthrough-previous] | [Next: Cloud-based development with GitHub Codespaces →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

[discussions]: https://github.com/features/discussions
[wikis]: https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis
[about-prs]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
[issues]: https://github.com/features/issues
[issues-docs]: https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues
[projects-docs]: https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/quickstart-for-projects
[skills-markdown]: https://github.com/skills/communicate-using-markdown
[walkthrough-next]: 3-codespaces.md
[walkthrough-previous]: 1-code-scanning.md