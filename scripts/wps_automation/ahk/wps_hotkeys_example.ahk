; WPS 自动化（AutoHotkey 示例）
; 作用：打开 WPS 并执行简单操作

#NoEnv
SendMode Input

^!w::  ; Ctrl + Alt + W
Run, wps.exe
WinWait, ahk_exe wps.exe
WinActivate

Sleep, 2000
Send, ^n   ; 新建文档
Sleep, 1000
Send, Hello WPS Automation!

return
