const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const drop = await connection('drop').select('*');
    
        return response.json(drop);
    },

    async create(request, response) {
        const { fk_shadow_fk_persona_persona_id, fk_item_item_id, chance } = request.body;

        await connection('drop').insert({
            fk_shadow_fk_persona_persona_id,
            fk_item_item_id,
            chance
        })

        return response.json({ fk_shadow_fk_persona_persona_id });
    }
}