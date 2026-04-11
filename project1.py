import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide6 import QtWidgets, QtCore
from shiboken6 import wrapInstance


def get_maya_main_win():
    """Return the Maya main window"""
    main_win_addr = omui.MQtUtil.mainWindow()
    wrapInstance(int(main_win_addr), QtWidgets.QWidget)


class BuildingWin(QtWidgets.QDialog):

    def __init__(self):
        super().__init__(parent=get_maya_main_win())
        self.building = Building()
        self.setWindowTitle("Building Generator")
        # self.resize(500, 200)
        self._mk_main_layout()
        self._connect_signals()

    def build_building(self):
        self.building.building_height = self.building_height_dspnbx.value()
        self.building.building_levels = self.building_levels_slider.value()
        self.building.generate_building()

    def _connect_signals(self):
        self.build_btn.clicked.connect(self.build_tree)
        self.cancel_btn.clicked.connect(self.close)

        self.building_levels_slider.valueChanged.connect(self.building_levels_slider_lbl.setValue)
        self.building_levels_slider_lbl.valueChanged.connect(self.building_levels_slider.setValue)

    def _mk_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()  # Creates our vertical box layout.
        self._mk_building_height_ui()
        self._mk_building_option_ui()
        self._mk_buttons_layout()
        self.setLayout(self.main_layout)

    def _mk_building_option_ui(self):
        self.building_levels_layout = QtWidgets.QHBoxLayout()
        self.building_levels_lbl = QtWidgets.QLabel("Building Levels")

        self.building_levels_slider = QtWidgets.QSlider()
        self.building_levels_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.building_levels_slider.setMaximum(3)
        self.building_levels_slider.setMinimumWidth(50)
        self.building_levels_slider.setValue(3)

        self.building_levels_slider_lbl = QtWidgets.QSpinBox()
        self.building_levels_slider_lbl.setValue(3)
        self.building_levels_slider_lbl.setMaximum(3)

        self.building_levels_layout.addWidget(self.building_levels_lbl)
        self.building_levels_layout.addWidget(self.building_levels_slider)
        self.building_levels_layout.addWidget(self.building_levels_slider_lbl)
        self.main_layout.addLayout(self.building_levels_layout)

    def _mk_building_height_ui(self):
        self.building_height_layout = QtWidgets.QHBoxLayout()
        self.building_height_lbl = QtWidgets.QLabel("Building Height")
        self.building_height_dspnbx = QtWidgets.QDoubleSpinBox()
        self.building_height_dspnbx.setMinimumWidth(50)
        self.building_height_dspnbx.setValue(5.0)
        self.building_height_dspnbx.setSingleStep(1.0)
        self.building_height_layout.addWidget(self.building_height_lbl)
        self.building_height_layout.addWidget(self.building_height_dspnbx)
        self.main_layout.addLayout(self.building_height_layout)  # Directs the Dialog Window to use the main layout

    def _mk_buttons_layout(self):
        self.build_btn = QtWidgets.QPushButton("Build")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.main_layout.addWidget(self.build_btn)  # Adds the build button into one of the rows in the vertical layout
        self.main_layout.addWidget(self.cancel_btn)  # Adds the build button into one of the rows in the vertical layout


class Building():

    building_height = 10
    building_width = 3
    building_length = 5
    building_levels = 3
    levels_height = 1

    def generate_building(self):
        grp_objs = []
        grp_objs.append(self.generate_trunk())
        grp_objs.append(self.generate_canopy())
        tree_grp = cmds.group(grp_objs, name="tree")
        self._set_pivot_to_origin(tree_grp)

    def generate_base(self):
        building_name = cmds.polyCube(height=self.building_height,
                                      depth=self.building_length,
                                      width=self.building_width,
                                      name="base")[0]
        # move to y=0
        cmds.xform(building_name,
                   translation=[0, self.building_height / 2.0, 0])
        self._freeze_transforms(building_name)
        self._set_pivot_to_origin(building_name)

    def generate_levels(self):
        cube_names = []
        for level in range(self.building_levels):
            # create cubes
            cube_name = cmds.polyCube(height=self.levels_height,
                                      depth=self.building_length + 0.5 / self.building_length,
                                      width=self.building_width + 0.5 / self.building_height,
                                      name="cube")[0]
            cmds.xform(cube_name, translation=[0, self.levels_height / 2.0, 0])
            self._freeze_transforms(cube_name)
            self._set_pivot_to_origin(cube_name)

            # move cubes into position
            if level != self.building_levels - 1:
                cmds.xform(cube_name, translation=[0, self.building_height / (level + 1), 0])
            cube_names.append(cube_name)

        # group cubes into group
        grp_name = cmds.group(cube_names, name="levels")
        # move canopy pivot to bottom
        self._set_pivot_to_origin(grp_name)

    def _freeze_transforms(self, obj):
        cmds.makeIdentity(obj, apply=True, translate=True, rotate=True,
                          scale=True, normal=False, preserveNormals=True)

    def _set_pivot_to_origin(self, obj_name):
        cmds.xform(obj_name, pivots=[0, 0, 0])




if "__main__" == __name__:
    # building1 = Building()
    # building1.building_height = 7
    # building1.generate_base()
    # building1.generate_levels()
    w = BuildingWin()
    w.show()
