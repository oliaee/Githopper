"""Changes the git working directory from the current location
    Inputs:
        path: The working directory path to be used by git
        create_path: Determines whether the given path will be created (Toggle)
        set: Triggers the git command (Button)
    Output:
        report: Output of the git operation
        help: Helpful tips about the git oporation"""

__author__ = "Amir Hossein Oliaee"
__version__ = "2019.06.24"

import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Git Path", "Path", """Changes the git working directory from the current location""", "Githopper", "Beginning")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("504cb3de-8ebc-42d7-a745-4554f35f0cb4")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "path", "path", "The working directory path to be used by git")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "create_path", "create_path", "Determines whether the given path will be created (Toggle)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "set", "set", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "report", "report", "Output of the git operation")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIESURBVEhLrZVLqE1RHIePROT9GsijPMLAwCMMTJQMRMrAxEjI9E6UcG8uA6KYIQxEMmPAiJkBEqIwMJDbLdQVA+/cXL7vv85u3845d+9znPPVV+u39jlrr7X2elSaZApuwW48g4dxM07CthiPJ/AX/sXf+BkHq/kHHsWx2DKL8DXa0FlcjRNwFE7EtXgBff4C52HTzMIPVVdYUcAa/IR9ONWKZriDP7G2V45iG66MlLMY/+DNSCWsR4e9M1JiCT5G6zMf4ALM2IfW24lCruPHVAym43t0urajL9uBTstbnIwyGr/gxUgF2NiVVAyOoT2bHynHF1l/IFLCKXqTio1xWboED0ZKPMF7qVhH7bPj+B0dTUPGoWu9J1LCuX6UinW8xLupGJzErzjiC8R5vZGKQRc6Fesi5WxA6/dGSrj6XqXiyJxDh5ntTkflVNiYR8VW7K3m+zgGxU3o6E9FKmA5+uf9kRJuoGtofeZlHH4WHUHr3ROlXMUhnB0pZyYuwxmRcuaijZcu0Yxp6EF2O1I5/s5pzfZEU+xCe+UxXcQm9He7I7XIQxxAP3QjXI79+CzSf7AU7d3pSPUcQp/XHn4t4e60EVfXcOag9ZcitYHr/B0+jZRzC10IXqdtk31Ij2TZiOY9kTqEx4cH4UL0xHyOHcVr9Bt6L9j7VdhxslvrfKRSKpV/IC50TXykfQYAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, path, create_path, set):
        
        report = None
        help = None
        
        if set and path:
            if (not os.path.exists(path)) and create_path:
                os.mkdir(path)
            os.chdir(path)
            rsc.sticky["git_path"] = os.getcwd()
        
        help = "Press the set button To set the git path\n"
        if not path: help+= "\n * You need to first enter a path\n"
        if not create_path : help += "\n* If the path doeasn't exist, you can use the create_path option"
        
        
        report = "The current working directory is:\n" + str(os.getcwd())
        
        return (report, help)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Git Path"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("83a36366-0f10-46e0-863e-47cec8e42a54")