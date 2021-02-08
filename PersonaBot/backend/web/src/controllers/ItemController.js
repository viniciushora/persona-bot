const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const item = await connection('item').select('*');
    
        return response.json(item);
    },

    async create(request, response) {
        const { item_id, nome, fk_tipo_item_tipo_id, valor } = request.body;

        console.log(data);

        await connection('item').insert({
            item_id,
            nome,
            fk_tipo_item_tipo_id,
            valor
        })

        return response.json({ nome });
    }
}