import sys
from maya import cmds
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
    pass

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

    # Move the object to world zero
    cmds.matchTransform(selection, world_zero, position=True)

    # Delete the original group
    cmds.delete(world_zero)

################################################################################
##### BUILD QT #####

# Create basic controls
lbl_name = QtWidgets.QLabel('Item name')
let_name = QtWidgets.QLineEdit()
lbl_save_to = QtWidgets.QLabel('Save to')
let_save_to = QtWidgets.QLineEdit(SAVE_TO)
cbx_move_origin = QtWidgets.QCheckBox('Change origin')
btn_move = QtWidgets.QPushButton('Move to world zero')
btn_move.clicked.connect(move_to_zero)
btn_export = QtWidgets.QPushButton('Export FBX')
btn_export.clicked.connect(export_fbx)

# Create layout
layout = QtWidgets.QVBoxLayout()
layout.addWidget(cbx_move_origin)
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