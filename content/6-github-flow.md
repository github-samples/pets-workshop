# GitHub flow

| [← Add new functionality][walkthrough-previous] | [Next: Deploy the application →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

The [GitHub flow][github-flow] is a lightweight, [branch-based][about-branches] workflow. It's designed to allow for free testing and exploration of ideas and novel approaches which are then reviewed and, if accepted, brought into the codebase. At a high level, the GitHub flow follows this pattern:

1. Create a branch
1. Make the desired changes
1. Create a [pull request][about-prs]
1. Review changes, gather feedback and make updates
1. Review results of automated operations such as testing for continuous integration
1. If changes are approved, merge into codebase

The GitHub flow is designed to work as a cycle, where contributors continuously explore, test, review, and build upon their work and the work of others.

> [!NOTE]
> One key philosophy for GitHub flow is not every pull request needs to be merged. Sometimes exploration is the goal, the feature isn't one which is desired by the greater team, or wholesale changes need to be made necessitating starting over. This is part of the process, and allows for free experimentation.

## Scenario

With the code changes created in the [prior exercise][code-exercise], it's time to walk through the GitHub flow to create a pull request and incorporate the updates into the codebase. While the changes have already been made (meaning we are slightly out of order from the "traditional" flow), you can still perform the steps to explore.

## Creating a branch

A [branch][about-branches] is a copy of the code stored in the same repository. By using branches to test updates you have a safe space to explore while keeping all code in the same repository.

There are different ways to create a branch when using [GitHub Codespaces][github-codespaces]. You can utilize the command-line to run [git](https://git-scm.com/docs/git-branch) commands. You can use the Source Control pane in your codespace to get the support of the UI for creating your branch. In our example we're going to use the command-line to create the branch.

1. Return to your codespace, or reopen it by navigating to your repository and selecting **Code** > **Codespaces** and the name of your codespace.
2. Open a **terminal window** by pressing <kbd>Ctl</kbd> + <kbd>`</kbd>.
3. In the terminal window, enter the following command to create and switch to a new branch named `add-filter`:

    ```bash
    git checkout -b add-filter
    ```

4. Stage all code to be committed to the new branch by entering the following command in the terminal window:

    ```bash
    git add .
    ```

5. Let Copilot generate a commit message by selecting the **Quick fix** icon (represented by sparkles) and **Generate Commit Message**.

    ![Screenshot of the quick fix menu with Generate Commit Message selected](./images/7-generate-commit-message.png).

6. Press <kbd>enter</kbd> to run the command.
7. Finally, push the new branch to the repository by entering the following command in the terminal window:

    ```bash
    git push -u origin add-filter
    ```

## Create the pull request to suggest updates

A [pull request][about-prs] is a request to pull or incorporate new code into the existing codebase. When a pull request is made it's customary to have other team members review the code and make comments, and for [CI/CD][cicd-resources] processes to run. Once everything is completed and the code is in a stage where everyone has signed-off, it's then merged into the codebase.

Pull requests can be made through the source control pane in the codespace, the repository's website, or through the command-line using the [GitHub CLI][github-cli]. In our example we're going to create the pull request in the CLI, then navigate to the website to see the pull request and the actions running, and merge the code into the codebase.

1. Return to your codespace.
1. Find the number for the [issue you created earlier][issues-exercise] titled **Add component to display hours** by entering the following command in the terminal window:

    ```bash
    gh issue list
    ```

1. Create a pull request with the title **Add hours component** and body **Resolves #\<ISSUE_NUMBER\>**, replacing **\<ISSUE_NUMBER\>** with the issue number you obtained in the previous step by entering the following command in the terminal window:

    ```bash
    gh pr create -t "Add hours component" -b "Resolves #<ISSUE_NUMBER>"
    ```

## Explore and merge the pull request

When the pull request is created, you will see a link appear to the page for the pull request. From there you can add comments, see any workflows running, and decide to close or merge the pull request. You can also see any workflows associated with the pull request run.

In our scenario, we created an automated workflow for front-end tests for our application, which runs whenever a push or pull request is made to `main`. We also enabled [code scanning][security-exercise], which was set to run on the same triggers. We've just created a pull request, which will cause both of those workflows to run!

Let's explore the pull request and watch the workflows run. We'll ensure the tests now run successfully and, assuming they do, merge the pull request.

1. Follow the link displayed in the terminal window by using <kbd>Ctl</kbd> - **Click** (or <kbd>Cmd</kbd> - **Click** on a Mac).
1. In the page displayed, note the workflow running the [end-to-end tests created earlier][testing-exercise] and [code scanning][security-exercise].
1. When the workflows complete successfully, select **Merge pull request** to merge your changes into the **main** branch.

Congratulations! You've now used the GitHub flow to suggest changes, perform a review, and merge those into your codebase.

## Summary and next steps

The GitHub flow is a workflow for managing changes and incorporating new features into a codebase. GitHub flow gives you the freedom to explore and experiment, while ensuring all code follows a validation process before being merged. Let's get our [application deployed][walkthrough-next].

## Resources

- [GitHub flow][github-flow]
- [GitHub Skills: Review pull requests][skills-review-prs]
- [GitHub Skills: Release based workflow][skills-release-workflow]

| [← Add new functionality][walkthrough-previous] | [Next: Deploy the application →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

[about-branches]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches
[about-prs]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
[cicd-resources]: https://resources.github.com/ci-cd/
[code-exercise]: ./6-code.md
[github-codespaces]: https://github.com/features/codespaces
[github-cli]: https://cli.github.com/
[github-flow]: https://docs.github.com/en/get-started/quickstart/github-flow
[issues-exercise]: ./2-issues.md
[security-exercise]: ./1-code-scanning.md
[skills-review-prs]: https://github.com/skills/review-pull-requests
[skills-release-workflow]: https://github.com/skills/release-based-workflow
[testing-exercise]: ./4-testing.md
[walkthrough-previous]: 6-code.md
[walkthrough-next]: 8-deployment.md
