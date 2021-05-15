const express = require('express')

const PersonaController = require('./controllers/PersonaController')
const ShadowController = require('./controllers/ShadowController')
const ItemController = require('./controllers/ItemController')
const PersonagemController = require('./controllers/PersonagemController')
const PersonagemPersonaController = require('./controllers/PersonagemPersonaController')
const DropController = require('./controllers/DropController')
const HabilidadeController = require('./controllers/HabilidadeController')
const HabilidadePersonaController = require('./controllers/HabilidadePersonaController')
const ReacaoElementalController = require('./controllers/ReacaoElementalController')
const PersonaAtributoController = require('./controllers/PersonaAtributoController')
const PersonaHabilidadeController = require('./controllers/PersonaHabilidadeController')
const ConfigController = require('./controllers/ConfigController')
const CrescimentoPersonagemController = require('./controllers/CrescimentoPersonagemController')
const BotController = require('./controllers/BotController')

const routes = express.Router()

routes.get('/bot', BotController.ligar);

routes.get('/persona', PersonaController.index)

routes.post('/crescimento_atributo', CrescimentoPersonagemController.create)

routes.get('/persona-ultimo-id', PersonaController.ultimoId)

routes.post('/persona-nivel', PersonaController.selectNivel)

routes.get('/config', ConfigController.index)

routes.post('/config/prefix', ConfigController.editPrefix)

routes.post('/config/token', ConfigController.editToken)

routes.post('/persona', PersonaController.create)

routes.post('/persona-info', PersonaController.select)

routes.get('/shadow', ShadowController.index)

routes.post('/shadow', ShadowController.create)

routes.get('/shadow-ultimo-id', ShadowController.ultimoId)

routes.get('/item', ItemController.index)

routes.post('/item', ItemController.create)

routes.get('/personagem', PersonagemController.index)

routes.post('/personagem-id', PersonagemController.personagemId)

routes.get('/personagem-ultimo-id', PersonagemController.ultimoId)

routes.post('/personagem', PersonagemController.create)

routes.get('/personagem_persona', PersonagemPersonaController.index)

routes.get('/personagem_persona-ultimo-id', PersonagemPersonaController.ultimoId)

routes.post('/personagem_persona', PersonagemPersonaController.create)

routes.get('/drop', DropController.index)

routes.post('/drop', DropController.create)

routes.get('/habilidade', HabilidadeController.index)

routes.post('/habilidade', HabilidadeController.create)

routes.get('/skills', HabilidadePersonaController.index)

routes.post('/habilidade_persona', HabilidadePersonaController.create)

routes.get('/reacao_elemental', ReacaoElementalController.index)

routes.post('/reacao_elemental', ReacaoElementalController.create)

routes.get('/persona_atributo', PersonaAtributoController.index)

routes.post('/persona_atributo', PersonaAtributoController.create)

routes.get('/persona_habilidade', PersonaHabilidadeController.index)

routes.post('/persona_habilidade', PersonaHabilidadeController.create)

module.exports = routes
