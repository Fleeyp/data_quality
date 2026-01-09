# Dadosfera – Olist E-commerce Case

Este repositório contém os artefatos técnicos desenvolvidos para o case de implementação da plataforma Dadosfera em um cenário de e-commerce, utilizando o dataset público da Olist.

O objetivo do case é demonstrar, de ponta a ponta, a construção de uma Plataforma de Dados voltada à geração de valor analítico, com foco em análises descritivas, prescritivas e uso de GenAI.

---

## Dataset Utilizado
- **Olist E-commerce Dataset**
- Fonte: Kaggle (dataset público)
- Volume: > 100.000 registros
- Tipo: Transacional + texto desestruturado

---

## Principais Etapas do Case
- Integração de dados via PostgreSQL + Dadosfera
- Catalogação e organização em Data Lake
- Validação de qualidade de dados (Great Expectations)
- Feature Engineering com LLMs

---

## Tecnologias Utilizadas
- PostgreSQL
- Dadosfera (Coleta, Catálogo, Visualização)
- Python
- Great Expectations
- OpenAI / GPT
- GitHub

---

## Objetivo
Este projeto foi desenvolvido como uma **Prova de Conceito (PoC)** técnica para avaliação da viabilidade da Dadosfera como plataforma central de dados.

## Important:
Comando que deve ser rodado para instalar os requirements necessários:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt