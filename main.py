# main.py
# Ponto de entrada da Fenix Execution Engine

import os
import sqlite3
import time

# CORREÇÃO APLICADA AQUI: AlgoritmoOtimo foi renomeado para AlgoritmoCIO
from fi_knowledge_base import AlgoritmoCIO, BancoAlgoritmosOtimos
from fi_runtime_core import FenixExecutionEngine
from fi_transmuter_ia import Transmutar_Codigo
from fi_scheduling_sai import CamadaAbstracaoHeterogenea

def main():
    print("Iniciando a Fenix Execution Engine...")
    
    # 1. Inicialização da Engine
    engine_fenix = FenixExecutionEngine(hardware_profile="AndroidTermux")
    
    # Exibe o estado inicial do MCA e BAO (para contexto)
    print(f"Engine Fênix inicializada. BAO carregado.")
    print(engine_fenix.MCA)
    
    # 2. Simular Transmutação de Código Bruto (MAI)
    print("\n---------------------------------------------------")
    print("SIMULANDO: Transmutar Código Bruto (Estado Inicial)")
    print("---------------------------------------------------")
    
    # O MAI gera uma lista de CIOs a serem agendados
    blocos_cio_para_agendar = Transmutar_Codigo("código_legado_com_O(n^2)_e_IO", engine_fenix)
    
    # 3. Execução e Agendamento (SAI/CAH)
    print("\n---------------------------------------------------")
    print("SIMULANDO: Agendamento e Execução (CAH Microsserviço Rust)")
    print("---------------------------------------------------")

    # Mostra o custo antes da execução (irá usar o custo persistido pelo PGO anterior)
    custo_inicial_qs = engine_fenix.BAO.get_custo_cpu("CIO_2_QuickSort_P")
    print(f"[Verificação Inicial]: Custo CPU do QuickSort ANTES do PGO: {custo_inicial_qs:.2f}")

    engine_fenix.Agendar_Tarefas(blocos_cio_para_agendar)
    
    # Simula o fim da execução assíncrona
    print("--- CAH: Execução Assíncrona Rust/GPU Despachada com Sucesso. ---")

    # 4. Auto-Reflexão e PGO (MARI/MTA)
    engine_fenix.Auto_Reflexao_E_PGO()
    
    # 5. Verificação Final (Conhecimento Otimizado)
    custo_final_qs = engine_fenix.BAO.get_custo_cpu("CIO_2_QuickSort_P")
    print(f"[Verificação Final]: Custo CPU do QuickSort DEPOIS do PGO: {custo_final_qs:.2f}")
    
    if custo_final_qs < custo_inicial_qs:
        print("\n[MTA-PGO SUCESSO]: O Motor Fênix aprendeu! O custo do QuickSort foi reduzido.")
    else:
        print("\n[MTA-PGO AVISO]: O custo do QuickSort não foi reduzido (já está otimizado ou não há dados).")

    # 6. Sumário do Estado Final
    print("\n---------------------------------------------------")
    print("RESULTADO FINAL DA TRANSMUTAÇÃO:")
    for bloco in blocos_cio_para_agendar:
        # Pega a informação do BAO para ter o custo atualizado
        custo = engine_fenix.BAO.get_custo_cpu(bloco.ID)
        print(f"- CIO Bloco: {bloco.nome} (Custo Final CPU: {custo:.2f})")
    print("---------------------------------------------------")
    
if __name__ == "__main__":
    main()

