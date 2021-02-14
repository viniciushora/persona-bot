const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const persona = await connection('persona').select('*');
    
        return response.json(persona);
    },

    async selectId (request, response) {
        const { nome } = request.body;

        const persona = await connection('persona')
        .select('persona_id')
        .where('nome', nome)
        .whereNotNull("persona_id")
        .first();

        const result = persona.persona_id;

        if (result == null) {
            return response.status(401).json({ error: 'Id não encontrado' });
        } else {
            return response.json({ result });
        }
    },

    async create(request, response) {
        const { nome, link_foto, nivel } = request.body;

        await connection('persona').insert({
            nome,
            link_foto,
            nivel
        })

        const persona = await connection('persona')
        .select('persona_id')
        .where('nome', nome)
        .whereNotNull("persona_id")
        .first();

        const result = persona.persona_id;

        console.log(result)

        return response.json({ result });
    }
}