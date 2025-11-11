# Running the Lab Outside the Ignite Virtual Machine Environment

Thank you for your interest in revisiting this GitHub Copilot workshop! Whether you attended Microsoft Ignite and want to practice what you learned, or someone who attended shared this lab with you, this guide will help you set up and run the workshop on your own machine.

During the Ignite conference, the lab was delivered in a pre-configured virtual machine environment with all the necessary tools, credentials, and Azure resources already set up for you. To repeat this lab on your own machine, you'll need to set up your local development environment and meet certain prerequisites.

This guide explains everything you need to know to recreate the workshop experience outside of the provided Microsoft Ignite virtual machine environment during the lab execution.

## Prerequisites

### General Prerequisites (All Modules)

- **GitHub Copilot** subscription (free, individual, business, or enterprise)
- **Visual Studio Code** (latest version recommended)
- **GitHub Copilot extensions** for VS Code:
  - GitHub Copilot
  - GitHub Copilot Chat
- **Git** installed on your machine
- **Node.js** (v18 or later)
- **Python** (v3.8 or later)
- **PowerShell** (for Windows) or **Bash** (for Linux/Mac)

### Module-Specific Prerequisites

#### Module 3: Modernizing Your Backend
- Python package manager (**pip**)
- Virtual environment support (**venv**)

#### Module 4: Interacting with Azure
- **[GitHub Copilot for Azure][gh-copilot-for-azure]** extension for VS Code
- Azure account with an active subscription
- Azure CLI (optional, but recommended)

#### Module 5: Working with SQL Server
- **[GitHub Copilot for MSSQL][mssql-extension]** (or any SQL Server edition)
- **GitHub Copilot for MSSQL** extension for VS Code
- SQL Server running locally (Docker or native installation) or accessible remotely

#### Module 6: Infrastructure as Code
- **Terraform** (for Terraform path)
  - [HashiCorp Terraform extension for VS Code](https://marketplace.visualstudio.com/items?itemName=HashiCorp.terraform) (nice to have)
- **Bicep** (for Bicep path)
  - [Bicep extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep) (nice to have)
- Azure account with permissions to deploy resources
- Terraform CLI (for Terraform path) or Bicep CLI (for Bicep path) is a nice to have. During the lab they were missing intentionally

## Getting Started

### 1. Clone the Repository

Clone the workshop repository from the `msignite-25` branch:

```bash
git clone -b msignite-25 https://github.com/github-samples/pets-workshop.git
cd pets-workshop
```

Login into Copilot in VS Code if you haven't already.

### 2. Follow the Instructions

Navigate to the **content/ignite** folder to find the workshop modules.

### 3. Complete Modules in Order

The modules are numbered and should be completed sequentially:

1. **[Module 1: Add Endpoint](./1-add-endpoint.md)** - Learn code completion with GitHub Copilot
2. **[Module 2: Explore Project](./2-explore-project.md)** - Use chat participants and context to understand your codebase
3. **[Module 3: Modernizing Your Backend](./3-cloudify-backend.md)** - Use Agent mode and Copilot instructions to add database support
4. **[Module 4: Interacting with Azure](./4-interating-with-azure-using-natural-language.md)** - Query Azure resources using natural language
5. **[Module 5: Working with SQL Server](./5-working-with-sqlserver.md)** - Generate and execute SQL queries with natural language
6. **[Module 6: Infrastructure as Code](./6-infra-as-code.md)** - Create Terraform or Bicep templates with Copilot

#### Bonus Modules (Optional)

If you want to explore other scenarios:

- **[Bonus 1: Add Filter Feature](./b1-add-feature-bonus.md)** - Use Copilot Edits mode to implement multi-file updates for filtering dogs by breed and availability
- **[Bonus 2: Add Themes](./b2-add-filter-bonus.md)** - Use Agent mode to add theme support to the website

### 4. Setup the Application

Before starting the modules, set up and start the application:

#### For Windows (PowerShell):
```powershell
.\scripts\start-app.ps1
```

#### For Linux/Mac (Bash):
```bash
./scripts/start-app.sh
```

The startup script will:
- Install all necessary dependencies
- Start the Flask backend on **http://localhost:5100**
- Start the Astro/Svelte frontend on **http://localhost:4321**

### 5. Verify Installation

Test that everything is working:
- Backend API: http://localhost:5100/api/dogs
- Frontend app: http://localhost:4321

## Additional Notes

- Some modules (like Module 4 and Module 6) require Azure resources. You may need to provision these separately or skip those sections if you don't have Azure access.
- For Module 5, ensure SQL Server is properly configured and accessible before starting, you will be also missing the pre configured database so you will need to pre seeded as explained in the module.
- The workshop is designed to be flexible - you can choose which modules to complete based on your interests and available resources.

## Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Workshop Repository](https://github.com/github-samples/pets-workshop)
- Module-specific resources are listed at the end of each module


[mssql-extension]: https://marketplace.visualstudio.com/items?itemName=ms-mssql.mssql
[gh-copilot-for-azure]: https://marketplace.visualstudio.com/items?