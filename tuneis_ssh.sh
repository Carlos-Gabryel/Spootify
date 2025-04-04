PORTS=(34567 34568 34569 34570 34571 35000 35001 35002 35003 35004 35555 35556 35557 35558 35559)
IPS=(191.252.38.73 191.252.38.74 191.252.38.75 191.252.38.78 191.252.38.79 191.252.38.84 \
     191.252.38.86 191.252.38.88 191.252.38.93 191.252.38.91 191.252.38.92 191.252.38.100 \
     191.252.38.94 191.252.38.99 191.252.38.98)


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