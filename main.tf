# Create Networking Module
module "networking" {
  source = "./modules/networking"

  vpc_cidr                 = var.vpc_cidr
  public_subnet_cidrs      = var.public_subnet_cidrs
  private_app_subnet_cidrs = var.private_app_subnet_cidrs
  private_db_subnet_cidrs  = var.private_db_subnet_cidrs
  availability_zones       = var.availability_zones
  project_name             = var.project_name
  environment              = var.environment
}

# Create Security Module
module "security" {
  source = "./modules/security"
  vpc_id = module.networking.vpc_id

  project_name = var.project_name
  environment  = var.environment

  depends_on = [module.networking]
}

# Create ALB Module
module "alb" {
  source            = "./modules/alb"
  vpc_id            = module.networking.vpc_id
  public_subnet_ids = module.networking.public_subnet_ids
  security_group_id = module.security.alb_sg_id

  project_name = var.project_name
  environment  = var.environment

  depends_on = [module.networking, module.security]
}

# Create Compute Module
module "compute" {
  source            = "./modules/compute"
  subnet_ids        = module.networking.private_app_subnet_ids
  security_group_id = module.security.app_sg_id
  target_group_arn  = module.alb.target_group_arn
  rds_endpoint      = module.database.address
  alb_dns_name      = module.alb.alb_dns_name

  instance_type = var.instance_type
  project_name  = var.project_name
  environment   = var.environment

  depends_on = [module.networking, module.security, module.alb]
}

# Create Database Module
module "database" {
  source            = "./modules/database"
  subnet_ids        = module.networking.private_db_subnet_ids
  security_group_id = module.security.db_sg_id

  db_name           = var.db_name
  db_username       = var.db_username
  db_password       = var.db_password
  db_instance_class = var.db_instance_class
  project_name      = var.project_name
  environment       = var.environment

  depends_on = [module.networking, module.security]
}
