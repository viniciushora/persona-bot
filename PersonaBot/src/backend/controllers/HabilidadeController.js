const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const habilidade = await connection('habilidade').select('*');
    
        return response.json(habilidade);
    },

    async create(request, response) {
        const { nome, fk_atributo_atributo_id, fk_intensidade_intensidade_id, fk_elemento_elemento_id, vezes } = request.body;

        await connection('habilidade').insert({
            nome,
            fk_atributo_atributo_id,
            fk_intensidade_intensidade_id,
            fk_elemento_elemento_id,
            vezes
        })

        return response.json({ nome });
    }
}