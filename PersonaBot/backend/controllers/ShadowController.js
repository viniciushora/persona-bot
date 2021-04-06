const connection = require('../database/connection')

module.exports = {
  async ultimoId (request, response) {
    try {
      const shadow = await connection('shadow')
        .select('shadow_id')
        .whereNotNull('shadow_id')
        .orderBy('shadow_id', 'desc')
        .first()

      const result = persona.persona_id

      return response.json(result)
    } catch {
      const result = 0

      return response.json(result)
    }
  },

  async index (request, response) {
    const shadow = await connection('shadow').select('*')

    return response.json(shadow)
  },

  async create(request, response) {
    const { codinome, fk_persona_persona_id, exp, dinheiro } = request.body

    await connection('shadow').insert({
      codinome,
      fk_persona_persona_id,
      exp,
      dinheiro
    })

    return response.json({ fk_persona_persona_id })
  }
}
