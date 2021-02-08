const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const habilidade_persona = await connection('habilidade_persona').select('*');
    
        return response.json(habilidade_persona);
    },

    async create(request, response) {
        const { nivel, fk_habilidade_habilidade_id, fk_persona_persona_id } = request.body;

        console.log(data);

        await connection('habilidade_persona').insert({
            nivel,
            fk_habilidade_habilidade_id,
            fk_persona_persona_id
        })

        return response.json({ fk_persona_persona_id });
    }
}