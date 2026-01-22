# Mini Text Service 

![Python](https://img.shields.io/badge/Python-3.9-3776AB?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)

---
## Introdução
> Solução containerizada para classificação de textos com foco em reprodutibilidade e monitoramento.

Este projeto consiste em uma API REST desenvolvida em FastAPI para classificar textos em categorias pré-definidas (Pergunta, Reclamação ou Relato). O foco principal é a reprodutibilidade de ambiente e boas práticas de DevOps/MLOps.



---

## Sobre o Projeto
O objetivo desta entrega é garantir a execução reprodutível de uma solução simples de classificação textual. A aplicação recebe um texto via API, aplica heurísticas baseadas em regras e retorna a categoria classificada junto com o tempo de inferência.

---
##  Metodologia
Para atender à demanda de empacotamento e performance, foram adotadas as seguintes abordagens:

* **Arquitetura de Microsserviço:** Utilização do `FastAPI` para criar endpoints rápidos e documentados automaticamente.
* **Estratégia de Classificação:** Implementação de um algoritmo baseado em regras (`rules strategy`) que analisa palavras-chave e pontuação no texto para definir a categoria (Pergunta, Reclamação ou Relato).
* **Containerização:** Criação de um `Dockerfile` otimizado para garantir que as dependências e o ambiente de execução sejam idênticos em desenvolvimento e produção.
* **Monitoramento (MLOps):** Instrumentação do código para calcular a latência da inferência (`elapsed_ms`) em cada requisição, dado essencial para observabilidade de modelos.
---
## Funcionalidades

A API expõe os seguintes endpoints:

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | **/classify** | Classifica o texto enviado. Retorna categoria, confiança e latência (`elapsed_ms`). |
| `GET` | **/health** | Check de saúde para orquestradores (K8s/Docker Swarm). Retorna `{"status": "ok"}`. |
| `GET` | **/info** | Metadados do serviço (Versão, Nome). |
| `POST` | **/echo** | Ferramenta de debug. Retorna o payload enviado para teste de rede. |

---
## Teste e Resultado

A lógica de classificação implementada segue as heurísticas definidas no anexo da avaliação:

* **Pergunta:** Identificada pela presença de `?` ou início com "como", "por que", "qual" (Confiança: 0.85).
* **Reclamação:** Identificada por palavras como "não funciona", "erro", "ruim", "problema" (Confiança: 0.75).
* **Relato:** Categoria padrão caso nenhuma regra anterior seja atendida (Confiança: 0.60).

### Resultado Esperado (Exemplo)
Para o input *"O sistema não funciona"*:

```json
{
  "category": "reclamacao",
  "confidence": 0.75,
  "strategy": "rules",
  "elapsed_ms": 1  
}
```
---
## Como Executar

Para garantir a reprodutibilidade exigida, recomenda-se o uso do Docker.

### Via Docker (Recomendado)

1. **Construir a imagem:**
```bash
docker build -t mini-text-service .
```
2. **Executar o container:**
```
docker run -d -p 8000:8000 --name classificador mini-text-service
```
3. **Acessar:** 
Abra o navegador em (`http://localhost:8000/docs`) para ver a interface interativa.
---

### Estrutura do Projeto

A organização dos arquivos cumpre os requisitos de entrega de código-fonte e automação :
```
.
├── Dockerfile            # Script de automação e setup de ambiente
├── main.py               # Código-fonte da aplicação (FastAPI)
├── requirements.txt      # Lista de dependências
└── README.md             # Documentação e tutorial técnico
```
---
### Referências e Fontes
## 8. Referências e Fontes

* **Documento Base:** Avaliação Prática – DevOps / MLOps (Arquivo PDF fornecido).
* **FastAPI:** [FastAPI Documentation](https://fastapi.tiangolo.com/) - Framework web moderno e rápido (alta performance).
* **Docker:** [Docker Documentation](https://docs.docker.com/) - Plataforma para desenvolvimento, envio e execução de aplicações.
* **Pydantic:** [Pydantic Documentation](https://docs.pydantic.dev/) - Validação de dados usando type hints do Python.
* **Uvicorn:** [Uvicorn Documentation](https://www.uvicorn.org/) - Servidor ASGI para Python.