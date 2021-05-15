# Documentação do Persona Bot

![GitHub repo size](https://img.shields.io/github/repo-size/ViniciusHora1009/persona-bot)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/ViniciusHora1009/persona-bot?include_prereleases)
![GitHub top language](https://img.shields.io/github/languages/top/ViniciusHora1009/persona-bot)

<span class="badge-buymeacoffee">
<a href="https://www.buymeacoffee.com/viniciusdahora" title="Donate to this project using Buy Me A Coffee"><img src="https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg" alt="Buy Me A Coffee donate button" /></a>
</span>

<span class="badge-download-latest">
<a href="https://github.com/ViniciusHora1009/persona-bot/releases/download/v.1.1.0-beta/PersonaBot-v1.1.0-beta.zip" title="Download PersonaBot latest version"><img src="https://badgen.net/badge/download/v1.1.0-beta/:blue?icon=github" alt="Download button" /></a>
</span>

<p align="center">
  <img img width="400" height="288" src="https://github.com/ViniciusHora1009/persona-bot/blob/main/imagens/persona-bot-circle.png">
</p>

## Sobre o Persona Bot
O Persona Bot é um bot de Discord criado para auxiliar a execução de sessões de RPG de mesa online com sistema baseada na série de jogos "Persona":<br>

| Função                                          | Status       |
|:-----------------------------------------------:|:------------:|
| Rolagem automática de dado                      | Finalizado   |
| Visualização de ficha do jogador e dos inimigos | Finalizado   |
| Sistema de inventário inteligente               | Finalizado   |
| Execução de drop de itens                       | Finalizado   |
| Cálculo de dano                                 | Finalizado   |
| Execução de mecânicas de combate                | Finalizado   |
| Sistema de canal inteligente dos jogadores      | Finalizado   |

[Baixe o PersonaBot](https://github.com/ViniciusHora1009/persona-bot/releases/download/v1.0.0-beta/personabot-v1.0.0-beta.zip)

## Funcionalidades

Confira a [Lista de Comandos](https://github.com/ViniciusHora1009/persona-bot/blob/main/comandos.md)

### Sistema de canal inteligente dos jogadores
No Persona Bot, o mestre gerencia a maioria dos comandos, sendo ele que envia os dados das ações aos jogadores, informações dos inimigos, informações do inventário, informações de combate, etc. Para aumentar a imersão, esses dados e informações são enviados diretamente para o jogador em seu canal, que será onde ele executará suas ações e visualizará suas informações. Esses canais serão previamente registrados através de comandos pelo mestre, podendo ser alterados caso necessário. Cada jogador tem seu canal, além do canal do mestre, do grupo, do suporte e dos inimigos.

<p align="center">
  <img src="https://github.com/ViniciusHora1009/persona-bot/blob/main/imagens/print0.PNG">
</p>

### Rolagem automática de dado
Para que os jogadores possam executar suas ações será necessário rodar um dado D100. Para que não seja necessário programas auxiliares, o Persona Bot se encarregará dessa tarefa, fornecendo comandos e funções automáticas para a rolagem de dados.<br>
Com o sistema de batalha, além do dado personalizado que será direcionado ao jogador, também mostrará informações importantes ao mesmo, como qual valor abaixo que ele deve tirar para acertar um golpe ou habilidade.

<p align="center">
  <img src="https://github.com/ViniciusHora1009/persona-bot/blob/main/imagens/print1.PNG">
</p>
<p align="center">
  <img src="https://github.com/ViniciusHora1009/persona-bot/blob/main/imagens/print2.PNG">
</p>

### Ficha dos jogadores e inimigos
O bot informará aos jogadores as informações essenciais de seu personagem e dos inimigos encontrados. Dentre as informações do jogador estão: nome, arcana, atributos, habilidades e fraquezas. Dentre as informações dos inimigos estarão somente as suas fraquezas, essas informações serão enviadas ao canal do suporte. <br>
As informações disponíveis serão modificadas pelo mestre e ficarão visíveis aos jogadores.

<p align="center">
  <img src="https://github.com/ViniciusHora1009/persona-bot/blob/main/imagens/print3.PNG">
</p>

### Sistema de inventário inteligente
O inventário nesse sistema é compartilhado entre o grupo, então todo dinheiro e itens adquiridos são direcionados ao inventário independente de quem o tenha. Os itens que podem ser adicionados no inventário são aqueles previamente registrados no banco de dados. O mestre se encarregará de gerenciar esses itens para os jogadores.

<p align="center">
  <img src="https://github.com/ViniciusHora1009/persona-bot/blob/main/imagens/print4.PNG">
</p>

### Execução do drop de itens
O drop de itens será automatico, gerado através de um comando, será calculada a experiência adquirida pelo grupo e os itens dropados pelos inimigos aleatoriamente.

<p align="center">
  <img src="https://github.com/ViniciusHora1009/persona-bot/blob/main/imagens/print5.PNG">
</p>

### Mecânicas de combate
O bot se encarrega de automatizar cada mecânica de combate para deixar a sessão cada vez mais dinâmica. Conta com sistema de marcadores para tratar dos buffs/debuffs, modificados através de comandos pelo mestre; interações com elementos dos jogadores e inimigos pode ser modificada no meio do combate para aplicar condições de habilidades e itens. As ações como usar ataques físicos, arma de fogo ou habilidades são gerenciadas pelo mestre, que irá utilizar o comando específico e enviará o dado para o jogador em seu devido canal. Caso o jogador consiga o dado necessário, o bot realizará o cálculo do dano, levando em conta os atributos do atacante e do defensor, marcadores, interações, armadura e bônus aplicados.

<p align="center">
  <img src="https://github.com/ViniciusHora1009/persona-bot/blob/main/imagens/print6.PNG">
</p>
