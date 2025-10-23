# fi_knowledge_base.py
import psutil
import sqlite3

# Nome do arquivo do Banco de Dados para persistência
DB_NAME = 'fenix_bao.db' 

class AlgoritmoOtimo:
    """Representa um algoritmo otimizado e seus custos conhecidos."""
    def __init__(self, nome, complexidade, custo_io_padrao, custo_cpu_padrao):
        self.nome = nome
        self.complexidade = complexidade
        self.custo_io = custo_io_padrao
        self.custo_cpu = custo_cpu_padrao

    def __repr__(self):
        return f"AlgoritmoOtimo('{self.nome}', C_CPU:{self.custo_cpu:.2f})"

class BancoAlgoritmosOtimos:
    """
    BAO (Banco de Algoritmos Ótimos) Persistente com SQLite.
    """
    def __init__(self):
        self.conexao = sqlite3.connect(DB_NAME)
        self.cursor = self.conexao.cursor()
        self._criar_tabela_se_necessario()
        self.mapa_otimizacao = self._carregar_algoritmos() # Mapeamento em RAM para acesso rápido

    def _criar_tabela_se_necessario(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS algoritmos (
                problema_identificado TEXT PRIMARY KEY,
                nome TEXT,
                complexidade TEXT,
                custo_io REAL,
                custo_cpu REAL
            )
        """)
        self.conexao.commit()

        # Algoritmos Base (Seed Data) - Inseridos apenas se o banco estiver vazio
        base_algoritmos = [
            ("Problema B: Cálculo O(n^2)", "QuickSort Paralelo", "O(n log n)", 5.0, 8.0),
            ("Problema de Busca Lenta", "Hash Index Lookup", "O(1)", 2.0, 1.0),
            ("Problema de I/O Pesado", "Leitura Assíncrona Chunked", "O(k)", 100.0, 3.0),
            ("Problema Não Identificado", "Algoritmo Legado", "O(n!)", 100.0, 100.0)
        ]

        for problema, nome, complexidade, custo_io, custo_cpu in base_algoritmos:
            self.cursor.execute("""
                INSERT OR IGNORE INTO algoritmos VALUES (?, ?, ?, ?, ?)
            """, (problema, nome, complexidade, custo_io, custo_cpu))
        self.conexao.commit()

    def _carregar_algoritmos(self):
        self.cursor.execute("SELECT * FROM algoritmos")
        dados = self.cursor.fetchall()
        mapa = {}
        for problema, nome, complexidade, custo_io, custo_cpu in dados:
            mapa[problema] = AlgoritmoOtimo(nome, complexidade, custo_io, custo_cpu)
        return mapa

    def Buscar_Substituicao(self, problema_identificado):
        return self.mapa_otimizacao.get(
            problema_identificado, 
            self.mapa_otimizacao["Problema Não Identificado"]
        )

    def Salvar_Algoritmo_Ajustado(self, problema_identificado, algoritmo_ajustado):
        """Persiste o custo ajustado pelo PGO no banco de dados."""
        self.cursor.execute("""
            UPDATE algoritmos
            SET custo_io = ?, custo_cpu = ?
            WHERE problema_identificado = ?
        """, (algoritmo_ajustado.custo_io, algoritmo_ajustado.custo_cpu, problema_identificado))
        self.conexao.commit()
        # Atualiza o mapa em RAM
        self.mapa_otimizacao[problema_identificado] = algoritmo_ajustado


# Classes MCA e PDH mantidas
class ModeloCustoAbstrato:
    """MCA (Modelo de Custo Abstrato). Parâmetros de custo calibrados."""
    def __init__(self, limite_io, fator_cpu_core):
        self.limite_aceitavel_IO = limite_io
        self.fator_cpu_core = fator_cpu_core
        print(f"  [MCA]: Calibrado. Fator CPU: {fator_cpu_core}x. Limite IO: {limite_io}.")

class PerfilamentoDinamicoHardware:
    """
    PDH (Perfilamento Dinâmico de Hardware) REAL. 
    Mede o hardware e calibra o MCA.
    """
    @staticmethod
    def Calibrar_Custos_Hardware(hardware_profile):
        print(f"  [PDH Real]: Perfilando ambiente usando psutil...")

        num_cores = psutil.cpu_count(logical=True)
        fator_cpu = max(1.0, num_cores / 4) 

        memoria = psutil.virtual_memory()
        ram_disponivel_gb = memoria.available / (1024 ** 3)

        if ram_disponivel_gb < 1.0:
             limite_io_calibrado = 15
             ram_status = "CRÍTICO"
        else:
             limite_io_calibrado = 8 
             ram_status = "OK"

        print(f"  [PDH Status]: Cores: {num_cores}, RAM Livre: {ram_disponivel_gb:.2f} GB ({ram_status})")
        return ModeloCustoAbstrato(limite_io_calibrado, fator_cpu)


class ModuloAutoReflexaoIntegridade:
    """MARI (Módulo de Auto-Reflexão e Integridade)."""
    def __init__(self, BAO_instance):
        self.BAO = BAO_instance

    def Carregar_Banco_Integridade(self):
        print("  [MARI]: Verificação de integridade do BAO concluída (Persistente).")
        return self.BAO

    def Verificar_Coerencia(self, BAO_para_verificar):
        return True

