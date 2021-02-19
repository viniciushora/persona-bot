# Documentação do Persona Bot

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/532ac7b89b9c43c18d8929af29915e6f)](https://app.codacy.com/gh/ViniciusHora1009/persona-bot?utm_source=github.com&utm_medium=referral&utm_content=ViniciusHora1009/persona-bot&utm_campaign=Badge_Grade)

![GitHub repo size](https://img.shields.io/github/repo-size/ViniciusHora1009/persona-bot)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/ViniciusHora1009/persona-bot?include_prereleases)
![GitHub top language](https://img.shields.io/github/languages/top/ViniciusHora1009/persona-bot)

<p align="center">
  <img img width="400" height="288" src="https://github.com/ViniciusHora1009/persona-bot/blob/main/imagens/persona-bot-circle.png">
</p>

## Sobre o Persona Bot
O Persona Bot é um bot de Discord criado para auxiliar a execução do meu sistema de combate de RPG baseado na série de jogos "Persona". O Bot conta com:<br>

| Função                                          | Status       |
|:-----------------------------------------------:|:------------:|
| Rolagem automática de dado                      | Finalizado   |
| Visualização de ficha do jogador e dos inimigos | Finalizado   |
| Sistema de inventário inteligente               | Finalizado   |
| Execução de drop de itens                       | Finalizado   |
| Cálculo de dano                                 | Finalizado   |
| Execução de mecânicas de combate                | Finalizado   |
| Sistema de canal inteligente dos jogadores      | Finalizado   |

[Convidar o Persona Bot ao meu servidor](https://discord.com/api/oauth2/authorize?client_id=788843258306101279&permissions=8&scope=bot)<br>

## Sobre o Sistema de combate
O sistema de combate está sendo criado do zero por mim e se encontra hospedado no meu Google Drive.<br>
[Pasta do Sistema](https://drive.google.com/drive/folders/16OB41w_IHq1p9vzMyiCOC2TrLpnopyDq?usp=sharing)

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
