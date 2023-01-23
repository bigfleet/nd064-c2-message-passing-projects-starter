kubectl apply -f deployment/

kubectl wait --for=condition=ready pod --selector=app=postgres --timeout=90s

# pod runs, give a second for listening
sleep 15

scripts/run_db_command.sh