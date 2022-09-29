# PFP Stacker
# created by: Brad Myrick - CodeMucho.com 2021
# Create NFT and metadata from png image layers.
import PIL
from PIL import Image
import os
import random
import json



example_json = {
    "description": "Friendly OpenSea Creature that enjoys long swims in the ocean.",
    "external_url": "https://openseacreatures.io/3",
    "image": "https://storage.googleapis.com/opensea-prod.appspot.com/puffs/3.png",
    "name": "Dave Starbelly",
    "attributes": [
        {
            "trait_type": "Base",
            "value": "Starfish"
        },
        {
            "trait_type": "Eyes",
            "value": "Big"
        },
        {
            "trait_type": "Mouth",
            "value": "Surprised"
        },
        {
            "trait_type": "Level",
            "value": 5
        },
        {
            "trait_type": "Stamina",
            "value": 1.4
        },
        {
            "trait_type": "Personality",
            "value": "Sad"
        },
        {
            "display_type": "boost_number",
            "trait_type": "Aqua Power",
            "value": 40
        },
        {
            "display_type": "boost_percentage",
            "trait_type": "Stamina Increase",
            "value": 10
        },
        {
            "display_type": "number",
            "trait_type": "Generation",
            "value": 2
        }
    ]
}


def set_up_dicts(_mainfolder):
    num = 0
    layers = {}
    for folder in os.listdir(_mainfolder):
        traistforlayer = []
        traitdir = _mainfolder + '\\' + folder
        for files in os.listdir(traitdir):
            traistforlayer.append(traitdir + '\\' + files)
        layers.update({num: traistforlayer})
        num += 1
    return layers


def traitPicker(_layers):
    traits = {}
    x = 0
    for x in _layers:
        choice = random.choice(_layers[x])
        ## the trait name is the folder name
        trait = choice.split('\\')[-2]
        traits.update({trait: choice})
        x += 1
    return traits


def assemble(_traits, _id):
    # write traits to a json file named meta
    file = "finished" + '\\' + str(_id)+".png"
    im = PIL.Image.new('RGBA', (1000, 1000), (255, 255, 255, 0))
    for trait in _traits:
        # get a random image from the trait folder
        img = _traits[trait]
        image = Image.open(img)
        image.convert('RGBA')
        # add the image to the nft
        im.paste(image, (0, 0), image)
        # save the nft
        nft = {'ID': _id, 'File': file}
    metadataBuilder(_traits, _id, file)
    ##print(ipfsupload.ipfsUpload(file))
    im.save(file)
    return nft


def metadataBuilder(_traits, _id, _file):
    attributes = []
    for trait in _traits:
        trait_type = trait
        ## remove the path and file extension
        value = _traits[trait].split('\\')[-1].split('.')[0]
        attributes.append({'trait_type': trait_type, 'value': value})      
    
    meta = {'description': 'PFP Stacker', 'external_url': 'https://codemucho.com', 'image': _file, 'name': 'PFP Stacker', 'attributes': attributes}
    with open("meta"+'\\'+str(_id)+".json", "w") as outfile:
        json.dump(meta, outfile)
    


def main(_base):
    base = _base
    layers = set_up_dicts(base)
    print(layers)
    for i in range(10):
        traits = traitPicker(layers)
        print(assemble(traits, i))


if __name__ == '__main__':
    main('hoppers')

