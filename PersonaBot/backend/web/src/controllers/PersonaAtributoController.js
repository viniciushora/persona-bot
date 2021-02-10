const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const persona_atributo = await connection('persona_atributo').select('*');
    
        return response.json(persona_atributo);
    },

    async create(request, response) {
        const { valor, fk_atributo_atributo_id, fk_persona_persona_id } = request.body;

        await connection('reacao_elemental').insert({
            valor,
            fk_atributo_atributo_id,
            fk_persona_persona_id
        })

        return response.json({ fk_persona_persona_id });
    }
}