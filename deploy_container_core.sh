#!/bin/bash

# Nome dinâmico com timestamp para evitar conflitos de DNS
DNS_LABEL="dan-core-$(date +%s)"

az container create \
  --resource-group rg-dan-creditado \
  --name container-core-dan \
  --image carlosmb2023/dan-core:latest \
  --cpu 2 \
  --memory 6 \
  --ports 10000 \
  --dns-name-label $DNS_LABEL \
  --environment-variables PORT=10000 \
  --restart-policy OnFailure

echo "✅ Container criado com DNS público:"
echo "http://$DNS_LABEL.eastus.azurecontainer.io:10000"
