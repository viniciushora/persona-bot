const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const shadow = await connection('shadow').select('*');
    
        return response.json(shadow);
    },

    async create(request, response) {
        const { codinome, fk_persona_persona_id, exp, dinheiro } = request.body;

        await connection('shadow').insert({
            codinome,
            fk_persona_persona_id,
            exp,
            dinheiro
        })

        return response.json({ codinome });
    }
}