terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket-for-app-ecommerce"
    key            = "ecommerce.tfstate"
    region         = "us-east-1"
    encrypt        = true
  }
}
