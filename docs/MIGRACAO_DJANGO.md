# Migração Streamlit para Django - I3 APS

## 1. Diagnóstico arquitetural

O Streamlit atual concentra UI, navegação, estado de sessão e acesso a dados no mesmo processo. Isso foi adequado para MVP, mas limita produção institucional porque cada interação tende a recalcular a tela, a autenticação fica fora dos mecanismos maduros do framework, e APIs/cache/permissões exigem trabalho manual.

Funcionalidades mapeadas:

- Navegação multipágina com sidebar.
- Páginas institucionais: Início, Serviços, Acesso, Sobre e Equipe.
- Downloads de documentos de governança.
- Formulário de solicitação de uso/apoio.
- Cadastro e login de usuários.
- Área do usuário com filtro por status.
- Painel administrativo para atualização de status e notas.
- Métricas simples de solicitações e instituições.

## 2. Arquitetura Django equivalente

A base Django foi organizada por domínio:

- `public_site`: conteúdo institucional e documentos.
- `access_requests`: solicitações de uso, status, formulários e importação legada.
- `accounts`: autenticação, cadastro e perfil institucional.
- `dashboards`: painéis autenticados.
- `api`: endpoints DRF e JWT.
- `analytics`, `interoperability`, `telehealth`, `ai_models`: módulos reservados para evolução de dashboards, FHIR/RNDS, cuidado remoto e IA.

Decisão frontend: Django Templates + Bootstrap 5 nesta primeira etapa. Isso preserva o conteúdo e a navegação com menor risco. React pode ser introduzido depois em dashboards específicos, consumindo a API DRF, sem reescrever o portal inteiro.

## 3. Diferenças importantes

- Streamlit re-renderiza a página inteira a cada interação; Django usa rotas HTTP, templates e APIs específicas.
- SQLite e funções manuais foram substituídos por ORM, migrations, índices e querysets.
- Autenticação própria por PBKDF2 foi substituída por Django Auth e JWT para APIs.
- Admin e dashboard agora usam permissões (`login_required`, `is_staff`) e filtros server-side.
- Documentos institucionais são servidos por view controlada, não por botões Streamlit.

## 4. Performance e escalabilidade

Melhorias já preparadas:

- PostgreSQL em produção.
- Índices para `status`, `responsavel_email` e `created_at`.
- Paginação padrão DRF.
- Redis configurado para cache.
- Celery configurado para tarefas assíncronas.
- Gunicorn + Nginx para execução institucional.

Próximas otimizações:

- Cache de catálogos públicos e métricas agregadas.
- Dashboards com APIs assíncronas e Chart.js/Plotly.
- Tasks Celery para importações, relatórios e integrações FHIR.

## 5. Segurança

Implementado/preparado:

- CSRF em formulários Django.
- JWT para API.
- Sessões HTTPOnly.
- Settings de produção com SSL redirect, cookies seguros e HSTS.
- `.env` para segredos.
- Controle de acesso por proprietário da solicitação ou staff.

Pendências antes de produção:

- Política de reset de senha para usuários importados.
- Matriz formal de perfis e permissões.
- Logs estruturados sem dados sensíveis.
- Revisão LGPD de campos, retenção e auditoria.

## 6. Plano incremental recomendado

1. Validar páginas institucionais Django contra o Streamlit atual.
2. Migrar dados de produção com `import_streamlit_sqlite`.
3. Homologar cadastro, login, solicitações e painel admin.
4. Recriar dashboards analíticos com APIs DRF + Chart.js/Plotly.
5. Adicionar módulos FHIR/RNDS, telemonitoramento e IA em apps próprios.
6. Executar deploy Docker em ambiente de homologação.
7. Desativar Streamlit somente após checklist funcional assinado.
