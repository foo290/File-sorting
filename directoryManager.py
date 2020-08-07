import os

"""     This module has all the paths that the software uses prefixed with cwd.     """

#-----------------------------------------------------  PATH FINDER SCRIPT  ---------------------------------------------

installed_path=os.getcwd()

#-----------------------------------------------------  DATABASE CONNECTIVITY  -----------------------------------------

user_configuration_DATABASE=f'{installed_path}/Configurations/database/user_config.db'
extensions_DATABASE=f'{installed_path}/Configurations/database/extensions.db'

#-----------------------------------------------------  COMPONENTS CONNECTIVITY  ---------------------------------------

icon_logo=f'{installed_path}/Configurations/Components/SoftFrontendManager/Graphics/Logo/_0101.ico'
nonsorted_graphic=f'{installed_path}/Configurations/Components/SoftFrontendManager/Graphics/001.png'
fileClash_graphic=f'{installed_path}/Configurations/Components/SoftFrontendManager/Graphics/002.png'
autoSense_Exit_graphic=f'{installed_path}/Configurations/Components/SoftFrontendManager/Graphics/003.png'
autoSense_404_graphic=f'{installed_path}/Configurations/Components/SoftFrontendManager/Graphics/004.png'
autoSense_Enable_graphic=f'{installed_path}/Configurations/Components/SoftFrontendManager/Graphics/005.png'
base_graphic_img=f'{installed_path}/Configurations/Components/SoftFrontendManager/Graphics/290670.png'





