import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide6 import QtWidgets, QtCore
from shiboken6 import wrapInstance
import random


def get_maya_main_win():
    """Return the Maya main window"""
    main_win_addr = omui.MQtUtil.mainWindow()
    wrapInstance(int(main_win_addr), QtWidgets.QWidget)


class BuildingWin(QtWidgets.QDialog):

    def __init__(self):
        super().__init__(parent=get_maya_main_win())
        self.building = Building()
        self.resize(300, 200)
        self.setWindowTitle("Building Generator")
        self._mk_main_layout()
        self._connect_signals()

    def build_building(self):
        self.building.building_height = self.building_height_dspnbx.value()
        self.building.building_levels = self.building_levels_slider.value()
        self.building.building_width = self.building_width_dspnbx.value()
        self.building.building_length = self.building_length_dspnbx.value()
        self.building.building_length = self.building_length_dspnbx.value()
        self.building.windows = self.window_checkbox.isChecked()
        self.building.random_windows = self.rndm_windows_checkbox.isChecked()
        self.building.window_width_mult = self.window_size_dspnbx.value()
        self.building.generate_building()

    def _connect_signals(self):
        self.build_btn.clicked.connect(self.build_building)
        self.delete_btn.clicked.connect(self.building.delete_building)
        self.delete_all_btn.clicked.connect(self.building.delete_all)
        self.cancel_btn.clicked.connect(self.close)

        self.building_levels_slider.valueChanged.connect(self.building_levels_slider_lbl.setValue)
        self.building_levels_slider_lbl.valueChanged.connect(self.building_levels_slider.setValue)

        self.window_checkbox.stateChanged.connect(self.rndm_windows_checkbox.setChecked)

    def _mk_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()  # Creates our vertical box layout.
        self._mk_building_height_ui()
        self._mk_building_width_ui()
        self._mk_building_length_ui()
        self._mk_building_levels_ui()
        self._mk_checkboxes_ui()
        self._mk_window_size_ui()
        self._mk_buttons_layout()
        self.setLayout(self.main_layout)

    def _mk_building_levels_ui(self):
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
        self.main_layout.addLayout(self.building_height_layout)

    def _mk_building_width_ui(self):
        self.building_width_layout = QtWidgets.QHBoxLayout()
        self.building_width_lbl = QtWidgets.QLabel("Building Width")
        self.building_width_dspnbx = QtWidgets.QDoubleSpinBox()
        self.building_width_dspnbx.setMinimumWidth(20)
        self.building_width_dspnbx.setValue(3.0)
        self.building_width_dspnbx.setSingleStep(1.0)
        self.building_width_layout.addWidget(self.building_width_lbl)
        self.building_width_layout.addWidget(self.building_width_dspnbx)
        self.main_layout.addLayout(self.building_width_layout)

    def _mk_building_length_ui(self):
        self.building_length_layout = QtWidgets.QHBoxLayout()
        self.building_length_lbl = QtWidgets.QLabel("Building Length")
        self.building_length_dspnbx = QtWidgets.QDoubleSpinBox()
        self.building_length_dspnbx.setValue(5.0)
        self.building_length_dspnbx.setSingleStep(1.0)
        self.building_length_layout.addWidget(self.building_length_lbl)
        self.building_length_layout.addWidget(self.building_length_dspnbx)
        self.main_layout.addLayout(self.building_length_layout)

    def _mk_window_size_ui(self):
        self.window_size_layout = QtWidgets.QHBoxLayout()
        self.window_size_lbl = QtWidgets.QLabel("Window Width")
        self.window_size_dspnbx = QtWidgets.QDoubleSpinBox()
        self.window_size_dspnbx.setMinimumWidth(50)
        self.window_size_dspnbx.setValue(5.0)
        self.window_size_dspnbx.setSingleStep(0.5)
        self.window_size_layout.addWidget(self.window_size_lbl)
        self.window_size_layout.addWidget(self.window_size_dspnbx)
        self.main_layout.addLayout(self.window_size_layout)

    def _mk_checkboxes_ui(self):
        self.building_checkbox_layout = QtWidgets.QHBoxLayout()

        self.window_checkbox = QtWidgets.QCheckBox()
        self.window_checkbox_lbl = QtWidgets.QLabel("Windows")

        self.rndm_windows_checkbox = QtWidgets.QCheckBox()
        self.rndm_windows_checkbox_lbl = QtWidgets.QLabel("Random Windows")

        self.building_checkbox_layout.addWidget(self.window_checkbox_lbl)
        self.building_checkbox_layout.addWidget(self.window_checkbox)
        self.building_checkbox_layout.addWidget(self.rndm_windows_checkbox_lbl)
        self.building_checkbox_layout.addWidget(self.rndm_windows_checkbox)
        self.main_layout.addLayout(self.building_checkbox_layout)

    def _mk_buttons_layout(self):
        self.build_btn = QtWidgets.QPushButton("Build")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.delete_btn = QtWidgets.QPushButton("Delete Building")
        self.delete_all_btn = QtWidgets.QPushButton("Delete All")
        self.main_layout.addWidget(self.build_btn)
        self.main_layout.addWidget(self.delete_btn)
        self.main_layout.addWidget(self.delete_all_btn)
        self.main_layout.addWidget(self.cancel_btn)


