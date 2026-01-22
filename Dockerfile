# Usa uma imagem base leve do Python para otimizar tamanho e performance
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia primeiro o arquivo de requisitos para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências sem armazenar cache desnecessário (melhora tamanho da imagem)
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código fonte [cite: 17]
COPY . .

# Expõe a porta que a aplicação vai rodar
EXPOSE 8000

# Comando para iniciar a aplicação usando Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]