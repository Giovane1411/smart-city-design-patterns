from abc import ABC, abstractmethod

# ==========================================
# 1. COMPONENTES DO OBSERVER (Eventos)
# ==========================================
class CentralAlertas(ABC):
    """Subject (Publicador)"""
    def __init__(self):
        self._orgaos_interessados = []

    def registrar_orgao(self, orgao):
        self._orgaos_interessados.append(orgao)

    def notificar_emergencia(self, local, tipo_emergencia):
        for orgao in self._orgaos_interessados:
            orgao.update(local, tipo_emergencia)

class OrgaoPublico(ABC):
    """Observer (Assinante)"""
    @abstractmethod
    def update(self, local, tipo_emergencia): pass


# ==========================================
# 2. COMPONENTES DA ESTRUTURA (Composite & Visitor)
# ==========================================
class Visitor(ABC):
    @abstractmethod
    def visit_sensor_temperatura(self, sensor): pass
    @abstractmethod
    def visit_sensor_fumaca(self, sensor): pass
    @abstractmethod
    def visit_regiao(self, regiao): pass

class ComponenteIoT(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor): pass

# TODO: Implementar a classe Regiao (Composite)
# TODO: Implementar SensorTemperatura e SensorFumaca (Leafs)
# TODO: Implementar RelatorioXMLVisitor e DiagnosticoBateriaVisitor
# TODO: Implementar CorpoDeBombeiros e Hospital (Observers)