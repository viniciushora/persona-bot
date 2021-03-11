const connection = require('../database/connection');
var fs = require('fs');

module.exports = {
    async write(request, response) {
        const { obj } = request.body;

        var json2 = JSON.stringify(obj);
        fs.writeFile('../../../frontend/src/bot/config.json', json2, 'utf8');

        return response.json({ obj });
    }
}