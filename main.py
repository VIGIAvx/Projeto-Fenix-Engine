# main.py
# Arquivo principal para demonstrar a Transmutação Fênix.

from fi_runtime_core import FenixExecutionEngine
from fi_transmuter_ia import Transmutar_Codigo
# Importamos AlgoritmoOtimo para criar um objeto que o SAI consiga agendar
from fi_knowledge_base import AlgoritmoOtimo, BancoAlgoritmosOtimos

# --- Configuração de Métodos de Serviço (Mocks Mínimos) ---

# A FenixExecutionEngine agora usa as classes reais PDH, CAH e SAI
# Apenas os métodos de serviço (lambda functions) são mantidos como mocks.

# NOTE: A função Coletar_Metricas_Execucao foi removida pois a métrica é coletada
# e salva DIRETAMENTE na engine (self.metricas_coletadas)
FenixExecutionEngine.Agendar_Tarefa_Compatibilidade = lambda self, ceo: print(f"     > Tarefa CEO Agendada: {ceo}")


# 2. Inicialização da Fenix Execution Engine
print("Iniciando a Fenix Execution Engine...")

# Inicializa com um perfil genérico que será lido pelo PDH real
engine_fenix = FenixExecutionEngine(hardware_profile="AndroidTermux") 

print(f"Engine Fênix inicializada. BAO carregado.")
print(f"MCA (Limite IO: {engine_fenix.MCA.limite_aceitavel_IO})")

# 3. Código Bruto de Exemplo (Ineficiente)
codigo_legado = """
# Função Lenta de Merge Sort
# ... código ...
# Leitura de 10GB de log via Disco
# ... código ...
"""

# 4. Iniciar a Transmutação
print("\n---------------------------------------------------")
print("SIMULANDO: Transmutar Código Bruto (Estado Inicial)")
print("---------------------------------------------------")

blocos_otimizados = Transmutar_Codigo(codigo_legado, engine_fenix)

# 5. Agendar os blocos otimizados (Execução Real)
print("\n---------------------------------------------------")
print("SIMULANDO: Agendamento e Execução (SAI e CAH Reais)")
print("---------------------------------------------------")

class BlocoCIO:
    def __init__(self, ID, nome, custo_cpu, tipo_calculo="Geral"):
        self.ID = ID 
        self.nome = nome
        self.custo_cpu = custo_cpu
        self.tipo_calculo = tipo_calculo

bloco_exemplo_1 = BlocoCIO(ID="CIO_1", nome="Processamento Gráfico", custo_cpu=50, tipo_calculo="GPU_Intenso")
bloco_exemplo_2 = BlocoCIO(ID="CIO_2", nome="Cálculo Algébrico", custo_cpu=200, tipo_calculo="CPU_Intenso")

# Guarda o custo inicial do QuickSort para comparação (será 8)
custo_inicial_quick_sort = engine_fenix.BAO.mapa_otimizacao["Problema B: Cálculo O(n^2)"].custo_cpu

engine_fenix.Agendar_Tarefas([bloco_exemplo_1, bloco_exemplo_2])

print(f"\n[Verificação Inicial]: Custo CPU do QuickSort ANTES do PGO: {custo_inicial_quick_sort:.2f}")


# 6. INICIAR O CICLO DE AUTO-REFLEXÃO (MTA-PGO)
engine_fenix.Auto_Reflexao_E_PGO()


# 7. VERIFICAR O RESULTADO DO PGO
custo_final_quick_sort = engine_fenix.BAO.mapa_otimizacao["Problema B: Cálculo O(n^2)"].custo_cpu

print(f"[Verificação Final]: Custo CPU do QuickSort DEPOIS do PGO: {custo_final_quick_sort:.2f}")
if custo_final_quick_sort < custo_inicial_quick_sort:
    print("\n[MTA-PGO SUCESSO]: O Motor Fênix aprendeu! O custo do QuickSort foi reduzido.")
else:
    print("\n[MTA-PGO FALHA]: O Motor Fênix não conseguiu aprender neste ciclo.")

# 8. Resultado Final da Transmutação (Para manter o formato anterior)
print("\n---------------------------------------------------")
print("RESULTADO FINAL DA TRANSMUTAÇÃO:")
for bloco in blocos_otimizados:
    print(f"- {bloco}")
print("---------------------------------------------------")

