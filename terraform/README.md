# Terraform AWS Basic Example

This example demonstrates how to use Terraform to provision basic AWS resources:
- VPC
- Subnet
- Security Group
- EC2 Instance
- S3 Bucket

## Prerequisites
- [Terraform](https://www.terraform.io/downloads.html) installed
- AWS account and credentials configured (via environment variables, `~/.aws/credentials`, or similar)

## Usage

1. **Initialize Terraform**
   ```sh
   terraform init
   ```

2. **Review the execution plan**
   ```sh
   terraform plan
   ```

3. **Apply the configuration**
   ```sh
   terraform apply
   ```
   Confirm with `yes` when prompted.

4. **View Outputs**
   After apply, Terraform will output the VPC ID, subnet ID, EC2 instance public IP, and S3 bucket name.

## Customization
You can override default variables by editing `variables.tf` or using `-var` flags, e.g.:
```sh
terraform apply -var="region=us-west-2" -var="instance_type=t3.micro"
```

## Cleanup
To destroy all resources created by this example:
```sh
terraform destroy
``` 