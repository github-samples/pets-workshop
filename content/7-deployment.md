# Deploying the project to the cloud

| [← GitHub flow][walkthrough-previous] | [Next: Pets workshop selection →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

The CD portion of CI/CD is continuous delivery or continuous deployment. In a nutshell, it's about taking the product you're building and putting it somewhere to be accessed by the people who need it. There's numerous ways to do this, and the process can become rather involved. We're going to focus on taking our application and deploying it to Azure.

> [!NOTE]
> We've taken a couple of shortcuts with the application structure to ensure things run smoothly in this workshop.

## Scenario

With the prototype built, the shelter is ready to begin gathering feedback from external users. They want to deploy the project to the internet, and ensure any updates merged into main are available as quickly as possible.

## Return to main

To streamline the process, we're going to work directly with the **main** branch. Let's change back to the **main** branch and obtain the updates we pushed previously.

1. Return to your codespace, or reopen it by navigating to your repository and selecting **Code** > **Codespaces** and the name of your codespace.
2. Open a new terminal window by selecting <kbd>Ctl</kbd>+<kbd>Shift</kbd>+<kbd>`</kbd>.
3. Run the following commands to checkout the main branch and obtain the updates from the repository:

    ```sh
    git checkout main
    git pull
    ```

## Identity management

Whenever you're interacting with an external service, you of course need credentials to perform any actions. This holds true when you're creating any form of automated tasks, such as a workflow in GitHub. There are several ways to manage identities, including access tokens, shared passwords, and [Open ID Connect (OIDC)][oidc-docs], with the latter being the newest and preferred mechanism. The advantage to OIDC is it uses short-lived tokens and provides granular control over the operations which can be performed.

Creating and setting up the credentials is typically a task performed by administrators. However, there are tools which can manage this for you, one of which we'll be taking advantage of!

## Asking Azure how to deploy to Azure

We previously talked about [extensions for GitHub Copilot chat][extensions-copilot-chat], which allow you to interact with external services. These external services could provide access to information about your DevOps flow, database, and other resources. One such extension is the [Azure extension][azure-copilot-extension], which as the name implies allows you to interact with Azure. You can use the extension to get advice on how to deploy your application, check the status of services, and perform other operations. We'll use this extension to ask how to deploy our application.

As we've done with other tasks, we don't have a specific prompt to use when talking with Azure, as part of the experience is to learn how best to interact with GitHub Copilot. The requirements for the deployment are:

- Deploy the project to the cloud
- Use a GitHub action to manage the deployment process

1. Open GitHub Copilot Chat.
2. Activate the Azure extension by typing `@azure`, selecting <kbd>Tab</kbd> then asking the extension how to perform the task you wish to perform (see the requirements above).

> [!NOTE]
> Since this is your first time using the extension, you will be prompted to signin to Azure. Follow the prompts as they appear.

3. You should receive a response which highlights the `azd` command, which can be used to both initialize a cloud environment and create the workflow.

## Overview of the response from Copilot

The response from GitHub Copilot will likely contain instructions to use the following commands:

- `azd init --from-code` to create the Azure configuration files using [bicep][bicep-docs].
- `azd auth login` to authenticate to Azure.
- `azd pipeline config` to create the GitHub Workflow.

[azd][azd-docs] is a commandline utility to help streamline the deployment process to Azure. We'll use it to:

- generate the bicep file.
- create the workflow file.
- create and configure OIDC for the workflow.

If you're curious about **azd** or Azure, you can always ask the extension using GitHub Copilot!

## Install azd

Let's start by installing **azd**.

1. Run the command in the terminal to install **azd**:

    ```sh
    curl -fsSL https://aka.ms/install-azd.sh | bash
    ```

## Create and configure the bicep file

Bicep is a domain specific language (DSL) for defining Azure resources. It's dynamic, allowing you to ensure your environment is configured exactly as you need it. We're going to start by allowing **azd** create the bicep file, then make an update to ensure we have an environment variable available for the client to connect to the server.

1. Run the `init` command to create the bicep file.

    ```sh
    azd init --from-code
    ```

2. Follow the prompts, accepting any defaults provided by the tool, and naming your namespace (which will be used to name the resource group and various resources in Azure) something unique.
3. Open the bicep file located at **infra**/**resources.bicep**.
4. Find the section (around line 130) which reads:

    ```bicep
    {
      name: 'PORT'
      value: '4321'
    }
    ```

5. Create a new line below the closing `}` and add the following to create an environment variable with the URL of the newly created Flask server:

    ```bicep
    {
      name: 'API_SERVER_URL'
      value: 'https://${server.outputs.fqdn}'
    }
    ```

> [!NOTE]
> While the syntax resembles JSON, it's not JSON. As a result, resist the urge to add commas to separate the values!

## Create the workflow

`azd` can create and configure a workflow (or sometimes called a pipeline) for deploying your project. In particular it will:

- create OIDC credentials to use for deployment.
- define the YML file in the **workflows** folder.

Let's let `azd` do its work!

1. Return to your terminal window, and run the following command to authenticate with `azd`

    ```sh
    azd auth login
    ```

2. Follow the prompts to authenticate to Azure using the credentials you specified previously.
3. Create the pipeline by running the following command:

    ```sh
    azd pipeline config
    ```

4. Follow the prompts, accepting the defaults. One of the prompts will ask if you wish to perform the deployment now - say yes!
5. Away your application goes to the cloud!

## Track the deployment and test your application

The `azd pipeline config` command will create a new workflow file at **.github/workflows/azure-dev.yml**. Let's explore the workflow, track the action as it runs (this will take a few minutes), and test the application!

1. Open the workflow at **.github/workflows/azure-dev.yml**.
2. Note the `on` section, which contains the flags for `workflow_dispatch` (to support manual deployment), and `push` to automatically deploy when code is pushed to the **main** branch.
3. Note the core steps, which checkout your code, authenticate to Azure, create or update the infrastructure, then deploy the application.
4. If you have questions about what the workflow is doing, ask GitHub Copilot!
5. Navigate to your repository on GitHub.
6. Open the **Actions** tab, then the action named **.github/workflows/azure-dev.yml**. You should see the action running (the icon will be yellow under the **workflow runs** section).
7. Select the running workflow (which should be named **Configure Azure Developer Pipeline**).
8. Select the **build** step.
9. Track the deployment process, which will take about 5-10 minutes (good time for a water break!).
10. Once the process completes, expand the **Deploy Application** section. You should see the log indicating the client and server were both deployed:

    ```
    Deploying service client
    Deploying service client (Building Docker image)
    Deploying service client (Tagging container image)
    Deploying service client (Tagging container image)
    Deploying service client (Logging into container registry)
    Deploying service client (Pushing container image)
    Deploying service client (Updating container app revision)
    Deploying service client (Fetching endpoints for container app service)
    (✓) Done: Deploying service client
    - Endpoint: https://client.delightfulfield-8f7ef050.westus.azurecontainerapps.io/

    Deploying service server
    Acquiring pack cli
    Deploying service server (Building Docker image from source)
    Deploying service server (Tagging container image)
    Deploying service server (Tagging container image)
    Deploying service server (Logging into container registry)
    Deploying service server (Pushing container image)
    Deploying service server (Updating container app revision)
    Deploying service server (Fetching endpoints for container app service)
    (✓) Done: Deploying service server
    - Endpoint: https://server.delightfulfield-8f7ef050.westus.azurecontainerapps.io/
    ```

11.  Select the Endpoint for the client. You should see your application!

You've now deployed your project!

## Summary

You've now created and configured a full CI/CD process. You implemented security checks, testing, and now deployment. As highlighted previously, enterprise CI/CD processes can be rather complex, but at their core they use the skills you explored during this workshop.

## Wrap-up and challenge

Congratulations! You've gone through an entire DevOps process. You began by creating an issue to document the required work, then ensured everything was in place to run automatically. You performed the updates to the application, pushed everything to your repository, and merged it in!

If you wish to continue exploring from here, there are a couple of tasks you could pursue:

- Add more functionality to the website! There's a lot you could do, like adding on an adoption form or the ability to store images.
- Migrate the database to something more powerful such as Postgres or SQL Server.

Work with the workshop leaders as needed to ask questions and get guidance as you continue to build on the skills you learned today!

## Resources

- [About security hardening with OpenID Connect][oidc-docs]
- [Deploying with GitHub Actions][actions-deploy]
- [What is the Azure Developer CLI?][azd-docs]

| [← GitHub flow][walkthrough-previous] | [Next: Pets workshop selection →][walkthrough-next] |
|:-----------------------------------|------------------------------------------:|

[actions-deploy]: https://docs.github.com/en/actions/use-cases-and-examples/deploying/deploying-with-github-actions
[azd-docs]: https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview?tabs=linux
[azure-copilot-extension]: https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azure-github-copilot
[bicep-docs]: https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview?tabs=bicep
[extensions-copilot-chat]: ./5-context.md
[oidc-docs]: https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect
[walkthrough-previous]: 7-github-flow.md
[walkthrough-next]: ../README.md