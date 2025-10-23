# fi_transmuter_ia.py
# Motor de Análise de Intenção (MAI) e Transmutador Fênix (Transmutar_Codigo)

from fi_runtime_core import FenixExecutionEngine
# CORREÇÃO APLICADA: Nome da classe renomeada de AlgoritmoOtimo para AlgoritmoCIO
from fi_knowledge_base import AlgoritmoCIO 
import time

def Transmutar_Codigo(codigo_bruto, engine: FenixExecutionEngine):
    """
    Simula a análise e transmutação do código legado em Blocos CIO (Instrução/Otimização).
    """
    blocos_cio_resultantes = []

    print("--- Início do Processo de Transmutação Fênix ---")
    print("1. MAI: Analisando intenção e gerando ADF.")

    # --- Simulação de Análise de Blocos ---

    # Bloco A: I/O Pesado (Lento)
    print("\n   - Processando: Seção A: I/O Pesado")

    # 1. Escolha de Algoritmo Otimizado pelo BAO
    # Simula a escolha de uma "Variante Min-IO" do BAO.
    algoritmo_io = engine.BAO.mapa_otimizacao.get("CIO_1_Min_IO")

    print(f"     > Refinando com {algoritmo_io.nome} (Custo {algoritmo_io.custo_io} alto).")

    # 2. Geração do CEO (Contrato de Execução Externa) para I/O
    ceo_contrato = "CEO Contrato: Chamada Externa de I/O"
    engine.Agendar_Tarefa_Compatibilidade(ceo_contrato)

    # 3. Agendamento do CEO na EAT (simulação)
    print(f"     > Agendado {ceo_contrato} via EAT/CAH.")

    # Bloco B: Cálculo O(n^2) (Substituído por QuickSort Paralelo)
    print("\n   - Processando: Seção B: Cálculo O(n^2)")

    # O resultado da transmutação é uma lista de objetos CIO com instruções de execução
    # CORREÇÃO APLICADA: Uso de AlgoritmoCIO em vez de AlgoritmoOtimo, com parâmetro 'tipo'
    return [
        # Bloco Legado (I/O, já processado acima)
        AlgoritmoCIO(nome="Algoritmo Legado (Min-IO)", custo_cpu=100, custo_io=5, tipo="IO_Bound"),

        # Bloco Otimizado (CPU) - Usará o custo atual do BAO (persistido pelo PGO)
        AlgoritmoCIO(nome="QuickSort Paralelo", custo_cpu=engine.BAO.get_custo_cpu("CIO_2_QuickSort_P"), custo_io=1, tipo="CPU_Bound")
    ]

