# dualshock4-remap

> 实现一个可远程控制的 dualshock4 手柄

## libPkg

[dualshock4](http://www.psdevwiki.com/ps4/DualShock_4) 按键薄膜引脚 pcb 元件库

## remapPcb

3cm * 5cm 改键 fpc 图

## ds4Client

基于 [nodemcu](https://nodemcu-build.com/) 的客户端, 包含9个模块: file, gpio, node, pwm, sjson, tmr, uart, websocket, wifi.

## ds4Server

基于 node.js 的服务器