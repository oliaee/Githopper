"""Initializes the git repository (git init equivalent)
    Inputs:
        name: The name of the created branch
        create: Triggers the git command (Button)
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
            "Create Branch", "Branch +", """Initializes the git repository (git init equivalent)""", "Githopper", "Branching")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("5925fe4c-66e3-4357-a0ad-64e409297401")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "name", "name", "The name of the created branch")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "create", "create", "Triggers the git command (Button)")
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
        result = self.RunScript(p0, p1)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIASURBVEhLrdVPSBRhGMfx0Uyi8pLRKaE0MCg8KeQ5CaJCkDxoal0jukmgCOFNUjpEGRQFQofoFglC1KEOKkVSireCLqZFSBT901C/v3nnGWfX2Z032B984H1m333fmdmdZ4KUbMMh7A2rEucMFrAeuYFylCQN0KJPcBK9UT2MkuQeFt0wzlWsYVdYbUa38SIeYQS1yMw43rhhnLPQVVSHlUslnkHHZ/Edf9CEorkAfelEWAXBHsxhBmU6EOUyNK85rNzV6cTmkZy3JfrwIfTlV/iELziCZJ5iyg3j2JXqpIpmO5ahydKD/NzBZzeMcw1/sSOsimQnlmAbnEN+6rEK/dvaMADN7UdmdkNnZxt0Iy3HYXNkFF7x3UAPn34fm3caXvHdYB9+w+apA3jFd4NLsDlyGF7J2qAGV6AHy+a8g3e/yt+gE8oQXuMn7DPTCu/kb9AFRf/x5KKmD/8VPfZpt+gb7Ng/qBe1IJkxDLph4ahdfIUt1gFlGrdxHnrQ0jKJ+25YOLeghd/jBz7gACqQFnVWXbW8hFq+1Wo7OWmHnbX6vRb+iBcolOtQuxbdupVErfdFTh7jrRvG0WbatFCXPIpTEb0bJhL1QeTkAXTGydhrsyqsiuc5brpheo5Bi+k+NkJ/UdV34RP9Bplz9Vb7BS0segFl9vgoddjvhpYg2AAgGZq3nDfvtQAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, name, create):
        
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
        
        def create_branch(name):
            """
            creates a branch with the given name
            """
            
            cb_msg = executor(["git", "branch", name])
            
            return name
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if create == True and name != None and not(name.count(" ") or name.count("\n")):
            r = create_branch(name) + " created"
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the create button to create the new branch\n"
        if not name: help +="\n* You need to enter a branch name first\n"
        try:
            if name.count(" ") or name.count("\n"): help +="\n* Branch name can't conntain spaces or new lines\n"
        except:
            pass
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_9"]
        except:
            rsc.sticky["Githopper_9"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_9"] == None:
            rsc.sticky["Githopper_9"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_9"]
            rsc.sticky["Githopper_9"] = None
        
        return (report, help)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Create Branch"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("9e5fbcda-97b6-4dbc-b35e-472186ba0094")