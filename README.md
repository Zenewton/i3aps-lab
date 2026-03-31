# I3-APS Lab

Plataforma de infraestrutura interoperável para dados clínicos no SUS.

## Como executar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Estrutura do projeto

- `app.py`: ponto de entrada e roteamento das páginas
- `pages/`: páginas da aplicação (início, serviços, agendamento, dashboard etc.)
- `database.py`: persistência SQLite e operações de dados
- `logos/`: identidade visual e marcas SVG/PNG
- `capa_i3_aps.svg`: diagrama conceitual detalhado

## Tecnologias

- Python 3
- Streamlit
- SQLite
