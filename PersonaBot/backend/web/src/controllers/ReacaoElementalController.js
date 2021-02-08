const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const reacao_elemental = await connection('reacao_elemental').select('*');
    
        return response.json(reacao_elemental);
    },

    async create(request, response) {
        const { fk_persona_persona_id, fk_elemento_elemento_id, fk_interacao_elemento_interacao_id } = request.body;

        console.log(data);

        await connection('reacao_elemental').insert({
            fk_persona_persona_id,
            fk_elemento_elemento_id,
            fk_interacao_elemento_interacao_id
        })

        return response.json({ fk_persona_persona_id });
    }
}