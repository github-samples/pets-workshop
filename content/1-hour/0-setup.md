# Workshop setup

| [← Getting started with GitHub Copilot][walkthrough-previous] | [Next: Coding with GitHub Copilot →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

To complete this workshop you will need to create a repository with a copy of the contents of this repository. While this can be done by [forking a repository][fork-repo], the goal of a fork is to eventually merge code back into the original (or upstream) source. In our case we want a separate copy as we don't intend to merge our changes. This is accomplished through the use of a [template repository][template-repo]. Template repositories are a great way to provide starters for your organization, ensuring consistency across projects.

The repository for this workshop is configured as a template, so we can use it to create your repository.

> [!IMPORTANT]
> Ensure you have the [requisite software][required-software] and [requisite resources][required-resources] setup.

## Create your repository

Let's create the repository you'll use for your workshop.

1. Navigate to [the repository root](/)
2. Select **Use this template** > **Create a new repository**

    ![Screenshot of Use this template dropdown](images/0-setup-template.png)

3. Under **Owner**, select the name of your GitHub handle, or the owner specified by your workshop leader.
4. Under **Repository**, set the name to **pets-workshop**, or the name specified by your workshop leader.
5. Ensure **Public** is selected for the visibility, or the value indicated by your workshop leader.
6. Select **Create repository from template**.

    ![Screenshot of configured template creation dialog](images/0-setup-configure.png)

In a few moments a new repository will be created from the template for this workshop!

## Clone the repository and start the app

With the repository created, it's now time to clone the repository locally. We'll do this from a shell capable of running BASH commands.

1. Copy the URL for the repository you just created in the prior set.
2. Open your terminal or command shell.
3. Run the following command to clone the repository locally (changing directories to a parent directory as appropriate):

    ```sh
    git clone <INSERT_REPO_URL_HERE>
    ```

4. Change directories into the cloned repository by running the following command:

    ```sh
    cd <REPO_NAME_HERE>
    ```

5. Start the application by running the script appropriate for your operating system:

    - macOS / Linux:

        ```sh
        ./scripts/start-app.sh
        ```

    - Windows (PowerShell):

        ```powershell
        ./scripts/start-app.ps1
        ```

    If you encounter execution policy warnings on Windows, run PowerShell as an administrator or execute the script with an explicit bypass, for example:

    ```powershell
    powershell -ExecutionPolicy Bypass -File .\scripts\start-app.ps1
    ```

The startup script will start two applications:

- The backend Flask app on [localhost:5100][flask-url]. You can see a list of dogs by opening the [dogs API][dogs-api].
- The frontend Astro/Svelte app on [localhost:4321][astro-url]. You can see the [website][website-url] by opening that URL.

## Open your editor

With the code cloned locally, and the site running, let's open the codebase up in VS Code.

1. Open VS Code.
2. Select **File** > **Open Folder**.
3. Navigate to the folder which contains the project you cloned earlier in this exercise.
4. With the folder highlighted, select **Open folder**.

## Summary and next steps

You've now cloned the repository you'll use for this workshop and have your IDE setup! Next let's [add a new endpoint to the server][walkthrough-next]!


| [← Getting started with GitHub Copilot][walkthrough-previous] | [Next: Coding with GitHub Copilot →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

[astro-url]: http://localhost:4321
[dogs-api]: http://localhost:5100/api/dogs
[flask-url]: http://localhost:5100
[fork-repo]: https://docs.github.com/en/get-started/quickstart/fork-a-repo
[required-resources]: ./README.md#required-resources
[required-software]: ./README.md#required-local-installation
[template-repo]: https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository
[walkthrough-previous]: README.md
[walkthrough-next]: ./1-add-endpoint.md
[website-url]: http://localhost:4321
