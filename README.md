# I3-APS Lab

Plataforma de infraestrutura interoperável para dados clínicos no SUS.

## Como executar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Execução robusta (recomendado no macOS)

Use o daemon com watchdog (auto-restart) para evitar quedas do servidor:

```bash
scripts/streamlit_daemon.sh start
scripts/streamlit_daemon.sh status
scripts/streamlit_daemon.sh open
```

Comandos úteis:

```bash
scripts/streamlit_daemon.sh restart
scripts/streamlit_daemon.sh logs
scripts/streamlit_daemon.sh stop
```

Por padrão roda em `http://127.0.0.1:8503`.

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
