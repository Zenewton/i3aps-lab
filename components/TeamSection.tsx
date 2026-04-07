import React from "react";

type TeamMember = {
  nome: string;
  afiliacao: string;
  area: string;
  sigaa: string;
  orcid: string;
};

const equipe: TeamMember[] = [
  {
    nome: "Zenewton André da Silva Gama",
    afiliacao: "UFRN – Saúde Coletiva | QualiSaúde | PPGSC",
    area: "Saúde coletiva, qualidade do cuidado e segurança do paciente",
    sigaa: "#",
    orcid: "#",
  },
  {
    nome: "Tatyana Maria S. S. Rosendo",
    afiliacao: "UFRN – Saúde Coletiva | PPGSF",
    area: "Epidemiologia e saúde materno-infantil",
    sigaa: "#",
    orcid: "#",
  },
  {
    nome: "Itamir de Morais Barroca Filho",
    afiliacao: "IMD/UFRN – Engenharia de Software",
    area: "Sistemas distribuídos e infraestrutura digital",
    sigaa: "#",
    orcid: "#",
  },
  {
    nome: "Marcelo Augusto Costa Fernandes",
    afiliacao: "UFRN – Engenharia da Computação",
    area: "Inteligência artificial e sistemas complexos",
    sigaa: "#",
    orcid: "#",
  },
  {
    nome: "César Rennó Costa",
    afiliacao: "IMD/UFRN – Bioinformática",
    area: "Integração de dados e IA em saúde",
    sigaa: "#",
    orcid: "#",
  },
  {
    nome: "Dyego Leandro Bezerra de Souza",
    afiliacao: "UFRN – Saúde Coletiva",
    area: "Epidemiologia e oncologia",
    sigaa: "#",
    orcid: "#",
  },
  {
    nome: "Angelo Roncalli",
    afiliacao: "UFRN – Saúde Coletiva",
    area: "Epidemiologia e avaliação em saúde",
    sigaa: "#",
    orcid: "#",
  },
  {
    nome: "Viviane Souza do Amaral",
    afiliacao: "UFRN – Saúde da Mulher",
    area: "Saúde materna e cuidado clínico",
    sigaa: "#",
    orcid: "#",
  },
  {
    nome: "Ana Katherine Oliveira",
    afiliacao: "UFRN – Saúde da Mulher",
    area: "Ginecologia e obstetrícia",
    sigaa: "#",
    orcid: "#",
  },
  {
    nome: "Karla Morganna P. P. Mendonça",
    afiliacao: "UFRN – Fisioterapia",
    area: "Doenças respiratórias e inovação clínica",
    sigaa: "#",
    orcid: "#",
  },
];

function ExternalLinkIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      aria-hidden="true"
      className="h-4 w-4"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M14 3h7v7" />
      <path d="M10 14L21 3" />
      <path d="M21 14v7h-7" />
      <path d="M3 10V3h7" />
      <path d="M3 21h7" />
      <path d="M3 21l7-7" />
    </svg>
  );
}

function OrcidIcon() {
  return (
    <span className="inline-flex h-5 w-5 items-center justify-center rounded-full bg-[#A6CE39] text-[10px] font-bold leading-none text-white">
      iD
    </span>
  );
}

type TeamCardProps = {
  membro: TeamMember;
};

export function TeamCard({ membro }: TeamCardProps) {
  return (
    <article className="flex h-full flex-col rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition-all duration-200 hover:-translate-y-[2px] hover:shadow-lg">
      <header className="space-y-2">
        <h3 className="text-lg font-semibold leading-snug text-slate-900">{membro.nome}</h3>
        <p className="text-sm text-slate-500">{membro.afiliacao}</p>
      </header>

      <p className="mt-4 text-sm leading-relaxed text-slate-700">{membro.area}</p>

      <footer className="mt-auto pt-5">
        <div className="flex items-center gap-3 border-t border-slate-200 pt-4">
          <a
            href={membro.sigaa}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-md px-2 py-1 text-sm text-slate-700 transition-colors hover:bg-slate-100 hover:text-slate-900"
            aria-label={`Perfil SIGAA de ${membro.nome}`}
            title="SIGAA"
          >
            <ExternalLinkIcon />
            <span>SIGAA</span>
          </a>
          <a
            href={membro.orcid}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-md px-2 py-1 text-sm text-slate-700 transition-colors hover:bg-slate-100 hover:text-slate-900"
            aria-label={`Perfil ORCID de ${membro.nome}`}
            title="ORCID"
          >
            <OrcidIcon />
            <span>ORCID</span>
          </a>
        </div>
      </footer>
    </article>
  );
}

export default function TeamSection() {
  return (
    <section className="bg-slate-50 py-14">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl">
          <h2 className="text-2xl font-semibold tracking-tight text-slate-900 sm:text-3xl">Equipe</h2>
          <p className="mt-4 text-sm leading-relaxed text-slate-700 sm:text-base">
            A equipe do I³-APS reúne pesquisadores líderes nas áreas de saúde coletiva, engenharia de
            software, inteligência artificial e epidemiologia, refletindo a natureza interdisciplinar
            necessária para a construção de uma infraestrutura nacional de dados clínicos interoperáveis
            voltada ao cuidado longitudinal no SUS.
          </p>
        </div>

        <div className="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {equipe.map((membro) => (
            <TeamCard key={membro.nome} membro={membro} />
          ))}
        </div>
      </div>
    </section>
  );
}
