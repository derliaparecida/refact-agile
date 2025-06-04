# Refatoração com github copilot

Este material foi produzido como parte da disciplina de Metodologias Ágeis, com o objetivo de explorar o uso de Modelos de Linguagem de Grande Escala (LLMs) na refatoração de sistemas legados.

---

## Sumário

1. [Sobre Refatoração](#1-sobre-refatoração)
2. [Processo de Refatoração](#2-processo-de-refatoracao)
3. [Boas Práticas no Uso de LLMs](#3-boas-práticas-no-uso-de-llms)
4. [Limitações e Cuidados](#4-limitações-e-cuidados)
5. [Reproduzibilidade e Ambiente](#5-reproduzibilidade-e-ambiente)
6. [Referências](#6-referências)

---

## 1. Sobre Refatoração

Sistemas legados geralmente apresentam alta complexidade, ausência de testes automatizados e o uso de ferramentas obsoletas. A refatoração é uma prática fundamental para entender e evoluir esses sistemas. No entanto, a falta de cobertura de testes torna esse processo ainda mais desafiador.

Embora a solução ideal seja adicionar testes, isso nem sempre é viável, principalmente quando o sistema original não foi projetado para ser testável. Este trabalho propõe combinar a prática de refatoração com o uso de LLMs, mais especificamente o GitHub Copilot Agent, como ferramenta de apoio à modernização de software legado. A abordagem segue os princípios do livro [_Refactoring_](https://refactoring.com/) de Martin Fowler.

---

## 2. Processo de refatoração

Selecionamos funções do repositório [RefactoringGuru](https://github.com/RefactoringGuru/refactoring-examples/tree/main) para aplicar diferentes técnicas de refatoração. O processo adotado foi o seguinte:

1. **Isolamos do código original**  
   O código original foi organizado na pasta `python-before`.

2. **Lista de técnicas de refatoração**  
   Adicionamos uma lista com técnicas de refatoração com base no livro de Martin Fowler, armazenada em `refatoracoes_possiveis.txt`.

3. **Uso do GitHub Copilot com GPT-4.1**  
   Para minimizar viés, a ordem da lista de técnicas foi embaralhada e o código final (`python-after`) foi ocultado do modelo. O GitHub Copilot foi instruído com o seguinte contexto:

   - A lista de refatorações possíveis (`refatoracoes_possiveis.txt`)
   - O conteúdo da pasta `python-before`
   - Um prompt com as instruções:
     > _“Read each file under the folder "codigos/python-before". For each file you will generate a new file with suffix "\_copilot" with a refactoring suggestion. The refactoring must be one listed in the file "refatoracoes_possiveis.txt". You should write the refactoring name as a comment on the first line of the generated file.”_

4. **Comparação com o código de referência**  
   Os resultados gerados pelo modelo foram comparados com as implementações da pasta `python_plus_after`, que representam refatorações manuais baseadas nas mesmas técnicas.

## 3. Resultados:

#### Técnica: Split Temporary Variable

A técnica dividir variável temporária consiste em substituir uma variável temporária reutilizada para guardar valores diferentes, dentro do método. Veja o exemplo abaixo:

**Código original:**

```python
    temp = 2 * (height + width)
    print(temp)
    temp = height * width
    print(temp)
```

A variável `temp` está sendo utilizada para armazenar dois valores distintos: o perímetro e a área de um retângulo.
Queremos usar variáveis diferentes, para valores diferentes, cada variável deve ser responsável por um valor apenas. Veja abaixo:

**Código refatorado:**

```python
    # Split Temporary Variable
    perimeter = 2 * (height + width)
    print(perimeter)
    area = height * width
    print(area)
```

Cada variável deve ter uma resposabilidade única, para facilitar legibilidade e manutenção do código.

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

A refatoração gerada pelo GitHub Copilot é bastante similar com o código `python-after`, de forma geral, o copilot aplicoua técnica substituindo a estrutura condicional por classes.

### 8. Referências

- [Refactoring.com (Martin Fowler)](https://refactoring.com/)
- [Documentação oficial do Copilot Agent](https://docs.github.com/en/copilot)
- [Coding agent](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

- Artigos:
  - [Refactoring with Large Language Models (arXiv)](https://arxiv.org/abs/2305.00000)
