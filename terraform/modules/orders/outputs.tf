# Output the Load Balancer DNS name for the orders Service
output "orders_lb_dns" {
  description = "The DNS name of the orders Service Load Balancer"
  value       = aws_lb.orders_lb.dns_name
}

# Output the Security Group ID for the orders Service
output "orders_security_group_id" {
  description = "The Security Group ID for the orders Service"
  value       = aws_security_group.orders_sg.id
}

# Output the orders Service Database Endpoint
output "orders_db_endpoint" {
  description = "The endpoint of the orders Service Database"
  value       = aws_db_instance.orders_db.endpoint
}

# Output the RDS Database Name
output "orders_db_name" {
  description = "The name of the orders Service Database"
  value       = aws_db_instance.orders_db.db_name
}

# Output the orders Service Launch Template ID
output "orders_launch_template_id" {
  description = "The ID of the Launch Template for the orders Service"
  value       = aws_launch_template.orders_lt.id
}
