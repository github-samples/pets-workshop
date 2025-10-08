# Working with Infrastructure as Code (IaC) using GitHub Copilot

Infrastructure as Code (IaC) enables teams to define, provision, and manage cloud infrastructure using code, bringing the benefits of version control, automation, and repeatability to infrastructure management.

Tools like Terraform and Bicep make it easier to describe and deploy cloud resources declaratively — but writing and maintaining IaC files can still be time-consuming and error-prone.

This is where GitHub Copilot shines. Why Use GitHub Copilot for IaC?

GitHub Copilot can help you write, refactor, and understand IaC templates faster. By leveraging natural language prompts and contextual awareness, Copilot can:

- **Generate infrastructure templates from plain-language descriptions** - Simply describe the resource you need — for example, “create an Azure storage account with a private endpoint” — and Copilot will suggest the Terraform or Bicep code to do it.
- **Reduce syntax errors and boilerplate** - Copilot understands the structure and schema of Terraform and Bicep resources, minimizing typos and repetitive declarations.
- **Speed up resource creation** - It can quickly scaffold complete configurations, including providers, variables, modules, and outputs.
- **Improve readability and maintainability** - Copilot can add comments, generate variable documentation, and suggest consistent naming conventions.
- **Support iterative learning and experimentation** - Instead of memorizing every resource property, you can explore and refine configurations interactively within your editor.

GitHub Copilot doesn’t replace understanding Terraform or Bicep — it enhances your workflow by reducing friction and helping you focus on design and intent rather than syntax.

## Scenario

You application has a database, a website and an API. While everything is hosted locally in our repo, we want to deploy it to Azure and create an automated way to deploy our Infrastructure as Code. Making our application less prone to human deployment errors and introducing continuous integration/continuous delivery (CI/CD) into our ways of working. We will create either a Bicep or Terraform configuration file and a GitHub Actions workflow to deploy to Azure. You can choose to build a Terraform configuration file or a Bicep file (or both!), navigate to the section below that you prefer to try!

[!NOTE] The same workflow can apply to other cloud providers - Copilot can suggest Terraform code for AWS, GCP, and more. 

## Prerequisites

Good news! We've already set up everything you need for this exercise:

- GitHub Copilot enabled in your IDE 
- HashiCorp Terraform (for .tf files) extension in VSCode
- Bicep (for .bicep files) extension in VSCode

## Creating a new Terraform Configuration with Copilot

Now that your environment is ready, let’s use GitHub Copilot to help you create your first Terraform configuration file.

Terraform enables you to define your infrastructure declaratively — specifying what you want, not how to build it.
Copilot enhances this experience by suggesting Terraform code directly in your editor as you describe your desired infrastructure in natural language.