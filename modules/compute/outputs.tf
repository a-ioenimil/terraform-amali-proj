output "asg_name" {
  description = "Name of the Auto Scaling Group"
  value       = aws_autoscaling_group.main.name
}

output "launch_template_id" {
  description = "ID of the Launch Template"
  value       = aws_launch_template.main.id
}

output "instance_ips" {
  description = "The private IP addresses of the instances in the ASG"
  value       = data.aws_instances.asg_instances.private_ips
}
