# Output values for the Pets Workshop Azure deployment

# Resource Group
output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.main.name
}

output "resource_group_location" {
  description = "Location of the resource group"
  value       = azurerm_resource_group.main.location
}

# Backend App Service
output "backend_app_service_name" {
  description = "Name of the backend App Service"
  value       = azurerm_linux_web_app.backend.name
}

output "backend_app_service_url" {
  description = "URL of the backend App Service"
  value       = "https://${azurerm_linux_web_app.backend.default_hostname}"
}

output "backend_app_service_hostname" {
  description = "Default hostname of the backend App Service"
  value       = azurerm_linux_web_app.backend.default_hostname
}

# Frontend Static Web App
output "frontend_static_web_app_name" {
  description = "Name of the frontend Static Web App"
  value       = azurerm_static_web_app.frontend.name
}

output "frontend_static_web_app_url" {
  description = "URL of the frontend Static Web App"
  value       = azurerm_static_web_app.frontend.default_host_name
}

output "frontend_deployment_token" {
  description = "Deployment token for Static Web App (sensitive)"
  value       = azurerm_static_web_app.frontend.api_key
  sensitive   = true
}

# Database
output "sql_server_name" {
  description = "Name of the SQL Server"
  value       = azurerm_mssql_server.main.name
}

output "sql_server_fqdn" {
  description = "Fully qualified domain name of the SQL Server"
  value       = azurerm_mssql_server.main.fully_qualified_domain_name
}

output "sql_database_name" {
  description = "Name of the SQL Database"
  value       = azurerm_mssql_database.main.name
}

# Key Vault
output "key_vault_name" {
  description = "Name of the Key Vault"
  value       = azurerm_key_vault.main.name
}

output "key_vault_uri" {
  description = "URI of the Key Vault"
  value       = azurerm_key_vault.main.vault_uri
}

# Application Insights
output "application_insights_name" {
  description = "Name of Application Insights"
  value       = azurerm_application_insights.main.name
}

output "application_insights_instrumentation_key" {
  description = "Application Insights instrumentation key"
  value       = azurerm_application_insights.main.instrumentation_key
  sensitive   = true
}

output "application_insights_connection_string" {
  description = "Application Insights connection string"
  value       = azurerm_application_insights.main.connection_string
  sensitive   = true
}

# Deployment Information
output "deployment_instructions" {
  description = "Instructions for deploying the application"
  value = <<-EOT
    
    ## Next Steps for Deployment:
    
    ### 1. Backend Flask App Deployment:
    - Update your Flask app to use SQL Server instead of SQLite
    - Deploy using: az webapp deploy --resource-group ${azurerm_resource_group.main.name} --name ${azurerm_linux_web_app.backend.name} --src-path ./server
    - Or use GitHub Actions with the workflow file provided
    
    ### 2. Frontend Astro App Deployment:
    - Update API endpoints in your Astro app to point to: ${azurerm_linux_web_app.backend.default_hostname}
    - Build your app: npm run build
    - Deploy using GitHub Actions with the Static Web App token
    
    ### 3. Database Setup:
    - Connect to SQL Server: ${azurerm_mssql_server.main.fully_qualified_domain_name}
    - Database: ${azurerm_mssql_database.main.name}
    - Run your database migration scripts
    
    ### 4. Monitoring:
    - Application Insights: ${azurerm_application_insights.main.name}
    - View logs and metrics in the Azure Portal
    
  EOT
}

# Environment Configuration
output "environment_variables" {
  description = "Environment variables for application configuration"
  value = {
    "AZURE_SQL_SERVER"      = azurerm_mssql_server.main.fully_qualified_domain_name
    "AZURE_SQL_DATABASE"    = azurerm_mssql_database.main.name
    "AZURE_KEY_VAULT_NAME"  = azurerm_key_vault.main.name
    "BACKEND_URL"           = "https://${azurerm_linux_web_app.backend.default_hostname}"
    "FRONTEND_URL"          = "https://${azurerm_static_web_app.frontend.default_host_name}"
  }
}