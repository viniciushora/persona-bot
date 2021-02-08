const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const personagem = await connection('personagem').select('*');
    
        return response.json(personagem);
    },

    async create(request, response) {
        const { nome, fk_grupo_grupo_id, usuario, fool, persona_equipada, foto } = request.body;

        console.log(data);

        await connection('personagem').insert({
            nome,
            fk_grupo_grupo_id,
            usuario, fool,
            persona_equipada,
            foto
        })

        return response.json({ nome });
    }
}