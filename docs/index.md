# Modernização de sistemas legados utilizando LLMs: Um estudo de caso

Este guia foi desenvolvido para a disciplina de metodologia ágeis, com o objetivo de apresentar um passo a passo prático para refatoração de sistemas legados utilizando LLMs, para este trabalho, utilizaremos GitHub Copilot Agent.

---

## Sumário (WIP)

1. [Introdução](#1-introdução)
2. [LLMs/Copilot Agent](#2-conhecendo-o-copilot-agent)
3. [Refatoração](#3-etapas-práticas-da-refatoração)
4. [Exemplos de Código](#4-exemplos-de-código)
5. [Boas práticas no uso de LLMs](#5-boas-práticas-no-uso-de-llms)
6. [Limitações e cuidados](#6-limitações-e-cuidados)
7. [Reproduzindo este ambiente](#7-reprodutibilidade-e-ambiente)
8. [Referências](#8-Referências)

---

## Resumo (TODO)

A modernização de sistemas legados é um desafio comum na indústria[citar_artigo], apesar de essenciais, frequentemente apresentam limitações de desempenho, escalabilidade e usabilidade. Este trabalho relata a experiência de utilizar Large Language Models (LLMs), como Copilot, para apoiar a reengenharia de um sistema legado [brainiak-api](https://github.com/bmentges/brainiak_api). Foram aplicadas diferentes xxx estratégias de interação com modelos xxx para melhorias do código. Como resultado.......

## 1. Introdução (TODO)

- **Contexto:** Material criado para entender como utilizar LLMs para efatoração em sistemas legados....
- **Objetivo:** Analisar se LLMs podem potencializar a produtividade e a qualidade do código em projetos reais.

---

#### 2. LLMs e Copilot Agent (TODO)

- descrição

---

#### 3. Refatoração de Sistemas Legados (WIP)

- [Conceito de refatoração](1-conceito-refatoracao.md)

### 3.1 . Etapas da Refatoração (TODO)

#### 3.2.1 Identificação de pontos críticos (TODO)

- Diagnóstico do código legado com prompts, ex:
  - _"Liste funções muito longas nesta func"_
- **Exemplo de prompt:** _"Copilot, identifique funcs com mais de xx linhas neste arquivo."_

#### 3.2.2 Geração de testes antes de alterar código

#### 3.2.3 Refatoração incremental (TODO)

- Dividir funções longas e reorganizar responsabilidades:

#### 3.2.4 Remoção de duplicações (TODO)

- Detectar e eliminar redundâncias

### 3.3 Exemplos de prompts para diagnóstico

## 4. Exemplos de código(WIP)

A pasta [`codigo-legado/`](./codigo-legado) contém trechos de código legado usados como base para este estudo.
Esses exemplos foram selecionados para demonstrar práticas de refatoração, como modularização, remoção de duplicações e legibilidade, utilizando LLMs como o Copilot Agent.

- [exemplos.py](https://github.com/derliaparecida/refact-agile/blob/main/docs/codigo-legado/exemplos.py): Função antes de refatorar.

**Como executar/testar:**

- Pré-requisitos: Python 3.10+, VS Code, extensão Copilot Agent.
- Instale dependências: `pip install -r requirements.txt`
- Execute os testes: `pytest` ou `python -m unittest`

---

## 5. Boas Práticas no Uso de LLMs (TODO)

---

## 6. Limitações e Cuidados (TODO)

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

## 8. Referências (WIP)

- [Refactoring.com (Martin Fowler)](https://refactoring.com/)
- [Documentação oficial do Copilot Agent](https://docs.github.com/en/copilot)
- Exemplos no GitHub:
  - [Copilot Agent Playground](https://github.com/github/copilot-agent)
- Artigos acadêmicos:
  - [Refactoring with Large Language Models (arXiv)](https://arxiv.org/abs/2305.00000)
