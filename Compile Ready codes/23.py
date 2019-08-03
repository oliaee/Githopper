"""Forcefully Pushes the local repository changes to the remote repository
    Inputs:
        branch: Name of the branch to be pushed
        repository: URL Address of the remote repository
        force: Triggers the git command (Button)
    Output:
        help: Output of the git operation / Helpful tips"""

__author__ = "Amir Hossein Oliaee"
__version__ = "2019.06.24"

from subprocess import check_output, Popen
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
            "Force Push", "Force", """Forcefully Pushes the local repository changes to the remote repository""", "Githopper", "Merging")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("0270722b-cc28-4415-b95e-a2a0b7f5f3c2")
    
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
        self.SetUpParam(p, "force", "force", "Triggers the git command (Button)")
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
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIYSURBVEhL7dVLSBVhGIfxKU2MsNI2ZffosolIiBQXdm8RigTZhUishW3cuBKhRUt3hitdFS3DqGgXoeVCxIgCkaTbSqJlpEFiUc9znA/mTGPH1GV/+HFm3vnmPTNzvm9O9D//kn14gbO5vT+zAxfRFn9uR1bOwT57cnuJ1GAWv3DJQpzV6MMMPBZ8Ry9KEXIZHnPsYQvpHMBnOCjcyRCSjdMGYbxy9z9hv4X5shcPsBk34Uk+kqPowNX4sw7him9gKzxvNxaUMkzDBkcsZOQ4PP4VayxkxWfYgzsJ61ELT55AEbJSjHdwXDUqkOxzC9FaTMFBwRacjLdH8be8hOOOwZmV7PMF0Qpsgs9cbptDcNBPzDclt+EbHFdlgSR7bbSQFa/G25/EKwzDqesjMOVowGvY/AN8jJ5XMP4enlSPC3iLdjxHmCEH4ZjgDBrj7W5kxqu6Cwc9QSWMi2wAnXDRGW8/NO+yQKw9hbXbsF9eTsOD95GeNdfh47CJ8cv9UtdHMj7Wh7DPCQvp+CUOWkpWwT6Lzqn4c9mzAY/h7T9CmFHLEt+MH2Hz4D1cK0vONbjYbOp6cHsk3v+BFiwqKxHWhO9+53p4ffgjuk7Cf4TvHN8IC84uPIMnj8P/CdMEa+dze3ML7g2sOW13omBKMAZPugdfhiE2tu4KD1mHflh3rThNC8ZXb+vcZl6uwEbNub38OD71NxlFvwFUSYtnC9WIiQAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, branch, repository, force):
        
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                Popen(["cmd", "/C"] + cmd, creationflags=0x08000000)
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
        
        push_options = ["--force"]
        
        if branch == None: push_options.append("--all")
        
        if repository == None:
            push_options.append("origin")
        else:
            push_options.append(repository)
        
        if branch != None: push_options.append(branch)
        
        if force:
            pusher(push_options)
        
        # Help production area ---------------------------------------------------------
        
        help = ("Press the force_push button to replace the remote repository with "
                  "your local git repository"
                  "\n\n* Warning: this component is dangerous --> It will completely "
                  "wipe out the git history of your remote repository !!!"
                  "\n\n* This component will not effect your local repository")
        
        return help


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Force Push"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("632f7681-3a28-485d-a6b6-7e164009d476")