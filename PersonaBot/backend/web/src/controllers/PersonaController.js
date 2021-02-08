const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const persona = await connection('persona').select('*');
    
        return response.json(persona);
    },

    async create(request, response) {
        const { nome, link_foto, nivel } = request.body;

        console.log(data);

        await connection('persona').insert({
            nome,
            link_foto,
            nivel
        })

        return response.json({ nome });
    }
}