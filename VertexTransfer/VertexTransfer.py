__author__ = 'Byungkuk'

""" vertex info transfer """

import maya.cmds as mc


def vertexTransfer(src_shape, tgt_shape):
    if isMeshType(src_shape) and isMeshType(tgt_shape):
        print "Source mesh: ", src_shape
        print "Target mesh: ", tgt_shape

        if checkTopology(src_shape, tgt_shape):
            doTransfer(src_shape, tgt_shape)
        else:
            return "Topology should be exactly same"
    else:
        print "Both source and target should be mesh object"
        return


def isMeshType(obj):
    if mc.objectType(obj) == 'mesh':
        return True
    else:
        return False


def checkTopology(src_shape, tgt_shape):
    src_n_v = mc.polyEvaluate(src_shape, vertex=True)
    src_n_f = mc.polyEvaluate(src_shape, face=True)
    src_n_e = mc.polyEvaluate(src_shape, edge=True)
    tgt_n_v = mc.polyEvaluate(tgt_shape, vertex=True)
    tgt_n_f = mc.polyEvaluate(tgt_shape, face=True)
    tgt_n_e = mc.polyEvaluate(tgt_shape, edge=True)

    if src_n_v != tgt_n_v:
        print "Number of vertices is not matched"
        return False
    elif src_n_f != tgt_n_f:
        print "Number of faces is not matched"
        return False
    elif src_n_e != tgt_n_e:
        print "Number of edges is not matched"
        return False

    print "Simple topology test is passed"
    return True


def doTransfer(src_shape, tgt_shape):
    print "Start transfer..."

    n_v = mc.polyEvaluate(src_shape, vertex=True)
    for i in range(n_v):
        src_vtx = src_shape + (".vtx[%d]" % i)
        src_pos = mc.pointPosition(src_vtx, local=True)

        tgt_vtx = tgt_shape + (".vtx[%d]" % i)
        tgt_pos = mc.pointPosition(tgt_vtx, local=True)

        vec = [t - s for t, s in zip(tgt_pos, src_pos)]
        # mc.polyMoveVertex(src_vtx, localTranslate=tuple(vec)) # why not working?
        mc.move(vec[0], vec[1], vec[2], src_vtx, r=True)

    print "Done transfer..."
