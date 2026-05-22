from pathlib import Path


DOCS_DIR = Path("assets/docs")

INFRASTRUCTURE_RESOURCES = [
    {
        "title": "Integração de Dados Clínicos do SUS",
        "description": "Apoio técnico para conectar sistemas da APS, atenção especializada e rede hospitalar com padrões interoperáveis e implantação progressiva.",
        "use_cases": "PEC, prontuários hospitalares, RNDS, linhas de cuidado e painéis assistenciais.",
    },
    {
        "title": "Ambiente Seguro para Dados Clínicos e Pesquisa",
        "description": "Espaço controlado para organização, tratamento e análise de dados sensíveis, com rastreabilidade, governança e atenção à LGPD.",
        "use_cases": "Estudos multicêntricos, avaliação de desfechos e análise de linhas de cuidado.",
    },
    {
        "title": "Monitoramento e Gestão do Cuidado",
        "description": "Dashboards, indicadores e rotinas analíticas para apoiar equipes e gestores no acompanhamento longitudinal da população.",
        "use_cases": "Hipertensão, diabetes, pós-alta, perda de seguimento e condições crônicas.",
    },
    {
        "title": "Telemonitoramento e Cuidado Remoto",
        "description": "Apoio à estruturação de fluxos de acompanhamento remoto, comunicação e priorização de pacientes para continuidade do cuidado.",
        "use_cases": "Condições crônicas, acompanhamento domiciliar e continuidade após internação.",
    },
    {
        "title": "Sandbox para Testes e Validação",
        "description": "Ambiente simulado e controlado para testar integrações, fluxos de dados e aderência a padrões antes de uso em operação real.",
        "use_cases": "Validação FHIR, integração com RNDS, MVPs e provas técnicas de interoperabilidade.",
    },
]

USER_PROFILES = [
    {
        "title": "Secretarias Municipais e Estaduais",
        "description": "Apoio para transformar dados já existentes em informação útil para gestão, regulação e coordenação do cuidado.",
        "examples": ["Integração progressiva de sistemas da rede.", "Dashboards assistenciais para linhas de cuidado.", "Monitoramento de condições crônicas na APS.", "Apoio à interoperabilidade APS-hospital."],
        "cta": "Solicitar uso da infraestrutura",
    },
    {
        "title": "Serviços de Saúde",
        "description": "Suporte para acompanhar pacientes ao longo do tempo e reduzir perda de seguimento em fluxos assistenciais prioritários.",
        "examples": ["Monitoramento longitudinal de usuários.", "Indicadores assistenciais para equipes.", "Apoio ao acompanhamento pós-alta.", "Continuidade do cuidado entre pontos da rede."],
        "cta": "Agendar reunião",
    },
    {
        "title": "Pesquisadores e Pós-graduação",
        "description": "Ambiente multiusuário para pesquisa aplicada, análise de dados e avaliação de problemas reais do SUS.",
        "examples": ["Ambiente seguro para análise de dados clínicos.", "Estudos multicêntricos e avaliação de desfechos.", "Avaliação de linhas de cuidado.", "Validação aplicada de indicadores e análises."],
        "cta": "Solicitar uso da infraestrutura",
    },
    {
        "title": "Empresas e Startups",
        "description": "Espaço de validação técnica para soluções de saúde digital, sem confundir o laboratório com canal comercial.",
        "examples": ["Testes de interoperabilidade com padrões FHIR.", "Validação técnica em ambiente simulado.", "Ensaios de integração com fluxos RNDS.", "Ajustes antes de pilotos institucionais."],
        "cta": "Solicitar validação técnica",
    },
]