class Building():

    building_height = 10
    building_width = 3
    building_length = 5
    building_levels = 3
    window_width_mult = 1.2
    windows = True
    random_windows = None
    recent_building = ""
    building_list = []

    def delete_building(self):
        cmds.delete(self.recent_building)

    def delete_all(self):
        for building in self.building_list:
            cmds.delete(building)

    def generate_building(self):
        self.recent_building = ""
        grp_objs = []
        grp_objs.append(self.generate_base())
        grp_objs.append(self.generate_levels())
        if self.windows is True:
            grp_objs.append(self.generate_windows())
        bldg_grp = cmds.group(grp_objs, name="building")
        self._set_pivot_to_origin(bldg_grp)

        self.recent_building = bldg_grp
        self.building_list.append(self.recent_building)

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
        return building_name

    def generate_levels(self):
        cube_names = []
        levels_height = self.building_height / 6
        for level in range(self.building_levels):
            # create cubes
            cube_name = cmds.polyCube(height=levels_height,
                                      depth=self.building_length + 0.5,
                                      width=self.building_width + 0.5,
                                      name="level")[0]
            cmds.xform(cube_name, translation=[0, levels_height / 2.0, 0])
            self._freeze_transforms(cube_name)
            self._set_pivot_to_origin(cube_name)

            # move cubes into position
            if level != self.building_levels - 1:
                cmds.xform(cube_name, translation=[0, self.building_height / (level + 1), 0])
            cube_names.append(cube_name)

        if self.building_levels != 0:
            grp_name = cmds.group(cube_names, name="levels")
            self._set_pivot_to_origin(grp_name)
            return grp_name

    def generate_windows(self):
        window_height = self.building_height / 4
        window_width = self.building_length / self.window_width_mult
        window_y = window_height - window_height / 5

        x_side = self.building_width / 2
        z_side = 0
        y_rotate = 0

        window_names = []
        for face in range(2):
            for side in range(2):
                for window in range(2):

                    # chance of window not generating
                    if self.random_windows is True:
                        if random.randint(1, 10) <= 4:
                            continue

                    window_name = cmds.polyCube(height=window_height,
                                                depth=window_width,
                                                width=0.1,
                                                name="window")[0]
                    cmds.xform(window_name, rotation=[0, y_rotate, 0], translation=[0, window_height / 2, 0])
                    self._freeze_transforms(window_name)
                    self._set_pivot_to_origin(window_name)

                    cmds.xform(window_name, translation=[x_side,  # move to the wall
                               window_y,  # move up the wall
                               z_side])

                    # alternate height
                    window_names.append(window_name)
                    window_y *= 3.5
                # alternate side
                window_y = window_height - window_height / 5
                x_side *= -1
                z_side *= -1
            # alternate face
            y_rotate = 90
            x_side = 0
            z_side = self.building_length / 2
            window_width = self.building_width / self.window_width_mult

        grp_name = cmds.group(window_names, name="windows")
        self._set_pivot_to_origin(grp_name)
        return grp_name

    def _freeze_transforms(self, obj):
        cmds.makeIdentity(obj, apply=True, translate=True, rotate=True,
                          scale=True, normal=False, preserveNormals=True)

    def _set_pivot_to_origin(self, obj_name):
        cmds.xform(obj_name, pivots=[0, 0, 0])


if "__main__" == __name__:
    building1 = Building()
    # building1.building_height = 7
    # building1.generate_base()
    # building1.generate_levels()
    w = BuildingWin()
    w.show()
    # building1.generate_windows()
    # building1.generate_building()
