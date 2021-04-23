# Lista de Comandos

Colchetes "[]" não inclusos.

## Canais

|                    Comando                    |                        Funcionalidade                        |
| :-------------------------------------------: | :----------------------------------------------------------: |
| p!canal_jogador [nome do personagem] [#canal] |       Define o canal do jogador como o canal declarado       |
|    p!canal_geral [tipo do canal] [#canal]     | Define um canal geral (grupo, inimigos, mestre ou suporte) como o canal declarado |
|                   p!canais                    |              Mostra todos os canais registrados              |

## Ficha

|                   Comando                   |                        Funcionalidade                        |      Canal enviado:      |
| :-----------------------------------------: | :----------------------------------------------------------: | :----------------------: |
|              p!atualizar_info               | Atualiza as informações conhecidas pelo grupo (Adiciona as novas Shadows cadastradas) |           ---            |
| p!persona <#canal> [nome] da persona> |                Mostra a ficha de uma Persona                 | Canal passado no comando |
|       p!shadow [nome da shadow]        |  Mostra as informações conhecidas pelo grupo de uma Shadow   |         Suporte          |
|             p!revelar_afinidade             | Desbloqueia ao grupo a informação sobre determinada interação com a Shadow |           ---            |
|            p!esconder_afinidade             | Bloqueia para o grupo a informação sobre determinada interação com a Shadow |           ---            |
|        p!ficha [nome do personagem]         |               Mostra a ficha de um personagem                |        Personagem        |

## Persona

|                           Comando                            |                        Funcionalidade                        | Canal enviado: |
| :----------------------------------------------------------: | :----------------------------------------------------------: | :------------: |
|                 p!upar [nome do personagem]                  | Aumenta o nível da Persona equipada do jogador em 1. Em caso de personagem de Arcana Fool, o nível aumentado é o do personagem |   Personagem   |
|                p!desupar [nome do personagem]                | Diminui o nível da Persona equipada do jogador em 1. Em caso de personagem de Arcana Fool, o nível diminuído é o do personagem |   Personagem   |
|             p!upar_persona [nome do personagem]              | Aumenta o nível da Persona equipada do personagem Fool em 1. |   Personagem   |
|            p!desupar_persona [nome do personagem]            | Diminui o nível da Persona equipada do personagem Fool em 1. |   Personagem   |
|            p!equipar_persona [nome do personagem]            |        Troca a Persona equipada de um personagem Fool        |   Personagem   |
|    p!tomar_persona [nome do personagem] [nome da persona]    |     Toma uma Persona para a posse de um personagem Fool      |   Personagem   |
|   p!soltar_persona [nome do personagem] [nome da persona]    |       Tira uma Persona da posse de um personagem Fool        |   Personagem   |
|         p!habilidades_conhecidas [nome dopersonagem]         | Mostra todas as habilidades que foram conhecidas pela Persona equipada de um personagem, sejam elas aprendidas ou não. |   Personagem   |
| p!aprender_habilidade [nome do personagem] [nome da habilidade] | Faz a Persona equipada do personagem aprender a habilidade desejada. |   Personagem   |
|          p!esquecer_habilidade [nome do personagem]          | Faz a Persona equipada do jogador esquecer a habilidade que for selecionada pelo mesmo. |   Personagem   |
| p!add_atributo [nome do personagem] [tipo do aumento] [quantidade] [id do atributo] | Aumenta o atributo de um jogador em determinada quantidade (percentual (p) ou normal (n)) |   Personagem   |
| p!del_atributo [nome do personagem] [quantidade] [id do atributo] | Diminui o atributo de um jogador em determinada quantidade.  |   Personagem   |

## Dado

|                           Comando                            |                        Funcionalidade                        | Canal enviado: |
| :----------------------------------------------------------: | :----------------------------------------------------------: | :------------: |
| p!rolagem [nome do personagem] [número de dados] [número de lados] |            Envia ao jogador uma rolagem de dados             |   Personagem   |
|                          p!rolldice                          | Informa uma determinada quantia de dados e lados e roda o dado. |      ---       |
|                  p!roll [xDy] ou p!r [xDy]                   |                Roda x dado(s) de y lado(s) .                 |      ---       |

## Item

|                     Comando                      |                        Funcionalidade                        | Canal enviado: |
| :----------------------------------------------: | :----------------------------------------------------------: | :------------: |
|      p!add_item [quantidade] [nome do item]      | Adiciona ao inventário do grupo uma determinada quantidade de um item |     Grupo      |
|      p!del_item [quantidade] [nome do item]      | Remove do inventário do grupo uma determinada quantidade de um item |     Grupo      |
|          p!modificar_dinheiro [quantia]          | Adiciona ou subtrai uma quantia de dinheiro do inventário do grupo. |     Grupo      |
|            p!setar_dinheiro [quantia]            |    Modifica o dinheiro do grupo para a quantia informada.    |     Grupo      |
|             p!drop [nome da shadow]              | Executa o drop automático de item de uma determinada Shadow, os itens vão automaticamente ao inventário do grupo. |     Grupo      |
|  p!equipar [nome do personagem] [nome do item]   |    Equipa em um personagem um determinado item equipável.    |   Personagem   |
| p!desequipar [nome do personagem] [nome do item] |   Desequipa em um personagem um determinado item equipado.   |   Personagem   |
|                   p!inventario                   |                Mostra o inventário do grupo.                 |     Grupo      |

## Combate

|                  Comando                  |                        Funcionalidade                        |     Canal enviado:     |
| :---------------------------------------: | :----------------------------------------------------------: | :--------------------: |
|  p!add_horda [s ou p] [nome do inimigo]   | Adiciona à horda um determinado inimigo, seja Shadow ou personagem. |          ---           |
|     p!add_party [nome do personagem]      |         Adiciona à party um determinado personagem.          |          ---           |
|       p!del_horda [nome do inimigo]       |           Retira da horda um determinado inimigo.            |          ---           |
|     p!del_party [nome do personagem]      |          Retira da party um determinado personagem.          |          ---           |
|   p!mestre [@nome do usuário do mestre]   |               Define um usuário como o mestre                |          ---           |
|   p!lider [nome do personagem do líder]   |            Define um jogador como líder da party.            |         Grupo          |
|                  p!party                  |                       Mostra a party.                        |          ---           |
|                  p!horda                  |                       Mostrar a horda.                       |          ---           |
|       p!lider [nome do personagem]        |          Denomina um personagem como líder da party          |         Grupo          |
|             p!calcular_turnos             |      Cálcula a ordem dos turnos com a horda e a party.       |         Grupo          |
|              p!ataque_fisico              | Escolhe um atacante e um defensor para um ataque físico. O dado é enviado ao atacante. | Inimigos ou Personagem |
|                  p!tiro                   | Escolhe um atacante da party para executar um tiro no inimigo. O dado é enviado ao atacante. |       Personagem       |
| p!habilidade [bônus] [nome da habilidade] | Escolhe um atacante e um defensor para uma habilidade de dano. O dado é enviado ao atacante. | Inimigos ou Personagem |
|          p!marcador [quantidade]          | Aumenta o diminui o marcador de determinado status de alguém da party ou da horda. | Inimigos ou Personagem |
|              p!cura [bônus]               | Escolhe um conjurador e a habilidade de cura e calcula a cura realizada. | Inimigos ou Personagem |
|     p!doenca [bônus] [nome da doença]     | Escolhe um conjurador de habilidade de doença para afetar um ou mais inimigos. | Inimigos ou Personagem |
|                p!interacao                | Define determinada interação elemental para alguém da party ou da horda. |          ---           |
