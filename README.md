# Documentação do Persona Bot

<p align="center">
  <img img width="400" height="288" src="https://github.com/ViniciusHora1009/persona-bot/blob/main/imagens/persona-bot-circle.png">
</p>

### Sobre o Persona Bot
O Persona Bot é um bot de Discord criado para auxiliar a execução do meu sistema de combate de RPG baseado na série de jogos "Persona". O Bot conta com:<br>

| Função                                          | Status       |
|:-----------------------------------------------:|:------------:|
| Rolagem automática de dado                      | Finalizado   |
| Visualização de ficha do jogador e dos inimigos | Finalizado   |
| Sistema de inventário inteligente               | Finalizado   |
| Execução de drop de itens                       | Andamento    |
| Cálculo de dano                                 | Andamento    |

[Convidar o Persona Bot ao meu servidor](https://discord.com/api/oauth2/authorize?client_id=788843258306101279&permissions=8&scope=bot)<br>

### Sobre o Sistema de combate
O sistema de combate está sendo criado do zero por mim e se encontra hospedado no meu Google Drive.<br>
[Pasta do Sistema](https://drive.google.com/drive/folders/16OB41w_IHq1p9vzMyiCOC2TrLpnopyDq?usp=sharing)

### Rolagem automática de dado
Para que os jogadores possam executar suas ações será necessário rodar um dado D100. Para que não seja necessário programas auxiliares, o Persona Bot se encarregará dessa tarefa, fornecendo comandos e funções automáticas para a rolagem de dados.

#### p!rolldice
A versão mais intuitiva da rolagem de dados, perguntando diretamente ao jogador qual a quantia de dados e lados dos dados que deseja rolar. Adequada a jogadores iniciantes.

#### p!roll xdy ou p!r xdy (onde "x" é um número inteiro maior que 0, que representa a quantidade de dados; e "y" é um número inteiro maior que 0 que representa a quantidade de lados do(s) dado(s))
A versão mais dinâmica e simples da rolagem de dados, para rolagens rápidas sem atrapalhar a sessão.

#### Rolagem pronta
A rolagem criada pelo bot diretamente ao jogador para que o valor da rolagem seja usado diretamente no cálculo de alguma ação ou mecânica, a rolagem pronta é definida pelo próprio bot e para executá-la o jogador necessita somente clicar na reação com emoji de dado. 
A rolagem pronta é muito importante para cálculo de dano, pois retorna a função de cálculo o valor exato do dado para que se dê procedência ao jogo.

### Visualização de ficha do jogador e dos inimigos

#### p!mostra_ficha <nome da persona>
Mostra a ficha com Atributos e Afinidades Elementais da um Persona. Para poder mostrar essa ficha completa é necessário saber o nome da Persona, que é revelado após se obter o poder dela.

#### p!info_shadow <nome da shadow>
Mostra as Afinidades Elementais conhecidas de uma Shadow inimiga, o parâmetro é o seu codinome, mostrado em batalha.
  
#### p!revelar_afinidade <nome da shadow>
Cria um embed sobre a Shadow, o jogador precisará reagir com o emote do elemento que deseja ser revelado. Utilizado depois de scans ou descobrir forçadamente a afinidade (através de habilidades do respectivo elemento).
  
#### p!esconder_afinidade <nome da shadow>
Cria um embed sobre a Shadow, o jogador precisará reagir com o emote do elemento que deseja ser escondida. Utilizado quando uma afinidade é revelada acidentamente.

### Sistema de inventário inteligente

#### p!add_item <quantidade> <nome do item>
Adiciona ou soma do inventário do grupo um determinado item.
  
#### p!del_item <quantidade> <nome do item>
Deleta ou subtrai do inventário do grupo um determinado item.
  
#### p!inventario
Mostra organizadamente o inventário e dinheiro do grupo, com itens separados por categoria.

#### p!setar_dinheiro <quantia>
Altera a quantia de dinheiro do grupo para a definida pelo jogador.

#### p!modificar_dinheiro <quantia (positiva ou negativa)>
Soma ou subtrai uma quantia à quantia de dinheiro do grupo.

### Execução do drop de itens

### Cálculo de dano
