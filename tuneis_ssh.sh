PORTS=(
    34567 34568 34569 34570 34571 35000 35001 35002 35003 35004 \
    35555 35556 35557 35558 35559 35560 35561 35562 35563 35564 \
    35565 35566 35567 35568 35569 35570 35571 35572 35573 35574 
    )

IPS=(
    191.252.196.233 191.252.179.221 191.252.220.28 191.252.221.161 191.252.5.247 191.252.60.237 \
    191.252.60.238 191.252.60.239 191.252.60.240 191.252.60.241 191.252.60.243 191.252.60.244 \
    191.252.60.246 191.252.60.247 191.252.60.248 191.252.60.249 191.252.60.250 191.252.60.253 191.252.60.254 \
    191.252.93.2 191.252.93.3 191.252.93.4 191.252.93.5 191.252.93.6 191.252.93.7 191.252.93.8 191.252.93.10 \
    191.252.93.11 191.252.93.12 191.252.93.13
     )

NAMES=(
    "Túnel 1" "Túnel 2" "Túnel 3" "Túnel 4" "Túnel 5" "Túnel 6" \
    "Túnel 7" "Túnel 8" "Túnel 9" "Túnel 10" "Túnel 11" "Túnel 12" \
    "Túnel 13" "Túnel 14" "Túnel 15" "Túnel 16" "Túnel 17" "Túnel 18" \
    "Túnel 19" "Túnel 20" "Túnel 21" "Túnel 22" "Túnel 23" "Túnel 24" \
    "Túnel 25" "Túnel 26" "Túnel 27" "Túnel 28" "Túnel 29" "Túnel 30" 
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