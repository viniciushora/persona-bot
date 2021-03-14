const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const reacao_elemental = await connection('reacao_elemental').select('*');
    
        return response.json(reacao_elemental);
    },

    async create(request, response) {
        const { fk_persona_persona_id, fraquezas } = request.body;

        var fk_elemento_elemento_id = 0;
        var fk_interacao_elemento_interacao_id = 0;

        for (var i=1; i <= fraquezas.length; i ++) {
            fk_elemento_elemento_id = i;
            fk_interacao_elemento_interacao_id = fraquezas[i-1];

            await connection('reacao_elemental').insert({
                fk_persona_persona_id,
                fk_elemento_elemento_id,
                fk_interacao_elemento_interacao_id
            })
        }

        return response.json({ fk_persona_persona_id });
    }
}