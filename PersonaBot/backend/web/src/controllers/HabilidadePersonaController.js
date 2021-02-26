const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const { nivel, fk_persona_persona_id } = request.body;
        
        const habilidade_persona = await connection('habilidade_persona')
        .select('fk_habilidade_habilidade_id')
        .where('nivel', nivel)
        .where('fk_persona_persona_id', fk_persona_persona_id)
        .whereNotNull("fk_habilidade_habilidade_id");

        console.log(habilidade_persona)

        var habilidades = [];
        for (var i = 0; i < habilidade_persona.length; i ++) {
            habilidades.push(habilidade_persona[i]["fk_habilidade_habilidade_id"])
        }

        console.log(habilidades)

        return response.json({ habilidades });
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