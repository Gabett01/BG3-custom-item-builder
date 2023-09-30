# BG3-custom-item-builder
Python script for quicker custom armor and weapon creation for Baldur's Gate 3.

##What does it do?

Pulls user defined data from a txt file. Appends new entries to Merged.lsx, <localization>.xml, Weapon.txt and/or Armor.txt using this data. Automatically generates UUIDs and handles where necessary.

##How to use

The script assumes that you have already set up the collect file structure for mod creation. It WILL either complain at you or just plain shut down if it can't find something. Check for typos if that happens.

Step 1: set up correct file structure
Step 2: place the script and any accompanying files next to your mod folder
Step 3: fill in desired values in weapon_values.txt and/or armor_values.txt
Step 4: run script
Step 5: drink water and stretch

##What it DOESN'T do

It won't fill in armor/weapon stats. I left these empty so you can easily customize them in their respective txt file.
However, you can open up the script in your preferred editor and fill in more default values if you want. These will then be used for every new item you create.

It also won't fill in armor visuals in Merged.lsx. There are too many possible variations here, and it would have taken away from the aim of this mod: simplicity.

You will still need to convert the resulting files into the right format (xml -> loca, lsx -> lsf) and finally package the mod.

##Permissions

Feel free to modify it however you like and share your modifications publicly. Just make sure that any tools you make based on my code remain free. Also, credit would be appreciated.
