# Coding with GitHub Copilot

| [← Continuous integration and testing][previous] | [Next: GitHub flow →][next] |
|:-----------------------------------|------------------------------------------:|

To truly experience the newly created workflow in action, and eventually the GitHub flow (which we'll see in the next exercise) we're going to add a small feature to our website. You'll do this by asking [GitHub Copilot][github-copilot] to generate the required code - and tests.

> [!IMPORTANT]
> The focus of this workshop is on DevOps with GitHub. If you'd like to explore more about GitHub Copilot in workshop form, you can see [Agents in SDLC][agents-in-sdlc], which is also available on [GitHub-samples][github-samples].

## Scenario

The website currently lists just the name and breed of the dog on the landing page. Users would like to see at a glance the adoption status so they don't get their hopes up only to discover a dog isn't available. You'll utilize Copilot to add the feature, as well as generate and run the tests to confirm the updates.

## Overview of this exercise

To streamline the creation of both the feature and required infrastructure you'll utilize GitHub Copilot agent mode to generate the code and tests.

## GitHub Copilot agent mode

In the [prior exercise][previous], you utilized **ask mode** in GitHub Copilot. Ask mode is focused on "single-turn" operations, where you ask a question, receive an answer, and then repeat the flow as needed. Ask mode is great for generating individual files, learning about your project, and generic code-related questions.

[**Agent mode**][agent-mode] allows Copilot to act like a peer programmer, both generating code suggestions and performing tasks on your behalf. Agent mode will explore your project, build an approach of how to resolve a problem, generate the code, perform supporting operations like running tests, and even self-heal should it find any problems.

> [!IMPORTANT]
> Before Copilot agent mode runs any external commands it will ask for confirmation. This allows you to ensure it's doing the right thing, cancelling any incorrect operations.

By using agent mode, we'll be able to both create the code and tests, but have Copilot run the tests and correct any mistakes it might find.

## Create the filter and tests

Let's ask Copilot to generate the code to add the feature and tests!

1. Return to your codespace, or reopen it by navigating to your repository and selecting **Code** > **Codespaces** and the name of your codespace.
2. Open Copilot Chat.
3. Below the prompt dialog, ensure **Agent** is selected from the mode dropdown on the left.
4. Use the following prompt to ask Copilot to generate the necessary code and tests to implement filtering:

    ```markdown
    Let's update the site to have an adoption status flag for the dogs! Create the necessary tests and ensure they all pass.
    ```

> [!IMPORTANT]
> Because AI is probabilistic rather than deterministic, the exact flow, code generated, and files changed will vary. We've highlighted a likely flow you'll experience with Copilot, but the specifics may be a bit different Copilot performs its tasks for you.
>
> The desired outcome is to have all tests passing, and the feature implemented. The exact code or look and feel are secondary to this goal.

5. Copilot agent mode gets to work on the project. You will notice it begins by exploring the project, determining what's already there, and coming up with a plan. It will then work on generating the necessary code and tests.
6. As Copilot performs its operations, you'll occasionally be prompted by Copilot to execute commands to run the tests and other operations. Review the commands and, as appropriate, select **Continue**.
7. Once Copilot completes its work, select **Keep** in the chat window to keep all files.

> [!NOTE]
> There's always a chance Copilot may do the wrong thing or be unsuccessful at completing the task. While care was taken when building out the lab and scenario, mistakes can happen. If you get stuck, you can start new chat and request Copilot perform the task again, or consult with the workshop leader. 

## Validating the changes

With the newly generated code in place, let's take a moment to ensure the site has the new behavior!

1. Open a terminal window in shell in your codespace by selecting <kbd>Ctl</kbd> + <kbd>Shift</kbd> + <kbd>\`</kbd>.
2. Run the following command to start the site:

    ```shell
    ./scripts/start-app.sh
    ```

3. Once the output indicates the site has started, hold down <kbd>Cmd</kbd> (or <kbd>Ctl<kbd> on a PC) and click on the URL for `http://localhost:4321`.
4. When page opens, view the updates, noticing the flag added.

> [!NOTE]
> The exact look and feel may vary depending on the code Copilot generated.

5. Stop the site by returning to your codespace, clicking on the terminal window, and selecting <kbd>Ctl</kbd> + <kbd>C</kbd>.

## Summary and next steps

Congratulations! You've worked with GitHub Copilot to a new flag to the site. Now it's time to take that feature and kickoff the rest of the DevOps flow. Let's close out by [creating a pull request with our new functionality][next]!

## Resources

- [Asking GitHub Copilot questions in your IDE][copilot-questions]
- [Copilot Edits][copilot-chat-edits]
- [Copilot Chat cookbook][copilot-chat-cookbook]

| [← Continuous integration and testing][previous] | [Next: GitHub flow →][next] |
|:-----------------------------------|------------------------------------------:|

[next]: ./6-github-flow.md
[previous]: ./4-continuous-integration.md

[agent-mode]: https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode
[agents-in-sdlc]: https://github.com/github-samples/agents-in-sdlc
[copilot-chat-cookbook]: https://docs.github.com/en/copilot/copilot-chat-cookbook
[copilot-chat-edits]: https://code.visualstudio.com/docs/copilot/copilot-edits
[copilot-questions]: https://docs.github.com/en/copilot/using-github-copilot/copilot-chat/asking-github-copilot-questions-in-your-ide
[github-copilot]: https://docs.github.com/en/copilot/get-started/what-is-github-copilot
[github-samples]: https://github.com/github-samples/
