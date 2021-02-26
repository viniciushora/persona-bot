const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const persona_habilidade = await connection('persona_habilidade').select('*');
    
        return response.json(persona_habilidade);
    },

    async create(request, response) {
        const { fk_personagem_persona_personagem_persona_id, habilidades } = request.body;

        var fk_habilidade_habilidade_id = 0;

        for (var i=0; i < habilidades.length; i ++) {
            fk_habilidade_habilidade_id = habilidades[i];

            await connection('persona_habilidade').insert({
                fk_habilidade_habilidade_id,
                fk_personagem_persona_personagem_persona_id
            })
        }

        return response.json({ fk_personagem_persona_personagem_persona_id });

    }
}