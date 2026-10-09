# Fontes e política de redistribuição — RadioSync

> **Do sinal à informação. Do Brasil para o mundo.**  
> Política de procedência do **RadioSync — Brasil Radio Frequências**, iniciativa de **[h4ckd4d](https://github.com/H4ckD4d)**.

## Por que registrar as fontes?

Uma informação técnica só é realmente útil quando podemos responder **quem publicou, quando, sobre qual região, em que contexto e com que autorização de uso**.

No RadioSync, cada registro técnico deve preservar sua procedência. **Estar visível na internet não equivale a estar liberado para cópia ou redistribuição.**

O campo `redistribution_permission` orienta os exportadores: registros restritos ou pendentes de análise não podem ser incluídos em exportações públicas por padrão.

## Classes de fontes

| Valor de `source_type` | O que significa | Comprova operação atual? |
|---|---|---|
| `official_documentation` | Documento de órgão regulador ou autoridade competente. | **Não** |
| `operator_report` | Informação fornecida pelo responsável pela estação ou sistema. | **Não, isoladamente** |
| `community_submission` | Contribuição comunitária acompanhada de evidências. | **Não, isoladamente** |
| `secondary_compilation` | Lista compilada a partir de terceiros. | **Não** |
| `independent_reception` | Observação direta documentada, com data e método. | **Sim, apenas no limite observado** |
| `unknown` | Origem ainda sob análise. | **Não** |

**Autorização e atividade são coisas diferentes:** um documento regulatório não prova que um transmissor esteja no ar; a recepção de um sinal também não prova que sua operação esteja autorizada.

## Cadastro de fontes atualmente referenciadas

### 1. IBGE — base geográfica brasileira

- **Órgão:** Instituto Brasileiro de Geografia e Estatística (IBGE).
- **Finalidade:** identificação territorial e códigos oficiais de estados e municípios.
- **Referência:** https://www.ibge.gov.br/explica/codigos-dos-municipios.php
- **API de localidades:** https://servicodados.ibge.gov.br/api/v1/localidades/
- **Aplicação no RadioSync:** índices territoriais das 27 unidades federativas.
- **Limitação:** códigos e nomes municipais **não constituem evidência de frequências ativas**.

A abrangência nacional da geografia foi implantada em outubro de 2026. O catálogo técnico continua em expansão progressiva.

### 2. Anatel — Ato nº 883/2024

- **Órgão:** Agência Nacional de Telecomunicações (Anatel).
- **Finalidade no conjunto inicial:** documentação técnica de canais VHF marítimos.
- **Referência:** https://informacoes.anatel.gov.br/legislacao/atos-de-requisitos-tecnicos-de-gestao-do-espectro/2024/1918-ato-883
- **Tratamento:** manter atribuição ao órgão e distinguir regras nacionais de atividade efetiva em uma localidade.
- **Atualização indicada no histórico do projeto:** o Ato nº 5018/2026 alterou requisitos; revisões futuras precisam comparar os dispositivos e campos afetados antes de modificar registros.

### 3. DECEA — AISWEB NOTAM E6356/26

- **Órgão:** Departamento de Controle do Espaço Aéreo (DECEA).
- **Finalidade no conjunto inicial:** referências de comunicação aeronáutica com validade temporal específica.
- **Referência:** https://aisweb.decea.mil.br/?i=notam&notam_id=12974142&view=single
- **Tratamento:** documentação oficial, **não** observação independente de recepção.
- **Limites:** os registros mantêm a janela de validade em `notes` e não podem ser interpretados como canais permanentes de aeródromo. Termos de redistribuição permanecem sujeitos a revisão.

### 4. Levantamento de repetidoras do Espírito Santo (2025)

- **Publicação:** levantamento datado de 18/02/2025, exibido no Scribd.
- **Publicador exibido:** Cleverson PU1CAC.
- **Referência:** https://pt.scribd.com/document/838374672/Repetidoras-ES-e-Mantenedores-18022025
- **Tratamento:** compilação secundária, classificada como `restricted` no histórico de dados; a página apresenta a indicação *All Rights Reserved*.
- **Limitação:** registros classificados como `source_only` reproduzem uma afirmação documental, não uma operação comprovada em campo. Não devem entrar em exportações redistribuíveis sem permissão ou fundamento factual independente e legalmente reutilizável.

### 5. RepeaterBook — referências históricas

Algumas observações legadas mencionam o RepeaterBook, mas **não houve importação de registros dessa plataforma** e não há URL de registro específico atualmente utilizada como verificação independente.

Qualquer integração futura deverá avaliar os termos vigentes e obter as permissões necessárias. Não faça coleta ou importação automatizada sem essa análise.

## Integração RadioReference: separação obrigatória

O RadioSync mantém uma fronteira técnica entre seu **repositório público** e uma eventual integração **privada**, por usuário, para programação pessoal de equipamentos, sujeita a autorização e aos termos do serviço.

- [Informações sobre a API](https://support.radioreference.com/hc/en-us/articles/18844460198932-Database-Web-Service-API)
- [Termos do RadioReference](https://www.radioreference.com/terms/)
- [Referência WSDL](https://api.radioreference.com/soap2/?wsdl&v=latest)

**Nunca inclua no Git:** credenciais, respostas autenticadas da API, caches ou material licenciado do RadioReference. Dados derivados dessa integração não devem ser incorporados aos CSVs públicos sem permissão expressa de redistribuição.

## Checklist antes de importar uma nova fonte

1. Identifique órgão, autor ou responsável pela publicação.
2. Registre URL canônica, data de publicação e data de consulta.
3. Consulte e documente os termos de licença e redistribuição.
4. Verifique se a extração e a republicação são permitidas.
5. Descreva como os campos foram interpretados ou transformados.
6. Valide dados, identificadores e possíveis duplicidades.
7. Se a situação dos direitos não estiver esclarecida, use `review_required`.
8. Mantenha materiais brutos restritos fora do Git e de exportações públicas.

Leia também o [formato dos dados](DATA_FORMAT.md), [como contribuir](../CONTRIBUTING.md) e a [proposta de licenciamento](LICENSING_PROPOSAL.md).

---

**RadioSync · Brasil Radio Frequências · h4ckd4d**
