output "address" {
  description = "The address of the RDS instance"
  value       = aws_db_instance.main.address
}

output "port" {
  description = "The port of the RDS instance"
  value       = aws_db_instance.main.port
}
