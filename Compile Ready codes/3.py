"""Clones a remote git repository (makes a local copy)
    Inputs:
        URL: Address of the remote git repository (GitHub link)
        location: Location that is used to store the cloned git repository
        user_name: The username used to sign git commits by Githopper
        user_email: The email used to sign git commits by Githopper
        clone: Triggers the git command (Button)
    Output:
        help: Helpful tips about the git oporation"""

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
            "Clone Repository", "Clone", """Clones a remote git repository (makes a local copy)""", "Githopper", "Beginning")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("2350aed6-c8b1-42f3-bc14-3112e961848c")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "URL", "URL", "Address of the remote git repository (GitHub link)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "location", "location", "Location that is used to store the cloned git repository")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "user_name", "user_name", "The username used to sign git commits by Githopper")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "user_email", "user_email", "The email used to sign git commits by Githopper")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "clone", "clone", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        p4 = self.marshal.GetInput(DA, 4)
        result = self.RunScript(p0, p1, p2, p3, p4)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIESURBVEhLxZVBSFRRFED/wkAsUoQKsmVFgbhKQqKFiZsEFxaZEbkKKhAsLGgRBILUtpViULhwlUEQVJuwNkqEuIjKRdYqKKVFuChC65w3Pmaa/2eacqADh/n3zZ9733/3vzfJ/+A4juM9vImtWBXq8Rn+zPA6RjbhfjyKR3AHRmrWPzOZxgW8hk/QJ3iIl9EiZ1Ga8Sq+Rse/4hW8hCcwk8PozS5NFib5jLUhymPxHxifNE4ihUvgDV0hSnMH/b4lRL8zhbHAkANZ2ExvaA9RmlH0+4MhynMIZ/ANvseLmMlpXMUHaLML2Ycuz3fc5kAJbL5m0oivcBKfoo2UAVxBZz/mQAE78RGeD1EFdONzHMHtDsAwmvwFbnVgHZMv4iz65L5FFdGGLtPuECXJGbyFm0OUowmX0aJiH5xExUXKsQs/4ku0qRfQnnXihouY3JnfD1GS3ECTuvtlQ0WKk8te/IImtX/SgX9dJCt5ZA4fo0l7HADPJ2N3+R/xvf+AEyFKYx/cnO4jk9qbLejR8w3PYVn2oD/sC1EaCxzLXSaf0HtdOnFz3s5dlifOzs9i3mEs4I4/gHXo0WHzva4I90NxkQZcwsEQ5XmLbsCSx0Yp+rGwSIz9DxHX/p+TR+KTnEQf/y76J1OV5JE4894Q5aha8kgs4kk6j1VNHjmFa+jxXiJ5kvwCY+uA63XPUxoAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, URL, location, user_name, user_email, clone):
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            """
            
            try:
                Popen(["cmd", "/C"] + cmd)
            except:
                pass
        
        def executor_alt(cmd):
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
        
        def clone_repository(repository_address, user_name, user_email):
            """
            Clones the remote repository from it's address
            """
            
            a = executor_alt(["git", "config", "--global", "user.name"])
            b = executor_alt(["git", "config", "--global", "user.email"])
            
            if user_name and user_email:
                creds = ["git", "config", "--global","user.name", user_name]
                creds += ["&", "git", "config", "--global", "user.email", user_email]
                executor_alt(creds)
            
            if a and b:
                executor(["git", "clone", str(repository_address)])
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        if clone and URL and location:
            if not os.path.exists(location): os.mkdir(location)
            real_location = os.getcwd()
            os.chdir(location)
            clone_repository(URL, user_name, user_email)
            os.chdir(real_location)
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the clone button to clone the remote repository\n"
        
        if not URL:
            help += ("\n* Please enter the git url."
                      "\n  For example:"
                      "\n  https://github.com/account/Project\n")
        
        if not location:
            help += ("\n* Please enter the location."
                      "\n  For example:"
                      "\n  C:\\Projects\n")
        
        if not (executor_alt(["git", "config", "--global", "user.name"]) and executor_alt(["git", "config", "--global", "user.email"])):
            help += ("\n* You must enter a user_name and user_email for the first time")
        
        return help


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Clone Repository"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("5cfdde34-e805-43e2-a474-289b9f86f574")