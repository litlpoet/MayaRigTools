__author__ = 'Byungkuk'

import maya.cmds as mc


def jiggleJoint(sel_obj):
    sel_obj_type = mc.objectType(sel_obj)
    if sel_obj_type == 'transform' or sel_obj_type == 'joint':
        print "make jiggle joint"
        obj_trans = mc.xform(sel_obj, q=True, r=True, translation=True)
        print "translation: ", obj_trans

        jiggle_grp = makeNullTransformOn(sel_obj, sel_obj+"_jiggle_grp")
        jiggle_rig_grp = makeNullTransformOn(jiggle_grp, sel_obj+"_jiggleRig_grp")
        jiggle_dyn_grp = makeNullTransformOn(jiggle_grp, sel_obj+"_jiggleDyn_grp")

        sel_jnt_radius = 0.5
        if sel_obj_type == 'joint':
            sel_jnt_radius = mc.joint(sel_obj, q=True, radius=True)[0]

        jiggle_jnt = makeJointOn(jiggle_rig_grp, sel_obj+"_jiggleJnt_bind", sel_jnt_radius + 0.1)

        jiggle_system = makeDynamicPlaneOn(worldPosition(sel_obj), sel_obj+"_jiggleDyn_sys")



def worldPosition(sel_obj):
    return mc.xform(sel_obj, q=True, ws=True, translation=True)


def makeNullTransformOn(sel_obj, obj_name):
    return mc.group(empty=True, parent=sel_obj, name=obj_name)


def makeJointOn(sel_obj, jnt_name, radius):
    return mc.joint(sel_obj, name=jnt_name, radius=radius)


def makeDynamicPlaneOn(world_pos, plane_name):
    poly_plane_obj = mc.polyPlane(w=1, h=1, sx=1, sy=1, name=plane_name, ch=False)
    mc.xform(poly_plane_obj, ws=True, translation=world_pos)
    result = mc.soft(poly_plane_obj, c=True, d=True, g=0.5)
    print result
    return poly_plane_obj
