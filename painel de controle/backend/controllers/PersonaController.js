const connection = require('../database/connection')

module.exports = {
  async index (request, response) {
    const persona = await connection('persona').select('*')

    return response.json(persona)
  },

  async selectNivel (request, response) {
    const { fk_persona_persona_id } = request.body

    console.log(fk_persona_persona_id)

    const persona = await connection('persona')
      .select('nivel')
      .where('persona_id', fk_persona_persona_id)
      .first()

    const result = persona.nivel

    if (result == null) {
      return response.status(401).json({ error: 'Id não encontrado' })
    } else {
      return response.json(result)
    }
  },

  async ultimoId (request, response) {
    try {
      const persona = await connection('persona')
        .select('persona_id')
        .whereNotNull('persona_id')
        .orderBy('persona_id', 'desc')
        .first()

      const result = persona.persona_id

      return response.json(result)
    } catch {
      const result = 0

      return response.json(result)
    }
  },

  async select(request, response) {
    const { persona_id } = request.body

    const persona = await connection('persona')
      .select('*')
      .where('persona_id', persona_id)

    return response.json(persona)
  },

  async create(request, response) {
    const { nome, link_foto, nivel, fk_arcana_arcana_id } = request.body

    await connection('persona').insert({
      nome,
      link_foto,
      nivel,
      fk_arcana_arcana_id
    })

    return response.json(nome)
  }
}
