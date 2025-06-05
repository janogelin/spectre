output "vpc_id" {
  value = aws_vpc.example.id
}

output "subnet_id" {
  value = aws_subnet.example.id
}

output "instance_public_ip" {
  value = aws_instance.example.public_ip
}

output "s3_bucket_name" {
  value = aws_s3_bucket.example.bucket
}

output "elb_dns_name" {
  value = aws_elb.example.dns_name
  description = "The DNS name of the example ELB."
} 