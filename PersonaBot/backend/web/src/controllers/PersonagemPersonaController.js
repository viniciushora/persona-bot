const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const personagem_persona = await connection('personagem_persona').select('*');
    
        return response.json(personagem_persona);
    },

    async create(request, response) {
        const { nivel, fk_personagem_personagem_id, fk_persona_persona_id, compendium } = request.body;

        await connection('personagem_persona').insert({
            nivel,
            fk_personagem_personagem_id,
            fk_persona_persona_id,
            compendium
        })

        return response.json({ fk_personagem_personagem_id });
    }
}