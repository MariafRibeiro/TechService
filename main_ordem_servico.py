from src.models.ordem_servico import OrdemServico
from src.repositories import cliente_repository
from src.repositories import equipamento_repository
from src.repositories import ordem_servico_repository


def menu():
    print("\n=== TechService - Gestão de Ordens de Serviço ===")
    print("1. Listar ordens em curso")
    print("2. Inserir ordem de serviço")
    print("3. Procurar ordem por ID")
    print("4. Atualizar status")
    print("5. Ver histórico de uma ordem")
    print("0. Sair")


def opcao_listar():
    ordens = ordem_servico_repository.listar()

    if not ordens:
        print("\nNão há ordens de serviço em curso.")
        return

    print(f"\n{len(ordens)} ordem(ns) em curso:")
    for item in ordens:
        atrasada = " (ATRASADA)" if item["atrasada"] else ""
        print(item["id_ordem"], "-", item["cliente_nome"], "-",
              item["equipamento_marca"], item["equipamento_modelo"], "-",
              item["status"], "-", item["prioridade"], "-",
              item["defeito_relatado"] + atrasada)


def opcao_inserir():
    id_equipamento = input("ID do equipamento: ")

    equipamento = equipamento_repository.procurar_por_id(id_equipamento)
    if equipamento is None:
        print("Esse equipamento não existe. Cria o equipamento primeiro.")
        return

    cliente = cliente_repository.procurar_por_id(equipamento.id_cliente)

    defeito_relatado = input("Defeito relatado: ")
    prioridade = input("Prioridade (BAIXA, MEDIA, ALTA, URGENTE) [MEDIA]: ") or "MEDIA"

    if prioridade not in OrdemServico.PRIORIDADES_VALIDAS:
        print("Prioridade inválida. Ordem não foi criada.")
        return

    ordem = OrdemServico(cliente=cliente, equipamento=equipamento,
                          defeito_relatado=defeito_relatado,
                          prioridade=prioridade)
    ordem = ordem_servico_repository.inserir(ordem)

    print("Ordem de serviço criada com sucesso. ID:", ordem.id_ordem)
    print("Cliente associado:", ordem.cliente.nome)
    print("Equipamento associado:", ordem.equipamento.marca, ordem.equipamento.modelo)


def opcao_procurar():
    id_ordem = input("ID da ordem: ")
    ordem = ordem_servico_repository.procurar_por_id(id_ordem)

    if ordem is None:
        print("Ordem de serviço não encontrada.")
        return

    ordem.mostrar()


def opcao_atualizar_status():
    id_ordem = input("ID da ordem: ")
    ordem = ordem_servico_repository.procurar_por_id(id_ordem)

    if ordem is None:
        print("Ordem de serviço não encontrada.")
        return

    print("Status atual:", ordem.status)
    print("Opções:", ", ".join(OrdemServico.STATUS_VALIDOS))
    novo_status = input("Novo status: ").upper()

    try:
        ordem_servico_repository.atualizar_status(id_ordem, novo_status)
        print("Status atualizado com sucesso.")
    except ValueError as erro:
        print("Não foi possível atualizar:", erro)


def opcao_historico():
    id_ordem = input("ID da ordem: ")
    historico = ordem_servico_repository.listar_historico(id_ordem)

    if not historico:
        print("Sem histórico para esta ordem.")
        return

    print(f"\nHistórico da ordem {id_ordem}:")
    for item in historico:
        item.mostrar()


def main():
    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            opcao_listar()
        elif opcao == "2":
            opcao_inserir()
        elif opcao == "3":
            opcao_procurar()
        elif opcao == "4":
            opcao_atualizar_status()
        elif opcao == "5":
            opcao_historico()
        elif opcao == "0":
            print("A sair...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()