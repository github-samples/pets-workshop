# Continuous integration and testing

| [← Cloud-based development with GitHub Codespaces][walkthrough-previous] | [Next: Helping GitHub Copilot understand context →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

Chances are you've heard the abbreviation CI/CD, which stands for continuous integration and continuous delivery (or sometimes continuous deployment). CI is centered on incorporating new code into the existing codebase, and typically includes running tests and performing builds. CD focuses on the next logical step, taking the now validated code and generating the necessary outputs to be pushed to the cloud or other destinations. This is probably the most focused upon component of DevOps.

CI/CD fosters a culture of rapid development, collaboration, and continuous improvement, allowing organizations to deliver software updates and new features more reliably and quickly. It ensures consistency, and allows developers to focus on writing code rather than performing manual processes.

[GitHub Actions][github-actions] is an automation platform upon which you can build your CI/CD process. It can also be used to automate other tasks, such as resizing images and validating machine learning models.

## Scenario

A set of unit tests exist for the Python server for the project. You want to ensure those tests are run whenever someone makes a [pull request][about-prs] (PR). To meet this requirement, you'll need to define a workflow for the project, and ensure there is a [trigger][workflow-triggers] for pull requests to main. Fortunately, [GitHub Copilot][copilot] can aid you in creating the necessary YML file!

## Exploring the test

Let's take a look at the tests defined for the project.

> [!NOTE]
> There are only a few tests defined for this project. Many projects will have hundreds or thousands of tests to ensure reliability.

1. Return to your codespace, or reopen it by navigating to your repository and selecting **Code** > **Codespaces** and the name of your codespace.
2. In **Explorer**, navigate to **server** and open **test_app.py**.
3. Open GitHub Copilot Chat and ask for an explanation of the file.

> [!NOTE]
> Consider using the following GitHub Copilot tips to gain an understanding of the tests:
>
> - `/explain` is a [slash command][copilot-slash-commands] to quickly ask for an explanation
> - Highlight specific sections of the file to focus on areas you may have questions about

## Understanding workflows

To ensure the tests run whenever a PR is made you'll define a workflow for the project. Workflows can perform numerous tasks, such as checking for security vulnerabilities, deploying projects, or (in our case) running unit tests. They're central to any CI/CD.

Creating a YML file can be a little tricky. Fortunately, GitHub Copilot can help streamline the process! Before we work with Copilot to create the file, let's explore some core sections of a workflow:

- `name`: Provides a name for the workflow, which will display in the logs.
- `on`: Defines what will trigger the workflow to run. Some common triggers include `pull_request` (when a PR is made), `merge` (when code is merged into a branch), and `workflow_dispatch` (manual run).
- `jobs`: Defines a series of jobs for this workflow. Each job is considered a unit of work and has a name.
    - **name**: Name and container for the job.
    - `runs-on`: Where the operations for the job will be performed.
    - `steps`: The operations to be performed.

## Create the workflow file

Now that we have an overview of the structure of a workflow, let's ask Copilot to generate it for us!

1. Create a new folder under **.github** named **workflows**.
2. Create a new file named **server-test.yml** and ensure the file is open.
3. If prompted to install the **GitHub Actions** extension, select **Install**.
4. Open GitHub Copilot Chat.
5. Add the test file **test_app.py** to the context by using the `#` in the Chat dialog box and beginning to type **test_app.py**, and pressing <kbd>enter</kbd> when it's highlighted.
6. Prompt Copilot to create a GitHub Action workflow to run the tests. Use natural language to describe the workflow you're looking to create (to run the tests defined in test_app.py), and that you want it to run on merge (for when new code is pushed), when a PR is made, and on demand.

  > [!IMPORTANT]
  > A prescriptive prompt isn't provided as part of the exercise is to become comfortable interacting with GitHub Copilot.

6. Add the generated code to the new file by hovering over the suggested code and selecting the **Insert at cursor** button. The generated code should resemble the following:

```yml
name: Server Tests

on:
  push:
    branches: [ main ]
    paths:
      - 'server/**'
  pull_request:
    branches: [ main ]
    paths:
      - 'server/**'

jobs:
  server-test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f server/requirements.txt ]; then pip install -r server/requirements.txt; fi
        pip install pytest
        
    - name: Run tests
      working-directory: ./server
      run: |
        python -m pytest test_app.py -v
```

> [!IMPORTANT]
> Note, the file generated may differ from the example above. Because GitHub Copilot uses generative AI, there results will be probabilistic rather than deterministic.

> [!TIP]
> If you want to learn more about the workflow you just created, ask GitHub Copilot!

## Push the workflow to the repository

With the workflow created, let's push it to the repository. Typically you would create a PR for any new code (which this is). To streamline the process, we're going to push straight to main as we'll be exploring pull requests and the [GitHub flow][github-flow] in a [later exercise][github-flow-exercise]. You'll start by obtaining the number of the [issue you created earlier][issues-exercise], creating a commit for the new code, then pushing it to main.

> [!NOTE]
> All commands are entered using the terminal window in the codespace.

1. Use the open terminal window in your codespace, or open it (if necessary) by pressing <kbd>Ctl</kbd> + <kbd>`</kbd>.
1. List all issues for the repository by entering the following command in the terminal window:

    ```bash
    gh issue list
    ```

1. Note the issue number for the one titled **Implement testing**.
1. Stage all files by entering the following command in the terminal window:

    ```bash
    git add .
    ```

1. Commit all changes with a message by entering the following command in the terminal window, replacing **<ISSUE_NUMBER>** with the number for the **Implement testing** issue:

    ```bash
    git commit -m "Resolves #<ISSUE_NUMBER>"
    ```

1. Push all changes to the repository by entering the following command in the terminal window:

    ```bash
    git push
    ```

Congratulations! You've now implemented testing, a core component of continuous integration (CI)!

## Seeing the workflow in action

Pushing the workflow definition to the repository counts as a push to `main`, meaning the workflow will be triggered. You can see the workflow in action by navigating to the **Actions** tab in your repository.

1. Return to your repository.
2. Select the **Actions** tab.
3. Select **Server test** on the left side.
4. Select the workflow run on the right side with a message of **Resolves #<ISSUE_NUMBER>**, matching the commit message you used.
5. Explore the workflow run by selecting the job name 

You've now seen a workflow, and explore the details of a run!

## Summary and next steps

Congratulations! You've implemented automated testing, a standard part of continuous integration, which is critical to successful DevOps. Automating these processes ensures consistency and reduces the workload required for developers and administrators. You have created a workflow to run tests on any new code for your codebase. Let's explore [context with GitHub Copilot chat][walkthrough-next].

### Resources
- [GitHub Actions][github-actions]
- [GitHub Actions Marketplace][actions-marketplace]
- [About continuous integration][about-ci]
- [GitHub Skills: Test with Actions][skills-test-actions]

| [← Cloud-based development with GitHub Codespaces][walkthrough-previous] | [Next: Helping GitHub Copilot understand context →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

[about-ci]: https://docs.github.com/en/actions/automating-builds-and-tests/about-continuous-integration
[about-prs]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
[actions-marketplace]: https://github.com/marketplace?type=actions
[workflow-triggers]: https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows
[copilot]: https://gh.io/copilot
[copilot-slash-commands]: https://docs.github.com/en/copilot/using-github-copilot/copilot-chat/github-copilot-chat-cheat-sheet
[github-actions]: https://github.com/features/actions
[github-flow]: https://docs.github.com/en/get-started/quickstart/github-flow
[github-flow-exercise]: ./7-github-flow.md
[issues-exercise]: ./2-issues.md
[skills-test-actions]: https://github.com/skills/test-with-actions
[walkthrough-previous]: 3-codespaces.md
[walkthrough-next]: 5-context.md
