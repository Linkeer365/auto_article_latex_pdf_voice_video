import comtypes.client

speak = comtypes.client.CreateObject("SAPI.SpVoice")
filestream = comtypes.client.CreateObject("SAPI.spFileStream")
filestream.open("ccbbdddc.mp3", 3, False)
speak.AudioOutputStream = filestream 
speak.Speak("独断万古荒天帝, 唯负罪州火桑女")
filestream.close()