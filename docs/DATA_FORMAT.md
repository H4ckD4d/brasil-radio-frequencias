# Formato dos dados — RadioSync

> **Do sinal à informação. Do Brasil para o mundo.**  
> Documentação técnica do RadioSync, criado por **[h4ckd4d](https://github.com/H4ckD4d)**.

**Versão do schema:** `1.0.0`

Esta página explica o significado dos campos usados no catálogo de frequências. Para quem está começando, pense em cada registro como uma **ficha técnica de uma referência de rádio**: informa *onde*, *o quê*, *em qual frequência*, *segundo qual fonte* e *com que grau de confirmação*.

As regras oficiais e a ordem das colunas estão em [`schemas/frequency-record.schema.json`](../schemas/frequency-record.schema.json). Todos os CSVs usam UTF-8, cabeçalho, vírgulas para separar campos, ponto como separador decimal e datas ISO 8601 (`AAAA-MM-DD`).

**Nunca complete dados desconhecidos por suposição.** Campos opcionais desconhecidos ficam vazios.

## Identificação e geografia

| Campo | Significado |
|---|---|
| `record_id` | Identificador único e estável do registro dentro do RadioSync. |
| `country_code` | Código ISO 3166-1 alfa-2 do país, como `BR`. |
| `country_name` | Nome do país em inglês, conforme o schema atual. |
| `state_code` | Sigla da UF ou subdivisão administrativa equivalente. |
| `state_name` | Nome oficial do estado ou província. |
| `state_id` | Identificador geográfico oficial; no Brasil, código de 2 dígitos do IBGE. |
| `municipality_name` | Nome oficial do município; opcional para dados estaduais ou nacionais. |
| `municipality_slug` | Nome simplificado usado no caminho da pasta, sem acentos e em minúsculas. |
| `municipality_id` | Identificador oficial; no Brasil, código IBGE de 7 dígitos. |
| `locality_name`, `locality_id` | Localidade, distrito ou referência administrativa complementar. |
| `latitude`, `longitude` | Coordenadas decimais WGS 84, sempre informadas juntas. |
| `location_precision` | Precisão da posição: `exact`, `approximate`, `municipality`, `state` ou `country`. |

**Importante:** nomes de pastas (`slugs`) ajudam na navegação, mas não substituem os códigos IBGE. Bairros e distritos não são municípios. O Distrito Federal tem organização administrativa própria.

### Índice territorial

Cada UF possui um arquivo `dados/UF/municipios.csv` com estas colunas:

```csv
codigo_ibge,municipio,uf,pais
3202603,Iconha,ES,BR
```

A estrutura nacional possui 27 índices territoriais baseados no IBGE. Eles são **referências geográficas**, não uma relação de frequências ativas.

## Estação e parâmetros de rádio

| Campo | Significado |
|---|---|
| `service` | Tipo de serviço, como `amateur_radio`, `aviation` ou `maritime`. |
| `station_name` | Nome publicado da estação ou do local de transmissão, quando disponível. |
| `callsign` | Indicativo de chamada atribuído à estação; não use rótulos genéricos. |
| `channel_designator` | Identificação publicada do canal, como `CH16`. |
| `rx_frequency_mhz` | Frequência de recepção no rádio programado, em MHz, com 4 a 6 casas decimais. |
| `tx_frequency_mhz` | Frequência de transmissão do rádio programado; opcional em referências apenas de recepção. |
| `modulation` | Modulação segundo os valores controlados pelo schema. Para sistemas digitais, `digital`. |
| `digital_protocol` | Protocolo, como `DMR`, `P25`, `TETRA`, `AIS` ou `DSC`. |
| `ctcss_hz`, `dcs_code` | Parâmetros de acesso analógico, quando documentados. |
| `dmr_color_code`, `dmr_timeslot` | Parâmetros DMR, somente quando conhecidos. |
| `repeater_offset_mhz` | Diferença `TX - RX`, com sinal; deixe vazia se os dados de origem forem incertos. |

**RX** significa *recepção* e **TX** significa *transmissão*, sempre sob a perspectiva do equipamento a ser programado. Em uma repetidora, RX normalmente corresponde à frequência de saída da repetidora e TX à frequência de entrada.

O preenchimento de uma frequência de TX **não concede autorização para transmitir**.

## Procedência e verificação

| Campo | Significado |
|---|---|
| `source_type` | Classe da fonte, conforme [Política de fontes](DATA_SOURCES.md). |
| `source_claim` | Afirmação original da fonte, sem elevar seu grau de certeza. |
| `source_name` | Nome da entidade, publicação ou fonte consultada. |
| `source_url` | Endereço HTTPS absoluto da fonte. |
| `source_publication_date` | Data de publicação ou atualização, se conhecida. |
| `source_accessed_date` | Data em que a fonte foi consultada. |
| `last_independently_verified_date` | Data da verificação independente efetiva — não a data da fonte. |
| `verification_method` | Método resumido utilizado para observar o sinal independentemente. |
| `verification_status` | `official_documentation`, `source_only`, `independently_verified`, `disputed` ou `unverified`. |
| `operational_status` | `unknown`, `reported_active`, `reported_inactive`, `verified_active`, `verified_inactive` ou `not_applicable`. |

**Exemplo de interpretação:** `reported_active` quer dizer que uma fonte *relatou* a estação como ativa. `verified_active` exige verificação independente, com data e método. Uma autorização oficial não comprova transmissão atual.

## Direitos de redistribuição e observações

| Campo | Significado |
|---|---|
| `redistribution_permission` | `allowed`, `allowed_with_attribution`, `restricted` ou `review_required`. |
| `data_license` | Identificador SPDX, URL/nome da licença ou declaração de direitos da fonte. |
| `attribution` | Créditos à fonte e ao responsável pelo conteúdo. |
| `notes` | Limitações, dúvidas, contexto, validade ou outras observações factuais. |

Exportadores públicos devem selecionar somente registros `allowed` ou `allowed_with_attribution`, mantendo os créditos exigidos. Os estados `restricted` e `review_required` não autorizam redistribuição por padrão.

## Identificadores e duplicidades

O validador rejeita `record_id` duplicados e duplicidades de chaves técnicas que combinam geografia, serviço, indicativo/canal e frequências RX/TX.

Não altere `record_id` por mudanças superficiais de nome ou situação operacional. Fontes diferentes que aparentem descrever a mesma estação precisam de análise antes de qualquer consolidação.

## Exemplo didático

O exemplo a seguir é **fictício e abreviado**; não representa uma estação real nem uma frequência confirmada:

```csv
record_id,country_code,country_name,state_code,state_name,state_id,municipality_name,municipality_slug,municipality_id,service,rx_frequency_mhz,modulation,source_type,source_name,source_url,verification_status,operational_status,redistribution_permission
EXAMPLE-001,BR,Brazil,ES,Espírito Santo,32,Vitória,vitoria,3205309,amateur_radio,145.0000,FM,community_submission,Example source,https://example.invalid/source,unverified,unknown,review_required
```

**Um arquivo de dados real precisa conter todas as colunas canônicas na ordem exigida pelo schema.** Veja [Como contribuir](../CONTRIBUTING.md) e execute o validador descrito no [README](../README.md).

---

**RadioSync · Brasil Radio Frequências · h4ckd4d**
