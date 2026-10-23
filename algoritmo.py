from copy import deepcopy

# DADOS DO ENUNCIADO(usados na opção 1 do menu)
def dados_do_enunciado():
    
    return {
        "disciplinas": [
            {"nome": "Banco de Dados", "professor": "Ana",
             "aulas": 2, "ambiente": "qualquer"},
            {"nome": "Algoritmos", "professor": "Carlos",
             "aulas": 2, "ambiente": "qualquer"},
            {"nome": "Redes", "professor": "Ana",
             "aulas": 2, "ambiente": "laboratorio"},
            {"nome": "Engenharia de Software", "professor": "Mariana",
             "aulas": 2, "ambiente": "qualquer"},
            {"nome": "Programação Web", "professor": "Carlos",
             "aulas": 2, "ambiente": "laboratorio"},
            {"nome": "Sistemas Operacionais", "professor": "Pedro",
             "aulas": 2, "ambiente": "qualquer"},
        ],
        "salas": {
            "Lab 1": "laboratorio",
            "Lab 2": "laboratorio",
            "Sala 3": "comum",
        },
        "horarios": ["H1", "H2", "H3", "H4", "H5"],
        "disponibilidade": {
            "Ana": ["H1", "H2", "H3", "H4"],
            "Carlos": ["H1", "H2", "H3", "H4"],
            "Mariana": ["H1", "H3", "H5"],
            "Pedro": ["H2", "H4", "H5"],
        },
        "bloqueios": {
            ("Lab 1", "H2"),
            ("Lab 2", "H3"),
        },
    }

# ENTRADA DE DADOS PELO TERMINAL

def ler_texto(mensagem):
    
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("  Valor vazio. Tente novamente.")


def ler_inteiro(mensagem, minimo=1):

    while True:
        valor = input(mensagem).strip()
        if valor.isdigit() and int(valor) >= minimo:
            return int(valor)
        print(f"  Digite um número inteiro maior ou igual a {minimo}.")


def ler_opcao(mensagem, opcoes):
    """Lê uma opção válida dentre as chaves do dicionário 'opcoes'."""
    while True:
        valor = input(mensagem).strip()
        if valor in opcoes:
            return opcoes[valor]
        print(f"  Opção inválida. Escolha entre: {', '.join(opcoes)}.")


def ler_lista(mensagem, permitidos=None, permitir_vazia=False):
    """
    Lê uma lista separada por vírgulas.
    Se 'permitidos' for informado, todos os itens devem estar nele.
    """
    while True:
        itens = [i.strip() for i in input(mensagem).split(",") if i.strip()]

        if not itens and not permitir_vazia:
            print("  Informe pelo menos um valor.")
            continue

        if permitidos is not None:
            invalidos = [i for i in itens if i not in permitidos]
            if invalidos:
                print(f"  Valores inválidos: {', '.join(invalidos)}. "
                      f"Válidos: {', '.join(permitidos)}.")
                continue

        return list(dict.fromkeys(itens))  # remove repetidos mantém ordem


def ler_dados_terminal():
    

    print("\n--- HORÁRIOS ---")
    horarios = ler_lista("Horários separados por vírgula (ex: H1,H2,H3): ")

    print("\n--- SALAS ---")
    salas = {}
    quantidade = ler_inteiro("Quantidade de salas: ")
    for i in range(1, quantidade + 1):
        while True:
            nome = ler_texto(f"Nome da sala {i} (ex: Lab 1): ")
            if nome in salas:
                print("  Essa sala já foi cadastrada.")
            else:
                break
        tipo = ler_opcao("  Tipo (1 = laboratório, 2 = comum): ",
                         {"1": "laboratorio", "2": "comum"})
        salas[nome] = tipo

    print("\n--- DISCIPLINAS ---")
    disciplinas = []
    quantidade = ler_inteiro("Quantidade de disciplinas: ")
    for i in range(1, quantidade + 1):
        print(f"Disciplina {i}:")
        nome = ler_texto("  Nome: ")
        professor = ler_texto("  Professor(a): ")
        aulas = ler_inteiro("  Quantidade de aulas: ")
        ambiente = ler_opcao("  Ambiente (1 = qualquer sala, 2 = laboratório): ",
                             {"1": "qualquer", "2": "laboratorio"})
        disciplinas.append({
            "nome": nome,
            "professor": professor,
            "aulas": aulas,
            "ambiente": ambiente
        })

    print("\n--- DISPONIBILIDADE DOS PROFESSORES ---")
    disponibilidade = {}
    professores = list(dict.fromkeys(d["professor"] for d in disciplinas))
    for professor in professores:
        disponibilidade[professor] = ler_lista(
            f"Horários disponíveis de {professor} (separados por vírgula): ",
            permitidos=horarios,
            permitir_vazia=True
        )

    print("\n--- BLOQUEIOS DE SALAS ---")
    bloqueios = set()
    print("Informe cada bloqueio. Deixe a sala em branco para terminar.")
    while True:
        sala = input("  Sala bloqueada: ").strip()
        if not sala:
            break
        if sala not in salas:
            print(f"  Sala inexistente. Salas cadastradas: {', '.join(salas)}.")
            continue
        horario = input("  Horário do bloqueio: ").strip()
        if horario not in horarios:
            print(f"  Horário inexistente. Horários: {', '.join(horarios)}.")
            continue
        bloqueios.add((sala, horario))

    return {
        "disciplinas": disciplinas,
        "salas": salas,
        "horarios": horarios,
        "disponibilidade": disponibilidade,
        "bloqueios": bloqueios,
    }


