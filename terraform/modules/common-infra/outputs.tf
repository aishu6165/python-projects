output "vpc_id" {
  value = aws_vpc.ecommerce_vpc.id
}

output "public_subnets" {
  value = aws_subnet.public_subnet[*].id
}

output "private_subnets" {
  value = aws_subnet.private_subnet[*].id
}

output "redis_endpoint" {
  value = aws_elasticache_cluster.redis_cluster.cache_nodes[0].address
}

output "products_ecr_url" {
  value = aws_ecr_repository.products_repo.repository_url
}

output "orders_ecr_url" {
  value = aws_ecr_repository.orders_repo.repository_url
}

output "inventory_ecr_url" {
  value = aws_ecr_repository.inventory_repo.repository_url
}
