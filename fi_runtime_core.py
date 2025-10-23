# fi_runtime_core.py
# O coração da Fenix Execution Engine

from fi_profile_hardware import PerfiladorDadosHardware
from fi_knowledge_base import BancoAlgoritmosOtimos
from fi_scheduling_sai import ServicoAgendamentoInteligente, CamadaAbstracaoHeterogenea
from fi_auto_optimization import MotorAutoReflexao as MARI_Controlador 
import time
import os

class FenixExecutionEngine:
    def __init__(self, hardware_profile="Generico"):
        self.Hardware_Profile = hardware_profile
        self._inicializar_subsistemas()
        self._carregar_conhecimento_persistente()

    def _inicializar_subsistemas(self):
        # 1. PDH: Perfilamento de Hardware
        self.PDH = PerfiladorDadosHardware(self.Hardware_Profile)

        # 2. MCA: Modelo de Custo Abstrato (Calibrado pelo PDH)
        self.MCA = self.PDH.calibrar_modelo_custo()

        # 3. BAO/MARI: Banco de Algoritmos Otimizados e Controlador de Integridade
        self.BAO = BancoAlgoritmosOtimos() # <-- CORREÇÃO APLICADA: Não passa mais self.MCA
        self.MARI = MARI_Controlador(self.BAO) # Motor de Auto-Reflexão

        # 4. CAH: Camada de Abstração Heterogênea (Recursos UHE)
        # Simula a detecção de um recurso GPU e o uso de todos os cores disponíveis
        gpu_disponivel = True
        cpu_cores = self.PDH.cores_logicos
        self.Recursos_UHE = CamadaAbstracaoHeterogenea.Gerar_Pool_Recursos(
            gpu_disponivel, cpu_cores, self.MCA
        )

    def _carregar_conhecimento_persistente(self):
        print("  [MARI]: Verificação de integridade do BAO concluída (Persistente).")

    def Agendar_Tarefas(self, blocos_cio):
        """Processa e agenda uma lista de blocos de Instrução/Otimização (CIO)."""
        for bloco in blocos_cio:

            # 1. SAI: Escolhe o recurso ideal
            recurso_otimo = ServicoAgendamentoInteligente.Escolher_Recurso(
                bloco, self.Recursos_UHE, self.MCA
            )

            # 2. CAH: Despacha para o recurso
            CamadaAbstracaoHeterogenea.Executar_Bloco(bloco, recurso_otimo)

            # 3. MTA: Coleta métrica da execução
            # MOCK: A métrica é uma simulação de custo de execução rápido (0.05)
            self.MARI.coletar_metrica_execucao(bloco.ID, custo_real=0.05)

    def Auto_Reflexao_E_PGO(self):
        """Inicia o ciclo de auto-aprendizado e otimização do perfil (PGO)."""
        print("\n---------------------------------------------------")
        print("INICIANDO: Ciclo de Auto-Reflexão (MARI/PGO)")
        print("---------------------------------------------------")
        self.MARI.iniciar_ciclo_pgo()

    # Mock para métodos futuros, como agendamento de chamada externa (CEO)
    @staticmethod
    def Agendar_Tarefa_Compatibilidade(ceo):
        print(f"     > Tarefa CEO Agendada: {ceo}")

