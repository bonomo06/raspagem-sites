# Raspagem de Dados

Script para fazer raspagem de informações.

## Instalação

Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

## Uso

Execute o script:

```bash
python raspagem.py
```

## Páginas Raspadas

O script coleta dados das URLs que você colocar aqui:

```python
self.urls = [
            'example.com',
            'example.com.br'
        ]
```

## Dados Coletados

Para cada página, o script extrai:

- **Metadados**: título da página e meta tags
- **Títulos**: todos os cabeçalhos (h1-h6)
- **Parágrafos**: todo conteúdo em tags <p>
- **Listas**: listas ordenadas e não ordenadas
- **Tabelas**: dados estruturados de tabelas (matriz curricular, etc.)
- **Links**: todos os links encontrados
- **Imagens**: informações sobre imagens
- **Texto completo**: todo o texto visível da página

## Arquivos Gerados

- `dados_example.json`: dados estruturados em formato JSON
- `dados_example.txt`: dados em formato texto legível

## Funcionalidades

- ✓ Extração completa de conteúdo
- ✓ Suporte a tabelas (matriz curricular)
- ✓ Extração de listas e parágrafos
- ✓ Coleta de metadados
- ✓ Exportação em JSON e TXT
- ✓ Relatório resumido da coleta
- ✓ Intervalo entre requisições (respeito ao servidor)
