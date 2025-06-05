# Refatoração com github copilot

Refatorar código legado pode ser uma tarefa desafiadora. Neste artigo, vamos explorar como ferramentas de IA, como o GitHub Copilot, podem ajudar nesse processo. Este material foi produzido como parte da disciplina de Metodologias Ágeis, com o objetivo de explorar o uso de LLMs na refatoração de sistemas legados.

---

## Sumário

1. [Sobre Refatoração](#1-sobre-refatoração)
2. [Processo de Refatoração](#2-processo-de-refatoração)
3. [Resultados](#3-resultados)
4. [Considerações](#4-considerações)
5. [Referências](#6-referências)

---

## 1. Sobre Refatoração

Sistemas legados geralmente apresentam alta complexidade, ausência de testes automatizados e o uso de ferramentas obsoletas. A refatoração é uma prática fundamental para entender e evoluir esses sistemas. No entanto, a falta de cobertura de testes torna esse processo ainda mais desafiador.

Embora a solução ideal seja adicionar testes, isso nem sempre é viável, principalmente quando o sistema original não foi projetado para ser testável. Este trabalho propõe combinar a prática de refatoração com o uso de LLMs, mais especificamente o GitHub Copilot Agent, como ferramenta de apoio à modernização de software legado. A abordagem segue os princípios do livro [_Refactoring_](https://refactoring.com/) de Martin Fowler.

---

## 2. Processo de Refatoração

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
   Os resultados gerados pelo Copilot foram comparados com versões refatoradas manualmente, armazenadas em `python_plus_after`.

## 3. Resultados:

#### Técnica: Split Temporary Variable

A técnica dividir variável temporária consiste em substituir uma variável temporária reutilizada para guardar valores diferentes no mesmo método. Veja o exemplo abaixo:

**Código original:**

```python
    temp = 2 * (height + width)
    print(temp)
    temp = height * width
    print(temp)
```

A variável `temp` está sendo utilizada para armazenar dois valores distintos: o perímetro e a área.
Aqui queremos evitar reuso da mesma varável, para evitar confusão e mlehorar legibilidade do código. Veja abaixo:

**Código refatorado:**

```python
    # Split Temporary Variable
    perimeter = 2 * (height + width)
    print(perimeter)
    area = height * width
    print(area)
```

#### Técnica: Replace Conditional With Polymorphism

A técnica _Replace Conditional With Polymorphism_ consiste em substituir estruturas condicionais, como `if` ou `else` por chamadas polimórficas, delegando o comportamento específico para subclasses. Isso melhora a legibilidade e facilita a extensão do código.

O código abaixo utiliza condicionais e centraliza mais de uam responsabilidade:

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

---

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

### 4. Considerações

Na refatoração da função validate\*instance_properties_type, substituímos um conjunto de estruturas if-elif por um dicionário que mapeia tipos e faz conversão. Essa mudança aplica a técnica **Substitute Algorithm**, isolando a lógica de conversão por tipo e deixa o código mais claro.

Além de melhorar a legibilidade, essa abordagem reduz a possibilidade de duplicação de lógica e facilita a manutenção: caso seja necessário adicionar um novo tipo, basta incluir uma nova entrada no dicionário, sem alterar a estrutura principal da função.

Na técnica Remove Assignments To Parameters a refatoração gerada pelo Copilot adicionou o `return result` no final da função, a versão manual não tem essa instrução por se tratar de um exemplo.

Na técnica Extract Method ambas abordagens extraíram um método auxiliar chamado `printDetails`. No entanto, a versão manual passa o valor `outstanding` como parâmetro para o novo método. o Copilot manteve a dependência da classe, acessando diretamente `self.getOutstanding()` ?? analisar a vantagem...

Ao aplicar Replace Conditional With Polymorphism, o Copilot implementa a substituição de condicionais por subclasses específicas para cada tipo de objeto, respeitando os princípios da técnica, a refatoração ficou muito próxima da refatoração manuial.

De modo geral o Copilot apresentou bom desempenho na aplicação das técnicas. Os exemplos acima demonstram que o Copilot é capaz de aplicar refatorações corretamente, em cenários reais a revisão é um processo necessário para garantir boas práticas e para manter o código funcionanado....

### 6. Referências

- [Refactoring.com (Martin Fowler)](https://refactoring.com/)
- [Documentação oficial do Copilot Agent](https://docs.github.com/en/copilot)
- [Coding agent](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

- [Refactoring with Large Language Models (arXiv)](https://arxiv.org/abs/2305.00000)
