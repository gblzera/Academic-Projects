#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NUM_PRISIONEIROS 100
#define TENTATIVAS 50

// Função para embaralhar um array (Algoritmo de Fisher-Yates)
void embaralhar(int caixas[], int n) {
    for (int i = n - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        int temp = caixas[i];
        caixas[i] = caixas[j];
        caixas[j] = temp;
    }
}

// Simula a estratégia ótima para um prisioneiro específico
int prisioneiro_sobrevive(int prisioneiro, int caixas[]) {
    int proxima_caixa = prisioneiro;
    
    for (int i = 0; i < TENTATIVAS; i++) {
        if (caixas[proxima_caixa] == prisioneiro) {
            return 1; // Sobreviveu
        }
        proxima_caixa = caixas[proxima_caixa]; // Seguir o ciclo
    }

    return 0; // Morreu
}

// Simulação completa
int simulacao() {
    int caixas[NUM_PRISIONEIROS];

    // Preencher as caixas com números de 0 a 99 (pois usamos índice 0-based)
    for (int i = 0; i < NUM_PRISIONEIROS; i++) {
        caixas[i] = i;
    }

    // Embaralhar os números dentro das caixas
    embaralhar(caixas, NUM_PRISIONEIROS);

    // Testar todos os prisioneiros
    for (int i = 0; i < NUM_PRISIONEIROS; i++) {
        if (!prisioneiro_sobrevive(i, caixas)) {
            return 0; // Se um falhar, todos morrem
        }
    }

    return 1; // Todos sobreviveram
}

int main() {
    srand(time(NULL));

    int rodadas = 10000; // Quantidade de testes
    int sucesso = 0;

    for (int i = 0; i < rodadas; i++) {
        if (simulacao()) {
            sucesso++;
        }
    }

    printf("Taxa de sucesso: %.2f%%\n", (sucesso / (double) rodadas) * 100);
    
    return 0;
}
