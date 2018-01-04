DS4_CROSS_PIN = 1;


print('Setting up WIFI...')
wifi.setmode(wifi.STATION)
cfg={}
cfg.ssid="xxx"
cfg.pwd="xxx!"
wifi.sta.config(cfg)
wifi.sta.autoconnect(1)

tmr.alarm(1, 1000, tmr.ALARM_AUTO, function()
    if wifi.sta.getip() == nil then
        print('Waiting for IP ...')
    else
        print('IP is ' .. wifi.sta.getip())
    tmr.stop(1)

    local ws = websocket.createClient()
    ws:on("connection", function(ws)
      ws:send('It\'s me!')
      print('got ws connection')
    end)
    ws:on("receive", function(_, msg, opcode)
      print('got message:', msg, opcode) -- opcode is 1 for text message, 2 for binary
    end)
    ws:on("close", function(_, status)
      print('connection closed', status)
      ws = nil -- required to lua gc the websocket client
    end)
    
    ws:connect('ws://10.0.1.102:3000')


    end
end)


