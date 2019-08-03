"""Modifies the last commit
    Inputs:
        files: List of the selected files
        message: The new message to replace the last commit's message
        modify: Triggers the git command (Button)
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
            "Modify Last Commit", "Modify", """Modifies the last commit""", "Githopper", "Committing")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("82f9bb62-e543-434c-8bc3-e2251024c695")
    
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
        self.SetUpParam(p, "message", "message", "The new message to replace the last commit's message")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "modify", "modify", "Triggers the git command (Button)")
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
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFFSURBVEhL7dXNK0RRGMfxK3mZ8rJRrMwo2fgHLK1shWhSyqysbGwsWWAhpZS1DQv+AdnIAmU1aYRiqyyUl2IlfH9jnjpuh2nuHAvlV5/udO5znts8c2Ym+s+fSReWcIRzHGIBaVSdcTzi3eMeo0icAfgax/UjUa5hTQoYQi9GoFHZvQv8mAZoFJMOzdga3KANbtpxC6uZh7s/izoUo81W6LMCX9bgq5dXtKKYcg+Ygy+L8NXLlwc0YR0bjj1YcR6+nMFqduHu17tL4dvU4wHWYBOdqEUG27B7d9B6xZmGNZFnXOHFWZMpJM4q3GZxy6g6wzjAE95K130MIh6NtvnzZeXR2e8pXX3pgE7cLLq1EDItOMUlZjCGYFHzY9jnohPWiCDRl8ltvoVg0dk/wa80V/qwAxtL8ExA/3Q51GghdMr8PETRB7zNgYOR3npxAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, files, message, modify):
        
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
        
        def amender(msg, f=[]):
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
            
            if msg == None or msg == "":
                commit_msg += executor(["git", "commit", "--amend", "--no-edit"])
            else:
                commit_msg += executor(["git", "commit", "--amend", "-m", msg])
            
            return commit_msg
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if modify == True:
            r = amender(message, files)
        
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the modify button to modify the last commit\n"
        if message == None: help += "\n* You can change the last commit's message by entering a message"
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_15"]
        except:
            rsc.sticky["Githopper_15"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_15"] == None:
            rsc.sticky["Githopper_15"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_15"]
            rsc.sticky["Githopper_15"] = None
        
        # return outputs if you have them; here I try it for you:
        return (report, help)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Modify Last Commit"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("f1cf55d9-848d-4dd3-a60a-3b9d3ef3d092")