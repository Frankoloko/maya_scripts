import sys
import os
from maya import cmds
from maya import mel
from PySide2 import QtCore, QtGui, QtWidgets

################################################################################
##### DEFAULT VALUES #####

SAVE_TO = '/Users/francois/Desktop/Test'

################################################################################
##### FUNCTIONS #####

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

def move_to_zero():
    '''
        This moves the object to world zero
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
btn_move = QtWidgets.QPushButton('Move to world zero')
btn_move.clicked.connect(move_to_zero)
btn_export = QtWidgets.QPushButton('Export FBX')
btn_export.clicked.connect(export_fbx)

# Create layout
layout = QtWidgets.QVBoxLayout()
layout.addWidget(cbx_move_origin)
layout.addWidget(cbx_remove_shading)
layout.addWidget(btn_move)
layout.addWidget(lbl_name)
layout.addWidget(let_name)
layout.addWidget(lbl_save_to)
layout.addWidget(let_save_to)
layout.addWidget(btn_export)

# Create the window
window = QtWidgets.QWidget()
window.setWindowFlags(QtCore.Qt.Tool)
# window.resize(800, 600) # If you want this
window.setLayout(layout)
window.show()