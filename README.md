# BG3-custom-item-builder
Python script for quicker custom armor and weapon creation for Baldur's Gate 3.

Nexus link: https://www.nexusmods.com/baldursgate3/mods/2791

## What does it do?

Pulls user defined data from a txt file. Appends new entries to Merged.lsx, <localization>.xml, Weapon.txt and/or Armor.txt using this data. Automatically generates UUIDs and handles where necessary.

## How to use

The script assumes that you have already set up the correct file structure for mod creation. It WILL either complain at you or just plain shut down if it can't find something. Check for typos if that happens.

Step 1: set up correct file structure

Step 2: place the script and any accompanying files next to your mod folder

Step 3: fill in desired values in weapon_values.txt and/or armor_values.txt

Step 4: run script

Step 5: drink water and stretch

## What it DOESN'T do

It won't fill in armor/weapon stats. I left these empty so you can easily customize them in their respective txt file.
However, you can open up the script in your preferred editor and fill in more default values if you want. These will then be used for every new item you create.

It also won't fill in armor visuals in Merged.lsx. There are too many possible variations here, and it would have taken away from the aim of this tool: simplicity.

You will still need to convert the resulting files into the right format (xml -> loca, lsx -> lsf) and finally package the mod.

## How to fill in weapon_values.txt / armor_values.txt

The included files already contain examples. You can create multiple items at once by adding values for multiple items under each other.


FOR WEAPONS:

The script will pull the necessary values from weapon_values.txt
The file needs to adhere to the following format:

Display name:
[name that will be displayed in-game]
Description:
[description that will be shown in-game]
Internal name tag:
[internal name tag (chosen by you, used to reference the item in other files)]
Icon tag:
[icon tag]
Parent template UUID:
[uuid]
Equipment type UUID:
[uuid]
Physics template UUID:
[uuid]
Visual template UUID:
[uuid]

Example:

Display name:
Example weapon
Description:
This is indeed an example weapon.
Internal name tag:
GAB_example_weapon_01
Icon tag:
Item_WPN_HUM_HandCrossbow_A_1
Parent template UUID:
d2f396c2-9b1b-4eea-bf21-2f25934f092d
Equipment type UUID:
87fbc05b-c870-4bc1-fb95-ea56cb3f229e
Physics template UUID:
b34614de-6a17-d61b-6716-f47324aa1dff
Visual template UUID:
79e935b4-9dca-7fdc-bc55-ba7e846909f9
Display name:
Example weapon 2
Description:
This is the next example weapon. See how there is no blank line between the two?
....


FOR ARMOR:

The script will pull the necessary values from armor_values.txt
The file needs to adhere to the following format:

Display name:
[name that will be displayed in-game]
Description:
[description that will be shown in-game]
Internal name tag:
[internal name tag (chosen by you, used to reference the item in other files)]
Icon tag:
[icon tag]
Parent template UUID:
[uuid]

Example:

Display name:
Example armor 1
Description:
This is the first example armor.
Internal name tag:
GAB_example_armor_01
Icon tag:
Item_ARM_Leather_3
Parent template UUID:
0985f767-4256-4f15-aabe-364e002f913f
Display name:
Example armor 2
Description:
This is the next example armor. See how there is no blank line between the two?
....

## Permissions

Feel free to modify it however you like and share your modifications publicly. Just make sure that any tools you make based on my code remain free. Also, credit would be appreciated.
