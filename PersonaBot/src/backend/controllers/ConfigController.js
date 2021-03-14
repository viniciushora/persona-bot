const connection = require('../database/connection');

module.exports = {
    async index (request, response) {
        const config = await connection('config').select('*');
    
        return response.json(config);
    },

    async editPrefix(request, response) {
        const { prefix } = request.body;
       
        await connection('config')
        .whereNotNull('prefix')
        .update('prefix', prefix)
        .then(data => data);
          
        return response.json(prefix);
    },

    async editToken(request, response) {
        const { token } = request.body;
       
        await connection('config')
        .whereNotNull('token')
        .update('token', token)
        .then(data => data);

        return response.json(token);
    }
}