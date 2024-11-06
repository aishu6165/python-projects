# Security Group for Inventory Service
resource "aws_security_group" "inventory_sg" {
  name   = "${var.service_name}-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_subnet_group" "inventory_db_subnet_group" {
  name       = "${var.service_name}-db-subnet-group"
  subnet_ids = var.subnets  # Use the subnets variable that you defined for your VPC

  tags = {
    Name = "${var.service_name}-db-subnet-group"
  }
}

data "template_file" "user_data" {
  template = file("./modules/inventory/user_data.yaml")
  vars = {
    redis_url = var.redis_url
    db_host   = aws_db_instance.inventory_db.address
    ecr_url   = var.ecr_url
  }
}
# Launch Template for Inventory Service
resource "aws_launch_template" "inventory_lt" {
  name_prefix   = "${var.service_name}-lt"
  image_id      = "ami-005fc0f236362e99f"
  instance_type = "t2.micro"
  user_data = base64encode(data.template_file.user_data.rendered)
}

# Auto Scaling Group for Inventory Service
resource "aws_autoscaling_group" "inventory_asg" {
  desired_capacity     = 1
  max_size             = 2
  min_size             = 1
  vpc_zone_identifier  = var.subnets

  launch_template {
    id      = aws_launch_template.inventory_lt.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.service_name}-asg"
    propagate_at_launch = true
  }
}

# Load Balancer for Inventory Service
resource "aws_lb" "inventory_lb" {
  name               = "${var.service_name}-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.inventory_sg.id]
  subnets            = var.subnets
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.inventory_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.inventory_tg.arn
  }
}

resource "aws_lb_target_group" "inventory_tg" {
  name     = "${var.service_name}-tg"
  port     = 5006
  protocol = "HTTP"
  vpc_id   = var.vpc_id
}

# RDS Database for Inventory Service
resource "aws_db_instance" "inventory_db" {
  identifier              = "${var.service_name}-db"
  engine                  = "postgres"
  engine_version          = "11"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  db_name                 = "${var.service_name}_db"
  username                = "inventory"
  password                = var.db_password
  vpc_security_group_ids  = [aws_security_group.inventory_sg.id]
  db_subnet_group_name    = aws_db_subnet_group.inventory_db_subnet_group.name
  skip_final_snapshot     = true
  publicly_accessible     = false
  backup_retention_period = 7
}
