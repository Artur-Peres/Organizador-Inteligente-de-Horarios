# Explicação do código: Organizador Inteligente de Horários

## 1. Ideia geral

O programa monta uma grade de horários usando backtracking. Ele vai escolhendo, uma aula por vez, um horário e uma sala que não quebrem nenhuma regra. Quando chega num ponto em que alguma aula não tem mais onde ser colocada, ele desfaz a última escolha e tenta outra. Se todas as possibilidades se esgotarem, ele avisa que não existe grade válida.

## 2. Como os dados entram no programa

Ao executar, o programa mostra um menu com duas opções:

- **Opção 1:** usa os dados do enunciado e roda os cenários A e B em sequência.
- **Opção 2:** o usuário digita os dados no terminal: horários, salas (laboratório ou comum), disciplinas (professor, número de aulas e ambiente), disponibilidade de cada professor e bloqueios de sala. Depois do cenário A, o programa pergunta se queremos rodar um cenário restrito, em que escolhemos um professor e informamos os novos horários dele.

Os dados ficam em estruturas separadas (listas, dicionários e um conjunto), e a busca só lê essas estruturas. Por isso dá para trocar completamente o problema sem mexer na lógica do algoritmo. Também há validação: se o usuário digitar um horário que não existe, uma sala que não foi cadastrada ou um número inválido, o programa pede de novo.

## 3. Como o problema foi modelado

Cada disciplina tem duas aulas, então o programa transforma cada aula em uma tarefa separada. São 6 disciplinas, logo 12 tarefas. Fazer assim facilita garantir que as duas aulas da mesma disciplina caiam em horários diferentes.

Uma alocação é um conjunto de quatro informações: disciplina, professor, horário e sala. A grade é a lista das alocações já feitas.

## 4. Restrições implementadas

A função `candidatos()` gera, para uma tarefa, todas as combinações de horário e sala que ainda são possíveis naquele momento. Uma combinação só entra na lista se passar nestas verificações:

- o professor está disponível naquele horário;
- o professor não tem outra aula no mesmo horário;
- a disciplina ainda não tem aula nesse horário;
- a sala não está bloqueada nesse horário;
- a sala não tem outra aula no mesmo horário;
- se a disciplina exige laboratório (Redes e Programação Web), a sala precisa ser um laboratório.

Assim a busca nunca tenta algo que já seria inválido de saída.

## 5. O backtracking

A função `backtracking()` recebe as aulas que faltam alocar e funciona assim:

1. Se não falta nenhuma aula, a grade está completa e a busca termina com sucesso.
2. Se falta alguma, o programa calcula as combinações possíveis de cada aula pendente e escolhe a que tem menos opções (explicamos isso no próximo item).
3. Se essa aula não tem nenhuma opção, aquele caminho não leva a lugar nenhum e a função devolve falha.
4. Se tem opções, testa uma por uma. Coloca a combinação na grade e chama `backtracking()` de novo para as aulas restantes.
5. Se a chamada seguinte devolver sucesso, tudo certo. Se devolver falha, a escolha é desfeita e passa para a próxima opção.

**O retrocesso acontece no passo 5**, nas duas linhas logo depois da chamada recursiva: `grade.pop()`, que remove a última alocação, e `estatisticas["retrocessos"] += 1`, que registra que uma decisão foi desfeita. Se todas as opções de uma aula falharem, a função devolve falha para quem a chamou, e aí a decisão anterior é que será desfeita, e assim por diante.

## 6. Escolha da próxima aula (MRV)

Em vez de seguir a ordem da lista, o programa sempre escolhe a aula que tem menos combinações possíveis naquele momento. Essa estratégia se chama MRV (Minimum Remaining Values). A vantagem é que as aulas mais difíceis de encaixar são tratadas primeiro, e os becos sem saída aparecem mais cedo, antes de a busca gastar tempo em decisões que não ajudavam.

## 7. Estatísticas

O programa conta três coisas durante a busca:

- **Combinações testadas:** quantas combinações foram experimentadas.
- **Alocações efetuadas:** quantas vezes uma aula foi colocada na grade.
- **Retrocessos:** quantas vezes uma alocação foi desfeita.

Do jeito que o código está, cada combinação testada vira uma alocação na mesma hora, então os dois primeiros números sempre saem iguais. A diferença que mostra o comportamento da busca é a dos retrocessos.

## 8. Resultados dos cenários

**Cenário A (configuração regular):** o programa encontrou uma grade completa com as 12 aulas. Foram 12 combinações testadas, 12 alocações e nenhum retrocesso. Isso aconteceu porque o MRV escolheu bem a ordem e a primeira opção de cada aula já servia. O retrocesso continua no código e é ele que aparece no cenário B.

**Cenário B (configuração restrita):** a disponibilidade da Ana passa a ser só H1 e H2. Ela dá Banco de Dados e Redes, que somam 4 aulas, e um professor não pode dar duas aulas ao mesmo tempo. Com apenas dois horários, é impossível. Mesmo assim o programa precisa chegar a essa conclusão pela busca: foram 7 combinações testadas, 7 alocações e 7 retrocessos, e no fim ele exibe a mensagem de que não existe grade válida.

## 9. Conclusão

O programa explora as possibilidades, desfaz as decisões que não funcionam e reconhece quando não há solução. Como os dados podem ser digitados no terminal, ele funciona para outros conjuntos de dados e não só para os dois cenários do enunciado.
