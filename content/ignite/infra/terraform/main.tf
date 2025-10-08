# Main Terraform configuration for Pets Workshop Azure deployment

# Generate random string for unique naming
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

# Get current user context for Key Vault access policy
data "azurerm_client_config" "current" {}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${var.resource_prefix}-rg-${random_string.suffix.result}"
  location = var.location

  tags = var.tags
}

# Application Insights for monitoring
resource "azurerm_application_insights" "main" {
  name                = "${var.resource_prefix}-ai-${random_string.suffix.result}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  application_type    = "web"

  tags = var.tags
}

# Key Vault for storing secrets
resource "azurerm_key_vault" "main" {
  name                = "${var.resource_prefix}-kv-${random_string.suffix.result}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  # Enable soft delete and purge protection
  soft_delete_retention_days = 7
  purge_protection_enabled   = false

  # Network access
  network_acls {
    default_action = "Allow"
    bypass         = "AzureServices"
  }

  tags = var.tags
}

# Key Vault access policy for current user
resource "azurerm_key_vault_access_policy" "current_user" {
  key_vault_id = azurerm_key_vault.main.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id

  secret_permissions = [
    "Get",
    "List",
    "Set",
    "Delete",
    "Recover",
    "Backup",
    "Restore"
  ]
}

# SQL Server
resource "azurerm_mssql_server" "main" {
  name                         = "${var.resource_prefix}-sql-${random_string.suffix.result}"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = azurerm_resource_group.main.location
  version                      = "12.0"
  administrator_login          = var.sql_admin_username
  administrator_login_password = var.sql_admin_password

  # Security configurations
  minimum_tls_version = "1.2"

  azuread_administrator {
    login_username = var.sql_admin_username
    object_id      = data.azurerm_client_config.current.object_id
  }

  tags = var.tags
}

# SQL Database
resource "azurerm_mssql_database" "main" {
  name           = "${var.resource_prefix}-sqldb-${random_string.suffix.result}"
  server_id      = azurerm_mssql_server.main.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  license_type   = "LicenseIncluded"
  max_size_gb    = 2
  sku_name       = var.sql_database_sku
  zone_redundant = false

  tags = var.tags
}

# SQL Server firewall rule to allow Azure services
resource "azurerm_mssql_firewall_rule" "allow_azure_services" {
  name             = "AllowAzureServices"
  server_id        = azurerm_mssql_server.main.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

# Store database connection string in Key Vault
resource "azurerm_key_vault_secret" "database_connection_string" {
  name         = "database-connection-string"
  value        = "mssql+pyodbc://${var.sql_admin_username}:${var.sql_admin_password}@${azurerm_mssql_server.main.fully_qualified_domain_name}:1433/${azurerm_mssql_database.main.name}?driver=ODBC+Driver+17+for+SQL+Server"
  key_vault_id = azurerm_key_vault.main.id

  depends_on = [azurerm_key_vault_access_policy.current_user]
}

# App Service Plan for Flask backend
resource "azurerm_service_plan" "main" {
  name                = "${var.resource_prefix}-asp-${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = var.app_service_sku

  tags = var.tags
}

# App Service for Flask backend
resource "azurerm_linux_web_app" "backend" {
  name                = "${var.resource_prefix}-backend-${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_service_plan.main.location
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      python_version = "3.11"
    }

    # Enable CORS for frontend
    cors {
      allowed_origins = ["*"] # In production, specify your frontend domain
      support_credentials = false
    }

    # Health check
    health_check_path = "/api/dogs"
  }

  # Application settings
  app_settings = {
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = azurerm_application_insights.main.connection_string
    "SCM_DO_BUILD_DURING_DEPLOYMENT"       = "true"
    "ENABLE_ORYX_BUILD"                    = "true"
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE"  = "false"
    
    # Database configuration will be set via Key Vault reference
    "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.database_connection_string.id})" = "DATABASE_URL"
  }

  # Identity for Key Vault access
  identity {
    type = "SystemAssigned"
  }

  tags = var.tags
}

# Key Vault access policy for App Service managed identity
resource "azurerm_key_vault_access_policy" "app_service" {
  key_vault_id = azurerm_key_vault.main.id
  tenant_id    = azurerm_linux_web_app.backend.identity[0].tenant_id
  object_id    = azurerm_linux_web_app.backend.identity[0].principal_id

  secret_permissions = [
    "Get",
    "List"
  ]
}

# Static Web App for frontend
resource "azurerm_static_web_app" "frontend" {
  name                = "${var.resource_prefix}-swa-${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.static_web_app_location
  sku_tier            = var.static_web_app_sku
  sku_size            = var.static_web_app_sku

  tags = var.tags
}

# Static Web App custom domain (optional)
# Uncomment and configure if you have a custom domain
# resource "azurerm_static_web_app_custom_domain" "frontend" {
#   static_web_app_id = azurerm_static_web_app.frontend.id
#   domain_name       = var.custom_domain
#   validation_type   = "cname-delegation"
# }