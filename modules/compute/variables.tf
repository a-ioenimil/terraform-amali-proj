variable "security_group_id" {
  description = "Security Group ID for the instances"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for the ASG"
  type        = list(string)
}

variable "target_group_arn" {
  description = "ARN of the target group to attach to"
  type        = string
}

variable "rds_endpoint" {
  description = "RDS database endpoint"
  type        = string
}

variable "alb_dns_name" {
  description = "ALB DNS name for phpMyAdmin absolute URI"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
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
