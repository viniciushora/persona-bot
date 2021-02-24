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

        const shadow = await connection('shadow')
        .select('shadow_id')
        .where('codinome', codinome)
        .whereNotNull("shadow_id")
        .first();

        const result = shadow.shadow_id;

        if (result == null) {
            return response.status(401).json({ error: 'Id não encontrado' });
        } else {
            return response.json({ result });
        }

        return response.json({ codinome });
    }
}