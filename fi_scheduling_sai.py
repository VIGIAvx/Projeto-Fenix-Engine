# fi_scheduling_sai.py
# Módulo de Agendamento Inteligente (SAI) e Abstração de Hardware (CAH)

# Importação para execução paralela real!
from multiprocessing import Pool
from fi_knowledge_base import ModeloCustoAbstrato
import time
import os

# Função externa para o Pool de processos (não pode ser um método de classe)
def simular_execucao_bloco(bloco_id, recurso_nome, tempo_simulado):
    """Simula o trabalho real do bloco de código em um processo separado."""
    pid = os.getpid()
    # print(f"        [CAH-Processo {pid}]: Bloco {bloco_id} INICIADO no {recurso_nome} por {tempo_simulado:.2f}s.")
    time.sleep(tempo_simulado) # Simula o tempo de trabalho
    # print(f"        [CAH-Processo {pid}]: Bloco {bloco_id} FINALIZADO.")
    return f"Bloco {bloco_id} concluído por PID {pid} em {recurso_nome}."


class UnidadeRecurso:
    """Representa uma unidade de recurso (Core, GPU, etc.) com seu custo real."""
    def __init__(self, nome, tipo, fator_velocidade, custo_por_ciclo):
        self.nome = nome
        self.tipo = tipo
        self.fator_velocidade = fator_velocidade
        self.custo_por_ciclo = custo_por_ciclo
        self.carga_atual = 0 
        self.pool = None # Pool de multiprocessamento para CPUs
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

        # Criamos um único recurso de CPU que gerencia um Pool de Threads/Processos
        num_processos = max(1, int(fator_cpu_calibrado)) 
        cpu_pool_recurso = UnidadeRecurso(
            nome="CPU_Pool", 
            tipo="CPU", 
            fator_velocidade=1.0 * num_processos, 
            custo_por_ciclo=0.01
        )
        # Inicializa o Pool de processos real
        cpu_pool_recurso.pool = Pool(processes=num_processos) 
        pool.append(cpu_pool_recurso)

        if GPU:
            # Recurso de GPU (simulado como thread/processo único)
            pool.append(UnidadeRecurso(
                nome="GPU_Unica", 
                tipo="GPU", 
                fator_velocidade=fator_cpu_calibrado * 2, 
                custo_por_ciclo=0.05 
            ))

        print(f"  [CAH Real]: Pool UHE gerado. CPU_Pool com {num_processos} processos.")
        return pool

    @staticmethod
    def Executar_Bloco(bloco, recurso_otimo):
        """Despacha o bloco de cálculo para o recurso escolhido (SAI)."""

        tempo_simulado = bloco.custo_cpu / recurso_otimo.fator_velocidade / 10 # Reduzimos o tempo para o teste ser rápido

        if recurso_otimo.tipo == "CPU":
            # Execução Paralela Real (Multiprocessing)
            # Usamos apply_async para não bloquear o Fenix Engine
            recurso_otimo.pool.apply_async(simular_execucao_bloco, 
                args=(bloco.ID, recurso_otimo.nome, tempo_simulado),
                callback=CamadaAbstracaoHeterogenea.Callback_Execucao # Chamada de retorno
            )
            print(f"     > CAH: Bloco {bloco.ID} DESPACHADO para {recurso_otimo.nome} (Multiprocessamento).")
        else:
            # Simulação de execução em GPU
            # Aqui você usaria CUDA/OpenCL (simulamos a execução em thread único)
            print(f"     > CAH: Bloco {bloco.ID} DESPACHADO para {recurso_otimo.nome} (Simulação GPU).")

    @staticmethod
    def Callback_Execucao(resultado):
        """Recebe o resultado do processo paralelo e imprime o status."""
        # print(f"     > CAH-Callback: {resultado}")
        pass

class ServicoAgendamentoInteligente:
    """
    SAI (Serviço de Agendamento Inteligente). 
    Aplica a lógica de decisão otimizada.
    """
    @staticmethod
    def Escolher_Recurso(bloco_cio, recursos_uhe, mca):
        recurso_escolhido = None
        melhor_custo_estimado = float('inf')

        for recurso in recursos_uhe:
            # O Custo é inversamente proporcional à velocidade do recurso
            custo_estimado = (bloco_cio.custo_cpu / recurso.fator_velocidade) * mca.fator_cpu_core

            # Penalidade de Carga: Se for o recurso de CPU (Pool), consideramos a carga
            if recurso.tipo == "CPU":
                custo_estimado += recurso.processos_ativos * 5 # Aumenta a penalidade de carga

            if custo_estimado < melhor_custo_estimado:
                melhor_custo_estimado = custo_estimado
                recurso_escolhido = recurso

        # Simula a ocupação: Se for CPU, aumenta a contagem de processos ativos no pool
        if recurso_escolhido.tipo == "CPU":
            recurso_escolhido.processos_ativos += 1

        print(f"  [SAI]: Escolhido {recurso_escolhido.nome} (Custo Est.: {melhor_custo_estimado:.2f}, Pool: {recurso_escolhido.processos_ativos} atv.)")
        return recurso_escolhido

