# Como contribuir com o RadioSync

> **RadioSync — Do sinal à informação. Do Brasil para o mundo.**  
> Projeto criado e mantido por **[h4ckd4d](https://github.com/H4ckD4d)**.

O **RadioSync — Brasil Radio Frequências** é uma iniciativa colaborativa para organizar referências de radiocomunicação de forma acessível e verificável. Você pode ajudar mesmo sem conhecer programação: uma fonte bem documentada ou uma correção fundamentada já faz diferença.

**Nosso princípio:** a origem e a qualidade da informação são mais importantes do que a quantidade de frequências cadastradas.

## Como posso ajudar?

- **Sou iniciante:** relate erros de digitação, links quebrados, dificuldades para entender a documentação ou termos que precisem de explicação.
- **Sou radioamador ou operador autorizado:** envie referências públicas de estações, indicativos e parâmetros, com a fonte e o contexto.
- **Sou pesquisador ou técnico:** revise metadados, métodos de verificação, classificações e documentação.
- **Sou desenvolvedor:** contribua com importadores, validadores, testes, filtros, documentação e exportadores.

Para começar, abra uma [Issue](https://github.com/H4ckD4d/brasil-radio-frequencias/issues) descrevendo sua sugestão ou envie um Pull Request com uma alteração bem delimitada.

## Regras para propor um registro de frequência

Cada registro precisa obedecer ao [formato oficial do projeto](docs/DATA_FORMAT.md) e deve informar, conforme aplicável:

1. **Localização:** país, UF, município e código IBGE correto. Não confunda distrito ou bairro com município.
2. **Identificação:** serviço, estação, indicativo ou designação do canal, quando conhecidos.
3. **Parâmetros técnicos:** RX/TX e demais campos comprovados pela fonte. Campos desconhecidos ficam vazios.
4. **Procedência:** nome da fonte, URL HTTPS e atribuição a quem publicou a informação.
5. **Datas:** publicação/consulta da fonte e data de observação independente, quando houver.
6. **Situação de verificação:** diferença clara entre afirmação de uma fonte e recepção independente documentada.
7. **Direitos:** `redistribution_permission` compatível com os termos do material consultado.

As categorias reconhecidas para `source_type` são: `official_documentation`, `operator_report`, `community_submission`, `secondary_compilation`, `independent_reception` e, quando necessário, `unknown`.

**Atenção:** uma frequência presente em documento oficial não é necessariamente uma transmissão ativa. Dados publicados na internet não são automaticamente livres para redistribuição.

## Se você verificou uma frequência pessoalmente

Use `source_type=independent_reception` **somente** quando houve observação direta e documentada. Inclua:

- Data em UTC ou com o fuso horário claramente identificado.
- Método geral de verificação e tipo de equipamento receptor.
- Contexto suficiente para diferenciar a estação ou o canal.
- Grau de certeza e limitações da identificação.

Uma portadora recebida, isoladamente, não confirma a identidade da estação. Se houver dúvida, abra uma Issue em vez de afirmar que a estação está identificada.

**Nunca envie** áudio de conversas privadas, dados pessoais desnecessários, credenciais ou conteúdo protegido.

## Como enviar uma alteração pelo GitHub

1. Leia o [README](README.md) e o [formato dos dados](docs/DATA_FORMAT.md).
2. Faça um *fork* do repositório e crie uma branch para sua correção.
3. Edite apenas os arquivos relevantes, sem remover registros ou créditos de terceiros.
4. Execute os testes, se sua contribuição envolver dados ou código Python:

   ```powershell
   python .\scripts\validate_csv.py
   python -m unittest discover -s tests -v
   ```

5. Abra um *Pull Request* explicando o que mudou, as fontes, as transformações e eventuais incertezas.

Prefira Pull Requests pequenos. Alterações de dados e alterações de software devem, em geral, ser separadas.

## Identidade dos registros

O campo `record_id` é estável: não o altere apenas porque o nome de uma estação ou seu status mudou. Ao corrigir um registro, documente a evidência. Suspeitas de duplicidade precisam de revisão; não apague registros silenciosamente.

## Segurança do ambiente de trabalho

Sempre que possível, mantenha a cópia de trabalho do Git em um disco local, **fora de pastas sincronizadas continuamente** por serviços como Google Drive. A sincronização dos arquivos internos de `.git` pode gerar conflitos ou cópias incompletas.

Se precisar trabalhar em pasta sincronizada, não abra a mesma cópia em dois computadores ao mesmo tempo. Espere a sincronização terminar antes e depois das operações Git e verifique `git status`. Em caso de conflito, faça backup e avalie `git fsck` antes de qualquer reparo.

## Autoria, fontes e licenças

O RadioSync foi criado por **[h4ckd4d](https://github.com/H4ckD4d)**. A contribuição de outras pessoas deve ser reconhecida pelo histórico Git, Pull Requests e pelo arquivo [AUTHORS.md](AUTHORS.md), quando apropriado.

A autoria das fontes também deve ser registrada em `attribution`. Ninguém adquire direitos sobre conteúdo de terceiros apenas por cadastrá-lo no RadioSync.

**Ainda não existe uma licença geral aprovada para o repositório.** Veja a [proposta de licenciamento](docs/LICENSING_PROPOSAL.md). Ao contribuir, você confirma que possui direito de enviar o conteúdo e informa quaisquer restrições aplicáveis. O mantenedor pode suspender a incorporação de material com situação de direitos indefinida.

## Respeito, responsabilidade e segurança

Siga o [Código de Conduta](CODE_OF_CONDUCT.md). Vulnerabilidades, dados privados e credenciais devem ser comunicados conforme a [Política de Segurança](SECURITY.md), nunca em Issues públicas.

Obrigado por contribuir para que o conhecimento em radiocomunicação seja mais organizado, acessível e responsável no Brasil.

**RadioSync · Brasil Radio Frequências · h4ckd4d**
