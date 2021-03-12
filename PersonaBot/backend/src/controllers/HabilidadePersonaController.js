const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        
        const habilidade_persona = await connection('habilidade_persona')
        .select('fk_habilidade_habilidade_id')
        .select('nivel')
        .select('fk_persona_persona_id')
        .whereNotNull("fk_habilidade_habilidade_id");

        return response.json(habilidade_persona);
    },

    async create(request, response) {
        const { fk_persona_persona_id, niveis, habilidadesPersona } = request.body;
        var nivel = 0;
        var fk_habilidade_habilidade_id = 0;

        for (var i=0; i < niveis.length; i ++) {
            nivel = niveis[i];
            fk_habilidade_habilidade_id = habilidadesPersona[i];

            await connection('habilidade_persona').insert({
                nivel,
                fk_habilidade_habilidade_id,
                fk_persona_persona_id
            })
        }

        return response.json({ fk_persona_persona_id });
    }
}