const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const persona_arcana = await connection('persona_arcana').select('*');
    
        return response.json(persona_arcana);
    },

    async create(request, response) {
        const { fk_persona_persona_id, fk_arcana_arcana_id } = request.body;

        console.log(data);

        await connection('persona_arcana').insert({
            fk_persona_persona_id,
            fk_arcana_arcana_id
        })

        return response.json({ fk_persona_persona_id });
    }
}