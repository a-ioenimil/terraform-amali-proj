variable "vpc_id" {
  description = "The VPC ID"
  type        = string
}

variable "public_subnet_ids" {
  description = "List of public subnet IDs"
  type        = list(string)
}

variable "security_group_id" {
  description = "Security Group ID for the ALB"
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
