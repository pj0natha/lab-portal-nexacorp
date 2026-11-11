# Portal NexaCorp — Instruções de Acesso

## Contexto

A NexaCorp é uma empresa fictícia. Você foi contratado(a) para um teste de
intrusão no portal interno de TI, disponível em `http://localhost:8084`. O
escopo é a aplicação completa — nenhuma área está fora de escopo.

## Formato

A aplicação reúne vulnerabilidades dos temas trabalhados ao longo do
semestre. Não há uma lista de onde cada uma está — isso faz parte do
reconhecimento.

A arquitetura geral é a seguinte:

- Existem **múltiplas trilhas independentes**. Você pode segui-las em
  qualquer ordem, e **não precisa explorar todas** para tirar a nota
  máxima (ver critérios de avaliação em `Requisitos-Relatorio.md`).
- Algumas dessas trilhas, quando exploradas com sucesso, concedem **acesso
  administrativo** na aplicação — por caminhos diferentes, você pode
  chegar ao mesmo lugar.
- Com acesso administrativo, um **objetivo final** fica desbloqueado,
  entregando a flag de maior valor.
- Existe um **bônus opcional**, também não detalhado aqui.

Ou seja: existem **várias portas de entrada possíveis para o mesmo
objetivo final**. Escolher um caminho e documentá-lo bem já contribui
para a nota — você não precisa encontrar todos.

## Credenciais fornecidas

Você recebe credenciais de uma colaboradora comum, para simular o ponto de
partida real de um atacante com acesso de baixo privilégio (ex: funcionário
que teve a senha vazada ou phishing):

```
usuario: ana.souza
senha:   Colab@123
```

Essas credenciais **não têm acesso administrativo**. É a partir delas (e do
reconhecimento da aplicação) que você deve escalar privilégios.

## Como subir o ambiente

```bash
git clone https://github.com/pj0natha/lab-portal-nexacorp.git
cd lab-portal-nexacorp
docker compose up --build
```

A aplicação ficará disponível em:

```
http://localhost:8084
```

Para derrubar o ambiente ao final:

```bash
docker compose down
```

## O entregável

Não existe entrega de código, script ou flag "solta" — a atividade é
avaliada pelo **relatório de pentest** que você produzir. Ver
[`Requisitos-Relatorio.md`](Requisitos-Relatorio.md) para a estrutura
completa, o mínimo exigido e os critérios de nota.

Bom pentest!
