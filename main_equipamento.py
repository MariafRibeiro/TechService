from src.models.equipamento import Equipamento
from src.repositories import equipamento_repository


def menu():
    print("\n=== TechService - Sistema de Gestão de Assistência Técnica ===")
    print("--- Equipamentos ---")
    print("6. Listar equipamentos")
    print("7. Inserir equipamento")
    print("8. Procurar equipamento por ID")
    print("9. Atualizar equipamento")
    print("10. Remover equipamento")
    print("0. Sair")


def opcao_listar_equipamentos():
    equipamentos = equipamento_repository.listar()

    if not equipamentos:
        print("\nNão há equipamentos ativos na base de dados.")
        return

    print(f"\n{len(equipamentos)} equipamento(s) ativo(s):")
    for item in equipamentos:
        print(item["id_equipamento"], "- Cliente", item["id_cliente"], "-",
              item["tipo"], item["marca"], item["modelo"], "- Série:", item["numero_serie"])


def opcao_inserir_equipamento():
    id_cliente = input("ID do cliente dono do equipamento: ")

    cliente = cliente_repository.procurar_por_id(id_cliente)
    if cliente is None:
        print("Esse cliente não existe. Cria o cliente primeiro.")
        return

    tipo = input("Tipo (ex: Notebook, Impressora): ")
    marca = input("Marca: ")
    modelo = input("Modelo: ")
    numero_serie = input("Número de série: ")
    observacoes = input("Observações (opcional): ") or None

    equipamento = Equipamento(id_cliente=id_cliente, tipo=tipo, marca=marca,
                              modelo=modelo, numero_serie=numero_serie,
                              observacoes=observacoes)
    equipamento = equipamento_repository.inserir(equipamento)

    print("Equipamento inserido com sucesso. ID:", equipamento.id_equipamento)


def opcao_procurar_equipamento():
    id_equipamento = input("ID do equipamento: ")
    equipamento = equipamento_repository.procurar_por_id(id_equipamento)

    if equipamento is None:
        print("Equipamento não encontrado.")
        return

    equipamento.mostrar()


def opcao_atualizar_equipamento():
    id_equipamento = input("ID do equipamento a atualizar: ")
    equipamento = equipamento_repository.procurar_por_id(id_equipamento)

    if equipamento is None:
        print("Equipamento não encontrado.")
        return

    novas_observacoes = input(
        f"Novas observações (atual: {equipamento.observacoes}, Enter para manter): "
    )

    if novas_observacoes:
        equipamento.observacoes = novas_observacoes

    equipamento_repository.atualizar(equipamento)
    print("Equipamento atualizado com sucesso.")


def opcao_remover_equipamento():
    id_equipamento = input("ID do equipamento a remover: ")
    equipamento_repository.remover(id_equipamento)
    print("Equipamento removido com sucesso.")


def main():
    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "6":
            opcao_listar_equipamentos()
        elif opcao == "7":
            opcao_inserir_equipamento()
        elif opcao == "8":
            opcao_procurar_equipamento()
        elif opcao == "9":
            opcao_atualizar_equipamento()
        elif opcao == "10":
            opcao_remover_equipamento()
        elif opcao == "0":
            print("A sair...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()

