provider "aws" {
  region = var.aws_region
}

module "common_infra" {
  source = "./modules/common-infra"

  aws_region      = var.aws_region
  vpc_cidr_block  = var.vpc_cidr
}

module "products_service" {
  source = "./modules/products"
  vpc_id = module.common_infra.vpc_id
  subnets = module.common_infra.public_subnets
  db_password = var.db_password
  redis_url = module.common_infra.redis_endpoint
  ecr_url      = module.common_infra.products_ecr_url
}

module "orders_service" {
  source = "./modules/orders"
  vpc_id = module.common_infra.vpc_id
  subnets = module.common_infra.public_subnets
  db_password = var.db_password
  redis_url = module.common_infra.redis_endpoint
  ecr_url      = module.common_infra.orders_ecr_url
}

module "inventory_service" {
  source = "./modules/inventory"
  vpc_id = module.common_infra.vpc_id
  subnets = module.common_infra.public_subnets
  db_password = var.db_password
  redis_url = module.common_infra.redis_endpoint
  ecr_url      = module.common_infra.inventory_ecr_url
}
