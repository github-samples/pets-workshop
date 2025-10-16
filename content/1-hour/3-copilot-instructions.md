# Providing custom instructions

| [← Coding with GitHub Copilot][walkthrough-previous] | [Next: Add the filter feature →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

There are always key pieces of information anyone generating code for your codebase needs to know - the technologies in use, coding standards to follow, project structure, etc. Since context is so important, as we've discussed, we likely want to ensure Copilot always has this information as well. Fortunately, we can provide this overview through the use of Copilot instructions.

## Scenario

Before we begin larger updates to the site with the help of Copilot, we want to ensure Copilot has a good understanding of how we're building our application. As a result, we're going to add a Copilot instructions file to the repository.

## Overview of Copilot instructions

Copilot instructions is a markdown file is placed in your **.github** folder. It becomes part of your project, and in turn to all contributors to your codebase. You can use this file to indicate various coding standards you wish to follow, the technologies your project uses, or anything else important for Copilot Chat to understand when generating suggestions.

> [!IMPORTANT]
> The *copilot-instructions.md* file is included in **every** call to GitHub Copilot Chat, and will be part of the context sent to Copilot. Because there is always a limited set of tokens an LLM can operate on, a large Copilot instructions file can obscure relevant information. As such, you should limit your Copilot instructions file to project-wide information, providing an overview of what you're building and how you're building it. If you need to provide more specific information for particular tasks, you can create [prompt files](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot?tool=vscode#about-prompt-files).

Here are some guidelines to consider when creating a Copilot instructions file:

- The Copilot instructions file becomes part of the project, meaning it will apply to every developer; anything indicated in the file should be globally applicable.
- The file is markdown, so you can take advantage of that fact by grouping content together to improve readability.
- Provide overview of **what** you are building and **how** you are building it, including:
    - languages, frameworks and libraries in use.
    - required assets to be generated (such as unit tests) and where they should be placed.
    - any language specific rules such as:
        - utilize [type hints][type-hints] in Python.
        - use [arrow functions][arrow-functions] rather than the `function` keyword in TypeScript.
- If you notice GitHub Copilot consistently provides an unexpected suggestion (e.g. using class components for React), add those notes to the instructions file.

## Create a Copilot instructions file

Let's create a Copilot instructions file. We'll start by asking Copilot to generate a block of code, then add the instructions file, then ask the same question again to see the changes.

1. Return to your IDE with your project open.
2. Close any tabs you may have open in your IDE to ensure Copilot chat has an empty context.
3. Select the `+` icon towards the top of Copilot chat to begin a new chat.
4. Open Copilot Chat and send the following prompt:

    ```
    Create a Python function to validate dog age. Ensure age is between 0 and 20. Throw an error if it is outside this range.
    ```

5. Note the function signature is similar to `def validate_dog_age(age)` without type hints.

> [!NOTE]
> Because LLMs are probabilistic rather than deterministic, the exact code will vary.

6. Create a new file in the **.github** folder called **copilot-instructions.md**.
7. Add the markdown to the file necessary which provides information about the project structure and requirements:

    ```markdown
    # Dog shelter

    This is an application to allow people to look for dogs to adopt. It is built in a monorepo, with a Flask-based backend and Astro-based frontend.

    ## Backend

    - Built using Flask and SQLAlchemy
    - Use type hints

    ## Frontend

    - Built using Astro and Svelte
    - TypeScript should use arrow functions rather than the function keyword
    - Pages should be in dark mode with a modern look and feel
    ```

8. **Save** the file.

## Watch the instructions file in action

Whenever you make a call to Copilot chat, the references dialog indicates all files used to generate the response. Once you create a Copilot instructions file, you will see it's always included in the references section. Since you included directions to use type hints, you'll notice the code suggestions will follow this guidance.

1. Close all files currently open in VS Code or your Codespace. (This will ensure we are working with an empty context.)
2. Select the `+` icon in GitHub Copilot chat to start a new chat.
3. Send Copilot chat the same prompt you used previously:

    ```
    Create a Python function to validate dog age. Ensure age is between 0 and 20. Throw an error if it is outside this range.
    ```

> [!TIP]
> You can use up arrow to resend previous prompts to Copilot chat.

4. Note the references now includes the instructions file and provides information gathered from it.

    ![Screenshot of the chat window with the references section expanded displaying Copilot instructions in the list](./images/copilot-chat-references.png)

5. Note the resulting Python now utilizes type hints, and the function signature will resemble the following:

    ```python
    def validate_dog_age(age: int):
    ```

> [!NOTE]
> The exact code generated will vary, but the new Python suggestion should now utilize type hints.

## Make the instructions even better

While we intentionally included a starter Copilot instructions file to illustrate how powerful they are, even with minimal content, you can leverage Copilot itself to either generate comprehensive instructions or improve existing ones.

### Using Copilot to generate instructions

1. Open Copilot Chat
2. Select the `+` icon towards the top of Copilot chat to begin a new chat.
3. Click on the `Cog` icon at the top of the Chat window and select `Generate Instructions` from the menu.
4. Copilot will analyze the repository and generate a comprehensive instructions file based on the project structure, technologies, and patterns.
5. Review the generated instructions. In a real-world scenario, you would customize them with items specific to your enterprise or team requirements (such as internal coding standards, security policies, or organizational best practices). For this lab, you can use the generated instructions as-is.

> [!TIP]
> The [github/awesome-copilot][awesome-copilot] repository contains a curated collection of example Copilot instructions files (as well as other resources like prompts, modes, etc.) from various projects and technologies. You can use these as inspiration or starting points for your own instructions.

### Beyond copilot-instructions.md: Specialized instructions

While `copilot-instructions.md` is included in every Copilot Chat interaction, you can also add more specialized instructions in the `.github/instructions` folder. These files can be:

- **Automatically applied** based on file patterns (using the `applyTo` frontmatter property). For example, you can ensure all React files (*.tsx and *.jsx) have the same instructions.
- **Included on demand** by adding context to the chat. This is useful for specific types of tasks, like creating a new API endpoint which might require tests and updates to a data abstraction layer.

For example, this repository includes:

- **bicep-code-best-practices.instructions.md** - Automatically applies when working with `*.bicep` files to ensure consistent Infrastructure as Code practices for Azure Bicep
- **terraform-azure.instructions.md** - Automatically applies when working with Terraform files (`*.tf`, `*.tfvars`, etc.) to follow best practices when deploying to Azure

Take some seconds to examine those files, they have been sourced from [github/awesome-copilot][awesome-copilot].

This approach keeps your main instructions file concise while providing deep, specialized guidance when needed. It's particularly useful for polyglot projects or teams working with multiple technologies and deployment targets.

## Summary and next steps

Copilot instructions improves the quality of suggestions, and ensures better alignment with the desired practices you have in place. With the groundwork in place, let's [add new functionality to our website][walkthrough-next]!

## Resources

- [Adding repository custom instructions for GitHub Copilot][custom-instructions]


| [← Coding with GitHub Copilot][walkthrough-previous] | [Next: Add the filter feature →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

[arrow-functions]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
[awesome-copilot]: https://github.com/github/awesome-copilot
[custom-instructions]: https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot
[type-hints]: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
[walkthrough-previous]: ./2-explore-project.md
[walkthrough-next]: ./4-add-feature.md