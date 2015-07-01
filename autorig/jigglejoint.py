__author__ = 'Byungkuk'

import maya.cmds as mc


def jiggleJoint(sel_obj):
    sel_obj_type = mc.objectType(sel_obj)
    if sel_obj_type == 'transform' or sel_obj_type == 'joint':
        print "make jiggle joint"

        jiggle_global_grp = makeNullTransformOn(None, sel_obj + "_jiggleGlobal_grp")
        jiggle_grp = makeNullTransformOn(sel_obj, sel_obj + "_jiggle_grp")
        jiggle_rig_grp = makeNullTransformOn(jiggle_grp, sel_obj + "_jiggleRig_grp")
        jiggle_dyn_grp = makeNullTransformOn(jiggle_grp, sel_obj + "_jiggleDyn_grp")

        sel_jnt_radius = 0.1
        if sel_obj_type == 'joint':
            sel_jnt_radius = mc.joint(sel_obj, q=True, radius=True)[0]

        jiggle_jnt = makeJointOn(jiggle_rig_grp, sel_obj + "_jiggleJnt_bind", sel_jnt_radius + 0.1)

        jiggle_soft, jiggle_particle, jiggle_tgt = makeDynamicPlaneOn(worldPosition(sel_obj), sel_obj + "_jiggleDyn")

        mc.parent(jiggle_tgt, jiggle_dyn_grp)
        jiggle_const = makeTransformConstraintOnSoft(worldPosition(sel_obj), jiggle_soft)
        mc.parentConstraint(jiggle_const, jiggle_rig_grp, maintainOffset=True)

        mc.parent(jiggle_soft, jiggle_global_grp)
        mc.parent(jiggle_const, jiggle_global_grp)


def worldPosition(sel_obj):
    return mc.xform(sel_obj, q=True, ws=True, translation=True)


def makeNullTransformOn(sel_obj, obj_name):
    if sel_obj is None:
        return mc.group(empty=True, name=obj_name)
    return mc.group(empty=True, parent=sel_obj, name=obj_name)


def makeJointOn(sel_obj, jnt_name, radius):
    return mc.joint(sel_obj, name=jnt_name, radius=radius)


def makeLocatorOn(world_pos, locator_name):
    locator_obj = mc.spaceLocator(name=locator_name)[0]
    mc.move(world_pos[0], world_pos[1], world_pos[2], locator_obj)
    return locator_obj


def makeDynamicPlaneOn(world_pos, dyn_obj):
    dyn_soft = mc.polyPlane(w=1, h=1, sx=1, sy=1, name=dyn_obj + "_soft", ch=False)[0]
    mc.xform(dyn_soft, ws=True, translation=world_pos)
    dyn_soft_particle = mc.soft(dyn_soft, c=True, d=True, g=0.5)[0]
    dyn_soft_goal = mc.rename("copyOf" + dyn_soft, dyn_obj + "_goal")
    return dyn_soft, dyn_soft_particle, dyn_soft_goal


def makeTransformConstraintOnSoft(world_pos, jiggle_dyn_soft):
    locator_obj = makeLocatorOn(world_pos, jiggle_dyn_soft+"Loc")
    poly_const = mc.pointOnPolyConstraint(jiggle_dyn_soft, locator_obj, w=1.0)[0]
    mc.setAttr(poly_const+"."+jiggle_dyn_soft+"U0", 0.5)
    mc.setAttr(poly_const+"."+jiggle_dyn_soft+"V0", 0.5)
    return locator_obj
