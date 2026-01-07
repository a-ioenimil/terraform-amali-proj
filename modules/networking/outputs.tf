output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "List of IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "private_app_subnet_ids" {
  description = "List of IDs of private app subnets"
  value       = aws_subnet.private_app[*].id
}

output "private_db_subnet_ids" {
  description = "List of IDs of private db subnets"
  value       = aws_subnet.private_db[*].id
}

output "public_route_table_id" {
  description = "ID of the public route table"
  value       = aws_route_table.public.id
}

output "private_app_route_table_id" {
  description = "ID of the private app route table"
  value       = aws_route_table.private_app.id
}

output "private_db_route_table_id" {
  description = "ID of the private db route table"
  value       = aws_route_table.private_db.id
}
