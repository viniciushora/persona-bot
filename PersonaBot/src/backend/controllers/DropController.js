const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const drop = await connection('drop').select('*');
    
        return response.json(drop);
    },

    async create(request, response) {
        const { fk_shadow_shadow_id, chances, dropItens } = request.body;
        
        var chance = 0;
        var fk_item_item_id = 0;

        for (var i=0; i < chances.length; i ++) {
            chance = chances[i];
            fk_item_item_id = dropItens[i];

            await connection('drop').insert({
                fk_shadow_shadow_id,
                fk_item_item_id,
                chance
            })
        }

        return response.json({ fk_shadow_shadow_id });
    }
}