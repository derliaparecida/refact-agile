# Guia Prático: Refatoração de Sistemas Legados com Copilot Agent

Este guia foi desenvolvido para uma disciplina de metodologia ágeis, com o objetivo de apresentar um passo a passo prático para refatoração de sistemas legados utilizando LLMs, para este trabalho, utilizaremos GitHub Copilot Agent.

---

## Sumário

1. [Introdução](#1-introdução)
2. [Conhecendo o Copilot Agent](#2-conhecendo-o-copilot-agent)
3. [Etapas Práticas da Refatoração](#3-etapas-práticas-da-refatoração)
4. [Exemplos de Código](#4-exemplos-de-código)
5. [Boas Práticas no Uso de LLMs](#5-boas-práticas-no-uso-de-llms)
6. [Limitações e Cuidados](#6-limitações-e-cuidados)
7. [Reprodutibilidade e Ambiente](#7-reprodutibilidade-e-ambiente)
8. [Recursos Extras](#8-recursos-extras)

---

## 1. Introdução

- **Contexto:** Material criado para entender como utilizar LLMs para efatoração em sistemas legados....
- **Objetivo:** Analisar se LLMs podem potencializar a produtividade e a qualidade do código em projetos reais.

---

## 2. Conhecendo o Copilot Agent

- O que é o GitHub Copilot Agent?

---

## 3. Etapas Práticas da Refatoração

### 3.1. Identificar pontos críticos

- Diagnóstico do código legado com prompts, ex:
  - _"Liste funções muito longas nesta func"_
- **Exemplo de prompt:** _"Copilot, identifique funcs com mais de xx linhas neste arquivo."_

### 3.2. Gerar testes antes de alterar código

### 3.3. Refatorar em pequenos passos

- Dividir funções longas e reorganizar responsabilidades:
  - _"Divida essa função em métodos menores"_
  - _"Aplique o padrão de design xxx"_
- **Antes/Depois:**  
  | Antes (Função legada) | Depois (Funções refatords) |
  |----------------------|--------------------------|
  | ...código... | ...código refatorado... |

### 3.4. Remover duplicações

- Detectar e eliminar redundâncias:
  - _"Essas 2 funções estão com código duplicado. refatore..."_

## 4. Exemplos de Código

A pasta [`examples/`](./examples) contém trechos de código legado usados como base para este tutorial.

- [format_response.py](./examples/format_response.py): Função complexa e sem modularização.
- [validate_instance.py](./examples/validate_instance.py): Função assíncrona com múltiplas validações.
- [utils.py](./examples/utils.py): Funções auxiliares sem tipagem e documentação.

**Como executar/testar:**

- Pré-requisitos: Python 3.10+, VS Code, extensão Copilot Agent.
- Instale dependências: `pip install -r requirements.txt`
- Execute os testes: `pytest` ou `python -m unittest`

---

## 5. Boas Práticas no Uso de LLMs

---

## 6. Limitações e Cuidados

---

## 7. Reprodutibilidade e Ambiente

- Ambiente sugerido: VS Code + Copilot Agent
- Como instalar dependências:
  - `pip install -r requirements.txt`
- Como rodar exemplos:
  - `python refactoring/exemplos.py`
- Como contribuir:
  - Fork, branch, pull request

---

## 8. Recursos Extras

- [Refactoring.com (Martin Fowler)](https://refactoring.com/)
- [Documentação oficial do Copilot Agent](https://docs.github.com/en/copilot)
- Exemplos no GitHub:
  - [Copilot Agent Playground](https://github.com/github/copilot-agent)
- Artigos acadêmicos:
  - [Refactoring with Large Language Models (arXiv)](https://arxiv.org/abs/2305.00000)
