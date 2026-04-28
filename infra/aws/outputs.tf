output "alb_url" {
  description = "Public URL of the FruitAPI Application Load Balancer"
  value       = "http://${aws_lb.main.dns_name}"
}

output "rds_endpoint" {
  description = "RDS MySQL endpoint (host:port)"
  value       = "${aws_db_instance.mysql.address}:${aws_db_instance.mysql.port}"
}

output "secret_arn" {
  description = "ARN of the Secrets Manager secret holding DB credentials"
  value       = aws_secretsmanager_secret.db.arn
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.main.name
}

output "log_group" {
  description = "CloudWatch Logs group for the ECS task"
  value       = aws_cloudwatch_log_group.fruitapi.name
}
