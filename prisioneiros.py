import random

NUM_PRISIONEIROS = 100
TENTATIVAS = 50
RODADAS = 10000  # Número de simulações

def embaralhar_caixas():
    """Cria uma lista de caixas embaralhadas"""
    caixas = list(range(NUM_PRISIONEIROS))
    random.shuffle(caixas)
    return caixas

def prisioneiro_sobrevive(prisioneiro, caixas):
    """Simula a tentativa de um único prisioneiro"""
    proxima_caixa = prisioneiro
    for _ in range(TENTATIVAS):
        if caixas[proxima_caixa] == prisioneiro:
            return True  # Sobreviveu
        proxima_caixa = caixas[proxima_caixa]  # Segue o ciclo
    return False  # Morreu

def simulacao():
    """Executa uma simulação completa"""
    caixas = embaralhar_caixas()
    return all(prisioneiro_sobrevive(i, caixas) for i in range(NUM_PRISIONEIROS))

# Simulações múltiplas
sucessos = sum(simulacao() for _ in range(RODADAS))

# Exibir a taxa de sucesso
print(f"Taxa de sucesso: {sucessos / RODADAS * 100:.2f}%")

#O diretor de uma prisão oferece a 100 prisioneiros condenados à morte, numerados de 1 a 100, uma última chance. 
#Uma sala contém um armário com 100 gavetas. O diretor coloca aleatoriamente o número de um prisioneiro em cada gaveta fechada.
#Os prisioneiros entram na sala, um após o outro. 
#Cada prisioneiro pode abrir e olhar em 50 gavetas em qualquer ordem.
#As gavetas são fechadas novamente depois.
#Se, durante essa busca, cada prisioneiro encontrar seu número em uma das gavetas, todos os prisioneiros são perdoados. 
#Se mesmo um prisioneiro não encontrar seu número, todos os prisioneiros morrem.
#Antes que o primeiro prisioneiro entre na sala, os prisioneiros podem discutir a estratégia — 
#mas não podem se comunicar quando o primeiro prisioneiro entra para olhar nas gavetas. 
#Qual é a melhor estratégia dos prisioneiros? 

#Se cada prisioneiro selecionar 50 gavetas de forma independente e aleatória , a probabilidade de que um único prisioneiro encontre seu número é de 50%. 
#A probabilidade de que todos os prisioneiros encontrem seus números é o produto das probabilidades individuais
#, que é ( ⁠1/2⁠ ) ​​100 ≈0,000 000 000 000 000 000 000 000 000 000 0008 , um número extremamente pequeno. A situação parece sem esperança.