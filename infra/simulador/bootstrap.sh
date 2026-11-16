#!/usr/bin/env bash
# infra/simulador/bootstrap.sh
# Levanta el simulador MiniStack y crea lo que en AWS Academy ya existe o se crea
# a mano: el bucket del estado de Terraform (con versionado) y el rol LabRole.
# La VPC por defecto y sus subredes ya vienen en el simulador.
# Es idempotente: se puede ejecutar varias veces.
set -euo pipefail

export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-test}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-test}"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
ENDPOINT="${AWS_ENDPOINT:-http://localhost:4566}"
BUCKET="tfstate-calculadora-jero98772"
IMAGE="ministackorg/ministack:1.5.41"
aws_sim() { aws --endpoint-url "$ENDPOINT" "$@"; }

# Simulador local de AWS (MiniStack). Las tareas de ECS corren como contenedores
# Docker reales (por eso se monta el socket de Docker) y el ALB enruta en
# http://localhost:4566/_alb/<nombre-alb>/. El volumen conserva el estado.
if [ -z "$(docker ps -q --filter name=^ministack$)" ]; then
  docker rm -f ministack > /dev/null 2>&1 || true
  docker run -d --name ministack --restart unless-stopped \
    -p 127.0.0.1:4566:4566 \
    -e PERSIST_STATE=1 -e STATE_DIR=/data/state \
    -e S3_PERSIST=1 -e S3_DATA_DIR=/data/s3 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v ministack-data:/data \
    "$IMAGE" > /dev/null
fi
echo "Esperando a MiniStack en $ENDPOINT..."
timeout 120 bash -c "until curl -sf $ENDPOINT/_ministack/health > /dev/null; do sleep 2; done"

if ! aws_sim s3api head-bucket --bucket "$BUCKET" 2> /dev/null; then
  aws_sim s3api create-bucket --bucket "$BUCKET" > /dev/null
fi
aws_sim s3api put-bucket-versioning --bucket "$BUCKET" \
  --versioning-configuration Status=Enabled

if ! aws_sim iam get-role --role-name LabRole > /dev/null 2>&1; then
  aws_sim iam create-role --role-name LabRole \
    --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ecs-tasks.amazonaws.com"},"Action":"sts:AssumeRole"}]}' \
    > /dev/null
fi

echo "Simulador listo: bucket $BUCKET y rol LabRole disponibles."
