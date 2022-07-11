import datetime
import hashlib

import requests

def hashedKey(timestamp, privateKey, publicKey):
    hash = hashlib.md5()
    hash.update(f'{timestamp}{privateKey}{publicKey}'.encode('utf-8'))
    hashed = hash.hexdigest()
    return hashed

def getStartsWithParams(character):
    character = character[12:]
    character.replace(" ", "%20")
    parameters = parametersToSend()
    parameters.update({'nameStartsWith': character})
    return parameters

def parametersToSend():
    publicKey = 'f319913152082ad795fb32cc1ed888ca'
    privateKey = '2c9ec9167ba293623b5771a3423d772301576772'
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    hashed = hashedKey(timestamp, privateKey, publicKey)
    return {'ts': timestamp, 'apikey': publicKey, 'hash': hashed}

def getCharacterParams(character):
    if "starts with" in character:
        return getStartsWithParams(character)
    else:
        parameters = parametersToSend()
        parameters.update({'name': character})
        return parameters

def getComicDescription(id):
    parameters = parametersToSend()
    parameters.update({'characters': id})
    r = requests.get('https://gateway.marvel.com:443/v1/public/comics?', params=parameters)
    r = r.json().get("data").get("results")
    listOfComics = []
    for comic in r:
        result = {'title': comic.get("title"), 'description': comic.get("description")}
        listOfComics.append(result)
    return listOfComics

def getCharacterInfo(character):
    character = input("Enter the name of a Marvel character: ")
    parameters = getCharacterParams(character)
    r = requests.get('https://gateway.marvel.com/v1/public/characters?', params=parameters)
    if r.json().get("data").get("results") == []:
        return None
    r = r.json().get("data").get("results")
    listOfCharacters = []
    for character in r:
        result = {'id': character.get("id"), 'name': character.get("name"), 'description': character.get("description")}
        result.update({'comics': getComicDescription(character.get("id"))})
        listOfCharacters.append(result)
    return listOfCharacters

#print(getCharacterInfo())
#print(getComicDescription(1009644))