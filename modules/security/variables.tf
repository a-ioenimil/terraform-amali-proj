variable "vpc_id" {
  description = "The VPC ID"
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
