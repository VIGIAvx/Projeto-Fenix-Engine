# main.py
# Arquivo principal para demonstrar a Transmutação Fênix.

from fi_runtime_core import FenixExecutionEngine
from fi_transmuter_ia import Transmutar_Codigo
# Importamos AlgoritmoOtimo para criar um objeto que o SAI consiga agendar
from fi_knowledge_base import AlgoritmoOtimo 

# --- Configuração de Métodos de Serviço (Mocks Mínimos) ---

# A FenixExecutionEngine agora usa as classes reais PDH, CAH e SAI
# Apenas os métodos de serviço (lambda functions) são mantidos como mocks.

FenixExecutionEngine.Coletar_Metricas_Execucao = lambda self, ID, custo: print(f"     > Métrica de Execução Coletada para {ID}. Custo: {custo:.2f}")
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
print("SIMULANDO: Transmutar Código Bruto")
print("---------------------------------------------------")

# O BAO real é usado aqui!
blocos_otimizados = Transmutar_Codigo(codigo_legado, engine_fenix)

# 5. Agendar os blocos otimizados (Execução Real)
# A Engine agora usa o SAI e o CAH reais para decidir onde rodar
print("\n---------------------------------------------------")
print("SIMULANDO: Agendamento e Execução (SAI e CAH Reais)")
print("---------------------------------------------------")

# --- CORREÇÃO: BlocoCIO AGORA TEM O CAMPO ID ---
class BlocoCIO:
    def __init__(self, ID, nome, custo_cpu, tipo_calculo="Geral"):
        self.ID = ID  # CORRIGIDO: O campo ID é essencial para o monitoramento
        self.nome = nome
        self.custo_cpu = custo_cpu
        self.tipo_calculo = tipo_calculo

# Instâncias de teste
bloco_exemplo_1 = BlocoCIO(ID="CIO_1", nome="Processamento Gráfico", custo_cpu=50, tipo_calculo="GPU_Intenso")
bloco_exemplo_2 = BlocoCIO(ID="CIO_2", nome="Cálculo Algébrico", custo_cpu=200, tipo_calculo="CPU_Intenso")

engine_fenix.Agendar_Tarefas([bloco_exemplo_1, bloco_exemplo_2])


# 6. Resultado Final da Transmutação (Para manter o formato anterior)
print("\n---------------------------------------------------")
print("RESULTADO FINAL DA TRANSMUTAÇÃO:")
for bloco in blocos_otimizados:
    print(f"- {bloco}")
print("---------------------------------------------------")

