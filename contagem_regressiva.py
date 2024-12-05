import time

def contagem_regressiva(n, callback):
    """
    Função para realizar a contagem regressiva para o Ano Novo.

    Parâmetros:
        n (int): Número de segundos até o Ano Novo (1 <= n <= 60).
        callback (function): Função a ser chamada a cada segundo com o valor atual.
    """
    if not (1 <= n <= 60):
        raise ValueError("O número deve estar entre 1 e 60.")
    
    for i in range(n, 0, -1):
        callback(i)  # Atualiza o valor atual na interface
        time.sleep(1)
    callback("🎉 Feliz Ano Novo!")  # Mensagem final
