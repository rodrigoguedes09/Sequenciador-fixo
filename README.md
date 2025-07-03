# Relatório do Projeto: Implementação de Sequenciador Fixo em Sistemas Distribuídos

## Visão Geral
Este projeto implementa um sequenciador fixo para sistemas distribuídos, demonstrando conceitos fundamentais como:
- Sincronização de processos
- Ordenação total de mensagens
- Comunicação cliente-servidor
- Exclusão mútua

## Tecnologias Utilizadas
- **Linguagem**: Python 3.x
- **Bibliotecas**:
  - `socket` para comunicação de rede
  - `threading` para concorrência
  - `tkinter` para interface gráfica
- **Protocolo**: TCP/IP

## Como Executar

### Pré-requisitos
- Python 3.x instalado
- Acesso a porta 5000 no localhost

### Instalação
```bash
git clone https://github.com/seu-usuario/sistemas-distribuidos-sequenciador.git
cd sistemas-distribuidos-sequenciador
```

### Execução
1. **Iniciar o Servidor Sequenciador**:
   ```bash
   python sequenciador.py
   ```
   (Ou clique no botão "Iniciar Servidor" na interface gráfica)

2. **Executar Clientes**:
   ```bash
   python sequenciador.py
   ```
   (Execute múltiplas instâncias para simular vários clientes)

## Interface Gráfica
A aplicação possui uma interface com:
- Área de mensagens recebidas (com números de sequência)
- Campo para envio de mensagens
- Controles de conexão/desconexão
- Botão para iniciar/parar o servidor

## Funcionamento do Algoritmo

### Lógica do Sequenciador
1. Recebe mensagens de múltiplos clientes
2. Atribui um número de sequência único a cada mensagem
3. Retransmite as mensagens para todos os clientes na ordem sequencial

### Mecanismos de Controle
- **Exclusão Mútua**: Uso de `threading.Lock()` para proteger:
  - Contador de sequência
  - Lista de clientes conectados
- **Sincronização**: Threads separadas para:
  - Aceitar conexões
  - Receber mensagens
  - Processar/envia mensagens

## Requisitos Cumpridos
- [x] Comunicação cliente-servidor
- [x] Interface visual mostrando mensagens e ordem de transmissão
- [x] Implementação dos conceitos de sistemas distribuídos
- [x] Documentação completa do projeto

## Exemplo de Funcionamento
1. Cliente A envia "Olá"
2. Cliente B envia "Mundo"
3. Todos clientes recebem:
   ```
   [Seq 1] Olá
   [Seq 2] Mundo
   ```
4. A ordem é garantida mesmo que as mensagens cheguem em momentos diferentes
A imagem abaixo mostra como ficou a interface da aplicação com esse exemplo:
![image](https://github.com/user-attachments/assets/b9c4f1e7-1eae-4a15-9d9e-7664265939bb)


## Autores
[Rodrio Guedes, João Pedro Tavares] - Engenharia de Computação - [UFSC] - [2025]
