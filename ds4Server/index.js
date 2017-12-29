
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var port = 3000;

app.get('/', function (req, res)
{
  res.send('Hello World!');
});

io.on('connection', function (socket)
{
  console.log('connection');
  socket.on('chat message', function (msg)
  {
    console.log('msg');
    io.emit('chat message', msg);
  });
});

http.listen(port, function ()
{
  console.log('listening on *:' + port);
});
