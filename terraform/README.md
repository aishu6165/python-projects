# Terraform AWS Infrastructure Setup

This repository contains Terraform configurations to set up an AWS infrastructure for products, orders & inventory microservices. The setup includes creating a VPC, subnets, ECR repositories, Redis cluster, an internet gateway,Route53 and other required services.Follow the instructions below to configure and manage the infrastructure.

## Prerequisites

1. **AWS Account**: Ensure you have access to an AWS account with sufficient permissions to create the resources mentioned.
2. **Terraform Installed**: Make sure you have Terraform installed on your machine.
3. **S3 Bucket**: An S3 bucket must be created beforehand to store the Terraform state files. This can be done via the AWS Management Console or using the AWS CLI.
4. (Optional) DynamoDB Table: You can create a DynamoDB table for state locking. While this is not required, it is recommended for collaboration to prevent concurrent state modifications.

# Infrastructure Setup

1. Configure Common Infrastructure
- Its better to create the common infra before hand so that we won't run in to any chicken-and-egg issues.
- Run Terraform Commands: Initialize Terraform and apply the common-infra module:
  "terraform init"
  "terraform plan -target=module.common_infra"
  "terraform apply -target=module.common_infra --auto-approve"
- This will create the following resources:
. VPC
. Subnets
. ECR Repositories
. Redis
. Internet Gateway
. Route53

2. Build Docker Images
Once the common infrastructure is successfully created, you will need to build and push your Docker images for the products, orders, and inventory microservices to their respective ECR repositories.

Build Docker Images: 
Navigate to each microservice directory and build the images.

products-service:
    Authenticate with ecr using "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 051826737447.dkr.ecr.us-east-1.amazonaws.com"
    - cd products
    - docker build -t products-repo .  (build docker image)
    - docker tag products-repo:latest 051826737447.dkr.ecr.us-east-1.amazonaws.com/products-repo:latest
    - docker push 051826737447.dkr.ecr.us-east-1.amazonaws.com/products-repo:latest (pushing docker image to ecr)
    Repeat the process for orders & inventory microservices as well.
3. Deploy Products, Orders and Inventory Modules:
From the root folder run below commands to install Infra for microservices:
  "terraform init"
  "terraform plan"
  "terraform apply --auto-approve"
- This will create the following resources for each microservice:
. Launch Template
. Auto scaling groups
. Security groups
. RDS instance
. Also runs a script to deploy and run microservices by pulling the images from repos which are discussed above.

- To terminate the infrastructure run the following command:
  "terraform destroy"

# Note: This terraform code has been tested to deploy in AWS. You can follow this document to have every service deployed

