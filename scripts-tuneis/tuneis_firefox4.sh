PORTS=(
    35560 35561 35562 35563 35564
    )

IPS=(
    191.252.60.249 191.252.60.250 191.252.60.253 191.252.60.254 191.252.93.2
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