# fi_profile_hardware.py
# Perfilador de Dados de Hardware (PDH) e Modelo de Custo Abstrato (MCA)

import psutil
import os

class ModeloCustoAbstrato:
    """Contém os fatores de custo e limiares calibrados para o hardware atual."""
    def __init__(self, fator_cpu_core, limite_aceitavel_IO):
        self.fator_cpu_core = fator_cpu_core
        self.limite_aceitavel_IO = limite_aceitavel_IO

    def __str__(self):
        return f"MCA (Fator CPU: {self.fator_cpu_core}x. Limite IO: {self.limite_aceitavel_IO})"

class PerfiladorDadosHardware:
    """Detecta o hardware físico e calibra o MCA."""
    def __init__(self, profile_name):
        self.profile_name = profile_name
        self.cores_logicos = 1
        self.ram_livre_gb = 0.0
        self._perfilamento_real()

    def _perfilamento_real(self):
        print("  [PDH Real]: Perfilando ambiente usando psutil...")
        try:
            # Cores
            self.cores_logicos = psutil.cpu_count(logical=True)
            if self.cores_logicos is None:
                self.cores_logicos = 1 # Fallback

            # RAM Livre
            mem = psutil.virtual_memory()
            self.ram_livre_gb = mem.available / (1024 ** 3) # Bytes para GB

        except Exception as e:
            # Ocorreu um erro no Termux/psutil. Usamos valores padrão.
            self.cores_logicos = 4
            self.ram_livre_gb = 0.5
            print(f"  [PDH AVISO]: psutil falhou ({e}). Usando fallback.")

        status = "CRÍTICO" if self.ram_livre_gb < 0.5 else "OK"
        print(f"  [PDH Status]: Cores: {self.cores_logicos}, RAM Livre: {self.ram_livre_gb:.2f} GB ({status})")

    def calibrar_modelo_custo(self):
        """Gera o Modelo de Custo Abstrato (MCA) baseado no PDH."""

        # 1. Fator CPU (Baseado nos cores, penalizado pela RAM baixa)
        fator_base = max(1.0, self.cores_logicos / 4) # Base de 4 cores

        # Penalidade se a RAM for baixa (simulação de gargalo)
        if self.ram_livre_gb < 0.5:
            fator_cpu = fator_base * 1.5 # Pior fator para simular Termux
        else:
            fator_cpu = fator_base * 2.0 # Fator ideal

        # 2. Limite I/O
        limite_io = 15 # Um valor constante no Termux

        mca = ModeloCustoAbstrato(fator_cpu_core=fator_cpu, limite_aceitavel_IO=limite_io)
        print(f"  [{mca.fator_cpu_core}] MCA]: Calibrado. {mca}")
        return mca

