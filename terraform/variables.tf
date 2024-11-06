variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  default     = "microservice-infra"
}

variable "db_password" {
  description = "RDS DB password"
  type        = string
  default     = "yourpassword"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "instance_type" {
  description = "EC2 instance type for services"
  default     = "t2.micro"
}

variable "microservices" {
  description = "List of microservices to deploy"
  type        = list(string)
  default     = ["product-service", "order-service", "inventory-service"]
}
