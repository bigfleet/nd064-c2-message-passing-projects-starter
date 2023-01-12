kubectl apply -f deployment/

kubectl wait --for=condition=ready pod --selector=app=postgres --timeout=90s

scripts/run_db_command.sh