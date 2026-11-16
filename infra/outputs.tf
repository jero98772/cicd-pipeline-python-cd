# infra/outputs.tf
output "alb_url" {
  description = "URL del Application Load Balancer (en el simulador MiniStack, la ruta /_alb/<nombre> enruta al ALB)"
  value       = var.aws_endpoint == null ? "http://${aws_lb.main.dns_name}" : "${var.aws_endpoint}/_alb/${aws_lb.main.name}"
}

output "ecs_cluster_name" {
  description = "Nombre del cluster ECS"
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "Nombre del servicio ECS"
  value       = aws_ecs_service.app.name
}
