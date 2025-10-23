# fi_scheduling_sai.py
# Módulo de Agendamento Inteligente (SAI) e Abstração de Hardware (CAH)

# Importação para execução real via subprocesso (Rust)
from multiprocessing import Pool
# Importação CORRIGIDA: MCA está agora no módulo de perfilamento
from fi_profile_hardware import ModeloCustoAbstrato 
import time
import os
import subprocess 

# Classe de recurso mantida
class UnidadeRecurso:
    """Representa uma unidade de recurso (Core, GPU, etc.) com seu custo real."""
    def __init__(self, nome, tipo, fator_velocidade, custo_por_ciclo):
        self.nome = nome
        self.tipo = tipo
        self.fator_velocidade = fator_velocidade
        self.custo_por_ciclo = custo_por_ciclo
        self.carga_atual = 0 
        self.pool = None
        self.processos_ativos = 0

    def __str__(self):
        return f"Recurso({self.nome}, Tipo:{self.tipo}, Carga:{self.carga_atual}%)"

class CamadaAbstracaoHeterogenea:
    """
    CAH (Camada de Abstração Heterogênea). 
    Gerencia o pool de recursos físicos (UHE) e DESPACHA o trabalho.
    """
    @staticmethod
    def Gerar_Pool_Recursos(GPU, CPU_cores, MCA):
        pool = []
        fator_cpu_calibrado = MCA.fator_cpu_core

        # Recurso CPU: Gerencia a execução dos Microsserviços Rust
        # O número de tarefas paralelas reflete o fator calibrado do MCA.
        num_processos = max(1, int(fator_cpu_calibrado)) 
        cpu_pool_recurso = UnidadeRecurso(
            nome="CPU_Rust_Pool", 
            tipo="CPU", 
            fator_velocidade=1.0 * num_processos, 
            custo_por_ciclo=0.01
        )
        # Mantemos o objeto para compatibilidade de contagem
        cpu_pool_recurso.pool = object() 
        pool.append(cpu_pool_recurso)

        if GPU:
            # Recurso de GPU (simulado)
            pool.append(UnidadeRecurso(
                nome="GPU_Unica", 
                tipo="GPU", 
                fator_velocidade=fator_cpu_calibrado * 2, 
                custo_por_ciclo=0.05 
            ))

        print(f"  [CAH Real]: Pool UHE gerado. CPU_Rust_Pool pronto para {num_processos} tarefas paralelas.")
        return pool

    @staticmethod
    def Executar_Bloco(bloco, recurso_otimo):
        """Despacha o bloco de cálculo para o binário Rust ou simula GPU."""

        # O tempo simulado é o argumento passado para o microsserviço Rust (Rust simula o tempo de execução)
        tempo_simulado = bloco.custo_cpu / recurso_otimo.fator_velocidade / 10 

        if recurso_otimo.tipo == "CPU":
            # --- Execução via Binário Rust (Assíncrono) ---
            caminho_binario = './fi_micros_cah'

            # Chamamos o microsserviço Rust em background (fire-and-forget)
            subprocess.Popen([caminho_binario, str(tempo_simulado)], 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE)

            print(f"     > CAH: Bloco {bloco.ID} DESPACHADO para {recurso_otimo.nome} (Binário Rust) por {tempo_simulado:.2f}s.")
        else:
            # Simulação de execução em GPU
            print(f"     > CAH: Bloco {bloco.ID} DESPACHADO para {recurso_otimo.nome} (Simulação GPU).")

    @staticmethod
    def Callback_Execucao(resultado):
        # Não é mais usado, mas mantido para evitar erros
        pass

class ServicoAgendamentoInteligente:
    """
    SAI (Serviço de Agendamento Inteligente). 
    Aplica a lógica de decisão otimizada.
    """
    @staticmethod
    def Escolher_Recurso(bloco_cio, recursos_uhe, mca: ModeloCustoAbstrato):
        recurso_escolhido = None
        melhor_custo_estimado = float('inf')

        for recurso in recursos_uhe:
            # O Custo é inversamente proporcional à velocidade do recurso
            custo_estimado = (bloco_cio.custo_cpu / recurso.fator_velocidade) * mca.fator_cpu_core

            # Penalidade de Carga 
            if recurso.tipo == "CPU":
                custo_estimado += recurso.processos_ativos * 5 

            if custo_estimado < melhor_custo_estimado:
                melhor_custo_estimado = custo_estimado
                recurso_escolhido = recurso

        # Simula a ocupação
        if recurso_escolhido.tipo == "CPU":
            recurso_escolhido.processos_ativos += 1

        # CORREÇÃO APLICADA: recurso_escolhidos -> recurso_escolhido
        print(f"  [SAI]: Escolhido {recurso_escolhido.nome} (Custo Est.: {melhor_custo_estimado:.2f}, Pool: {recurso_escolhido.processos_ativos} atv.)")
        return recurso_escolhido

