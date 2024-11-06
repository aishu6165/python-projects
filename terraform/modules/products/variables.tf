variable "service_name" {
  description = "Name of the service"
  default     = "product"
}

variable "vpc_id" {
  description = "ID of the VPC to launch the service"
}

variable "subnets" {
  description = "Subnets to launch the service in"
  type        = list(string)
}

variable "db_password" {
  description = "Password for the RDS database"
  default     = "yourpassword"
}

variable "redis_url" {
  description = "Redis connection URL for inter-service communication"
}

variable "ecr_url" {
  description = "Ecr repository url of products service"
}

