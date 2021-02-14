const express = require('express');

const PersonaController = require('./controllers/PersonaController');
const PersonaArcanaController = require('./controllers/PersonaArcanaController');
const ShadowController = require('./controllers/ShadowController');
const ItemController = require('./controllers/ItemController');
const PersonagemController = require('./controllers/PersonagemController');
const PersonagemPersonaController = require('./controllers/PersonagemPersonaController');
const DropController = require('./controllers/DropController');
const HabilidadeController = require('./controllers/HabilidadeController');
const HabilidadePersonaController = require('./controllers/HabilidadePersonaController');
const ReacaoElementalController = require('./controllers/ReacaoElementalController');
const PersonaAtributoController = require('./controllers/PersonaAtributoController');

const routes = express.Router();

routes.get('/persona', PersonaController.index);

routes.get('/persona-id', PersonaController.selectId);

routes.post('/persona', PersonaController.create);

routes.get('/shadow', ShadowController.index);

routes.post('/shadow', ShadowController.create);

routes.get('/item', ItemController.index);

routes.post('/item', ItemController.create);

routes.get('/personagem', PersonagemController.index);

routes.post('/personagem', PersonagemController.create);

routes.get('/personagem_persona', PersonagemPersonaController.index);

routes.post('/personagem_persona', PersonagemPersonaController.create);

routes.get('/drop', DropController.index);

routes.post('/drop', DropController.create);

routes.get('/persona_arcana', PersonaArcanaController.index);

routes.post('/persona_arcana', PersonaArcanaController.create);

routes.get('/habilidade', HabilidadeController.index);

routes.post('/habilidade', HabilidadeController.create);

routes.get('/habilidade_persona', HabilidadePersonaController.index);

routes.post('/habilidade_persona', HabilidadePersonaController.create);

routes.get('/reacao_elemental', ReacaoElementalController.index);

routes.post('/reacao_elemental', ReacaoElementalController.create);

routes.get('/persona_atributo', PersonaAtributoController.index);

routes.post('/persona_atributo', PersonaAtributoController.create);

module.exports = routes;