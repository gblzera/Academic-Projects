#include <iostream>
#include <fstream>
#include <queue>
#include <vector>
#include <unordered_map>
#include <bitset>
#include <algorithm>
#include <string>
using namespace std;

// Estrutura para representar nós da árvore de Huffman
struct HuffmanNode {
    unsigned char data;
    unsigned frequency;
    HuffmanNode* left;
    HuffmanNode* right;
    
    HuffmanNode(unsigned char data, unsigned frequency) : 
        data(data), frequency(frequency), left(nullptr), right(nullptr) {}
    
    ~HuffmanNode() {
        delete left;
        delete right;
    }
};

// Comparador para a fila de prioridade (min heap)
struct Compare {
    bool operator()(HuffmanNode* a, HuffmanNode* b) {
        return a->frequency > b->frequency;
    }
};

// Classe principal do compressor
class HuffmanCompressor {
private:
    unordered_map<unsigned char, string> huffmanCodes;
    HuffmanNode* root;
    
    // Calcula a frequência de cada byte no arquivo
    unordered_map<unsigned char, unsigned> calculateFrequencies(const string& filename) {
        unordered_map<unsigned char, unsigned> frequencies;
        ifstream file(filename, ios::binary);
        
        if (!file) {
            throw runtime_error("Não foi possível abrir o arquivo: " + filename);
        }
        
        unsigned char byte;
        while (file.read(reinterpret_cast<char*>(&byte), sizeof(byte))) {
            frequencies[byte]++;
        }
        
        file.close();
        return frequencies;
    }
    
    // Constrói a árvore de Huffman a partir das frequências
    HuffmanNode* buildHuffmanTree(const unordered_map<unsigned char, unsigned>& frequencies) {
        priority_queue<HuffmanNode*, vector<HuffmanNode*>, Compare> minHeap;
        
        // Criação dos nós folha
        for (const auto& pair : frequencies) {
            minHeap.push(new HuffmanNode(pair.first, pair.second));
        }
        
        // Caso especial: arquivo com apenas um tipo de byte
        if (minHeap.size() == 1) {
            HuffmanNode* singleNode = minHeap.top();
            minHeap.pop();
            HuffmanNode* newRoot = new HuffmanNode('\0', singleNode->frequency);
            newRoot->left = singleNode;
            minHeap.push(newRoot);
        }
        
        // Construção da árvore
        while (minHeap.size() > 1) {
            HuffmanNode* left = minHeap.top();
            minHeap.pop();
            
            HuffmanNode* right = minHeap.top();
            minHeap.pop();
            
            HuffmanNode* internalNode = new HuffmanNode('\0', left->frequency + right->frequency);
            internalNode->left = left;
            internalNode->right = right;
            
            minHeap.push(internalNode);
        }
        
        return minHeap.top();
    }
    
    // Gera códigos de Huffman recursivamente a partir da árvore
    void generateCodes(HuffmanNode* node, const string& code) {
        if (!node) return;
        
        // Nó folha
        if (!node->left && !node->right) {
            huffmanCodes[node->data] = code;
        }
        
        // Recursão para subárvores
        generateCodes(node->left, code + "0");
        generateCodes(node->right, code + "1");
    }
    
    // Serializa a árvore de Huffman para armazenar no arquivo comprimido
    void serializeTree(HuffmanNode* node, ofstream& outFile) {
        if (!node) return;
        
        // Indica se é nó interno (0) ou folha (1)
        bool isLeaf = (!node->left && !node->right);
        outFile.write(reinterpret_cast<const char*>(&isLeaf), sizeof(bool));
        
        // Se for folha, escreve o byte
        if (isLeaf) {
            outFile.write(reinterpret_cast<const char*>(&node->data), sizeof(unsigned char));
        }
        
        // Recursão para subárvores
        serializeTree(node->left, outFile);
        serializeTree(node->right, outFile);
    }
    
    // Deserializa a árvore de Huffman do arquivo comprimido
    HuffmanNode* deserializeTree(ifstream& inFile) {
        bool isLeaf;
        inFile.read(reinterpret_cast<char*>(&isLeaf), sizeof(bool));
        
        if (isLeaf) {
            unsigned char data;
            inFile.read(reinterpret_cast<char*>(&data), sizeof(unsigned char));
            return new HuffmanNode(data, 0);
        }
        
        HuffmanNode* node = new HuffmanNode('\0', 0);
        node->left = deserializeTree(inFile);
        node->right = deserializeTree(inFile);
        return node;
    }
    
public:
    HuffmanCompressor() : root(nullptr) {}
    
    ~HuffmanCompressor() {
        delete root;
    }
    
