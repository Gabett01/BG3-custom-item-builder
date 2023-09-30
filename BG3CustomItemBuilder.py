import xml.etree.ElementTree as ET
from uuid import uuid4
from pathlib import Path

"""
!!! If you don't know where these values come from, refer to the tutorials linked on the mod page. !!!

============
FOR WEAPONS:
============
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

==========
FOR ARMOR:
==========
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

"""


def pull_values(file: str):
    """Pull values from file and return them as a list of dictionaries."""
    with open(file, 'r', encoding='UTF-8') as f:
        values = f.readlines()

    if file == 'weapon_values.txt' and len(values) % 16 == 0:
        n = 16
    elif file == 'armor_values.txt' and len(values) % 10 == 0:
        n = 10
    else:
        print(f"Error: Incorrect number of lines in {file}!")
        return

    values = [value.strip() for value in values]
    value_dictionaries = []
    lists = [values[i * n:(i + 1) * n] for i in range((len(values) + n - 1) // n)]
    for list in lists:
        it = iter(list)
        value_dictionary = dict(zip(it, it))
        value_dictionaries.append(value_dictionary)

    return value_dictionaries


class GenerateItem:
    def __init__(self, value_dicts: list[dict], folder_name: str):
        self.value_dicts = value_dicts
        self.mod_folder_path = f"{str(Path(__file__).parent)}/{folder_name}"
        self.merged_lsx_path = f"{self.mod_folder_path}/Public/{folder_name}/RootTemplates/Merged.lsx"
        self.merged_lsx = ET.parse(self.merged_lsx_path)
        self.data_folder_path = f"{self.mod_folder_path}/Public/{folder_name}/Stats/Generated/Data"
        self.localization_xml_path = f"{self.mod_folder_path}/Localization/English/{folder_name}.xml"
        # This is the parent all the localization elements will be appended to
        self.localization_root = self.get_root(self.localization_xml_path)

    def get_root(self, file):
        """Parse xml structure and return root."""
        parsed = ET.parse(file)
        root = parsed.getroot()
        return root

    def update_localization(self, name, name_handle, desc, desc_handle):
        """Append ElementTree Element objects to the localization root."""
        display_name = ET.fromstring(f'<content contentuid="{name_handle}" version="1">{name}</content>')
        description = ET.fromstring(f'<content contentuid="{desc_handle}" version="1">{desc}</content>')
        self.localization_root.append(display_name)
        self.localization_root.append(description)

    def write_localization_xml(self):
        """Create and format ElementTree object and write it to the localization xml."""
        tree = ET.ElementTree(self.localization_root)
        ET.indent(tree, ' ')
        tree.write(self.localization_xml_path, encoding="utf-8", xml_declaration=True)
        print("Localization xml updated successfully.")

    def write_merged_lsx(self):
        """Write ElementTree object to Merged.lsx."""
        self.merged_lsx.write(self.merged_lsx_path, encoding="utf-8", xml_declaration=True)
        print('Merged.lsx updated successfully.')


class GenerateWeapon(GenerateItem):
    def __init__(self, value_dicts: list[dict], folder_name: str):
        super().__init__(value_dicts, folder_name)
        # one game object represents one item
        # each game object will be appended to this parent as a child element
        self.game_object_parent = self.merged_lsx.getroot().find('.//children')
        # and this is where we store the stat templates until it's time to write them to the file
        self.stat_templates = []

        for value_dict in value_dicts:
            # create all attributes for one item
            self.display_name_handle = 'h' + str(uuid4()).replace('-', 'g')
            self.description_handle = 'h' + str(uuid4()).replace('-', 'g')
            self.map_key_uuid = str(uuid4())
            self.display_name = value_dict['Display name:']
            self.description = value_dict['Description:']
            self.internal_name_tag = value_dict['Internal name tag:']
            self.icon_tag = value_dict['Icon tag:']
            self.parent_template_uuid = value_dict['Parent template UUID:']
            self.equipment_type_uuid = value_dict['Equipment type UUID:']
            self.physics_template_uuid = value_dict['Physics template UUID:']
            self.visual_template_uuid = value_dict['Visual template UUID:']

            # fill in template and append to parent
            self.update_weapon_attributes()
            self.update_weapon_stats()
            self.update_localization(self.display_name, self.display_name_handle, self.description,
                                     self.description_handle)

        # once every new item is appended, write to the files
        self.write_merged_lsx()
        self.write_localization_xml()
        self.write_weapon_txt()

    def update_weapon_attributes(self):
        """Modify item attributes and append game object to the parent element."""

        template_root = self.get_root('WeaponTemplate.lsx')
        game_object = template_root.find('.//node[@id="GameObjects"]')

        comment = ET.Comment(self.display_name)
        comment.tail = "\n\t\t\t\t\t"
        game_object.insert(0, comment)

        description_handle = game_object.find('.//attribute[@id="Description"]')
        description_handle.set('handle', self.description_handle)
        display_name_handle = game_object.find('.//attribute[@id="DisplayName"]')
        display_name_handle.set('handle', self.display_name_handle)
        map_key = game_object.find('.//attribute[@id="MapKey"]')
        map_key.set('value', self.map_key_uuid)
        name = game_object.find('.//attribute[@id="Name"]')
        name.set('value', self.internal_name_tag)
        stats = game_object.find('.//attribute[@id="Stats"]')
        stats.set('value', self.internal_name_tag)
        icon = game_object.find('.//attribute[@id="Icon"]')
        icon.set('value', self.icon_tag)
        parent_template = game_object.find('.//attribute[@id="ParentTemplateId"]')
        parent_template.set('value', self.parent_template_uuid)
        # weapon specific values
        equipment_type = game_object.find('.//attribute[@id="EquipmentTypeID"]')
        equipment_type.set('value', self.equipment_type_uuid)
        physics_template = game_object.find('.//attribute[@id="PhysicsTemplate"]')
        physics_template.set('value', self.physics_template_uuid)
        visual_template = game_object.find('.//attribute[@id="VisualTemplate"]')
        visual_template.set('value', self.visual_template_uuid)

        self.game_object_parent.append(game_object)

    def update_weapon_stats(self):
        """Write weapon stat template and store it in a list."""

        # you can modify this template if you for example want all weapons to have the same rarity
        template = f'''\
new entry "{self.internal_name_tag}"
type "Weapon"  
using ""
data "RootTemplate" "{self.map_key_uuid}"
data "Damage Type" ""
data "Damage" ""
data "ValueOverride" ""
data "Weight" ""
data "Rarity" ""
data "Weapon Properties" ""
data "DefaultBoosts" ""
data "BoostsOnEquipMainHand" ""
data "BoostsOnEquipOffHand" ""
data "PassivesOnEquip" ""
data "Boosts" ""


'''
        self.stat_templates.append(template)

    def write_weapon_txt(self):
        """Convert list of templates to str, write them to Weapon.txt."""
        templates = "".join(self.stat_templates)
        with open(self.data_folder_path + '/Weapon.txt', 'a', encoding='utf-8') as f:
            f.write(templates)
        print('Weapon.txt updated successfully.')


class GenerateArmor(GenerateItem):
    def __init__(self, value_dicts: list[dict], folder_name: str):
        super().__init__(value_dicts, folder_name)
        # one game object represents one item
        # each game object will be appended to this parent as a child element
        self.game_object_parent = self.merged_lsx.getroot().find('.//children')
        # and this is where we store the stat templates until it's time to write them to the file
        self.stat_templates = []

        for value_dict in value_dicts:
            # create all attributes for one item
            self.display_name_handle = 'h' + str(uuid4()).replace('-', 'g')
            self.description_handle = 'h' + str(uuid4()).replace('-', 'g')
            self.map_key_uuid = str(uuid4())
            self.display_name = value_dict['Display name:']
            self.description = value_dict['Description:']
            self.internal_name_tag = value_dict['Internal name tag:']
            self.icon_tag = value_dict['Icon tag:']
            self.parent_template_uuid = value_dict['Parent template UUID:']

            # fill in template and append to parent
            self.update_armor_attributes()
            self.update_armor_stats()
            self.update_localization(self.display_name, self.display_name_handle, self.description,
                                     self.description_handle)

        # once every new item is appended, write to the files
        self.write_merged_lsx()
        self.write_localization_xml()
        self.write_armor_txt()

    def update_armor_attributes(self):
        """Modify item attributes and append game object to the parent element."""

        template_root = self.get_root('ArmorTemplate.lsx')
        game_object = template_root.find('.//node[@id="GameObjects"]')

        comment = ET.Comment(self.display_name)
        comment.tail = "\n\t\t\t\t\t"
        game_object.insert(0, comment)

        description_handle = game_object.find('.//attribute[@id="Description"]')
        description_handle.set('handle', self.description_handle)
        display_name_handle = game_object.find('.//attribute[@id="DisplayName"]')
        display_name_handle.set('handle', self.display_name_handle)
        map_key = game_object.find('.//attribute[@id="MapKey"]')
        map_key.set('value', self.map_key_uuid)
        name = game_object.find('.//attribute[@id="Name"]')
        name.set('value', self.internal_name_tag)
        stats = game_object.find('.//attribute[@id="Stats"]')
        stats.set('value', self.internal_name_tag)
        icon = game_object.find('.//attribute[@id="Icon"]')
        icon.set('value', self.icon_tag)
        parent_template = game_object.find('.//attribute[@id="ParentTemplateId"]')
        parent_template.set('value', self.parent_template_uuid)

        self.game_object_parent.append(game_object)

    def update_armor_stats(self):
        """Write armor stat template and store it in a list."""

        # you can modify this template if you for example want all armors to have the same rarity
        template = f'''\
new entry "{self.internal_name_tag}"
type "Armor"
using ""
data "RootTemplate" "{self.map_key_uuid}"
data "ArmorClass" ""
data "Armor Class Ability" "Dexterity"
data "ValueOverride" ""
data "Weight" ""
data "Rarity" ""
data "Ability Modifier Cap" ""
data "Proficiency Group" ""
data "PassivesOnEquip" ""
data "Boosts" ""

'''
        self.stat_templates.append(template)

    def write_armor_txt(self):
        """Convert list of templates to str, write them to Armor.txt."""
        templates = "".join(self.stat_templates)
        with open(self.data_folder_path + '/Armor.txt', 'a', encoding='utf-8') as f:
            f.write(templates)
        print('Armor.txt updated successfully.')


def driver():
    print("To exit the program, type 'q'.")
    while True:
        mod_name = input("Please input the name of your working folder: ")
        if mod_name.lower() == 'q':
            return
        elif not Path(f"./{mod_name}").exists():
            print(f"{mod_name} does not exist. Check that you didn't make a typo!")
        else:
            while True:
                item_type = input("Type 'w' if you are creating weapons or type 'a' if you are creating armor: ")
                if item_type.lower() == 'w':
                    if not Path("./weapon_values.txt").exists():
                        print("Error: no weapon_values.txt in current directory!")
                        continue
                    values = pull_values('weapon_values.txt')
                    GenerateWeapon(values, mod_name)
                    continue
                elif item_type.lower() == 'a':
                    if not Path("./armor_values.txt").exists():
                        print("Error: no armor_values.txt in current directory!")
                        continue
                    values = pull_values('armor_values.txt')
                    GenerateArmor(values, mod_name)
                    continue
                elif item_type.lower() == 'q':
                    return
                else:
                    continue


"""
If you are continuously working on the same thing, uncomment and change what you need here:
"""
# mod_name = "TheNameOfYourMod"
# weapon_vals = pull_values('weapon_values.txt')
# GenerateWeapon(weapon_vals, mod_name)
# armor_vals = pull_values('armor_values.txt')
# GenerateArmor(armor_vals, mod_name)

"""
If you uncommented some of the above, don't forget to comment out this function call:
"""
driver()
