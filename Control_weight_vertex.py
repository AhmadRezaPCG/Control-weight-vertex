###############################################################################
# Name: 
#   Cpntrol weight vertex
#
# Description: 
#    in maya when object is bind to joint , by this scrip you can control weight verex and also you can mirror single joint with more control
#    or you can zero value weight transform that you selected or use againts joint mode to zero.
#
# Author: 
#   Ahmadreza Rezaei
#
# Copyright (C) 2022 Ahmadreza Rezaei. All rights reserved.
###############################################################################

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.mel as mel

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

def maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window),QtWidgets.QWidget)
    
class controlweightvertex(QtWidgets.QDialog):
    
    extrasource = []
    extratarget = []
    dialog_window = None
    
    def __init__(self,parent=maya_main_window()):
        super(controlweightvertex,self).__init__(parent)
        
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Control weight vertex")
        self.createwidget()
        self.createlayout()
        self.connectsignalslot()
    
    @classmethod
    def show_dialog(cls):
        if cls.dialog_window:
            if cls.dialog_window.isHidden():
                cls.dialog_window.show()
            else:
                cls.dialog_window.raise_()
                cls.dialog_window.activateWindow()
        else:
            cls.dialog_window = controlweightvertex()
            cls.dialog_window.show()
    
    def createwidget(self):
        
        self.L_side      = QtWidgets.QLabel("Symmetry : ")
        
        self.RB_x        = QtWidgets.QRadioButton("x")
        self.RB_y        = QtWidgets.QRadioButton("y")
        self.RB_z        = QtWidgets.QRadioButton("z")
        self.RB_x.setChecked                     (True)
        self.F__1 = QtWidgets.QFrame()
        self.F__1.setFrameStyle(QtWidgets.QFrame.HLine)
        
        self.L_object    = QtWidgets.QLabel("Object : ")
        self.LE_object   = QtWidgets.QLineEdit()
        self.LE_object              .setEnabled(False)
        self.PB_object   = QtWidgets.QPushButton(" Set ")
        
        self.F_0 = QtWidgets.QFrame()
        self.F_0.setFrameStyle(QtWidgets.QFrame.HLine)
        
        self.L_sourcejnt    = QtWidgets.QLabel("Source joint : ")
        self.LE_sourcejnt   = QtWidgets.QLineEdit()
        self.LE_sourcejnt              .setEnabled(False)
        self.PB_sourcejnt   = QtWidgets.QPushButton(" Set ")
        
        self.L_targetjnt    = QtWidgets.QLabel("Target joint : ")
        self.LE_targetjnt   = QtWidgets.QLineEdit()
        self.LE_targetjnt              .setEnabled(False)
        self.PB_targetjnt   = QtWidgets.QPushButton(" Set ")
        
        self.F_1 = QtWidgets.QFrame()
        self.F_1.setFrameStyle(QtWidgets.QFrame.HLine)
        
        self.L_extrasource  = QtWidgets.QLabel("Extra source joint :")
        self.VL_extrasource  = QtWidgets.QVBoxLayout()
        self.PB_extrasource = QtWidgets.QPushButton(" Set ")
        
        self.F_2 = QtWidgets.QFrame()
        self.F_2.setFrameStyle(QtWidgets.QFrame.HLine)
        
        self.L_extratarget  = QtWidgets.QLabel("Extra target joint :")
        self.VL_extratarget  = QtWidgets.QVBoxLayout()
        self.PB_extratarget = QtWidgets.QPushButton(" Set ")
        
        self.F_3 = QtWidgets.QFrame()
        self.F_3.setFrameStyle      (   QtWidgets.QFrame.HLine  )
        self.F_3.setLineWidth       (   50  )
        self.F_3.setFrameShadow     (QtWidgets.QFrame.Sunken)
        
        self.PB_mirror      = QtWidgets.QPushButton("Mirror skin weight")
        
        self.F_4 = QtWidgets.QFrame()
        self.F_4.setFrameStyle      (   QtWidgets.QFrame.HLine  )
        self.F_4.setLineWidth   (   10  )
        
        self.CB_switch          = QtWidgets.QComboBox()
        self.CB_switch.addItem    ("By replace")
        self.CB_switch.addItem    ("By select")
        self.CB_switch.setEditable(False)      
        
        self.L_searchkw     = QtWidgets.QLabel("Search key world : ")
        self.LE_searchkw    = QtWidgets.QLineEdit()
        self.LE_searchkw.setText("_L_")
        
        self.L_replacekw    = QtWidgets.QLabel("Replace key world : ")
        self.LE_replacekw   = QtWidgets.QLineEdit()
        self.LE_replacekw.setText("_R_")
        
        self.PB_setselected= QtWidgets.QPushButton("Set selected")
        self.VL_selected   = QtWidgets.QVBoxLayout()
        
        self.PB_zero        = QtWidgets.QPushButton("Zero weight") 
        
        self.L_copyright    = QtWidgets.QLabel("Copyright2022-Ahmadreza Rezaei.")
        self.L_reserved     = QtWidgets.QLabel("All Rights Reserved.")
        
        
    def createlayout        (self):
        
        HL_side      =QtWidgets.QHBoxLayout()
        HL_side.addWidget  (     self.L_side      )
        HL_side.addWidget  (     self.RB_x        )
        HL_side.addWidget  (     self.RB_y        )
        HL_side.addWidget  (     self.RB_z        )
        
        HL_object    = QtWidgets.QHBoxLayout()
        HL_object.addWidget(     self.L_object    )
        HL_object.addWidget(     self.LE_object   )
        HL_object.addWidget(     self.PB_object   )
        
        
        
        HL_sourcejnt    = QtWidgets.QHBoxLayout()
        HL_sourcejnt.addWidget(     self.L_sourcejnt    )
        HL_sourcejnt.addWidget(     self.LE_sourcejnt   )
        HL_sourcejnt.addWidget(     self.PB_sourcejnt   )
        
        
        
        HL_targetjnt    = QtWidgets.QHBoxLayout()
        HL_targetjnt.addWidget(     self.L_targetjnt    )
        HL_targetjnt.addWidget(     self.LE_targetjnt   )
        HL_targetjnt.addWidget(     self.PB_targetjnt   )
        
        
        
        HL_setextrasource = QtWidgets.QHBoxLayout()
        HL_setextrasource.addWidget (   self.L_extrasource      )
        HL_setextrasource.addStretch(                           )
        HL_setextrasource.addWidget (   self.PB_extrasource     )
        
        VL_extrasource  = QtWidgets.QVBoxLayout()
        VL_extrasource.addLayout(   HL_setextrasource    )
        VL_extrasource.addLayout(   self.VL_extrasource  )
        
        
        
        HL_setextratarget = QtWidgets.QHBoxLayout()
        HL_setextratarget.addWidget (   self.L_extratarget      )
        HL_setextratarget.addStretch()
        HL_setextratarget.addWidget (   self.PB_extratarget     )
        
        VL_extratarget  = QtWidgets.QVBoxLayout()
        VL_extratarget.addLayout(   HL_setextratarget   )
        VL_extratarget.addLayout(   self.VL_extratarget  )
        
        HL_searchkw = QtWidgets.QHBoxLayout()
        HL_searchkw.addWidget(  self.L_searchkw     )
        HL_searchkw.addWidget(  self.LE_searchkw     )
        
        HL_replacekw = QtWidgets.QHBoxLayout()
        HL_replacekw.addWidget(  self.L_replacekw     )
        HL_replacekw.addWidget(  self.LE_replacekw     )
        
        
        
        MAIN_LAY = QtWidgets.QVBoxLayout(self)
        MAIN_LAY.addLayout(     HL_side             )
        MAIN_LAY.addWidget(     self.F__1           )
        MAIN_LAY.addLayout(     HL_object           )
        MAIN_LAY.addWidget(     self.F_0            )
        MAIN_LAY.addLayout(     HL_sourcejnt        )
        MAIN_LAY.addLayout(     HL_targetjnt        )
        MAIN_LAY.addWidget(     self.F_1            )
        MAIN_LAY.addLayout(     VL_extrasource      )
        MAIN_LAY.addWidget(     self.F_2            )
        MAIN_LAY.addLayout(     VL_extratarget      )
        MAIN_LAY.addWidget(     self.PB_mirror      )
        MAIN_LAY.addWidget(     self.F_3            )
        MAIN_LAY.addWidget(     self.CB_switch      )
        MAIN_LAY.addLayout(     HL_searchkw         )
        MAIN_LAY.addLayout(     HL_replacekw        )
        MAIN_LAY.addWidget(     self.PB_setselected )
        MAIN_LAY.addLayout(     self.VL_selected    )
        MAIN_LAY.addWidget(     self.PB_zero        )
        MAIN_LAY.addWidget(     self.F_4            )
        MAIN_LAY.addWidget(     self.L_copyright    )
        MAIN_LAY.addWidget(     self.L_reserved     )
        
        MAIN_LAY.setAlignment   (self.L_copyright    ,   QtCore.Qt.AlignCenter)
        MAIN_LAY.setAlignment   (self.L_reserved     ,   QtCore.Qt.AlignCenter)
        
    def connectsignalslot       (self):
        
        self.PB_object.clicked.connect              (self.set_object        )
        self.PB_sourcejnt.clicked.connect           (self.set_sourcejnt     )
        self.PB_targetjnt.clicked.connect           (self.set_targetjnt     )
        self.PB_extrasource.clicked.connect         (self.set_extrasource   )
        self.PB_extratarget.clicked.connect         (self.set_extratarget   )
        self.PB_mirror.clicked.connect              (self.mirror            )
        self.CB_switch.currentTextChanged.connect   (self.switchview        )
        self.PB_setselected.clicked.connect         (self.set_select        )
        self.PB_zero.clicked.connect                (self.zeroweight        )
        
    def switchview              (self):
        
        text_combo = self.CB_switch.currentText()
        if text_combo == "By replace":
            self.LE_replacekw.setVisible    (True                  )
            self.L_replacekw.setVisible     (True                  )
            self.LE_searchkw.setVisible     (True                  )
            self.L_searchkw.setVisible      (True                  )
            self.PB_setselected.setHidden   (True                  )
            self.Hidden_label               (self.VL_selected,True )
        else:
            self.LE_replacekw.setHidden     (True                  )
            self.L_replacekw.setHidden      (True                  )
            self.LE_searchkw.setHidden      (True                  )
            self.L_searchkw.setHidden       (True                  )
            self.PB_setselected.setVisible  (True                  )
            self.Hidden_label               (self.VL_selected,False)
        
            
    def zeroweight              (self):
        
        cmds.undoInfo(openChunk=True)
        
        list_vtx    =    cmds.ls(sl=True,long=True)
        skin_cluster=   self.get_skin_cluster()
        
        
        
        if self.CB_switch.currentText() == "By replace":
        
            search_key  =   self.LE_searchkw.text()
            replace_key =   self.LE_replacekw.text()
            
            if  search_key and replace_key:
                for vtx in list_vtx:
                    influence_joints = cmds.skinCluster(vtx,inf=True,q=True)
                    for influence   in  influence_joints:
                        if search_key in influence:
                            if self.check_count_search(influence,search_key):
                                new_influence       =   influence.replace        (search_key,replace_key)
                                try:
                                    cmds.skinPercent                                 (skin_cluster,vtx,tv =   (new_influence,0))
                                except:
                                    pass
                                    
                            else :
                                om.MGlobal.displayWarning("{0} has more than one ({1})".format(influence,search_key))
                        else :
                            om.MGlobal.displayWarning("{0} doesn't have ({1})".format(influence,search_key))
                            
                            
                            
        elif self.CB_switch.currentText() == "By select":
            
            if self.selected:
                for vtx in list_vtx:
                    for influence in self.selected:
                        try:
                            cmds.skinPercent(skin_cluster,vtx,tv =   (influence,0))
                        except:
                            pass
            else:
                om.MGlobal.displayError("First select your joints . ")
            
            
            
        cmds.undoInfo(closeChunk=True)            
                        
        
    def mirror                  (self):        
        
        cmds.undoInfo(openChunk=True)
        
        skin_cluster = self.get_skin_cluster()
        
        cmds.select(cl=True)
        mel.eval("skinCluster -e -selectInfluenceVerts {0} {1}".format(self.source_joint,skin_cluster))
        list_selected_vtx = cmds.ls(sl=True,flatten=True)
        
        if list_selected_vtx :
            
            side = self.get_symmetryside()
            
            if len(self.extrasource)>0:
                if len(self.extrasource)==len(self.extratarget):
                    
                    self.extrasource.append(self.source_joint)
                    self.extratarget.append(self.target_joint)

                    for vtx in list_selected_vtx:
                        
                        source_values = self.get_value_skin(vtx,skin_cluster)
                        
                        new_vtx = self.get_new_vtx(vtx,side)
                        if new_vtx:
                            for index in range(len(source_values)):
                                try:
                                    cmds.skinPercent(skin_cluster,new_vtx,transformValue =(self.extratarget[index],source_values[index]))
                                except:
                                    pass
                                    
                    del self.extrasource[-1]
                    del self.extratarget[-1]
                
                else:
                    raise RuntimeError("Your extra sorce and extra target must be equal .")
            else: 
            
                for vtx in list_selected_vtx:
                    value = self.get_value_skin(vtx,skin_cluster)
                    new_vtx = self.get_new_vtx(vtx,side)
                    if new_vtx :
                        try:
                            cmds.skinPercent(skin_cluster,new_vtx,transformValue = (self.target_joint,value))
                        except:
                            pass
                            
        cmds.undoInfo(closeChunk=True)
          
    def set_object              (self):
        
        name_obj = cmds.ls      (   sl=True,long=True               )[0]
        self.object         =       name_obj
        self.get_skin_cluster   ()
        self.LE_object.setText  (   self.get_absolute_name(name_obj))
        
                
    def set_sourcejnt           (self):
        
        name_source_joint = cmds.ls (   sl=True,long=True)[0]
        self.LE_sourcejnt.setText   (   self.get_absolute_name(name_source_joint))
        self.source_joint       =       name_source_joint
        
    def set_targetjnt           (self):
        
        name_target_joint = cmds.ls (   sl=True,long=True)[0]
        self.LE_targetjnt.setText   (   self.get_absolute_name(name_target_joint))
        self.target_joint       =       name_target_joint
        
    def set_extrasource         (self):
        
        list_selected = cmds.ls (   sl=True,long=True   )
        self.delete_label       (   self.VL_extrasource )
        
        self.extrasource = []
        for selected in list_selected:
            
            self.extrasource.append         (   selected                                )
            label = QtWidgets.QLabel        (   "   "+self.get_absolute_name(selected)  )
            self.VL_extrasource.addWidget   (   label                                   )
            
    def set_extratarget         (self):
        
        list_selected = cmds.ls (   sl=True,long=True   )
        self.delete_label       (   self.VL_extratarget )
        
        self.extratarget = []
        for selected in list_selected:
            
            self.extratarget.append         (   selected                             )
            label = QtWidgets.QLabel        (   "   "+self.get_absolute_name(selected))
            self.VL_extratarget.addWidget   (   label                                )
        
    def set_select              (self):
        
        self.delete_label(self.VL_selected)
        
        self.selected = cmds.ls(sl=True,long=True)
        if self.selected:
            for select in self.selected:
                label = QtWidgets.QLabel(self.get_absolute_name(select))
                self.VL_selected.addWidget(label)
       
        
    def get_absolute_name       (self,name):
        
        return name.split("|")[-1]
        
    def get_value_skin         (self,vtx,skin_cluster):
        
        if len(self.extrasource)>0:
            
            source_values = []
            for source_joints in self.extrasource :
                source_values.append(cmds.skinPercent(skin_cluster,vtx,transform = source_joints,q=True,value=True))
            return source_values
            
        else:
            return cmds.skinPercent(skin_cluster,vtx,transform = self.source_joint,q=True,value=True)
        
    def get_new_vtx             (self,vtx,side):
        
        mel.eval("reflectionSetMode object{0}".format(side))
        cmds.select(vtx,r=True,sym=True)
        mel.eval("reflectionSetMode none")
        cmds.select(vtx,d=True)
        new_vtx = cmds.ls(sl=True,flatten=True)
        if new_vtx:
            return new_vtx[0]
        else:
            om.MGlobal.displayWarning("{0} dosen't have symmetry . ".format(vtx))
            return False
    
    def get_skin_cluster        (self):
        
        shape_selected = cmds.listRelatives(self.object,s=True)
        if shape_selected:
            history =  cmds.listHistory(shape_selected,lv=3)

            for hist_obj in history:
                if cmds.objectType(hist_obj)=="skinCluster":
                    skin_cluster = hist_obj
                    break
                elif hist_obj == history[-1]:
                    raise RuntimeError("Your object doesn't have skincluster .")
        else:
            raise RuntimeError("Your object doesn't have skincluster .")
        
        
        return skin_cluster
        
    def get_symmetryside        (self):
        
        if self.RB_x.isChecked():
            return "x"
            
        elif self.RB_y.isChecked():
            return "y"

        else:
            return "z"

    def delete_label(self,VL):
        
        count = VL.count()
        for index in range(count):
            VL.itemAt(index).widget().deleteLater()
            
    def Hidden_label(self,VL,bool_hid):
        
        count = VL.count()
        for index in range(count):
            VL.itemAt(index).widget().setHidden(bool_hid)
            
    def check_count_search(self,name,search_key):
        
        new = name.split(search_key)
        if len(new)>2:
            return False
        else:
            return True
            
    def showEvent          (self,e):
        
        super(controlweightvertex,self).showEvent(e)
        e.accept()
        self.switchview()

