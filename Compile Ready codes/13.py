"""Selects files in the working directory
    Inputs:
        indexes: Indexs of the selected files inside the directory (int list)
        select_all: Determines whether all files should be selected (Toggle)
    Output:
        files: Selected files
        directory: List of all the files inside the current directory"""

__author__ = "Amir Hossein Oliaee"
__version__ = "2019.06.24"

from os import listdir, getcwd
from os.path import isfile, join
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Select File", "Select File", """Selects files in the working directory""", "Githopper", "Committing")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("87a30863-64e1-400a-bee4-ae5318fc4aeb")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "indexes", "indexes", "Indexs of the selected files inside the directory (int list)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "select_all", "select_all", "Determines whether all files should be selected (Toggle)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "files", "files", "Selected files")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "directory", "directory", "List of all the files inside the current directory")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFeSURBVEhLxda9LwRBGMfxEYVONFQaCZWXgkanEK8NBYcgEcR7o+MPEFpC6x9QSpQq0aIRhYJOoqXm+5szyVnP2h17iV/yye2zmblndye3c+6/UsIZLiNo/CQys4+PAvaQmi5o0D260RihBw/Q/A6YWYUGLPgqPkvQ/GVfGdmABmgN/pIZaL4u1Mw6NEADlVHs5DACZRaav+IrI6HBlK+ce4LqLI9Qwh1kNgh30IbBHFqhzCGqQWwWoflbvjKSfEQXeM/hHEofXhHW5EdCg2lfOXeCW9xkOEJIw9enmaKPKDPJBgPYNqyhHtFJrsEzVFv0G4lO8g7aMW4YQh2iU6012EVv+fB7qtFgAvqOTl8lUrRBCzRfTcxsQgPyvk37MVw+dLXQu+vYVymJ3Q/mofHNOMUdfk3ljqYdqnLH0hVaOcQbXtCkE1lJ25OvUAMr1xgrH+aL9a/iAGkNUs479wkCEpLaMnJeZQAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, indexes, select_all):
        
        files = None
        directory = None
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        mypath = getcwd()
        f_list = listdir(mypath)
        
        try:
            f_list.remove(".git")
        except:
            pass
        
        if len(indexes) == 1:
            indexes = indexes[0].split("\n")
            indexes = [i.strip("\r") for i in indexes]
        
        temp_list = []
        for i in indexes:
            try:
                temp_list.append(int(i))
            except:
                pass
        indexes = temp_list
        
        files = []
        directory = []
        
        for f in range(len(f_list)):
            if isfile(join(mypath, f_list[f])):
                if f in indexes:
                    files.append(f_list[f])
                    directory.append ("> " + str(f_list[f]))
                else:
                    directory.append ("  " + str(f_list[f]))
            else:
                if f in indexes:
                    files.append(f_list[f])
                    directory.append ("> " + str(f_list[f]) + " (dir)")
                else:
                    directory.append ("  " + str(f_list[f]) + " (dir)")
        
        if select_all:
            files = ["-A"]
            directory = ["> " + str(f) for f in f_list]
        
        return (files, directory)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Select File"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("abd7cef7-52a2-4ba2-9077-0751f03a2c13")