## Using MCP tools

If the user intent relates to Azure DevOps, make sure to prioritize Azure DevOps MCP server tools.

## Using MCP Server for Azure DevOps

When getting work items using MCP Server for Azure DevOps, always try to use batch tools for updates instead of many individual single updates. For updates, try and update up to 200 updates in a single batch. When getting work items, once you get the list of IDs, use the tool `get_work_items_batch_by_ids` to get the work item details. By default, show fields ID, Type, Title, State. Show work item results in a rendered markdown table.

# Using MCP Server for Azure Devops to "get my work items"

1. Get my assigned work items for `PetsWorkshop` project.

2. Take Id's from that result and fetch work items in batch. Get fields Id, Type, Title, State, and Priority fields. Ignore any Test Case or Test Plan work item types.

3. Show the results to me in a table with headers.

# Using MCP Server for Azure Devops to "Clean up my Epics"

When the user wants to "clean up my epics", do the following:

1. Get work items for `PetsWorkshop` project, `PetsWorkshop Team` team, and backlog category `Microsoft.EpicCategory`. When you get work items in batch, get ID, State, Priority, StackRank, and Description fields.

2. Fetch wiki page content from `https://dev.azure.com/PUnlimited/PetsWorkshop/_wiki/wikis/PetsWorkshop.wiki/5/Defining-Good-Epics`

3. Go through the description and title of each Epic where the state equals "New". If they do not align with the wiki page, update the title and description to match wiki page guidelines. I like using an emoji as a prefix before the title text. The description should be in markdown format. Make sure you set the format to 'Markdown'. Only update the Epics where State equals "New".

4. If the Epic does not have any tags, add appropriate tags based on the title and description. Only use these tags of "Security", "Performance", "Reliability", "Usability", "Maintainability", and "Scalability", "High Priority" as appropriate.

5. Set priority of the Epic. Security and High Priority should be priority 1. Performance and Reliability should be Priority 2. Scalability should be Priority 3. Everything else should be Priority 4.

6. Set the StackRank to 1 for priority 1 items. Set StackRank to 2 for priority 2 items. Set StackRank to 3 for priority 3 items. Set StackRank to 99 for priority 4 items.

7. Try and use batch update tool to update description, title, tags, and priority of the Epics. You can update 100 Epics at a time.

# Using MCP Server for Azure Devops to "Create child stories for feature"

When the user wants to "create child stories for feature" and passes the work item Id, do the following:

1. Get the feature for work item for `PetsWorkshop` project by Id. Get the comments for the work item as well.

2. Fetch wiki page content from `https://dev.azure.com/PUnlimited/PetsWorkshop/_wiki/wikis/PetsWorkshop.wiki/6/Defining-Good-Features`

3. Go through the description, title and comments of the feature. Create child user stories based on the description and comments of the feature. Each user story should follow the guidelines in the wiki page `https://dev.azure.com/PUnlimited/PetsWorkshop/_wiki/wikis/PetsWorkshop.wiki/11/Defining-Good-User-Stories`. Use `wit_add_child_work_items` tool to create child work items. Create only necessary user stories. They need to have enough detail for coding agent to get work done. But not too much so that only one small change will be made per story. Use the area path and iteration path of the feature. Format of the description should be 'Markdown'.

