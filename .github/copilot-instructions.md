## Using MCP tools

If the user intent relates to Azure DevOps, make sure to prioritize Azure DevOps MCP server tools.

## Using MCP Server for Azure DevOps

When getting work items using MCP Server for Azure DevOps, always try to use batch tools for updates instead of many individual single updates. For updates, try and update up to 200 updates in a single batch. When getting work items, once you get the list of IDs, use the tool `get_work_items_batch_by_ids` to get the work item details. By default, show fields ID, Type, Title, State. Show work item results in a rendered markdown table.

# Using MCP Server for Azure Devops to "get my work items"

1. Get my assigned work items for `PartsUnlimitedGH` project.

2. Take Id's from that result and fetch work items in batch. Get fields Id, Type, Title, State, and Priority fields. Ignore any Test Case or Test Plan work item types.

3. Show the results to me in a table with headers.

# Using MCP Server for Azure Devops to "Clean up my Epics"

When the user wants to "clean up my epics", do the following:

1. Get work items for `PetsWorkshop` project, `PetsWorkshop Team` team, and backlog category `Microsoft.EpicCategory`. When you get work items in batch, get ID, State, Priority, StackRank, and Description fields.

2. Fetch wiki page content from `https://dev.azure.com/PUnlimited/PetsWorkshop/_wiki/wikis/PetsWorkshop.wiki/5/Defining-Good-Epics`

3. Go through the description and title of each Epic. If they do not align with the wiki page, update the title and description to match wiki page guidelines. I like using an emoji as a prefix before the title text. The description should be in markdown format. Make sure you set the format to 'Markdown' as well.

4. If the Epic does not have any tags, add appropriate tags based on the title and description.

5. Set priority of the Epic. Security should be priority 1. Performance should be Priority 2.

6. Set the StackRank to 1 for priority 1 items. Set StackRank to 2 for priority 2 items.

7. Try and use batch update tool to update description, title, tags, and priority of the Epics. You can update 100 Epics at a time.

# Using MCP Server for Azure Devops to "Clean up my Features"

When the user wants to "clean up my features", do the following:

1. Get work items for `PetsWorkshop` project, `PartsUnlimitedGH Team` team, and backlog category `Microsoft.FeatureCategory`. When you get work items in batch, get ID, State, Priority, StackRank, and Description fields.

2. Fetch wiki page content from `https://dev.azure.com/PUnlimited/PetsWorkshop/_wiki/wikis/PetsWorkshop.wiki/6/Defining-Good-Features`

3. Go through the description and title of each Epic. If they do not align with the wiki page, update the title and description to match wiki page guidelines. I like using an emoji as a prefix before the title text.

4. If the work does not have any tags, add appropriate tags based on the title and description.

5. Set priority of the work item. Security should be priority 1. Performance should be Priority 2.

6. Set the StackRank to 1 for priority 1 items. Set StackRank to 2 for priority 2 items.

7. Try and use batch update tool to update description, title, tags, and priority of the work items. You can update 100 work items at a time.
