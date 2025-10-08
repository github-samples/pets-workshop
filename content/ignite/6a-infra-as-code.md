# Working with Infrastructure as Code (IaC) using GitHub Copilot

GitHub Copilot for the MSSQL extension brings AI-powered assistance directly into your SQL development workflow within Visual Studio Code. This integration enables developers to work more efficiently with SQL Server, Azure SQL, and Microsoft Fabric databases by:

- **Writing and optimizing queries** - Generate SQL queries from natural language descriptions and receive AI-recommended improvements for performance
- **Exploring and designing schemas** - Understand, design, and evolve database schemas using intelligent, code-first guidance with contextual suggestions for relationships and constraints
- **Understanding existing code** - Get natural language explanations of stored procedures, views, and functions to help you understand business logic quickly
- **Generating test data** - Create realistic, schema-aware sample data to support testing and development environments
- **Analyzing security** - Receive recommendations to avoid SQL injection, excessive permissions, and other security vulnerabilities
- **Accelerating development** - Scaffold backend components and data access layers based on your database context

This powerful combination allows you to focus on solving problems rather than memorizing SQL syntax, making database development more intuitive and productive.

## Scenario

Now that your application supports multiple database systems including SQL Server, you want to explore how GitHub Copilot can help you interact with your SQL Server database directly from VS Code. You'll use the GitHub Copilot for MSSQL extension to generate queries and explore your data using natural language.

## Prerequisites

Good news! We've already set up everything you need for this exercise:

- SQL Server Express is installed and running locally 
  - With pets database populated with data
- The **GitHub Copilot for MSSQL** extension is installed in VS Code
- A SQL Server connection has been pre-registered in your environment

You're ready to connect and start querying right away!

## Understanding GitHub Copilot for MSSQL

The GitHub Copilot for MSSQL extension brings AI-powered assistance to your database work. It can:

- Generate SQL queries from natural language descriptions
- Explain existing queries in plain English
- Suggest query optimizations and best practices
- Help explore database schemas and relationships
- Convert natural language questions into executable SQL

This integration makes working with databases more intuitive, especially when you're exploring unfamiliar schemas or need to write complex queries 