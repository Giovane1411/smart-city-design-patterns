import base

if __name__ == "__main__":
    
    # 1) Criado a central e realizado o registro
    central = base.CentralAlertas()
    central.registrar_orgao(base.CorpoDeBombeiros())
    central.registrar_orgao(base.Hospital())

    # 2) Criar os sensores (folhas). O de fumaça recebe a central
    sensor_temp = base.SensorTemperatura("TEMP-01", bateria=87)
    sensor_fumaca = base.SensorFumaca("FUMACA-01", bateria=64, nivel_fumaca=92, central=central)

    # 3) Monta a árvore com adicionar_filho (de baixo para cima)
    rua = base.Regiao("Rua Doutor Flores")
    rua.adicionar_filho(sensor_temp)
    rua.adicionar_filho(sensor_fumaca)

    bairro = base.Regiao("Bairro Centro")
    bairro.adicionar_filho(rua)

    zona = base.Regiao("Zona Norte")
    zona.adicionar_filho(bairro)

    # 4) Roda os dois visitors a partir da raiz
    relatorio = base.RelatorioXMLVisitor()
    zona.accept(relatorio)
    print(relatorio.xml)

    print("---- Diagnóstico de bateria ----")
    zona.accept(base.DiagnosticoBateriaVisitor())

    # 5) Dispara o alerta (Ex.: fumaça 92% > 80% aciona a central)
    print("---- Alerta ----")
    sensor_fumaca.verificar_fumaca("Rua Doutor Flores")



