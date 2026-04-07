import maya.cmds as cmds


class Building():

    building_height = 10
    building_width = 3
    building_length = 5
    building_levels = 3
    levels_height = 1

    def generate_base(self):
        building_name = cmds.polyCube(height=self.building_height,
                                      depth=self.building_length,
                                      width=self.building_width,
                                      name="base")[0]
        # move to y=0
        cmds.xform(building_name, translation=[0, self.building_height / 2.0, 0])
        self._freeze_transforms(building_name)
        self._set_pivot_to_origin(building_name)

    def generate_levels(self):
        cube_names = []
        for level in range(self.building_levels):
            # create cubes
            cube_name = cmds.polyCube(height=self.levels_height,
                                      depth=self.building_length + 1,
                                      width=self.building_width + 1,
                                      name="cube")[0]
            cmds.xform(cube_name, translation=[0, self.levels_height / 2.0, 0])
            self._freeze_transforms(cube_name)
            self._set_pivot_to_origin(cube_name)

            # move cubes into position
            if level != self.building_levels - 1:
                cmds.xform(cube_name,
                           translation=[0, self.building_height / (level + 1), 0])
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
    building1 = Building()
    building1.building_height = 7
    building1.generate_base()
    building1.generate_levels()