SERVICE_OFFERINGS = [
    {
        "title": "Integração de Dados Clínicos do SUS",
        "summary": "Apoio para conectar sistemas e organizar fluxos de dados clínicos de forma gradual, com prioridade para problemas assistenciais concretos.",
        "problem": "Dados fragmentados entre APS, serviços especializados e hospitais.",
        "examples": ["Integrar PEC e prontuário hospitalar.", "Apoiar validação de fluxos com RNDS.", "Mapear dados necessários para uma linha de cuidado."],
        "users": "Secretarias, serviços de saúde, ICTs e equipes de tecnologia.",
        "infra": "Integração de Dados Clínicos do SUS; Sandbox para Testes e Validação.",
        "cta": "Solicitar validação técnica",
    },
    {
        "title": "Ambiente Seguro para Dados Clínicos e Pesquisa",
        "summary": "Ambiente governado para análise de dados sensíveis, com regras de acesso, registro de uso e escopo definido por projeto.",
        "problem": "Necessidade de pesquisar e avaliar dados clínicos sem ampliar riscos de privacidade.",
        "examples": ["Analisar desfechos em condições crônicas.", "Avaliar linhas de cuidado em múltiplos municípios.", "Organizar bases para pesquisa aplicada na APS."],
        "users": "Pesquisadores, programas de pós-graduação, gestores e instituições parceiras.",
        "infra": "Ambiente Seguro para Dados Clínicos e Pesquisa.",
        "cta": "Solicitar uso da infraestrutura",
    },
    {
        "title": "Inteligência Analítica para Apoio ao Cuidado",
        "summary": "Construção e validação progressiva de indicadores, painéis e análises aplicadas para apoiar decisões de gestão e cuidado.",
        "problem": "Equipes precisam priorizar usuários e identificar riscos com base em dados confiáveis.",
        "examples": ["Identificar usuários com perda de seguimento.", "Priorizar acompanhamento de hipertensos sem consulta recente.", "Avaliar padrões de encaminhamento e retorno."],
        "users": "Gestores, equipes assistenciais, pesquisadores e programas de avaliação.",
        "infra": "Monitoramento e Gestão do Cuidado; Ambiente Seguro para Dados Clínicos e Pesquisa.",
        "cta": "Agendar reunião",
    },
    {
        "title": "Monitoramento e Gestão do Cuidado",
        "summary": "Apoio à construção de painéis e rotinas de acompanhamento para condições e linhas de cuidado prioritárias.",
        "problem": "Dificuldade de acompanhar longitudinalmente usuários em redes assistenciais complexas.",
        "examples": ["Monitorar hipertensos e diabéticos sem acompanhamento recente.", "Acompanhar pacientes pós-alta.", "Construir dashboards assistenciais para gestão e equipes da APS."],
        "users": "Secretarias, serviços de saúde, equipes da APS e coordenações de linha de cuidado.",
        "infra": "Monitoramento e Gestão do Cuidado.",
        "cta": "Agendar reunião",
    },
]

CONCRETE_EXAMPLES = [
    "Integrar PEC e prontuário hospitalar para apoiar continuidade do cuidado.",
    "Monitorar hipertensos sem consulta recente ou sem registro de acompanhamento.",
    "Identificar perda de seguimento em linhas de cuidado prioritárias.",
    "Acompanhar pacientes pós-alta com dados mínimos e alertas assistenciais.",
    "Validar integração com padrões FHIR/RNDS em ambiente controlado.",
    "Construir dashboards assistenciais para gestão e equipes da APS.",
]

GOVERNANCE_ITEMS = [
    "Escopo definido por projeto",
    "Autorização institucional",
    "Controle de acesso",
    "Rastreabilidade",
    "Conformidade com LGPD",
    "Uso progressivo da infraestrutura",
]

ACCESS_MODALITIES = [
    {"title": "Cooperação científica", "description": "Uso da infraestrutura em projetos de pesquisa aplicada e formação avançada."},
    {"title": "Projetos institucionais com o SUS", "description": "Apoio a demandas pactuadas com secretarias, serviços e redes assistenciais."},
    {"title": "Validação técnica de soluções digitais", "description": "Testes controlados de interoperabilidade, fluxos de dados e aderência a padrões."},
    {"title": "Serviços especializados mediante avaliação de viabilidade", "description": "Atendimento de demandas específicas conforme escopo, capacidade operacional e governança."},
]

GOVERNANCE_DOCUMENTS = [
    {"title": "Criação do I³ APS", "description": "Portaria que institui formalmente o Laboratório Multiusuário I³ APS.", "tokens": ("portaria 1", "cria"), "slug": "criacao"},
    {"title": "Regimento interno", "description": "Documento que define finalidade, estrutura, funcionamento e regras institucionais.", "tokens": ("regimento",), "slug": "regimento"},
    {"title": "Coordenação", "description": "Portaria de designação da coordenação do laboratório.", "tokens": ("portaria 2", "coorden"), "slug": "coordenacao"},
    {"title": "Comitê Gestor", "description": "Portaria que institui a instância de gestão e acompanhamento institucional.", "tokens": ("portaria 3", "gestor"), "slug": "comite-gestor"},
    {"title": "Comitê de Usuários", "description": "Portaria que institui a representação de usuários da infraestrutura multiusuária.", "tokens": ("portaria 4", "usua"), "slug": "comite-usuarios"},
]

PARTNER_LABS = [
    {"name": "Centro Multiusuário de Bioinformática - BIOME", "description": "Apoio à bioinformática, análise de dados biológicos e integração com pesquisa translacional em saúde.", "url": "https://bioinfo.imd.ufrn.br/site/pt"},
    {"name": "Laboratório de Inovação em Inteligência Artificial - InovaAI Lab", "description": "Infraestrutura e desenvolvimento aplicado em inteligência artificial, aprendizado de máquina e modelos analíticos.", "url": "https://inovailab.imd.ufrn.br"},
    {"name": "Núcleo de Processamento de Alto Desempenho - NPAD", "description": "Infraestrutura computacional de alto desempenho para processamento escalável e análise intensiva de dados.", "url": "https://npad.ufrn.br/npad/bemvindo"},
    {"name": "Laboratório de Avaliação e Intervenção Respiratória - LAIRE", "description": "Pesquisa aplicada e validação clínica em doenças respiratórias e cuidado longitudinal.", "url": "http://laire.ufrn.br/"},
]

