const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const persona_atributo = await connection('persona_atributo').select('*');
    
        return response.json(persona_atributo);
    },

    async create(request, response) {
        const { fk_persona_persona_id, atributos } = request.body;

        var valor = 0;
        var fk_atributo_atributo_id = 0;

        for (var i=1; i <= atributos.length; i ++) {
            valor = i;
            fk_atributo_atributo_id = atributos[i-1];

            await connection('persona_atributo').insert({
                valor,
                fk_atributo_atributo_id,
                fk_persona_persona_id
            })
        }

        return response.json({ fk_persona_persona_id });
    }
}