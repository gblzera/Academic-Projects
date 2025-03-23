#include <stdio.h>

int josephus(int n, int k) {
    if (n == 1)
        return 0;
    return (josephus(n - 1, k) + k) % n;
}

int main() {
    int NC, n, k;
    scanf("%d", &NC);
 
    for(int i = 1; i<= NC; i++){
        scanf("%d %d", &n, &k);
        int result = josephus(n, k) + 1;
        printf("Case %d: %d\n", i, result);
    }

    return 0;
}