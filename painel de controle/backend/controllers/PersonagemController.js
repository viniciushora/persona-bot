const connection = require('../database/connection')

module.exports = {
  async index (request, response) {
    const personagem = await connection('personagem').select('*')

    return response.json(personagem)
  },

  async personagemId (request, response) {
    const { nome } = request.body

    const personagem = await connection('personagem')
      .select('personagem_id')
      .where('nome', nome)
      .whereNotNull('personagem_id')
      .first()

    const result = personagem.personagem_id

    return response.json(result)
  },

  async ultimoId (request, response) {
    try {
      const personagem = await connection('personagem')
        .select('personagem_id')
        .whereNotNull('personagem_id')
        .orderBy('personagem_id', 'desc')
        .first()

      const result = personagem.personagem_id

      return response.json(result)
    } catch {
      const result = 0

      return response.json(result)
    }
  },

  async create(request, response) {
    const { nome, usuario, fool, persona_equipada, foto } = request.body

    await connection('personagem').insert({
      nome,
      usuario,
      fool,
      persona_equipada,
      foto
    })

    return response.json(nome)
  }
}
