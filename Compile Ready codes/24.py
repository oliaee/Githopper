"""Finishes the conflict resolve operation
    Inputs:
        resolve: Ends the merge operation (Button)
        abort: Aborts the merge operation (Button)
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
            "Conflict Manager", "Conflict", """Finishes the conflict resolve operation""", "Githopper", "Utility")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("c254d51d-d235-46a4-a0e2-1a7a63e50a1f")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "resolve", "resolve", "Ends the merge operation (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "abort", "abort", "Aborts the merge operation (Button)")
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
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHWSURBVEhLzda9L2RRHMbxs14jIQQbBEviJYRslixREIVQbbfK1WjRiLeIBPGSbLNLZ3UKhUro/BEaNEhsIhQU6w9Q2O9zZk5mcs3LuTOReJJP5v5+c8+9mXvPPXdMyAxgHX22eoMs4wUztsoiFdhFv61imYVOMGGrWIawgzJbeeQHdKAHtKgRzTzUn7RVJJ34B/W/q+GTHGxDg/6iGUrwF7TjDur9xAeEyh40+NBWxpSjDboUOtgJ9P0fZJxNtEY2X6UDG5HN8KmOfvqmKvrplRE8YcFW6bMK3ehBW3nkG3RtZVqNFFmE9nvGsBq+6YGmaaqTuIPf47MaiaI5fxxwhH3cwP2SJeRBKcAa3HfX0P4aFzyW2YLbMZUrFEPRNL1Fov2CTC2+BnyBLtEZtNM5ahCfelxC35+iGxoXPFbC5MI9ZDp4silYB3cSrV3eT7LWGg26QLr5rZPoHmj/cTV8UoQVNNgqfbQgaikvtNV7iu7Fb2hJTpQu/IpsZpYD6Nq61fQjNFMqEb+aakKESj60BGuwZsknKO6FM2UrY5qg94V6en+4BzFtxqBBWgIa1YhmDurHv9G0lD9C/VE1fFIKPeG9tool2TtZ/zZ0L0pslUVC/qsw5j+9LnlCUMbwHAAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, resolve, abort):
        
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
        
        def finish_merge(abort):
            """
            Finishes the merge process by continuing or aborting the oporation
            """
        
            if abort:
                try:
                    fm_msg = executor(["git","merge","--abort"])
                except subprocess.CalledProcessError as cpe_error:
                    fm_msg = cpe_error.output
                    fm_msg = str(fm_msg, "utf-8")
            else:
                try:
                    fm_msg = executor(["git","merge","--continue"])
                except subprocess.CalledProcessError as cpe_error:
                    fm_msg = cpe_error.output
                    fm_msg = str(fm_msg, "utf-8")
            
            return fm_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if resolve != abort:
            if resolve:
                r = finish_merge(False)
                if r != "" : r += "\n"
                r += "* Resolved conflicts will be implimented (check repository status for more info)"
            
            if abort:
                r = finish_merge(True)
                if r != "" : r += "\n"
                r = "The merge oporation will be aborted and file changes will be cancelled"
        
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the abort or resolve button to finish resolving the merge conflict\n"
        
        if resolve == True and abort == True:
            help += "\n* You can not resolve and abort the oporation at the sae time !"
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_24"]
        except:
            rsc.sticky["Githopper_24"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_24"] == None:
            rsc.sticky["Githopper_24"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_24"]
            rsc.sticky["Githopper_24"] = None
        
        return (report, help)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Conflict Manager"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("76c4d824-987e-41de-aa87-9b2ae17de0b1")