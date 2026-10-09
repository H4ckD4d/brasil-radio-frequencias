# Política de Segurança — RadioSync

> **RadioSync — Brasil Radio Frequências**  
> **Do sinal à informação. Do Brasil para o mundo.**  
> Projeto criado e mantido por **[h4ckd4d](https://github.com/H4ckD4d)**.

## Versões suportadas

O RadioSync encontra-se **em desenvolvimento, antes de uma versão estável**. Correções de segurança são aplicadas à branch `main`. Ainda não há uma versão publicada com suporte de segurança separado.

## Como informar uma vulnerabilidade

**Não abra uma Issue pública** para relatar vulnerabilidades que possam expor dados pessoais, credenciais, informações privadas ou conteúdos cuja redistribuição seja restrita.

Use, preferencialmente, o recurso de **relato privado de vulnerabilidades do GitHub**, quando estiver disponível neste repositório. Caso contrário, contate o mantenedor reservadamente pelos meios indicados no [perfil de h4ckd4d](https://github.com/H4ckD4d).

Descreva, na medida do possível:

1. O problema identificado e os arquivos ou versões afetados.
2. Os passos mínimos necessários para demonstrá-lo.
3. O possível impacto.
4. Uma medida de correção sugerida, caso exista.

Não acesse conteúdo além do necessário para demonstrar um problema. Não encaminhe credenciais RadioReference, tokens de sessão, dados de terceiros ou respostas de APIs licenciadas.

## Problemas de qualidade de dados

Uma frequência imprecisa, uma situação operacional desatualizada ou um link de fonte quebrado normalmente constitui um **problema de qualidade de dados**, não uma vulnerabilidade. Utilize uma Issue de correção, desde que sua publicação não exponha conteúdo privado ou restrito.

## Proteção de segredos

Credenciais devem ser fornecidas em tempo de execução por variáveis de ambiente ou por gerenciadores de segredos aprovados.

**Nunca publique segredos** em:

- Scripts, arquivos de configuração ou CSVs;
- Testes e dados fictícios de exemplo;
- Logs e resultados de exportação;
- Issues ou Pull Requests;
- Respostas de serviços autenticados.

A eventual integração RadioReference é separada da base pública e deve respeitar os termos do serviço e os direitos de redistribuição.

Veja também o [Código de Conduta](CODE_OF_CONDUCT.md) e a [Política de fontes](docs/DATA_SOURCES.md).

---

**RadioSync · Brasil Radio Frequências · h4ckd4d**
