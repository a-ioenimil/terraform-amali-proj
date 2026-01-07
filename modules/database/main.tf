resource "aws_db_subnet_group" "main" {
  name       = "db-subnet-${var.project_name}"
  subnet_ids = var.subnet_ids

  tags = {
    Name        = "db-subnet-${var.project_name}"
    Environment = var.environment
  }
}

resource "aws_db_instance" "main" {
  identifier             = "db-${var.project_name}"
  engine                 = var.db_engine
  engine_version         = var.db_engine_version
  instance_class         = var.db_instance_class
  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [var.security_group_id]
  skip_final_snapshot    = var.skip_final_snapshot
  allocated_storage      = var.db_allocated_storage

  tags = {
    Name        = "${var.project_name}-db"
    Environment = var.environment
  }
}
