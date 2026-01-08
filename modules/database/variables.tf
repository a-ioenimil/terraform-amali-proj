variable "subnet_ids" {
  description = "List of subnet IDs for the DB"
  type        = list(string)
}

variable "security_group_id" {
  description = "Security Group ID for the DB"
  type        = string
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "3tier-project"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "db_name" {
  description = "Name of the database"
  type        = string
  default     = "appdb"
}

variable "db_username" {
  description = "Username for the database"
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "Password for the database"
  type        = string
  sensitive   = true
}

variable "db_engine" {
  description = "The database engine to use"
  type        = string
  default     = "mysql"
}

variable "db_engine_version" {
  description = "The engine version to use"
  type        = string
  default     = "8.0"
}

variable "db_instance_class" {
  description = "The instance type of the RDS instance"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "The allocated storage in gigabytes"
  type        = number
  default     = 20
}

variable "skip_final_snapshot" {
  description = "Skip final snapshot when destroying the DB"
  type        = bool
  default     = true
}
