PORTS=(
    35555 35556 35557 35558 35559
    )

IPS=(
    191.252.60.243 191.252.60.244 191.252.60.246 191.252.60.247 191.252.60.248
    )

NAMES=(
    "Túnel 1" "Túnel 2" "Túnel 3" "Túnel 4" "Túnel 5"
    )


for i in "${!PORTS[@]}"; do
    PORT=${PORTS[$i]}
    IP=${IPS[$i]}

    echo "Criando túnel na porta $PORT para $IP..."

    ssh -D $PORT -N -q -f root@$IP

    if [ $? -eq 0 ]; then
        echo "Túnel para $IP na porta $PORT criado com sucesso!"
    else
        echo "Falha ao criar túnel para $IP na porta $PORT."
    fi
done

echo "Todos os 15 tuneis foram criados"

echo "Lista de Túneis SSH Ativos:"
echo "--------------------------------------------"
INDEX=0
ps aux | grep "[s]sh" | grep -v "grep" | while read -r PID TTY TIME CMD; do

    # TUNNEL_TIME=$(ps -p $PID lstart=)
    echo "PID $PID | Nome: ${NAMES[$INDEX]} | IP: ${IPS[$INDEX]} | Porta: ${PORTS[$INDEX]}"
    INDEX=$((INDEX+1))
done

echo "--------------------------------------------"


# COMANDOS PARA FECHAR TODOS OS TUNEIS DE UMA SÓ VEZ
# ps aux | grep ssh | awk '{print $1}' | xargs kill -9 