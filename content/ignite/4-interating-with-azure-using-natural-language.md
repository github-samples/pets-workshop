# Interacting with Azure Using GitHub Copilot

GitHub Copilot can help you manage and interact with your Azure resources directly from Visual Studio Code. Through the GitHub Copilot for Azure extension, you can query your Azure subscriptions, resource groups, and deployed resources using natural language - no need to switch between windows or memorize Azure CLI commands.

## Scenario

As the shelter's application grows, you may need to deploy it to Azure. Before doing so, it's helpful to understand what Azure resources you already have available. You'll use GitHub Copilot in Agent mode with the [GitHub Copilot for Azure][gh-copilot-for-azure] extension to explore your Azure environment using simple natural language queries.

## Overview of GitHub Copilot for Azure

The GitHub Copilot for Azure extension brings Azure management capabilities directly into your development workflow. With this extension, Copilot can:

- List your Azure subscriptions and resources
- Query resource properties and configurations
- Provide information about Azure services
- Help you understand your Azure environment

This integration allows you to stay in your coding flow while gathering information about your cloud infrastructure.

## Prerequisites

Good news! We've already set up everything you need for this exercise:

- The **[GitHub Copilot for Azure][gh-copilot-for-azure]** extension is installed in VS Code
- Azure credentials are ready for authentication
- An Azure subscription with resources is available

You're ready to start exploring your Azure environment!

## Explore your Azure resources

Let's use GitHub Copilot's Agent mode to discover what Azure resources are available in your subscription.

1. []  Close any tabs you may have open in your VS Code to ensure Copilot has a clean context.
2. []  Open or switch to GitHub Copilot Chat if it's not already open.
3. []  Switch to Agent mode by clicking on the chat mode dropdown at the bottom of the Chat view and selecting **Agent**.
    - If asked **Changing the chat mode will end your current session. Would you like to continue?** click **Yes**
    - If you were already in Agent mode, press **+** to start a new session.
4. []  Select **Claude Sonnet 4.5** from the list of available models.
5. []  Send the following prompt to the agent:

    ```text
    show me the list of my azure resources
    ```

6. Since we never logged in on Azure, the extension will guide us through the login process interactively.
7. []  The **GitHub Copilot for Azure** extension will prompt you to log in. Click **Allow** to proceed. (after Copilot attempted to run **@azure query azure resource graph**)
8. []  When prompted authenticate on popup, use the following credentials:
  -  +++@lab.CloudPortalCredential(User1).Username+++ on the **Email, phone, or Skype** input box and click on **Next**
  -  +++@lab.CloudPortalCredential(User1).AccessToken+++ on the **Temporary Access Pass** field and click on **Sign in** button
9. [] Says **Yes, all apps** when asked to **Automatically sign in to all desktop apps and websites on this device?**
10. [] Click **Allow** if prompt (**The extension 'GitHub Copilot for Azure'  wants to sign in sign in GitHub**)
11. [] Select the user to login (**User1-.....**) when prompt at the top of VS Code screen (**Select an account for 'GitHub Copilot for Azure' to use or Esc to cancel**)
12. [] With authentication in place, Copilot retrieves your resources, displaying a comprehensive list including:
    - Resource names
    - Resource types (You should have access to at least two resources: A managed identity, and a storage account)
    - Resource groups
    - Locations

> [!Tip]
> Notice how you can ask questions in natural language without needing to know specific Azure CLI commands or navigate the Azure Portal. Copilot translates your intent into the appropriate Azure queries.

> [!Tip]
> We recommend that you continue to the next lab, but we have a hidden Easter Egg in the Azure resources if you want to use Copilot to find it.

## Understanding tool execution

When you run the prompt, observe how the agent works:

- The agent identifies that it needs to interact with Azure
- It requests permission to use the Azure resource query tool
- After authentication, it executes the query and formats the results
- You receive a readable summary of your Azure resources

This demonstrates how Copilot's tool-calling capability allows it to interact with external services like Azure on your behalf, Copilot knows nothing about Azure, but the GitHub Copilot for Azure extension provides him with the tools necessary to interact with an Azure subscription and Copilot will call the necessary tools. If you click on the **Wrench** icon at the bottom of Copilot Chat, you can see the list of tools available to Copilot. The tools are made available to Copilot either by VS Code extensions or by installing an MCP server.

> [!NOTE]
> The GitHub Copilot for Azure extension provides many more capabilities beyond listing resources. You can ask questions about specific resources, query logs, get cost information, and much more - all using natural language within Copilot Chat.

> [!TIP]
> The GitHub Copilot for Azure includes the `@azure` chat participant, which allows you to specify Azure-related tasks directly without relying so much on Copilot understanding your intent. For example, you can use prompts like `@azure show me the details of my storage account` to get specific information.

## Summary and next steps

You've successfully used GitHub Copilot's Agent mode with the Azure extension to explore your Azure environment! You saw how:

- Natural language queries can retrieve Azure resource information
- Tool-calling enables Copilot to interact with external services
- You can stay in your development environment while managing cloud resources

This integration makes it easier to understand your Azure infrastructure without context switching, keeping you focused on your development tasks.

## What's next?

Now that you understand how to interact with Azure through Copilot, you can explore additional capabilities:

- **Using the MSSQL extension for Visual Studio Code** - Learn how to use Copilot to interact with SQL Server databases directly from VS Code
- **Using GitHub Copilot for Azure** - Discover how to interact with Azure resources using Copilot's Azure integration

**Choose the path** that interests you most, or explore both to get the full cloud development experience!

> [!TIP]
> In the interest of time we recommend you choose just one.

## Resources

- [GitHub MCP registry][gh-mcp-registry]
- [GitHub Copilot for Azure VS Code extension][gh-copilot-for-azure]
- [What is the Model Context Protocol (MCP)?][what-is-mcp]

[gh-copilot-for-azure]: https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azure-github-copilot
[gh-mcp-registry]: https://github.com/mcp
[what-is-mcp]: https://modelcontextprotocol.io/docs/getting-started/intro
