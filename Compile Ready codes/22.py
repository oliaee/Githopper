"""Pushes the local repository changes to the remote repository
    Inputs:
        branch: Name of the branch to be pushed
        repository: URL Address of the remote repository
        push: Triggers the git command (Button)
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
            "Push to Repository", "Push", """Pushes the local repository changes to the remote repository""", "Githopper", "Merging")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("97deeaa3-1d5d-4c69-849a-17b1113837e1")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "branch", "branch", "Name of the branch to be pushed")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "repository", "repository", "URL Address of the remote repository")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "push", "push", "Triggers the git command (Button)")
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
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGiSURBVEhLrdTLK4RRHMbxIZdsEFI2bmUrRSRlp7Cxlo0s/AtioWzcosTWhigZyXUhkQUWVi65lCg7e8klt+/zvu/hTdM7Z2bepz6d95w558w70zm/SBLJ8NpQ0455nOHea+fQipRSjG18B1hHIRKOFl0h1qb/nSMfCWUVWjyBZqxBbzuLDejzJsxA85ZgnUaYt+vTQEAGYebWacAm5q0+0aaBgHTgC5qvX2uVA2jBjdOLnzto/q7Ts8gJtEDH0SbX0Pwjp2eRHWjBM4o0EJASvEDzNzVgkyFogUSRjljRrV6EmTsAq1RBC6ZxjAcMIxtKDnR6LmA2f0cZrDOOV+jo6YxPwvwStbpcZnPRFyYc/ac6SZ2o0YAv5iLKggaSzSi0yaHT+8sentDv9FJMOWrdx9+oX+o+hpsWrw09qq5b0N+lYleA0FIPUw4evfYW1sUtKD1Q0dOmI1DdH/P6H+hGUtFZ10XTRroPOqr+dOEN+nwKabBOJUxFvUQ1YkV3wxS6fVQgbrJgSsAychGUPKxA80+RibhpQK/7aB3N12HwJRL5AetketrxxHLdAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, branch, repository, push):
        
        help =None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                Popen(["cmd", "/C"] + cmd)
            except:
                pass
        
        def pusher(options):
            """
            pushes repository to server
            """
            
            executor(["git", "push"] + options)
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        push_options = []
        
        if branch == None or branch == "": push_options.append("--all")
        
        if repository == None or repository == "":
            push_options.append("origin")
        else:
            push_options.append(repository)
        
        if branch != None: push_options.append(branch)
        
        if push:
            pusher(push_options)
        
        # Help production area ---------------------------------------------------------
        
        if branch and repository:
            help = "Press the push button to push the selected branch to the selected remote repository\n"
        elif branch:
            help = "Press the push button to push all branches to the selected remote repository\n"
        else:
            help = "Press the push button to push all branches to the remote repository\n"
        
        return help


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Push to Repository"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("9f63defb-ecd6-41a1-8064-b4aa4df051af")