import sys
import os
from maya import cmds
from maya import mel
from PySide2 import QtCore, QtGui, QtWidgets

################################################################################
##### DEFAULT VALUES #####

SAVE_TO = '/Users/francois/Desktop/tester'

################################################################################
##### FUNCTIONS #####

def import_folder():
    '''
        This will import FBX items from a folder
    '''
    folder_path = let_save_to.text()

    if cbx_import_walk.isChecked():
        # Walk
        for base, folders, files in os.walk(folder_path):
            for file in files:
                if '.fbx' not in file and '.FBX' not in file:
                    continue
                file_path = os.path.join(base, file)
                cmds.file(file_path, i=True)
    else:
        # Top folder only
        for file in os.listdir(folder_path):
            if '.fbx' not in file and '.FBX' not in file:
                continue
            file_path = os.path.join(folder_path, file)
            cmds.file(file_path, i=True)

def fix_folder():
    '''
        This will run through a folder, import each asset, fix it, and export it.
    '''
    folder_path = let_save_to.text()

    for base, folders, files in os.walk(folder_path):
        for file in files:
            if '.fbx' not in file and '.FBX' not in file:
                continue

            print('Doing: {}'.format(file))

            cmds.file(force=True, new=True)

            file_path = os.path.join(base, file)

            # Import the file
            imported_nodes = cmds.file(file_path, i=True, returnNewNodes=True)

            # Get the parent node
            parent_node = None
            for node_name in imported_nodes:
                if node_name.count('|') == 1:
                    parent_node = node_name
                    break

            # Select the imported item
            cmds.select(parent_node)

            # Fix the file
            fix_model()
            
            # Export the object
            mel.eval('FBXExport -f "{}" -s'.format(file_path))

    print('FINISHED')

def export_fbx():
    '''
        Export the item
    '''
    # Get the export filename
    file_path = os.path.join(let_save_to.text(), let_name.text() + '.fbx')

    # Check if the file exists already
    if os.path.isfile(file_path):
        result = cmds.confirmDialog( title='File Already Exists', message='Do you want to overwrite the file?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if result == 'No':
            return

    # Export the object
    mel.eval('FBXExport -f "{}" -s'.format(file_path))
    cmds.confirmDialog(title='Success', message='Exported successfully')

def fix_model():
    '''
        This will run many function to clean and fix the model
    '''
    # Get the selected item (do this before creating a group because
    # creating a group makes it automatically selected as well)
    selection = cmds.ls(selection=True)

    # Create a group at world 0
    world_zero = cmds.group(empty=True, name='world_zero')

    if cbx_move_origin.isChecked():
        # Move the object's origin to the middle-bottom of its bounding box
        bbox = cmds.exactWorldBoundingBox(selection)
        bottom = [(bbox[0] + bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2]
        cmds.xform(selection, piv=bottom, ws=True)

    if cbx_remove_shading.isChecked():
        # Select the object again
        cmds.select(selection)

        # Remove all the shading groups off the object
        nodes = cmds.ls(sl=True, dag=True, s=True)
        shading_engines = cmds.listConnections(nodes , type="shadingEngine")
        materials = cmds.ls(cmds.listConnections(shading_engines), materials=True)

        # Filter out unique items from lists
        materials = list(set(materials))
        shading_engines = list(set(shading_engines))

        # Delete everything
        for item in materials:
            cmds.delete(item)
        for item in shading_engines:
            cmds.delete(item)

    # Move the object to world zero
    cmds.matchTransform(selection, world_zero, position=True)

    # Delete the original group
    cmds.delete(world_zero)

    # Select the object again
    cmds.select(selection)

################################################################################
##### BUILD QT #####

# Create basic controls
lbl_name = QtWidgets.QLabel('Item name')
let_name = QtWidgets.QLineEdit()
lbl_save_to = QtWidgets.QLabel('Save to')
let_save_to = QtWidgets.QLineEdit(SAVE_TO)
cbx_move_origin = QtWidgets.QCheckBox('Change origin')
cbx_move_origin.setChecked(True)
cbx_remove_shading = QtWidgets.QCheckBox('Remove shading groups')
cbx_remove_shading.setChecked(True)
btn_fix = QtWidgets.QPushButton('Fix model')
btn_fix.clicked.connect(fix_model)
btn_export = QtWidgets.QPushButton('Export FBX')
btn_export.clicked.connect(export_fbx)
btn_fix_folder = QtWidgets.QPushButton('Fix folder')
btn_fix_folder.clicked.connect(fix_folder)
cbx_import_walk = QtWidgets.QCheckBox('Walk through all folders')
cbx_import_walk.setChecked(True)
btn_import_folder = QtWidgets.QPushButton('Import folder')
btn_import_folder.clicked.connect(import_folder)

# Create layout
layout = QtWidgets.QVBoxLayout()
layout.addWidget(cbx_move_origin)
layout.addWidget(cbx_remove_shading)
layout.addWidget(btn_fix)
layout.addWidget(lbl_name)
layout.addWidget(let_name)
layout.addWidget(lbl_save_to)
layout.addWidget(let_save_to)
layout.addWidget(btn_export)
layout.addWidget(btn_fix_folder)
layout.addWidget(cbx_import_walk)
layout.addWidget(btn_import_folder)

# Create the window
window = QtWidgets.QWidget()
window.setWindowFlags(QtCore.Qt.Tool)
window.resize(300, 200)
window.setLayout(layout)
window.show()