TEAM_BLOCKS = [
    {
        "titulo": "Saúde Coletiva e APS",
        "membros": [
            {"nome": "Zenewton André da Silva Gama", "afiliacao": "UFRN - Saúde Coletiva | QualiSaúde | PPGSC", "area": "Saúde coletiva, qualidade do cuidado e segurança do paciente", "lattes": "http://lattes.cnpq.br/8885774273217562", "orcid": "https://orcid.org/0000-0003-0818-9680"},
            {"nome": "Tatyana Maria S. S. Rosendo", "afiliacao": "UFRN - Saúde Coletiva | PPGSF", "area": "Epidemiologia e saúde materno-infantil", "lattes": "http://lattes.cnpq.br/4946747115155324", "orcid": "https://orcid.org/0000-0003-0233-3119"},
            {"nome": "Angelo Roncalli", "afiliacao": "UFRN - Saúde Coletiva", "area": "Epidemiologia e avaliação em saúde", "lattes": "http://lattes.cnpq.br/0023445563721084", "orcid": "https://orcid.org/0000-0001-5311-697X"},
            {"nome": "Severina Alice da Costa Uchoa", "afiliacao": "UFRN - Departamento de Saúde Coletiva", "area": "Saúde coletiva, atenção primária e saúde internacional", "lattes": "http://lattes.cnpq.br/8414233332373275", "orcid": "https://orcid.org/0000-0002-2531-9937"},
        ],
    },
    {
        "titulo": "Inteligência Artificial e Engenharia",
        "membros": [
            {"nome": "Itamir de Morais Barroca Filho", "afiliacao": "IMD/UFRN - Engenharia de Software", "area": "Sistemas distribuídos e infraestrutura digital", "lattes": "http://lattes.cnpq.br/1093675040121205", "orcid": "https://orcid.org/0000-0003-1694-8237"},
            {"nome": "Marcelo Augusto Costa Fernandes", "afiliacao": "UFRN - Engenharia da Computação", "area": "Inteligência artificial e sistemas complexos", "lattes": "http://lattes.cnpq.br/3475337353676349", "orcid": "https://orcid.org/0000-0001-7536-2506"},
            {"nome": "César Rennó Costa", "afiliacao": "IMD/UFRN - Bioinformática", "area": "Integração de dados e IA em saúde", "lattes": "http://lattes.cnpq.br/9222565820639401", "orcid": "https://orcid.org/0000-0003-0417-8108"},
        ],
    },
    {
        "titulo": "Linhas de cuidado",
        "membros": [
            {"nome": "Dyego Leandro Bezerra de Souza", "afiliacao": "UFRN - Saúde Coletiva", "area": "Epidemiologia e oncologia", "lattes": "http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4702617H2", "orcid": "https://orcid.org/0000-0001-8426-3120"},
            {"nome": "Viviane Souza do Amaral", "afiliacao": "UFRN - Saúde da Mulher", "area": "Saúde materna e cuidado clínico", "lattes": "http://lattes.cnpq.br/4440806451383783", "orcid": "https://orcid.org/0000-0002-9326-9054"},
            {"nome": "Ana Katherine da Silveira Goncalves de Oliveira", "afiliacao": "UFRN - Departamento de Toco-Ginecologia", "area": "Ginecologia, obstetrícia e saúde da mulher", "lattes": "http://lattes.cnpq.br/3436756337251449", "orcid": "https://orcid.org/0000-0002-8351-5119"},
            {"nome": "Karla Morganna Pereira Pinto de Mendonça", "afiliacao": "UFRN - Departamento de Fisioterapia", "area": "Doenças respiratórias crônicas", "lattes": "http://lattes.cnpq.br/1736384836028397", "orcid": "https://orcid.org/0000-0001-5734-3707"},
            {"nome": "Thiago Gomes da Trindade", "afiliacao": "UFRN - Departamento de Medicina Clínica", "area": "Linhas de cuidado às condições crônicas e prática clínica", "lattes": "http://lattes.cnpq.br/5992470800302814", "orcid": "https://orcid.org/0000-0001-8178-0982"},
            {"nome": "Marise Reis de Freitas", "afiliacao": "UFRN - Departamento de Infectologia", "area": "Linhas de cuidado, doenças infecciosas, segurança do paciente e qualidade", "lattes": "http://lattes.cnpq.br/9028554205811163", "orcid": "https://orcid.org/0000-0002-5679-6672"},
        ],
    },
]
