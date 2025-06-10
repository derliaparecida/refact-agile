# Refatorando com github copilot agent

> copilot agent , uma ferramenta para automatizar tarefas repetitivas no desenvolvimento de software.

Existem diversas maneiras de usar o copilot, uma das mais comuns é o autocompletar, --utilizo há algum tempo e recomendo, só preste atenção ele pode recomendar alguns códigos estranhos--. Apesar disso, o autocomplete é bastante eficiente para tarefas repetitivas,como geração de logs e testes unitários, especialmente quando sabemos o que deve ser implementado.

Outra forma interessante de uso é por meio de comentários com pequenas dicas, como o nome de um método ou um TODO. Nessas situações, o copilot faz sugestões bastante úteis.

Esses são exemplos de usos mais recorrentes no dia a dia. Agora queremos explorar um desafio maior e mais estruturado: a refatoração de código.

Refatorar é uma técnica utilizada para reestruturar o código, sem modificar seu comportamento. A essência da refatoração é realizar pequenas transformações incrementais, o ideal é que o software refatorado permaneça com o mesmo comportamento após cada iteração.

Considerando as técnicas de refatoração descritas no livro [Refatoração](https://refactoring.com/) vamos analisar como o GitHub Copilot Agent pode nos ajudar nesse processo.

## Sumário

1. [Refatorando](#1-refatorando)
2. [Resultados](#2-resultados)
3. [Conclusão](#3-conclusão)
4. [Referências](#4-referências)

---

## 1. Refatorando

Selecionamos funções do repositório [_RefactoringGuru_](https://github.com/RefactoringGuru/refactoring-examples/tree/main/simple/python) para aplicar diferentes técnicas de refatoração. O processo adotado foi o seguinte:

1. **Isolamento do código original**  
   O código original foi organizado na pasta `python-before`.

2. **Lista de técnicas de refatoração**  
   Criamos um arquivo chamado _`refatoracoes_possiveis.txt`_, contendo uma lista de técnicas de refatoração.

3. **Uso do GitHub Copilot com GPT-4.1**  
   Para minimizar viés, a ordem das técnicas foi embaralhada e o código final manual (_`python-after`_) foi ocultado do modelo. O GitHub Copilot foi instruído com o seguinte contexto:

   - A lista de técnicas possíveis (_`refatoracoes_possiveis.txt`_)
   - O conteúdo da pasta _`python-before`_
   - Um prompt com as instruções:
     > _“Read each file under the folder 'codigos/python-before'. For each file you will generate a new file with suffix '\_copilot' with a refactoring suggestion. The refactoring must be one listed in the file 'refatoracoes_possiveis.txt'. You should write the refactoring name as a comment on the first line of the generated file.”_

4. **Comparação com código de referência**  
   Os resultados gerados pelo Copilot foram comparados com versões refatoradas manualmente, [conferir aqui](https://github.com/RefactoringGuru/refactoring-examples/tree/main/simple/python).

## 2. Resultados

**Problema: reuso de variáveis temporárias:**

No exemplo abaixo, a variável `temp` é usada para armazenar dois valores diferentes: o perímetro e área. Em um sistema maior, esse tipo de reutilização pode causar diversos problemas. O uso de um nome genérico dificulta a compreensão do propósito da variável, especialmente quando ela assume valores distintos ao longo do código. Isso também atrapalha o processo de depuração, pois torna mais difícil entender qual valor está sendo manipulado em cada ponto. Além disso, há o risco de sobrescrever um valor que ainda seria necessário. Esse padrão compromete a legibilidade e a manutenção do código, além de violar o princípio de que cada variável deve ter um único propósito.

**Código original:**

```python
    temp = 2 * (height + width)
    print(temp)
    temp = height * width
    print(temp)
```

#### Técnica: Split Temporary Variable

para o cenário acima a técnica aplicada pelo copilot foi Split Temporary Variable, evitando reuso e melhorando legibilidade do código. Veja abaixo:

**Código refatorado:**

```python
    # Split Temporary Variable
    perimeter = 2 * (height + width)
    print(perimeter)
    area = height * width
    print(area)
```

Neste exemplo, o copilot apresentou um desempenho preciso na refatoraçnao, sua sugestão é a mesma abordagem recomendada pelo [RefactoringGuru](https://github.com/RefactoringGuru/refactoring-examples/blob/main/simple/python/split-temporary-variable_after.py) para a técnica Split Temporary Variable. A substituição da variável genérica `temp` por variáveis com nomes específicos, como `perimeter` e `area`, torna o código mais claro, e aderente às boas práticas de legibilidade e manutenção. Isso demonstra que, para refatorações pontuais e bem definidas, o copilot pode ser um bom apoio na aplicação de padrões reconhecidos.

**Problema: estruturas aninhadas:**

No cenário abaixo temos uma funcão com várias condicionais `if/elif` que tratam diferentes comportamentos de acordo com o tipo de `Bird`, e quais são os problemas? manutenção, extensão do código, a aorganização do código em geral está confusa, e viola o princípio como o Open/Closed Principle (aberto para extensão, fechado para modificação), em cenários reais, quando mais casos são adicionados, o método cresce e se torna mais difícil de testar e compreender isoladamente.

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

#### Técnica: Replace Conditional With Polymorphism

A técnica _Replace Conditional With Polymorphism_ consiste em substituir estruturas condicionais, como `if/elif` por chamadas polimórficas, passando o comportamento específico para cada subclasse. Isso melhora a legibilidade e facilita a extensão do código.

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

Ao aplicar Replace Conditional With Polymorphism, o copilot implementa a substituição de condicionais por subclasses específicas para cada tipo de objeto, respeitando os princípios da técnica, a refatoração ficou muito próxima da inidcada pelo [RefactoringGuru](https://github.com/RefactoringGuru/refactoring-examples/blob/main/simple/python/replace-conditional-with-polymorphism_after.py) .

#### Técnica: Substitute Algorithm em um código real e legado

Para explorar a capacidade do modelo em contextos reais, aplicamos a técnica **Substitute Algorithm** a uma função de um sistema legado [BrainiakAPI](https://github.com/bmentges/brainiak_api) que trata da validação de tipos de propriedades de uma instância. O código original apresenta muitos blocos `if/elif` que verifica o tipo de cada propriedade.

Estruturas condicionais tornam o código repetitivo e aumentam a complexidade da função. Com a técnica **Substitute Algorithm**, vamos tentar melhorar a estrtura.

Função original:

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

**Como ficou após a refatoração:**

- prompt:
  > Refactor the validate_instance_properties_type function using the Substitute Algorithm technique. Ensure the refactored code preserves the original behavior and improves readability

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

Na refatoração da função **validate_instance_properties_type**, o copilot substituiu um conjunto de estruturas `if-elif` por um dicionário que mapeia tipos e faz conversão. Essa mudança aplica a técnica **Substitute Algorithm**, isolando a lógica de conversão por tipo e deixa o código mais claro.

Além de melhorar a legibilidade, essa abordagem reduz a possibilidade de duplicação de lógica e facilita a manutenção: caso seja necessário adicionar um novo tipo, basta incluir no dicionário, sem alterar a estrutura principal da função.

## 3. Conclusão

Ao fazer a mesma análise a todas as técnicas da lista `refatoracoes_possiveis.txt`, o copilot demonstrou um bom desempenho na refatoração. Na tabela:`copilot_x_especialista.xlsx` comparamos a refatoração feita pelo copilot x refatoração manual.

As divergências entre o copilot e a refatoração manual concentram-se na interpretação da intenção da refatoração: enquanto a refatoração manual busca mostrar a técnica com base no conceito — sem garantir a completude do código —, o copilot fez ajustes para que o código fosse funcional. Por exemplo, o copilot interpretou a ausência de um `return` como um erro e inseriu a correção (mostrar técnica). Além da aplicação da técnica, o modelo introduziu pequenas modificações adicionais para tornar o código executável.

De modo geral o copilot apresentou bom desempenho na aplicação das técnicas. Os exemplos acima demonstram que o copilot é capaz de aplicar refatorações corretamente. Em cenários reais, é necessário o processo de revisnao do código gerado para garantir boas práticas e para manter o código funcionanado....

## 4. Referências

- [Refactoring.com (Martin Fowler)](https://refactoring.com/)
- [Copilot Agent](https://docs.github.com/en/copilot)

- [AI-Driven Code Optimization](https://najer.org/najer/article/view/115/121)
- [Leveraging LLMs for Legacy Code Modernization](https://arxiv.org/abs/2411.14971)
- [An Empirical Study on the Potential of LLMs in Automated Software Refactoring](https://arxiv.org/abs/2411.04444)
- [Using Large Language Models to Re-Engineer a Legacy System](https://ieeexplore.ieee.org/abstract/document/10992377)
