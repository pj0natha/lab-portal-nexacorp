# Relatório de Pentest — Portal NexaCorp

## O que é entregue

Um **relatório de teste de intrusão**, no formato **`.pdf`**, documentando
a exploração de vulnerabilidades encontradas no portal NexaCorp
(`lab-portal-nexacorp`). Não é entregue código, script de automação nem a
flag "solta" — o que vale nota é o **relatório**, como se fosse o
entregável de um engajamento real de pentest para um cliente.

### Nome do arquivo

O arquivo **deve** seguir esta nomenclatura, sem acentos e em MAIÚSCULAS:

```
2TDCPR_2026_GS_WEB-MOB_SOBRENOME-NOME_RM123456.pdf
```

| Campo | Significado |
|---|---|
| `2TDCPR` | turma |
| `2026` | ano |
| `GS` | código da atividade |
| `WEB-MOB` | matéria (Web and Mobile Exploitation) |
| `SOBRENOME-NOME` | seu sobrenome e nome, nessa ordem |
| `RM123456` | seu RM, sempre por último |

Um arquivo fora desse padrão (nome com acento, minúsculas, campos fora de
ordem, extensão diferente de `.pdf`) **não é recusado**, mas tem
**0,5 ponto descontado** da nota final.

## Requisito mínimo

Documentar, **de forma completa**, pelo menos **3 vulnerabilidades
distintas exploradas com sucesso**, sendo obrigatoriamente:

- **ao menos uma das vulnerabilidades que concede acesso administrativo**
  na aplicação (qualquer uma, você escolhe o caminho);
- **o objetivo final da cadeia de ataque** — alcançável só depois de
  obter acesso admin por algum caminho.

A terceira vulnerabilidade (e eventuais adicionais) fica a seu critério —
documente o que você conseguiu explorar com sucesso.

Documentar mais de 3 vulnerabilidades, incluindo o bônus, é permitido e
bem-vindo, e pode ser usado para compensar algum critério perdido em outro
bloco, mas não aumenta a nota além do máximo (10) — o foco é a
**qualidade e completude** de cada bloco documentado, não a quantidade.

## Estrutura obrigatória do relatório

### 1. Identificação

- Nome do aluno
- Data da execução
- Alvo testado: `NexaCorp` (`http://localhost:8084`, ambiente local via
  Docker)

### 2. Metodologia (breve)

Um parágrafo descrevendo a abordagem geral: reconhecimento manual da
aplicação, uso das credenciais de baixo privilégio fornecidas, e a
exploração manual de cada ponto encontrado. Ferramentas utilizadas (ex:
Burp Suite, `curl`, navegador, DevTools).

### 3. Um bloco por vulnerabilidade documentada

Repita esta estrutura para **cada** vulnerabilidade documentada (mínimo 3
blocos, ver requisito mínimo acima):

#### 3.X. [Nome da vulnerabilidade] — [rota/parâmetro afetado]

**a) Reconhecimento**
Como você chegou até esse ponto. Se envolveu descobrir algo que não estava
visível na navegação normal (ex: um comentário HTML, um endpoint de API),
mostre como achou.

**b) Identificação da vulnerabilidade**
O que indicou que o ponto era explorável (ex: erro de sintaxe do banco,
mudança de comportamento, campo refletido sem tratamento, campo aceito sem
validação). Print do teste inicial que confirmou a suspeita.

**c) Exploração / Prova de Conceito (PoC)**
- O(s) payload(s)/requisição(ões) final(is) utilizado(s), formatados como
  código — completo, sem cortar.
- O comando exato usado para enviar a requisição (`curl`, requisição do
  Burp, ou similar).
- Print de tela mostrando a requisição sendo enviada e a resposta
  recebida.

**d) Resultado obtido**
A flag extraída, em destaque, e o print de onde ela apareceu na resposta
da aplicação (ou no cookie, quando for o caso).

**e) Recomendação de correção**
Como a vulnerabilidade deveria ser corrigida. Específico para o ponto em
questão, não uma resposta genérica de "usar boas práticas" — a
recomendação certa depende da causa raiz que você identificou naquele
ponto específico.

**f) Referência**
Ao menos uma referência externa relevante para a técnica (ex: OWASP Top
10, um CWE, PortSwigger Web Security Academy, documentação oficial). Link
ou citação.

### 4. Conclusão (opcional)

Um parágrafo curto resumindo o risco geral encontrado e a criticidade das
vulnerabilidades exploradas, incluindo o impacto da cadeia completa.

## Regras sobre as evidências

- As capturas de tela devem ser **suas**, da sua própria execução do
  laboratório (`docker compose up --build`).
- Prints devem ser legíveis e mostrar o necessário (comando + resposta),
  sem cortar informação relevante.
- Payloads e comandos devem estar em texto (não só na imagem), para
  facilitar a leitura e a correção.

## Como você será avaliado

A nota (0 a 10) é a soma de **5 critérios por bloco** — reconhecimento,
identificação/exploração, PoC documentada, recomendação de correção e
referência — aplicados a cada um dos 3 blocos mínimos exigidos, até o teto
de 10 pontos.

| Bloco | Peso |
|---|---|
| Vulnerabilidade de acesso admin escolhida | 5 critérios |
| Vulnerabilidade adicional (sua escolha) | 5 critérios |
| Objetivo final da cadeia de ataque | 5 critérios |
| Vulnerabilidade bônus documentada | bônus (até +1, com os mesmos 5 critérios) |
