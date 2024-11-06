# Output the Load Balancer DNS name for the products Service
output "products_lb_dns" {
  description = "The DNS name of the products Service Load Balancer"
  value       = aws_lb.products_lb.dns_name
}

# Output the Security Group ID for the products Service
output "products_security_group_id" {
  description = "The Security Group ID for the products Service"
  value       = aws_security_group.products_sg.id
}

# Output the products Service Database Endpoint
output "products_db_endpoint" {
  description = "The endpoint of the products Service Database"
  value       = aws_db_instance.products_db.endpoint
}

# Output the RDS Database Name
output "products_db_name" {
  description = "The name of the products Service Database"
  value       = aws_db_instance.products_db.db_name
}

# Output the products Service Launch Template ID
output "products_launch_template_id" {
  description = "The ID of the Launch Template for the products Service"
  value       = aws_launch_template.products_lt.id
}