    // Comprime um arquivo
    void compress(const string& inputFile, const string& outputFile) {
        // Calcula frequências
        unordered_map<unsigned char, unsigned> frequencies = calculateFrequencies(inputFile);
        if (frequencies.empty()) {
            throw runtime_error("Arquivo vazio ou não encontrado: " + inputFile);
        }
        
        // Constrói árvore de Huffman
        root = buildHuffmanTree(frequencies);
        
        // Gera códigos para cada byte
        huffmanCodes.clear();
        generateCodes(root, "");
        
        // Abre arquivos
        ifstream inFile(inputFile, ios::binary);
        ofstream outFile(outputFile, ios::binary);
        
        if (!inFile || !outFile) {
            throw runtime_error("Erro ao abrir arquivos");
        }
        
        // Escreve o tamanho original do arquivo
        inFile.seekg(0, ios::end);
        size_t fileSize = inFile.tellg();
        inFile.seekg(0, ios::beg);
        outFile.write(reinterpret_cast<const char*>(&fileSize), sizeof(fileSize));
        
        // Serializa a árvore
        serializeTree(root, outFile);
        
        // Comprime os dados
        unsigned char currentByte = 0;
        int bitCount = 0;
        
        unsigned char byte;
        while (inFile.read(reinterpret_cast<char*>(&byte), sizeof(byte))) {
            string code = huffmanCodes[byte];
            
            for (char bit : code) {
                if (bit == '1') {
                    currentByte |= (1 << (7 - bitCount));
                }
                
                bitCount++;
                
                if (bitCount == 8) {
                    outFile.write(reinterpret_cast<const char*>(&currentByte), sizeof(currentByte));
                    currentByte = 0;
                    bitCount = 0;
                }
            }
        }
        
        // Escreve o último byte (parcial)
        if (bitCount > 0) {
            outFile.write(reinterpret_cast<const char*>(&currentByte), sizeof(currentByte));
        }
        
        // Fecha arquivos
        inFile.close();
        outFile.close();
        
        // Exibe estatísticas
        ifstream compressedFile(outputFile, ios::binary | ios::ate);
        size_t compressedSize = compressedFile.tellg();
        compressedFile.close();
        
        cout << "Arquivo original: " << fileSize << " bytes" << endl;
        cout << "Arquivo comprimido: " << compressedSize << " bytes" << endl;
        cout << "Taxa de compressão: " << (1.0 - static_cast<double>(compressedSize) / fileSize) * 100 << "%" << endl;
    }
    
    // Descomprime um arquivo
    void decompress(const string& inputFile, const string& outputFile) {
        ifstream inFile(inputFile, ios::binary);
        ofstream outFile(outputFile, ios::binary);
        
        if (!inFile || !outFile) {
            throw runtime_error("Erro ao abrir arquivos");
        }
        
        // Lê o tamanho original do arquivo
        size_t originalSize;
        inFile.read(reinterpret_cast<char*>(&originalSize), sizeof(originalSize));
        
        // Deserializa a árvore
        root = deserializeTree(inFile);
        
        // Descomprime os dados
        size_t bytesWritten = 0;
        HuffmanNode* current = root;
        
        unsigned char byte;
        while (inFile.read(reinterpret_cast<char*>(&byte), sizeof(byte)) && bytesWritten < originalSize) {
            for (int i = 0; i < 8 && bytesWritten < originalSize; ++i) {
                bool bit = (byte & (1 << (7 - i)));
                
                if (bit) {
                    current = current->right;
                } else {
                    current = current->left;
                }
                
                // Chegou em um nó folha
                if (!current->left && !current->right) {
                    outFile.write(reinterpret_cast<const char*>(&current->data), sizeof(current->data));
                    bytesWritten++;
                    current = root;
                }
            }
        }
        
        // Fecha arquivos
        inFile.close();
        outFile.close();
    }
};

int main(int argc, char* argv[]) {
    try {
        if (argc != 4) {
            cout << "Uso: huffman <modo> <arquivo_entrada> <arquivo_saida>" << endl;
            cout << "onde <modo> é 'c' para comprimir ou 'd' para descomprimir" << endl;
            return 1;
        }
        
        string mode = argv[1];
        string inputFile = argv[2];
        string outputFile = argv[3];
        
        HuffmanCompressor compressor;
        
        if (mode == "c") {
            cout << "Comprimindo " << inputFile << " para " << outputFile << "..." << endl;
            compressor.compress(inputFile, outputFile);
            cout << "Compressão concluída." << endl;
        } else if (mode == "d") {
            cout << "Descomprimindo " << inputFile << " para " << outputFile << "..." << endl;
            compressor.decompress(inputFile, outputFile);
            cout << "Descompressão concluída." << endl;
        } else {
            cout << "Modo inválido. Use 'c' para comprimir ou 'd' para descomprimir." << endl;
            return 1;
        }
    } catch (const exception& e) {
        cerr << "Erro: " << e.what() << endl;
        return 1;
    }
    
    return 0;
}