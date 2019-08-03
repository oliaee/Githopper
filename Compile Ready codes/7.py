"""Lists all the branches in the local git repository
    Inputs:
        check: Refreshes the List (Button)
    Output:
        branches: List of all the branches in the git repository"""

__author__ = "Amir Hossein Oliaee"
__version__ = "2019.06.24"

from subprocess import check_output
import subprocess
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
            "Branch List", "Branches", """Lists all the branches in the local git repository""", "Githopper", "Branching")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("103f8be5-992a-4026-8a1c-af7c4790d05a")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "check", "check", "Refreshes the List (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "branches", "branches", "List of all the branches in the git repository")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGoSURBVEhLzdRLKAZRGMbxkZAUK7dERMglZcGCpKQICWVBVoqiLCwUyUoSxcrGRinZC8mejaIol+QSIRbkHin+zxzKcs5nvvLUr94z03fmm3PeM85/TTwKTOl/ynGDWywiEr5mB0OIwh3aEHCK0I4Yd2Syhmnk4hHVCCj64TOusY9YKFk4wAcmdIGkINqU3rOFKVO6kzWZ0k0LdF+ZxSv0Ryp1wWuGcYFJaK3jkIdsDEBLlY9PpGEEe/CcEIxCE1RgHE/Qw95Qh2Tofj3msQ6rJOEErbhHOjK+60IoHdBDdpGpCzbRhp5hEL9f/xxq1Sp3ZJar15R20SE6xhwOsYJtPECbqj1SIyxhDNbR5mmztUzqFC2FxuoineZ+6G10vwdWycEVdAZWoSXQwSqGsgC17zJ0XlJhFU14iTJoonBoH37Og9pVb6TJO3XBNuqgTagldWLVtqeohTID7UupOwowYdBbdLsjxzlCA/qgf6/v0Z/TDE2miTfwAj2oBL6lC2rNd6j/Q+F7EqHW1GcjaFG/N5oyONGG//5s+x590GpMGZwkIMKUXuI4X1acZKfIe0wWAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, check):
        
        branches = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def branch_list():
            """
            Returns a list of existing branches
            """
            
            branch_list_msg = executor(["git", "branch"])
            
            return branch_list_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        
        branches = branch_list()
        
        return branches


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Branch List"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("7621f75a-d0b3-4045-b211-ea7c842928ee")