# Coding with GitHub Copilot

| [← Helping GitHub Copilot understand context][walkthrough-previous] | [Next: GitHub flow →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

We've explored how we can use GitHub Copilot to explore our project and to provide context to ensure the suggestions we receive are to the quality we expect. Now let's turn our attention to putting all this prep work into action by generating new code! We'll use GitHub Copilot to aid us in adding functionality to our website and generate the necessary unit tests.

> [!IMPORTANT]
> Something something, we're not going too deep into copilot, check out our other amazing workshop!!

## Scenario

The website currently lists all dogs in the database. While this was appropriate when the shelter only had a few dogs, as time has gone on the number has grown and it's difficult for people to sift through who's available to adopt. The shelter has asked you to add filters to the website to allow a user to select a breed of dog and only display dogs which are available for adoption.

## Overview of this exercise

To streamline the creation of both the feature and required infrastructure you'll utilize GitHub Copilot agent mode to generate the code and tests.

## GitHub Copilot agent mode

In the [prior exercise][walkthrough-previous], you utilized **ask mode** in GitHub Copilot. Ask mode is focused on "single-turn" operations, where you ask a question, receive an answer, and then repeat the flow as needed. Ask mode is great for generating individual files, learning about your project, and generic code-related questions.

**Agent mode** allows Copilot to act more like a peer programmer, both generating code suggestions and performing tasks on your behalf. Agent mode will explore your project, build an approach of how to resolve a problem, generate the code, perform supporting operations like running tests, and even self-heal should it find any problems.

By using agent mode, we'll be able to both create the code and tests, but have Copilot run the tests and correct any mistakes it might find.

## Create the filter and tests

Let's ask Copilot to generate the code to add the feature and tests!

1. Return to your codespace, or reopen it by navigating to your repository and selecting **Code** > **Codespaces** and the name of your codespace.
2. Open Copilot Chat.
3. Below the prompt dialog, ensure **Agent** is selected from the mode dropdown on the left.
4. Use the following prompt to ask Copilot to generate the necessary code and tests to implement filtering:

    ```markdown
    Update the website to allow for filtering of dogs by breed and adoption status. The page should update as filters are modified. Ensure both unit tests and end to end tests are created, and they all pass. If any tests are failing, make the necessary updates so they pass.
    ```

## Summary and next steps

Congratulations! You've worked with GitHub Copilot to add new features to the website - the ability to filter the list of dogs. Let's close out by [creating a pull request with our new functionality][walkthrough-next]!

## Resources

- [Asking GitHub Copilot questions in your IDE][copilot-questions]
- [Copilot Edits][copilot-chat-edits]
- [Copilot Chat cookbook][copilot-chat-cookbook]

| [← Helping GitHub Copilot understand context][walkthrough-previous] | [Next: GitHub flow →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

[copilot-chat-cookbook]: https://docs.github.com/en/copilot/copilot-chat-cookbook
[copilot-chat-edits]: https://code.visualstudio.com/docs/copilot/copilot-edits
[copilot-questions]: https://docs.github.com/en/copilot/using-github-copilot/copilot-chat/asking-github-copilot-questions-in-your-ide
[localhost]: http://localhost:4321
[localhost-breeds]: http://localhost:5100/api/breeds
[walkthrough-previous]: 5-context.md
[walkthrough-next]: 7-github-flow.md
