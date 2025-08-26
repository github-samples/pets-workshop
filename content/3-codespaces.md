# Cloud-based development with GitHub Codespaces

| [← Project management with GitHub Issues][walkthrough-previous] | [Next: Continuous integration and testing →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

One of the biggest challenges organizations face is onboarding new developers to projects. There are libraries to install, services to configure, version issues, obscure error messages... It can literally take days to get everything running before a developer is able to write their first line of code.

[GitHub Codespaces][codespaces] is built to streamline this entire process. You can configure a container for development which your developers can access with just a couple of clicks - from basically anywhere in the world. The container runs in the cloud, has everything already setup, and ready to go. Instead of days, your developers can start writing code in seconds.

GitHub Codespaces allows you to develop using the cloud-based container and Visual Studio Code in your browser window, meaning no local installation is required; you can do development with a tablet and a keyboard! You can also connect your local instance of [Visual Studio Code][vscode-codespaces].

Let's explore how to create and configure a codespaces for your project, and see how you can develop in your browser.

## Using the default container

GitHub provides a [default container][github-universal-container] for all repositories. This container is based on a Linux image, and contains many popular runtimes including Node.js, Python, PHP and .NET. In many scenarios, this default container might be all you need. You also have the ability to configure a custom container for the repository, as you'll see later in this exercise. For now, let's explore how to use the default container.

1. If not already open, open your repository in your browser.
2. From the **Code** tab (suggest to open a new browser tab) in your repo, access the green **<> Code** dropdown button and from the **Codespaces** tab click **Create codespace on main**.
3. Allow the Codespace to load; it should take less than 30 seconds because we are using the default image.

## Defining a custom container

One thing that's really great is the [default dev container][github-universal-container-definition] has **.NET 7**, **node**, **python**, **mvn**, and more. But what if you need other tools? Or in our case, we want don't want to have each developer install the **[GitHub Copilot Extension][copilot-extension]**; we want to have everything pre-configured from the start!

Let's create our own dev container!

The [dev container is configured][dev-containers-docs] by creating the Docker files Codespaces will use to create and configure the container, and providing any customizations in the `devcontainer.json` file. Customizations provided in `devcontainer.json` can include ports to open, commands to run, and extension to install in Visual Studio Code (either running locally on the desktop or in the browser). This configuration becomes part of the repository. All developers who wish to contribute can then create a new instance of the container based on the configuration you provided.

1. Access the Command Palette (<kbd>F1</kbd> or clicking ☰ → View → Command Palette), then start typing **dev container**.
2. Select **Codespaces: Add Development Container Configuration Files...** .
3. Select **Create a new configuration...**.
4. Scroll down and select **Node.js & TypeScript**.
5. Select **22-bookworm (default)**.
6. Select the following features to add into your container:
    - **Azure CLI**
    - **GitHub CLI**
    - **Python**

> [!NOTE]
> You can type the name of the feature you want to filter the list.

7. Select **OK** to add the features.
8. Select **Keep defaults** to use the default configuration.
9. If you receive the prompt **File './.github/dependabot.yml' already exists, overwrite?**, select **Skip**.

> [!IMPORTANT]
> Your new container definition files will be created into the **.devcontainer** folder. **DO NOT** select **Rebuild Now**; we'll do that in just a moment.

You have now defined the container to be used by your codespace. This contains the necessary services and tools for your code.

## Customize the extensions

Creating a development environment isn't solely focused on the services. Developers rely on various extensions and plugins for their [integrated development environments (IDEs)][IDE]. To ensure consistency, you may want to define a set of extensions to automatically install. When using GitHub Codespaces and either a local instance of Visual Studio Code or the browser-based version, you can add a list of [extensions][vscode-extensions] to the **devcontainer.json** file.

Before rebuilding the container, let's add the project-specific extensions our developers will want to the list defined in **devcontainer.json**.

1. Remaining in the codespace, open **devcontainer.json** inside the **.devcontainer** folder.
2. Locate the following section:

    ```json
    "features": {
		"ghcr.io/devcontainers/features/github-cli:1": {},
		"ghcr.io/devcontainers/features/python:1": {}
	}
    ```

3. Add a comma (`,`) to the end of the last `}`, which should be line 10.
4. Immediately below that line, paste the following code to provide the list of extensions you wish to have for your dev container:

    ```json
    "customizations": {
		"vscode": {
			"extensions": [
				"GitHub.copilot",
				"GitHub.copilot-chat",
                "ms-azuretools.vscode-azure-github-copilot",
				"alexcvzz.vscode-sqlite",
				"astro-build.astro-vscode",
				"svelte.svelte-vscode",
				"ms-python.python",
				"ms-python.vscode-pylance"
			]
		}
	},
    ```

## Add forwarded ports

As we're working on the website we'll want to be able to run it and confirm things are working as we expected. Codespaces allows you to [forward ports][codespaces-forward-ports], allowing you to access them, almost as if they were running locally. Let's add the ports for our webapp to the list of ones to be forwarded by the codespace.

1. Return to **devcontainer.json**.
2. Just below the `customizations` section you utilized a moment ago, paste the following code to provide the list of ports which should be made available for development by the codespace:

    ```json
    "forwardPorts": [
		4321,
		5100,
		5000
	],
    ```

## Startup scripts

You frequently will need to run scripts to finish the configuration of an environment, or to start the required services. To support this, you can define a [`postStartCommand`][vscode-post-start-command] in your **devcontainer.json**. In our case, we want to ensure the app starts to streamline debugging. Let's get that added.

1. Return to **devcontainer.json**.
2. Just below the `forwardedPorts` section you utilized a moment ago, add the command to run the startup script to the container definition:

    ```json
    "postStartCommand": "chmod +x /workspaces/dog-shelter/scripts/start-app.sh && /workspaces/dog-shelter/scripts/start-app.sh",
    ```

You've now defined a custom container!

## Use the newly defined custom container

Whenever someone uses the codespace you defined they'll have an environment with Node.js and Mongo DB, and the GitHub Copilot extension installed. Let's use this container!

1. Access the Command Palette (<kbd>F1</kbd> or clicking ☰ → View → Command Palette), then start typing **dev container**.
2. Type **rebuild** and select **Codespaces: Rebuild container**.
3. Select **Rebuild Container** on the dialog box. Your container now rebuilds.

> [!IMPORTANT]
> Rebuilding the container can take several minutes. Obviously this isn't an ideal situation for providing fast access to your developers, even if it's faster than creating everything from scratch. Fortunately you can [prebuild your codespaces][codespace-prebuild] to ensure developers can spin one up within seconds.
>
> You may also be prompted to reload the window as extensions install. Reload the window as prompted.

## Interacting with the repository

Custom containers for GitHub Codespaces become part of the source code for the repository. Thus they are maintained through standard source control, and will follow the repository as it's forked in the future. This allows this definition to be shared across all developers contributing to the project. Let's upload our new configuration, closing the [issue you created][walkthrough-previous] for defining a development environment.

> [!IMPORTANT]
> For purposes of this exercise we are pushing code updates directly to `main`, our default branch. Normally you would follow the [GitHub flow][github-flow], which we will do in a [later exercise][github-flow-exercise].

1. Open a new terminal window in the codespace by selecting <kbd>Ctl</kbd> + <kbd>Shift</kbd> + <kbd>`</kbd> or clicking ☰ → View → Terminal.
2. Find the issue number for defining the codespace by entering the following command:

    ```bash
    gh issue list
    ```

> [!NOTE]
> It will likely be #1. You'll use this number later in this exercise.

3. Stage all files, commit the changes with a message to resolve the issue, and push to main by entering the following command in the terminal window, replacing `<ISSUE_NUMBER>` with the number you obtained in the previous step:

    ```bash
    git add .
    git commit -m "Resolves #<ISSUE_NUMBER>"
    git push
    ```
> [!NOTE]
> If prompted, select **Allow** to enable copy/paste for the codespace.

4. When the command completes, enter the following to list all open issues:

    ```bash
    gh issue list
    ```

5. Note the issue for defining a codespace is no longer listed; you completed it and marked it as such with your pull request!


## Summary and next steps

Congratulations! You have now defined a custom development environment including all services and extensions. This eliminates the initial setup hurdle normally required when contributing to a project. Let's use this codespace to [implement testing and continuous integration][walkthrough-next] for the project.

## Resources

- [GitHub Codespaces][codespaces]
- [Getting started with GitHub Codespaces][codespaces-docs]
- [Defining dev containers][dev-containers-docs]
- [GitHub Skills: Code with Codespaces][skills-codespaces]

| [← Project management with GitHub Issues][walkthrough-previous] | [Next: Continuous integration and testing →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

[codespaces]: https://github.com/features/codespaces
[codespaces-forward-ports]: https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace
[copilot-extension]: https://marketplace.visualstudio.com/items?itemName=GitHub.copilot
[codespaces-docs]: https://docs.github.com/en/codespaces/overview
[codespace-prebuild]: https://docs.github.com/en/codespaces/prebuilding-your-codespaces
[dev-containers-docs]: https://docs.github.com/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers
[github-flow]: https://docs.github.com/en/get-started/quickstart/github-flow
[github-flow-exercise]: ./7-github-flow.md
[github-universal-container]: https://docs.github.com/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers#using-the-default-dev-container-configuration
[github-universal-container-definition]: https://github.com/devcontainers/images/blob/main/src/universal/.devcontainer/Dockerfile
[IDE]: https://en.wikipedia.org/wiki/Integrated_development_environment
[skills-codespaces]: https://github.com/skills/code-with-codespaces
[vscode-codespaces]: https://docs.github.com/en/codespaces/developing-in-codespaces/using-github-codespaces-in-visual-studio-code
[vscode-extensions]: https://code.visualstudio.com/docs/editor/extension-marketplace
[vscode-post-start-command]: https://code.visualstudio.com/remote/advancedcontainers/start-processes
[walkthrough-previous]: 2-issues.md
[walkthrough-next]: 4-testing.md
