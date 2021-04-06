const { ipcRenderer } = require('electron')

module.exports = {
  async ligar (request, response) {
    const res = await ipcRenderer.sendSync('ligarBot')
    return res
  }
}
