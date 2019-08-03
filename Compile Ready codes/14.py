"""Commits the changes to the selected files
    Inputs:
        files: List of the selected files
        message: commit message
        commit: Triggers the git command (Button)
    Output:
        report: Output of the git operation
        help: Helpful tips about the git oporation"""

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
            "Commit Changes", "Commit", """Commits the changes to the selected files""", "Githopper", "Committing")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("d4a9b289-3f73-4888-a8c9-37d4717c2905")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "files", "files", "List of the selected files")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "message", "message", "commit message")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "commit", "commit", "Triggers the git command (Button)")
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
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFCSURBVEhL7dVNKwVRGMDxKSG5ZaNs5CV1N3wIKxsLISUrO1n4DK7CQqLESkjZ+ASyIAnbW9eNBVtlobwUCwn/55559JgOMi8L5V+/7pmZM2e6c2e6wX9/pnbM4hhnOMI0WpG4EdzjzeMWQ4hdD3wLR3UjVpfQRU7Rj04MQm6VHjvHt9VCbsWoIfdYF7hCI2xNuIbOKcCeP4xqVJKTdaLPPHwtwTdfvKABlX66wCR8zcA3X3y6QA4r2DB2oZOL8FWGztmBPV++XR2+rAZ30AW20IIqtGEbeuwGsv/XTUAXEY+4wJPZJ8YQu0XYxaLmkLgBHOABr+HnPvqQavLs58PPaJuYcsNsOsG6G6aXPGn1oUOsme2PtzhJC5DfQ8iL9Wy2x5G4LvSGSpCXTbflPyTV9rDshtkkv8GqG2ZTB5rdUAuCd53UgEObnuwGAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, files, message, commit):
        
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
        
        def commiter(msg="No comment", f=[]):
            """
            This function saves the selected portion of the gh file from clipboard
            and commits it with the given massage
            * files: a list of file names that will be committed
            * if files contains "-A" then all files will be committed 
            """
            
            commit_msg = "" 
            
            for i in f:
                try:
                    executor(["git", "add", str(i)])
                except:
                    commit_msg += "Could not add" + str(i) + "to the repository\n"
            
            commit_msg += executor(["git", "commit" , "-m", msg])
            
            return commit_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area + help ------------------------------------------------
        
        help = "Press the commit button to commit the changes (to the selected files)\n"
        
        r = None
        if message == None or message.startswith("Double click"):
            message = "Commit message not specified"
            help += "\n* Are you sure you don't want to leave a message ?!\n"
        
        if len(files) == 0 or files == None:
            files = ["-A"]
            help += "\n* All files will be committed"
        
        r= None
        if commit == True:
            r = commiter(message,files)
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_14"]
        except:
            rsc.sticky["Githopper_14"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_14"] == None:
            rsc.sticky["Githopper_14"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_14"]
            rsc.sticky["Githopper_14"] = None
        
        return (report, help)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Commit Changes"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("12e52e31-d58f-4f35-aec2-ccbedf096688")