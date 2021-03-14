const ipcRenderer = window.require('electron').ipcRenderer;

export async function executarBot() {
    const res = await ipcRenderer.sendSync('ligarBot');
    return res;
}
  