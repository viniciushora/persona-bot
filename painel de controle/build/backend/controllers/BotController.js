const exec = require('child_process').exec;

module.exports = {
  async ligar (request, response) {
    console.log("Foi")
    exec("cd bot && bot.exe", function(err, data) {  
      console.log(err)
      console.log(data.toString());                       
    });  
  }
}
