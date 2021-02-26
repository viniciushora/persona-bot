const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const personagem = await connection('personagem').select('*');
    
        return response.json(personagem);
    },

    async create(request, response) {
        const { nome, fk_grupo_grupo_id, usuario, fool, persona_equipada, foto } = request.body;

        await connection('personagem').insert({
            nome,
            fk_grupo_grupo_id,
            usuario, fool,
            persona_equipada,
            foto
        })

        const personagem = await connection('personagem')
        .select('personagem_id')
        .where('nome', nome)
        .whereNotNull("personagem_id")
        .first();

        const result = personagem.personagem_id;

        return response.json({ result });
    }
}