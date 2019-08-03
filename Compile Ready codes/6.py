"""Provides a text graph of commits including branches and merges
    Inputs:
        check: Refreshes the graph (Button)
    Output:
        graph: Text graph of commits"""

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
            "Branch Graph", "Graph", """Provides a text graph of commits including branches and merges""", "Githopper", "Status")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("79f504f6-2840-4e88-971c-159d9e8c360c")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "check", "check", "Refreshes the graph (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "graph", "graph", "Text graph of commits")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAG3SURBVEhLrdVNKARhHMfxUURSkqTk5eAikiKSg7xecXCguCiJIyWJUtxIHBwdcXByc1EKN5GIoigHDgp5fwvf38zO7tp27czu/OrTPs+08/xnn5dZI0ryfZ9OkodUqxk9SVjGOzaRjv8yjk+co1gXoqUaP2jGK1oQKWnQd/uwBz1Y1GTjEtvQzdOIlETsYB/36IWjlEGDT0FTpWmIlAzcYtHsOYzm/Qm5qIGKjUKFCxGaAwxZTWfRND2jyuwZRgO0kF94RCuCcwQ9gOPYBSrNnpUbjGAFmvPgeFJgAVe4w6AuBMV1AXsNSs1eIMdYtZp/cghXBSqghW0ze4Ho4IXbtmfQjnOUHFxjF9p+JbCzhXmr6U8/9DA6mI5SC93Q5PvsgZ3QAjrB+k6X2XOYFKxBN+pXZMKOCsxZTf/gnWbPZXQ631Bu9gLRGkygHRq8AzElC9qmWmw7jfiAzsMDYh5cCXcOLjCDdeiXxJVwBU6hN6cKzepCPLEL2Gugede0LEH7PRlxRX9/GrAAw9CC1sOzdEODbuAFdfAsRfjGJFRkAJ5GLzgNPAYV0on2PHrqE2hBE3TBfQzjF8EcZ9ipu9U2AAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, check):
        
        graph = None
        
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
        
        def graph():
        
            """
            This function provides an ANSI text graph of the local repository
            """
        
            graph_msg = executor(["git", "log", "--graph", "--oneline", "--decorate", "--all"])
        
            return graph_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        
        graph = graph()
        
        return graph


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Branch Graph"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("61b865a3-8f14-470b-a55e-a6b8288528b0")