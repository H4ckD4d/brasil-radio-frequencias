# RadioSync — Brasil Radio Frequências

> **Do sinal à informação. Do Brasil para o mundo.**  
> Uma iniciativa de **[h4ckd4d](https://github.com/H4ckD4d)** para organizar, documentar e tornar mais acessível o conhecimento sobre radiocomunicação.

**RadioSync** é um projeto colaborativo de documentação técnica e organização geográfica de radiofrequências. Sua missão é reunir informações de fontes identificadas, com critérios verificáveis, para apoiar estudantes, radioamadores, técnicos, pesquisadores e entusiastas.

**Cobertura geográfica nacional implantada; catálogo de frequências em expansão.** A presença de um município na estrutura do projeto **não significa** que suas frequências já tenham sido cadastradas.

[Conheça o projeto](#por-que-o-radiosync-existe) · [Consulte os dados](#como-explorar-o-repositório) · [Contribua](CONTRIBUTING.md) · [Fontes](docs/DATA_SOURCES.md) · [Formato técnico](docs/DATA_FORMAT.md)

---

## Por que o RadioSync existe?

Imagine procurar a frequência de uma repetidora, consultar um canal marítimo ou entender a diferença entre uma comunicação analógica e uma digital. Muitas vezes, as informações estão espalhadas por documentos técnicos, listas desatualizadas, publicações oficiais e contribuições comunitárias.

A proposta do **RadioSync** é aproximar esses universos: **organizar dados, explicar o contexto e mostrar a origem de cada informação**.

O projeto começou com um conjunto técnico inicial no **Espírito Santo**. Em seguida, sua estrutura geográfica foi ampliada com dados do **Instituto Brasileiro de Geografia e Estatística (IBGE)**, preparando o caminho para a catalogação progressiva dos serviços de radiocomunicação em todo o território brasileiro.

O objetivo não é apenas criar uma lista de frequências. É construir uma base em que seja possível saber **de onde veio um registro, quando foi consultado, que uso descreve e o que realmente foi verificado**.

## Panorama atual

| Indicador | Situação |
|---|---|
| Cobertura geográfica | **27 unidades federativas** |
| Índices geográficos do IBGE | **5.571 registros territoriais** |
| Composição territorial | **5.570 municípios e 1 registro correspondente ao DF** |
| Índices municipais | **27 arquivos `municipios.csv`** |
| Base técnica inicial | **Espírito Santo** |
| Arquivos CSV de frequências | **7** |
| Registros técnicos iniciais | **15** — radioamadorismo, aviação e serviço marítimo |
| Validação local da expansão | **27 índices + 7 CSVs de frequência sem erros; 16 testes aprovados** |
| Situação do projeto | **Em desenvolvimento contínuo** |

*Os números refletem a etapa de expansão nacional concluída em outubro de 2026. Os índices territoriais não equivalem a uma cobertura nacional de canais ou estações ativas.*

## O que é possível encontrar aqui?

| Área | Explicação acessível |
|---|---|
| **Radioamadorismo** | Referências a repetidoras, indicativos e canais de radioamadores, quando documentados. |
| **Aviação** | Informações públicas sobre comunicações aeronáuticas e seus contextos de uso. |
| **Comunicação marítima** | Referências a canais VHF marítimos e serviços associados. |
| **Rádio analógico e digital** | Campos preparados para FM, DMR e outros protocolos documentados. |
| **SDR e pesquisa técnica** | Dados organizados para estudos de recepção e análise de sinais. |
| **Geografia** | Municípios e códigos oficiais do IBGE para localizar corretamente as referências. |
| **Ferramentas futuras** | Pesquisa, filtros e exportação para softwares e equipamentos compatíveis, quando implementadas. |

**Para quem está começando:** uma *frequência* é uma referência dentro do espectro de rádio; uma *repetidora* pode retransmitir sinais de estações autorizadas; *SDR* é o uso de software para processar sinais de rádio; *DMR* é um padrão digital de radiocomunicação. Esses termos não significam, por si só, autorização para transmitir.

## A diferença entre informação publicada e sinal ativo

Uma frequência aparecer em uma lista **não comprova** que a estação esteja operando neste momento.

Por isso, o RadioSync separa:

1. **Fonte e procedência:** publicação oficial, informação do operador, contribuição comunitária, compilação secundária ou observação independente.
2. **Verificação:** existência de documentação não deve ser confundida com uma recepção comprovada.
3. **Situação operacional:** uma fonte pode relatar uma estação como ativa ou inativa, mas isso não equivale a uma verificação atual.
4. **Direitos de uso dos dados:** conteúdo disponível na internet não é automaticamente autorizado para redistribuição.

Datas, parâmetros de rádio ou posições geográficas desconhecidos devem permanecer em branco — nunca serão preenchidos por suposição.

Saiba mais em [Fontes, procedência e redistribuição](docs/DATA_SOURCES.md).

## Como explorar o repositório

A pasta `dados/` está organizada por **UF** e, dentro dela, por municípios identificados por um nome simplificado (*slug*).

```text
brasil-radio-frequencias/
├── dados/
│   ├── AC/
│   │   ├── municipios.csv
│   │   └── rio-branco/
│   ├── DF/
│   │   ├── municipios.csv
│   │   └── brasilia/
│   ├── ES/
│   │   ├── municipios.csv
│   │   └── ...                # referências técnicas iniciais
│   └── ...                   # demais unidades federativas
├── schemas/                 # regras de validação dos dados
├── scripts/                 # ferramentas Python
├── tests/                   # testes automatizados
├── docs/                    # documentação e fontes
├── radiosync/               # componentes e integrações controladas
├── exports/                 # destinos de futuras exportações
└── .github/                 # colaboração e automação
```

**Comece por aqui:**

- `dados/UF/municipios.csv`: relação territorial da unidade federativa, com código IBGE, município, UF e país.
- `dados/UF/<municipio>/`: espaço destinado às referências técnicas locais, quando disponíveis.
- [Formato dos registros](docs/DATA_FORMAT.md): significado dos campos de frequências e exemplos.
- [Como contribuir](CONTRIBUTING.md): procedimento para propor correções ou incluir novas informações.

O Distrito Federal possui tratamento administrativo próprio; não é dividido em municípios como os estados brasileiros. Localidades, bairros e distritos também não devem ser cadastrados como municípios independentes.

## Como validar os dados

É possível conferir a consistência dos arquivos com **Python 3.11 ou superior**, utilizando ferramentas da biblioteca padrão.

```powershell
python .\scripts\validate_csv.py
python -m unittest discover -s tests -v
```

A sincronização geográfica com o IBGE também possui um modo de conferência antes de alterar arquivos:

```powershell
python .\scripts\sync_ibge_municipios.py
```

Para criar apenas os índices ainda ausentes:

```powershell
python .\scripts\sync_ibge_municipios.py --apply
```

O gerador preserva os arquivos municipais que já existem. Antes de executar sincronizações, contribuições ou exportações, verifique as alterações no Git e mantenha cópias de segurança quando necessário.

## Caminho de evolução

| Etapa | Situação |
|---|---|
| Estrutura inicial, schemas e validação | **Concluída** |
| Catálogo técnico inicial do Espírito Santo | **Iniciado** |
| Cobertura geográfica das 27 UFs via IBGE | **Concluída** |
| Importadores de fontes públicas e critérios de licenciamento | **Planejado / em evolução** |
| Ampliação do catálogo técnico por região | **Em expansão** |
| Pesquisa pública e visualização cartográfica | **Planejado** |
| Exportadores para softwares de programação de rádio | **Planejado** |
| Internacionalização da arquitetura | **Visão futura** |

O avanço será gradual: **qualidade, verificabilidade e direitos de publicação têm prioridade sobre quantidade de registros**.

## Construído com a comunidade

Você não precisa ser especialista para participar. É possível ajudar corrigindo nomes, relatando links quebrados, explicando termos técnicos, encontrando documentos públicos ou contribuindo com software.

Se desejar enviar dados de radiofrequência, inclua uma **fonte identificável**, o contexto do registro e a situação da permissão de redistribuição. Relatos de recepção independente precisam de data e método de observação.

Leia o [Guia de contribuição](CONTRIBUTING.md), o [Código de Conduta](CODE_OF_CONDUCT.md) e a [Política de Segurança](SECURITY.md).

## Responsabilidade e licenciamento

- O RadioSync é uma **iniciativa comunitária independente**, não um cadastro oficial da Anatel ou de outro órgão governamental.
- Frequências documentadas **não representam permissão para transmitir**. Observe a regulamentação, a licença e a homologação aplicáveis.
- O projeto não deve divulgar credenciais, conteúdo de comunicações privadas protegidas ou dados restritos de terceiros.
- Informações de fontes como RadioReference não podem ser incorporadas à base pública sem autorização de redistribuição adequada.
- **A licença geral do repositório ainda não foi adotada.** Uma [proposta de licenciamento](docs/LICENSING_PROPOSAL.md) está em análise; não presuma autorização para reutilizar todo o conteúdo apenas porque o repositório é público.

## Criador e identidade do projeto

**RadioSync — Brasil Radio Frequências** é uma iniciativa idealizada, criada e mantida por **[h4ckd4d](https://github.com/H4ckD4d)**.

> **Do sinal à informação. Do Brasil para o mundo.**

Contribuidores recebem o devido reconhecimento por suas contribuições, assim como autores e organizações responsáveis pelas fontes consultadas. Conheça a seção de [Autoria e colaboradores](AUTHORS.md).

---

**RadioSync · Brasil Radio Frequências · h4ckd4d**  
*Conhecimento técnico com origem identificada, linguagem acessível e compromisso com a informação responsável.*
