provider "aws" {
  region = var.aws_region
}

data "aws_availability_zones" "available" {}


# VPC
resource "aws_vpc" "ecommerce_vpc" {
  cidr_block = var.vpc_cidr_block
  tags = {
    Name = "ecommerce_vpc"
  }
}

# Subnets
resource "aws_subnet" "public_subnet" {
  count = 2
  vpc_id = aws_vpc.ecommerce_vpc.id
  cidr_block = element(var.public_subnet_cidrs, count.index)
  availability_zone = element(data.aws_availability_zones.available.names, count.index)
  map_public_ip_on_launch = true

  tags = {
    Name = "public_subnet-${count.index}"
  }
}

resource "aws_subnet" "private_subnet" {
  count = 2
  vpc_id = aws_vpc.ecommerce_vpc.id
  cidr_block = element(var.private_subnet_cidrs, count.index)
  availability_zone = element(data.aws_availability_zones.available.names, count.index)

  tags = {
    Name = "private_subnet-${count.index}"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "ecommerce_internet_gateway" {
  vpc_id = aws_vpc.ecommerce_vpc.id

  tags = {
    Name = "ecommerce_internet_gateway"
  }
}

# Route Table
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.ecommerce_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.ecommerce_internet_gateway.id
  }

  tags = {
    Name = "public_route_table"
  }
}

resource "aws_route_table_association" "public_subnet_route_association" {
  count = 2
  subnet_id = aws_subnet.public_subnet[count.index].id
  route_table_id = aws_route_table.public_route_table.id
}


# ECR Repository
resource "aws_ecr_repository" "products_repo" {
  name = "products-repo"
}

resource "aws_ecr_repository" "orders_repo" {
  name = "orders-repo"
}

resource "aws_ecr_repository" "inventory_repo" {
  name = "inventory-repo"
}


# Redis using ElastiCache
resource "aws_elasticache_subnet_group" "redis_subnet_group" {
  name       = "redis-subnet-group"
  subnet_ids = aws_subnet.private_subnet[*].id
}

resource "aws_elasticache_cluster" "redis_cluster" {
  cluster_id           = "redis-cluster"
  engine               = "redis"
  node_type            = "cache.t2.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  subnet_group_name    = aws_elasticache_subnet_group.redis_subnet_group.name
  port                 = 6379

  tags = {
    Name = "redis-cluster"
  }
}
