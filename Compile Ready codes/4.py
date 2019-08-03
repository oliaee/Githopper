"""Sets/Changes the address of remote repository for git
    Inputs:
        URL: Address of the remote git repository (GitHub link)
        replace: Determines whether an existing remote address could be replaced
        set: Triggers the git command (Button)
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
            "Set Remote Address", "Remote", """Sets/Changes the address of remote repository for git""", "Githopper", "Beginning")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("3dda517f-a117-42e2-8bf0-a4b2d6a53925")
    
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
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "replace", "replace", "Determines whether an existing remote address could be replaced")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "set", "set", "Triggers the git command (Button)")
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
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFySURBVEhL7dW/K0VhHMfxk+GSgSgZDAYMbAzCzIRFKWWwCJNNKUYGJf8CiZj8GE12MwOrKL/y22DA+1PnW0+355zzHO6k+6lX5z7f+3yf7u1+z7lROaVOLRrja8nSgiWc4A6v8VXrZbTi11nAO75TfGARubMN34FJdhCcVajpCpt4iNfFVN/AdbxeQ2a6YQesq0CaMIkB6H1dtVZd0T7r6VEhLXuwzYcqBGQf1nOgQlLq8ALbPI2QTMF6NGX18KYXtvEWVQhJJW5gvX3wZhC26UKFHDmH9Q6p4Es/bNMTQu/YGjzCejUE3uiu/IJtHENIRmE96m+DNxU4hTZ+4g1ZY6f37T6QM+icxMxCG+ewFb8+wgTcjENj7H5jUX9qCtCneEYzdqHRm4GbebgHi/o0UZlphx5ix9DjuQHF0aS4h+tH7kBwOqFnkZo148NwMwI7XCPdhdzR+K3gHjrQje6ZS+g/4c9/QNXQb+NGa9X/daLoB/OXg/hnM6GqAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, URL, replace, set):
        
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
        
        def change_origin(url, r=False):
            co_msg = executor(["git", "remote", "add", "origin", url])
            
            if r : co_msg = executor(["git", "remote", "set-url", "origin", url])
            
            return co_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if str(URL).endswith(".git") and str(URL).startswith("https:") and set:
            change_origin(URL, replace)
            r = "The remote address is as follows:\n" + executor(["git", "remote", "-v"])
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the set button to set the remote repository address\n"
        
        if not URL:
            help += ("\n* Please enter the git url."
                      "\n  For example:"
                      "\n  https://github.com/account/Project\n")
        
        if not replace:
            help += "\n* If you want to allow git to overwrite old remote addresses, set replace toggle to True\n"
        else:
            help += "\n* The old remote addresses will be overwriten\n"
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_4"]
        except:
            rsc.sticky["Githopper_4"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_4"] == None:
            rsc.sticky["Githopper_4"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_4"]
            rsc.sticky["Githopper_4"] = None
        
        return (report, help)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Set Remote Address"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("b4cb7cab-2bc0-42e3-8cb2-79bf58cd50fa")