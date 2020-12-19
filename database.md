# Banco de dados do Persona Bot

### Sobre o banco de dados
O banco de dados utilizado é o PostgreSQL, hosteado na nuvem através do ElephantSQL, escolhido devido a alguns relacionamentos entre as classes, que ao meu ver seriam melhor trabalhadas em um banco de dados relacional. <br>
Como o bot se engarregará somente de tarefas "simples" e automatizadas como calcular o dano, gerenciar inventário, dropar os itens, evoluir atributos e habilidades das Personas, não é necessário uma lógica muito aprofundada no banco de dados. Sendo assim, as tabelas tem poucos atributos e a base de dados foi separada em "Árvore" e "Construção".<br>
A "Árvore" é a base dos valores do jogo. Ela armazena informações sobre os números de desenvolvimento das Personas, como o crescimento de atributo por nível e os golpes aprendidos por nível. A "Construção" se refere aos valores dos atributos e golpes aprendidos pela Persona do jogador em um momento específico do jogo.

### Modelo conceitual do banco de dados

### Informações armazenadas

Do jogador: Nome do personagem, Persona(s) (Nome, Foto (link), Atributos e Habilidades);<br>
Do Grupo: Dinheiro e Itens;<br>
Das Personas: Nome, árvore de crescimento de atributos, árvore de habilidades, atributos e interações com atributos<br>
Dos itens: Nome<br>
Dos atributos: Intensidade do multiplicador<br>

![Alt text](https://github.com/ViniciusHora1009/persona-bot/blob/main/imagens/PersonaBot.png "Modelo conceitual")

### Inserindo informações nas colunas primárias
São as colunas que dependem apenas de si para existir, sem chaves estrangeiras.

### Tabela arcana
![Alt text](https://github.com/ViniciusHora1009/persona-bot/blob/main/imagens/insert1.PNG "Arcana")

### Tabela atributo
![Alt text](https://github.com/ViniciusHora1009/persona-bot/blob/main/imagens/insert2.PNG "Atributo")

### Tabela elemento
![Alt text](https://github.com/ViniciusHora1009/persona-bot/blob/main/imagens/insert5.PNG "Interação Atributo")

### Tabela interacao_elemento
![Alt text](https://github.com/ViniciusHora1009/persona-bot/blob/main/imagens/insert4.PNG "Interação Atributo")

### Tabela intensidade
![Alt text](https://github.com/ViniciusHora1009/persona-bot/blob/main/imagens/insert3.PNG "Intensidade")
