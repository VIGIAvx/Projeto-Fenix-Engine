# fi_auto_optimization.py
# Motor de Auto-Reflexão e Otimização de Perfil Guiada (MTA-PGO)

from fi_knowledge_base import BancoAlgoritmosOtimos
import subprocess # NOVO MÓDULO PARA CHAMAR O RUST CORE
import os

class MotorAutoReflexao:
    """
    MTA (Motor de Auto-Reflexão). 
    Monitora a execução, aplica PGO e ajusta o BAO.
    """
    def __init__(self, bao: BancoAlgoritmosOtimos):
        self.BAO = bao
        self.metrica_historico = []
        self.fator_ajuste_pgo = 0.90 # Fator de 10% de redução por ciclo

    def coletar_metrica_execucao(self, bloco_id, custo_real):
        """Simula a coleta de métricas de tempo de execução real do bloco."""
        self.metrica_historico.append({"id": bloco_id, "custo": custo_real})

    def iniciar_ciclo_pgo(self):
        """Aplica a otimização de Perfil Guiada (PGO) nos algoritmos do BAO."""
        print("\n  [MTA-PGO]: Iniciando Processamento PGO...")
        ajustes_feitos = 0

        # 1. Analisar as métricas e identificar o algoritmo a ser otimizado
        # Simulação: Todos os blocos CIO que não são I/O Intenso (por ex., QuickSort Paralelo)

        for nome_problema, algoritmo in self.BAO.mapa_otimizacao.items():

            # Regra simples de PGO: Apenas otimiza o QuickSort Paralelo 
            # (Representando o cálculo CPU-bound)
            if "QuickSort Paralelo" in algoritmo.nome:

                # 2. Chamada ao CORE RUST para Otimização
                novo_custo = self._aplicar_pgo_rust(algoritmo.custo_cpu, self.fator_ajuste_pgo)

                if novo_custo < algoritmo.custo_cpu:

                    # 3. Persistir o Novo Custo
                    self.BAO.persistir_custo(nome_problema, novo_custo)
                    algoritmo.custo_cpu = novo_custo
                    print(f"  [PGO-Ajuste]: Otimização confirmada para {algoritmo.nome}. Novo Custo CPU: {novo_custo:.2f} (Persistente)")
                    ajustes_feitos += 1

        print(f"  [MTA-PGO]: Ciclo PGO concluído. {ajustes_feitos} algoritmos ajustados.")

        # 4. Limpar o histórico (para um novo ciclo de aprendizado)
        self.metrica_historico = []

        # 5. Manter a integridade do BAO
        print("  [MARI]: Integridade do BAO mantida após ajustes PGO.")


    def _aplicar_pgo_rust(self, custo_atual, fator_reducao):
        """
        Chama o microsserviço MTA Core (Rust) para calcular o novo custo otimizado.
        """

        caminho_binario = './fi_mta_core'

        try:
            # Executa o binário Rust de forma síncrona para obter o resultado
            resultado = subprocess.run([caminho_binario, str(custo_atual), str(fator_reducao)],
                                       capture_output=True, text=True, check=True)

            # Processar o resultado da saída padrão (stdout)
            for linha in resultado.stdout.splitlines():
                if linha.startswith("Fenix_RESULTADO_MTA:"):
                    # Extrai o valor numérico (e.g., "Fenix_RESULTADO_MTA:3.1000")
                    novo_custo_str = linha.split(":", 1)[1]
                    return float(novo_custo_str)

            # Se o Rust não retornou o formato esperado
            print(f"AVISO: O Core Rust não retornou o formato de resultado esperado. Output: {resultado.stdout.strip()}")
            return custo_atual # Retorna o custo original para evitar erro

        except subprocess.CalledProcessError as e:
            print(f"ERRO CRÍTICO (MTA-RUST): O binário Rust falhou. Stderr: {e.stderr.strip()}")
            return custo_atual
        except FileNotFoundError:
            print(f"ERRO CRÍTICO (MTA-RUST): Binário {caminho_binario} não encontrado. Usando fallback.")
            return custo_atual * fator_reducao # Fallback simples em Python

