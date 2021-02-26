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

        const personagem_persona = await connection('personagem_persona')
        .select('personagem_persona_id')
        .where('fk_personagem_personagem_id', fk_personagem_personagem_id)
        .where('fk_persona_persona_id', fk_persona_persona_id)
        .whereNotNull("personagem_persona_id")
        .first();

        const result = personagem_persona.personagem_persona_id;

        return response.json({ result });
    }
}