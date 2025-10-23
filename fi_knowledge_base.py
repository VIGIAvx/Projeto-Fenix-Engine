# fi_knowledge_base.py
# Banco de Algoritmos Otimizados (BAO) e Armazenamento de Conhecimento (SQLite)

import sqlite3
import os

class AlgoritmoCIO:
    """Representa um Bloco de Instrução/Otimização (CIO) com seus custos."""
    def __init__(self, nome, custo_cpu, custo_io, tipo):
        self.nome = nome
        self.custo_cpu = custo_cpu
        self.custo_io = custo_io
        self.tipo = tipo # Ex: "CPU_Bound", "IO_Bound"
        self.ID = nome # Simplificação para ID

class BancoAlgoritmosOtimos:
    """Gerencia os custos persistentes dos algoritmos no SQLite."""
    def __init__(self):
        # Mapeamento: Nome do Problema -> AlgoritmoCIO (contém custos atuais)
        self.mapa_otimizacao = {} 
        self._inicializar_simulacao_sqlite()
        self._carregar_custos()

    def _inicializar_simulacao_sqlite(self):
        self.db_path = "fenix_knowledge.db"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS custos (
                nome TEXT PRIMARY KEY,
                custo_cpu REAL,
                custo_io REAL
            )
        """)
        self.conn.commit()

    def _carregar_custos(self):
        """Carrega custos persistentes ou insere valores default para simulação."""

        # Algoritmos Default (incluindo o estado do último ciclo PGO para QuickSort)
        default_algoritmos = {
            "CIO_1_Min_IO": AlgoritmoCIO("Variante Min-IO", 5.0, 100.0, "IO_Bound"),
            "CIO_2_QuickSort_P": AlgoritmoCIO("QuickSort Paralelo", 3.44, 0.5, "CPU_Bound"),
            "CIO_3_QuickSort_P": AlgoritmoCIO("QuickSort Paralelo", 3.44, 0.5, "CPU_Bound"),
            "CIO_4_QuickSort_P": AlgoritmoCIO("QuickSort Paralelo", 3.44, 0.5, "CPU_Bound"),
        }

        # Carrega do DB
        db_data = self.cursor.execute("SELECT nome, custo_cpu, custo_io FROM custos").fetchall()

        if not db_data:
            # Se o banco está vazio, insere defaults
            for nome, algo in default_algoritmos.items():
                self.cursor.execute("INSERT INTO custos VALUES (?, ?, ?)", 
                                    (nome, algo.custo_cpu, algo.custo_io))
                self.mapa_otimizacao[nome] = algo
            self.conn.commit()
        else:
            # Se há dados, carrega os custos otimizados (especialmente o último custo do QuickSort)
            ultimo_custo_qs = default_algoritmos["CIO_2_QuickSort_P"].custo_cpu
            for nome, custo_cpu, custo_io in db_data:
                if "QuickSort" in nome:
                    ultimo_custo_qs = custo_cpu # Carrega o último custo salvo (pode ser 2.26, 2.03, etc.)

            # Atualiza o mapa com o custo persistido
            for nome, algo in default_algoritmos.items():
                if "QuickSort" in nome:
                    algo.custo_cpu = ultimo_custo_qs
                self.mapa_otimizacao[nome] = algo

    def persistir_custo(self, nome_problema, novo_custo):
        """
        [MÉTODO CORRIGIDO] Atualiza o custo CPU de um algoritmo persistente no SQLite.
        Salva o custo de volta, mantendo a integridade do conhecimento.
        """

        # 1. Atualizar o SQLite com o novo custo
        # Atualiza o custo para todos os blocos QuickSort Paralelo (assumindo otimização de perfil)
        self.cursor.execute("UPDATE custos SET custo_cpu = ? WHERE nome LIKE 'CIO_%QuickSort_P'", 
                            (novo_custo,))
        self.conn.commit()

        # 2. Atualizar o mapa interno (em memória)
        for nome in self.mapa_otimizacao:
             if "QuickSort Paralelo" in self.mapa_otimizacao[nome].nome:
                self.mapa_otimizacao[nome].custo_cpu = novo_custo

    def get_custo_cpu(self, nome_algoritmo):
        """Retorna o custo CPU atual para o algoritmo nomeado."""
        return self.mapa_otimizacao.get(nome_algoritmo, AlgoritmoCIO("", 0, 0, "")).custo_cpu

