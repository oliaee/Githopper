"""Lists all the commits in the local git repository
    Inputs:
        check: Refreshes the List (Button)
    Output:
        commits: List of all the commits in the git repository"""

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
            "Commit List", "Commits", """Lists all the commits in the local git repository""", "Githopper", "Committing")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("47998cf2-1c23-41cc-b9b3-7a0d5903cb1d")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "check", "check", "Refreshes the List (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "commits", "commits", "List of all the commits in the git repository")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAG1SURBVEhL1dU5SB1BHMfxjUcRg1iosdIoBkTBwlpUvC0tJGoiJATBAy0NYpdYWNlYKmgr4tWLgoKBRMVCSYpESTSgkiJ4JhYav7/ZebCI7wDnFf7gw5v/MDuzu2931ntoSUQunpjKcRrwA/9xjE44Sz4u8R3vsAwtVAsn6YUm1O0J5QzTfvP+GYUWKDCV5yXjApOmiiFJaEU/ytRh04wv0ORygCFs2rocUZOGjwhNIhNYs+1dvEAltmzfL7xCTNEZ6aCXeIYxW+/jNfRoBpOJ230Rs4FvftNEE2iBdlM5yDiuUYJH6IMWqIGT5OEImvS3/Z2F0+RgGPM4xwLiljboKvTGxi1TuEIXGpEKp6mDriLkJ4oQNXrFs/xm2GjMV2jnrEA9TrEOPWVh8waH0BltI7glBJMOjekxlZ8PUF+Gqe5IFTTgMwahPUW7oXZHXVEp9GKN4BM0NriRLUHjH5vqjsxAl5lgKs8rhCb5Z3+DdHsWbXsHe7bdjbCZw4nfNHkOHaQN7T2aUAxtfKG8xSr0cWlRR6Toj9KEKxiAnoq/eApn6cAfaCF9+qrhPCnIRsTHLfZ43g3RfG3n8GC5mgAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, check):
        
        commits = None
        
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
        
        def log():
            """
            This function provides a log of commits
            """
        
            log_msg = executor(["git", "log", "--oneline"])
        
            return log_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        commits = log()
        
        return commits


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Commit List"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("dee5789a-9fb9-4aba-9233-6db5aefae9b3")