"""Pulls the remote repository changes to the local repository
    Inputs:
        branch: Name of the branch to be pulled
        favor_this_side: Determines whether to resolve conflicts by favoring this side of the pull (Toggle)
        manual_resolve: Determines whether to leave conflict solving to the user (Toggle)
        pull: Triggers the git command (Button)
    Output:
        help: Output of the git operation / Helpful tips"""

__author__ = "Amir Hossein Oliaee"
__version__ = "2019.06.24"

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
from subprocess import check_output, Popen
import subprocess
import os
import scriptcontext as rsc

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Pull from Repository", "Pull", """Pulls the remote repository changes to the local repository""", "Githopper", "Merging")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("97c47f69-1430-4e51-847d-aa5a6d106e11")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "branch", "branch", "Name of the branch to be pulled")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "favor_this_side", "favor_this_side", "Determines whether to resolve conflicts by favoring this side of the pull (Toggle)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "manual_resolve", "manual_resolve", "Determines whether to leave conflict solving to the user (Toggle)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "pull", "pull", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Output of the git operation / Helpful tips")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        result = self.RunScript(p0, p1, p2, p3)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGjSURBVEhLrdXLKwVhHMbxQy5ZiHIpKWyspBQlKckKGyvJVtnZi4VSbokNWxui1Cm5S1IWSMoCuWzc/gaJlMv3mZmXk46Zd845T32aeX/n/c2ZOb3znkgCyfCOKU07FnCOe+84j1YklWJs4cvHGgoQOmq6RryL/nWBfITKCtQ8hSasQnc7h3Xo80bMQvOWYZ0GmLvrV8EnQzBz61SwibmrD7Sp4JMOfELz9bRWOYAabp1RcO6g+XvOyCKnUIOWo01uoPlHzsgiu1DDCwpV8EkJXqH5GyrYZBhqkCjSES96q5dg5g7CKpVQwwyO8YQxZEPJgVbPJczF31EO60ziDVp6WuPTME+io14uc3HRF4aOflOtpG7UqBAT8yLKogqJZgK6yKEz+s0+njHgjJJMBWrd059oXOaehk8pmt1T62i+lmxgsqAXTD/LqAoWGYfmnyFTBb+koQUPUNMm/nvZirADzdN2oadQv1XUvA0161+sHrHRjvuIoJsIjHl86VGB9MLURlRINl0w+82Jd9Q+1YmUpRpX0MW1RVQh5clDH3KdUWAikW894HrsUOMkFAAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, branch, favor_this_side, manual_resolve, pull):
        
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                Popen(["cmd", "/C"] + cmd)
            except:
                pass
        
        def puller(options):
            """
            pushes repository to server
            """
            
            executor(["git", "pull"] + options)
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area & help ------------------------------------------------
        
        if not manual_resolve:
            help = "Merge conflicts will be resolved automatically\n"
            if favor_this_side:
                conf_manager = "--strategy-option=ours"
                help += ("\n* In the case of a conflict it will be resolved"
                           " by favoring this side of the conflict")
            else:
                conf_manager = "--strategy-option=theirs"
                help += ("\n* In the case of a conflict it will be resolved"
                           " by favoring the other side of the conflict")
        else:
            conf_manager = "manual"
            help = ("Conflicting files will be altered\n"
                      "\n* You have to manualy edit the files and resolve the conflicts"
                      "\n\n* After manualy resolving the conflict make sure to use "
                      "\"Finish Conflict\" component to either resolve the merge conflict"
                      " or abort the oporation")
        
        pull_options = []
        
        if branch == None or branch == "": pull_options.append("--all")
        
        if conf_manager != "manual":
            pull_options.append(conf_manager)
        
        if branch != None: pull_options.append(branch)
        
        if pull:
            puller(pull_options)
        
        return help


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Pull from Repository"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("2373329f-ac19-43ab-8b71-c8b09ce3e906")