"""Provides a status report of the local git repository
    Inputs:
        check: Refreshes the status (Button)
    Output:
        status: Status report of the local git repository"""

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
            "Check Status", "Status", """Provides a status report of the local git repository""", "Githopper", "Status")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("8695d84d-4069-47e9-a2f2-e0b007ce460c")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "check", "check", "Refreshes the status (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "status", "status", "Status report of the local git repository")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHqSURBVEhL3dXLSxVhHIfxMexiWVq6LcouJFjQBVK7QLQoyFqVtU7EjaAQEhH9B7VJoV0g2AVpH0FXU7GLi+i6ChdR0LZFW59n3jOHOTfOdA606Asf5sd5z8w78877vhP9d2mq02qUTRte4hM+1uELrqAkR7GEndiBLX9pKzxvGK9REjt4G8o4m9AOn6wa/7cW5hh+YgKDWIE4R7AYyqgTH+Djfs7gK+7AnMB33MBv7EWcdAeVshKtoayYs3gayugNekNZ2MFm3Mb9FO/wOMxNPEC6/RpMH2ZCGV+vO5SFHZzHL4zmjOA57sGcw0CRUzBnULWDC3gcynzs6G4o43e0H/tyrLfDZOqgH89Cmc9VTIYymoZTcSHHehwm0xBdxJNQ5jMGx7paMj3BSfzBK8zmjj9wC+YhnCHeuVw/znuT6Qka0QWnWOIANsDsgvM7zZVsMj2Bq9OZ4UpM2wPjJBgqchomUwfejS90qkhyEVdp+ndnl5PAZBqieuJKfhHKwg7c7N6FsmQv8qhLMI/g/lNuL3KI3LZXwZffgziHYUOSFmyEe4+sG2DWobhtDUwz/K64sudwCHG8oN+Dy9iNbWX4rbCtI/VbwpVsW3K8jm9Yj3wOYh7pL1Qt3sP14xZSNo6f39Zaef6/ShQtA8+Ln7H2/gKRAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, check):
        
        status = None
        
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
        
        def stat():
            """
            reports the status of the local repository
            """
            
            status_msg = executor(["git", "status"])
            
            return status_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        
        status = stat()
        
        
        return status


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Check Status"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("bcfa3c84-402a-4e22-a1be-8c94bacb9d20")