# Input variables for Terraform configuration

variable "resource_prefix" {
  description = "Prefix for all resource names to ensure uniqueness"
  type        = string
  default     = "petswrkshp"
  
  validation {
    condition     = length(var.resource_prefix) <= 10 && can(regex("^[a-z0-9]+$", var.resource_prefix))
    error_message = "Resource prefix must be 10 characters or less and contain only lowercase letters and numbers."
  }
}

variable "location" {
  description = "Azure region for resource deployment"
  type        = string
  default     = "East US"
  
  validation {
    condition = contains([
      "East US", "East US 2", "West US", "West US 2", "West US 3",
      "Central US", "North Central US", "South Central US", "West Central US",
      "Canada Central", "Canada East", "Brazil South", "UK South", "UK West",
      "West Europe", "North Europe", "France Central", "Germany West Central",
      "Norway East", "Switzerland North", "Sweden Central",
      "Australia East", "Australia Southeast", "Japan East", "Japan West",
      "Korea Central", "Southeast Asia", "East Asia", "Central India",
      "South India", "West India"
    ], var.location)
    error_message = "Location must be a valid Azure region."
  }
}

variable "static_web_app_location" {
  description = "Azure region for Static Web App (limited regions available)"
  type        = string
  default     = "East US 2"
  
  validation {
    condition = contains([
      "East US 2", "Central US", "West US 2", "West Europe"
    ], var.static_web_app_location)
    error_message = "Static Web App location must be East US 2, Central US, West US 2, or West Europe."
  }
}

variable "sql_admin_username" {
  description = "Administrator username for SQL Server"
  type        = string
  default     = "sqladmin"
  
  validation {
    condition     = length(var.sql_admin_username) >= 1 && length(var.sql_admin_username) <= 128
    error_message = "SQL admin username must be between 1 and 128 characters."
  }
}

variable "sql_admin_password" {
  description = "Administrator password for SQL Server"
  type        = string
  sensitive   = true
  
  validation {
    condition = length(var.sql_admin_password) >= 8 && length(var.sql_admin_password) <= 128
    error_message = "SQL admin password must be 8-128 characters and contain uppercase, lowercase, digit, and special character."
  }
}

variable "app_service_sku" {
  description = "SKU for the App Service Plan"
  type        = string
  default     = "B1"
  
  validation {
    condition = contains([
      "F1", "D1", "B1", "B2", "B3", "S1", "S2", "S3", "P1", "P2", "P3", "P1v2", "P2v2", "P3v2", "P1v3", "P2v3", "P3v3"
    ], var.app_service_sku)
    error_message = "App Service SKU must be a valid tier (F1, D1, B1-B3, S1-S3, P1-P3, P1v2-P3v2, P1v3-P3v3)."
  }
}

variable "sql_database_sku" {
  description = "SKU for the SQL Database"
  type        = string
  default     = "Basic"
  
  validation {
    condition = contains([
      "Basic", "S0", "S1", "S2", "S3", "S4", "S6", "S7", "S9", "S12",
      "P1", "P2", "P4", "P6", "P11", "P15"
    ], var.sql_database_sku)
    error_message = "SQL Database SKU must be a valid service tier."
  }
}

variable "static_web_app_sku" {
  description = "SKU for Static Web App"
  type        = string
  default     = "Free"
  
  validation {
    condition     = contains(["Free", "Standard"], var.static_web_app_sku)
    error_message = "Static Web App SKU must be Free or Standard."
  }
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    Environment = "dev"
    Project     = "PetsWorkshop"
    ManagedBy   = "Terraform"
    Owner       = "DevTeam"
  }
}