const connection = require('../database/connection')

module.exports = {
  async create(request, response) {
    const { fk_personagem_personagem_id } = request.body
    var quant = 0
    var fk_atributo_atributo_id = 0
    var tipo_crescimento = 0
    var i = 1

    for (i = 1; i < 8; i++) {
      fk_atributo_atributo_id = i
      tipo_crescimento = 1

      await connection('crescimento_personagem').insert({
        quant,
        fk_atributo_atributo_id,
        fk_personagem_personagem_id,
        tipo_crescimento
      })
    }
    for (i = 1; i < 8; i++) {
      fk_atributo_atributo_id = i
      tipo_crescimento = 2

      await connection('crescimento_personagem').insert({
        quant,
        fk_atributo_atributo_id,
        fk_personagem_personagem_id,
        tipo_crescimento
      })
    }

    return response.json(fk_personagem_personagem_id)
  }
}
