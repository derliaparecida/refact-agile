# Refatorando com github copilot agent

> copilot agent , uma ferramenta para automatizar tarefas repetitivas no desenvolvimento de software.

**Data: Junho de 2025**

![removendo coisas](assets/ref.png)

[Créditos aqui](https://www.monkeyuser.com/tags/refactor/)

> Este artigo foi desenvolvido como parte da disciplina **Metodologias Ágeis para o Desenvolvimento de Software**, oferecida no [Programa de Pós-Graduação em Computação Aplicada (PPGCA) da **UTFPR**](https://www.utfpr.edu.br/cursos/programas-de-pos-graduacao/ppgca-ct), ministrada pelo Professor [Adolfo Neto](https://adolfont.github.io/), durante o primeiro semestre de 2025.
>
> Escrito por: [Ana Schwaab](https://github.com/anaschwaab) e [Derli Machado](https://github.com/derliaparecida).

A refatoração contínua é uma prática valorizada dentro das metodologias ágeis por contribuir diretamente para a manutenção da qualidade do software ao longo do tempo. Uma das primeiras metodologias formalizadas foi o Extreme Programming (XP), descrito no livro [Extreme Programming Explained](https://www.oreilly.com/library/view/extreme-programming-explained/0201616416/), de Kent Beck. Nele, a refatoração é apresentada como uma das doze práticas centrais, justamente pelo seu papel em manter o design limpo e adaptável à mudanças frequentes. XP é considerado por autores como Martin Fowler como um [catalisador importante do movimento ágil](https://martinfowler.com/bliki/ExtremeProgramming.html), ajudando a consolidar práticas como desenvolvimento incremental e melhoria contínua. Foi justamente essa conexão entre refatoração e desenvolvimento ágil que motivou a escolha do tema deste trabalho.

Existem diversas maneiras de usar o copilot, uma das mais comuns é o autocompletar, -- **_após utilizar por algum tempo recomendamos prestar atenção, pois o copilot pode recomendar alguns códigos estranhos_** --. Apesar disso, o autocomplete é bastante eficiente para tarefas repetitivas, como geração de logs e testes unitários, especialmente quando sabemos o que deve ser implementado. Essa eficiência, inclusive, já é demonstrada por estudos recentes que mostram que o uso de LLMs para sugestões de código pode aumentar significativamente a produtividade e reduzir erros em tarefas de baixa complexidade [(Vaithilingam et al., 2022](https://www.researchgate.net/publication/360267490_Expectation_vs_Experience_Evaluating_the_Usability_of_Code_Generation_Tools_Powered_by_Large_Language_Models); [Jaffe et al., 2024)](https://www.microsoft.com/en-us/research/wp-content/uploads/2024/07/Generative-AI-in-Real-World-Workplaces.pdf).

Outra forma interessante de uso é por meio de comentários com pequenas dicas, como o nome de um método ou um TODO. Nessas situações, o copilot faz sugestões bastante úteis.

Mais recentemente, essas capacidades foram ampliadas com a introdução do **Agent**. Este novo modo permite que a ferramenta vá além das sugestões pontuais: ela pode editar múltiplos arquivos, entendendo o contexto do projeto e fazendo mudanças estruturais.

Esse avanço amplia o potencial de uso de LLMs em tarefas mais sofisticadas. Refatorar significa melhorar a estrutura interna do código sem alterar seu comportamento, um conceito central na engenharia de software que tem sido explorado com LLMs como ferramenta de apoio [(Kass, 2025)](https://www.authorea.com/doi/full/10.22541/au.174768395.52918781). É também uma prática para manter a legibilidade, reduzir problemas técnicos e facilitar manutenções. A ideia é começar com tarefas pequenas preservando o funcionamento do código e evoluir para tarefas mais complexas.

Ainda que com limitações em segurança e precisão, a capacidade de LLMs de identificar e aplicar refatorações automaticamente já foi demonstrada em estudos recentes [(Liu et al., 2023)](https://www.researchgate.net/publication/385629991_An_Empirical_Study_on_the_Potential_of_LLMs_in_Automated_Software_Refactoring).

Neste artigo, exploramos o uso do _GitHub Copilot Agent - GPT-4.1_ como ferramenta de apoio à refatoração de código. Combinando teoria e prática, avaiamos a eficácia do agente em aplicar técnicas clássicas de refatoração do livro [Refatoração](https://refactoring.com/) de Martin Fowler. Para isso, utilizamos trechos de código representativos de problemas comuns no desenvolvimento de software, além de utilizar a ferramenta em um cenário real. O objetivo é entender o potencial dessas ferramentas baseadas em modelos de linguagem para apoiar a manutenção e evolução de sistemas.

O processo é interativo:

- Você descreve o que precisa ser feito;
- Adiciona arquivos ou diretórios no contexto que deseja alterar;
- Analisa os _diffs_ gerados;
- Revisa, adapta e decide se aceita ou rejeita as sugestões.

Seguindo este processo, primeiro passamos para o Copilot uma lista de técnicas de refatoração e analisamos alguns exemplos da lista. Os demais casos são resumidos em uma tabela, mostrando acertos e erros. E para testar a ferramenta em um cenário real, usamos uma [API](<(https://github.com/bmentges/brainiak_api)>) e aplicamos a refatoração para remover a integração com um banco de dados.

## Sumário

1. [Como estruturamos os testes](#1-como-estruturamos-os-testes)
2. [Análise das refatorações](#2-análise-das-refatorações)  
     2.1 [Análises de exemplos de código do RefactoringGuru](#21-análises-de-exemplos-de-código-do-refactoringguru)  
       2.1.1 [Split Temporary Variable: substituindo variável com múltiplos usos](#211-split-temporary-variable-substituindo-variável-com-múltiplos-usos)  
       2.1.2 [Replace Conditional With Polymorphism: delegando lógica específica para subclasses](#212-replace-conditional-with-polymorphism-delegando-lógica-específica-para-subclasses)  
       2.1.3 [Replace Temp With Query: removendo variáveis temporárias desnecessárias](#213-replace-temp-with-query-removendo-variáveis-temporárias-desnecessárias)  
       2.1.4 [Replace Magic Number With Symbolic Constant: dando significado a números "mágicos"](#214-replace-magic-number-with-symbolic-constant-dando-significado-a-números-mágicos)  
       2.1.5 [Extract Method: separando blocos com responsabilidades distintas](#215-extract-method-separando-blocos-com-responsabilidades-distintas)  
       2.1.6 [Replace Exception With Test: eliminando uso de exceções para controle de fluxo](#216-replace-exception-with-test-eliminando-uso-de-exceções-para-controle-de-fluxo)  
       2.1.7 [Tabela comparativa de todas as técnicas](#217-tabela-comparativa-de-todas-as-técnicas)  
     2.2 [Reestruturando uma API alterando multiplos arquivos](#22-reestruturando-uma-api-alterando-multiplos-arquivos)  
     2.3 [Removendo a integração com o Banco de Dados Neptune](#23-removendo-a-integracao-com-o-banco-de-dados-neptune)
3. [Conclusão](#3-conclusão)  
   3.1 [Tempo e custo da refatoração com o Copilot Agent](#31-tempo-e-custo-da-refatoração-com-o-copilot-agent)

4. [Saiba mais](#4-saiba-mais)

---

## 1. Como estruturamos os testes

Para realizar os testes, organizamos o código original na pasta `python-before`, criamos também um arquivo chamado `refatoracoes_possiveis.txt`, contendo a lista embaralhada de técnicas de refatoração. Em seguida, utilizamos o GitHub Copilot com o modelo GPT-4.1, e para evitar viés ocultamos o código original refatorado (`python`) durante o processo. Passamos para o Copilot como contexto a lista das técnicas, o conteúdo da pasta `python-before` e um prompt com instruções.

- Prompt utilizado:
  > _“Read each file under the folder 'codigos/python-before'. For each file you will generate a new file with suffix '\_copilot' with a refactoring suggestion. The refactoring must be one listed in the file 'refatoracoes_possiveis.txt'. You should write the refactoring name as a comment on the first line of the generated file.”_

## 2. Análise das refatorações

### 2.1 Análises de exemplos de código do RefactoringGuru

Selecionamos funções python do repositório [_RefactoringGuru_](https://github.com/RefactoringGuru/refactoring-examples/tree/main/simple/python), que reúne exemplos práticos de código, baseado no livro Refatoração. A intenção desta etapa é avaliar a capacidade do Copilot em aplicar as técnicas de refatoração descritas no livro. Para isso, vamos comparar as sugestões do Copilot com as versões refatoradas manualmente disponíveis no repositório.

#### 2.1.1 Split Temporary Variable: substituindo variável com múltiplos usos

No código abaixo, a variável `temp` é usada para armazenar dois valores: o perímetro e área. Isso torna o código mais difícil de entender, especialmente porque o nome genérico da variável não revela seu propósito. Essa prática pode dificultar o processo de depuração, aumentar o risco de sobrescrita do valor e compromete a legibilidade — além de violar o princípio de responsabilidade única.

**Código original:**

```python
    temp = 2 * (height + width)
    print(temp)
    temp = height * width
    print(temp)
```

> Um valor utilizado para diferentes própósitos, é um tereno fértil para confusão e bugs, - então, quando vejo um, utilizo _Split Variable_ para separar o uso.
>
> Martin Folwer.

**Código refatorado:**

```python
    # Split Temporary Variable
    perimeter = 2 * (height + width)
    print(perimeter)
    area = height * width
    print(area)
```

Neste exemplo, o copilot manteve a mesma abordagem do [RefactoringGuru](https://github.com/RefactoringGuru/refactoring-examples/blob/main/simple/python/split-temporary-variable_after.py). A substituição da variável genérica `temp` por variáveis com nomes específicos, torna o código mais claro e cada variável fica com uma responsabilidade, tornando o processo de leitura do código mais claro.

#### 2.1.2 Replace Conditional With Polymorphism: delegando lógica específica para subclasses

![Processo da refatoração](assets/large-class-01.png)

[Créditos aqui](https://refactoring.guru/smells/large-class)

No cenário abaixo temos uma funcão com várias condicionais `if/elif` que tratam diferentes comportamentos de acordo com o tipo de `Bird`. Problema: essa classe dificulta manutenção, extensão do código, a organização do código em geral está confusa, e viola o princípio como o [Open/Closed Principle](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle). Em cenários reais, quando mais casos são adicionados, o método cresce e se torna mais difícil de testar e compreender isoladamente.

**Código original:**

```python
class Bird:
    def getSpeed(self):
        if self.type == EUROPEAN:
            return self.getBaseSpeed()
        elif self.type == AFRICAN:
            return self.getBaseSpeed() - self.getLoadFactor() * self.numberOfCoconuts
        elif self.type == NORWEGIAN_BLUE:
            return 0 if self.isNailed else self.getBaseSpeed(self.voltage)
        else:
            raise Exception("Should be unreachable")
```

A técnica acima consiste em substituir estruturas condicionais, como `if/elif` por chamadas polimórficas, passando o comportamento específico para cada subclasse. Isso melhora a legibilidade e facilita a extensão do código.

**Código refatorado:**

```python
    class Bird:
        def getSpeed(self):
            raise NotImplementedError()

    class European(Bird):
        def getSpeed(self):
            return self.getBaseSpeed()

    class African(Bird):
        def getSpeed(self):
            return self.getBaseSpeed() - self.getLoadFactor() * self.numberOfCoconuts

    class NorwegianBlue(Bird):
        def getSpeed(self):
            return 0 if self.isNailed else self.getBaseSpeed(self.voltage)
```

O copilot implementa a substituição de condicionais por subclasses específicas para cada tipo de objeto, respeitando os princípios da técnica, a refatoração ficou muito próxima da indicada pelo [RefactoringGuru](https://github.com/RefactoringGuru/refactoring-examples/blob/main/simple/python/replace-conditional-with-polymorphism_after.py).

#### 2.1.3 Replace Temp With Query: removendo variáveis temporárias desnecessárias

No código original, a função `calculateTotal` utiliza uma variável temporária chamada `basePrice` apenas para armazenar o resultado de uma expressão que poderia ser calculada diretamente (quantity \* itemPrice). Essa variável pode ser substituída por uma query que encapsula a lógica, melhorando a clareza e a coesão do código.

**Código original:**

```python
    def calculateTotal():
        basePrice = quantity * itemPrice
        if basePrice > 1000:
            return basePrice * 0.95
        else:
            return basePrice * 0.98
```

O copilot utilizou a técnica `Replace Temp With Query`, substituindo a variável `basePrice` diretamente pela expressão lógica.

**Código refatorado:**

```python
    # Replace Temp With Query
    def calculateTotal():
        if quantity * itemPrice > 1000:
            return quantity * itemPrice * 0.95
        else:
            return quantity * itemPrice * 0.98
```

Apesar do copilot substituir corretamente a variável `basePrice` pela expressão lógica, falhou em encapsular essa lógica em um método que poderia ser reutilizado no código, como é indicado pelo [RefactoringGuru](https://github.com/RefactoringGuru/refactoring-examples/blob/main/simple/python/replace-temp-with-query_after.py). Isso mostra que o Copilot foi capaz de compreender o problema da variável temporária, mas não soube propor a melhor abstração para legibilidade e manutenção.

#### 2.1.4 Replace Magic Number With Symbolic Constant: dando significado a números "mágicos"

No código original, a constante `9.81` aparece de forma "solta" dentro da fórmula de cálculo da energia potencial. Esse valor representa a aceleração gravitacional na Terra, mas como está escrito diretamente no cálculo, é conhecido como **número mágico** - um valo numérico usado sem contexto explícito. Esse tipo de prática prejudica a legibilidade, dificulta manutenção e reutilização desse valor além de reduz a clareza semântica do código.

**Código original:**

```python
    def potentialEnergy(mass, height):
        return mass * height * 9.81
```

O Copilot aplicou a técnica `Replace Magic Number With Symbolic Constant`, atrelando o valor da aceleração gravitacional na Terra à variável `GRAVITY`.

**Código refatorado:**

```python
    # Replace Magic Number With Symbolic Constant
    GRAVITY = 9.81

    def potentialEnergy(mass, height):
        return mass * height * GRAVITY
```

Neste exemplo, o Copilot aplicou a técnica `Replace Magic Number With Symbolic Constant` e seu código difere do proposto pelo [RefactoringGuru](https://github.com/RefactoringGuru/refactoring-examples/blob/main/simple/python/replace-magic-number-with-symbolic-constant_after.py) apenas no nome da variável, enquanto o especialista utilizou o nome `GRAVITATIONAL_CONSTANT`, o Copilot escolheu `GRAVITY`, e neste caso, podemos considerar que ambos os nomes tem poder explicativo para a variável.

#### 2.1.5 Extract Method: separando blocos com responsabilidades distintas

No código original, o método `printOwing` realiza duas tarefas: exibe um banner e imprime os detalhes do cliente (nome e valor devido). Esse tipo de método com múltiplas responsabilidades prejudica a legibilidade e dificulta testes e manutenção.

**Código original:**

```python
    def printOwing(self):
        self.printBanner()

        # print details
        print("name:", self.name)
        print("amount:", self.getOutstanding())
```

O Copilot aplicou a técnica `Extract Method`, encapsulando os prints em um novo método `printDetails`.

**Código refatorado:**

```python
    # Extract Method
    def printOwing(self):
        self.printBanner()
        self.printDetails()


    def printDetails(self):
        print("name:", self.name)
        print("amount:", self.getOutstanding())
```

O Copilot aplicou corretamente a técnica `Extract Method` mas seu código difere do proposto pelo [RefactoringGuru](https://github.com/RefactoringGuru/refactoring-examples/blob/main/simple/python/extract-method_after.py), pois enquanto o Guru extraiu o valor retornado por `getOutstanding()` passando como argumento para `printDetails`, o Copilot manteve o cálculo dentro do novo método, o que reduz a flexibilidade e dificulta o resuo do método extraído. Ainda assim o Copilot demonstrou boa capacidade em detectar e isolar responsabilidades.

#### 2.1.6 Replace Exception With Test: eliminando uso de exceções para controle de fluxo

O código original utiliza um bloco `try/except` para capturar `IndexError`. Esse padrão é problemático porque usa exceções para tratar fluxos esperados do programa, como o acesso a uma posição inexistente em uma lista. Embora válido, o uso compromate a clareza do código e pode impactar negativamente a performance.

```python
    def getValueForPeriod(periodNumber):
    try:
        return values[periodNumber]
    except IndexError:
        return 0
```

Segundo o _RefactoringGuru_, a refatoração correta consistiria em substituir o uso da exceção por uma verificação explícita, utilizando a técnica [Replace Exception With Test](https://github.com/RefactoringGuru/refactoring-examples/blob/main/simple/python/replace-exception-with-test_after.py), no entanto o copilot sugeriu o seguinte código:

```python
    # Replace Error Code With Exception
    def getValueForPeriod(periodNumber):
        try:
            return values[periodNumber]
        except IndexError:
            raise Exception("Invalid period number")
```

Nesse caso, o copilot aplicou uma técnica diferente: `Replace Error Code With Exception`, substituindo o valor do retorno por uma exceção explícita. Isso mostra que o modelo foi capaz de identificar que havia um padrão a ser transformado, mas não reconheceu corretamente qual téncica de refatoração era mais adequada ao contexto. O copilot não entendeu que o uso da exceção era o problema em si, mas sim que a resposta ao erro era insuficiente. Nesse caso, a refatoração tem um sentido técnico, mas falha em determinar o problema no código. Isso evidencia uma limitação importante: o copilot pode sugerir refatorações corretas, mas desalinhadas da intenção original.

#### 2.1.7 Tabela comparativa de todas as técnicas

Após a análise individual de cada técnica, organizamos os resultados da etapa 2.1 na tabela abaixo. Para cada caso, consideramos como acerto quando o Copilot aplicou a técnica correta com clareza e manteve o comportamento do código, mesmo que não tenha seguindo exatamente a implementação esperada ou sugerida pelo _RefactoringGuru_.

| Técnica de Refatoração                        | Copilot     | Referência |
| --------------------------------------------- | ----------- | ---------- |
| Consolidate Conditional Expression            | Correta     | Diferente  |
| Consolidate Duplicate Conditional Fragments   | Correta     | Diferente  |
| Decompose Conditional                         | Correta     | Diferente  |
| Extract Class                                 | Parcial     | Diferente  |
| Extract Method                                | Correta     | Diferente  |
| Inline Method                                 | Correta     | Igual      |
| Inline Temp                                   | Correta     | Igual      |
| Introduce Assertion                           | Correta     | Igual      |
| Introduce Foreign Method                      | Correta     | Diferente  |
| Introduce Null Object                         | Correta     | Diferente  |
| Preserve Whole Object                         | Correta     | Igual      |
| Pull Up Constructor Body                      | Correta     | Diferente  |
| Remove Assignments To Parameters              | Correta     | Igual      |
| Replace Array With Object                     | Correta     | Diferente  |
| Replace Conditional With Polymorphism         | Correta     | Igual      |
| Replace Error Code With Exception             | Correta     | Diferente  |
| Replace Exception With Test                   | Não aplicou | —          |
| Replace Magic Number With Constant            | Correta     | Igual      |
| Replace Method With Method Object             | Correta     | Igual      |
| Replace Nested Conditional With Guard Clauses | Correta     | Igual      |
| Replace Parameter With Explicit Methods       | Correta     | Igual      |
| Replace Parameter With Method Call            | Correta     | Diferente  |
| Replace Temp With Query                       | Correta     | Diferente  |
| Split Temporary Variable                      | Correta     | Igual      |
| Substitute Algorithm                          | Correta     | Diferente  |

## 2.2 Reestruturando uma API alterando multiplos arquivos

Para explorar o copilot agent em um contexto mais complexo e real, vamos utilizar o [BrainiakAPI](https://github.com/bmentges/brainiak_api), uma API da [Globo](https://www.globo.com/) voltada para manipulação de dados semânticos. Essa API é responsável por várias operações: CRUD, permalinks, buscas, sugestões e consultas parametrizadas, e faz integração com bancos de dados: [Neptune](https://docs.aws.amazon.com/neptune/) e [Elasticsearch](https://www.elastic.co/elasticsearch). Na Globo, o Neptune é utilizado para armazenar dados em grafo, seguindo o modelo [RDF](https://www.w3.org/RDF/). O Elasticsearch é usado para buscas rápidas e indexação de dados.

Vamos olhar para uma função da API e refatorar...

Vamos começar com um exemplo simples, a função `validate_instance_properties_type` é responsável por garantir que os valores de uma instância estejam de acordo com os tipos definidos no `props_type`. Para isso, ela percorre cada propriedade da instância e verifica, com `if/elif`, se o valor está no formato esperado (lista, string, número ou booleano). Se não estiver, a função converte o valor.

Vamos refatorar para deixar a estrutura da função mais legível e fácil de reutilizar.

**Código original:**

```python
def validate_instance_properties_type(instance, props_type):
    for k, v in instance.items():
        if k in props_type["properties"]:
            if props_type["properties"][k]["type"] == "array":
                if not isinstance(v, list):
                    instance[k] = [v]
            elif props_type["properties"][k]["type"] == "string":
                if not isinstance(v, str):
                    instance[k] = str(v)
            elif props_type["properties"][k]["type"] == "number":
                if not isinstance(v, int):
                    instance[k] = int(v)
            elif props_type["properties"][k]["type"] == "boolean":
                if not isinstance(v, bool):
                    instance[k] = bool(v)

    return instance

```

- prompt:
  > Refactor the validate_instance_properties_type function using the Substitute Algorithm technique. Ensure the refactored code preserves the original behavior and improves readability

**Código refatorado:**

```python
def validate_instance_properties_type(instance, props_type):
    type_converters = {
        "array": lambda v: v if isinstance(v, list) else [v],
        "string": lambda v: v if isinstance(v, str) else str(v),
        "number": lambda v: v if isinstance(v, int) else int(v),
        "boolean": lambda v: v if isinstance(v, bool) else bool(v),
    }

    for k, v in instance.items():
        if k in props_type["properties"]:
            prop_type = props_type["properties"][k]["type"]
            if prop_type in type_converters:
                instance[k] = type_converters[prop_type](v)

    return instance

```

O copilot substituiu o conjunto de estruturas `if-elif` por um dicionário que mapeia tipos e faz conversão, aplicando a técnica **Substitute Algorithm**.

A função é a mesma, mas a refatoração torna a estrutura do método mais claro, o mapeamanto ficou separado da iteração, o que evita repetição e permite que a extenção do código possa ser feito de forma mais segura.

## 2.3 Removendo a integração com o Banco de Dados Neptune

Para ir um pouco além, vamos remover uma funcionalidade de um _handler_ . No arquivo `handler-antes.py`, temos um trecho de código responsável por gerenciar a comunicação entre os dois bancos de dados: Neptune e Elasticsearch.

Esse handler é responsável por manter a consistência entre os dois bancos, garantindo que as operações reflitam em ambas as bases. Nosso objetivo é remover a lógica relacionada ao Neptune, mantendo apenas a comunicação com o Elasticsearch.

![Processo da refatoração](assets/dead-code-01.png)

[Créditos aqui](https://refactoring.guru/smells/dead-code)

A primeira interação com o Copilot Agent foi:

> **Refatore o `InstanceHandlerES` removendo a comunicação com Neptune.**

Durante esse processo, o copilot analisou o arquivo e removeu as chamadas e importações relacionadas ao Neptune.

![Processo da refatoração](assets/ex1.png)

Depois de aceitar as sugestões, passamos um novo prompt:

> **Revise todos os arquivos da pasta `brainiak` e remova as dependências do Neptune.**

Esse segundo passo envolveu alterações em 14 arquivos diferentes. O copilot identificou e editou os pontos de dependência distribuídos no projeto.

![Processo de remoção](assets/ex2.png)

A reestruturacão resultou na remoção de muito código, o que exigiu uma revisão mais cuidadosa. Durante a revisão, identificamos que ainda restavam algumas referências ao Neptune, o que exigiu instruções adicionais para fazer a remoção completa.

**E por que remover o Neptune?**

A decisão de remover o Neptune da aplicação faz parte de uma estratégia de modernização da infraestrutura semântica da Globo. Atualmente, temos cerca de 15 grafos que sustentam páginas como o [Tudo Sobre](https://g1.globo.com/tudo-sobre/ministerio-da-justica-e-seguranca-publica/), e enriquecem conteúdos em produtos como o [G1](https://g1.globo.com/mundo/noticia/2025/06/17/quem-era-ali-shadmani-lider-militar-iraniano-que-israel-anunciou-ter-matado.ghtml), conectando entidades e temas relacionados. Por um bom tempo, o Neptune foi o banco usado para manter a base semântica, mas a aplicação foi ganhando novas responsabilidades:`ifs, elses e mais ifs`, e com isso 2 problemas surgiram: custo do banco e manutenção da API.

Diante disso, decidimos repensar a semântica Globo, e estamos no processo de reestruturação, avaliando outros formatos, como taxonomias ou vocabulários controlados, e enquanto pensamos, optamos por manter apenas o Elasticsearch. A estratégia adotada foi a migração por paths, onde as queries [SPARQL](https://www.w3.org/TR/sparql11-query/) foram substituídas por consultas adaptadas para o ES, e este foi o primeiro passo da reestruturação semantica.

O segundo passo foi a limpeza do código, e nesta fase usamos o copilot agent para elimiar as dependências do Neptune de forma mais rápida.

## 3. Conclusão

> Para realmente funcionar de modo ágil, uma equipe deve ser capacitada a fazer refatorações e ser entusiasmada com elas - e, para isso, muitos aspectos de seu processo devem estar alinhados com fazer as refatorações como parte constante do seu trabalho.
>
> Martin Fowler

Em todo processo de refatoração, o **Github Copilot Agent** demonstrou boa capacidade para entender o contexto das tarefas. Nos exemplos acima, vimos que, em tarefas pontuais como modificar uma função ou aplicar uma técnica de refatoração isolada, a ferramenta é bastante útil e suas sugestões são fáceis de entender e avaliar.

Neste aspecto o _copilot agent_ pode ajudar no hábito de refatorar com mais frequência, alinhando com práticas ágeis como melhorias incrementais.

Já em contextos mais complexos, como a reestruturação de múltiplos arquivos, precisamos ter mais cuidado. Na execusão acima, estavamos bastante familiarizadas com o código, foi mais fácil decidir quando aceitar ou rejeitar as sugestões.

E este cenário nos leva a uma pergunta respondida no livro de Fowler: **Quando refatorar?** o autor reforça que depende, pois refatorar deve sempre ter um propósito claro, e precisamos responder se vale o custo.

### 3.1 Tempo de refatoraçao do Copilot Agent

A aplicação das técnicas de refatoração listadas levou cerca de 1 minuto e meio com o Copilot Agent, demonstrando agilidade nas tarefas pontuais. Já no caso da refatoração da API, a primeira interação (removendo a integração com o banco Neptune em um único arquivo) levou cerca de 30 segundos. No entanto, ao solicitar a remoção completa de todas as referências ao Neptune, o processo se estendeu: o Copilot passou a realizar sugestões por etapas e interrompeu a execução em alguns momentos para confirmar se deveria continuar. Considerando essas pausas e as revisões necessárias, essa fase levou aproximadamente 1 hora, seguida por novas interações para eliminar referências restantes.

### 3.1 Tempo e Custo da Refatoração com Copilot Agent

A aplicação das técnicas de refatoração, levou **menos de um minito**. Já no caso da refatoração da API, a primeira interação levou cerca de **30 segundos**. No entanto, ao solicitar a remoção completa de todas as referências ao Neptune, o processo foi um pouco mais demorado: o Copilot passou a realizar sugestões por etapas e interrompendo a execução em alguns momentos para confirmar se deveria continuar. Considerando essas pausas e as revisões necessárias, essa fase levou aproximadamente **1 hora**, seguida por novas interações para eliminar referências restantes. Algo interessante de cometar é que Copilot Agent é uma ferramenta paga, e para o uso de modelos mais robustos, como o GPT-4.1 que foi utilizado, temos um limite de uso, par ao plano empresarial. Ou seja, a cada request estamos gastando o limite .... além do plano bussines, existem tbm diferentes [planos](https://docs.github.com/pt/copilot/about-github-copilot/plans-for-github-copilot), com versão gratuita com recursos limitados e opções pagas voltadas para usuários individuais

### 3.1 Tempo e custo da refatoração com o Copilot Agent

A aplicação das técnicas clássicas de refatoração levou **menos de um minuto**. No caso da refatoração da API, a primeira solicitação — removendo um `if` da lógica de comunicação com o Neptune — levou cerca de **30 segundos**. Porém, na remoção completa das referências do banco, o processo foi mais demorado: o Copilot passou a sugerir mudanças em etapas e interrompendo a execução em alguns momentos para confirmar se deveria continuar. Com as pausas e as revisões necessárias, essa etapa levou cerca de **1 hora**, seguida de interações adicionais para eliminar referências que restaram que não foram cronometradas.

É importante destacar que o Copilot Agent é uma ferramenta paga e, no plano empresarial (**Copilot Business**), o uso de modelos mais robustos como o **GPT-4.1** tem limite de uso **300 _premium requests_** por usuário. Cada requisição consome parte da cota. Além do plano Business, o GitHub oferece [outros planos](https://docs.github.com/pt/copilot/about-github-copilot/plans-for-github-copilot), incluindo uma versão gratuita com recursos limitados e opções pagas voltadas para planos individuais.

## 4. Saiba Mais

- [Refactoring.com (Martin Fowler)](https://refactoring.com/) — Livro do Martin Fowler sobre refatoração de código. Tenho esse livro há bastante tempo e sempre recorro a ele quando me deparo com um código difícil de alterar. Na primeira vez em que li, foi uma leitura contínua, passando pelas técnicas e tentando entender o que estava acontecendo. Com um pouco mais de experiência, sempre que encontro um código complicado, lembro e uso o livro como referência para refatorar.

- [GitHub Copilot Agent](https://docs.github.com/en/copilot) — Documentação oficial do Copilot. Na documetação é possível ter uma visão completa das funcionalidades oferecidas pela ferramenta, incluindo um [guia de início](https://docs.github.com/en/copilot/quickstart) dos recursos disponíveis. Durante a escrita deste artigo, buscamos uma API oficial do Copilot que permitisse automatizar o processo de refatoração, mas não encontramos. Em discussões em blogs e issues, vimos que o GitHub não oferece esse tipo de automação, o foco da ferramenta está no uso interativo, via prompts.

- [Refactoring.Guru](https://refactoring.guru/) O site Refactoring Guru é uma fonte bastante didática sobre refatoração e padrões de projeto. Para cada situação, ele apresenta explicações claras sobre quando e por que aplicar determinada técnica, seja relacionada à refatoração ou design patterns, recomendamos a visita.

- [Exploring GenAI: Multi-file Editing](https://martinfowler.com/articles/exploring-gen-ai/11-multi-file-editing.html) — Este post faz parte de uma [série](<(https://martinfowler.com/articles/exploring-gen-ai.html)>) publicada no blog do Martin Fowler sobre o uso de LLMs no desenvolvimento de software. A série documenta o uso de algumas ferramentas, como o copilot agent, compartilha aprendizados e reflexões sobre o uso.

- Artigos que abordam o uso de LLMs: Encontramos támbém alguns artigos interessantes que exploram na pratica o uso de LLMs para refatoração e modernização de código:

  - [Leveraging LLMs for Legacy Code Modernization](https://arxiv.org/abs/2411.14971) — Este artigo analisa como LLMs podem ajudar na documentação de sistemas legados escritos nas linguagens: MUMPS e Assembly para mainframe. Ao ler o artigo, testei o coplit agent para escrever um readme de uma app e o teste foi bem sucedido.

  - [An Empirical Study on the Potential of LLMs in Automated Software Refactoring](https://arxiv.org/abs/2411.04444) — Este artigo testa a capacidade do ChatGPT-4 e Gemini-1.0, o estudo envolveu aplicar técnivas de refatoração para um conjunto de dados a avaliar as sugestões dos modelos.
