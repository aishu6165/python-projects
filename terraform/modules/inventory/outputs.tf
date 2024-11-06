# Output the Load Balancer DNS name for the Inventory Service
output "inventory_lb_dns" {
  description = "The DNS name of the Inventory Service Load Balancer"
  value       = aws_lb.inventory_lb.dns_name
}

# Output the Security Group ID for the Inventory Service
output "inventory_sg_id" {
  description = "The Security Group ID for the Inventory Service"
  value       = aws_security_group.inventory_sg.id
}

# Output the Inventory Service Database Endpoint
output "inventory_db_endpoint" {
  description = "The endpoint of the Inventory Service Database"
  value       = aws_db_instance.inventory_db.endpoint
}

# Output the RDS Database Name
output "inventory_db_name" {
  description = "The name of the Inventory Service Database"
  value       = aws_db_instance.inventory_db.db_name
}

# Output the Inventory Service Launch Template ID
output "inventory_launch_template_id" {
  description = "The ID of the Launch Template for Inventory Service"
  value       = aws_launch_template.inventory_lt.id
}
