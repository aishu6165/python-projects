output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.common_infra.vpc_id
}

output "public_subnets" {
  description = "The IDs of the public subnets"
  value       = module.common_infra.public_subnets
}

output "redis_endpoint" {
  description = "The endpoint for the Redis cluster"
  value       = module.common_infra.redis_endpoint
}


output "products_ecr_url" {
  value = module.common_infra.products_ecr_url
}

output "orders_ecr_url" {
  value = module.common_infra.orders_ecr_url
}

output "inventory_ecr_url" {
  value = module.common_infra.inventory_ecr_url
}

