output "alb_dns" {
  value = module.alb.alb_dns_name
}

output "rds_endpoint" {
  value = module.database.address
}

output "asg_name" {
  value = module.compute.asg_name
}

output "app_instance_ips" {
  description = "Private IPs of the application instances"
  value       = module.compute.instance_ips
}
