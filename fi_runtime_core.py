# fi_runtime_core.py
# Componente Central: Fenix Execution Engine (Motor de Execução Fênix)

# Importa a Base de Conhecimento real (PDH, MCA, BAO, MARI)
from fi_knowledge_base import (
    BancoAlgoritmosOtimos, 
    PerfilamentoDinamicoHardware,
    ModeloCustoAbstrato,
    ModuloAutoReflexaoIntegridade # <-- RE-ADICIONADO
)

# Importa as classes reais de Agendamento e Abstração (SAI e CAH)
from fi_scheduling_sai import ServicoAgendamentoInteligente, CamadaAbstracaoHeterogenea

# Importa o novo módulo de Otimização e o controlador MARI
from fi_auto_optimization import ModuloAutoReflexaoIntegridade as MARI_Controlador


class FenixExecutionEngine:
    # --- Módulos Principais (Classes Reais) ---
    PDH = PerfilamentoDinamicoHardware 
    CAH = CamadaAbstracaoHeterogenea
    SAI = ServicoAgendamentoInteligente

    class MTA_PGO: pass # Placeholder para a classe PGO

    def __init__(self, hardware_profile):
        # 1. Lista de Métricas Coletadas (Para o ciclo PGO)
        self.metricas_coletadas = []

        # 2. MCA (Modelo de Custo Abstrato) – Calibrado pelo PDH real
        self.MCA = self.PDH.Calibrar_Custos_Hardware(hardware_profile) 

        # 3. Inicializa o BAO
        self.BAO = BancoAlgoritmosOtimos() 

        # 4. Inicializa o MARI e carrega o BAO <-- CORRIGIDO AQUI
        self.MARI = ModuloAutoReflexaoIntegridade(self.BAO) 
        self.BAO = self.MARI.Carregar_Banco_Integridade()

        # 5. Pool de Recursos (CAH Real)
        self.Recursos_UHE = self.CAH.Gerar_Pool_Recursos(GPU=True, CPU_cores=True, MCA=self.MCA)


    # --- Serviço de Agendamento Inteligente (SAI) ---
    def Agendar_Tarefas(self, CIO_paralelizado):
        # Lógica de Agendamento e Migração (SAI Real)
        for bloco in CIO_paralelizado:
            # O SAI usa o MCA para decidir
            recurso_otimo = self.SAI.Escolher_Recurso(bloco, self.Recursos_UHE, self.MCA)
            self.CAH.Executar_Bloco(bloco, recurso_otimo)

            # Métrica de Latência: A métrica é coletada e SALVA para o PGO
            custo_execucao_simulado = recurso_otimo.custo_por_ciclo # Simula o custo real
            self.metricas_coletadas.append((bloco.ID, custo_execucao_simulado))
            print(f"     > Métrica de Execução Coletada para {bloco.ID}. Custo: {custo_execucao_simulado:.2f}")

    # --- Módulo de Auto-Reflexão e Otimização (MARI/PGO) ---
    def Auto_Reflexao_E_PGO(self):
        """Inicia o ciclo de Otimização Guiada por Perfil após a execução."""
        print("\n---------------------------------------------------")
        print("INICIANDO: Ciclo de Auto-Reflexão (MARI/PGO)")
        print("---------------------------------------------------")

        # Chama o controlador estático do MARI (que instancia e roda o PGO)
        MARI_Controlador.Gerenciar_PGO_e_BAO(self, self.metricas_coletadas)

