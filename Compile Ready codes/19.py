"""Reverts the selected files to the selected commit's state
    Inputs:
        commit: Selected commit to revert the files state to
        files: Selected files to revert
        revert: Triggers the git command (Button)
    Output:
        report: Output of the git operation
        help: Helpful tips about the git oporation"""

__author__ = "Amir Hossein Oliaee"
__version__ = "2019.06.24"

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Revert File", "Revert", """Reverts the selected files to the selected commit's state""", "Githopper", "Committing")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("31ba183a-aab7-4305-a4cd-a800a0c4e877")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "commit", "commit", "Selected commit to revert the files state to")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "files", "files", "Selected files to revert")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "revert", "revert", "Triggers the git command (Button)")
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
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFaSURBVEhLxda9LwRBHMbxEQWVaBR6GkRBRKkQhErj5UIhiHeFTqIWOonEXyE0EqVKTyUkCmq1mu8za5LN7uzOjEt4kk9uf8lvMjs7dztn/ivzuMRdAvXPIZgTfDXhGJUZhJqeMISuBMN4hsYPwJtNqGHFVulZg8av28qTHahBe/CbNKDxulFvtqEGNSozOIwwDWUJGr9hK0/cBAu2MuYNqkNeobgVBCdwK+jFZIQeKMtImiA1q9D4PVt5UnxEt/iMcANlDB9we1KKm2DRVsZc4BEPAedw6fz59KbZRxRMcYIJHHhsoQPJKe7BO1T76DeSnOIK+jHrMYU2JOfP9yA2+xjJLuuTOoEe0xE0RgeO9q4VldmFmmPfpuNQf94LuuFN6nmgu9XXVmPOoNf9Fa7RjlLyJ5pOqPyJVbd0vXtGs0sbvTL6sstyqs7ke7QgNrV74ftXcYqUCYgx37zrk+qH0M/bAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, commit, files, revert):
        
        report = None
        help = None
        
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
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if revert and commit and files:
            if files[0] == "-A":
                r = "You can not revert all files (you can use \"hard reset\" component for that)"
            else:
                r = ""
                for i in files:
                    try:
                        temp = executor(["git", "checkout", commit, str(i)]) + "\n"
                        if temp != None or temp != "":
                            r += temp
                    except:
                        r += "Could not revert " + str(i) + "\n"
                if r == None or r == "":
                    r = "revert oporation finished"
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the revert button to revert the selected files to the selected commit state"
        if not commit: help += "\n\n* Please first enter the commit"
        if not files: help += "\n\n* Please remember to add the file names"
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_19"]
        except:
            rsc.sticky["Githopper_19"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_19"] == None:
            rsc.sticky["Githopper_19"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_19"]
            rsc.sticky["Githopper_19"] = None
        
        return (report, help)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Revert File"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("7cc08d6e-682a-46f7-b9fa-f6e82d3fac39")