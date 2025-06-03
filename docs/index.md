# Modernização de sistemas legados utilizando LLMs: Um estudo de caso

Este material foi produzido para a disciplina de metodologia ágeis, com o objetivo de explorar LLMs e refatoração a de sistemas legados.

---

## Sumário (WIP)

1. [Introdução](#1-sobre-refatoração)
2. [Copilot](#2-sobre-o-copilot-agent)
3. [Refatoração](#3-refatorando)
4. [Exemplos de Código](#4-exemplos-de-código)
5. [Boas práticas no uso de LLMs](#5-boas-práticas-no-uso-de-llms)
6. [Limitações e cuidados](#6-limitações-e-cuidados)
7. [Reproduzindo este ambiente](#7-reprodutibilidade-e-ambiente)
8. [Referências](#8-Referências)

---

## 1. Sobre refatoração

Códigos legados geralmente são complexos e muitos não tem testes automatizados, no geral, utilizam ferramentas obsoletas ou apresentam versionamentos confusos. A refatoração é um pratica que pode ser aplicada para entender e evoluir sistemas legados. No entanto, a ausência de uma boa cobertura de testes torna o processo de refatoração ainda mais desafiador. Embora a resposta óbvia seja adicionar testes, isso nem sempre é simples, especialmente quando o design original do sistema não foi pensado para ser testável. Este trabalho combina a prática de refatoração de sistemas legados com o uso de Modelos de Linguagem de Grande Escala (LLMs), propondo uma abordagem exploratória do copilot agent, para modernização de software. O material segue a linha do livro [Refatoração](<(https://refactoring.com/)>).

[GitHub Copilot Agent](https://docs.github.com/en/copilot/building-copilot-extensions/building-a-copilot-agent-for-your-copilot-extension/using-copilots-llm-for-your-agent) falar da ferramenta?

Vamos refatorar algumas funçoes da API[brainiak-api](https://github.com/bmentges/brainiak_api), analisando como a interação com o copilot pode contribuir para a clareza, organização e manutenção do código.

Vamos seguir uma abordagem com pequenos passos para isolando pequenas partes do código para testar e refatorar gradualmente.
Martin Fowler:

> _“Refatoração (substantivo): uma modificação feita na estrutura interna do software para deixá-lo mais fácil de compreender e menos custoso para alterar, sem que seu comportamento observável seja alterado.”_

#### 2. Sobre o Copilot Agent

O GitHub Copilot Agent é uma ferramenta baseada em LLMs (Large Language Models). Segundo a documentação oficial:

> “Copilot's Large Language Model (LLM) is a powerful, large-scale language model that is trained on a diverse range of data sources, including code, documentation, and other text. Copilot's LLM underpins the functionality for GitHub Copilot, and is used to power all of Copilot's features, including code generation, documentation generation, and code completion.”  
> ([Fonte: Documentação Copilot Agent](https://docs.github.com/en/copilot/building-copilot-extensions/building-a-copilot-agent-for-your-copilot-extension/using-copilots-llm-for-your-agent))

---

### 3. Refatorando

> _"Copilot, analise a função `validate_and_return_instance_data` e sugira o que pode ser refatorado."_

Na primeira iteração pedi ao Copilot sugestões de refatoração passando a função `validate_and_return_instance_data`.

#### Resposta:

Aqui estão sugestões de refatoração para a função validate_and_return_instance_data:

1. **Quebrar a função em partes menores**
   - A função executava diversas tarefas: validação de tipos, verificação de unicidade, geração de erros, etc.
   - Separar essas responsabilidades melhora a clareza, manutenção e testabilidade.

Após analisar a resposta do Copilot, iniciamos o processo pela primeira sugestão dada, separar a função em partes menores...

> _"Copilot, quebre a função em partes menores..."_

**Resposta:**

> Vou quebrar a função `validate_and_return_instance_data` em partes menores para melhorar a legibilidade e manutenção. A abordagem será:
>
> - Uma função principal que orquestra o fluxo geral
> - Uma função para validar um predicado (propriedade)
> - Uma função para verificar propriedades obrigatórias
> - Uma função para gerar mensagens de erro

---

#### 🛠 Aplicação prática (`exemplos.py`)

A refatoração foi implementada no arquivo `exemplos.py`. A função foi dividida nas seguintes partes:

- `**_validate_predicate**`: responsável por validar individualmente cada predicado.
- `**_validate_obligatory_properties**`: verifica a presença de propriedades obrigatórias.
- A função principal passou a apenas coordenar essas funções auxiliares.

```python
# Antes:
async def validate_and_return_instance_data(
    instance_uri, instance_data, class_object, graph_uri, query_params
):
    class_id = class_object["id"]
    copy_instance_data = instance_data.copy()
    predicate_object_tuples = unpack_tuples(copy_instance_data)

    errors = []
    template_msg = _(
        "Incorrect value for property ({1}). A value compatible with a ({2}) was expected, but ({0}) was given."
    )

    for predicate_uri, object_value in predicate_object_tuples:
        if not is_reserved_attribute(predicate_uri):
            predicate_has_error = False
            try:
                predicate_datatype = get_predicate_datatype(class_object, predicate_uri)
            except KeyError:
                template = _(
                    "Inexistent property ({0}) in the schema ({1}), used to create instance ({2})"
                )
                msg = template.format(predicate_uri, class_id, instance_uri)
                errors.append(msg)
                predicate_datatype = None
                predicate_has_error = True
            else:
                if predicate_datatype is None:
                    try:
                        object_ = sparqlfy_object(object_value)
                    except InstanceError:
                        msg = template_msg.format(
                            object_value, predicate_uri, "owl:ObjectProperty"
                        )
                        errors.append(msg)
                        predicate_has_error = True
                else:
                    if is_instance(object_value, predicate_datatype):
                        object_ = sparqlfy(object_value, predicate_datatype)
                    else:
                        msg = template_msg.format(
                            object_value, predicate_uri, predicate_datatype
                        )
                        errors.append(msg)
                        predicate_has_error = True
                if not predicate_has_error:
                    if property_must_map_a_unique_value(class_object, predicate_uri):
                        if await is_value_already_used(
                            instance_uri,
                            object_,
                            predicate_uri,
                            class_object,
                            graph_uri,
                            query_params,
                        ):
                            template = _(
                                "The property ({0}) defined in the schema ({1}) must map a unique value. The value provided ({2}) is already used by another instance."
                            )
                            msg = template.format(predicate_uri, class_id, object_value)
                            errors.append(msg)

    undefined_obligatory_properties = find_undefined_obligatory_properties(class_object, instance_data)
    template = _(
        "The property ({0}) is obligatory according to the definition of the class ({1}). A value must be provided for this field in order to create or edit ({2})."
    )
    for property_ in undefined_obligatory_properties:
        msg = template.format(property_, class_id, instance_uri)
        errors.append(msg)

    if errors:
        error_msg = json.dumps(errors)
        raise InstanceError(error_msg)
    return instance_data
```

Após a primeira iteração, a função foi divida em funçoes menores, `validate_predicate`: valida cada predicado individualmente.
`validate_obligatory_properties`: verifica propriedades obrigatórias. Assim a função princiapl fica com menos responsabildiade. Após essa iteração rodamos os testes para garantir que tudo continua funcionando e vamos reavalir a mesma funcao, para ver o que mais pode ser melhorado.

### Renomear funçoes e variáveis

Um passo simples de executar é renomear funçoes e variáveis, vamos tentar.

> _"Copilot, refatore a funções adicionando nomes mais descritivos." _

**Resposta:**

A função foi refatorada com nomes mais descritivos:
Parâmetros e variáveis como property_uri, property_value, class_schema, validated_value, unique_value_checks.
Funções auxiliares agora são `validate_property` e `validate_required_properties`.
Adicionados type hints e docstring à função principal.

### Adicinar mais testes

> _"Copilot, adicione mais testes para cobrir as funcionalidades da função: validate_and_return_instance_data ..." _

**Resposta:**

Testes complementares foram implementados em test_exemplos.py para cobrir:

Propriedade que deve ser única e já está em uso.
Propriedade obrigatória ausente.
Propriedade inexistente no schema.
Todos os tipos suportados (boolean, integer, string, string_uri, array_string_uri).

### Função refatorada

```python
# Depois:
  async def validate_and_return_instance_data(
      instance_uri, instance_data, class_object, graph_uri, query_params
  ): ...

```

### 6. Limitações do modelo

---

### 8. Referências

- [Refactoring.com (Martin Fowler)](https://refactoring.com/)
- [Documentação oficial do Copilot Agent](https://docs.github.com/en/copilot)
- [Coding agent](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/)

- Artigos:
  - [Refactoring with Large Language Models (arXiv)](https://arxiv.org/abs/2305.00000)
