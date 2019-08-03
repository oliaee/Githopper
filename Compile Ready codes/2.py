"""Initializes the git repository (git init equivalent)
    Inputs:
        user_name: The username used to sign git commits by Githopper
        user_email: The email used to sign git commits by Githopper
        initialize: Triggers the git command (Button)
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
from subprocess import check_output, Popen
import subprocess
import os
import scriptcontext as rsc

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Create Git Repository", "Create Git", """Initializes the git repository (git init equivalent)""", "Githopper", "Beginning")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("fae82167-2de3-4054-9be4-c10a5509d306")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "user_name", "user_name", "The username used to sign git commits by Githopper")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "user_email", "user_email", "The email used to sign git commits by Githopper")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "initialize", "initialize", "Triggers the git command (Button)")
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
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGdSURBVEhLzdXNK0RRGMfxm9ciRTZey1tYKH8AshKxsvUfWChZKsrWwsqKKAsLa6/lpVCKjbKwtRIRC5LyEt/fOffkds3NTGem/OqT81zT85w5M/dO8J/ShXy7zG7ysI0vHKIYWYt2vI5bDOMBJ8jKEDXfhXY+ogukGo/wHqLme7jHKu4whSo0wmuImu/jBS26QC6hd7JhKo8h0ebtuhBmDBrwiW5dIBkPSWqu1OEZp9CgHig1SGtICTahb0m8udKKdzRjAa9YQy0acIMDlCFleqGdDZjqdzRA/9df5Q2qZ01lj031oKlSRJO1g2vobONxAzpNFQQT2EITdExX0DGVIzE6Q71IZxofUg8NaDPVTyqh4zlHqS78laQh49CASVPZaOcZNXdJNWQHGnBsKo/mLvEh+rZMh2vv5i7RIXoGKRVIar6CGbtMP26I7o9+6FuWtHO9btkuM4uG6HdAn8EZos2LoFqOsBSpC5F2CtAHDYtmDk+hD+gGdPUovNOBodAF9Mvn6vi95B09KOftMjfRZ7Bol7mJnrR6rEcSBN/Rl2f8RlX+tgAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, user_name, user_email, initialize):
        
        report = None
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            """
            
            try:
                out_put = Popen(["cmd", "/C"] + cmd)
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
        
        def init(user_name, user_email):
            
            if user_name:
                executor_alt(["git", "config", "--global", "user.name", user_name])
            if user_email:
                executor_alt(["git", "config", "--global", "user.email", user_email])
            
            cwd = os.getcwd().split("\\")
            if cwd.pop() != "System":
                executor(["git", "init"])
            else:
                return ("Error: The repository could not be created\n"
                        "\n* Please use the \"Git Path\" component to specify the path "
                        "for your local git repository")
                
            if os.path.exists(".git"):
                init_msg = "The git repository initialized successfully"
            else:
                return ("Error: The repository could not be created\n"
                    "\n* Please make sure you have done the following:\n"
                    "1 - Install the Git software from www.git-scm.com\n"
                    "2 - Set Rhino to Run as Administrator if you are using the C drive")
            
            return init_msg
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if initialize:
            r = init(user_name, user_email)
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the initialize button to create the new repository\n"
        if not user_name: help +="\n* You need to enter a user_name first\n"
        if not user_email: help += "\n* You need to enter a user_email first\n"
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_2"]
        except:
            rsc.sticky["Githopper_2"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_2"] == None:
            rsc.sticky["Githopper_2"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_2"]
            rsc.sticky["Githopper_2"] = None
        
        return (report, help)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Create Git Repository"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("24ef3996-a7f9-4078-8726-233554d025f0")