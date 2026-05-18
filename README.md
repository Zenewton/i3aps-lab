# I3 APS Platform

Portal institucional e operacional do I3 APS, em migração incremental de Streamlit para Django.

## Diagnóstico do sistema legado

O sistema Streamlit atual foi preservado e continua disponível em `app.py` e `pages/`. A análise identificou:

- Páginas públicas: Início, Serviços, Acesso, Equipe e Sobre.
- Fluxo operacional: formulário de solicitação de uso, área do usuário e painel administrativo.
- Persistência legada: SQLite em `data/i3_aps.db`, com tabelas `users` e `requests`.
- Autenticação legada: hash PBKDF2 próprio em `database.py`.
- Documentos institucionais: PDFs em `assets/docs/`.
- Ativos visuais: logos em `logos/` e diagramas SVG na raiz.

## Arquitetura Django criada

- `i3aps_platform/`: projeto Django, URLs, ASGI/WSGI, Celery e settings por ambiente.
- `apps/core/`: health check e contexto de navegação.
- `apps/accounts/`: cadastro, login e perfil institucional.
- `apps/access_requests/`: modelo, formulário, painel admin e importação do SQLite legado.
- `apps/public_site/`: páginas institucionais migradas para templates.
- `apps/dashboards/`: área autenticada do usuário.
- `apps/api/`: DRF, JWT, catálogo de serviços e ViewSet de solicitações.
- Apps reservados para expansão: `analytics/`, `interoperability/`, `telehealth/`, `ai_models/`.

## Execução local Django

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

Acesse `http://127.0.0.1:8000`.

## Importar dados do Streamlit

```bash
python manage.py import_streamlit_sqlite --db data/i3_aps.db
```

Usuários importados recebem senha inutilizável por segurança. A redefinição de senha deve ser feita por fluxo institucional antes de produção.

## APIs principais

- `GET /api/health/`
- `POST /api/auth/token/`
- `POST /api/auth/token/refresh/`
- `GET /api/catalogo/`
- `GET|POST /api/solicitacoes/`
- `GET /api/solicitacoes/metrics/`

As APIs de solicitações usam JWT ou sessão Django e restringem visibilidade ao proprietário da solicitação ou a usuários staff.

## Produção com Docker

```bash
cp .env.example .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# cole a chave gerada em DJANGO_SECRET_KEY no .env
docker compose up --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Nginx expõe a aplicação em `http://127.0.0.1:8080`.

Antes de colocar online, edite o `.env`:

- `DJANGO_ALLOWED_HOSTS`: domínio público e/ou IP do servidor.
- `DJANGO_CSRF_TRUSTED_ORIGINS`: origem HTTPS completa, por exemplo `https://seu-dominio.gov.br`.
- `DJANGO_SECURE_SSL_REDIRECT`, `DJANGO_SESSION_COOKIE_SECURE` e `DJANGO_CSRF_COOKIE_SECURE`: use `true` quando houver HTTPS configurado.
- `POSTGRES_PASSWORD`: senha forte do banco.

## Componentes de produção

- Django + Django REST Framework
- PostgreSQL
- Redis cache
- Celery
- Gunicorn
- Nginx reverse proxy
- WhiteNoise para estáticos
- Variáveis de ambiente via `.env`
- JWT com `djangorestframework-simplejwt`

## Streamlit legado

Durante a migração, o app Streamlit permanece executável:

```bash
streamlit run app.py
```

A remoção do Streamlit deve ocorrer somente após validação funcional completa das páginas, formulários, dashboards e relatórios em Django.