def ler_cenario_restrito(dados):
    """
    Lê do terminal a alteração de disponibilidade de um professor,
    gerando uma cópia dos dados (cenário restrito).
    """
    professores = list(dados["disponibilidade"])
    print(f"\nProfessores: {', '.join(professores)}")

    while True:
        professor = input("Professor cuja disponibilidade será alterada: ").strip()
        if professor in dados["disponibilidade"]:
            break
        print("  Professor inexistente.")

    novos = ler_lista(
        f"Novos horários disponíveis de {professor} (separados por vírgula): ",
        permitidos=dados["horarios"],
        permitir_vazia=True
    )

    novos_dados = deepcopy(dados)
    novos_dados["disponibilidade"][professor] = novos
    return novos_dados

# ALGORITMO DE BACKTRACKING

def resolver_grade(disciplinas, salas, horarios,disponibilidade, bloqueios):

    tarefas = []

    for disciplina in disciplinas:
        for numero in range(1, disciplina["aulas"] + 1):
            tarefas.append({
                "disciplina": disciplina["nome"],
                "professor": disciplina["professor"],
                "ambiente": disciplina["ambiente"],
                "numero_aula": numero
            })

    grade = []

    estatisticas = {
        "combinacoes_testadas": 0,
        "alocacoes": 0,
        "retrocessos": 0
    }

    def candidatos(tarefa):
        """Gera as combinações possíveis de horário e sala."""

        resultado = []

        professor = tarefa["professor"]
        nome_disciplina = tarefa["disciplina"]

        for horario in horarios:

            if horario not in disponibilidade.get(professor, []):
                continue

            if any(
                aula["disciplina"] == nome_disciplina
                and aula["horario"] == horario
                for aula in grade
            ):
                continue

            if any(
                aula["professor"] == professor
                and aula["horario"] == horario
                for aula in grade
            ):
                continue

            for sala, tipo_sala in salas.items():

                if (
                    tarefa["ambiente"] == "laboratorio"
                    and tipo_sala != "laboratorio"
                ):
                    continue

                if (sala, horario) in bloqueios:
                    continue

                if any(
                    aula["sala"] == sala
                    and aula["horario"] == horario
                    for aula in grade
                ):
                    continue

                resultado.append({
                    "disciplina": nome_disciplina,
                    "professor": professor,
                    "horario": horario,
                    "sala": sala,
                    "numero_aula": tarefa["numero_aula"]
                })

        return resultado

    def backtracking(pendentes):
        if not pendentes:
            return True

        opcoes_por_tarefa = []

        for tarefa in pendentes:
            opcoes = candidatos(tarefa)
            opcoes_por_tarefa.append((tarefa, opcoes))

        tarefa, opcoes = min(
            opcoes_por_tarefa,
            key=lambda item: len(item[1])
        )

        if not opcoes:
            return False

        restantes = pendentes.copy()
        restantes.remove(tarefa)

        for opcao in opcoes:
            estatisticas["combinacoes_testadas"] += 1

            grade.append(opcao)
            estatisticas["alocacoes"] += 1

            if backtracking(restantes):
                return True

            grade.pop()                       # RETROCESSO: desfaz a escolha
            estatisticas["retrocessos"] += 1

        return False

    encontrou = backtracking(tarefas)

    if encontrou:
        return grade.copy(), estatisticas

    return None, estatisticas

# EXECUÇÃO E EXIBIÇÃO

def executar_cenario(nome, dados):
    print("\n" + "=" * 55)
    print(nome)
    print("=" * 55)

    grade, estatisticas = resolver_grade(
        disciplinas=dados["disciplinas"],
        salas=dados["salas"],
        horarios=dados["horarios"],
        disponibilidade=dados["disponibilidade"],
        bloqueios=dados["bloqueios"]
    )

    if grade is None:
        print("Não existe uma grade válida para estes dados.")
    else:
        print("Grade encontrada:\n")

        grade_ordenada = sorted(
            grade,
            key=lambda aula: (
                dados["horarios"].index(aula["horario"]),
                aula["sala"]
            )
        )

        print(
            f"{'Disciplina':<27}"
            f"{'Professor':<12}"
            f"{'Horário':<10}"
            f"{'Sala':<10}"
        )
        print("-" * 59)

        for aula in grade_ordenada:
            print(
                f"{aula['disciplina']:<27}"
                f"{aula['professor']:<12}"
                f"{aula['horario']:<10}"
                f"{aula['sala']:<10}"
            )

    print("\nEstatísticas da busca:")
    print("Combinações testadas:", estatisticas["combinacoes_testadas"])
    print("Alocações efetuadas:", estatisticas["alocacoes"])
    print("Retrocessos realizados:", estatisticas["retrocessos"])


def main():
    print("ORGANIZADOR INTELIGENTE DE HORÁRIOS (Backtracking)")
    print("1 - Usar os dados do enunciado (cenários A e B)")
    print("2 - Digitar os dados no terminal")

    escolha = ler_opcao("Escolha uma opção: ", {"1": 1, "2": 2})

    if escolha == 1:
        dados_a = dados_do_enunciado()
        executar_cenario("CENÁRIO A - CONFIGURAÇÃO REGULAR", dados_a)

        dados_b = deepcopy(dados_a)
        dados_b["disponibilidade"]["Ana"] = ["H1", "H2"]
        executar_cenario("CENÁRIO B - CONFIGURAÇÃO RESTRITA", dados_b)
        return

    dados_a = ler_dados_terminal()
    executar_cenario("CENÁRIO A - CONFIGURAÇÃO REGULAR", dados_a)

    resposta = input("\nExecutar um cenário restrito com a disponibilidade "
                     "de um professor alterada? (s/n): ").strip().lower()
    if resposta == "s":
        dados_b = ler_cenario_restrito(dados_a)
        executar_cenario("CENÁRIO B - CONFIGURAÇÃO RESTRITA", dados_b)


if __name__ == "__main__":
    main()